#Copyright (c) 2011, 2012, Ian Daniher
#Copyright (c) 2012, Tony Forster, Walter Bender
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import os
sys.path.append(os.path.dirname(__file__))
import usb.core
import logging

TILT_FORWARD = 0
TILT_LEFT = 1
TILT_RIGHT = 2
TILT_BACK = 3
NO_TILT = -1


class WeDo:
    def __init__(self):
        """Find a USB device with the VID and PID of the Lego
        WeDo. If the HID kernel driver is active, detatch
        it."""
        self.dev = usb.core.find(idVendor=0x0694, idProduct=0x0003)
        if self.dev is None:
                logging.debug("No Lego WeDo found")
        else:
            if self.dev.is_kernel_driver_active(0):
                try:
                    self.dev.detach_kernel_driver(0)
                except usb.core.USBError as e:
                    sys.exit("Could not detatch kernel driver: %s" % str(e))
        self.valMotorA = 0
        self.valMotorB = 0

    def getRawData(self):
        """Read 64 bytes from the WeDo's endpoint, but only
        return the last eight."""
        self.endpoint = self.dev[0][(0,0)][0]
        data = list(self.endpoint.read(64)[-8:])
        return data

    def processMotorValues(self, value):
        """Check to make sure motor values are sane."""
        retValue = int(value)
        if 0 < value < 101:
            retValue += 27 
        elif -101 < value < 0:
            retValue -= 27
        elif value == 0:
            retValue = 0
        return retValue
    
    def setMotors(self, valMotorA, valMotorB):
        """Arguments should be in form of a number between 0
        and 100, positive or negative. Magic numbers used for
        the ctrl_transfer derived from sniffing USB coms."""
        if self.dev is None:
            return
        self.valMotorA = self.processMotorValues(valMotorA)
        self.valMotorB = self.processMotorValues(valMotorB)
        data = [64, self.valMotorA&0xFF,
            self.valMotorB&0xFF, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.dev.ctrl_transfer(bmRequestType = 0x21, bRequest = 0x09,
                       wValue = 0x0200, wIndex = 0,
                       data_or_wLength = data)

    def getData(self):
        """Sensor data is contained in the 2nd and 4th byte,
        with sensor IDs being contained in the 3rd and 5th
        byte respectively."""
        rawData = self.getRawData()
        sensorData = {rawData[3]: rawData[2], rawData[5]: rawData[4]}
        return sensorData

    def processTilt(self, v):
        """Use a series of elif/value-checks to process the
        tilt sensor data."""
        if v in [24, 25, 26, 27]:
            return TILT_BACK
        elif v in [73, 74, 75, 76]:
            return TILT_RIGHT
        elif v in [175, 176, 177, 178, 179, 180]:
            return TILT_FORWARD
        elif v in [229, 230]:
            return TILT_LEFT
        else:
            return NO_TILT

    def interpretData(self):
        """This function contains all the magic-number
        sensor/actuator IDs. It returns a list containing one
        or two tuples of the form (name, value)."""
        data = self.getData()
        response = []
        for num in data.keys():
            if num in [0, 1, 2]:
                response.append(('motor', 1))
            elif num in [176, 177, 178, 179]: 
                response.append(('distance', data[num]-69))
            elif num in [38, 39]: 
                response.append(('tilt', self.processTilt(
                            data[num])))
            elif num in [238, 239]:
                response.append(('motor', 0))
            elif num in [228, 230]: 
                response.append(('normal', 1))
        return response

    def getTilt(self):
        if self.dev is None:
            return NO_TILT
        data = self.getData()
        for num in data.keys():
            if num in [38, 39]:
                return self.processTilt(data[num])
        return NO_TILT

    def getDistance(self):
        if self.dev is None:
            return 0
        data = self.getData()
        for num in data.keys():
            if num in [176, 177, 178, 179]:
                return data[num] - 69
        return 0

    def setMotorA(self, valMotorA):
        self.setMotors(valMotorA, self.valMotorB)

    def setMotorB(self, valMotorB):
        self.setMotors(self.valMotorA, valMotorB)

    def getMotorA(self):
        if self.dev is None:
            return 0
        return self.valMotorA

    def getMotorB(self):
        if self.dev is None:
            return 0
        return self.valMotorB