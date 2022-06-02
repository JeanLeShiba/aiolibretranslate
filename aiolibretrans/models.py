import aiohttp


class BaseClass:
    def __init__(self, json_response: dict):
        self._dict = json_response

    def __str__(self):
        return str(self._dict)

    def __dict__(self):
        return self._dict


class Translation(BaseClass):
    def __str__(self):
        return self._dict["translatedText"]

    def __repr__(self):
        return f"Translation('{self.__str__()}')"


class Detection(BaseClass):
    @property
    def confidence(self):
        """Confidence of the detection."""
        return self._dict['confidence']

    @property
    def language(self):
        """Language code (ISO 639)."""
        return self._dict['language']

    def __repr__(self):
        return f"Detection({self.__dict__()})"


class Language(BaseClass):
    @property
    def code(self):
        """Language code (ISO 639)."""
        return self._dict['code']

    @property
    def name(self):
        """Full language name."""
        return self._dict['name']

    def __repr__(self):
        return f"Language({self.__dict__()})"
