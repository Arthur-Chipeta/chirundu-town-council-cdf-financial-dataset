# Chirundu processed datasets

The canonical workflow is [`notebooks/chirundu_cdf_project.ipynb`](../../notebooks/chirundu_cdf_project.ipynb). Run its cells in order from the project root with the packages in `src/requirements-cdf-pilot.txt`. Every released CSV is UTF-8, pipe (`|`) separated, and begins `db-unza26-csc4792-` as required by the CSC 4792 assignment.

- `cdf_projects/` contains approved 2022-2026 lists, member project-type labels, proposed 2022-2024 lists and the 2025 approved/unapproved decision list. These source documents describe different stages; do not treat every proposal as funded.
- `finance/` contains the consistent budget and signed-statement extracts plus the wider year-specific member financial and OBB extracts. `financial_detail_2022_2025.csv` and `obb_detail_2023_2026.csv` combine the latter without changing their mixed schemas.
- `performance/` contains 2023 project progress and 2025 half-year financial and CDF indicator tables.
- `procurement/` contains planned procurement records from the 2023 and 2025 PDFs and 2026 `.xls` workbook. Estimates and planned dates are not confirmed contracts or spending.
- `cdf_pilot/` holds two early 2025 OCR samples for comparison, not additional released observations.

The original member notebooks are preserved as source material under `data/interim/member_notebooks/`. One supplied notebook, `final_extract_chirundu_cdf_2023.ipynb`, was empty; its corresponding classified-project CSV is present. The manually curated detailed finance and OBB CSVs are checked and combined in the main notebook; their original extraction steps remain in the archived member notebooks. The council source PDFs and download inventory are under `data/raw/` and `data/source_inventory/`.

The 2022 and 2023 proposed-project PDFs each print the same 35 project names and applied amounts. Nine member-transcribed amounts disagreed with the scanned pages; section 8 of the notebook records the image-checked corrections before export. The two annual files remain separate because their source documents and years differ.

The existing Data in Brief paper under `output/` describes the earlier ten-table release. Its table inventory and row counts need revision before it is submitted alongside this expanded dataset.
