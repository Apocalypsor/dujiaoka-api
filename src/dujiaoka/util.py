from bs4 import BeautifulSoup

from .config import config
from .log import Log

logger = Log(__name__).getlog()


def getPage(
        suffix: str,
):
    res = config.session.get(suffix)
    soup = BeautifulSoup(res.text, "html.parser")
    soup_page = soup.find("table", class_="table custom-data-table data-table").tbody

    if "暂无数据" in soup_page.text:
        logger.info("[+] Empty page")
        return []
    else:
        page_num = int(soup.find_all("li", class_="page-item")[-2].get_text())
        logger.info(f"[+] {page_num} pages in total")
        if "?" not in suffix:
            suffix += "?page="
        else:
            suffix.replace("page=", "")
            suffix += "&page="

        pages = soup_page.find_all("tr")
        if page_num > 1:
            for i in range(1, page_num):
                res = config.session.get(suffix + str(i + 1))
                soup = BeautifulSoup(res.text, "html.parser")
                soup_page = soup.find(
                    "table", class_="table custom-data-table data-table"
                ).tbody
                pages += soup_page.find_all("tr")

        return pages
