import nut2


class UndefinedError(Exception):
    pass


class WebNUT(object):
    def __init__(self, server='127.0.0.1', port=3493, username=None, password=None):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def get_ups_list(self):
        try:
            with nut2.PyNUTClient(host=self.server, port=self.port,
                    login=self.username, password=self.password) as client:
                ups_dict = client.list_ups()
                ups_list = dict()
                for ups in ups_dict:
                    try:
                        ups_vars = client.list_vars(ups)
                        ups_list[ups] = {
                        'ups': ups,
                        'description': client.description(ups),
                        'status': self._get_ups_status(ups_vars),
                        'battery': ups_vars['battery.charge'],
                        'load': ups_vars['ups.load'],
                        'batterylow': ups_vars['battery.charge.low'],
                    }
                    except (nut2.PyNUTError, KeyError):
                        continue                    

                return ups_list
        except nut2.PyNUTError:
            return dict()
        except AttributeError:
            print("ERROR: Is the NUT Server even running?....")
            return dict()

    def get_ups_name(self, ups):
        try:
            with nut2.PyNUTClient(host=self.server, port=self.port,
                    login=self.username, password=self.password) as client:
                return client.list_ups()[ups]
        except nut2.PyNUTError:
            return dict()

    def get_ups_vars(self, ups):
        try:
            with nut2.PyNUTClient(host=self.server, port=self.port,
                    login=self.username, password=self.password) as client:
                ups_vars = client.list_vars(ups)
                for var in ups_vars:
                    ups_vars[var] = (ups_vars[var],
                            client.var_description(ups, var))
                return (ups_vars, self._get_ups_status(ups_vars))
        except nut2.PyNUTError:
            raise UndefinedError

    def _get_ups_status(self, ups_vars):
        return ups_vars['ups.status']
