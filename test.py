from bs4 import BeautifulSoup
import aiohttp

# import re
import asyncio


# def getSize(num):
#     for unit in ("", "KB", "MB"):
#         if num < 1000.0:
#             return f"{num:3.1f} {unit}"
#         num /= 1000.0
#     return f"{num:.1f} GB"
#
#
# async def fetch(session, url):
#     async with session.head(url) as response:
#         return response.headers.get("Content-Length", 0)


async def getDownloadLinks(availableModels, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            rows = soup.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                if columns:
                    link = columns[0].a
                    if not link:
                        continue

                    print(columns)
                    size = columns[1].text.strip()
                    errorRate = columns[2].text.strip()
                    notes = columns[3].text.strip()
                    modelLicense = columns[4].text.strip()

                    availableModels[link.get_text()] = [
                        link.get("href"),
                        size,
                        errorRate,
                        notes,
                        modelLicense,
                    ]
            # return availableModels


#
# async def getDownloadLinksAsync(availableModels: dict, url: str):
#     links, sizes = await getDownloadLinks(url)
#     for link, size in zip(links, sizes):
#         availableModels[link.get_text()] = [link.get("href"), getSize(int(size))]


if __name__ == "__main__":
    availableModels = {}
    modelsUrl = "https://alphacephei.com/vosk/models"
    asyncio.run(getDownloadLinks(availableModels, modelsUrl))
    for model, data in availableModels.items():
        print(f"Name: {model.ljust(42)}   Data: {data}")  #   desc: {model[2]}")
