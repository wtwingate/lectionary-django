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
        logger.error(f"Error: could not fetch HTML for {reference}.")
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
        logger.error(f"Error: could not fetch Text for {reference}.")
        return ""


def get_kjv_passage_id(reference: str) -> str:
    url = f"{BIBLE_API_URL}v1/bibles/{KJV_ID}/search"

    params = {
        "query": long_reference(reference),
        "sort": "relevance",
    }

    headers = {"api-key": BIBLE_API_KEY}

    response = requests.get(url, params=params, headers=headers, timeout=30)

    passage_ids = [p["id"] for p in response.json()["data"]["passages"]]

    if passage_ids:
        return passage_ids
    else:
        logger.error(f"Error: could not fetch IDs for {reference}.")
        return ""


def get_kjv_html(passage_ids: list[str]) -> str:
    url = f"{BIBLE_API_URL}v1/bibles/{KJV_ID}/passages"

    passages = []
    for id in passage_ids:
        params = {
            "passageId": id,
            "content-type": "html",
        }

        headers = {"api-key": BIBLE_API_KEY}

        response = requests.get(url, params=params, headers=headers, timeout=30)

        try:
            passages.append(response.json()["data"]["content"])
        except KeyError:
            logger.error(f"Error: could not fetch HTML for {id}.")

    if passages:
        return "".join(passages)
    else:
        return ""


def get_kjv_text(passage_ids: list[str]) -> str:
    url = f"{BIBLE_API_URL}v1/bibles/{KJV_ID}/passages"

    passages = []
    for id in passage_ids:
        params = {
            "passageId": id,
            "content-type": "text",
        }

        headers = {"api-key": BIBLE_API_KEY}

        response = requests.get(url, params=params, headers=headers, timeout=30)

        try:
            passages.append(response.json()["data"]["content"])
        except KeyError:
            logger.error(f"Error: could not fetch Text for {id}.")

    if passages:
        return "".join(passages).replace("[", "").replace("]", "")
    else:
        return ""
