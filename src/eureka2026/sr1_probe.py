from __future__ import annotations

import json
import re
import requests
from bs4 import BeautifulSoup

URL = "https://pxweb.nso.gov.vn/pxweb/en/Enterprise/Enterprise/E05.08.px/"


def main() -> int:
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 Eureka2026Research"
    r = s.get(URL, timeout=45)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    controls = []
    for tag in soup.find_all(["input", "select", "button", "textarea"]):
        typ = tag.get("type")
        name = tag.get("name")
        ident = tag.get("id")
        value = tag.get("value")
        if typ == "hidden":
            value = f"<hidden len={len(value or '')}>"
        item = {
            "tag": tag.name, "type": typ, "name": name, "id": ident,
            "value": value,
        }
        if tag.name == "select":
            opts = tag.find_all("option")
            item["option_count"] = len(opts)
            item["options"] = [
                {"value": o.get("value"), "text": o.get_text(" ", strip=True)}
                for o in opts
            ]
        controls.append(item)

    text = soup.get_text(" ", strip=True)
    fragments = {}
    for needle in [
        "Select all available values", "Continue", "Show table",
        "Number of acting enterprises", "Year", "province"
    ]:
        idx = text.lower().find(needle.lower())
        fragments[needle] = None if idx < 0 else text[max(0, idx-300):idx+800]

    html_fragments = {}
    raw = r.text
    for needle in [
        "Select all available values", "Continue", "VariableSelector1",
        "FileTypeCsvWithHeadingAndComma"
    ]:
        idx = raw.find(needle)
        html_fragments[needle] = None if idx < 0 else raw[max(0, idx-1200):idx+2400]

    info = {
        "status": r.status_code,
        "final_url": r.url,
        "form": {
            "action": soup.find("form").get("action") if soup.find("form") else None,
            "method": soup.find("form").get("method") if soup.find("form") else None,
            "id": soup.find("form").get("id") if soup.find("form") else None,
        },
        "control_count": len(controls),
        "controls": controls,
        "text_fragments": fragments,
        # Không ghi VIEWSTATE hoặc mã phiên vào nhật ký công khai.
    }
    print(json.dumps(info, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
