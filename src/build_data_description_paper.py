"""Build the CSC 4792 Data in Brief-style data description PDF."""

from pathlib import Path
from xml.sax.saxutils import escape
import csv

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, KeepTogether, ListFlowable, ListItem,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "chirundu_cdf_data_description_paper.pdf"
CSV_ROOT = ROOT / "data" / "processed"
FILES = [p for p in sorted(CSV_ROOT.rglob("*.csv")) if "cdf_pilot" not in p.parts]
assert len(FILES) == 10

def nrows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle, delimiter="|"))

counts = {p.name.removeprefix("db-unza26-csc4792-chirundu_"): nrows(p) for p in FILES}
assert sum(counts.values()) == 730

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#2C607C")
PALE = colors.HexColor("#EAF1F5")
GRAY = colors.HexColor("#52606B")
RULE = colors.HexColor("#CFDCE4")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", fontName="Helvetica-Bold", fontSize=17,
    leading=20.5, textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle(name="BylineCustom", fontName="Helvetica", fontSize=9,
    leading=12, textColor=GRAY, spaceAfter=12))
styles.add(ParagraphStyle(name="H1Custom", fontName="Helvetica-Bold", fontSize=11.5,
    leading=14, textColor=NAVY, spaceBefore=11, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="H2Custom", fontName="Helvetica-Bold", fontSize=9.7,
    leading=12, textColor=BLUE, spaceBefore=7, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="BodyCustom", fontName="Helvetica", fontSize=9.2,
    leading=13.3, spaceAfter=6, textColor=colors.HexColor("#1E2830")))
styles.add(ParagraphStyle(name="SmallCustom", fontName="Helvetica", fontSize=8.2,
    leading=11.4, spaceAfter=5, textColor=colors.HexColor("#26333C")))
styles.add(ParagraphStyle(name="TableLabelCustom", fontName="Helvetica-Bold", fontSize=8.1,
    leading=10.4, textColor=NAVY))
styles.add(ParagraphStyle(name="TableValueCustom", fontName="Helvetica", fontSize=8.1,
    leading=10.4, textColor=colors.HexColor("#1E2830")))
styles.add(ParagraphStyle(name="CaptionCustom", fontName="Helvetica-Bold", fontSize=8.3,
    leading=11, textColor=NAVY, spaceBefore=7, spaceAfter=4))
styles.add(ParagraphStyle(name="RefCustom", fontName="Helvetica", fontSize=8,
    leading=11, spaceAfter=4, textColor=colors.HexColor("#27343D"), wordWrap="CJK"))

def P(text, sty="BodyCustom"):
    return Paragraph(text, styles[sty])

def heading(text):
    return P(text, "H1Custom")

def subheading(text):
    return P(text, "H2Custom")

def bullet(text):
    return P("<font color='#2C607C'>&bull;</font>  " + text, "BodyCustom")

def table(rows, widths, header=False, font=8.1):
    data = []
    for i, row in enumerate(rows):
        data.append([P(escape(str(x)), "TableLabelCustom" if (header and i == 0) or (not header and j == 0) else "TableValueCustom")
                     for j, x in enumerate(row)])
    t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, RULE),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), PALE),
                 ("LINEBELOW", (0, 0), (-1, 0), 0.7, BLUE)]
    else:
        cmds += [("BACKGROUND", (0, 0), (0, -1), PALE)]
    t.setStyle(TableStyle(cmds))
    return t

PAGE_W, PAGE_H = A4
MARGIN_X = 19 * mm
FRAME_W = PAGE_W - 2 * MARGIN_X

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.line(MARGIN_X, PAGE_H - 17 * mm, PAGE_W - MARGIN_X, PAGE_H - 17 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(MARGIN_X, PAGE_H - 14 * mm, "CSC 4792  |  DATA DESCRIPTION PAPER")
    canvas.drawRightString(PAGE_W - MARGIN_X, 13 * mm, f"{doc.page}")
    canvas.restoreState()

OUT.parent.mkdir(parents=True, exist_ok=True)
doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=MARGIN_X,
    rightMargin=MARGIN_X, topMargin=22 * mm, bottomMargin=19 * mm,
    title="Chirundu Town Council CDF and Local Finance Data, 2022-2026",
    author="CSC 4792 Group 39")
frame = Frame(MARGIN_X, 19 * mm, FRAME_W, PAGE_H - 41 * mm,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=on_page))

story = []
story += [
    P("Chirundu Town Council constituency development and local finance data, 2022-2026", "TitleCustom"),
    P("CSC 4792 Data Mining and Warehousing - Group 39, University of Zambia<br/>Data article prepared 14 September 2026", "BylineCustom"),
    heading("Abstract"),
    P("This data article describes ten pipe-delimited CSV tables curated from 16 published Chirundu Town Council PDF documents. The 730 records cover annual Constituency Development Fund (CDF) approved community-project lists for 2022-2026, budget programmes and revenue estimates, signed financial-statement lines for 2022-2024, and selected 2023 and 2025 performance reports. Each extracted record retains a source URL and one-based PDF page reference. Scanned pages were processed with optical character recognition and checked against the source images; selectable-text PDFs were parsed directly. The tables preserve source labels and reported monetary units, distinguish budgeted, actual, estimated and contract values, and retain missing information rather than converting it to zero. The data files and a reproducible Jupyter notebook accompany the course project; a public repository identifier was not available when this paper was prepared."),
    P("<b>Keywords:</b> local government; Zambia; Chirundu; Constituency Development Fund; public finance; administrative data", "SmallCustom"),
    heading("Specifications table"),
]

spec = [
    ("Subject", "Public administration; local government finance"),
    ("Specific subject area", "Constituency Development Fund projects, council budgets and performance reporting in Chirundu, Zambia"),
    ("Type of data", "Ten structured CSV tables; source documents are council PDFs"),
    ("Data collection", "Document retrieval from the council website; selectable-text extraction and OCR-assisted transcription of scanned tables; manual image review"),
    ("Data format", "Curated UTF-8 CSV with pipe (|) delimiters; blank cells represent unavailable values"),
    ("Data source location", "Chirundu Town Council, Chirundu District, Zambia; https://www.chirunducouncil.gov.zm"),
    ("Data accessibility", "Ten CSV files in the accompanying course project under data/processed/. No verified public dataset URL or persistent identifier was available at preparation."),
    ("Related work", "CSC 4792 group project notebook: notebooks/chirundu_cdf_project.ipynb"),
]
story.append(table(spec, [43 * mm, FRAME_W - 43 * mm]))

story += [PageBreak(), heading("Value of the Data"),
    bullet("Year-labelled, source-linked tables let users audit how local council project approvals and financial lines were recorded across successive publications."),
    bullet("Researchers and civic analysts can compare the availability and structure of CDF, budget, revenue and performance data across years and, with equivalent council data, across local authorities."),
    bullet("The separation of approved projects, allocations, financial statements and progress observations supports reuse without treating approval or budget figures as expenditure or completed outputs."),
    bullet("Page-level provenance, recorded ambiguities and reproducible extraction steps support correction, extension and future linkage to later council reports."),
    heading("1. Data Description"),
    P("The release consists of the ten curated files in Table 1. File names share the required prefix <b>db-unza26-csc4792-chirundu_</b>. All files are UTF-8 text with a pipe delimiter and a header row. Counts refer to source-table observations, not necessarily independent projects or transactions. The 2025 pilot extraction files are retained separately for process comparison and are excluded from the release to avoid duplicate project rows."),
    P("Table 1. Curated data files, units of observation and coverage.", "CaptionCustom"),
]

inventory = [
    ("File suffix (.csv)", "Rows", "Unit of observation and coverage"),
    ("cdf_approved_projects_2022_2026", "83", "One numbered annual approved-list entry; 2022-2026"),
    ("budget_programmes", "70", "One printed programme allocation; 2022-2026"),
    ("cdf_budget_subprogrammes", "22", "One CDF subprogramme allocation; 2022-2026"),
    ("budget_revenue", "231", "One detailed revenue estimate; 2022, 2023, 2025, 2026"),
    ("budget_totals", "5", "One printed annual council budget total; 2022-2026"),
    ("financial_statements", "207", "One cash-statement line; 2022-2024"),
    ("budget_vs_actual", "66", "One final-budget/actual comparison line; 2022-2024"),
    ("cdf_project_progress_2023_q1", "8", "One procurement or contract observation; Q1 2023"),
    ("cdf_performance_indicators_2025", "7", "One CDF indicator; to 30 June 2025"),
    ("half_year_finances_2025", "31", "One half-year finance line; January-June 2025"),
    ("Total", "730", "Ten distinct files"),
]
story.append(table(inventory, [70 * mm, 13 * mm, FRAME_W - 83 * mm], header=True))
story += [
    Spacer(1, 6),
    P("Approved-project records contain <i>project_no</i>, <i>year</i>, project text, source-given sector and place fields, approval wording, optional amount/type, and provenance. A row identifies an entry in a year's published list: projects may recur across years. Budget records retain programme or revenue codes and values in Zambian kwacha (ZMW). Statement and comparison records use <i>statement</i>, <i>section</i> and <i>row_type</i> to distinguish detail, subtotal, total and balance rows. Performance tables include reporting periods, indicator targets and actuals, or procurement stages and contract information."),
    P("The project lists contain 16, 19, 15, 14 and 19 entries for 2022 through 2026, respectively. Only one approved-list row contains an explicit monetary value; all 83 <i>implementation_status</i> cells are blank because those lists do not report implementation progress. The separate 2023 progress table reports eight historical procurement/contract observations, six linked by reviewed descriptions and locations to 2022 approvals. These links are documented in the table and are not official identifiers."),
]

story += [PageBreak(), heading("2. Experimental Design, Materials and Methods"),
    subheading("2.1 Source selection and acquisition"),
    P("The source universe was the council's public web documents. A download inventory records 104 files across CDF, finance, performance, procurement, planning, governance and other categories. This release uses 16 distinct source PDFs: five selected annual approved-project lists, five annual budgets, three signed annual financial reports, two 2025 half-year performance reports and one 2023 procurement report. Duplicate copies and alternative lists were not appended. The approved-project sources are inventory items 001, 002, 003, 059 and 005. Every output row stores its original <i>source_url</i> and one-based <i>source_page</i>. The source year is taken from the annual list or report heading, not a web upload timestamp."),
    subheading("2.2 Extraction and curation"),
    P("The accompanying Jupyter notebook reproduces extraction and cleaning. For selectable-text pages, pdfplumber captured text and tabular positions. Scanned pages were rendered to images and read with RapidOCR using the English recognition model; table-specific row and column boundaries reconstructed records. A rotated 2023 project-list page was corrected before OCR. Raw OCR and intermediate page output are retained under <i>data/interim/</i>. The 2025 approved-project list is demonstrated step by step in the notebook. Extracted records were checked against source images, especially around stamps, borders, wrapped labels and amount signs, and documented corrections were applied before export."),
    P("Cleaning trims spacing, joins wrapped descriptions, parses printed ZMW values without thousands separators, removes duplicate extracted rows and preserves source wording when harmonisation would be uncertain. Blank or dashed amounts remain blank; explicitly printed zeroes remain zero. Table-specific notes record obscured cells, restored text and mismatches in source totals. The notebook exports the ten CSV files and the project README files explain each table's fields and exceptions."),
    subheading("2.3 Variables and derived fields"),
    P("The files are related by source year and provenance, but they are not a single transaction ledger. <i>project_no</i> is unique only within a year's approved list. <i>period_start</i> and <i>period_end</i> identify performance-report windows, which differ from approval years. In <i>budget_vs_actual</i>, <i>calculated_variance_zmw = actual_amount_zmw - final_budget_zmw</i>; a missing input yields a missing variance. In <i>half_year_finances_2025</i>, <i>reported_variance_zmw</i> is the source's budget-minus-actual figure, so its sign convention is different. The printed percentage-like field is retained as text where it includes formula errors or implausible displays."),
    subheading("2.4 Verification and limits"),
    P("The release was checked for parseable pipe-delimited records, row counts, year coverage and page-level source links. Its 730 rows all have a source URL. Source anomalies remain visible: the 2025 CDF programme allocation differs by K1 from its subprogramme total; several statement totals and category values differ by K1; and the 2023 financial comparison and cash statement disagree on two receipt lines. These were not silently reconciled. A 2023 statement has a closing-balance label with the wrong printed year. The 2025 report includes source formula artefacts such as <i>#DIV/0!</i>."),
    P("The selected documents do not establish all requested council functions or all project-level disbursements. There is no detailed revenue schedule in the selected 2024 budget and no 2025-2026 actual annual financial statement in this extraction. Approved-list status is not proof of implementation; estimated procurement and contract amounts are not actual payments. Council totals overlap with fund totals, and detail rows overlap with subtotals. Analyses must filter <i>row_type</i> and respect these distinctions before summing values. Ward spelling varies between source years; ward-level linkage needs further review."),
]

story += [PageBreak(), heading("3. Data Access and Reuse"),
    P("The ten CSV files are stored under <i>data/processed/cdf_projects/</i>, <i>data/processed/finance/</i> and <i>data/processed/performance/</i> in the accompanying course project. The Jupyter notebook and intermediate OCR records provide the processing trail. Each CSV embeds links to its primary council PDFs; the source inventory also records the downloaded documents. A verified public Kaggle URL or persistent identifier was not present in the workspace at preparation, so readers should use the accompanying project files until the team supplies a public repository record. Public repository deposition is required before claiming journal-level data accessibility."),
    P("Reuse should preserve attribution to Chirundu Town Council as the source publisher and cite the specific PDF URLs in the rows used. The released tables contain public project, financial and report information rather than newly collected participant responses. The manuscript does not redistribute unextracted beneficiary lists; users seeking to extend the corpus should review personal-data and source-use requirements before publication."),
    heading("Declaration of competing interest"),
    P("No competing interest information was provided in the project materials. The author group should confirm this statement before external submission."),
    heading("References"),
    P("[1] Chirundu Town Council. Official council document portal and published PDF documents. https://www.chirunducouncil.gov.zm (source-specific URLs and pages are recorded in each CSV).", "RefCustom"),
    P("[2] CSC 4792 Data Mining and Warehousing. Mini Project Practical Assignment, 4 September 2026, University of Zambia. Local assignment brief supplied with the project.", "RefCustom"),
    P("[3] H.-R. Wang. How to write a good Data in Brief article. Elsevier Researcher Academy, June 2024. https://researcheracademy.elsevier.com/uploads/2024-07/Quick_guide_Data_in_brief.pdf", "RefCustom"),
    P("[4] Data in Brief. Guide for Authors. https://www.sciencedirect.com/journal/data-in-brief/publish/guide-for-authors (accessed 14 September 2026).", "RefCustom"),
]

doc.build(story)
print(OUT)
