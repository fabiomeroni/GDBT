"""
Digital Boasian Trilogy — Gaua Languages
Flask backend: auth · XML upload · grammar rendering · shortcode resolution
Run: python app.py   (then open http://localhost:5000)
"""

import os
import re
import json
from html import escape as _esc
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
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        content = f.read().strip()
    if not content:
        return {}
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # File may have extra data (two objects concatenated after interrupted save).
        # raw_decode parses the first valid JSON value and ignores the rest.
        try:
            obj, _ = json.JSONDecoder().raw_decode(content)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
        return {}

def _cite_ilg_table(words, stored_gloss, lang_code=''):
    """Word-aligned interlinear table from _parse_tx words + stored gloss."""
    if words and any(w.get('gloss') for w in words):
        fc = ''.join(f'<td class="cite-form-cell" data-lang="{lang_code}" data-form="{w["form"]}">{w["form"]}</td>' for w in words)
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
    ilg       = _cite_ilg_table(sent.get('words', []), stored, lang_code)
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
    # Prefer author-stored translation; fall back to Bislama prompt
    display_transl = (
        stored.get('translation')
        if stored and isinstance(stored, dict) and stored.get('translation') is not None
        else prompt
    )
    return _cite_fn_table(tokens, col_glosses, n_cols, display_transl,
                          f'Fieldnotes \u00b7 {ti} \u00b7 {sent_id}', n)


# ── "Examples from papers": a text made of the <Example>s of the corpus XML ──────────
# Shown and cited exactly like a fieldwork text (aligned columns, glosses, translation),
# but with its own gloss store (glosses/papers_0.json) so fieldnotes glosses are never touched.
PAPERS_TITLE = 'Examples from papers'

def _root_tag(path):
    """Root element name, read without parsing the whole file (or fetching its DTD)."""
    try:
        for _ev, el in etree.iterparse(path, events=('start',), load_dtd=False,
                                       no_network=True, resolve_entities=False):
            return el.tag
    except Exception:
        return None

def _is_examples_file(path):
    return _root_tag(path) == 'Examples'

def _paper_examples():
    """Every <Example> of the files in transcribed_narratives/ whose root is <Examples>."""
    out, seen = [], set()
    for fn in sorted(os.listdir(TRANSCRIPTIONS_FOLDER)):
        path = os.path.join(TRANSCRIPTIONS_FOLDER, fn)
        if not fn.endswith('.xml') or not _is_examples_file(path):
            continue
        try:
            root = etree.parse(path, _XML_PARSER).getroot()
        except Exception:
            continue
        for ex in root.findall('.//Example'):
            if ex.get('id') not in seen:          # ids are unique; the first one wins
                seen.add(ex.get('id'))
                out.append(ex)
    return out

def _paper_example(example_id):
    return next((e for e in _paper_examples() if e.get('id') == example_id), None)

def _paper_tokens(ex):
    """{lang code: [token, ...]} from an <Example>'s tiers ('—' = no word in that language)."""
    out = {}
    for code, _abbr, _name in _FN_LANGS:
        tier = ex.find(f'Tier[@lang="{code}"]')
        toks = tier.text.split() if tier is not None and tier.text else []
        out[code] = ['' if t == '\u2014' else t for t in toks]
    return out

def _paper_defaults(ex):
    """Alignment + glosses exactly as published; used until the author edits them."""
    tokens  = _paper_tokens(ex)
    glosses = (ex.findtext('Glosses') or '').split()
    n = max([len(glosses)] + [len(v) for v in tokens.values()])
    for c in tokens:
        tokens[c] += [''] * (n - len(tokens[c]))
    return {'tokens': tokens, 'glosses': glosses + [''] * (n - len(glosses))}

def _paper_link_map(ex):
    """(lang code, cleaned form) -> dictionary entry id, from the example's <TokenLinks>.
    Keyed by form rather than column, so the links survive a re-alignment by the author."""
    toks, links = _paper_tokens(ex), {}
    for tk in ex.findall('TokenLinks/Token'):
        idx, did = tk.get('index', ''), tk.get('dictId', '')
        if idx.isdigit() and did:
            for code in toks:
                t = toks[code][int(idx)] if int(idx) < len(toks[code]) else ''
                if t:
                    links[(code, _clean_form(t))] = did
    return links

def _paper_state(ex):
    """(tokens, column glosses, n columns, translation) to display for an example."""
    stored = _load_stored_glosses('papers_0').get(ex.get('id'))
    d = _paper_defaults(ex)
    if isinstance(stored, dict) and isinstance(stored.get('tokens'), dict):
        tokens, glosses = stored['tokens'], stored.get('glosses', [])
    else:
        tokens, glosses = d['tokens'], d['glosses']
    n_cols = max((len(tokens.get(c, [])) for c, _, _ in _FN_LANGS), default=0)
    transl = (stored.get('translation') if isinstance(stored, dict) and stored.get('translation') is not None
              else (ex.findtext('Translation[@lang="eng"]') or '').strip())
    return tokens, glosses, n_cols, transl

def _cite_fn_table(tokens, col_glosses, n_cols, transl, ref, n, dict_links=None):
    """Numbered five-language example: aligned forms, gloss line, translation, reference.
    Each form carries data-lang / data-form / data-gloss so the page can link it to the
    dictionary (only where the gloss agrees); words with a known entry also carry data-dict-id."""
    dict_links = dict_links or {}
    lang_rows = ''
    for code, abbr, name in _FN_LANGS:
        color = LANG_COLORS.get(name, '#888')
        toks, cells = tokens.get(code, []), ''
        for i in range(n_cols):
            tok   = toks[i] if i < len(toks) else ''
            gl    = col_glosses[i] if i < len(col_glosses) else ''
            shown = tok or '\u2014'
            link  = dict_links.get((code, _clean_form(tok))) if tok else None
            attrs = (f' data-lang="{code}" data-form="{_esc(shown)}" data-gloss="{_esc(gl)}"'
                     + (f' data-dict-id="{_esc(link)}"' if link else ''))
            cells += f'<td class="cite-fn-form" style="color:{color};"{attrs}>{_esc(shown)}</td>'
        lang_rows += f'<tr><td class="cite-fn-abbr" style="color:{color};">{abbr}</td>{cells}</tr>'
    sep    = '<td></td>' * (n_cols + 1)
    gcells = ''.join(f'<td class="cite-fn-gloss">{_esc(col_glosses[i]) if i < len(col_glosses) else ""}</td>'
                     for i in range(n_cols))
    return (f'<div class="grammar-cite">'
            f'<span class="cite-n">({n})</span>'
            f'<div class="cite-body">'
            f'<div class="cite-ilg"><table class="cite-fn-table">{lang_rows}'
            f'<tr class="cite-fn-sep">{sep}</tr>'
            f'<tr><td></td>{gcells}</tr></table></div>'
            f'<div class="cite-transl">\u2018{_esc(transl)}\u2019</div>'
            f'<div class="cite-ref">[{_esc(ref)}]</div>'
            f'</div></div>')

def build_papers_citation(example_id, n):
    """{{cite: papers#ID}} - an example from the "Examples from papers" text."""
    ex = _paper_example(example_id)
    if ex is None:
        return f'<span class="shortcode-error">Example not found in "{PAPERS_TITLE}": {_esc(example_id)}</span>'
    tokens, glosses, n_cols, transl = _paper_state(ex)
    label = (ex.findtext('Label') or '').strip()
    ref   = f'{PAPERS_TITLE} \u00b7 {label}' if label else f'{PAPERS_TITLE} \u00b7 {example_id}'
    return _cite_fn_table(tokens, glosses, n_cols, transl, ref, n, _paper_link_map(ex))

def build_citation(spec, n):
    """Dispatch {{cite: spec}} — all exceptions become inline error spans, never HTML."""
    try:
        if spec.startswith('papers#'):
            return build_papers_citation(spec.split('#', 1)[1].strip(), n)
        if spec.startswith('fieldnotes#'):
            parts = spec.split('#', 2)
            if len(parts) < 3:
                return f'<span class="shortcode-error">Invalid fieldnotes cite: {spec}</span>'
            try:
                idx = int(parts[1])
            except ValueError:
                return f'<span class="shortcode-error">Bad group index: {parts[1]}</span>'
            return build_fieldnotes_citation(idx, parts[2].strip(), n)
        elif '#' in spec:
            filename, sent_id = spec.split('#', 1)
            return build_narrative_citation(filename.strip(), sent_id.strip(), n)
        return f'<span class="shortcode-error">Invalid cite spec: {spec}</span>'
    except Exception as e:
        import traceback as _tb
        return (f'<details class="shortcode-error">'
                f'<summary>Citation error: {e}</summary>'
                f'<pre>{_tb.format_exc()}</pre></details>')

#  SHORTCODE RESOLVERS
# ══════════════════════════════════════════════════════════════

def build_example_table(ex_id, n=None):
    """
    Resolve {{example: ID}} — builds a numbered five-language interlinear example
    from the corpus XML: "(n)  <source label>", the aligned forms, the gloss line
    and the translation. Each language row carries data-lang="…" so the client-side
    language-toggle pills can show/hide rows without a round-trip.
    Words that have no explicit <TokenLinks> entry still carry data-lang / data-form /
    data-gloss, so the page can link them to the dictionary - but only where the
    gloss agrees with the dictionary entry (so a homophone is not linked wrongly).
    """
    ex = _paper_example(ex_id)
    if ex is None:
        return f'<p class="shortcode-error">Example not found in "Examples from papers": <code>{_esc(ex_id)}</code></p>'

    translation  = ex.findtext('Translation[@lang="eng"]', '').strip()
    glosses_raw  = ex.findtext('Glosses', '').strip()
    glosses      = glosses_raw.split() if glosses_raw else []
    label        = (ex.findtext('Label') or '').strip()
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
            f_esc   = _esc(form)
            if form == '—':
                cells += '<td class="ex-cell ex-dash">—</td>'
            elif dict_id:
                cells += (f'<td class="ex-cell">'
                          f'<a class="lexlink" href="dictionary.html#{dict_id}" '
                          f'data-dict-id="{dict_id}">{f_esc}</a></td>')
            else:
                g_esc = _esc(glosses[i]) if i < len(glosses) else ''
                cells += (f'<td class="ex-cell" data-lang="{code}" '
                          f'data-form="{f_esc}" data-gloss="{g_esc}">{f_esc}</td>')

        rows_html += (f'<tr data-lang="{lang}">'
                      f'<td class="ex-abbr" style="color:{color};">{abbr}</td>'
                      f'{cells}</tr>\n')

    # Separator + gloss row
    n_cols     = len(glosses)
    sep_cells  = '<td></td>' + '<td></td>' * n_cols
    gloss_cells = ''.join(f'<td class="ex-gloss">{_esc(g)}</td>' for g in glosses)

    pangloss_link = ''
    if pangloss_url:
        pangloss_link = (f'<a class="corpus-ref" href="{_esc(pangloss_url)}" target="_blank" '
                         f'rel="noopener">🎧 Pangloss archive →</a>')

    number = f'<span class="cite-n">({n})</span>' if n is not None else ''
    source = f'<div class="ex-source">{_esc(label)}</div>' if label else ''
    transl = f'<div class="ex-transl">\u2018{_esc(translation)}\u2019</div>' if translation else ''

    return f'''<div class="example-block grammar-cite" data-example-id="{_esc(ex_id)}">
  {number}
  <div class="cite-body">
    {source}
    <div class="example-wrap">
      <table class="ex-table">
        {rows_html}
        <tr class="ex-sep">{sep_cells}</tr>
        <tr><td class="ex-gloss-empty"></td>{gloss_cells}</tr>
      </table>
      {transl}
      {pangloss_link}
    </div>
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

    # A shortcode alone on a line becomes <p>{{…}}</p>; the block it expands to must not sit in a <p>
    html = re.sub(r'<p>\s*(\{\{\s*(?:example|cite)\s*:[^}]*\}\})\s*</p>', r'\1', html)

    # {{example:}} and {{cite:}} share one counter, numbered in document order
    counter = [0]
    def _numbered(m):
        counter[0] += 1
        kind, arg = m.group(1), m.group(2).strip()
        return (build_example_table(arg, counter[0]) if kind == 'example'
                else build_citation(arg, counter[0]))
    html = re.sub(r'\{\{\s*(example|cite)\s*:\s*([^\}]+)\}\}', _numbered, html)

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

# ── "Examples from papers" text: same shape as a fieldnotes text, so the viewer reuses it ──
@app.route('/api/papers/groups')
def papers_groups():
    n = len(_paper_examples())
    return jsonify({'groups': [{'index': 0, 'title': PAPERS_TITLE, 'count': n}] if n else []})

@app.route('/api/papers/tx/<int:index>')
def papers_tx(index):
    if index != 0:
        return jsonify({'error': 'Group not found'}), 404
    try:
        sentences = []
        for ex in _paper_examples():
            toks = _paper_tokens(ex)
            words = [{'form': ' '.join(t for t in toks[code] if t) or '\u2014',
                      'gloss': abbr, 'lang': code, 'lang_name': name}
                     for code, abbr, name in _FN_LANGS]
            sentences.append({
                'id': ex.get('id'), 'form': '', 'label': (ex.findtext('Label') or '').strip(),
                'transl': (ex.findtext('Translation[@lang="eng"]') or '').strip(),
                'transl_lang': 'eng', 'words': words, 'has_gloss': True,
                'is_comparative': True, 'audio': None})
        return jsonify({'title': PAPERS_TITLE, 'is_fieldnotes': True, 'is_papers': True,
                        'lang': 'comparative', 'sentences': sentences})
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@app.route('/api/papers/tx/<int:index>/glosses', methods=['GET'])
def get_papers_glosses(index):
    # the alignment and glosses as published, overlaid with whatever the author has saved
    merged = {e.get('id'): _paper_defaults(e) for e in _paper_examples()}
    merged.update(_load_stored_glosses('papers_0'))
    return jsonify(merged)

@app.route('/api/papers/tx/<int:index>/glosses', methods=['POST'])
def save_papers_gloss(index):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json(silent=True) or {}
    sent_id = data.get('sentence_id', '')
    if not sent_id:
        return jsonify({'error': 'No sentence_id'}), 400
    stored = _load_stored_glosses('papers_0')
    stored[sent_id] = data.get('gloss', '')
    p, tmp = _gloss_path('papers_0'), _gloss_path('papers_0') + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(stored, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)
    return jsonify({'ok': True})

@app.route('/api/fieldnotes/tx/<int:index>/glosses', methods=['GET'])
def get_fieldnotes_glosses(index):
    """Dedicated gloss GET for fieldnotes — avoids routing ambiguity."""
    return jsonify(_load_stored_glosses(f'fieldnotes_{index}'))

@app.route('/api/fieldnotes/tx/<int:index>/glosses', methods=['POST'])
def save_fieldnotes_gloss(index):
    """Dedicated gloss POST for fieldnotes — avoids routing ambiguity."""
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json(silent=True) or {}
    sent_id = data.get('sentence_id', '')
    gloss   = data.get('gloss', '')
    if not sent_id:
        return jsonify({'error': 'No sentence_id'}), 400
    p      = _gloss_path(f'fieldnotes_{index}')
    stored = _load_stored_glosses(f'fieldnotes_{index}')   # robust: handles corrupted files
    stored[sent_id] = gloss
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(stored, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)
    return jsonify({'ok': True})

@app.route('/api/fieldnotes/tx/<int:index>')
def fieldnotes_tx(index):
    """Return a fieldnotes tiGroup in transcription-viewer format."""
    try:
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
            grp = rfg.find('bslGroup')
            if grp is None:
                grp = rfg.find('frGroup')
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
                    'form':          '',
                    'transl':        prompt,
                    'transl_lang':   'bsl',
                    'words':         words,
                    'has_gloss':     True,
                    'is_comparative': True,
                    'audio':         None,
                })
        return jsonify({
            'title':        ti,
            'is_fieldnotes': True,
            'lang':         'comparative',
            'sentences':    sentences,
        })
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


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
    })


# ── Grammar sections ──────────────────────────────────────────

@app.route('/api/grammar/<section_id>')
def get_grammar_html(section_id):
    path = _section_path(section_id)
    if not os.path.exists(path):
        return jsonify({'error': f'Section not found: {section_id}'}), 404
    with open(path, encoding='utf-8') as f:
        source = f.read()
    try:
        html = render_grammar(source)
    except Exception as e:
        html = f'<div class="shortcode-error">Render error: {e}</div>'
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
    try:
        html = render_grammar(source)
    except Exception as e:
        html = f'<div class="shortcode-error">Render error: {e}</div>'
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
_ABBREV_LINKS_PATH      = os.path.join(TRANSCRIPTIONS_FOLDER, 'abbrev_links.json')
_CONFIRMED_GLOSSES_PATH = os.path.join(TRANSCRIPTIONS_FOLDER, 'confirmed_glosses.json')

def _load_confirmed_glosses():
    if os.path.exists(_CONFIRMED_GLOSSES_PATH):
        with open(_CONFIRMED_GLOSSES_PATH, encoding='utf-8') as f:
            content = f.read().strip()
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                try:
                    obj, _ = json.JSONDecoder().raw_decode(content)
                    return obj if isinstance(obj, dict) else {}
                except Exception:
                    pass
    return {}

_PROPOSED_ENTRIES_PATH = os.path.join(TRANSCRIPTIONS_FOLDER, 'proposed_entries.json')

def _load_proposed_entries():
    if os.path.exists(_PROPOSED_ENTRIES_PATH):
        with open(_PROPOSED_ENTRIES_PATH, encoding='utf-8') as f:
            content = f.read().strip()
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                try:
                    obj, _ = json.JSONDecoder().raw_decode(content)
                    return obj if isinstance(obj, dict) else {}
                except Exception:
                    pass
    return {}

def _save_proposed_entries(data):
    tmp = _PROPOSED_ENTRIES_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _PROPOSED_ENTRIES_PATH)

def _existing_dict_forms():
    """Return a set of lowercase forms already in the dictionary."""
    d = get_dict_xml()
    if d is None:
        return set()
    forms = set()
    for el in d.findall('.//EntréeLexicale'):
        for node in el.findall('Lemme/ReprésentationDeForme'):
            if node.text:
                forms.add(node.text.strip().lower())
    return forms

@app.route('/api/dictionary/proposed')
def get_proposed_entries():
    return jsonify(_load_proposed_entries())

@app.route('/api/dictionary/proposed', methods=['POST'])
def save_proposed_entries():
    """Receive {colKey: {gloss, examples}} from confirmed sentences.
    Skip any entry whose forms are already in the dictionary."""
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data       = request.get_json(silent=True) or {}
    stored     = _load_proposed_entries()
    existing   = _existing_dict_forms()
    fn_codes   = [c for c, _, _ in _FN_LANGS]

    for col_key, entry_data in data.items():
        gloss    = entry_data.get('gloss', '').strip()
        examples = entry_data.get('examples', [])
        if not gloss:
            continue
        # Decode forms from col_key (positional: num|drg|kro|olr|lkn)
        parts = col_key.split('|')
        forms = {fn_codes[i]: parts[i] for i in range(min(len(fn_codes), len(parts)))}
        # Skip if any form already in dictionary
        if any(f.strip().lower() in existing for f in forms.values() if f and f != '—'):
            continue
        if col_key not in stored:
            stored[col_key] = {'gloss': gloss, 'forms': forms, 'examples': []}
        # Merge examples (deduplicate by sentence_id)
        known = {e['sentence_id'] for e in stored[col_key]['examples']}
        for ex in examples:
            if ex.get('sentence_id') not in known:
                stored[col_key]['examples'].append(ex)
                known.add(ex.get('sentence_id'))

    _save_proposed_entries(stored)
    return jsonify({'ok': True})

@app.route('/api/dictionary/proposed/add', methods=['POST'])
def add_proposed_to_dictionary():
    """Add a proposed entry to the dictionary XML and remove it from proposed."""
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json(silent=True) or {}
    col_key = data.get('col_key', '')
    stored  = _load_proposed_entries()
    if col_key not in stored:
        return jsonify({'error': 'Entry not found'}), 404
    entry = stored[col_key]
    gloss = entry.get('gloss', '')
    forms = entry.get('forms', {})

    # Find the active dictionary file
    dict_path = os.path.join(UPLOAD_FOLDER, 'dictionary.xml')
    if not os.path.exists(dict_path):
        dict_path = 'dbt_dictionary.xml'
    if not os.path.exists(dict_path):
        return jsonify({'error': 'Dictionary XML not found'}), 404

    tree = etree.parse(dict_path, _XML_PARSER)
    root = tree.getroot()

    # Generate a unique identifiant
    base_id   = re.sub(r'[^a-zA-Z0-9]', '_', gloss.lower())[:20]
    entry_id  = f'proposed_{base_id}'
    taken     = {el.get('identifiant', '') for el in root.findall('.//EntréeLexicale')}
    counter   = 1
    while entry_id in taken:
        entry_id = f'proposed_{base_id}_{counter}'; counter += 1

    dictionnaire = root.find('Dictionnaire')
    if dictionnaire is None:
        return jsonify({'error': 'No <Dictionnaire> element in XML'}), 500

    # Build new entry element
    el    = etree.SubElement(dictionnaire, 'EntréeLexicale', identifiant=entry_id)
    lemme = etree.SubElement(el, 'Lemme')
    for code in [c for c, _, _ in _FN_LANGS]:
        form = forms.get(code, '').strip()
        if form and form != '—':
            etree.SubElement(lemme, 'ReprésentationDeForme', langue=code).text = form
    etree.SubElement(el, 'ClasseGrammaticale')
    etree.SubElement(el, 'DomaineSémantique')
    sens = etree.SubElement(el, 'Sens', identifiant=f'{entry_id}\u24a2{1}')
    etree.SubElement(sens, 'NuméroDeSens').text = '1'
    glose = etree.SubElement(sens, 'Glose'); glose.set('langue', 'eng'); glose.text = gloss
    etree.SubElement(sens, 'gloss').text = gloss

    # Write back atomically
    tmp = dict_path + '.tmp'
    tree.write(tmp, pretty_print=True, encoding='UTF-8', xml_declaration=True)
    os.replace(tmp, dict_path)

    # Remove from proposed
    del stored[col_key]
    _save_proposed_entries(stored)
    return jsonify({'ok': True, 'id': entry_id})

@app.route('/api/dictionary/proposed/dismiss', methods=['POST'])
def dismiss_proposed_entry():
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    col_key = (request.get_json(silent=True) or {}).get('col_key', '')
    stored  = _load_proposed_entries()
    stored.pop(col_key, None)
    _save_proposed_entries(stored)
    return jsonify({'ok': True})

@app.route('/api/confirmed_glosses')
def get_confirmed_glosses():
    return jsonify(_load_confirmed_glosses())

@app.route('/api/confirmed_glosses', methods=['POST'])
def save_confirmed_glosses():
    """Receive {colKey: [gloss, ...]} pairs from confirmed sentences."""
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data   = request.get_json(silent=True) or {}
    stored = _load_confirmed_glosses()
    for col_key, glist in data.items():
        if col_key not in stored:
            stored[col_key] = []
        for g in glist:
            if g and g not in stored[col_key]:
                stored[col_key].append(g)
    tmp = _CONFIRMED_GLOSSES_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(stored, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _CONFIRMED_GLOSSES_PATH)
    return jsonify({'ok': True})

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

def _dict_path():
    """Return path of the currently active dictionary XML."""
    p = os.path.join(UPLOAD_FOLDER, 'dictionary.xml')
    return p if os.path.exists(p) else 'dbt_dictionary.xml'

def _read_dict():
    return etree.parse(_dict_path(), _XML_PARSER)

def _write_dict(tree):
    p   = _dict_path()
    tmp = p + '.tmp'
    tree.write(tmp, pretty_print=True, encoding='UTF-8', xml_declaration=True)
    os.replace(tmp, p)

def _build_entry_el(data, existing_ids=None, force_id=None):
    """Build an <EntréeLexicale> lxml element from a dict of field values."""
    LANG_CODES_5 = ['num','drg','kro','olr','lkn']
    forms  = data.get('forms', {})
    pos    = data.get('pos', '')
    domain = data.get('domain', '')
    gloss  = data.get('gloss', '')
    short  = data.get('shortGloss', '') or gloss
    notes  = data.get('notes', '')
    etym   = data.get('etym', {})  # {lang, form, gloss, tlopo, etymograph}

    # Generate or validate ID
    if force_id:
        eid = force_id
    else:
        base = re.sub(r'[^a-zA-Z0-9]', '_',
                      (forms.get('kro') or forms.get('num') or gloss or 'new').lower())[:20]
        eid  = base; n = 1
        while existing_ids and eid in existing_ids:
            eid = f'{base}_{n}'; n += 1

    el    = etree.Element('EntréeLexicale', identifiant=eid)
    lemme = etree.SubElement(el, 'Lemme')
    for code in LANG_CODES_5:
        form = (forms.get(code) or '').strip()
        if form:
            etree.SubElement(lemme, 'ReprésentationDeForme', langue=code).text = form
    etree.SubElement(el, 'ClasseGrammaticale').text   = pos
    etree.SubElement(el, 'DomaineSémantique').text    = domain

    if etym and etym.get('form'):
        etym_el = etree.SubElement(el, 'Étymologie')
        ety     = etree.SubElement(etym_el, 'Étymon')
        etree.SubElement(ety, 'Langue').text     = etym.get('lang', 'POc')
        etree.SubElement(ety, 'Forme').text      = etym.get('form', '')
        etree.SubElement(ety, 'Glose', langue='eng').text = etym.get('gloss', '')
        if etym.get('tlopo'):
            etree.SubElement(ety, 'LienTLOPO').text      = etym['tlopo']
        if etym.get('etymograph'):
            etree.SubElement(ety, 'LienEtymograph').text = etym['etymograph']

    sens = etree.SubElement(el, 'Sens', identifiant=f'{eid}\u24a2{1}')
    etree.SubElement(sens, 'NuméroDeSens').text = '1'
    glose = etree.SubElement(sens, 'Glose'); glose.set('langue','eng'); glose.text = gloss
    etree.SubElement(sens, 'gloss').text = short
    if notes:
        n_el = etree.SubElement(sens, 'Notes')
        etree.SubElement(n_el, 'ReprésentationDeTexte', langue='eng').text = notes
    return el, eid

# ── Dictionary CRUD ───────────────────────────────────────────

@app.route('/api/dictionary/xml')
def dictionary_xml():
    """Serve the ACTIVE dictionary XML - the very file the add/edit/delete routes write to
    (an uploaded dictionary if there is one, otherwise dbt_dictionary.xml). The pages load
    the dictionary from here instead of guessing which file is current."""
    from flask import Response
    p = _dict_path()
    if not os.path.exists(p):
        return jsonify({'error': 'Dictionary XML not found'}), 404
    with open(p, 'rb') as f:
        data = f.read()
    return Response(data, mimetype='application/xml',
                    headers={'Cache-Control': 'no-store'})

@app.route('/api/dictionary/entry', methods=['POST'])
def add_dict_entry():
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    try:
        tree = _read_dict()
        root = tree.getroot()
        existing = {el.get('identifiant','') for el in root.findall('.//EntréeLexicale')}
        dictionnaire = root.find('Dictionnaire')
        if dictionnaire is None:
            return jsonify({'error': 'No <Dictionnaire> element'}), 500
        el, eid = _build_entry_el(data, existing_ids=existing)
        dictionnaire.append(el)
        _write_dict(tree)
        return jsonify({'ok': True, 'id': eid})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dictionary/entry/<entry_id>', methods=['PUT'])
def update_dict_entry(entry_id):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json(silent=True) or {}
    try:
        tree = _read_dict()
        root = tree.getroot()
        old  = root.find(f'.//EntréeLexicale[@identifiant="{entry_id}"]')
        if old is None:
            return jsonify({'error': 'Entry not found'}), 404
        parent = old.getparent()
        idx    = list(parent).index(old)
        new_el, _ = _build_entry_el(data, force_id=entry_id)
        parent.remove(old)
        parent.insert(idx, new_el)
        _write_dict(tree)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dictionary/entry/<entry_id>', methods=['DELETE'])
def delete_dict_entry(entry_id):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        tree = _read_dict()
        root = tree.getroot()
        el   = root.find(f'.//EntréeLexicale[@identifiant="{entry_id}"]')
        if el is None:
            return jsonify({'error': 'Entry not found'}), 404
        el.getparent().remove(el)
        _write_dict(tree)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Text examples for dictionary entries ─────────────────────────────────────
# An entry's examples are the sentences, in texts whose glosses the author has
# CONFIRMED, that contain one of its forms. Computed on the fly, so they stay in
# sync with confirmations and also work for entries added earlier.

_DBT_CODES = ['num', 'drg', 'kro', 'olr', 'lkn']
# Language code used in a transcription XML (xml:lang) -> DBT language code.
# Languages that are not Gaua languages (e.g. Lo-Toga, Mwotlap) are simply absent.
_TX_LANG_TO_CODE = {'wwo': 'drg', 'drg': 'drg', 'lkn': 'lkn', 'krf': 'kro',
                    'kro': 'kro', 'num': 'num', 'olr': 'olr'}

def _clean_form(s):
    """Lower-case a form and strip morpheme-boundary and punctuation marks."""
    return re.sub(r'^[-=]+|[-=.,;!?]+$', '', (s or '').strip()).lower()

@app.route('/api/dictionary/examples')
def dictionary_examples():
    try:
        d = get_dict_xml()
        if d is None:
            return jsonify({})
        entry_forms = {}
        for el in d.findall('.//EntréeLexicale'):
            forms = {}
            for node in el.findall('Lemme/ReprésentationDeForme'):
                code = node.get('langue', '')
                c = _clean_form(node.text)
                if code in _DBT_CODES and c and c != '\u2014':
                    forms[code] = c
            if forms:
                entry_forms[el.get('identifiant', '')] = forms
        result = {eid: [] for eid in entry_forms}

        # ---- fieldwork-style texts (fieldnotes + examples from papers): five parallel languages ----
        fx = get_fieldnotes_xml()
        groups = fx.findall('.//tiGroup') if fx is not None else []
        sources = []   # (type, index, gloss-store key, title, {sentence id: default translation})
        for fname in sorted(os.listdir(GLOSSES_FOLDER)):
            m = re.fullmatch(r'fieldnotes_(\d+)\.json', fname)
            if not m:
                continue
            idx = int(m.group(1))
            title, prompts = '', {}
            if idx < len(groups):
                title = (groups[idx].findtext('ti') or '').strip()
                for rfg in groups[idx].findall('rfGroup'):
                    grp = rfg.find('bslGroup')
                    if grp is None:
                        grp = rfg.find('frGroup')
                    if grp is not None:
                        prompts[(rfg.findtext('rf') or '').strip()] = (
                            grp.findtext('bsl') or grp.findtext('fr') or '').strip()
            sources.append(('fieldnotes', idx, f'fieldnotes_{idx}', title, prompts))
        sources.append(('papers', 0, 'papers_0', PAPERS_TITLE,
                        {x.get('id'): (x.findtext('Translation[@lang="eng"]') or '').strip()
                         for x in _paper_examples()}))
        for typ, idx, key, title, prompts in sources:
            stored = _load_stored_glosses(key)
            for sid, g in stored.items():
                if not (isinstance(g, dict) and g.get('confirmed') is True
                        and isinstance(g.get('tokens'), dict)):
                    continue
                tokens = g['tokens']
                n_cols = max((len(tokens.get(c, [])) for c in _DBT_CODES), default=0)
                matched = {}   # entry id -> [column indexes]
                for ci in range(n_cols):
                    col = {c: _clean_form(tokens.get(c, [])[ci]
                                          if ci < len(tokens.get(c, [])) else '')
                           for c in _DBT_CODES}
                    for eid, ef in entry_forms.items():
                        hits = sum(1 for c, v in ef.items() if col.get(c) == v)
                        if hits >= min(2, len(ef)):
                            matched.setdefault(eid, []).append(ci)
                for eid, cols in matched.items():
                    transl = (g.get('translation') if g.get('translation') is not None
                              else prompts.get(sid, ''))
                    result[eid].append({
                        'type': typ, 'index': idx, 'title': title,
                        'sentence_id': sid, 'tokens': tokens,
                        'glosses': g.get('glosses', []),
                        'translation': transl, 'match_cols': cols})

        # ---- transcribed narratives: a single language per sentence ----
        for fn in sorted(os.listdir(TRANSCRIPTIONS_FOLDER)):
            if not fn.endswith('.xml'):
                continue
            stored = _load_stored_glosses(fn)
            confirmed = {sid: g for sid, g in stored.items()
                         if isinstance(g, dict) and g.get('confirmed') is True
                         and isinstance(g.get('tokens'), list)}
            if not confirmed:
                continue
            try:
                data = _parse_tx(os.path.join(TRANSCRIPTIONS_FOLDER, fn))
            except Exception:
                continue
            code = _TX_LANG_TO_CODE.get((data.get('lang') or '').strip())
            if not code:
                continue
            sent_transl = {s['id']: s['transl'] for s in data['sentences']}
            for sid, g in confirmed.items():
                toks = [_clean_form(t) for t in g['tokens']]
                for eid, ef in entry_forms.items():
                    if code not in ef:
                        continue
                    cols = [i for i, t in enumerate(toks) if t == ef[code]]
                    if cols:
                        transl = (g.get('translation') if g.get('translation') is not None
                                  else sent_transl.get(sid, ''))
                        result[eid].append({
                            'type': 'narrative', 'file': fn, 'title': data['title'],
                            'lang': code, 'sentence_id': sid,
                            'tokens': g['tokens'], 'glosses': g.get('glosses', []),
                            'translation': transl, 'match_cols': cols})
        return jsonify({k: v for k, v in result.items() if v})
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

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

# ══════════════════════════════════════════════════════════════
#  LATEX EXPORT
# ══════════════════════════════════════════════════════════════

# Characters that must be escaped in LaTeX prose (not in math/verbatim)
_LATEX_ESC = str.maketrans({
    '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
    '_': r'\_', '{': r'\{', '}': r'\}',
    '~': r'\textasciitilde{}', '^': r'\textasciicircum{}',
    '\\': r'\textbackslash{}',
})

def _le(s):
    """Escape a plain-text string for LaTeX."""
    return str(s).translate(_LATEX_ESC)

# ── Shortcode → LaTeX ─────────────────────────────────────────

def _example_latex(ex_id, n):
    ex = _paper_example(ex_id)
    if ex is None:
        return f'\\textit{{[Example {_le(ex_id)} not found]}}'
    glosses_raw = (ex.findtext('Glosses') or '').split()
    translation = (ex.findtext('Translation[@lang="eng"]') or '').strip()
    label = (ex.findtext('Label') or '').strip()
    cols = [_le(g) for g in glosses_raw]
    rows = []
    for code in LANG_CODES:
        lang = LANG_MAP[code]
        abbr = LANG_ABBR[lang]
        tier = ex.find(f'Tier[@lang="{code}"]')
        if tier is None or not tier.text:
            continue
        forms = [_le(f) for f in tier.text.strip().split()]
        rows.append(f'\\textit{{{_le(abbr)}}} & ' + ' & '.join(forms) + r' \\')
    sep = 'l' * (len(cols) + 1)
    gloss_row = ' & '.join([''] + cols) + r' \\'
    tabular = (
        f'\\begin{{tabular}}[t]{{@{{}}{sep}@{{}}}}\n'
        + '\n'.join(rows) + '\n'
        + r'\midrule' + '\n'
        + gloss_row + '\n'
        + r'\end{tabular}'
    )
    transl = _le(translation)
    label_tex = f'\\textit{{{_le(label)}}}\\\\\n' if label else ''
    return (f'\\begin{{exe}}\n\\ex\\label{{ex:{_le(ex_id)}}}\n'
            f'{label_tex}{tabular}\\\\\n'
            f'\\trans `{transl}\'\n'
            f'\\end{{exe}}')

def _entry_latex(entry_id):
    d = get_dict_xml()
    if d is None:
        return f'\\textit{{{_le(entry_id)}}}'
    el = d.find(f'.//EntréeLexicale[@identifiant="{entry_id}"]')
    if el is None:
        return f'\\textit{{{_le(entry_id)}}}'
    gloss = (el.findtext('Sens/Glose[@langue="eng"]') or entry_id).strip()
    parts = []
    for code in LANG_CODES:
        lang = LANG_MAP[code]
        abbr = LANG_ABBR[lang]
        node = el.find(f'Lemme/ReprésentationDeForme[@langue="{code}"]')
        form = (node.text or '').strip() if node is not None else ''
        if form:
            parts.append(f'{_le(abbr)}.~\\textit{{{_le(form)}}}')
    forms_str = ', '.join(parts)
    return f'\\textit{{{_le(gloss)}}} [{forms_str}]'

def _cite_fieldnotes_latex(group_index, sent_id, n):
    xml = get_fieldnotes_xml()
    if xml is None:
        return f'\\textit{{[Fieldnotes not loaded]}}'
    tgs = xml.findall('.//tiGroup')
    if group_index >= len(tgs):
        return f'\\textit{{[Group {group_index} not found]}}'
    tg  = tgs[group_index]
    rfg = next((r for r in tg.findall('rfGroup')
                if (r.findtext('rf') or '').strip() == sent_id), None)
    if rfg is None:
        return f'\\textit{{[{_le(sent_id)} not found]}}'
    grp    = rfg.find('bslGroup') or rfg.find('frGroup')
    prompt = (grp.findtext('bsl') or grp.findtext('fr') or '').strip() if grp else ''
    stored = _load_stored_glosses(f'fieldnotes_{group_index}').get(sent_id)
    display_transl = (stored.get('translation') if stored and isinstance(stored, dict)
                      and stored.get('translation') is not None else prompt)
    if stored and isinstance(stored, dict) and stored.get('tokens'):
        tokens     = stored['tokens']
        col_glosses = stored.get('glosses', [])
        n_cols = max((len(tokens.get(c, [])) for c, _, _ in _FN_LANGS), default=0)
    else:
        tokens = {}; n_cols = 0
        for code, _, _ in _FN_LANGS:
            toks = _tokenize_form((grp.findall(code)[0].text or '') if grp and grp.findall(code) else '')
            tokens[code] = toks; n_cols = max(n_cols, len(toks))
        col_glosses = [''] * n_cols
        for code, _, _ in _FN_LANGS:
            while len(tokens[code]) < n_cols: tokens[code].append('')
    rows = []
    for code, abbr, _ in _FN_LANGS:
        cells = [_le(tokens[code][i] if i < len(tokens[code]) else '---') for i in range(n_cols)]
        rows.append(f'\\textit{{{_le(abbr)}}} & ' + ' & '.join(cells) + r' \\')
    gloss_cells = [_le(col_glosses[i] if i < len(col_glosses) else '') for i in range(n_cols)]
    sep      = 'l' * (n_cols + 1)
    gloss_row = ' & '.join([''] + gloss_cells) + r' \\'
    tabular = (f'\\begin{{tabular}}[t]{{@{{}}{sep}@{{}}}}\n'
               + '\n'.join(rows) + '\n'
               + r'\midrule' + '\n'
               + gloss_row + '\n'
               + r'\end{tabular}')
    return (f'\\begin{{exe}}\n\\ex\\label{{ex:{n}}}\n'
            f'{tabular}\\\\\n'
            f'\\trans `{_le(display_transl)}\'\n'
            f'\\end{{exe}}')

def _cite_narrative_latex(filename, sent_id, n):
    path = os.path.join(TRANSCRIPTIONS_FOLDER, filename)
    if not os.path.exists(path):
        return f'\\textit{{[{_le(filename)} not found]}}'
    try:
        data = _parse_tx(path)
    except Exception:
        return f'\\textit{{[Parse error in {_le(filename)}]}}'
    sent = next((s for s in data['sentences'] if s['id'] == sent_id), None)
    if not sent:
        return f'\\textit{{[{_le(sent_id)} not found]}}'
    stored = _load_stored_glosses(filename).get(sent_id)
    transl = (stored.get('translation') if stored and isinstance(stored, dict)
              and stored.get('translation') is not None else sent['transl'])
    if sent['has_gloss'] and sent['words']:
        form_cells  = ' & '.join(_le(w['form'])  for w in sent['words'])
        gloss_cells = ' & '.join(_le(w['gloss'] or '') for w in sent['words'])
        sep = 'l' * len(sent['words'])
        body = (f'\\begin{{tabular}}[t]{{@{{}}{sep}@{{}}}}\n'
                f'{form_cells}\\\\\n{gloss_cells}\\\\\n\\end{{tabular}}')
    else:
        manual = (stored if isinstance(stored, str) else '')
        body = f'\\gll {_le(sent["form"])} \\\\\n     {_le(manual)} \\\\'
    return (f'\\begin{{exe}}\n\\ex\\label{{ex:{n}}}\n'
            f'{body}\\\\\n'
            f'\\trans `{_le(transl)}\'\n'
            f'\\end{{exe}}')

# ── Markdown → LaTeX ──────────────────────────────────────────

def _cite_papers_latex(example_id, n):
    ex = _paper_example(example_id)
    if ex is None:
        return f'\\textit{{[{_le(example_id)} not found]}}'
    tokens, col_glosses, n_cols, transl = _paper_state(ex)
    rows = []
    for code, abbr, _ in _FN_LANGS:
        cells = [_le((tokens.get(code, [])[i] if i < len(tokens.get(code, [])) else '') or '---')
                 for i in range(n_cols)]
        rows.append(f'\\textit{{{_le(abbr)}}} & ' + ' & '.join(cells) + r' \\')
    gloss_row = ' & '.join([''] + [_le(col_glosses[i] if i < len(col_glosses) else '') for i in range(n_cols)]) + r' \\'
    label = (ex.findtext('Label') or '').strip()
    label_tex = f'\\textit{{{_le(label)}}}\\\\\n' if label else ''
    tabular = (f'\\begin{{tabular}}[t]{{@{{}}{"l" * (n_cols + 1)}@{{}}}}\n'
               + '\n'.join(rows) + '\n' + r'\midrule' + '\n' + gloss_row + '\n' + r'\end{tabular}')
    return (f'\\begin{{exe}}\n\\ex\\label{{ex:{n}}}\n{label_tex}{tabular}\\\\\n'
            f'\\trans `{_le(transl)}\'\n\\end{{exe}}')

def _md_to_latex_body(source):
    """Convert grammar Markdown (with shortcodes) to a LaTeX body string."""
    counter = [0]

    def resolve_cite(m):
        counter[0] += 1; spec = m.group(1).strip(); n = counter[0]
        try:
            if spec.startswith('papers#'):
                return _cite_papers_latex(spec.split('#', 1)[1].strip(), n)
            if spec.startswith('fieldnotes#'):
                parts = spec.split('#', 2)
                return _cite_fieldnotes_latex(int(parts[1]), parts[2].strip(), n)
            elif '#' in spec:
                fn, sid = spec.split('#', 1)
                return _cite_narrative_latex(fn.strip(), sid.strip(), n)
        except Exception as e:
            return f'\\textit{{[cite error: {_le(str(e))}]}}'
        return f'\\textit{{[invalid cite]}}'

    def resolve_example(m):
        counter[0] += 1
        return _example_latex(m.group(1).strip(), counter[0])

    # 1. Resolve shortcodes
    src = re.sub(r'\{\{\s*cite\s*:\s*([^\}]+)\}\}',    resolve_cite,    source)
    src = re.sub(r'\{\{\s*example\s*:\s*([^\}]+)\}\}', resolve_example, src)
    src = re.sub(r'\{\{\s*entry\s*:\s*([^\}]+)\}\}',
                 lambda m: _entry_latex(m.group(1).strip()), src)

    lines = src.split('\n')
    out   = []
    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False; return
        # Find separator row (--|--|--)
        header = table_rows[0] if table_rows else []
        data   = [r for r in table_rows[1:] if not all(c.strip().replace('-','') == '' for c in r)]
        ncols  = max(len(header), max((len(r) for r in data), default=0))
        sep    = 'l' * ncols
        hcells = ' & '.join(_le(c) for c in header) + r' \\'
        rows   = '\n'.join(' & '.join(_le(c) for c in row) + r' \\' for row in data)
        out.append(f'\\begin{{tabular}}{{@{{}}{sep}@{{}}}}\n\\toprule\n{hcells}\n\\midrule\n{rows}\n\\bottomrule\n\\end{{tabular}}\n')
        in_table = False; table_rows.clear()

    for line in lines:
        # Table row
        if line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            # Skip separator rows
            if not all(c.replace('-','').replace(':','').strip() == '' for c in cells):
                if not in_table: in_table = True
                table_rows.append(cells)
            continue
        else:
            if in_table: flush_table()

        # ATX headings
        m = re.match(r'^(#{1,4})\s+(.*)', line)
        if m:
            depth = len(m.group(1))
            title = _apply_inline(m.group(2))
            cmd   = {1:'section',2:'section',3:'subsection',4:'subsubsection'}[depth]
            out.append(f'\\{cmd}{{{title}}}'); continue

        # Horizontal rule
        if re.match(r'^---+$', line.strip()):
            out.append(r'\medskip\noindent\rule{\linewidth}{0.4pt}\medskip'); continue

        # Blank line
        if not line.strip():
            out.append(''); continue

        # Already a LaTeX block (shortcode output)
        if line.strip().startswith('\\begin{') or line.strip().startswith('\\end{'):
            out.append(line); continue

        # Normal prose line
        out.append(_apply_inline(line))

    if in_table: flush_table()

    # Merge consecutive prose lines into paragraphs
    result = '\n'.join(out)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result

def _apply_inline(text):
    """Apply inline Markdown formatting and escape for LaTeX."""
    # Bold before italic to handle **...**
    text = re.sub(r'\*\*(.+?)\*\*', lambda m: f'\\textbf{{{_le(m.group(1))}}}', text)
    text = re.sub(r'\*(.+?)\*',     lambda m: f'\\textit{{{_le(m.group(1))}}}', text)
    text = re.sub(r'`(.+?)`',       lambda m: f'\\texttt{{{_le(m.group(1))}}}', text)
    # Escape remaining plain text (not already inside \command{})
    # Simple heuristic: escape & % $ # _ outside braces — already done by _le above
    # for the portions not inside LaTeX commands. For inline-converted text we just
    # escape the literal parts between commands.
    return text

_LATEX_DOC = r"""\documentclass[12pt, a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{gb4e}}\noautomath
\usepackage{{booktabs}}
\usepackage{{microtype}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\definecolor{{NumeColor}}{{HTML}}{{2e5c8a}}
\definecolor{{DorigColor}}{{HTML}}{{c07820}}
\definecolor{{KoroColor}}{{HTML}}{{922810}}
\definecolor{{OlratColor}}{{HTML}}{{267040}}
\definecolor{{LakonColor}}{{HTML}}{{5c2878}}
\title{{Comparative Grammar of the Gaua Languages\\
\large Banks Islands, Vanuatu}}
\author{{Alexandre Fran\c{{c}}ois \& Fabio Meroni}}
\date{{\today}}
\begin{{document}}
\maketitle
\tableofcontents
\newpage

{body}

\end{{document}}
"""

@app.route('/api/grammar/export/latex')
def export_grammar_latex():
    """Render all grammar sections as a single downloadable .tex file."""
    sections_latex = []
    for fname in sorted(os.listdir(GRAMMAR_FOLDER)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(GRAMMAR_FOLDER, fname)
        with open(path, encoding='utf-8') as f:
            source = f.read()
        try:
            sections_latex.append(_md_to_latex_body(source))
        except Exception as e:
            sections_latex.append(f'% ERROR in {fname}: {e}')

    body = '\n\n'.join(sections_latex)
    tex  = _LATEX_DOC.format(body=body)

    from flask import Response
    return Response(
        tex,
        mimetype='text/plain; charset=utf-8',
        headers={'Content-Disposition': 'attachment; filename="grammar.tex"'}
    )

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
        if _is_examples_file(path):          # examples from papers, not a recording
            continue
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

@app.route('/api/transcription/<string:text_key>')
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

@app.route('/api/transcription/<string:text_key>/glosses', methods=['GET'])
def get_glosses(text_key):
    # text_key is the XML filename; gloss stored by sanitised filename key
    return jsonify(_load_stored_glosses(text_key))

@app.route('/api/transcription/<string:text_key>/glosses', methods=['POST'])
def save_gloss(text_key):
    if not session.get('author'):
        return jsonify({'error': 'Unauthorized'}), 401
    data    = request.get_json(silent=True) or {}
    sent_id = data.get('sentence_id', '')
    gloss   = data.get('gloss', '')
    if not sent_id:
        return jsonify({'error': 'No sentence_id'}), 400
    p       = _gloss_path(text_key)
    glosses = _load_stored_glosses(text_key)   # robust: handles corrupted files
    glosses[sent_id] = gloss
    # Atomic write: temp file + rename prevents corruption on interrupted saves
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(glosses, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)
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
