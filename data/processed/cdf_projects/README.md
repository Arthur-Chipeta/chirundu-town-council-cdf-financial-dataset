# Chirundu CDF approved-project lists, 2022–2026

The main file is `db-unza26-csc4792-chirundu_cdf_approved_projects_2022_2026.csv`. It contains 83 entries from five selected annual approved-project lists. Use this file instead of adding the earlier 2025 sample to it again.

| List year | Records |
|---|---:|
| 2022 | 16 |
| 2023 | 19 |
| 2024 | 15 |
| 2025 | 14 |
| 2026 | 19 |

These are annual list entries, not necessarily 83 different physical projects. Some projects reappear for additional works in later years. The 2026 list explicitly includes work on two 2024 projects.

## How the table was made

Run `notebooks/chirundu_cdf_project.ipynb` using the project's `.venv` Python interpreter. The notebook converts scanned pages to images, runs English OCR, groups text by measured table positions, applies visible manual corrections and exports the CSV. The second 2023 page is rotated before OCR. The row positions exclude the 2026 ward headings.

All extraction functions, page layouts and manual corrections are included directly in section 3 of the notebook. The 2025 example is shown step by step. No local Python scripts are imported. Raw OCR output is kept in `data/interim/ocr_2025/` and `data/interim/cdf_other_years/`.

## Columns

The file is UTF-8, with `|` as the separator. Empty cells mean unavailable, not zero.

| Column | Meaning |
|---|---|
| project_no | Number printed in that year's source list; not a unique project ID across years |
| year | Annual list year, not a payment or completion date |
| project_name | Project name read from the source |
| project_description | Separate description, where the source provides one |
| sector | Sector given by the source; not guessed from the project name |
| ward | Source ward text, including multiple-ward and all-wards entries |
| zone | Zone where reported |
| location | Site or location where reported |
| work_item | Item details from the 2026 table; multiple sites/items remain in source order |
| approval_status | Approved-list membership; the 2025 machinery entry has a scope restriction |
| approval_comment | Actual approval comment, where the source provides it |
| amount_zmw | Monetary amount explicitly reported in the source |
| amount_type | Meaning of the reported amount |
| implementation_status | Actual progress; not established by these lists and left blank |
| source_url | Original council PDF URL |
| source_page | One-based PDF page number |
| notes | Source ambiguities, unreadable cells or details needed to interpret a record |

## Interpretation

- The council download titles identify the 2022–2024 list years. Later stamps do not change their year labels. The 2025 and 2026 headings also state their years.
- The selected sources are inventory entries 001, 002, 003, 059 and 005. Other copies and alternative versions are not appended to this table.
- The one recorded amount, ZMW1,746,363.23, is the stated value of supplying desks in the 2022 list. It is not labelled as an allocation, disbursement or actual expenditure.
- The last three 2024 entries do not state a ward. Locations obscured by stamps stay blank where they cannot be read.
- Source spelling differences are retained. For example, related ward spellings vary between lists. They should not be merged automatically for ward-level analysis without further checking.
- A 2023 entry covers several wards, and a 2026 entry covers two schools. Each remains one numbered source record.
- The 2025 machinery description lists three types of equipment but its approval comment covers only the motor grader.
- OCR required manual corrections, particularly near stamps and column borders. Those edits are documented in the notebook; this is not fully automatic extraction.

The consolidated notebook now also includes proposed 2022-2024 projects, the 2025 approval-decision list and member project-type labels. These remain separate tables because their rows have different meanings. Planning, governance and other CDF categories remain outside this dataset.
