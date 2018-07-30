#!/usr/bin/env python3

from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from os import path
import OPi.GPIO as GPIO # to install "pip3 install --upgrade OPi.GPIO"
import sys
import os
import time
import yaml
import logging
import subprocess
import smbus
GPIO.setmode(GPIO.BOARD)

bus = smbus.SMBus(1)
address = 0x10

# Change working dir to the same dir as this script
os.chdir(sys.path[0])

class DataCollector:
    def __init__(self, influx_client, inputspins_yaml):
        self.influx_client = influx_client
        self.max_iterations = None  # run indefinitely by default

    def collect_and_store(self):
        t_utc = datetime.utcnow()
        t_str = t_utc.isoformat() + 'Z'
 
        save = False
        datas = dict()

		## inicio while :
        while:
            start_time = time.time()


            statusRF24 = bus.read_byte_data(address, 12)
            if statusRF24 != statusRF24old
                statusRF24old = statusRF24
                save = True
                RadioPacket = unpack('BcBll', statusRF24)
                datas['FromRadioId'] = RadioPacket[0]
                datas['DataType'] = RadioPacket[1]
                datas['InputNumber'] = RadioPacket[2]
                datas['RadioData'] = RadioPacket[3]
                datas['FailedTxCount'] = RadioPacket[4]

			
            datas['ReadTime'] =  time.time() - start_time

            if save:
                save = False
                json_body = [
                    {
                        'measurement': 'LocalInputsLog',
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
			## delay 10 ms between read inputs
            time.sleep(0.01)


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
