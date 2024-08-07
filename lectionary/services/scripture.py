import os
import logging
import re

import requests

ESV_HTML_URL = "https://api.esv.org/v3/passage/html/"
ESV_TEXT_URL = "https://api.esv.org/v3/passage/text/"
ESV_API_KEY = os.environ.get("ESV_API_KEY")
TIMEOUT = 30

logger = logging.getLogger("django")


def long_reference(reference: str) -> str:
    return re.sub(r"\(|\)", "", reference)


def short_reference(reference: str) -> str:
    return re.sub(r"\(.*\),?\s*", "", reference)


def get_esv_html(reference: str) -> str:
    params = {
        "q": long_reference(reference),
        "include-passage-references": False,
        "include-footnotes": False,
        "include-headings": False,
        "include-short-copyright": False,
        "include-audio-link": False,
    }

    headers = {
        "Authorization": f"Token {ESV_API_KEY}",
    }

    response = requests.get(
        ESV_HTML_URL, params=params, headers=headers, timeout=TIMEOUT
    )

    passages = "".join(response.json()["passages"])

    if passages:
        return passages
    else:
        logger.error(f"Error: could not fetch {reference}.")
        return ""


def get_esv_text(reference: str) -> str:
    params = {
        "q": long_reference(reference),
        "include-footnotes": False,
        "include-headings": False,
        "include-short-copyright": False,
        "indent-paragraphs": 0,
        "indent-poetry": False,
        "indent-declares": 0,
        "indent-psalm-doxology": 0,
    }

    headers = {
        "Authorization": f"Token {ESV_API_KEY}",
    }

    response = requests.get(
        ESV_TEXT_URL, params=params, headers=headers, timeout=TIMEOUT
    )

    passages = "".join(response.json()["passages"])

    if passages:
        return passages.replace("[", "").replace("]", "")
    else:
        logger.error(f"Error: could not fetch {reference}.")
        return ""
