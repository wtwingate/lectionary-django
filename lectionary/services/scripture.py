import os
import requests

ESV_HTML_URL = "https://api.esv.org/v3/passage/html/"
ESV_TEXT_URL = "https://api.esv.org/v3/passage/text/"
ESV_API_KEY = os.environ.get("ESV_API_KEY")
TIMEOUT = 30


def get_esv_html(reference):
    params = {
        "q": reference,
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

    passages = response.json()["passages"]

    if passages:
        return passages[0]
    else:
        raise Exception("Error: passage not found")


def get_esv_text(reference):
    params = {
        "q": reference,
        "include-passage-references": False,
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

    passages = response.json()["passages"]

    if passages:
        return split_text(passages[0])
    else:
        raise Exception("Error: passage not found")


def split_text(text):
    return [p for p in text.splitlines() if p]
