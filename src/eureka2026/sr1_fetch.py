from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
import unicodedata
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup

from .province_names import CANONICAL_PROVINCES

USER_AGENT = "Eureka2026Research/2.0 (+https://github.com/Tienkhoaa2908/Eureka2026)"
PCI_PROVINCES_URL = "https://pcivietnam.vn/en/provinces"

CORE_YEARS = tuple(range(2015, 2024))
ENTRY_YEARS = tuple(range(2016, 2025))

NSO_DATABASE_SEGMENTS = {
    "enterprise": "Enterprise",
    "population": "Population%20and%20Employment",
    "trade_price": "Trade%2C%20Price%20and%20Tourist",
}

# These are the data needed for the active scientific design.  The first block
# forms the enterprise accounting system; the second block supplies scale,
# human-capital and spatial-price information needed to interpret it.
NSO_TABLES: dict[str, dict[str, Any]] = {
    "E05.08": {"database": "enterprise", "name": "active_results", "years": CORE_YEARS, "unit": "enterprises"},
    "E05.11": {"database": "enterprise", "name": "workers", "years": CORE_YEARS, "unit": "persons"},
    "E05.17": {"database": "enterprise", "name": "capital", "years": CORE_YEARS, "unit": "billion_vnd"},
    "E05.23": {"database": "enterprise", "name": "revenue", "years": CORE_YEARS, "unit": "billion_vnd"},
    "E05.35": {"database": "enterprise", "name": "monthly_income", "years": CORE_YEARS, "unit": "thousand_vnd"},
    "E05.38": {"database": "enterprise", "name": "profit", "years": CORE_YEARS, "unit": "billion_vnd"},
    "E05.41": {"database": "enterprise", "name": "profitability_ratio", "years": CORE_YEARS, "unit": "percent"},
    "E05.44": {"database": "enterprise", "name": "fixed_assets_per_worker", "years": CORE_YEARS, "unit": "million_vnd"},
    "E05.02": {"database": "enterprise", "name": "new_registrations", "years": ENTRY_YEARS, "unit": "enterprises"},
    "E05.04": {"database": "enterprise", "name": "active_all", "years": tuple(range(2017, 2025)), "unit": "enterprises"},
    "E05.05": {"database": "enterprise", "name": "active_per_1000", "years": tuple(range(2017, 2025)), "unit": "enterprises_per_1000_people"},
    "E02.03-07": {"database": "population", "name": "average_population", "years": CORE_YEARS, "unit": "thousand_persons"},
    "E02.55": {"database": "population", "name": "trained_labor_share", "years": CORE_YEARS, "unit": "percent"},
    "E11.23": {"database": "trade_price", "name": "spatial_cost_index", "years": CORE_YEARS, "unit": "hanoi_equals_100"},
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
    raw = str(value or "").strip().lower().replace("đ", "d")
    raw = unicodedata.normalize("NFKD", raw)
    raw = "".join(ch for ch in raw if not unicodedata.combining(ch))
    raw = re.sub(r"[^a-z0-9]+", " ", raw)
    return " ".join(raw.split())


_CANONICAL_BY_KEY = {_ascii_key(p): p for p in CANONICAL_PROVINCES}
_CANONICAL_BY_KEY.update(
    {
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
    }
)


def normalize_province_loose(value: object, *, historical_63: bool = False) -> str | None:
    raw = re.sub(r"\*+$", "", str(value or "").strip()).strip()
    key = _ascii_key(raw)
    # NQ 175/2024/QH15: the centrally governed Hue uses the whole former
    # province. Only accept the renamed label in explicitly pre-2025 panels.
    if historical_63 and key == "hue":
        return "Thừa Thiên Huế"
    # PX-Web English labels are not fully consistent with Vietnamese Unicode
    # names. Keep explicit reviewed exceptions rather than fuzzy matching.
    if key in {"thua thien hue", "thua thien hue province"}:
        return "Thừa Thiên Huế"
    return _CANONICAL_BY_KEY.get(key)


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    timeout: float = 60.0,
    attempts: int = 4,
    **kwargs: Any,
) -> requests.Response:
    last: Exception | None = None
    for attempt in range(attempts):
        try:
            response = session.request(method, url, timeout=timeout, **kwargs)
            if response.status_code >= 500 or response.status_code == 429:
                raise requests.HTTPError(f"{response.status_code} from {url}", response=response)
            response.raise_for_status()
            return response
        except Exception as exc:
            last = exc
            if attempt == attempts - 1:
                break
            time.sleep(2**attempt)
    raise RuntimeError(f"request failed after {attempts} attempts: {url}") from last



def decode_jsonstat2(dataset: dict[str, Any]) -> list[dict[str, Any]]:
    """Compatibility helper retained for deterministic unit tests.

    The active NSO downloader no longer depends on JSON-stat because the public
    NSO deployment currently rejects the standard API POST endpoint.  Keeping
    this decoder costs little and preserves a tested parser for any future API
    restoration.
    """
    ids = list(dataset["id"])
    sizes = [int(x) for x in dataset["size"]]
    dimensions = dataset["dimension"]
    codes_by_dim: list[list[str]] = []
    labels_by_dim: list[dict[str, str]] = []
    for dim in ids:
        category = dimensions[dim]["category"]
        index = category.get("index", {})
        if isinstance(index, list):
            codes = [str(x) for x in index]
        else:
            codes = [
                str(code)
                for code, _ in sorted(index.items(), key=lambda item: int(item[1]))
            ]
        codes_by_dim.append(codes)
        labels_by_dim.append(
            {str(k): str(v) for k, v in category.get("label", {}).items()}
        )

    values = dataset.get("value", [])
    rows: list[dict[str, Any]] = []
    flat = 0

    def walk(level: int, coords: list[int]) -> None:
        nonlocal flat
        if level == len(sizes):
            row: dict[str, Any] = {}
            for pos, (dim, coord) in enumerate(zip(ids, coords)):
                code = codes_by_dim[pos][coord]
                row[dim] = labels_by_dim[pos].get(code, code)
            row["value"] = (
                values.get(str(flat))
                if isinstance(values, dict)
                else (values[flat] if flat < len(values) else None)
            )
            rows.append(row)
            flat += 1
            return
        for coord in range(sizes[level]):
            walk(level + 1, coords + [coord])

    walk(0, [])
    return rows


def nso_ui_url(table_code: str, database: str) -> str:
    segment = NSO_DATABASE_SEGMENTS[database]
    return f"https://pxweb.nso.gov.vn/pxweb/en/{segment}/{segment}/{table_code}.px/"


def _values_listboxes(form: BeautifulSoup) -> list[Any]:
    return [
        sel
        for sel in form.find_all("select")
        if str(sel.get("name", "")).endswith("$ValuesListBox")
    ]


def _identify_nso_dimensions(form: BeautifulSoup) -> tuple[Any, Any, list[Any]]:
    boxes = _values_listboxes(form)
    province_box = None
    year_box = None
    others: list[Any] = []
    for box in boxes:
        labels = [" ".join(o.get_text(" ", strip=True).split()) for o in box.find_all("option")]
        province_hits = sum(normalize_province_loose(x) is not None for x in labels)
        year_hits = sum(bool(re.fullmatch(r"(?:19|20)\d{2}", x)) for x in labels)
        if province_hits >= 40:
            province_box = box
        elif year_hits >= 3:
            year_box = box
        else:
            others.append(box)
    if province_box is None or year_box is None:
        raise ValueError(
            "Could not identify province/year listboxes; "
            f"box_count={len(boxes)} names={[x.get('name') for x in boxes]}"
        )
    return province_box, year_box, others


def _choose_scalar_option(box: Any) -> tuple[str, str]:
    options = box.find_all("option")
    if not options:
        raise ValueError(f"empty auxiliary listbox {box.get('name')}")
    preferred = (
        "total",
        "total population",
        "both sexes",
        "both sex",
        "total average population",
    )
    for option in options:
        label = " ".join(option.get_text(" ", strip=True).split())
        if _ascii_key(label) in preferred:
            return str(option.get("value")), label
    if len(options) == 1:
        option = options[0]
        return str(option.get("value")), " ".join(option.get_text(" ", strip=True).split())
    raise ValueError(
        "Chiều phụ có nhiều lựa chọn nhưng chưa xác minh lựa chọn tổng số: "
        + repr([o.get_text(" ", strip=True) for o in options])
    )


def _normal_number(raw: str) -> float | None:
    value = raw.strip().replace("\xa0", " ").strip()
    if value in {"", "..", "...", "-", "–", "—", "na", "n/a"}:
        return None
    value = value.replace(" ", "")
    # PX-Web's comma-delimited files quote values that contain thousands
    # separators.  The statistics in these tables use a dot as decimal mark.
    value = value.replace(",", "")
    return float(value)


def _parse_wide_pxweb_csv(
    body: bytes,
    years: tuple[int, ...],
    table_code: str,
    series_name: str,
    unit: str,
) -> list[dict[str, Any]]:
    decoded = None
    for encoding in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            decoded = body.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if decoded is None:
        raise ValueError(f"{table_code}: unable to decode PX-Web CSV")

    lines = [line for line in decoded.splitlines() if line.strip()]
    header_idx = None
    delimiter = ","
    for idx, line in enumerate(lines[:12]):
        for candidate in (",", ";", "\t"):
            cells = [x.strip().strip('"') for x in next(csv.reader([line], delimiter=candidate))]
            hits = sum(str(y) in cells for y in years)
            if hits >= min(2, len(years)):
                header_idx = idx
                delimiter = candidate
                break
        if header_idx is not None:
            break
    if header_idx is None:
        raise ValueError(f"{table_code}: year header not found in PX-Web export")

    parsed = list(csv.reader(lines[header_idx:], delimiter=delimiter))
    header = [x.strip().strip('"') for x in parsed[0]]
    year_columns: dict[int, int] = {}
    for year in years:
        if str(year) not in header:
            raise ValueError(f"{table_code}: requested year {year} absent from CSV header {header}")
        year_columns[year] = header.index(str(year))

    records: list[dict[str, Any]] = []
    for row in parsed[1:]:
        if not row:
            continue
        province = normalize_province_loose(row[0], historical_63=max(years) <= 2024)
        if not province:
            continue
        for year, col in year_columns.items():
            raw = row[col] if col < len(row) else ""
            records.append(
                {
                    "province": province,
                    "year": year,
                    "value": _normal_number(raw),
                    "table_code": table_code,
                    "series": series_name,
                    "unit": unit,
                }
            )
    return records


def _submit_nso_form(
    session: requests.Session,
    page_url: str,
    years: tuple[int, ...],
) -> tuple[bytes, dict[str, Any], bytes]:
    page = request_with_retry(session, "GET", page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    form = soup.find("form", id="aspnetForm")
    if form is None:
        raise ValueError(f"aspnetForm not found at {page_url}")

    province_box, year_box, other_boxes = _identify_nso_dimensions(form)

    province_values: list[str] = []
    province_names: list[str] = []
    province_labels: list[dict[str, str]] = []
    for option in province_box.find_all("option"):
        label = " ".join(option.get_text(" ", strip=True).split())
        canonical = normalize_province_loose(label, historical_63=max(years) <= 2024)
        if canonical:
            province_values.append(str(option.get("value")))
            province_names.append(canonical)
            province_labels.append({"source_label": label, "canonical": canonical})
    if len(province_names) != len(set(province_names)):
        raise ValueError(f"duplicate province labels after normalization at {page_url}")
    if set(province_names) != set(CANONICAL_PROVINCES):
        missing = sorted(set(CANONICAL_PROVINCES) - set(province_names))
        extra = sorted(set(province_names) - set(CANONICAL_PROVINCES))
        unmapped = [o.get_text(" ", strip=True) for o in province_box.find_all("option")
                    if normalize_province_loose(o.get_text(" ", strip=True), historical_63=max(years) <= 2024) is None]
        raise ValueError(f"province coverage mismatch at {page_url}: missing={missing} extra={extra}; unmapped={unmapped}")

    year_options = {
        " ".join(o.get_text(" ", strip=True).split()): str(o.get("value"))
        for o in year_box.find_all("option")
    }
    year_values = []
    for year in years:
        if str(year) not in year_options:
            raise ValueError(
                f"requested year {year} unavailable at {page_url}; "
                f"available={sorted(year_options)}"
            )
        year_values.append(year_options[str(year)])

    output_box = next(
        (
            x
            for x in form.find_all("select")
            if str(x.get("name", "")).endswith("$OutputFormatDropDownList")
        ),
        None,
    )
    if output_box is None:
        raise ValueError(f"output-format listbox not found at {page_url}")
    csv_format = "FileTypeCsvWithHeadingAndComma"
    available_formats = {str(o.get("value")) for o in output_box.find_all("option")}
    if csv_format not in available_formats:
        raise ValueError(f"CSV output unavailable at {page_url}")

    submit = form.find("input", attrs={"name": re.compile(r"\$ButtonViewTable$")})
    if submit is None:
        raise ValueError(f"Continue button not found at {page_url}")

    selected_aux: list[dict[str, str]] = []
    aux_values: dict[str, list[str]] = {}
    for box in other_boxes:
        value, label = _choose_scalar_option(box)
        aux_values[str(box.get("name"))] = [value]
        selected_aux.append({"control": str(box.get("name")), "label": label, "value": value})

    selections = {
        str(province_box.get("name")): province_values,
        str(year_box.get("name")): year_values,
        **aux_values,
    }

    payload: list[tuple[str, str]] = []
    selected_counts: dict[str, int] = {}
    for select_name, values in selections.items():
        selected_counts[select_name.rsplit("$ValuesListBox", 1)[0]] = len(values)

    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        typ = str(inp.get("type", "text")).lower()
        if typ == "hidden":
            payload.append((str(name), str(inp.get("value") or "")))
        elif typ == "text":
            value = str(inp.get("value") or "")
            if str(name).endswith("$NumberValuesSelected"):
                prefix = str(name).rsplit("$NumberValuesSelected", 1)[0]
                value = str(selected_counts.get(prefix, 0))
            payload.append((str(name), value))
        elif typ == "checkbox" and inp.has_attr("checked"):
            payload.append((str(name), str(inp.get("value") or "on")))

    for select_name, values in selections.items():
        for value in values:
            payload.append((select_name, value))

    payload.append((str(output_box.get("name")), csv_format))
    payload.append((str(submit.get("name")), str(submit.get("value") or "Continue")))

    response = request_with_retry(
        session,
        "POST",
        page_url,
        data=payload,
        headers={"Referer": page_url, "Accept": "text/csv,application/octet-stream,*/*"},
    )

    content_type = response.headers.get("Content-Type", "")
    head = response.content[:1000].decode("utf-8", errors="ignore").lower()
    if "text/html" in content_type.lower() or "<html" in head or "<!doctype" in head:
        result_soup = BeautifulSoup(response.text, "html.parser")
        error_text = " | ".join(
            x.get_text(" ", strip=True)
            for x in result_soup.select(
                ".variableselector_selectionerror_label, "
                ".variableselector_selectionerror_label_text, "
                ".pxweb-input-error, .error"
            )
            if x.get_text(" ", strip=True)
        )
        raise ValueError(
            "PX-Web returned HTML after CSV request; "
            f"url={page_url} content_type={content_type!r} errors={error_text[:1200]!r}"
        )

    meta_title = None
    og_title = soup.find("meta", attrs={"property": "og:title"})
    if og_title is not None:
        meta_title = og_title.get("content")

    form_metadata = {
        "source_url": page_url,
        "title": meta_title,
        "selected_years": list(years),
        "province_count": len(province_values),
        "province_label_mapping": province_labels,
        "page_text": soup.get_text(" ", strip=True),
        "auxiliary_selections": selected_aux,
        "page_sha256": sha256_bytes(page.content),
        "raw_export_sha256": sha256_bytes(response.content),
        "content_type": content_type,
    }
    return response.content, form_metadata, page.content


def fetch_nso_table(
    session: requests.Session,
    table_code: str,
    config: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    years = tuple(int(x) for x in config["years"])
    page_url = nso_ui_url(table_code, str(config["database"]))
    raw_bytes, form_meta, page_bytes = _submit_nso_form(session, page_url, years)

    records = _parse_wide_pxweb_csv(
        raw_bytes,
        years,
        table_code,
        str(config["name"]),
        str(config["unit"]),
    )
    expected_keys = {(p, y) for p in CANONICAL_PROVINCES for y in years}
    keys = {(r["province"], int(r["year"])) for r in records}
    if len(keys) != len(records):
        raise ValueError(f"{table_code}: trùng khóa tỉnh-năm trong bản xuất")
    if keys != expected_keys:
        missing = sorted(expected_keys - keys)
        extra = sorted(keys - expected_keys)
        raise ValueError(
            f"{table_code}: normalized coverage mismatch "
            f"missing={missing[:12]} extra={extra[:12]}"
        )

    source_dir = output_dir / "source"
    normalized_dir = output_dir / "normalized"
    metadata_dir = output_dir / "metadata"
    source_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    raw_path = source_dir / f"{table_code}.csv"
    raw_path.write_bytes(raw_bytes)
    (source_dir / f"{table_code}.html").write_bytes(page_bytes)
    normalized_path = normalized_dir / f"{table_code}_{config['name']}.csv"
    with normalized_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["province", "year", "value", "table_code", "series", "unit"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(records, key=lambda r: (r["province"], r["year"])))

    metadata_path = metadata_dir / f"{table_code}.json"
    metadata = {
        **form_meta,
        "table_code": table_code,
        "series": config["name"],
        "declared_unit": config["unit"],
        "normalized_rows": len(records),
        "nonnull_rows": sum(r["value"] is not None for r in records),
        "normalized_sha256": hashlib.sha256(normalized_path.read_bytes()).hexdigest(),
    }
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


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
        component = PCI_ROW_TO_COMPONENT.get(row[0] if row else "")
        if not component:
            continue
        values = row[1 : 1 + len(years)]
        if len(values) != len(years):
            raise ValueError(f"PCI row width mismatch {province_hint} {row[0]}")
        for year, value in zip(years, values):
            numeric = None if value.strip().upper() in {"N/A", "NA", ""} else float(value)
            output.append(
                {
                    "province": province_hint,
                    "year": year,
                    "component": component,
                    "value": numeric,
                }
            )
    return output


def discover_pci_profiles(session: requests.Session) -> dict[str, str]:
    response = request_with_retry(session, "GET", PCI_PROVINCES_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    found: dict[str, str] = {}
    for anchor in soup.find_all("a", href=True):
        href = str(anchor["href"])
        if "/en/provinces/" not in href:
            continue
        canonical = normalize_province_loose(" ".join(anchor.get_text(" ", strip=True).split()))
        if not canonical:
            continue
        if href.startswith("/"):
            href = "https://pcivietnam.vn" + href
        elif not href.startswith("http"):
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
        records.extend(
            r
            for r in _parse_pci_table(response.text, province)
            if 2013 <= int(r["year"]) <= 2024
        )
        if idx and idx % 15 == 0:
            time.sleep(0.4)

    if len({(r["province"], r["year"], r["component"]) for r in records}) != len(records):
        raise ValueError("duplicate PCI province-year-component keys")
    expected = len(CANONICAL_PROVINCES) * 12 * 10
    if len(records) != expected:
        raise ValueError(f"PCI expected {expected} rows for 2013-2024, got {len(records)}")

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "pci_components_2013_2024.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["province", "year", "component", "value"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(records, key=lambda r: (r["province"], r["year"], r["component"])))

    (output_dir / "pci_profile_hashes.json").write_text(
        json.dumps(profile_hashes, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "source": PCI_PROVINCES_URL,
        "profile_count": len(profiles),
        "rows": len(records),
        "nulls": sum(r["value"] is None for r in records),
        "csv_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "redistribution_note": (
            "Derived research input; original VCCI PCI files are not vendored. "
            "VCCI citation/data-use policy must be followed."
        ),
    }


def run(output_root: str | Path) -> dict[str, Any]:
    root = Path(output_root)
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,text/csv,application/octet-stream,*/*",
        }
    )

    nso_manifest = []
    for code, config in NSO_TABLES.items():
        print(f"Acquiring NSO {code}: {config['name']}", flush=True)
        nso_manifest.append(fetch_nso_table(session, code, config, root / "raw" / "nso"))

    pci_manifest = fetch_pci(session, root / "raw" / "pci")
    manifest = {
        "nso": nso_manifest,
        "pci": pci_manifest,
        "generated_at_utc": None,
        "note": "Timestamp omitted from deterministic payload; source hashes identify the retrieval.",
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "source_manifest.json").write_text(
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
    print(json.dumps(run(args.output_root), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
