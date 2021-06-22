import toml


class Misc:
    """
    This entity holds all the raw meta data conveniently as a dict
    """

    def __init__(self, toml_string):
        self.data = self.get_toml(toml_string)

    def get_toml(self, toml_string):
        return toml.loads(toml_string)