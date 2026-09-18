# NEXT EXPERIMENT — DATA-INTEGRITY-01

Priority: P0
Gate: G1 Data integrity

## Question
Are the enterprise-revenue panel values accurate enough to support modeling, especially the three known source subtotal discrepancies?

## Inputs
- Existing `panel_PCI_doanhthu_2010_2024.xlsx`.
- Original GSO/NSO yearbook / enterprise-survey PDF tables used for transcription.
- Current revenue screenshots only as secondary visual evidence.

## Procedure
1. Identify exact official publication, table number, page, unit, and year range for every revenue block.
2. Re-read the three flagged cases from the original PDF, not from the derived workbook:
   - Tây Nguyên 2023: recorded province-sum vs published subtotal difference +2,001.
   - Đồng bằng sông Cửu Long 2023: recorded difference -21.
   - Trung du và miền núi phía Bắc 2016: recorded difference -10,000.
3. Double-entry verify the relevant province values and subtotal.
4. Produce a machine-readable `data_lineage.csv` with source, table, page, unit, extraction method, verifier, and status.
5. Run panel invariants: unique key, 63 provinces/year, 15 years/province, nonnegative revenue, merge coverage, expected missingness only.
6. If an error is found, correct it only in a derived clean dataset and record the correction in `DECISIONS.md` and `CHANGELOG.md`; preserve raw evidence.

## Pass criteria
- All three flagged cases independently resolved.
- No unexplained key or unit inconsistency.
- 100% of revenue observations traceable to official source locations or explicitly marked pending.
- Automated invariant checks pass.

## Output artifacts
- `data/metadata/data_lineage.csv`
- `artifacts/qa/DATA-INTEGRITY-01.md`
- test output/checksum

## Unlocks
G2 reproducible pipeline and then G3 final statistical baseline.
