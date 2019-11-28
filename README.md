# Master application
The Master app runs asynchronously 5 slave applications and wait until all applications are finished with zero exit code in case it doesn't succeed it retries at least 5 times.

## Configuration file
The file with name master.ini contains the configurations necessary to run the application

```ini
[DEFAULT]
cmd = python slave.py -d 
```

the cmd configuration variable will be used on the master.py app in order to trigger a shell command to create the slave application.

```py
def requestFromSlave(self):
        config = configparser.ConfigParser()
        config.read('master.ini')
        cmd = config['DEFAULT']['cmd']
````

## Run
To execute the application you should execute the following command after configuration is correctly set:

```bash
python master.py
```

## Test

To execute the test run the following command:
```bash
python test_master.py
```


# Slave application
The Slave app sends a GET request to https://postman-echo.com/delay/<seconds> where <seconds> is a random number from 1 to 5, check the response status and exit with zero code if postman-echo responded with 200 status code, or exit with 1 code if status code is not equal 200. The Slave app exits with code 2 in case of any network errors.


## Configuration file
The file with name slave.ini contains the configurations necessary to run the application

```ini
[DEFAULT]
BaseUrl = https://postman-echo.com/delay/
```

the cmd configuration variable will be used on the slave.py app in order to set the variable baseUrl

```py
def postmanEchoRequest(self):
        config = configparser.ConfigParser()
        config.read('slave.ini')
        baseUrl = config['DEFAULT']['BaseUrl']
```

## Run
To execute the application you should execute the following command after configuration is correctly set:

```bash
python slave.py -d value
```

## Test

To execute the test run the following command:
```bash
python test_slave.py
```
