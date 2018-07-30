# PinPy
Python wrapper for the Pinterest's API

#What it offers
Basically its just a wrapper on Pinterest API to make things easy for projects which use pinterest's API.
Right now It only offers wrapper on few major things like 


- [ ]    General information about user who's authentication or access token is entered
- [ ]    Get all boards of user
- [ ]    Get all Pins of user [IDs of pins]
- [ ]    Using these Pin ids to get further information about specific Pin


#How to use it

install it using pip

    pip install pin-py

usage

    from pin_py.pinterest.pinpy import PinPy;

    pin = PinPy()
    pins_list = pin.get_details_of_all_pins("access_token");

    for pin_one in pins_list:
        print(pin.get_single_pin_details(pin_one,"access_token"))