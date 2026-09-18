# Data policy and canonical build

The repository is public, so raw binary source/migration workbooks are not committed by default. Their fingerprints and lineage are committed instead.

## Local layout

```text
data/
  raw/
    migration/
      panel_PCI_doanhthu_2010_2024.xlsx
      Panel_10_CSTP_2010_2024.xlsx
  processed/
    panel.csv
  metadata/
    data_lineage.csv
    revenue_corrections.csv
    canonical_build_manifest.json
```

`data/raw/**` and `data/processed/**` remain git-ignored.

## Canonical one-command build

Place the two identified migration workbooks at the paths above and run from repository root:

```bash
python -m src.eureka2026.pipeline
```

The command will:

1. read the two XLSX inputs without modifying them;
2. normalize province names against the explicit pre-2025 63-province contract;
3. apply only the three verified revenue corrections;
4. rebuild revenue growth and PCI lag;
5. normalize the 10 CSTP columns and preserve CSTP6 structural missingness in 2010–2012;
6. build all one-year CSTP lag fields;
7. enforce one-to-one province-year merge coverage;
8. validate 945 rows = 63 × 15;
9. write deterministic UTF-8 `data/processed/panel.csv`;
10. write local machine-readable QA metadata.

Current expected fingerprints are in `data/metadata/canonical_build_manifest.json`.

## Rules

1. Never edit raw files in place.
2. Never edit `data/processed/panel.csv` manually; rebuild it.
3. Every source correction requires evidence plus a decision-log entry.
4. Unknown province names fail instead of fuzzy-matching silently.
5. CSTP6 before 2013 is structurally unavailable and must not be imputed.
6. Public release of source binaries requires a separate source/license review.
