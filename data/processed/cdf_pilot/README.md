# 2025 CDF sample

Open `notebooks/chirundu_cdf_project.ipynb` and run the cells in order. Install the packages in `src/requirements-cdf-pilot.txt` if needed.

The current output is `db-unza26-csc4792-chirundu_cdf_projects_2025_ocr_sample.csv`. It contains 14 entries from the detailed 2025 approved-project list. The notebook now runs RapidOCR on the scanned page, groups the text by table position and cleans it using pandas. Eight cell corrections read from the source are shown in the notebook. It is OCR-assisted extraction with manual cleaning, not a fully automatic or complete assignment dataset.

Use the project's `.venv` Python interpreter in your notebook editor. To set up another environment, install `src/requirements-cdf-pilot.txt` and obtain the English model as explained in `models/README.md`. All notebook cells have been run successfully through a Jupyter kernel.

The earlier manually transcribed sample is retained only for comparison. It incorrectly spelled row 10's ward as Nkadabwe; the OCR output and PDF show Nkaddabwe, which the current output retains. Do not combine the manual sample and OCR sample as separate project records.

Raw OCR text and its uncorrected table are in `data/interim/ocr_2025/`. The table boundaries are specific to this PDF and render scale. Other years need their own layout handling.

The CSV uses `|` as its separator. Empty cells mean the information was not reported.

| Column | Description |
|---|---|
| project_no | Row number in the source table |
| year | CDF list year from the heading |
| project_name | Project description |
| ward | Ward name with consistent capitalisation |
| zone | Zone listed in the source |
| location | Location listed in the source |
| approval_comment | Approval wording, including any restrictions |
| amount_zmw | Amount in kwacha; not provided in this list |
| implementation_status | Progress status; not provided in this list |
| source_url | Document URL for referencing |
| source_page | Page containing the record |

Project 11's comment approves only a motor grader, although its project name lists three types of machinery. Missing locations are left blank. Approval does not establish spending or completion.

