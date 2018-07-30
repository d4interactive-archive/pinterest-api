import unittest
from pin_py.pinterest.pinpy import PinPy
from pin_py.utils.config import access_token

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False





class MyTestCase(unittest.TestCase):

    def test_working(self):
        pinPy = PinPy()
        user = pinPy.authorize(access_token)
        if user is not None:
            if "data" in user:
                self.assertEqual("Stephen", user["data"]["first_name"])
            else:
                self.fail("object was corrupt")
        else:
            self.fail("Null object is received")

    def test_getting_pins(self):
        pinPy = PinPy()
        pins = pinPy.get_details_of_all_pins(access_token)
        if pins is not None:
            for pin in pins:
                if RepresentsInt(pin):
                    pass;
                else:
                    self.fail("pins are corrupt")
            self.assertEqual(True, True);
        else:
            self.fail("Null object is received")

    def test_fail(self):
        self.fail("I am failed")