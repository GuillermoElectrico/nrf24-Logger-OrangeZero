#!/usr/bin/env python3

from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from struct import unpack
from os import path
import sys
import os
import time
import yaml
import logging
import subprocess
from smbus2 import SMBus

bus = SMBus(1)  # Puerto i2c-1 auxiliar de la Orange Pi Zero H2
address = 0x05        # Dirección por defecto esclavo 10 en decimal

# Change working dir to the same dir as this script
os.chdir(sys.path[0])

class DataCollector:
    def __init__(self, influx_client):
        self.influx_client = influx_client
        self.max_iterations = None  # run indefinitely by default

    def collect_and_store(self):
        t_utc = datetime.utcnow()
        t_str = t_utc.isoformat() + 'Z'

        save = False
        datas = dict()
        statusRF24old = 0

		## inicio while :
        while (1):
		
            datas[0] = dict()
			
 ##           try:
            start_time = time.time()

            statusRF24 = bus.read_i2c_block_data(address,0,15)

            if statusRF24 != statusRF24old:
                statusRF24old = statusRF24
                save = True
                datas[0]['FromRadioId'] = statusRF24[0]
                datas[0]['DataType'] = chr(statusRF24[1])
                datas[0]['InputNumber'] = statusRF24[2]
                datas[0]['RadioDataLong'] = (statusRF24[3] <<24) + (statusRF24[4] <<16) + (statusRF24[5] <<8) + statusRF24[6];
                datas[0]['RadioDataFloat'] = float((statusRF24[8] <<24) + (statusRF24[9] <<16) + (statusRF24[10] <<8) + statusRF24[11]);
                datas[0]['FailedTxCount'] = (statusRF24[11] <<24) + (statusRF24[12] <<16) + (statusRF24[13] <<8) + statusRF24[14];
			
            datas[0]['ReadTime'] =  time.time() - start_time

            if save:
                save = False
                json_body = [
                    {
                        'measurement': 'nrfliteLog',
                        'tags': {
                            'id': nrflite_id,
                        },
                        'time': t_str,
                        'fields': datas[nrflite_id]
                    }
                    for nrflite_id in datas
                ]
                if len(json_body) > 0:
                    try:
                        self.influx_client.write_points(json_body)
                        log.info(t_str + ' Data written for %d inputs.' % len(json_body))
                    except Exception as e:
                        log.error('Data not written!')
                        log.error(e)
                        raise
                else:
                    log.warning(t_str, 'No data sent.')
##            except:
##                log.error('Remote not found!')
##                pass
			## delay 100 ms between read inputs
            time.sleep(0.1)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--log', default='CRITICAL',
                        help='Log levels, DEBUG, INFO, WARNING, ERROR or CRITICAL')
    parser.add_argument('--logfile', default='',
                        help='Specify log file, if not specified the log is streamed to console')
    args = parser.parse_args()
    loglevel = args.log.upper()
    logfile = args.logfile

    # Setup logging
    log = logging.getLogger('nrflite-logger')
    log.setLevel(getattr(logging, loglevel))

    if logfile:
        loghandle = logging.FileHandler(logfile, 'w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        loghandle.setFormatter(formatter)
    else:
        loghandle = logging.StreamHandler()

    log.addHandler(loghandle)

    log.info('Started app')

    # Create the InfluxDB object
    influx_config = yaml.load(open('influx_config.yml'))
    client = InfluxDBClient(influx_config['host'],
                            influx_config['port'],
                            influx_config['user'],
                            influx_config['password'],
                            influx_config['dbname'])

    collector = DataCollector(influx_client=client)

    collector.collect_and_store()
