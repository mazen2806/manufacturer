import asyncio
from typing import List

from constants import DOMAIN_URL
from utils import parse_page


class ManufacturerInfoParser:
    async def get_category_urls(self, load_url: str) -> List:
        """
        Returns all categories on the page
        :param load_url: page url with all categories
        :return:
        """
        tasks = []
        manufacturer_result = await parse_page(load_url, "allmakes")
        for manufacturer in manufacturer_result:
            url = f"{DOMAIN_URL}{manufacturer}"
            tasks.append(parse_page(url, "allcategories"))

        category_result = await asyncio.gather(*tasks)
        return await self._get_values(category_result)

    async def get_model_urls(self, category_urls: List) -> List:
        """
        Returns all models for each category
        :param category_urls: category urls
        :return:
        """
        tasks = []
        for category in category_urls:
            model_url = f"{DOMAIN_URL}{category}"
            tasks.append(parse_page(model_url, "allmodels"))

        models_result = await asyncio.gather(*tasks)
        return await self._get_values(models_result)

    async def get_manufacturer_info(self, model_urls: List) -> List:
        """
        Returns detailed info for each manufacturer.
        This info is ready to be saved to the file
        :param model_urls: model urls
        :return:
        """
        manufacturer_details = []
        for model in model_urls:
            parts_url = f"{DOMAIN_URL}{model}"
            parts_result = await parse_page(parts_url, "allparts", receive_text=True)

            parts = await self._get_model_parts(parts_result)
            lst = await self._get_manufacturer_details(model, parts)
            manufacturer_details.extend(lst)

        return manufacturer_details

    @staticmethod
    async def _get_manufacturer_details(model, parts):
        """
        Collect data to write to csv file
        :param model: model name
        :param parts: parts and part category for each model
        :return:
        """
        url_parts = model.split('/')
        lst = []
        for part in parts:
            lst.append((url_parts[3], url_parts[4], url_parts[5], part[0], part[1]))

        return lst

    @staticmethod
    async def _get_model_parts(data):
        """
        Parses model part data
        :param data:
        :return: parsed part and part category
        """
        parts = []
        for name in data:
            names = name.split(" - ")
            part = names[0]
            part_category = names[1] if len(names) > 1 else ''
            parts.append((part, part_category))
        return parts

    @staticmethod
    async def _get_values(values_result):
        """
        Get values from coroutine result
        :param values_result:
        :return:
        """
        values = []
        for v in values_result:
            values.extend(v)
        return values
