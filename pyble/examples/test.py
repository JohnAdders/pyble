#!/usr/bin/python3

"""Copyright (c) 2019, Douglas Otwell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import dbus

from pyble.advertisement import Advertisement
from pyble.service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 1000


class TestAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("Test Service")
        self.include_tx_power = True


class TestService(Service):
    TEST_SVC_UUID = "2f952b2a-db6c-42e8-a652-c572e6522bf8"

    def __init__(self, index):
        Service.__init__(self, index, self.TEST_SVC_UUID, True)
        self.add_characteristic(TestCharacteristic(self))
        # self.add_characteristic(UnitCharacteristic(self))


class TestCharacteristic(Characteristic):
    TEST_CHARACTERISTIC_UUID = "27e6ce9b-ac76-4b2d-bc1a-674a16728c8f"

    def __init__(self, service):
        self.notifying = False
        self._value = '1'

        Characteristic.__init__(
            self, self.TEST_CHARACTERISTIC_UUID,
            ["notify", "read", "write"], service)
        self.add_descriptor(TestDescriptor(self))

    def get_value(self):
        return dbus.ByteArray(self._value.encode())

    def notify(self):
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": self.get_value()}, [])
        print('notified')

    def StartNotify(self):
        print('StartNotify')
        if self.notifying:
            return

        self.notifying = True

        value = self.get_value()
        self.notify()

    def WriteValue(self, value, options):
        print('WriteValue')
        self._value = ''.join([str(v) for v in value])
        print('New value:', self._value)
        if self.notifying:
            self.notify()

    def StopNotify(self):
        print('StopNotify')
        self.notifying = False

    def ReadValue(self, options):
        print('ReadValue')
        value = self.get_value()
        print('value to return:', value)
        return value


class TestDescriptor(Descriptor):
    TEMP_DESCRIPTOR_UUID = "57a1524f-aab4-4162-911a-17d368696b15"
    TEMP_DESCRIPTOR_VALUE = "Test Value"

    def __init__(self, characteristic):
        Descriptor.__init__(
            self, self.TEMP_DESCRIPTOR_UUID,
            ["read"],
            characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.TEMP_DESCRIPTOR_VALUE

        for c in desc:
            value.append(dbus.Byte(c.encode()))

        return value


if __name__ == '__main__':
    app = Application()
    app.add_service(TestService(0))
    app.register()

    adv = TestAdvertisement(0)
    adv.register()

    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()
