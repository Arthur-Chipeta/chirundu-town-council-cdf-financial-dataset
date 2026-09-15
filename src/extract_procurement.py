"""Extract Chirundu annual procurement plans for 2023, 2025 and 2026.

The consolidated notebook includes this same code so it can run independently.
"""
from pathlib import Path
import re

import pandas as pd
import pdfplumber


def clean_amount(value):
    value = re.sub(r'[^0-9.]', '', str(value or ''))
    return pd.to_numeric(value, errors='coerce')


def export_plan(df, year, source, output_dir, source_page):
    df = df.rename(columns={
        'Category': 'category', 'Procurement item': 'procurement_item',
        'Estimated Amount': 'estimated_amount_zmw',
        'Source of Funds': 'source_of_funds',
        'Procurement Method': 'procurement_method', 'date': 'planned_award_date',
    })
    cols = ['category', 'procurement_item', 'estimated_amount_zmw',
            'source_of_funds', 'procurement_method', 'planned_award_date']
    df = df.reindex(columns=cols).copy()
    df['year'] = year
    df['source_document'] = source.name
    df['source_page'] = source_page
    df['estimated_amount_zmw'] = df['estimated_amount_zmw'].map(clean_amount)
    df['category'] = df['category'].astype('string').str.strip().str.lower()
    df['procurement_item'] = df['procurement_item'].astype('string').str.replace(r'\s+', ' ', regex=True).str.strip()
    df['source_of_funds'] = df['source_of_funds'].astype('string').str.replace(r'\s+', ' ', regex=True).str.strip()
    df['source_of_funds'] = df['source_of_funds'].str.replace(r'Local ResouNrces', 'Local resources', regex=False)
    df['procurement_method'] = df['procurement_method'].astype('string').str.strip().str.lower()
    date_format = '%d-%m-%y' if year == 2023 else '%m/%d/%Y' if year == 2025 else None
    df['planned_award_date'] = pd.to_datetime(df['planned_award_date'], format=date_format, errors='coerce').dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['procurement_item']).drop_duplicates().reset_index(drop=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f'db-unza26-csc4792-chirundu_procurement_plan_{year}.csv'
    df.to_csv(output, sep='|', index=False, encoding='utf-8')
    return df


def extract_2023(source_dir, output_dir):
    pdf_path = next(source_dir.glob('076--*'))
    columns = {
        'Category': (50, 113), 'Procurement item': (196, 341),
        'Estimated Amount': (524, 548), 'Source of Funds': (589, 637),
        'Procurement Method': (637, 661), 'date': (695, 730),
    }
    with pdfplumber.open(pdf_path) as pdf:
        words = pdf.pages[0].extract_words()
    rows = []
    for word in words:
        if word['top'] < 165:
            continue
        row = next((r for r in rows if abs(r['top'] - word['top']) <= 2), None)
        if row is None:
            row = {'top': word['top'], 'words': []}
            rows.append(row)
        row['words'].append(word)
    records = [
        {name: ' '.join(w['text'] for w in row['words'] if left <= w['x0'] < right).strip()
         for name, (left, right) in columns.items()}
        for row in sorted(rows, key=lambda r: r['top'])
    ]
    raw = pd.DataFrame(records)
    classes = {'goods', 'works', 'non consulting services', 'consulting services'}
    raw = raw[raw['Category'].str.lower().isin(classes)].copy()
    raw['Procurement item'] = raw['Procurement item'].str.replace(r'^0+', '', regex=True)
    result = export_plan(raw, 2023, pdf_path, output_dir, 1)
    assert len(result) > 20
    return result


# Exact substitutions recorded during the member's row-by-row review of the 2025 PDF.
DESCRIPTION_FIXES = {
    'acceEssaocrhies': 'accessories', 'servicesE': 'services',
    'accessoriesE)ach': 'accessories', 'WDC 1p8rojects': 'WDC projects',
    'SerivEeasc)h': 'Services)', 'Comm1u9nity': 'Community',
    'Cleani2n0g': 'Cleaning', 'procur2e1ment': 'procurement',
    'genera2l2': 'general', 'Abl2u3tion': 'Ablution',
    'opposEitaec': 'opposite', 'Aba2t4toir': 'Abattoir',
    'maintenance2 a5nd': 'maintenance and', 'township2 6roads': 'township roads',
    'com27pletion': 'completion', 'undeEr': 'under',
    'Co2m8munity': 'Community', '2w9ater': 'water',
    'Sola3r 0powered': 'Solar powered', 'Abl3u1tion': 'Ablution',
    'towns3h2ip': 'township', 'L3a3trine': 'Latrine',
    'Kaban3a4na': 'Kabana', 'mainte3n5ance': 'maintenance',
    'e3q6uipment': 'equipment', 'S3ta7tionery': 'Stationery',
    '3C8ouncil': 'Council', 'differentE': 'different',
    'WDC 3p9rojects': 'WDC projects', 'SocEiaacl': 'Social',
    'WDC 4p0rojects': 'WDC projects', 'SEoacciahl': 'Social',
    'WDC 4p1rojects': 'WDC projects', 'anEd': 'and',
    'WDC 4p2rojects': 'WDC projects', 'SoEcaiaclh': 'Social',
    'WDC 4p3rojects': 'WDC projects', 'CommunEitay': 'Community',
    'WDC 4p4rojects': 'WDC projects', 'WDC 4p5rojects': 'WDC projects',
    'WDC 4p6rojects': 'WDC projects', 'WDC 4p7rojects': 'WDC projects',
    'anEda': 'and', 'WDC 4p8rojects': 'WDC projects',
    'aEnadc': 'and', 'WDC 4p9rojects': 'WDC projects',
    'CommunityE': 'Community', 't5o0ols': 'tools',
    'AdditiEoancahl': 'Additional',
}

# The PDF text layer also inserts the reference number and unit into some words.
# These corrections were checked against the member's row review and page text.
ROW_DESCRIPTION_FIXES = {
    2: {'officestationery': 'office stationery'},
    3: {'Office3': 'Office'},
    10: {'t1o0ols': 'tools'},
    11: {'a1n1d': 'and'},
    12: {'Shir1ts2': 'Shirts'},
    13: {'sports1 a3ttires': 'sports attires'},
    14: {'adver1ts4': 'adverts', 'daechvices': ''},
    15: {'Brand1in5g': 'Branding'},
    16: {'Zesco1 u6nits': 'Zesco units'},
    17: {'se1rv7ices': 'services'},
    20: {'Esuapcphlies': 'supplies'},
    23: {'Chhirundu': 'Chirundu'},
    27: {'athceh': 'the'},
    38: {'inascthituion': 'institution'},
    39: {'hSerives': 'Services'},
    40: {'Serives': 'Services'},
    41: {'aScohcial': 'Social', 'Serives': 'Services'},
    42: {'Serives': 'Services'},
    43: {'cahnd': 'and', 'Serives': 'Services'},
    44: {'andE Sacohcial': 'and Social', 'Serives': 'Services'},
    45: {'SEoaccihal': 'Social', 'Serives': 'Services'},
    46: {'andE aScohcial': 'and Social', 'Serives': 'Services'},
    47: {'anda Schocial': 'and Social', 'Serives': 'Services'},
    48: {'Shocial': 'Social', 'Serives': 'Services'},
    49: {'aanchd': 'and', 'Serives': 'Services'},
}


def extract_2025(source_dir, output_dir):
    pdf_path = next(source_dir.glob('070--*'))
    with pdfplumber.open(pdf_path) as pdf:
        left = pdf.pages[0].extract_tables()[0]
        right = pdf.pages[1].extract_tables()[0]
        text_lines = pdf.pages[0].extract_text().splitlines()
    left = {int(r[0]): r for r in left if r[0] and str(r[0]).isdigit() and 11 <= int(r[0]) <= 60}
    right = {int(r[0]): r for r in right if r[0] and str(r[0]).isdigit() and 11 <= int(r[0]) <= 60}
    assert set(left) == set(right) == set(range(11, 61))
    descriptions = {}
    for line in text_lines:
        match = re.match(r'^(\d+) (?:goods|works|consulting services|non consulting services) \d+ 0 (.*)$', line)
        if match and 11 <= int(match.group(1)) <= 60:
            # The text layer has the full description; table cell boundaries cut words.
            descriptions[int(match.group(1))] = re.sub(
                r'\s+(?:\d[\d,]*\.\d{2}|#+)\s+\d[\d,]*\.\d{2}$', '', match.group(2)
            )
    assert set(descriptions) == set(range(11, 61))
    records = []
    for row_no in range(11, 61):
        a, b = left[row_no], right[row_no]
        description = descriptions[row_no]
        for bad, good in DESCRIPTION_FIXES.items():
            description = description.replace(bad, good)
        ref_no = row_no - 10
        for bad, good in ROW_DESCRIPTION_FIXES.get(ref_no, {}).items():
            description = description.replace(bad, good)
        # Ref numbers may be inserted within a word by the PDF text layer.
        description = re.sub(r'(?<=\w)\s*' + str(ref_no) + r'(?=\w)', '', description)
        if ref_no == 2:
            description = description.replace('officestationery', 'office stationery')
        if ref_no == 17 and description.endswith('accessories'):
            description += ')'
        description = re.sub(r'\bEach\b', '', description, flags=re.I)
        description = re.sub(r'\s+', ' ', description).strip()
        records.append({
            'Category': a[1], 'Procurement item': description,
            'Estimated Amount': a[11] or a[9], 'Source of Funds': b[1],
            'Procurement Method': b[3], 'date': b[5],
        })
    result = export_plan(pd.DataFrame(records), 2025, pdf_path, output_dir, '1-2')
    assert len(result) == 50
    return result


def extract_2026(source_dir, output_dir):
    xls_path = next(source_dir.glob('069--*.xls'))
    raw = pd.read_excel(xls_path, sheet_name='Data', header=9, engine='xlrd')
    raw = raw[['Class', 'Description', 'Total', 'Source of Funds',
               'Procurement Method', 'Start ']].rename(columns={
        'Class': 'Category', 'Description': 'Procurement item',
        'Total': 'Estimated Amount', 'Start ': 'date',
    })
    raw = raw.dropna(subset=['Category', 'Procurement item'], how='all')
    result = export_plan(raw, 2026, xls_path, output_dir, 'Data')
    assert len(result) > 0
    return result


def extract_all(root):
    source_dir = root / 'data/raw/council_documents/05_procurement_plans_and_reports'
    output_dir = root / 'data/processed/procurement'
    return {year: function(source_dir, output_dir) for year, function in [
        (2023, extract_2023), (2025, extract_2025), (2026, extract_2026)
    ]}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    for year, frame in extract_all(root).items():
        print(year, len(frame), 'procurement records')
