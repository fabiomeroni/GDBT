"""
Digital Boasian Trilogy — Gaua Languages
Flask backend: auth · XML upload · grammar rendering · shortcode resolution
Run: python app.py   (then open http://localhost:5000)
"""

import os
import re
from flask import Flask, request, jsonify, session, send_from_directory
from lxml import etree
import markdown as md_lib

# ── App setup ──────────────────────────────────────────────────
app = Flask(__name__, static_folder='.')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

UPLOAD_FOLDER  = 'uploads'
GRAMMAR_FOLDER = 'grammar_content'
AUTHOR_PASSWORD = os.environ.get('AUTHOR_PASSWORD', 'gaua2026')

os.makedirs(UPLOAD_FOLDER,  exist_ok=True)
os.makedirs(GRAMMAR_FOLDER, exist_ok=True)

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


# ── List available sections ───────────────────────────────────

@app.route('/api/grammar')
def list_sections():
    sections = []
    for fname in sorted(os.listdir(GRAMMAR_FOLDER)):
        if fname.endswith('.md'):
            sections.append({'id': fname[:-3]})
    return jsonify({'sections': sections})


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
