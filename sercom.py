#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Serial communicator written in python.
This module allows to communicate standalone with arduinos and other
devices that use a serial port to communicate with the host computer.
Author: Matthias Kesenheimer (m.kesenheimer@gmx.net)
Copyright: Copyright 2021, Matthias Kesenheimer
License: GPL
Version: 0.7
"""

import serial
import threading
import time
import argparse
import re

class listening(threading.Thread):
  """listening class capable of threading."""

  def __init__(self, ser, encoding="utf-8", outputhex=False):
    """class initializer"""
    self.__stopEvent = threading.Event()
    self.__ser = ser
    self.__encoding = encoding
    self.__outputhex = outputhex
    super().__init__()

  def read(self):
    """function to read data from the serial port"""
    data = str("")
    while self.__ser.in_waiting > 0:
      data += self.__ser.read(self.__ser.in_waiting).decode(self.__encoding)
    return data

  def run(self):
    """main thread"""
    while not self.__stopEvent.isSet():
      data = self.read()
      if self.__outputhex:
        for d in data:
          h = "{0:02x}".format(ord(d))
          if h == "0a": # line feed
            print()
          elif h == "0d": # carriage return
            continue
          else:
            print(h, end=' ')
      else:
        print(data, end='')
      time.sleep(0.1)

  def join(self, timeout=None):
    """set stop event and join within a given time period"""
    self.__stopEvent.set()
    print("stopping listening thread.")
    super().join(timeout)


class sending(threading.Thread):
  """writing class capable of threading."""

  def __init__(self, ser, encoding="utf-8", ending="\r\n"):
    """class initializer"""
    self.__stopEvent = threading.Event()
    self.__ser = ser
    self.__encoding = encoding
    self.__ending = ending
    super().__init__()

  def write(self, x):
    """function to write data to the serial port"""
    if self.__ending != "":
      x += self.__ending
    self.__ser.write(bytes(x, self.__encoding))

  def run(self):
    """main thread"""
    while not self.__stopEvent.isSet():
      data = input()
      self.write(data)

  def join(self, timeout=None):
    """set stop event and join within a given time period"""
    self.__stopEvent.set()
    print("stopping sending thread.")
    super().join(timeout)


if __name__ == "__main__":
  print(" ___  ____  ____   ___  _____  __  __ ")
  print("/ __)( ___)(  _ \ / __)(  _  )(  \/  )")
  print("\__ \ )__)  )   /( (__  )(_)(  )    ( ")
  print("(___/(____)(_)\_) \___)(_____)(_/\/\_)")
  print("Serial Communication program")
  print("Matthias Kesenheimer, 2021")

  parser = argparse.ArgumentParser(description="Connect to a serial port and send and receive messages. Exit program with ctrl+c.")
  parser.add_argument('port', metavar='SERIALPORT', type=str, nargs=1,
                      help='serial port to connect to')
  parser.add_argument('--baudrate', dest='baudrate', type=int, nargs=1, default=[19200],
                      help='sum the integers (default: find the max)')
  parser.add_argument('--timeout', dest='timeout', type=float, nargs=1, default=[0.1],
                      help='Timeout of the serial connection')
  parser.add_argument('--encoding', dest='encoding', type=str, nargs=1, default=["utf-8"],
                      help='Byte encoding to use: utf-8, ascii')
  parser.add_argument('--lineending', dest='lineending', type=str, nargs=1, default=["rn"],
                      help='Line ending to use: none [N], carriage return [r], new line [n], both [rn]')
  parser.add_argument('--hex', dest='outputhex', action='store_true',
                      help='Print the output as hex values')
  args = parser.parse_args()

  lineending = str("\r\n")
  if args.lineending[0] == "N":
    lineending = ""
  elif args.lineending[0] == "r":
    lineending = "\r"
  elif args.lineending[0] == "n":
    lineending = "\n"
  else:
    lineending = "\r\n"

  ser = serial.Serial(port=args.port[0], baudrate=args.baudrate[0], timeout=args.timeout[0])

  x = listening(ser, args.encoding[0], args.outputhex)
  y = sending(ser, args.encoding[0], lineending)
  y.start()
  x.start()
  
  try:
    while True:
      time.sleep(args.timeout[0])
  except (KeyboardInterrupt, SystemExit):
    x.join(args.timeout[0])
    y.join(args.timeout[0])
    print("\nGood bye.")