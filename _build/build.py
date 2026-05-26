#!/usr/bin/env python3
"""
Bull Binder build script.
Loads content from content_data.json + any overrides, merges with the HTML template,
outputs to /mnt/user-data/outputs/index.html.

To update a topic: modify the OVERRIDES dict below or edit content_data.json directly.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

# Load base content (extracted from last good build)
with open(f'{BASE}/content_data.json', encoding='utf-8') as f:
    data = json.load(f)

C = data['C']
M = data['M']

# Load HTML template
with open(f'{BASE}/template_check.html', encoding='utf-8') as f:
    HTML = f.read()

# ── BINDER CONTENT OVERRIDES ──────────────────────────────────────────────────
# Add authored Binder topics here as they are completed.
# Format: C['binder']['topics'][index]['slides'] = [list of slide dicts]
#
# Example:
# BINDER_OVERRIDES = {
#     'B06': [
#         {"k":"Customer Service · Greeting","t":"The Greeting","body":[...]},
#         ...
#     ]
# }

BINDER_OVERRIDES = {
    # Populated as binder topics are authored
}

# Apply overrides
binder_topics = C['binder']['topics']
num_to_idx = {t['num']: i for i, t in enumerate(binder_topics)}
for num, slides in BINDER_OVERRIDES.items():
    if num in num_to_idx:
        binder_topics[num_to_idx[num]]['slides'] = slides

# Build output
out = HTML.replace('__CONTENT__', json.dumps(C, ensure_ascii=False))
out = out.replace('__MOTIFS__', json.dumps(M, ensure_ascii=False))

out_path = '/mnt/user-data/outputs/index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Built {len(out):,} bytes — {len(out)//1024} KB → {out_path}")

# Verify
assert '__CONTENT__' not in out and '__MOTIFS__' not in out, "placeholder not replaced"
print("Verified — no leftover placeholders")
