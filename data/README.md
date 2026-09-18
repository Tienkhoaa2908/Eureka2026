# Data policy and layout

Raw binary datasets are intentionally not committed during bootstrap.

Reasons:
- the repository is public;
- some source files are copied from official publications and may have redistribution/licensing constraints;
- the current revenue data were partly transcribed from screenshots/PDF tables and need lineage verification before publication.

Expected local layout:

`data/raw/pci/` — untouched original PCI files.
`data/raw/gso/` — original GSO/NSO source files or locally stored references.
`data/interim/` — parsed but not analysis-ready.
`data/processed/panel.csv` — canonical province-year analysis table.
`data/metadata/data_lineage.csv` — source/table/page/unit/extraction/verification metadata.

Rules:
1. Never edit raw files in place.
2. Derived datasets must be reproducible by script.
3. Every correction gets a decision-log entry.
4. Public release requires a source/license review.
