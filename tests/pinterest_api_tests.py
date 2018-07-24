import unittest
from pinterest.pinpy import PinPy


def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


access_token = "AeSNbHAlqm44R2u748yqrgJiZWjzFKi37tKqdLdD1NITIuAxeQAAAAA"


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

# if __name__ == '__main__':
#     unittest.main()
