import os, re, json
from glob import glob

root = os.path.dirname(os.path.dirname(__file__))
files = glob(os.path.join(root, '**', '*.html'), recursive=True)
script_re = re.compile(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.S|re.I)

results = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        txt = fh.read()
    matches = script_re.findall(txt)
    for i, m in enumerate(matches, start=1):
        entry = {'file': f, 'index': i}
        try:
            data = json.loads(m)
            entry['valid_json'] = True
            entry['type'] = data.get('@type') if isinstance(data, dict) else None
            # basic checks
            errors = []
            if isinstance(data, dict):
                t = data.get('@type')
                if t == 'Organization':
                    for k in ('name','url'):
                        if not data.get(k): errors.append(f"missing {k}")
                if t == 'NewsArticle':
                    for k in ('headline','datePublished','publisher'):
                        if not data.get(k): errors.append(f"missing {k}")
                if t in ('CollectionPage','ItemList'):
                    if not data.get('name') and not data.get('itemListElement'):
                        errors.append('missing name or itemListElement')
                if t == 'WebPage':
                    if not data.get('name'):
                        errors.append('missing name')
            entry['errors'] = errors
        except Exception as e:
            entry['valid_json'] = False
            entry['error_msg'] = str(e)
        results.append(entry)

# Print summary
print('Checked', len(results), 'JSON-LD script blocks')
for r in results:
    print('\nFile:', r['file'], 'script #', r['index'])
    if not r['valid_json']:
        print(' INVALID JSON:', r.get('error_msg'))
    else:
        print(' Type:', r.get('type'), ' Errors:', r.get('errors'))

print('\nDone')
