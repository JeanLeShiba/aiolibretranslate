import aiohttp
from typing import List
try:
    from orjson import loads, dumps
except ImportError:
    from json import loads, dumps

from .exceptions import (
    LengthExceeded,
    TextEmpty,
    SameSourceTarget,
    TooManyRequests,
    RequestError,
    BadRequest
)
from .constants import *
from .models import Detection, Language, Translation


def is_input_valid(text: str, limit: int = 5000) -> bool:
    """Checks if the text is standarts or not.

    Args:
        text (str): Source text.
        limit (int, optional): Limit of characters. Defaults to 5000.

    Returns:
        bool
    """
    if not isinstance(text, str):
        raise ValueError(f"Text must be a string not '{type(text)}'.")
    elif len(text) > limit:
        raise LengthExceeded(
            f"Maximum length exceeded : {len(text)} (text) --> {limit} (limit).")
    elif text == "":
        raise TextEmpty("The text is empty.")
    return True


async def check_response(response: aiohttp.ClientResponse) -> bool:
    """Checks the response.

    Args:
        response (aiohttp.ClientResponse): The client reponse.

    Raises:
        TooManyRequests: Too many requests were made (error 429).
        RequestError: Failed trying to make a request call (error 200).

    Returns:
        bool
    """
    if response.status == 400:
        error = (await response.json(loads=loads))["error"]
        raise BadRequest(error)
    elif response.status == 429:
        raise TooManyRequests(
            "You made too many requests.")
    elif response.status != 200:
        raise RequestError(
            "Error while trying to make a request call to the API, try again and check your connexion.")
    return True


class LibreTranslate:
    """Wrapper class for the LibreTranslate API.

    Args:
        source (str, optional): Source language. Defaults to "auto".
        target (str, optional): Target language. Defaults to "en".
        session (aiohttp.ClientSession, optional): the aiohttp session. Defaults to None.
        url (str, optional): Your server's host url. Defaults to URLS["argosopentech.com"].
        api_key (str, optional): Your api token, if you have one. Defaults to None.

    Raises:
        SameSourceTarget: Raised when the source and target are the same

    Methods:
        close() -> Coroutine : Closes the aiohttp session.
        translate(text:str) -> Coroutine : Translates text.
        detect(text:str) -> Coroutine : Detects the language(s) of a text.
        get_languages() -> Coroutine : Retrieve list of supported languages.
    """

    def __init__(
        self,
        source: str = "auto",
        target: str = "en",
        session: aiohttp.ClientSession = None,
        url: str = URLS["argosopentech.com"],
        api_key: str = None,
        **kwargs
    ):
        self.source = source
        self.target = target
        if source == target:
            raise SameSourceTarget(
                f"The source and the target cant be the same : '{source}' (source) --> '{target}' (target)")
        self.session = session if session else aiohttp.ClientSession(
            headers={"Content-Type": "application/json"})
        self.url = url
        self.api_key = api_key
        self.kwargs = kwargs

    async def close(self) -> None:
        """Closes the aiohttp session."""
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def translate(self, text: str) -> Translation:
        """Translates text.

        Args:
            text (str): The text you want to translate.

        Returns:
            str: Translated text.
        """
        if is_input_valid(text):
            params = {
                "source": self.source,
                "target": self.target,
                "q": text,
            }
            if self.api_key:
                params["api_key"] = self.api_key
            async with self.session.post(url=self.url+"translate", data=dumps(params), **self.kwargs) as response:
                if await check_response(response):
                    return Translation(await response.json(loads=loads))

    async def detect(self, text: str) -> List[Detection]:
        """Detects the language(s) of a text.

        Args:
            text (str): Text.

        Returns:
            List[Detection]: list of `aiolibretrans.Detection`.
        """
        if is_input_valid(text):
            params = {
                "q": text,
            }
            if self.api_key:
                params["api_key"] = self.api_key
            async with self.session.post(url=self.url+"detect", data=dumps(params), **self.kwargs) as response:
                if await check_response(response):
                    return [
                        Detection(detection_dict)
                        for detection_dict in await response.json(loads=loads)
                    ]

    async def get_languages(self) -> List[Language]:
        """Retrieve list of supported languages.

        Returns:
            List[Language]: List of `aiolibretrans.Language`.
        """
        async with self.session.post(url=self.url+"languages", data=dumps({"api_key": self.api_key}) if self.api_key else None, **self.kwargs) as response:
            if await check_response(response):
                return [
                    Language(language_dict)
                    for language_dict in await response.json(loads=loads)
                ]
