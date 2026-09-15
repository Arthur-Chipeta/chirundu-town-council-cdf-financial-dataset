# Chirundu budgets and financial statements

These six tables were extracted from five annual budgets and three signed financial reports. They use UTF-8 encoding, a pipe (`|`) separator, blank cells for missing values, and amounts in Zambian Kwacha (ZMW). Sections 4–5 of `notebooks/chirundu_cdf_project.ipynb` reproduce them after the setup cells. All extraction functions and page layouts are defined inside the notebook.

| CSV filename after `db-unza26-csc4792-chirundu_` | Rows | Coverage |
|---|---:|---|
| `budget_programmes.csv` | 70 | Programme allocations, 2022–2026 |
| `cdf_budget_subprogrammes.csv` | 22 | CDF subprogramme allocations, 2022–2026 |
| `budget_revenue.csv` | 231 | Detailed revenue estimates, 2022, 2023, 2025 and 2026 |
| `budget_totals.csv` | 5 | Printed annual council budget totals, 2022–2026 |
| `financial_statements.csv` | 207 | Main cash receipts, payments and balances, 2022–2024 |
| `budget_vs_actual.csv` | 66 | Final budgets and actual amounts, 2022–2024 |

## Columns and interpretation

All tables contain `year`, `source_url` and `source_page`. Page numbers start at the first PDF page, including any cover. Budget rows use the year of the budget, and financial rows use the year in the statement heading. Prior-year comparison figures and future estimates are excluded.

Budget tables contain `amount_zmw`. Programme and subprogramme tables retain the source's codes and descriptions. Revenue records include `category`, `revenue_code`, `revenue_description` and `notes`. Codes are identifiers, so read these columns as strings if leading zeroes matter.

Financial tables contain `statement` (Council, CDF, LGEF, ZDSP capital grant or Sector grant), `section` (receipts, payments or cash balance), optional `subsection` (operational or capital), `row_type` (detail, subtotal, total or balance), `description`, `amount_zmw` and `notes`.

The comparison table uses `final_budget_zmw` and `actual_amount_zmw`. Its `calculated_variance_zmw` is actual minus final budget, computed from those two columns; it is not a transcription of the source's printed variance. Missing inputs produce a missing variance. For payments, a positive difference means spending exceeded the final budget.

## Cleaning and limitations

- Text budgets were read using pdfplumber. Scanned statements were rendered and read using RapidOCR. Page positions separate descriptions from figures. Cleaning removes thousands separators, trims text, converts amounts and removes duplicate rows.
- Four labels obscured by a stamp in the 2022 council cash statement were restored from the image. Split labels and OCR spelling were corrected. The missed minus sign on the 2023 CDF cash decrease was restored.
- The 2025 K8,340,000 revenue description, `Capital Grant Credit ($300k)`, was restored from the image because text extraction omitted it. Its category heading is blank in the source and remains missing.
- Dashes and blank amount cells remain missing; explicitly printed zeroes remain zero. Missing does not mean an invented zero.
- There is no detailed revenue schedule in the selected 2024 annual budget. The separate 2024 budget-versus-actual table does contain final budget categories. No 2025–2026 actual financial statements are included in this extraction.
- Published amounts are retained even when totals differ by K1 from their components. For example, the 2025 CDF programme budget is K36,058,150, while its subprogrammes and revenue line total K36,058,151. The 2024 LGEF total payments are printed as K10,189,906, although the two subtotals sum to K10,189,907.
- The 2023 cash statement reports Commercial Venture of K77,959 and Other Receipts of K317,359, while its comparison table reports K77,958 and K317,360. These differences were not silently reconciled.
- The 2024 ZDSP statement reports funding of K2,694,737; the main council statement's Other Grants line reports K2,694,736.
- The 2023 CDF closing-balance label says “31 December 2022” within the 2023 statement. Its original label and a note are retained.
- The 2024 CDF receipts include K10,000,000 of funding and K675,337 of loan repayments. Total receipts are not the same as a fresh government allocation.
- Council totals include fund activity. Do not sum council totals together with CDF/LGEF totals. Do not sum detail rows together with their subtotals and totals. Budget and CDF subprogramme tables also overlap.

The consolidated notebook also validates and combines the wider member financial extracts for 2022-2025 and OBB extracts for 2023-2026. The year-specific files and combined `financial_detail_2022_2025.csv` and `obb_detail_2023_2026.csv` are stored here. Their source extraction notebooks are archived under `data/interim/member_notebooks/`. These additions contain supporting notes and programme outputs, but do not establish complete coverage of every transaction or project-level status.
