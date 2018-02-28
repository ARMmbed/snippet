import unittest


class Test(unittest.TestCase):
    def test(self):
        # /// this is an example: print devices
        devices = self.connect_api.list_connected_devices()
        for device in devices:
            print(device.name)
        # end of example
        self.assertGreaterEqual(len(devices), 1)
