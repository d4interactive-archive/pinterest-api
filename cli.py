from pin_py.pinterest.pinpy import PinPy
from pin_py.utils.config import access_token

if __name__ == "__main__":
    pin = PinPy()
    pins_list = pin.get_details_of_all_pins(access_token)
    boards = pin.get_all_boards_of_user(access_token)
    pass
    for pin_one in pins_list:
        print(pin.get_single_pin_details(pin_one,access_token))