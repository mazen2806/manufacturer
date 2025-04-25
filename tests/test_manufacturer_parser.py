import pytest

from loader.constants import SITE_URL
from loader.manufacturer_info_parser import ManufacturerInfoParser


@pytest.mark.asyncio
async def test_fetch_data():
    parser = ManufacturerInfoParser()
    categories = await parser.get_category_urls(SITE_URL)
    assert len(categories) == 42
