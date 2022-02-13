import re

from bs4 import BeautifulSoup

from log import Log
from .config import config

logger = Log(__name__).getlog()


def parseOrder(order, require_text):
    order_params = order.find_all("td")
    order = {
        "id": order_params[1].get_text().strip(),
        "order_id": order_params[2].a["data-content"].strip(),
        "email": order_params[5].a["data-content"].strip(),
        "number": int(order_params[8].get_text().strip()),
    }

    if require_text:
        res = config.session.get("/order/" + order["id"])
        soup = BeautifulSoup(res.text, "html.parser")
        order_text = (
            soup.find(
                "textarea", class_="form-control field_wholesale_price_cnf _normal_"
            )
                .get_text()
                .strip()
        )

        order["text"] = order_text

    return order


def get(
        suffix: str = "/order",
        require_text: bool = False,
):
    res = config.session.get(suffix)
    soup = BeautifulSoup(res.text, "html.parser")
    soup_orders = soup.find("table", class_="table custom-data-table data-table").tbody

    if "暂无数据" in soup_orders.text:
        logger.info("[+] No orders")
        return []
    else:
        orders = soup_orders.find_all("tr")
        return [parseOrder(order, require_text) for order in orders]


def modify(id: str, status: int, order_id: str):
    res = config.session.get("/order/" + id)
    token = re.search(r'Dcat\.token = "(.*?)"', res.text).group(1)
    mod_order = config.session.post(
        "/order/" + id,
        data={
            "status": status,
            "_method": "PUT",
            "_token": token,
        },
    ).json()

    if mod_order["status"]:
        logger.info(f"[+] Order {order_id} status modified")
    else:
        logger.error(f"[-] Order {order_id} status not modified")

    return mod_order["status"]
