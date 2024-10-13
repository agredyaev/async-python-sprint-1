from collections.abc import Generator

from pydantic import BaseModel, HttpUrl

from src.core.settings import settings as s
from src.helpers.get_json_data import from_json_file


class City(BaseModel):
    name: str
    url: HttpUrl


def generate_links() -> Generator[str, None, None]:
    links = from_json_file(s.inpt.links_path)
    for name, url in links.items():
        yield City(name=name, url=url).url.unicode_string()
