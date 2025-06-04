import re
from bs4 import BeautifulSoup

# Read the HTML file
with open('Agents/elements_data.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')

# Get element names from header row (skip first empty cell)
header_cells = rows[0].find_all('td')[1:]
elements = [re.sub(r'<.*?>', '', str(cell)).strip().replace('<b>', '').replace('</b>', '') for cell in header_cells]

combinations = {}
for i, row in enumerate(rows[1:]):
    cells = row.find_all('td')
    if not cells:
        continue
    row_element = re.sub(r'<.*?>', '', str(cells[0])).strip().replace('<b>', '').replace('</b>', '')
    for j, cell in enumerate(cells[1:]):
        col_element = elements[j]
        result = re.sub(r'<.*?>', '', str(cell)).strip().replace('<small>', '').replace('</small>', '')
        if result and result.lower() != 'n/a':
            key = frozenset([row_element, col_element])
            combinations[key] = result

# Write to a Python file
with open('Agents/elements_combinations.py', 'w', encoding='utf-8') as f:
    f.write('element_combinations = {\n')
    for k, v in combinations.items():
        elems = ', '.join([repr(e) for e in k])
        f.write(f'    frozenset([{elems}]): {repr(v)},\n')  # <-- Use colon, not comma
    f.write('}\n')

print('Done! Combinations saved to Agents/elements_combinations.py')
