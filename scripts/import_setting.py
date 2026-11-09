"""Export the original setting guide chapters from a local DOCX for the atlas."""

import argparse
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
DATA = Path(__file__).resolve().parents[1] / 'dist/data'


def read_chapters(document):
    with ZipFile(document) as archive:
        body = ET.fromstring(archive.read('word/document.xml')).find(W + 'body')
        styles = ET.fromstring(archive.read('word/styles.xml'))
    levels = {}
    for style in styles.findall(W + 'style'):
        name = style.find(W + 'name')
        heading = re.fullmatch(r'heading ([1-9])', name.get(W + 'val', ''), re.I) if name is not None else None
        if heading:
            levels[style.get(W + 'styleId')] = int(heading[1])

    breaks = {W + 'br': '\n', W + 'cr': '\n', W + 'tab': '\t', W + 'noBreakHyphen': '\u2011'}
    chapters = []
    # The Word table of contents is a separate content control, outside these body paragraphs.
    for paragraph in body.findall(W + 'p'):
        value = ''.join(
            (node.text or '') if node.tag == W + 't' else breaks.get(node.tag, '')
            for node in paragraph.iter()
        ).strip()
        if not value:
            continue
        style = paragraph.find(f'{W}pPr/{W}pStyle')
        level = levels.get(style.get(W + 'val')) if style is not None else None
        if level:
            chapters.append(dict(title=value, level=level, paragraphs=[]))
        elif chapters:
            chapters[-1]['paragraphs'].append(value)
    return chapters


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('document', type=Path)
    args = parser.parse_args()
    chapters = read_chapters(args.document)
    links = json.loads((DATA / 'country-backgrounds.json').read_text(encoding='utf-8'))
    required = {title for entry in links.values() for title in entry['chapter'].split('；')}
    titles = {chapter['title'] for chapter in chapters}
    if len(titles) != len(chapters) or required - titles:
        parser.error(f'Duplicate or missing chapter headings: {sorted(required - titles)}')
    (DATA / 'setting-chapters.json').write_text(
        json.dumps(chapters, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
    )
    print(f'Exported {len(chapters)} setting chapters.')


if __name__ == '__main__':
    main()
