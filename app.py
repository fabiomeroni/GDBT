"""
Digital Boasian Trilogy — Gaua Languages
Flask backend: auth · XML upload · grammar rendering · shortcode resolution
Run: python app.py   (then open http://localhost:5000)
"""

import os
import re
import json
from flask import Flask, request, jsonify, session, send_from_directory
from lxml import etree
import markdown as md_lib

# ── App setup ──────────────────────────────────────────────────
app = Flask(__name__, static_folder='.')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

UPLOAD_FOLDER  = 'uploads'
GRAMMAR_FOLDER = 'grammar_content'
AUTHOR_PASSWORD = os.environ.get('AUTHOR_PASSWORD', 'gaua2026')

IMAGES_FOLDER         = 'images'
TRANSCRIPTIONS_FOLDER = 'transcribed_narratives'
GLOSSES_FOLDER        = os.path.join(TRANSCRIPTIONS_FOLDER, 'glosses')
TRANSCRIPTIONS_INDEX  = os.path.join(TRANSCRIPTIONS_FOLDER, 'index.json')

os.makedirs(UPLOAD_FOLDER,         exist_ok=True)
os.makedirs(GRAMMAR_FOLDER,        exist_ok=True)
os.makedirs(IMAGES_FOLDER,         exist_ok=True)
os.makedirs(TRANSCRIPTIONS_FOLDER, exist_ok=True)
os.makedirs(GLOSSES_FOLDER,        exist_ok=True)

# ── Language constants (mirrors JS side) ───────────────────────
LANGS5      = ['Nume', 'Dorig', 'Koro', 'Olrat', 'Lakon']
LANG_CODES  = ['num',  'drg',   'kro',  'olr',   'lkn']
LANG_MAP    = dict(zip(LANG_CODES, LANGS5))
LANG_ABBR   = {'Nume':'Num','Dorig':'Drg','Koro':'Kro','Olrat':'Olr','Lakon':'Lkn'}
LANG_COLORS = {'Nume':'#2e5c8a','Dorig':'#c07820','Koro':'#922810','Olrat':'#267040','Lakon':'#5c2878'}

# ══════════════════════════════════════════════════════════════
#  XML HELPERS
# ══════════════════════════════════════════════════════════════

def _load_xml(upload_name, fallback):
    """Load XML from uploads/ folder, falling back to project root."""
    primary = os.path.join(UPLOAD_FOLDER, upload_name)
    path = primary if os.path.exists(primary) else fallback
    if not os.path.exists(path):
        return None
    try:
        return etree.parse(path)
    except etree.XMLSyntaxError:
        return None

def get_dict_xml():
    return _load_xml('dictionary.xml', 'dbt_dictionary.xml')

def get_corpus_xml():
    return _load_xml('corpus.xml', 'dbt_corpus.xml')

def get_fieldnotes_xml():
    return _load_xml('fieldnotes.xml', 'AlexFrancois_Questionnaire_Gaua-languages.xml')

# ══════════════════════════════════════════════════════════════
# ISO / Pangloss lang-code → Gaua language name (for transcription metadata)
_LANG_FROM_CODE = {
    'wwo':'Dorig','drg':'Dorig','lkn':'Lakon',
    'krf':'Koro', 'kro':'Koro', 'num':'Nume','olr':'Olrat',
}

# ── Citation builders ─────────────────────────────────────────

def _tokenize_form(form):
    """Python mirror of the JS tokenizeForm() in transcription.html.
    Splits on whitespace then on morpheme boundaries (- and =),
    keeping the marker with the left fragment and stripping trailing punctuation."""
    if not form or form == '—':
        return []
    tokens = []
    for word in form.strip().split():
        clean = re.sub(r'[.,;!?]+$', '', word)
        if not clean:
            continue
        if '-' not in clean and '=' not in clean:
            tokens.append(clean)
            continue
        parts = re.split(r'([-=])', clean)
        current = ''
        frags   = []
        for p in parts:
            if p in ('-', '='):
                current += p
                frags.append(current)
                current = ''
            else:
                current = p
        if current:
            frags.append(current)
        tokens.extend(f for f in frags if f)
    return tokens

def _load_stored_glosses(key):
    p = _gloss_path(key)
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    return {}

def _cite_ilg_table(words, stored_gloss):
    """Word-aligned interlinear table from _parse_tx words + stored gloss."""
    if words and any(w.get('gloss') for w in words):
        fc = ''.join(f'<td class="cite-form-cell">{w["form"]}</td>' for w in words)
        gc = ''.join(f'<td class="cite-gloss-cell">{w["gloss"] or ""}</td>' for w in words)
        return f'<table class="cite-ilg-table"><tr>{fc}</tr><tr class="cite-gloss-row">{gc}</tr></table>'
    elif isinstance(stored_gloss, str) and stored_gloss:
        form = words[0]['form'] if words else ''
        return (f'<table class="cite-ilg-table">'
                f'<tr><td class="cite-form-cell">{form}</td></tr>'
                f'<tr class="cite-gloss-row"><td class="cite-gloss-cell">{stored_gloss}</td></tr>'
                f'</table>')
    else:
        form = words[0]['form'] if words else ''
        return f'<table class="cite-ilg-table"><tr><td class="cite-form-cell">{form}</td></tr></table>'

def build_narrative_citation(filename, sent_id, n):
    path = os.path.join(TRANSCRIPTIONS_FOLDER, filename)
    if not os.path.exists(path):
        return f'<span class="shortcode-error">Transcription not found: {filename}</span>'
    try:
        data = _parse_tx(path)
    except Exception as e:
        return f'<span class="shortcode-error">Parse error in {filename}: {e}</span>'
    sent = next((s for s in data['sentences'] if s['id'] == sent_id), None)
    if not sent:
        return f'<span class="shortcode-error">Sentence {sent_id} not found in {filename}</span>'
    stored_glosses = _load_stored_glosses(filename)
    stored   = stored_glosses.get(sent_id)
    lang_code = data.get('lang', '')
    lang_name = _LANG_FROM_CODE.get(lang_code, lang_code)
    color     = LANG_COLORS.get(lang_name, '#8a5f18')
    ilg       = _cite_ilg_table(sent.get('words', []), stored)
    ref       = f'{lang_name} · {filename[:-4]} · {sent_id} · A. François 2003'
    return (f'<div class="grammar-cite">'
            f'<span class="cite-n">({n})</span>'
            f'<div class="cite-body">'
            f'<div class="cite-ilg" style="--cite-color:{color};">{ilg}</div>'
            f'<div class="cite-transl">‘{sent["transl"]}’</div>'
            f'<div class="cite-ref">[{ref}]</div>'
            f'</div></div>')

def build_fieldnotes_citation(group_index, sent_id, n):
    xml = get_fieldnotes_xml()
    if xml is None:
        return '<span class="shortcode-error">No fieldnotes XML loaded</span>'
    tgs = xml.findall('.//tiGroup')
    if group_index < 0 or group_index >= len(tgs):
        return f'<span class="shortcode-error">Fieldnotes group {group_index} not found</span>'
    tg  = tgs[group_index]
    ti  = (tg.findtext('ti') or '').strip()
    rfg = next((r for r in tg.findall('rfGroup')
                if (r.findtext('rf') or '').strip() == sent_id), None)
    if rfg is None:
        return f'<span class="shortcode-error">{sent_id} not found in fieldnotes group {group_index}</span>'
    grp    = rfg.find('bslGroup') or rfg.find('frGroup')
    prompt = (grp.findtext('bsl') or grp.findtext('fr') or '').strip() if grp else ''
    raw = {}
    for code, abbr, name in _FN_LANGS:
        nodes = grp.findall(code) if grp else []
        vals  = [nd.text.strip() for nd in nodes if nd.text and nd.text.strip()]
        raw[code] = ' '.join(vals) if vals else '—'
    stored_glosses = _load_stored_glosses(f'fieldnotes_{group_index}')
    stored         = stored_glosses.get(sent_id)
    if stored and isinstance(stored, dict) and stored.get('tokens'):
        tokens      = stored['tokens']
        col_glosses = stored.get('glosses', [])
        n_cols      = max((len(tokens.get(c, [])) for c, _, _ in _FN_LANGS), default=0)
    else:
        tokens = {}; n_cols = 0
        for code, _, _ in _FN_LANGS:
            toks = _tokenize_form(raw[code]) if raw[code] != '—' else []
            tokens[code] = toks; n_cols = max(n_cols, len(toks))
        col_glosses = [''] * n_cols
        for code, _, _ in _FN_LANGS:
            while len(tokens[code]) < n_cols: tokens[code].append('')
    lang_rows = ''
    for code, abbr, name in _FN_LANGS:
        color = LANG_COLORS.get(name, '#888')
        cells = ''.join(
            f'<td class="cite-fn-form" style="color:{color};">{tokens[code][i] if i < len(tokens[code]) else "—"}</td>'
            for i in range(n_cols))
        lang_rows += f'<tr><td class="cite-fn-abbr" style="color:{color};">{abbr}</td>{cells}</tr>'
    sep    = '<td></td>' + '<td></td>' * n_cols
    gcells = ''.join(f'<td class="cite-fn-gloss">{col_glosses[i] if i < len(col_glosses) else ""}</td>' for i in range(n_cols))
    return (f'<div class="grammar-cite">'
            f'<span class="cite-n">({n})</span>'
            f'<div class="cite-body">'
            f'<div class="cite-ilg"><table class="cite-fn-table">{lang_rows}'
            f'<tr class="cite-fn-sep">{sep}</tr>'
            f'<tr><td class="cite-fn-label">gloss</td>{gcells}</tr></table></div>'
            f'<div class="cite-transl">‘{prompt}’</div>'
            f'<div class="cite-ref">[Fieldnotes · {ti} · {sent_id}]</div>'
            f'</div></div>')

def build_citation(spec, n):
    if spec.startswith('fieldnotes#'):
        parts = spec.split('#', 2)
        if len(parts) < 3:
            return f'<span class="shortcode-error">Invalid fieldnotes cite: {spec}</span>'
        try: idx = int(parts[1])
        except ValueError:
            return f'<span class="shortcode-error">Bad group index: {parts[1]}</span>'
        return build_fieldnotes_citation(idx, parts[2].strip(), n)
    elif '#' in spec:
        filename, sent_id = spec.split('#', 1)
        return build_narrative_citation(filename.strip(), sent_id.strip(), n)
    return f'<span class="shortcode-error">Invalid cite spec: {spec}</span>'

#  SHORTCODE RESOLVERS
# ══════════════════════════════════════════════════════════════

def build_example_table(ex_id):
    """
    Resolve {{example: ID}} — builds a full five-language interlinear table
    from the corpus XML. Each language row carries data-lang="…" so the
    client-side language-toggle pills can show/hide rows without a round-trip.
    """
    corpus = get_corpus_xml()
    if corpus is None:
        return f'<p class="shortcode-error">Corpus XML not found (looking for uploads/corpus.xml or dbt_corpus.xml)</p>'

    ex = corpus.find(f'.//Example[@id="{ex_id}"]')
    if ex is None:
        return f'<p class="shortcode-error">Example not found in corpus: <code>{ex_id}</code></p>'

    translation  = ex.findtext('Translation[@lang="eng"]', '').strip()
    glosses_raw  = ex.findtext('Glosses', '').strip()
    glosses      = glosses_raw.split() if glosses_raw else []
    pangloss_url = ex.findtext('Source/PanglossURL', '').strip()

    # Token → dict-entry link map
    token_links = {}
    for tok in ex.findall('TokenLinks/Token'):
        idx     = tok.get('index', '')
        dict_id = tok.get('dictId', '')
        if idx.isdigit() and dict_id:
            token_links[int(idx)] = dict_id

    # Build one table row per language
    rows_html = ''
    for code in LANG_CODES:
        lang = LANG_MAP[code]
        tier = ex.find(f'Tier[@lang="{code}"]')
        if tier is None or not tier.text:
            continue
        forms  = tier.text.strip().split()
        color  = LANG_COLORS[lang]
        abbr   = LANG_ABBR[lang]

        cells = ''
        for i, form in enumerate(forms):
            dict_id = token_links.get(i, '')
            if form == '—':
                cells += '<td class="ex-cell ex-dash">—</td>'
            elif dict_id:
                cells += (f'<td class="ex-cell">'
                          f'<a class="lexlink" href="dictionary.html#{dict_id}" '
                          f'data-dict-id="{dict_id}">{form}</a></td>')
            else:
                cells += f'<td class="ex-cell">{form}</td>'

        rows_html += (f'<tr data-lang="{lang}">'
                      f'<td class="ex-abbr" style="color:{color};">{abbr}</td>'
                      f'{cells}</tr>\n')

    # Separator + gloss row
    n_cols     = len(glosses)
    sep_cells  = '<td></td>' + '<td></td>' * n_cols
    gloss_cells = ''.join(f'<td class="ex-gloss">{g}</td>' for g in glosses)

    pangloss_link = ''
    if pangloss_url:
        pangloss_link = (f'<a class="corpus-ref" href="{pangloss_url}" target="_blank" '
                         f'rel="noopener">🎧 Pangloss archive →</a>')

    return f'''<div class="example-block" data-example-id="{ex_id}">
  <div class="example-wrap">
    <table class="ex-table">
      {rows_html}
      <tr class="ex-sep">{sep_cells}</tr>
      <tr><td class="ex-gloss-empty"></td>{gloss_cells}</tr>
    </table>
    <div class="ex-transl">{translation}</div>
    {pangloss_link}
  </div>
</div>'''


def build_entry_chip(entry_id):
    """
    Resolve {{entry: ID}} — builds a compact inline citation chip
    showing all five language forms and the gloss, hyperlinked to
    the full dictionary entry.
    """
    d = get_dict_xml()
    if d is None:
        return f'<span class="shortcode-error">Dictionary XML not found</span>'

    entry = d.find(f'.//EntréeLexicale[@identifiant="{entry_id}"]')
    if entry is None:
        return f'<span class="shortcode-error">Dictionary entry not found: <code>{entry_id}</code></span>'

    forms = {}
    for node in entry.findall('Lemme/ReprésentationDeForme'):
        code = node.get('langue', '')
        if code in LANG_MAP:
            forms[LANG_MAP[code]] = (node.text or '').strip()

    gloss = (entry.findtext('Sens/Glose[@langue="eng"]', '') or '').strip()
    pos   = (entry.findtext('ClasseGrammaticale', '') or '').strip()

    forms_html = ' · '.join(
        f'<span class="chip-form" style="color:{LANG_COLORS[lang]};">'
        f'{forms.get(lang, "—")}</span>'
        for lang in LANGS5
    )

    return (f'<a href="dictionary.html#{entry_id}" class="entry-chip" '
            f'title="{pos} — {gloss}">'
            f'<span class="chip-forms">{forms_html}</span>'
            f'<span class="chip-gloss"> \u2018{gloss}\u2019</span>'
            f'</a>')


# ══════════════════════════════════════════════════════════════
#  GRAMMAR RENDERER
#  Pass 1: Markdown → HTML
#  Pass 2: resolve {{example:…}} and {{entry:…}} shortcodes
# ══════════════════════════════════════════════════════════════

_MD = md_lib.Markdown(extensions=['extra', 'tables', 'attr_list', 'toc'])

def render_grammar(md_text):
    _MD.reset()
    html = _MD.convert(md_text)

    html = re.sub(
        r'\{\{\s*example\s*:\s*([^\}]+)\}\}',
        lambda m: build_example_table(m.group(1).strip()),
        html
    )
    html = re.sub(
        r'\{\{\s*entry\s*:\s*([^\}]+)\}\}',
        lambda m: build_entry_chip(m.group(1).strip()),
        html
    )
    # {{cite:}} — numbered automatically within each section
    _counter = [0]
    def _resolve_cite(m):
        _counter[0] += 1
        return build_citation(m.group(1).strip(), _counter[0])
    html = re.sub(r'\{\{\s*cite\s*:\s*([^\}]+)\}\}', _resolve_cite, html)
    return html


def _section_path(section_id):
    # Sanitise: only allow alphanumeric + underscore to prevent path traversal
    safe = re.sub(r'[^a-zA-Z0-9_]', '', section_id)
    return os.path.join(GRAMMAR_FOLDER, f'{safe}.md')


# ══════════════════════════════════════════════════════════════
#  API ROUTES
# ══════════════════════════════════════════════════════════════

# ── Auth ──────────────────────────────────────────────────────

@app.route('/api/auth/status')
def auth_status():
    return jsonify({'logged_in': bool(session.get('author'))})


@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json(silent=True) or {}
    if data.get('password') == AUTHOR_PASSWORD:
        session['author'] = True
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'Wrong password'}), 401


@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    session.pop('author', None)
    return jsonify({'ok': True})


# ── XML upload ────────────────────────────────────────────────

def _handle_upload(filename):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'No file provided'}), 400
    try:
        etree.parse(f)          # validate XML before saving
    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {e}'}), 400
    f.seek(0)
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify({'ok': True, 'message': f'{filename} saved.'})


@app.route('/api/upload/dictionary', methods=['POST'])
def upload_dictionary():
    return _handle_upload('dictionary.xml')


@app.route('/api/upload/corpus', methods=['POST'])
def upload_corpus():
    return _handle_upload('corpus.xml')

@app.route('/api/upload/fieldnotes', methods=['POST'])
def upload_fieldnotes():
    return _handle_upload('fieldnotes.xml')

# Language columns for fieldnotes comparative display
_FN_LANGS = [
    ('num', 'Num', 'Nume'),
    ('drg', 'Drg', 'Dorig'),
    ('kro', 'Kro', 'Koro'),
    ('olr', 'Olr', 'Olrat'),
    ('lkn', 'Lkn', 'Lakon'),
]

@app.route('/api/fieldnotes/tx/<int:index>')
def fieldnotes_tx(index):
    """Return a fieldnotes tiGroup in transcription-viewer format.
    Each rfGroup becomes a sentence with:
      - words: [{form: langForm, gloss: langAbbr, lang: code, lang_name: name}]
      - transl: the Bislama prompt
      - is_comparative: True  →  triggers comparative display in the viewer
    """
    xml = get_fieldnotes_xml()
    if xml is None:
        return jsonify({'error': 'No fieldnotes XML found'}), 404
    tgs = xml.findall('.//tiGroup')
    if index < 0 or index >= len(tgs):
        return jsonify({'error': 'Group not found'}), 404
    tg = tgs[index]
    ti = (tg.findtext('ti') or '').strip()
    sentences = []
    for rfg in tg.findall('rfGroup'):
        rf  = (rfg.findtext('rf') or '').strip()
        grp = rfg.find('bslGroup') or rfg.find('frGroup')
        if grp is None:
            continue
        prompt = (grp.findtext('bsl') or grp.findtext('fr') or '').strip()
        words = []
        for code, abbr, name in _FN_LANGS:
            nodes = grp.findall(code)
            vals  = [n.text.strip() for n in nodes if n.text and n.text.strip()]
            form  = ' / '.join(vals) if vals else '—'
            words.append({'form': form, 'gloss': abbr,
                          'lang': code, 'lang_name': name})
        if prompt or any(w['form'] != '—' for w in words):
            sentences.append({
                'id':            rf,
                'form':          '',      # display handled via words
                'transl':        prompt,
                'transl_lang':   'bsl',
                'words':         words,
                'has_gloss':     True,    # use word-aligned block
                'is_comparative': True,   # flag → special comparative rendering
                'audio':         None,
            })
    return jsonify({
        'title':        ti,
        'is_fieldnotes': True,
        'lang':         'comparative',
        'sentences':    sentences,
    })


# ── Fieldnotes routes ─────────────────────────────────────────

_FN_CODES = ['num', 'drg', 'kro', 'olr', 'lkn']

@app.route('/api/fieldnotes/groups')
def fieldnotes_groups():
    xml = get_fieldnotes_xml()
    if xml is None:
        return jsonify({'groups': [], 'error': 'No fieldnotes XML found'})
    groups = []
    for i, tg in enumerate(xml.findall('.//tiGroup')):
        ti = (tg.findtext('ti') or '').strip()
        if ti:
            groups.append({'index': i, 'title': ti})
    return jsonify({'groups': groups})

@app.route('/api/fieldnotes/group/<int:index>')
def fieldnotes_group(index):
    xml = get_fieldnotes_xml()
    if xml is None:
        return jsonify({'error': 'No fieldnotes XML found'}), 404
    tgs = xml.findall('.//tiGroup')
    if index < 0 or index >= len(tgs):
        return jsonify({'error': 'Group not found'}), 404
    tg  = tgs[index]
    ti  = (tg.findtext('ti') or '').strip()
    items = []
    for rfg in tg.findall('rfGroup'):
        rf  = (rfg.findtext('rf') or '').strip()
        grp = rfg.find('bslGroup') or rfg.find('frGroup')
        if grp is None:
            continue
        prompt = (grp.findtext('bsl') or grp.findtext('fr') or '').strip()
        forms  = {}
        for code in _FN_CODES:
            nodes = grp.findall(code)
            vals  = [n.text.strip() for n in nodes if n.text and n.text.strip()]
            forms[code] = ' / '.join(vals)
        if prompt or any(forms.values()):
            items.append({'rf': rf, 'prompt': prompt, 'forms': forms})
    return jsonify({'title': ti, 'index': index, 'items': items})

@app.route('/api/upload/status')
def upload_status():
    """Tell the client which XMLs are currently loaded."""
    return jsonify({
        'dictionary': os.path.exists(os.path.join(UPLOAD_FOLDER, 'dictionary.xml'))
                      or os.path.exists('dbt_dictionary.xml'),
        'corpus':     os.path.exists(os.path.join(UPLOAD_FOLDER, 'corpus.xml'))
                      or os.path.exists('dbt_corpus.xml'),
    })


# ── Grammar sections ──────────────────────────────────────────

@app.route('/api/grammar/<section_id>')
def get_grammar_html(section_id):
    path = _section_path(section_id)
    if not os.path.exists(path):
        return jsonify({'error': f'Section not found: {section_id}'}), 404
    with open(path, encoding='utf-8') as f:
        html = render_grammar(f.read())
    return jsonify({'html': html, 'id': section_id})


@app.route('/api/grammar/<section_id>/source')
def get_grammar_source(section_id):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    path = _section_path(section_id)
    if not os.path.exists(path):
        return jsonify({'error': f'Section not found: {section_id}'}), 404
    with open(path, encoding='utf-8') as f:
        return jsonify({'source': f.read(), 'id': section_id})


@app.route('/api/grammar/<section_id>', methods=['POST'])
def save_grammar(section_id):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    source = data.get('source', '')
    path = _section_path(section_id)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(source)
    html = render_grammar(source)
    return jsonify({'ok': True, 'html': html})


@app.route('/api/grammar/<section_id>', methods=['DELETE'])
def delete_grammar(section_id):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    path = _section_path(section_id)
    if os.path.exists(path):
        os.remove(path)
    return jsonify({'ok': True})


@app.route('/api/grammar', methods=['POST'])
def create_grammar_section():
    """Create a new grammar section with an auto-generated ID."""
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json(silent=True) or {}
    title   = data.get('title', '').strip() or 'New section'
    # Auto-generate next available sN id
    n = len([f for f in os.listdir(GRAMMAR_FOLDER) if f.endswith('.md')]) + 1
    section_id = f's{n}'
    while os.path.exists(_section_path(section_id)):
        n += 1
        section_id = f's{n}'
    initial = f'## {title}\n\n[Start writing here…]\n'
    with open(_section_path(section_id), 'w', encoding='utf-8') as f:
        f.write(initial)
    return jsonify({'ok': True, 'id': section_id, 'title': title})


_ALLOWED_IMG_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

@app.route('/api/upload/image', methods=['POST'])
def upload_image():
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'No file provided'}), 400
    ext = os.path.splitext(f.filename or '')[1].lower()
    if ext not in _ALLOWED_IMG_EXT:
        return jsonify({'error': f'Allowed types: {", ".join(_ALLOWED_IMG_EXT)}'}), 400
    safe = re.sub(r'[^a-zA-Z0-9._-]', '_', f.filename)
    f.save(os.path.join(IMAGES_FOLDER, safe))
    return jsonify({'ok': True, 'url': f'images/{safe}', 'filename': safe})


@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_FOLDER, filename)


# ── Dictionary entries (compact JSON for client-side gloss lookup) ────────────
_ABBREV_LINKS_PATH = os.path.join(TRANSCRIPTIONS_FOLDER, 'abbrev_links.json')

@app.route('/api/abbrev_links')
def get_abbrev_links():
    if os.path.exists(_ABBREV_LINKS_PATH):
        with open(_ABBREV_LINKS_PATH, encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/abbrev_links', methods=['POST'])
def save_abbrev_link():
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data  = request.get_json(silent=True) or {}
    abbr  = data.get('abbr', '').strip()
    link  = data.get('link', '').strip()
    if not abbr:
        return jsonify({'error': 'No abbreviation provided'}), 400
    links = {}
    if os.path.exists(_ABBREV_LINKS_PATH):
        with open(_ABBREV_LINKS_PATH, encoding='utf-8') as f:
            links = json.load(f)
    if link:
        links[abbr] = link
    else:
        links.pop(abbr, None)   # empty link = remove
    with open(_ABBREV_LINKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(links, f, ensure_ascii=False, indent=2)
    return jsonify({'ok': True})

@app.route('/api/dictionary/entries')
def dictionary_entries():
    """Return all entries with their 5-language forms and English gloss.
    Used by the transcription viewer to suggest dictionary glosses for columns."""
    d = get_dict_xml()
    if d is None:
        return jsonify({'entries': []})
    entries = []
    for el in d.findall('.//EntréeLexicale'):
        # Prefer <gloss> (short interlinear label) over <Glose> (full definition)
        gloss = (el.findtext('Sens/gloss')
                 or el.findtext('Sens/Glose[@langue="eng"]')
                 or '').strip()
        if not gloss:
            continue
        forms = {}
        for node in el.findall('Lemme/ReprésentationDeForme'):
            lang = node.get('langue', '')
            if lang and node.text:
                forms[lang] = node.text.strip()
        entries.append({
            'id':    el.get('identifiant', ''),
            'gloss': gloss,
            'forms': forms,
        })
    return jsonify({'entries': entries})

# ── List available sections ───────────────────────────────────

@app.route('/api/grammar')
def list_sections():
    sections = []
    for fname in sorted(os.listdir(GRAMMAR_FOLDER)):
        if fname.endswith('.md'):
            sections.append({'id': fname[:-3]})
    return jsonify({'sections': sections})


# ── Transcription helpers ─────────────────────────────────────

# xml:lang="en" uses the XML namespace
_XMLLANG = '{http://www.w3.org/XML/1998/namespace}lang'
# Parse without downloading DTD (Pangloss DTD referenced in files)
_XML_PARSER = etree.XMLParser(load_dtd=False, no_network=True, resolve_entities=False)

def _tx_index():
    if os.path.exists(TRANSCRIPTIONS_INDEX):
        with open(TRANSCRIPTIONS_INDEX, encoding='utf-8') as f:
            return json.load(f)
    return {}

def _tx_path(text_key):
    idx = _tx_index()
    fn  = idx.get(text_key)
    if not fn:
        return None
    p = os.path.join(TRANSCRIPTIONS_FOLDER, fn)
    return p if os.path.exists(p) else None

def _gloss_path(text_key):
    safe = re.sub(r'[^a-zA-Z0-9_-]', '_', text_key)
    return os.path.join(GLOSSES_FOLDER, f'{safe}.json')

_TRANSL_PREFS = ('en', 'fr', 'it', 'de', 'es', 'nl')

def _best_transl(el):
    """Return (text, lang_code) of the most preferred translation on an element."""
    found = {}
    for t in el.findall('TRANSL'):
        lv  = t.get(_XMLLANG, '') or t.get('xml:lang', '')
        txt = (t.text or '').strip()
        if txt:
            found[lv] = txt
    for pref in _TRANSL_PREFS:
        if pref in found:
            return found[pref], pref
    # Fallback: any available
    for lv, txt in found.items():
        return txt, lv
    return '', ''

def _extract_words(s_el):
    """
    Extract word-aligned gloss from <W><M> elements.
    Returns a list of {'form': str, 'gloss': str} — one entry per <W>.
    Returns [] if no W elements or none have M children with content.
    """
    words = []
    for w in s_el.findall('W'):
        morphs_form  = []
        morphs_gloss = []
        for m in w.findall('M'):
            mf = (m.findtext('FORM')  or '').strip()
            mg = (m.findtext('TRANSL') or '').strip()
            if mf:
                morphs_form.append(mf)
            if mg:
                morphs_gloss.append(mg)
        if morphs_form:
            words.append({
                'form':  '-'.join(morphs_form),
                'gloss': '-'.join(morphs_gloss) if morphs_gloss else '',
            })
    return words

def _parse_tx(path):
    xml  = etree.parse(path, _XML_PARSER)
    root = xml.getroot()
    lang_code = (root.get(_XMLLANG) or root.get('xml:lang', '')).strip()
    text_id   = root.get('id', '')

    # Titles — prefer English, fall back to French or first available
    titles = {}
    for t in root.findall('HEADER/TITLE'):
        lv = (t.get(_XMLLANG) or t.get('xml:lang', '')).strip()
        if t.text: titles[lv] = t.text.strip()
    title = titles.get('en') or titles.get('fr') or next(iter(titles.values()), '')

    # Sentences
    sentences = []
    for s in root.findall('S'):
        sid  = s.get('id', '')
        form = (s.findtext('FORM') or '').strip()
        if not form:
            continue
        transl, transl_lang = _best_transl(s)
        audio_el = s.find('AUDIO')
        audio    = {'start': audio_el.get('start', ''),
                    'end':   audio_el.get('end', '')} if audio_el is not None else None
        words     = _extract_words(s)
        has_gloss = bool(words and any(w['gloss'] for w in words))
        sentences.append({
            'id': sid, 'form': form,
            'transl': transl, 'transl_lang': transl_lang,
            'audio': audio,
            'words': words,          # word-aligned gloss from W/M
            'has_gloss': has_gloss,  # True = gloss already in XML
        })

    return {
        'id': text_id, 'lang': lang_code,
        'title': title,
        'sentences': sentences,
    }

# ── Transcription API routes ──────────────────────────────────

@app.route('/api/transcriptions/list')
def tx_list():
    """Return metadata for every XML in transcribed_narratives/ — drives the recordings tab."""
    items = []
    for fn in sorted(os.listdir(TRANSCRIPTIONS_FOLDER)):
        if not fn.endswith('.xml'):
            continue
        path = os.path.join(TRANSCRIPTIONS_FOLDER, fn)
        try:
            xml  = etree.parse(path, _XML_PARSER)
            root = xml.getroot()
            lang = (root.get(_XMLLANG) or root.get('xml:lang', '')).strip()
            tx_id = root.get('id', fn[:-4])
            titles = {}
            for t in root.findall('HEADER/TITLE'):
                lv = (t.get(_XMLLANG) or t.get('xml:lang', '')).strip()
                if t.text: titles[lv] = t.text.strip()
            title = (titles.get('en') or titles.get('fr')
                     or next(iter(titles.values()), fn[:-4]))
            items.append({
                'filename': fn,
                'id': tx_id,
                'lang': lang,
                'title': title,
                'n_sentences': len(root.findall('S')),
            })
        except Exception:
            continue
    return jsonify({'transcriptions': items})

@app.route('/api/transcription/<path:text_key>')
def get_transcription(text_key):
    # text_key is the XML filename (e.g. crdo-WWO_FARFADETS.xml)
    path = os.path.join(TRANSCRIPTIONS_FOLDER, text_key)
    if not os.path.exists(path):
        return jsonify({'error': 'Transcription not found'}), 404
    try:
        data = _parse_tx(path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify(data)

@app.route('/api/transcription/<path:text_key>/glosses', methods=['GET'])
def get_glosses(text_key):
    # text_key is the XML filename; gloss stored by sanitised filename key
    p = _gloss_path(text_key)
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/api/transcription/<path:text_key>/glosses', methods=['POST'])
def save_gloss(text_key):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json(silent=True) or {}
    sent_id = data.get('sentence_id', '')
    gloss   = data.get('gloss', '')
    if not sent_id:
        return jsonify({'error': 'No sentence_id'}), 400
    p = _gloss_path(text_key)
    glosses = {}
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            glosses = json.load(f)
    glosses[sent_id] = gloss
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(glosses, f, ensure_ascii=False, indent=2)
    return jsonify({'ok': True})

@app.route('/api/upload/transcription', methods=['POST'])
def upload_transcription():
    """Save a transcription XML to transcribed_narratives/.
    The title and language are read from the XML itself — no manual linking needed."""
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    f = request.files.get('file')
    if not f:
        return jsonify({'error': 'No file provided'}), 400
    try:
        etree.parse(f, _XML_PARSER)
    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {e}'}), 400
    f.seek(0)
    safe_fn = re.sub(r'[^a-zA-Z0-9._-]', '_', f.filename or 'transcription.xml')
    f.save(os.path.join(TRANSCRIPTIONS_FOLDER, safe_fn))
    return jsonify({'ok': True, 'filename': safe_fn})

# ── Static file serving ───────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


# ── Dev entry point ───────────────────────────────────────────

if __name__ == '__main__':
    print("DBT Gaua — starting on http://localhost:5000")
    print(f"Author password: {AUTHOR_PASSWORD}")
    app.run(debug=True, port=5000, host='0.0.0.0')
