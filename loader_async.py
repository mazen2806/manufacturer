import asyncio
import logging

from constants import SITE_URL
from utils import write_data_to_file
from manufacturer_info_parser import ManufacturerInfoParser


async def main():
    try:
        parser = ManufacturerInfoParser()
        category_urls = await parser.get_category_urls(SITE_URL)
        model_urls = await parser.get_model_urls(category_urls)
        manufacturer_info = await parser.get_manufacturer_info(model_urls)
        await write_data_to_file(manufacturer_info)
    except Exception as exc:
        logging.exception(exc)


if __name__ == '__main__':
    print("Scraping started ...")
    asyncio.run(main())
    print("Scraping finished ...")
