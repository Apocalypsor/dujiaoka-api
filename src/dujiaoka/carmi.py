from .log import Log
from .util import getPage

logger = Log(__name__).getlog()


def parseCarmi(carmi):
    carmi_params = carmi.find_all("td")
    carmi_options = carmi_params[3].div.find("select").find_all("option")
    sold = "selected" in carmi_options[1].attrs

    carmi = {
        "id": carmi_params[1].get_text().strip(),
        "group": carmi_params[2].get_text().strip(),
        "sold": sold,
        "text": carmi_params[4].find_all("div")[-1].span.get_text().strip(),
        "created_time": carmi_params[5].get_text().strip(),
        "updated_time": carmi_params[6].get_text().strip(),
    }

    return carmi


def get(
    suffix: str = "/carmis",
):
    if not suffix.startswith("/carmis"):
        logger.error("[-] Invalid suffix, please include /carmis")
        return []

    return [parseCarmi(carmi) for carmi in getPage(suffix)]
