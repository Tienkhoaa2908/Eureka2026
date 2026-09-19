from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import re
import time
import unicodedata
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

from .province_names import CANONICAL_PROVINCES

NSO_API_BASE = "https://pxweb.nso.gov.vn/api/v1/en/Enterprise"
PCI_PROVINCES_URL = "https://pcivietnam.vn/en/provinces"
USER_AGENT = "Eureka2026Research/1.0 (+https://github.com/Tienkhoaa2908/Eureka2026)"

CORE_YEARS = tuple(range(2015, 2024))
ENTRY_YEARS = tuple(range(2016, 2025))

NSO_TABLES: dict[str, dict[str, Any]] = {
    "E05.08": {"name": "active_results", "years": CORE_YEARS, "unit": "enterprises"},
    "E05.11": {"name": "workers", "years": CORE_YEARS, "unit": "persons"},
    "E05.17": {"name": "capital", "years": CORE_YEARS, "unit": "billion_vnd"},
    "E05.23": {"name": "revenue", "years": CORE_YEARS, "unit": "billion_vnd"},
    "E05.35": {"name": "monthly_income", "years": CORE_YEARS, "unit": "thousand_vnd"},
    "E05.38": {"name": "profit", "years": CORE_YEARS, "unit": "billion_vnd"},
    "E05.41": {"name": "profitability_ratio", "years": CORE_YEARS, "unit": "percent"},
    "E05.44": {"name": "fixed_assets_per_worker", "years": CORE_YEARS, "unit": "million_vnd"},
    "E05.02": {"name": "new_registrations", "years": ENTRY_YEARS, "unit": "enterprises"},
    "E05.04": {"name": "active_all", "years": tuple(range(2017, 2025)), "unit": "enterprises"},
    "E05.05": {"name": "active_per_1000", "years": tuple(range(2017, 2025)), "unit": "enterprises_per_1000_people"},
}

PCI_ROW_TO_COMPONENT = {
    "Entry Costs": "cstp1",
    "Access to land": "cstp2",
    "Transparency": "cstp3",
    "Time Costs": "cstp4",
    "Informal Charges": "cstp5",
    "Policy Bias": "cstp6",
    "Proactivity": "cstp7",
    "Business Support Policy": "cstp8",
    "Labor Policy": "cstp9",
    "Law & Order": "cstp10",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ascii_key(value: object) -> str:
    raw = str(value or "").strip().lower()
    raw = raw.replace("đ", "d")
    raw = unicodedata.normalize("NFKD", raw)
    raw = "".join(ch for ch in raw if not unicodedata.combining(ch))
    raw = re.sub(r"[^a-z0-9]+", " ", raw)
    return " ".join(raw.split())


_CANONICAL_BY_KEY = {_ascii_key(p): p for p in CANONICAL_PROVINCES}
_CANONICAL_BY_KEY.update({
    "hcmc": "TP. Hồ Chí Minh",
    "tp hcm": "TP. Hồ Chí Minh",
    "tp ho chi minh": "TP. Hồ Chí Minh",
    "ho chi minh": "TP. Hồ Chí Minh",
    "ho chi minh city": "TP. Hồ Chí Minh",
    "brvt": "Bà Rịa - Vũng Tàu",
    "ba ria vung tau": "Bà Rịa - Vũng Tàu",
    "tt hue": "Thừa Thiên Huế",
    "thua thien hue": "Thừa Thiên Huế",
    "thua thien hue province": "Thừa Thiên Huế",
})


def normalize_province_loose(value: object) -> str | None:
    raw = re.sub(r"\*+$", "", str(value or "").strip()).strip()
    key = _ascii_key(raw)
    return _CANONICAL_BY_KEY.get(key)


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    timeout: float = 45.0,
    attempts: int = 4,
    **kwargs: Any,
) -> requests.Response:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            response = session.request(method, url, timeout=timeout, **kwargs)
            if response.status_code >= 500 or response.status_code == 429:
                raise requests.HTTPError(
                    f"{response.status_code} from {url}", response=response
                )
            response.raise_for_status()
            return response
        except Exception as exc:  # network retry boundary
            last = exc
            if attempt == attempts - 1:
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"request failed after {attempts} attempts: {url}") from last


def _category_codes(category: dict[str, Any]) -> list[str]:
    index = category.get("index", {})
    if isinstance(index, list):
        return [str(x) for x in index]
    if isinstance(index, dict):
        return [
            str(code)
            for code, _ in sorted(index.items(), key=lambda item: int(item[1]))
        ]
    raise ValueError("unsupported JSON-stat category index")


def decode_jsonstat2(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    ids = list(dataset["id"])
    sizes = [int(x) for x in dataset["size"]]
    dimensions = dataset["dimension"]
    codes_by_dim: list[list[str]] = []
    labels_by_dim: list[dict[str, str]] = []
    for dim in ids:
        category = dimensions[dim]["category"]
        codes = _category_codes(category)
        labels = {str(k): str(v) for k, v in category.get("label", {}).items()}
        codes_by_dim.append(codes)
        labels_by_dim.append(labels)

    values = dataset.get("value", [])
    rows: list[dict[str, Any]] = []
    flat = 0
    for coords in itertools.product(*[range(s) for s in sizes]):
        if isinstance(values, dict):
            value = values.get(str(flat))
        else:
            value = values[flat] if flat < len(values) else None
        row: dict[str, Any] = {}
        for pos, (dim, coord) in enumerate(zip(ids, coords)):
            code = codes_by_dim[pos][coord]
            row[dim] = labels_by_dim[pos].get(code, code)
        row["value"] = value
        rows.append(row)
        flat += 1
    return rows


def _find_metadata_variable_any(
    metadata: dict[str, Any], needles: tuple[str, ...]
) -> dict[str, Any]:
    needle_keys = [_ascii_key(x) for x in needles]
    for variable in metadata.get("variables", []):
        hay = _ascii_key(
            str(variable.get("text", "")) + " " + str(variable.get("code", ""))
        )
        if any(needle in hay for needle in needle_keys):
            return variable
    raise ValueError(
        f"metadata variable containing one of {needles!r} not found; "
        f"available={[v.get('text') for v in metadata.get('variables', [])]}"
    )


def fetch_nso_table(
    session: requests.Session,
    table_code: str,
    years: tuple[int, ...],
    output_dir: Path,
    expected_name: str,
    expected_unit: str,
) -> dict[str, Any]:
    url = f"{NSO_API_BASE}/{table_code}.px/"
    meta_response = request_with_retry(session, "GET", url)
    metadata = meta_response.json()
    province_var = _find_metadata_variable_any(
        metadata, ("cities", "province", "tinh")
    )
    year_var = _find_metadata_variable_any(metadata, ("year", "nam"))

    province_values = list(province_var["values"])
    province_texts = list(province_var.get("valueTexts", province_values))
    selected_province_codes = []
    province_code_to_name: dict[str, str] = {}
    for code, label in zip(province_values, province_texts):
        canonical = normalize_province_loose(label)
        if canonical:
            selected_province_codes.append(str(code))
            province_code_to_name[str(code)] = canonical

    if set(province_code_to_name.values()) != set(CANONICAL_PROVINCES):
        missing = sorted(set(CANONICAL_PROVINCES) - set(province_code_to_name.values()))
        raise ValueError(f"{table_code}: NSO province metadata missing canonical provinces: {missing}")

    year_values = list(year_var["values"])
    year_texts = list(year_var.get("valueTexts", year_values))
    year_code_by_text = {str(text).strip(): str(code) for code, text in zip(year_values, year_texts)}
    selected_year_codes = []
    for year in years:
        code = year_code_by_text.get(str(year))
        if code is None:
            raise ValueError(
                f"{table_code}: requested year {year} absent; available={sorted(year_code_by_text)}"
            )
        selected_year_codes.append(code)

    query = {
        "query": [
            {
                "code": province_var["code"],
                "selection": {"filter": "item", "values": selected_province_codes},
            },
            {
                "code": year_var["code"],
                "selection": {"filter": "item", "values": selected_year_codes},
            },
        ],
        "response": {"format": "json-stat2"},
    }
    data_response = request_with_retry(session, "POST", url, json=query)
    dataset = data_response.json()
    decoded = decode_jsonstat2(dataset)

    province_dim = province_var["code"]
    year_dim = year_var["code"]
    normalized = []
    for row in decoded:
        province = normalize_province_loose(row[province_dim])
        if not province:
            continue
        year = int(str(row[year_dim]).strip())
        normalized.append({
            "province": province,
            "year": year,
            "value": row["value"],
            "table_code": table_code,
            "series": expected_name,
            "unit": expected_unit,
        })

    keys = {(r["province"], r["year"]) for r in normalized}
    expected_keys = {(p, y) for p in CANONICAL_PROVINCES for y in years}
    if keys != expected_keys:
        missing = sorted(expected_keys - keys)
        extra = sorted(keys - expected_keys)
        raise ValueError(
            f"{table_code}: key coverage mismatch missing={missing[:10]} extra={extra[:10]}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    meta_path = output_dir / f"{table_code}_metadata.json"
    meta_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    csv_path = output_dir / f"{table_code}_{expected_name}.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["province", "year", "value", "table_code", "series", "unit"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(normalized, key=lambda r: (r["province"], r["year"])))

    nonnull = sum(r["value"] is not None for r in normalized)
    return {
        "table_code": table_code,
        "series": expected_name,
        "url": url,
        "metadata_sha256": sha256_bytes(meta_response.content),
        "response_sha256": sha256_bytes(data_response.content),
        "rows": len(normalized),
        "nonnull": nonnull,
        "years": list(years),
        "unit": expected_unit,
        "title": metadata.get("title"),
        "updated": metadata.get("updated"),
    }


def _parse_pci_table(html: str, province_hint: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    best: list[list[str]] | None = None
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [
                " ".join(cell.get_text(" ", strip=True).split())
                for cell in tr.find_all(["th", "td"])
            ]
            if cells:
                rows.append(cells)
        flat = " | ".join(" ".join(r) for r in rows)
        if "Entry Costs" in flat and "Informal Charges" in flat and "Law & Order" in flat:
            best = rows
            break
    if not best:
        raise ValueError(f"PCI score table not found for {province_hint}")

    year_row = next((r for r in best if r and r[0].strip().lower() == "year"), None)
    if not year_row:
        raise ValueError(f"PCI year row not found for {province_hint}")
    years = [int(x) for x in year_row[1:] if re.fullmatch(r"20\d{2}", x)]

    output = []
    for row in best:
        if not row:
            continue
        label = row[0]
        component = PCI_ROW_TO_COMPONENT.get(label)
        if not component:
            continue
        values = row[1 : 1 + len(years)]
        if len(values) != len(years):
            raise ValueError(f"PCI row width mismatch {province_hint} {label}")
        for year, value in zip(years, values):
            value = value.strip()
            if value.upper() in {"N/A", "NA", ""}:
                numeric = None
            else:
                numeric = float(value)
            output.append({
                "province": province_hint,
                "year": year,
                "component": component,
                "value": numeric,
            })
    return output


def discover_pci_profiles(session: requests.Session) -> dict[str, str]:
    response = request_with_retry(session, "GET", PCI_PROVINCES_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    found: dict[str, str] = {}
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"])
        if "/en/provinces/" not in href:
            continue
        label = " ".join(anchor.get_text(" ", strip=True).split())
        canonical = normalize_province_loose(label)
        if not canonical:
            continue
        if href.startswith("/"):
            href = "https://pcivietnam.vn" + href
        elif href.startswith("http"):
            pass
        else:
            href = "https://pcivietnam.vn/" + href.lstrip("/")
        found[canonical] = href
    if set(found) != set(CANONICAL_PROVINCES):
        missing = sorted(set(CANONICAL_PROVINCES) - set(found))
        raise ValueError(f"PCI profile discovery missing provinces: {missing}")
    return found


def fetch_pci(session: requests.Session, output_dir: Path) -> dict[str, Any]:
    profiles = discover_pci_profiles(session)
    records: list[dict[str, Any]] = []
    profile_hashes: dict[str, str] = {}
    for idx, province in enumerate(CANONICAL_PROVINCES):
        response = request_with_retry(session, "GET", profiles[province])
        profile_hashes[province] = sha256_bytes(response.content)
        parsed = _parse_pci_table(response.text, province)
        records.extend(r for r in parsed if 2013 <= int(r["year"]) <= 2024)
        if idx and idx % 15 == 0:
            time.sleep(0.5)

    key_count = len({(r["province"], r["year"], r["component"]) for r in records})
    if key_count != len(records):
        raise ValueError("duplicate PCI province-year-component keys")
    expected_2013_2024 = len(CANONICAL_PROVINCES) * 12 * 10
    if len(records) != expected_2013_2024:
        raise ValueError(
            f"PCI expected {expected_2013_2024} records for 2013-2024, got {len(records)}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "pci_components_2013_2024.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["province", "year", "component", "value"], lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(sorted(records, key=lambda r: (r["province"], r["year"], r["component"])))
    hashes_path = output_dir / "pci_profile_hashes.json"
    hashes_path.write_text(
        json.dumps(profile_hashes, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    nulls = sum(r["value"] is None for r in records)
    return {
        "source": PCI_PROVINCES_URL,
        "rows": len(records),
        "nulls": nulls,
        "profile_count": len(profiles),
        "csv_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def run(output_root: str | Path) -> dict[str, Any]:
    root = Path(output_root)
    raw = root / "raw"
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json,text/html,*/*"})

    nso_manifest = []
    for code, config in NSO_TABLES.items():
        nso_manifest.append(
            fetch_nso_table(
                session,
                code,
                tuple(config["years"]),
                raw / "nso",
                str(config["name"]),
                str(config["unit"]),
            )
        )

    pci_manifest = fetch_pci(session, raw / "pci")
    manifest = {
        "nso": nso_manifest,
        "pci": pci_manifest,
        "generated_at_utc": None,
        "note": "generated_at deliberately omitted from deterministic scientific payload",
    }
    path = root / "source_manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default="artifacts/sr1")
    return p


def main() -> int:
    args = parser().parse_args()
    result = run(args.output_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
