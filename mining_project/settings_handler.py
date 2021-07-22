"""
Handel the settings file

"""


class Configuration(dict):
    """
    Represents the settings file as a dictionary
    """
    def __init__(self, *args):
        """
        Initialize class
        :param args: a dictionary
        """
        super(Configuration, self).__init__()

        for arg in args:
            for key, value in arg.items():
                value = Configuration(value) if isinstance(value, dict) else value
                self.__setattr__(key, value)

    def __getattr__(self, attr):
        """
        Get item
        :param attr:
        :return:
        """
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Configuration, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Configuration, self).__delitem__(key)
        del self.__dict__[key]

