# CDF progress and half-year performance

Sections 6-7 of `notebooks/chirundu_cdf_project.ipynb` reproduce these tables after setup and the approved-project extraction. All required functions are defined in the notebook. Files use UTF-8, a pipe (`|`) delimiter and blank cells for missing values.

| Filename after `db-unza26-csc4792-chirundu_` | Rows | Coverage |
|---|---:|---|
| `half_year_finances_2025.csv` | 31 | Council receipts, payments, subtotals, totals and net balance, January-June 2025 |
| `cdf_performance_indicators_2025.csv` | 7 | CDF indicators and explanations, as at 30 June 2025 |
| `cdf_project_progress_2023_q1.csv` | 8 | Five procurements in progress and three signed contracts, first quarter 2023 |

## Source selection

- Inventory 31: one-page 2025 biannual performance report, financial tables. Selectable PDF text is extracted with pdfplumber. Figures were compared with page 1 of the signed report, inventory 36.
- Inventory 36: signed January-June 2025 report, page 4, CDF block A1-A11. Seven indicator rows are extracted; heading rows are excluded. Inventory 37 appears to reproduce the same signed report and is not counted again.
- Inventory 75: first-quarter 2023 procurement report dated 15 April 2023, Part A on pages 2-3 and Part C on pages 8-9. These sections explicitly identify GRZ-CDF funding.
- Inventory 88 is an empty beneficiary template despite its community-project download title. Inventory 90 is another approved-project list, not an implementation report. Neither provides progress observations.

The remaining council output indicators, internal audit recommendations, arrears, procurement transactions and newsletter content have not been extracted in this step. This is a focused CDF extraction, not a complete transcription of every report.

## Fields and meaning

`period_start` and `period_end` describe the reporting period, not the approval year or the date the file was uploaded. `source_page` counts from the first PDF page. `source_page_end` records descriptions continuing onto another page.

Half-year finance fields are `section`, `category`, `row_type`, `source_code`, `description`, `annual_budget_zmw`, `actual_to_date_zmw`, `reported_variance_zmw`, `performance_as_printed`, source and notes. The reported variance is **budget minus actual**. It has the opposite sign to the calculated variance in the earlier annual comparison dataset. These are six-month actuals against an annual budget, not full-year actuals. Do not add totals and subtotals to their detail rows.

CDF indicator fields include `indicator_code`, `programme`, `indicator`, `unit`, `target`, `actual`, `reported_variance` and `comment`. Percentage indicators describe the council's aggregate programme. For example, 20% of community projects implemented does not mean every project is 20% complete.

Progress fields include the reported description, tender/contract number, procurement method, funding source, approval and signing dates, `amount_zmw`, `amount_type`, `reported_stage`, `execution_percent` and contractor. Estimated amounts and contract values are **not actual payments or disbursements**. The five procurement-stage records do not provide physical execution percentages. Blank percentages must not be treated as zero.

## Linking projects

Six of the eight progress records are linked by reviewed location and compatible work descriptions to the 2022 approved list: Siabulembo, Chisamu, Hambuto, Munenga, Machavika and Hamunjo. These links are inferences, not official shared identifiers. `approved_year`, `approved_project_no`, `approved_project_name`, `approved_ward`, `approved_source_url` and `approved_source_page` show the linked approval. The ward comes from that approval, not the procurement report.

Velu remains unlinked because its description is less specific than the approval's scope. Lusitu East remains unlinked because no matching classroom approval was found in the selected annual lists; its 2024 entry concerns a staff house. The source reuses tender numbers for different descriptions, so tender number alone is not a unique project identifier. Original approvals are not overwritten with these historical statuses.

## Cleaning and source issues

- Scanned pages were rendered, rotated where needed, and read with RapidOCR. Column and row boundaries group the text. Whitespace and line-wrapped money/dates are cleaned; duplicate records are removed.
- Chisamu's description continues onto page 3; Hamunjo's final word continues onto page 9. These continuations are joined.
- Hamunjo's 61.25% execution figure was restored from the image because OCR merged it with the manager column. The other reported figures are Munenga 65% and Machavika 70%, all for Q1 2023. They are not current completion statuses.
- A clipped final word in indicator A11 is completed as “sponsored” and noted.
- The half-year source's `Others OSR` actual amount is printed as 355,200, while its variance implies a 0.10 difference. Printed amounts are retained.
- `performance_as_printed` intentionally retains `#DIV/0!`, a total shown as `0.40`, and an implausible net percentage. These are source formatting/formula issues, not reliable numeric percentages. The net budget row also prints 0.01. Notes identify this issue rather than silently replacing source values.
- Missing/dashed monetary values remain missing; explicitly printed zeroes are retained.
