from __future__ import annotations

from pathlib import Path, PurePosixPath
import re
from xml.etree import ElementTree as ET
from zipfile import ZipFile

_NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
_CELL_RE = re.compile(r"([A-Z]+)([0-9]+)$")


def _col_index(cell_ref: str) -> int:
    m = _CELL_RE.fullmatch(cell_ref)
    if not m:
        raise ValueError(f"invalid XLSX cell reference: {cell_ref!r}")
    n = 0
    for ch in m.group(1):
        n = n * 26 + (ord(ch) - ord("A") + 1)
    return n - 1


def _shared_strings(zf: ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(path))
    out: list[str] = []
    for si in root.findall(f"{{{_NS_MAIN}}}si"):
        parts = [t.text or "" for t in si.iter(f"{{{_NS_MAIN}}}t")]
        out.append("".join(parts))
    return out


def _sheet_path(zf: ZipFile, sheet_name: str) -> str:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall(f"{{{_NS_REL_PKG}}}Relationship")
    }
    sheets = wb.find(f"{{{_NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("workbook has no sheets collection")
    for sheet in sheets:
        if sheet.attrib.get("name") != sheet_name:
            continue
        rid = sheet.attrib.get(f"{{{_NS_REL_DOC}}}id")
        if rid not in rel_targets:
            raise ValueError(f"sheet relationship not found: {sheet_name}")
        target = rel_targets[rid]
        if target.startswith("/"):
            return target.lstrip("/")
        return str(PurePosixPath("xl") / target)
    raise ValueError(f"sheet not found: {sheet_name!r}")


def read_sheet_rows(path: str | Path, sheet_name: str) -> list[list[object | None]]:
    with ZipFile(Path(path)) as zf:
        shared = _shared_strings(zf)
        sheet_xml = _sheet_path(zf, sheet_name)
        root = ET.fromstring(zf.read(sheet_xml))
        data = root.find(f"{{{_NS_MAIN}}}sheetData")
        if data is None:
            return []
        rows: list[list[object | None]] = []
        max_cols = 0
        for row_el in data.findall(f"{{{_NS_MAIN}}}row"):
            cells: dict[int, object | None] = {}
            for c in row_el.findall(f"{{{_NS_MAIN}}}c"):
                ref = c.attrib.get("r")
                if not ref:
                    continue
                col = _col_index(ref)
                typ = c.attrib.get("t")
                value: object | None
                if typ == "inlineStr":
                    is_el = c.find(f"{{{_NS_MAIN}}}is")
                    value = "" if is_el is None else "".join(
                        t.text or "" for t in is_el.iter(f"{{{_NS_MAIN}}}t")
                    )
                else:
                    v = c.find(f"{{{_NS_MAIN}}}v")
                    if v is None or v.text is None:
                        value = None
                    elif typ == "s":
                        value = shared[int(v.text)]
                    elif typ == "b":
                        value = v.text == "1"
                    elif typ in {"str", "e"}:
                        value = v.text
                    else:
                        num = float(v.text)
                        value = int(num) if num.is_integer() else num
                cells[col] = value
                max_cols = max(max_cols, col + 1)
            row = [None] * max_cols
            for col, value in cells.items():
                if col >= len(row):
                    row.extend([None] * (col + 1 - len(row)))
                row[col] = value
            rows.append(row)
        return [row + [None] * (max_cols - len(row)) for row in rows]


def read_sheet_records(path: str | Path, sheet_name: str) -> list[dict[str, object | None]]:
    rows = read_sheet_rows(path, sheet_name)
    if not rows:
        return []
    headers = [str(x).strip() if x is not None else "" for x in rows[0]]
    if not all(headers):
        raise ValueError(f"blank header in {sheet_name}: {headers}")
    if len(set(headers)) != len(headers):
        raise ValueError(f"duplicate headers in {sheet_name}: {headers}")
    return [dict(zip(headers, row)) for row in rows[1:] if any(v is not None for v in row)]
