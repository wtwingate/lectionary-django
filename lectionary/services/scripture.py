import os
import logging
import re

import requests

ESV_API_URL = "https://api.esv.org/"
ESV_API_KEY = os.environ.get("ESV_API_KEY")
BIBLE_API_URL = "https://api.scripture.api.bible/"
BIBLE_API_KEY = os.environ.get("BIBLE_API_KEY")
KJV_ID = "de4e12af7f28f599-01"
TIMEOUT = 30

logger = logging.getLogger("django")


def long_reference(reference: str) -> str:
    return re.sub(r"\(|\)", "", reference)


def short_reference(reference: str) -> str:
    return re.sub(r"\(.*\),?\s*", "", reference)


def get_kjv_html(reference: str) -> str:
    url = f"{BIBLE_API_URL}v1/bibles/{KJV_ID}/search"

    params = {
        "query": long_reference(reference),
        "sort": "relevance",
    }

    headers = {"api-key": BIBLE_API_KEY}

    response = requests.get(url, params=params, headers=headers, timeout=30)

    passages = "".join([p["content"] for p in response.json()["data"]["passages"]])

    if passages:
        return passages
    else:
        logger.error(f"Error: could not fetch {reference}.")
        return ""


def get_esv_html(reference: str) -> str:
    url = f"{ESV_API_URL}/v3/passage/html/"

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

    response = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)

    passages = "".join(response.json()["passages"])

    if passages:
        return passages
    else:
        logger.error(f"Error: could not fetch {reference}.")
        return ""


def get_esv_text(reference: str) -> str:
    url = f"{ESV_API_URL}/v3/passage/text/"

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

    response = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)

    passages = "".join(response.json()["passages"])

    if passages:
        return passages.replace("[", "").replace("]", "")
    else:
        logger.error(f"Error: could not fetch {reference}.")
        return ""
