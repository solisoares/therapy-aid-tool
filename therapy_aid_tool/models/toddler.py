class Toddler:
    def __init__(self, name: str) -> None:
        self.__name = name
        self.__birthdate = None

    def __repr__(self):
        return f"Toddler(name='{self.name}')"

    @property
    def name(self):
        return self.__name

    @property
    def birthdate(self):
        return self.__birthdate

    @name.setter
    def name(self, name):
        self.__name = name

    @birthdate.setter
    def birthdate(self, birthdate):
        self.__birthdate = birthdate
