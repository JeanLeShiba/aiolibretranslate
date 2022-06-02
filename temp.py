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
