from __future__ import annotations

import json
import requests
from bs4 import BeautifulSoup

URL = "https://pxweb.nso.gov.vn/pxweb/en/Enterprise/Enterprise/E05.08.px/"


def main() -> int:
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 Eureka2026Research"
    r = s.get(URL, timeout=45)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    info = {
        "status": r.status_code,
        "final_url": r.url,
        "forms": [],
        "scripts": [x.get("src") for x in soup.find_all("script") if x.get("src")],
    }
    for form in soup.find_all("form"):
        f = {
            "action": form.get("action"),
            "method": form.get("method"),
            "id": form.get("id"),
            "inputs": [],
            "selects": [],
        }
        for x in form.find_all("input"):
            f["inputs"].append({
                "name": x.get("name"), "type": x.get("type"),
                "value": x.get("value"), "id": x.get("id"),
            })
        for sel in form.find_all("select"):
            f["selects"].append({
                "name": sel.get("name"), "id": sel.get("id"),
                "options": [
                    {"value": o.get("value"), "text": o.get_text(" ", strip=True)}
                    for o in sel.find_all("option")[:5]
                ],
                "option_count": len(sel.find_all("option")),
            })
        info["forms"].append(f)
    print(json.dumps(info, ensure_ascii=False, indent=2)[:30000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
