# aioLibreTranslate

Python asynchronous bindings for LibreTranslate.

### Install the library

```
pip install git+https://github.com/JeanLeShiba/aioLibreTranslate
```

### Quickstart/Example of usage

Code example (not representative) :

```python
import asyncio
from aiolibretrans import LibreTranslate, URLS


async def main():
    async with LibreTranslate(target="it", url=URLS["pussthecat.org"]) as translator:
        tasks = []
        for text in ["Ayo, I got a pizza here !", "Comment ça va ?", "You good ?"]:
            tasks.append(translator.translate(text))
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)


asyncio.run(main())
```

Output :

```
Ayo, ho una pizza qui!
Come stai?
Stai bene?
```

### Wiki

[Click here to jump into the wiki.](https://github.com/JeanLeShiba/aioLibreTranslate/wiki)
