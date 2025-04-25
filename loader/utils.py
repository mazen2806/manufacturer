import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from typing import List

from loader.constants import FILE_NAME, FILE_HEADERS


async def parse_page(url, class_name, receive_text=False) -> List:
    """
    Parses page by indicated url
    :param url:
    :param class_name:
    :param receive_text:
    :return:
    """
    values = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, ssl=False) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            container = soup.find_all(class_=class_name)

            if len(container) > 0:
                result = container[0].select('li > a')
                for r in result:
                    v = r.text if receive_text else r["href"]
                    values.append(v)

            return values


async def write_data_to_file(result):
    """
    Writes parsed data to csv file
    :param result:
    :return:
    """
    async with aiofiles.open(FILE_NAME, mode='w+') as f:
        await f.write(','.join(FILE_HEADERS) + '\n')

        line = ''
        for data in result:
            line += ','.join(data) + '\n'
        await f.write(line)
