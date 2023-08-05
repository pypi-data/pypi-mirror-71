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
from time import perf_counter
import Jetson.GPIO as GPIO
from threading import Thread, Lock, Event
import numpy as np

_INIT = 0
_START_TIME = 1
_END_TIME = 2

class IOEvent(Thread):
    def __init__(self, trigger_pin, echo_pin , invert_echo_pin = False, max_timeout = 10, callback = None, args=[] ):
        Thread.__init__(self)
        self._stopped = Event()
        self._startSignal = Event()
        self._oneRunFinished = Event()

        self._process = _INIT

        self._echo_pin = echo_pin
        self._trigger_pin = trigger_pin
        self._invert_echo_pin = invert_echo_pin
        self._echo_times = np.array([0.0, 0.0])
        self._time_diff = 0.0
        self._response_after_trig_timeout = 0.005   #ms
        self._max_timeout = self._response_after_trig_timeout + max_timeout

        self._call_back_fn = callback
        self._call_back_args = args

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._echo_pin, GPIO.IN)
        GPIO.setup(self._trigger_pin, GPIO.OUT, initial=GPIO.HIGH)
        
    def __del__(self):
        self.stop()
        # Reset GPIO settings

    def stop(self):
        self._startSignal.set()
        self._oneRunFinished.set()
        self._stopped.set()


    def run(self):


        while not self._stopped.is_set():
            #Wait trigger
            self._startSignal.wait()
            self._startSignal.clear()

            self._process = _START_TIME
            check_value = False
            #old_value = False

            if self._invert_echo_pin :
                check_value = True
                #old_value = True

            start_time =  monotonic()


            while not self._oneRunFinished.is_set():

                value = GPIO.input(self._echo_pin)
                time_elapsed = monotonic() - start_time

                if self._process == _START_TIME:
                    if value == (not check_value):
                        self._echo_times[0] =  monotonic()
                        start_time = self._echo_times[0]
                        self._process = _END_TIME
                        
                    elif  time_elapsed > self._response_after_trig_timeout:
                        #print("After trig timeout %f > %f"% (time_elapsed, self._response_after_trig_timeout))
                        self._oneRunFinished.set()
                        break
                elif self._process == _END_TIME:
                    if value == check_value:
                        self._echo_times[1] =  monotonic()
                        self._time_diff = np.diff(self._echo_times)
                        if self._call_back_fn!= None:
                            self._call_back_fn(self._time_diff,self._call_back_args)

                        self._oneRunFinished.set()
                        self._process = _INIT
                        break

                    elif  time_elapsed > self._max_timeout:
                        #print("Max timeoue %f > %f"% (time_elapsed, self._max_timeout))
                        self._oneRunFinished.set()
                        break
                
                if self._stopped.is_set():
                    self._oneRunFinished.set()
                    break



    def trig(self):
        # Trigger 10us pulse for initial sensor cycling.
        #print("Trig")
        self._echo_times[0] = 0.0
        self._echo_times[1] = 0.0
        self._time_diff = 0.0
        GPIO.output(self._trigger_pin, True)
        sleep(0.00001)
        GPIO.output(self._trigger_pin, False)
        self._startSignal.set()
        

    def join(self):
        """ This join will only wait for one single run (target functioncall) to be finished"""
        self._oneRunFinished.wait()
        self._oneRunFinished.clear()






class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.5):
            print("my thread")
            # call a function




#