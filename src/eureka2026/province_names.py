from __future__ import annotations

CANONICAL_PROVINCES: tuple[str, ...] = (
    "An Giang", "Bà Rịa - Vũng Tàu", "Bắc Giang", "Bắc Kạn", "Bạc Liêu",
    "Bắc Ninh", "Bến Tre", "Bình Định", "Bình Dương", "Bình Phước",
    "Bình Thuận", "Cà Mau", "Cao Bằng", "Cần Thơ", "Đà Nẵng", "Đắk Lắk",
    "Đắk Nông", "Điện Biên", "Đồng Nai", "Đồng Tháp", "Gia Lai", "Hà Giang",
    "Hà Nam", "Hà Nội", "Hà Tĩnh", "Hải Dương", "Hải Phòng", "Hậu Giang",
    "Hòa Bình", "Hưng Yên", "Khánh Hòa", "Kiên Giang", "Kon Tum", "Lai Châu",
    "Lâm Đồng", "Lạng Sơn", "Lào Cai", "Long An", "Nam Định", "Nghệ An",
    "Ninh Bình", "Ninh Thuận", "Phú Thọ", "Phú Yên", "Quảng Bình", "Quảng Nam",
    "Quảng Ngãi", "Quảng Ninh", "Quảng Trị", "Sóc Trăng", "Sơn La", "Tây Ninh",
    "Thái Bình", "Thái Nguyên", "Thanh Hóa", "Thừa Thiên Huế", "Tiền Giang",
    "TP. Hồ Chí Minh", "Trà Vinh", "Tuyên Quang", "Vĩnh Long", "Vĩnh Phúc", "Yên Bái",
)

# Explicit aliases accepted at the ingestion boundary. The analysis universe is the
# pre-2025 63-province geography used by the 2010-2024 source panels.
PROVINCE_ALIASES: dict[str, str] = {name: name for name in CANONICAL_PROVINCES}
PROVINCE_ALIASES.update({
    "Bà Rịa-Vũng Tàu": "Bà Rịa - Vũng Tàu",
    "Bà Rịa – Vũng Tàu": "Bà Rịa - Vũng Tàu",
    "Ba Ria - Vung Tau": "Bà Rịa - Vũng Tàu",
    "TP Hồ Chí Minh": "TP. Hồ Chí Minh",
    "TP.Hồ Chí Minh": "TP. Hồ Chí Minh",
    "TP.HCM": "TP. Hồ Chí Minh",
    "Hồ Chí Minh": "TP. Hồ Chí Minh",
    "Ho Chi Minh City": "TP. Hồ Chí Minh",
    "Thừa Thiên - Huế": "Thừa Thiên Huế",
    "Thừa Thiên-Huế": "Thừa Thiên Huế",
    "ĐắkLắk": "Đắk Lắk",
    "ĐắkNông": "Đắk Nông",
})


def normalize_province_name(value: object) -> str:
    raw = " ".join(str(value or "").strip().split())
    if not raw:
        raise ValueError("blank province name")
    try:
        return PROVINCE_ALIASES[raw]
    except KeyError as exc:
        raise ValueError(f"unknown province name: {raw!r}") from exc
