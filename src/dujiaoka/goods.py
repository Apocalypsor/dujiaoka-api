import re

from .config import config
from .log import Log
from .util import getPage

logger = Log(__name__).getlog()


def parseGood(good):
    good_params = good.find_all("td")
    good_listed = good_params[11].input
    listed = "checked" in good_listed.attrs

    good = {
        "id": good_params[1].get_text().strip(),
        "name": good_params[3].get_text().strip(),
        "group": good_params[4].get_text().strip(),
        "type": good_params[5].get_text().strip(),
        "retail_price": good_params[6].get_text().strip(),
        "actual_price": good_params[7].get_text().strip(),
        "inventory": good_params[8].get_text().strip(),
        "sales": good_params[9].get_text().strip(),
        "sort_weight": good_params[10].div.find("span", class_="grid-column-editable").get_text().strip(),
        "listed": listed,
        "created_time": good_params[12].get_text().strip(),
        "updated_time": good_params[13].get_text().strip(),
    }

    return good


def get(
        suffix: str = "/goods",
):
    if not suffix.startswith("/goods"):
        logger.error("[-] Invalid suffix, please include /goods")
        return []

    return [parseGood(good) for good in getPage(suffix)]


def restocking(
        id,
        mode: str = "~",
        amount: int = 0
):
    id = str(id)
    res = config.session.get("/goods/" + id)
    if "详细" not in res.text:
        return "not_found", -1

    token = re.search(r'Dcat\.token = "(.*?)"', res.text).group(1)

    stock = int(re.search(r'库存.+?<div class="box-body">(\d+)&nbsp;', res.text.replace("\n", "")).group(1))
    type = re.search(r'商品类型.*?<div class="box-body">(.+?)&nbsp;', res.text.replace("\n", "")).group(1)

    if type != "人工处理": return -1

    if mode == "~":
        return "viewed", stock

    elif mode in ["+", "-"]:
        new_stock = stock + int(mode + str(amount))
        if new_stock < 0:
            return "not_enough_stock", stock

        mod_good = config.session.post(
            "/goods/" + id,
            data={
                "in_stock": new_stock,
                "_method": "PUT",
                "_token": token,
            },
        ).json()

        if mod_good["status"]:
            return "modified", new_stock
        else:
            return "failed", stock
