import re

from bs4 import BeautifulSoup

from .config import config
from .log import Log
from .util import getPage

logger = Log(__name__).getlog()


def parseOrder(order, require_text):
    order_params = order.find_all("td")
    order = {
        "id": order_params[1].get_text().strip(),
        "order_id": order_params[2].a["data-content"].strip(),
        "order_name": order_params[3].get_text().strip(),
        "email": order_params[5].a["data-content"].strip(),
        "product": order_params[6].get_text().strip(),
        "unit_price": order_params[7].get_text().strip(),
        "number": int(order_params[8].get_text().strip()),
        "total_price": order_params[9].get_text().strip(),
        "actual_payment": order_params[13].get_text().strip(),
        "payment_channel": order_params[14].get_text().strip(),
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
    if not suffix.startswith("/order"):
        logger.error("[-] Invalid suffix, please include /order")
        return []

    return [parseOrder(order, require_text) for order in getPage(suffix)]


def modify(id, status: int, order_id: str = None):
    id = str(id)
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
