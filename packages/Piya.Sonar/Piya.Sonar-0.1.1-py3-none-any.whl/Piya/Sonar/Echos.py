# Copyright (c) 2020 Piya Pimchankam <piya.pimchankam@gmail.com>.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

# Python 2 & 3 print function compatibility
from __future__ import print_function

from time import time
from time import monotonic
from time import sleep
import Jetson.GPIO as GPIO
import threading
import numpy as np
from Piya.Sonar.IOEvent import  IOEvent

class Echos(object):
    # Use over 50ms measurement cycle. 
    def __init__(self, pairs_list_pin={}, mPerSecond = 343, max_distance=5, mIOMode=GPIO.BOARD, invert_echo_pin = False, callback=None):

        self._gpio_mode = mIOMode
        self._mPerSecond = mPerSecond
        self._invert_echo_pin = invert_echo_pin
        self._call_back_fn = callback
        # How frequently are we going to send out a ping (in milliseconds). 50ms would be 20 times a second.
        self._defaultUnit = 'cm'
        self._max_timeout = (max_distance / mPerSecond) #sec
        self._trigger_offset = 0.005         # > 2.3 ms
        self._pairs_list_pin = pairs_list_pin
        self._io_events = {}
        self._results = {}

        for echo,(trigger_pin, echo_pin)  in self._pairs_list_pin.items(): 
            print("Init %s trigger pin[%d], echo pin[%d]"%(echo, trigger_pin, echo_pin))
            self._io_events[echo] = IOEvent(trigger_pin, echo_pin, self._invert_echo_pin, self._max_timeout, self._echo_back, [echo])
            self._results[echo] = 0.0

        for echo,elem in self._io_events.items():
            print("start:",echo)
            elem.start()


    def __del__(self):
        self.stop()
        # Reset GPIO settings

        
    def _echo_back(self, value, args):
        self._results[args[0]] = self._valueToUnit(value[0], self._defaultUnit)
        
       

    """
    Convert echo time to distance unit of measure.
    """
    def _valueToUnit(self, value = 0.0, unit = 'cm'):
        if value > 0:
            if unit == 'mm':
                # return mm
                distance = (value * self._mPerSecond * 1000) / 2
            elif unit == 'cm':
                # return cm
                distance = (value * self._mPerSecond * 100) / 2
            elif unit == 'm':
                # return m
                distance = (value * self._mPerSecond) / 2
            elif unit == 'inch':
                # return inch
                distance = (value * self._mPerSecond * 39.3701) / 2
        else:
            distance = 0
            
        return distance

    def _echo_ready(self, echo):

        if echo in self._pairs_list_pin:
            if self._invert_echo_pin :
                return GPIO.input(self._pairs_list_pin[echo][1])

            return not GPIO.input(self._pairs_list_pin[echo][1])
        
        return False

    def send(self):
        for elem in self._io_events.values():
            #print("trig:", echo)
            elem.trig()
            elem.join()
    
    def wait(self):
        sleep(self._trigger_offset)

    def stop(self):
        for elem in self._io_events.values():
            elem.stop()
        
    def results(self):
        if self._call_back_fn != None:
            self._call_back_fn(self._results)
        
    def read_loop(self):
        try:
            while True:
                for elem in self._io_events.values():
                    #print("trig:", echo)
                    elem.trig()
                    elem.join()

                self.results()
                sleep(self._trigger_offset)
        finally:
            self.stop()
    
    @property
    def default_unit(self):
        return self._defaultUnit

    
    @default_unit.setter
    def default_unit(self, unit):
        unitPass = False
        if unit == 'mm':
            unitPass = True
        elif unit == 'cm':
            unitPass = True
        elif unit == 'm':
            unitPass = True
        elif unit == 'inch':
            unitPass = True

        if unitPass == True:
            self._defaultUnit = unit
        else:
            raise RuntimeError("Incorrect Unit for Default Unit")

