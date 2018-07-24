# Author Hassan Alvi
# Creation date : 20th July 2018

from utils.http import Requests



try:
    import simplejson as json
except ImportError:
    import json



class PinPy:

    pinterest_url = "https://api.pinterest.com/"

    def __init__(self):
        self.request = Requests()
        self.all_pins = []
        pass

    def authorize(self, user_auth_token):

        query = "v1/me?access_token={}".format(user_auth_token)
        request = self.request.get(PinPy.pinterest_url + query)
        if request.status_code != 200:
            return None
        json_object = json.loads(request.text)
        # authorize user and if he authorizes, it returns a User Object
        # if he fails to authorize return null
        return json_object

    # it returns a dict of data about pin
    # in data attribute there is creator of pin, media type of pin
    # created_time of pin, board of pin, and analytics of its likes and comments

    def get_single_pin_details(self, pin_id, access_token):
        if pin_id is None or pin_id == '' or access_token is None or access_token == '':
            return ' pin_id or access_token is wrong'

        pinterest_url = 'https://api.pinterest.com/v1/pins/{0}/?access_token={1}&fields=counts,board,creator,' \
                        'created_at,media'.format(pin_id, access_token)
        request = self.request.get(pinterest_url)
        if request.status_code != 200:
            json_object = json.loads(request.text)
            error = 'Status code is not 200 it is ' + str(request.status_code) + ' ' + json_object['message']
            return error, None

        json_object = json.loads(request.text)

        if 'data' not in json_object:
            return json_object['message'], None

        return json_object

    # Return the array of Pins, these are just ids of PINS and if you require specific detail of sme pin you need to
    # call get_details_of_all_pins and pass that pin ID
    def get_details_of_all_pins(self, user_auth_token):

        query = "v1/me/pins?access_token={}".format(user_auth_token)
        url = PinPy.pinterest_url + query

        while url is not None:
            request = self.request.get(url)
            if request.status_code != 200:
                return None

            json_object = json.loads(request.text)
            if "data" in json_object:
                for pin in json_object["data"]:
                    self.all_pins.append(pin["id"])

            if "page" in json_object:
                url = json_object["page"]["next"]
                # url = None  # JUST FOR DEBUGGINJ
            else:
                url = None

        return self.all_pins

    # return a dict in which array of boards is embedded.
    # Typical board has following attributes URL, ID, NAME
    def get_all_boards_of_user(self, user_auth_token):
        query = "v1/me/boards?access_token={}".format(user_auth_token)
        request = self.request.get(PinPy.pinterest_url + query)
        if request.status_code != 200:
            return None
        json_object = json.loads(request.text)
        return json_object





if __name__ == "__main__":
    pin = PinPy()
    print(pin.authorize("AeSNbHAlqm44R2u748yqrgJiZWjzFKi37tKqdLdD1NITIuAxeQAAAAA"))