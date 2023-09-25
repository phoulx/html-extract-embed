import re
from collections import namedtuple
from pathlib import Path

from bs4 import BeautifulSoup

import qdrant
import sbert

columns = ['Title', 'Action', 'Text', 'Link', 'Timestamp', 'Products', 'CleanText']
Cell = namedtuple('Cell', columns)

def handle(file_path: Path):
    data = parse(file_path)
    embedding = sbert.vectorize([d.CleanText for d in data])
    result = qdrant.save(zip(embedding, [d._asdict() for d in data]))

    return {'status': result}


def parse(file_path: Path) -> list[Cell]:
    with open(file_path, 'r') as f:
        html_data = f.read()
    soup = BeautifulSoup(html_data, 'html.parser')    
    body = soup.div
    if not body:
        return []
    data = []
    for child in body.children:
        title = child.find('p', class_="mdl-typography--title")
        action = child.find('div', class_="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1")
        link = action.find('a')
        products = child.find('div', class_="content-cell mdl-cell mdl-cell--12-col mdl-typography--caption")
        clean_text = clean(link.string)

        data.append(Cell(
            title.contents[0],
            action.contents[0].rstrip(),
            link.string,
            link.get('href'),
            action.contents[-1],
            products.contents[2].strip(),
            clean_text,
        ))

    return data

def clean(text):
    text = re.sub(r'\W+', ' ', text)
    things = ['https', 'www.', '.com']
    for t in things:
        text.replace(t, ' ')
    return ' '.join(text.split())