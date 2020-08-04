import requests

from typing import Tuple, List
from bs4 import BeautifulSoup


def _text_to_tuple(s: str) -> Tuple[str, int]:
    split_data = s.replace("(", "").replace(")", "").split(" ")
    return " ".join(split_data[:-1]), int(split_data[-1])


def get_data(uri: str, requests_module) -> List[Tuple[str, int]]:
    html = requests_module.get(uri).text

    soup = BeautifulSoup(html, "html.parser")
    ps = soup.find("div", "data_grid_box").find_all("p")
    return [_text_to_tuple(p.get_text()) for p in ps]


def main():
    uri = "https://www.basketball-reference.com/friv/high_schools.fcgi"
    data = get_data(uri, requests)
    assert len(data) == 51


if __name__ == "__main__":
    main()
