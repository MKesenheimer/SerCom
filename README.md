![Screenshot](https://raw.githubusercontent.com/MKesenheimer/SerCom/main/Screenshot.png)

# SerCom
Standalone program to interface serial communications with Arduinos and other peripherals.

## Prerequisites
```
python -m pip install -r requirements.txt
```

## Usage
This program can be used similar to the serial monitor of the Arduino IDE.

```
usage: sercom [-h] [--baudrate BAUDRATE] [--timeout TIMEOUT] [--encoding ENCODING] [--lineending LINEENDING] [--hex]
              SERIALPORT

Connect to a serial port and send and receive messages. Exit program with ctrl+c.

positional arguments:
  SERIALPORT            serial port to connect to

optional arguments:
  -h, --help            show this help message and exit
  --baudrate BAUDRATE   sum the integers (default: find the max)
  --timeout TIMEOUT     Timeout of the serial connection
  --encoding ENCODING   Byte encoding to use: utf-8, ascii
  --lineending LINEENDING
                        Line ending to use: none [N], carriage return [r], new line [n], both [rn]
  --hex                 Print the output as hex values
```

## Example
```
sercom /dev/tty.wchusbserial1420 --baudrate 19200
```

