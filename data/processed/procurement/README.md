# Annual procurement plans

Run section 10 of `notebooks/chirundu_cdf_project.ipynb` or `src/extract_procurement.py` from the project root. Both contain the same extraction functions. The source files are inventory 076 (2023 PDF), 070 (2025 PDF) and 069 (2026 Excel workbook). The 2025 plan spans two table pages; records are matched by their printed row numbers, and the text corrections are explicit in `DESCRIPTION_FIXES`.

Files use UTF-8 and the pipe (`|`) separator. `estimated_amount_zmw` is planned spending, `planned_award_date` is a scheduled milestone, and `source_page` identifies the PDF page or Excel sheet. Missing information is left blank. Row counts are 46 (2023), 50 (2025) and 60 (2026). The 2026 workbook requires `xlrd`.
