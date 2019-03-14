# nrf24-Logger-OrangeZero
Log nrf24 devices with nfrlite arduino librarie on a Orange Pi zero and plot graphs of your data.
Its been verified to work with a orange pi zero with a Attiny gateway into nrflite network vía i2c comunication (coming soon PCB and sketch). Used second I2C port in the Orange Pi Zero. (It is possible to change it for another or in case of using a raspberry emulate i2c operation in other pins.)

### Requirements

#### Hardware

* Orange Pi Zero
* Attiny gateway I2C (coming soon PCB and sketch) or other module DIY

#### Software

* Armbian
* Python 3.4 and PIP3
* python3-smbus
* [InfluxDB](https://docs.influxdata.com/influxdb/v1.3/)
* [Grafana](http://docs.grafana.org/)

### Prerequisite

### Installation
#### Install InfluxDB*

##### Step-by-step instructions
* Add the InfluxData repository
    ```sh
    $ curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
    $ source /etc/os-release
    $ test $VERSION_ID = "9" && echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
    ```
* Download and install
    ```sh
    $ sudo apt-get update && sudo apt-get install influxdb
    ```
* Start the influxdb service
    ```sh
    $ sudo service influxdb start
    ```
* Create the database
    ```sh
    $ influx
    CREATE DATABASE db_nrf24
    exit
    ```
[*source](https://docs.influxdata.com/influxdb/v1.3/introduction/installation/)

#### Install Grafana*

##### Step-by-step instructions
* Add APT Repository
    ```sh
    $ echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
    ```
* Add Bintray key
    ```sh
    $ curl https://packages.grafana.com/gpg.key | sudo apt-key add -
    ```
* Now install
    ```sh
    $ sudo apt-get update && sudo apt-get install grafana
    ```
* Start the service using systemd:
    ```sh
    $ sudo systemctl daemon-reload
    $ sudo systemctl start grafana-server
    $ systemctl status grafana-server
    ```
* Enable the systemd service so that Grafana starts at boot.
    ```sh
    $ sudo systemctl enable grafana-server.service
    ```
* Go to http://localhost:3000 and login using admin / admin (remember to change password)
[*source](http://docs.grafana.org/installation/debian/)

#### Install nrf24-Logger-OrangeZero:
* Download and install from Github and install pip3
    ```sh
    $ git clone https://github.com/GuillermoElectrico/nrf24-Logger-OrangeZero.git
	$ sudo apt-get install python3-pip
    ```
* Run setup script (must be executed as root (sudo) if the application needs to be started from rc.local, see below)
    ```sh
    $ cd nrf24-Logger-OrangeZero
	$ sudo apt-get install python3-smbus
    $ sudo python3 setup.py install
    ```    
* Make script file executable
    ```sh
    $ chmod 777 read_nrflite_orangezero.py
	$ chmod 777 setup_nrflite_orangezero.py
    ```
* Edit setup_nrflite_orangezero.py to match your configuration and launch (if necessary to configure attiny)
    ```sh
    ./setup_nrflite_orangezero.py
    ```
* Test the configuration by running:
    ```sh
    ./read_nrflite_orangezero.py
    ./read_nrflite_orangezero.py --help # Shows you all available parameters
    ```
* To run the python script at system startup. Add to following lines to the end of /etc/rc.local but before exit:
    ```sh
    # Start nrf24 Logger
    /home/pi/nrf24-Logger-OrangeZero/read_nrflite_orangezero.py > /var/log/nrflite-logger.log &
    ```
    Log with potential errors are found in /var/log/nrflite-logger.log
