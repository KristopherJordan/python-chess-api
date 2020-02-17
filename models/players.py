

class Player:

    def __init__(self, name, colour):
        self._name = name
        self._colour = colour
        # games

    def __repr__(self):
        return "%s" % self._name

    def get_colour(self):
        return self._colour

    def get_name(self):
        return self._name
