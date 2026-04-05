import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Digital Boasian Trilogy — Gaua Languages",
    page_icon="◬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Query params → session state ───────────────────────────────────────────
params = st.query_params
if "word" in params:
    st.session_state["dict_word"] = params["word"]
    st.session_state["page"] = "dictionary"
elif "page" in params and "page" not in st.session_state:
    st.session_state["page"] = params["page"]

if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "dict_word" not in st.session_state:
    st.session_state["dict_word"] = ""

# ── Styles ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600&family=Crimson+Pro:ital,wght@0,300;0,400;1,300;1,400&family=Fira+Sans:wght@300;400;500;600&display=swap');

/* === Root === */
html, body, .stApp { background: #f7f3ed !important; }
.block-container { padding-top: 2rem !important; }

/* === Typography === */
.main-title {
    font-family: 'EB Garamond', serif;
    font-size: 2.8rem;
    font-weight: 500;
    color: #1c0f06;
    letter-spacing: -0.5px;
    line-height: 1.15;
    margin-bottom: 0.15rem;
}
.subtitle {
    font-family: 'Fira Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 300;
    color: #8a6f52;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.section-header {
    font-family: 'EB Garamond', serif;
    font-size: 1.75rem;
    font-weight: 500;
    color: #1c0f06;
    border-bottom: 1.5px solid #c9b99a;
    padding-bottom: 0.3rem;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
}
.body-text {
    font-family: 'Crimson Pro', serif;
    font-size: 1.05rem;
    line-height: 1.82;
    color: #2a1f14;
    margin-bottom: 1rem;
    max-width: 72ch;
}

/* === Gloss boxes === */
.gloss-box {
    background: #fffdf8;
    border-left: 3px solid #a07850;
    border-radius: 0 6px 6px 0;
    padding: 0.8rem 1.3rem;
    margin: 0.6rem 0 1.4rem 2.5rem;
    box-shadow: 0 1px 5px rgba(80,40,0,0.07);
    display: inline-block;
    min-width: 200px;
}
.gloss-table { border-collapse: collapse; margin-bottom: 0.45rem; }
.morph-cell { padding: 2px 14px 2px 0; vertical-align: bottom; }
.morph-cell a {
    font-family: 'EB Garamond', serif;
    font-size: 1.18rem;
    color: #3d1f0b;
    text-decoration: none;
    border-bottom: 1.5px dotted #a07850;
    transition: color 0.15s, border-color 0.15s;
}
.morph-cell a:hover { color: #b84c1e; border-bottom-color: #b84c1e; }
.gloss-cell {
    padding: 0 14px 0 0;
    font-family: 'Fira Sans', sans-serif;
    font-size: 0.73rem;
    font-weight: 400;
    color: #7a6248;
    letter-spacing: 0.04em;
}
.gloss-transl {
    font-family: 'Crimson Pro', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #3a2a1a;
    margin-top: 0.35rem;
}
.gloss-source {
    font-family: 'Fira Sans', sans-serif;
    font-size: 0.68rem;
    color: #b8a08a;
    margin-top: 0.15rem;
    letter-spacing: 0.03em;
}
.lang-chip {
    display: inline-block;
    padding: 1px 9px 2px;
    border-radius: 2px;
    font-family: 'Fira Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: white;
    margin-bottom: 7px;
}
.ex-wrap {
    margin: 0.6rem 0 1.6rem 0;
}
.ex-num {
    font-family: 'Fira Sans', sans-serif;
    font-size: 0.78rem;
    color: #b0906a;
    margin-bottom: 2px;
}

/* === Tables === */
.ling-table { border-collapse: collapse; width: auto; margin: 1.2rem 0 1.6rem 0; background: white; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.07); }
.ling-table th { background: #1c0f06; color: #e8d8c0; font-family: 'Fira Sans', sans-serif; font-size: 0.76rem; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; padding: 8px 16px; text-align: left; }
.ling-table td { padding: 7px 16px; font-family: 'EB Garamond', serif; font-size: 1rem; color: #2a1f14; border-bottom: 1px solid #ede4d7; }
.ling-table tr:last-child td { border-bottom: none; }
.ling-table tr:hover td { background: #faf5ee; }
.ling-table caption { font-family: 'Fira Sans', sans-serif; font-size: 0.73rem; color: #8a7060; text-align: left; padding: 0 0 6px 0; letter-spacing: 0.03em; }

/* === Dictionary === */
.dict-entry {
    background: white;
    border: 1px solid #ddd5c5;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.7rem;
    transition: box-shadow 0.18s;
}
.dict-entry:hover { box-shadow: 0 3px 10px rgba(80,40,0,0.09); }
.dict-entry.highlighted {
    border-color: #a07850;
    box-shadow: 0 0 0 2.5px #d4b896;
    background: #fffdf5;
}
.dict-headword { font-family: 'EB Garamond', serif; font-size: 1.65rem; font-weight: 500; color: #1c0f06; }
.dict-pos { font-family: 'Crimson Pro', serif; font-style: italic; font-size: 0.85rem; color: #a07850; margin-left: 7px; }
.dict-gloss { font-family: 'Crimson Pro', serif; font-size: 1.05rem; color: #2a1f14; margin: 0.25rem 0 0.5rem 0; }
.dict-langs { display: flex; gap: 5px; flex-wrap: wrap; margin: 0.4rem 0; }
.dict-lang-chip { background: #f0e8dc; border-radius: 3px; padding: 2px 8px; font-family: 'Fira Sans', sans-serif; font-size: 0.72rem; color: #5c4030; }
.dict-lang-chip b { color: #3d2010; }
.dict-notes { font-family: 'Crimson Pro', serif; font-style: italic; font-size: 0.92rem; color: #7a6550; margin-top: 0.35rem; }

/* === Texts === */
.text-card {
    border: 1px solid #ddd5c5;
    border-radius: 6px;
    padding: 0.7rem 1.1rem;
    margin-bottom: 0.45rem;
    background: white;
    transition: box-shadow 0.15s;
}
.text-card:hover { box-shadow: 0 2px 8px rgba(80,40,0,0.08); }
.text-title { font-family: 'EB Garamond', serif; font-size: 1.1rem; font-weight: 500; }
.text-title a { color: #1c0f06; text-decoration: none; border-bottom: 1px solid #c9b99a; }
.text-title a:hover { color: #a07850; border-bottom-color: #a07850; }
.text-meta { font-family: 'Fira Sans', sans-serif; font-size: 0.72rem; color: #9a856a; margin-top: 3px; display: flex; gap: 8px; align-items: center; }
.genre-badge { background: #f0e8dc; border-radius: 3px; padding: 1px 8px; font-size: 0.68rem; font-weight: 500; color: #6a4a30; letter-spacing: 0.04em; }

/* === Homepage === */
.dbt-intro {
    font-family: 'Crimson Pro', serif;
    font-size: 1.12rem;
    line-height: 1.85;
    color: #1c0f06;
    max-width: 68ch;
}
.component-card {
    background: white;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    border: 1px solid #ddd5c5;
    height: 100%;
    transition: box-shadow 0.2s;
}
.component-card:hover { box-shadow: 0 4px 14px rgba(80,40,0,0.1); }
.component-card h3 { font-family: 'EB Garamond', serif; font-size: 1.45rem; font-weight: 500; margin-bottom: 0.6rem; color: #1c0f06; }
.component-card p { font-family: 'Crimson Pro', serif; font-size: 0.97rem; color: #5a4535; line-height: 1.7; }

/* === Sidebar === */
section[data-testid="stSidebar"] > div { background: #16090200 !important; }
[data-testid="stSidebar"] { background: #1c0f06 !important; }
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span,
[data-testid="stSidebar"] caption { color: #e0cdb5 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f2e5cc !important; }
[data-testid="stSidebar"] hr { border-color: #3a2010 !important; }
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────
LANG_COLORS = {
    "Nume":  "#3d6b9e",
    "Dorig": "#c87d30",
    "Koro":  "#b03020",
    "Olrat": "#2d8a50",
    "Lakon": "#6b3090",
}

TEXTS_DATA = {
    "Nume": [
        {"title": "The origin of fire",           "url": "https://pangloss.cnrs.fr/corpus/Nume", "genre": "Myth",               "recorder": "A. François", "year": "2000"},
        {"title": "How the sea became salt",       "url": "https://pangloss.cnrs.fr/corpus/Nume", "genre": "Myth",               "recorder": "A. François", "year": "2001"},
        {"title": "Fishing with nets",             "url": "https://pangloss.cnrs.fr/corpus/Nume", "genre": "Procedural",         "recorder": "A. François", "year": "2000"},
        {"title": "The orphan and the chief",      "url": "https://pangloss.cnrs.fr/corpus/Nume", "genre": "Narrative",          "recorder": "A. François", "year": "2002"},
    ],
    "Dorig": [
        {"title": "Qat and his brothers",          "url": "https://pangloss.cnrs.fr/corpus/Dorig", "genre": "Myth",              "recorder": "A. François", "year": "2001"},
        {"title": "Building a canoe",              "url": "https://pangloss.cnrs.fr/corpus/Dorig", "genre": "Procedural",        "recorder": "A. François", "year": "2002"},
        {"title": "The flying fox and the rat",    "url": "https://pangloss.cnrs.fr/corpus/Dorig", "genre": "Fable",             "recorder": "A. François", "year": "2001"},
        {"title": "A feast in the village",        "url": "https://pangloss.cnrs.fr/corpus/Dorig", "genre": "Personal narrative","recorder": "A. François", "year": "2003"},
    ],
    "Koro": [
        {"title": "The origin of the coconut",     "url": "https://pangloss.cnrs.fr/corpus/Koro_Gaua", "genre": "Myth",         "recorder": "A. François", "year": "2003"},
        {"title": "A journey to Santo",            "url": "https://pangloss.cnrs.fr/corpus/Koro_Gaua", "genre": "Personal narrative","recorder": "A. François", "year": "2004"},
        {"title": "Kava ceremonies",               "url": "https://pangloss.cnrs.fr/corpus/Koro_Gaua", "genre": "Procedural",   "recorder": "A. François", "year": "2003"},
        {"title": "The jealous brother",           "url": "https://pangloss.cnrs.fr/corpus/Koro_Gaua", "genre": "Narrative",    "recorder": "A. François", "year": "2005"},
        {"title": "Preparing a garden",            "url": "https://pangloss.cnrs.fr/corpus/Koro_Gaua", "genre": "Procedural",   "recorder": "A. François", "year": "2004"},
    ],
    "Olrat": [
        {"title": "The woman who became stone",    "url": "https://pangloss.cnrs.fr/corpus/Olrat", "genre": "Myth",             "recorder": "A. François", "year": "2004"},
        {"title": "Garden magic spells",           "url": "https://pangloss.cnrs.fr/corpus/Olrat", "genre": "Ritual speech",    "recorder": "A. François", "year": "2004"},
        {"title": "Childhood memories",            "url": "https://pangloss.cnrs.fr/corpus/Olrat", "genre": "Personal narrative","recorder": "A. François", "year": "2005"},
    ],
    "Lakon": [
        {"title": "Origin of the Lakon dances",   "url": "https://pangloss.cnrs.fr/corpus/Lakon", "genre": "Myth",              "recorder": "A. François", "year": "2006"},
        {"title": "A day of fishing",              "url": "https://pangloss.cnrs.fr/corpus/Lakon", "genre": "Personal narrative","recorder": "A. François", "year": "2007"},
        {"title": "The seven brothers",            "url": "https://pangloss.cnrs.fr/corpus/Lakon", "genre": "Traditional narrative","recorder": "A. François","year": "2006"},
        {"title": "Healing plants of Gaua",        "url": "https://pangloss.cnrs.fr/corpus/Lakon", "genre": "Ethnobotanical",   "recorder": "A. François", "year": "2007"},
    ],
}

DICTIONARY = {
    "kan": {
        "gloss": "eat",
        "pos": "v.tr",
        "langs": {"Nume":"kan","Dorig":"kan","Koro":"kan","Olrat":"kan","Lakon":"kan"},
        "notes": "Transitive verb requiring a direct object. Subject agreement expressed through proclitic (no=kan '1sg eats').",
    },
    "mōtō": {
        "gloss": "taro (Colocasia esculenta)",
        "pos": "n",
        "langs": {"Nume":"mōtō","Dorig":"mōtō","Koro":"mōtō","Olrat":"mōto","Lakon":"mōtō"},
        "notes": "Staple food crop throughout Gaua. Takes food-class possessive classifier.",
    },
    "lō": {
        "gloss": "go",
        "pos": "v.intr",
        "langs": {"Nume":"lō","Dorig":"lō","Koro":"lō","Olrat":"lō","Lakon":"lō"},
        "notes": "Intransitive motion verb. Often followed by a directional verb to specify orientation or direction.",
    },
    "wia": {
        "gloss": "see, look at",
        "pos": "v.tr",
        "langs": {"Nume":"wia","Dorig":"wia","Koro":"wia","Olrat":"wia","Lakon":"wia"},
        "notes": "Transitive visual perception verb. Also used for 'find' in some contexts.",
    },
    "gōr": {
        "gloss": "man, person",
        "pos": "n",
        "langs": {"Nume":"gōr","Dorig":"gōr","Koro":"gōr","Olrat":"gōr","Lakon":"gōr"},
        "notes": "Common noun referring to an adult male; used generically for 'person' in some contexts.",
    },
    "ēgēl": {
        "gloss": "village",
        "pos": "n",
        "langs": {"Nume":"ēgēl","Dorig":"ēgēl","Koro":"ēgēl","Olrat":"ēgēl","Lakon":"ēgēl"},
        "notes": "Noun referring to an inhabited settlement; central concept in social organization.",
    },
    "are": {
        "gloss": "DEM — proximal demonstrative",
        "pos": "det",
        "langs": {"Nume":"are","Dorig":"are","Koro":"are","Olrat":"are","Lakon":"are"},
        "notes": "Post-nominal proximal demonstrative determiner. Invariant across all five languages.",
    },
    "qēt": {
        "gloss": "COMPL — completive aspect",
        "pos": "part",
        "langs": {"Nume":"qēt","Dorig":"qēt","Koro":"qēt","Olrat":"qēt","Lakon":"qēt"},
        "notes": "Post-verbal completive/perfective aspect particle. Invariant form across all five languages — a remarkable isogloss.",
    },
    "wer": {
        "gloss": "big, large",
        "pos": "v.stat",
        "langs": {"Nume":"wer","Dorig":"wer","Koro":"wer","Olrat":"wer","Lakon":"wer"},
        "notes": "Stative predicate verb; also used attributively in post-nominal position.",
    },
    "no": {
        "gloss": "I — 1st person singular",
        "pos": "pro",
        "langs": {"Nume":"no","Dorig":"no","Koro":"no","Olrat":"no","Lakon":"no"},
        "notes": "1sg free pronoun and subject proclitic (no=) prefixed to the verb.",
    },
    "o": {
        "gloss": "she/he/it — 3rd person singular",
        "pos": "pro",
        "langs": {"Nume":"o","Dorig":"o","Koro":"o","Olrat":"o","Lakon":"o"},
        "notes": "3sg subject proclitic (o=) prefixed to the verb; homophonous with 2sg in most languages.",
    },
    "tō": {
        "gloss": "NEG — negation particle",
        "pos": "part",
        "langs": {"Nume":"tō","Dorig":"tō","Koro":"tō","Olrat":"tō","Lakon":"tō"},
        "notes": "Pre-verbal negation particle; part of a potentially discontinuous negation construction with post-verbal suffix -(V)t.",
    },
    "qōl": {
        "gloss": "plant, cultivate",
        "pos": "v.tr",
        "langs": {"Nume":"qōl","Dorig":"qōl","Koro":"qōl","Olrat":"qōl","Lakon":"qōl"},
        "notes": "Transitive verb used with garden produce and agricultural activities.",
    },
    "u": {
        "gloss": "you — 2nd person singular",
        "pos": "pro",
        "langs": {"Nume":"u","Dorig":"u","Koro":"u","Olrat":"u","Lakon":"u"},
        "notes": "2sg subject proclitic (u=) prefixed to the verb.",
    },
}

GRAMMAR_SECTIONS = [
    {
        "title": "1. Phonology",
        "body": [
            ("p", (
                "The five languages of Gaua share a common phonological inventory inherited from Proto-Oceanic, "
                "though each has developed distinct local innovations. All five languages possess a series of prenasalized "
                "stops (mb, nd, ngg), contrasting with plain stops (p, t, k). Vowel length is phonemically distinctive in "
                "all languages, as illustrated by minimal pairs such as Koro <i>gōr</i> 'man' vs <i>gor</i> 'to call'. "
                "The languages also exhibit a uvular stop /q/ and a mid-back rounded vowel /ō/ — both rare in the wider "
                "Oceanic family yet consistent across the entire Gaua dialect chain."
            )),
            ("p", (
                "A notable areal feature is the retention of Proto-Oceanic *R as a uvular trill in Koro and Lakon, "
                "which has merged with /r/ in Nume, Dorig, and Olrat. Stress is generally penultimate but shifts to the "
                "final syllable in verb stems followed by the completive aspect marker <i>qēt</i>."
            )),
            ("ex", {
                "n": "1", "language": "Koro",
                "morphemes": ["gōr", "are", "o=wer"],
                "glosses":   ["man", "DEM", "3SG=big"],
                "dict_keys": ["gōr", "are", "wer"],
                "translation": "That man is big.",
                "source": "Koro corpus, KOR_001",
            }),
        ],
    },
    {
        "title": "2. Personal Pronouns",
        "body": [
            ("p", (
                "The Gaua languages have a rich pronominal system with distinctions of person (1st, 2nd, 3rd), "
                "number (singular, dual, paucal, plural), and clusivity (inclusive vs exclusive in non-singular "
                "1st person). Subject pronouns function as proclitics attaching to the left edge of the verb, "
                "separated by the phonological boundary marker =."
            )),
            ("p", (
                "Remarkably, the singular forms are near-identical across all five languages, attesting to the "
                "conservative nature of this paradigm within the Gaua dialect chain. Divergence emerges in the dual "
                "and plural, where Lakon shows the most pronounced differences from the eastern varieties."
            )),
            ("table", {
                "caption": "Table 1 — Singular subject proclitics across the five Gaua languages",
                "headers": ["Person", "Gloss", "Nume", "Dorig", "Koro", "Olrat", "Lakon"],
                "rows": [
                    ["1sg", "I",         "no=", "no=", "no=", "no=", "no="],
                    ["2sg", "you",       "u=",  "u=",  "u=",  "u=",  "u="],
                    ["3sg", "s/he/it",   "o=",  "o=",  "o=",  "o=",  "o="],
                ],
            }),
            ("ex", {
                "n": "2", "language": "Koro",
                "morphemes": ["no=kan", "are", "mōtō"],
                "glosses":   ["1SG=eat", "DEM", "taro"],
                "dict_keys": ["no", "are", "mōtō"],
                "translation": "I am eating this taro.",
                "source": "Koro corpus, KOR_012",
            }),
            ("ex", {
                "n": "3", "language": "Lakon",
                "morphemes": ["o=lō", "ēgēl"],
                "glosses":   ["3SG=go", "village"],
                "dict_keys": ["o", "ēgēl"],
                "translation": "She/He went to the village.",
                "source": "Lakon corpus, LAK_004",
            }),
        ],
    },
    {
        "title": "3. Verb Morphology",
        "body": [
            ("p", (
                "Verbs in the Gaua languages are morphologically conservative: they do not inflect for tense, "
                "aspect, or mood through affixation. Instead, temporal and aspectual meaning is expressed through "
                "post-verbal particles. The completive aspect is marked by <i>qēt</i>, found in identical form "
                "across all five languages, which follows the verb and signals that an action has been completed. "
                "This remarkable isogloss confirms the coherence of the Gaua dialect chain."
            )),
            ("p", (
                "Verbs are broadly divided into transitive and intransitive based on whether they require a direct "
                "object. Serial verb constructions are common for expressing complex events involving motion and "
                "action. The realis/irrealis distinction is expressed through the choice of subject proclitic form."
            )),
            ("ex", {
                "n": "4", "language": "Nume",
                "morphemes": ["no=kan", "qēt"],
                "glosses":   ["1SG=eat", "COMPL"],
                "dict_keys": ["kan", "qēt"],
                "translation": "I have already eaten.",
                "source": "Nume corpus, NUM_008",
            }),
            ("ex", {
                "n": "5", "language": "Dorig",
                "morphemes": ["o=lō", "qēt"],
                "glosses":   ["3SG=go", "COMPL"],
                "dict_keys": ["lō", "qēt"],
                "translation": "She/He has already gone.",
                "source": "Dorig corpus, DOR_003",
            }),
        ],
    },
    {
        "title": "4. Possessive Constructions",
        "body": [
            ("p", (
                "Possession in the Gaua languages is encoded through a system of possessive classifiers — a "
                "well-known feature of Oceanic languages. Nouns are classified semantically according to the type "
                "of relationship they hold with their possessor. Two main classes are distinguished: "
                "<i>direct possession</i> (for inalienable nouns such as body parts and kinship terms) and "
                "<i>indirect possession</i> (mediated by a possessive classifier)."
            )),
            ("p", (
                "The three main classifier classes found across the five languages are: (i) the consumable "
                "classifier <i>no-</i> (for food and drink consumed by the possessor); (ii) the locative "
                "classifier <i>me-</i> (for items associated with the possessor's location or dwelling); and "
                "(iii) the neutral classifier <i>ne-</i> (for all other alienable objects). This tripartite "
                "distinction is preserved intact across all five languages, constituting one of the strongest "
                "shared structural features of the Gaua dialect chain."
            )),
            ("ex", {
                "n": "6", "language": "Koro",
                "morphemes": ["no=wia", "gōr", "are"],
                "glosses":   ["1SG=see", "man", "DEM"],
                "dict_keys": ["wia", "gōr", "are"],
                "translation": "I see that man.",
                "source": "Koro corpus, KOR_007",
            }),
        ],
    },
    {
        "title": "5. Negation",
        "body": [
            ("p", (
                "Verbal negation in the Gaua languages follows a consistent pattern. The primary negation "
                "strategy uses a pre-verbal negative particle <i>tō</i> which precedes the subject–verb complex. "
                "In some registers and languages, a post-verbal negation suffix <i>-(V)t</i> co-occurs with "
                "<i>tō</i>, creating a discontinuous negation pattern parallel to the Jespersen cycle. "
                "This structure is remarkably uniform across the dialect chain, suggesting shared historical origin."
            )),
            ("p", (
                "In casual speech, the post-verbal element is frequently dropped, especially in Lakon and Olrat, "
                "leaving <i>tō</i> as the sole negator. The particle <i>tō</i> also functions as a prohibitive "
                "in second-person commands (<i>tō u=kan</i> 'Don't eat!')."
            )),
            ("ex", {
                "n": "7", "language": "Koro",
                "morphemes": ["no", "tō", "no=kan", "qēt"],
                "glosses":   ["1SG", "NEG", "1SG=eat", "COMPL"],
                "dict_keys": ["no", "tō", "kan", "qēt"],
                "translation": "I have not eaten yet.",
                "source": "Koro corpus, KOR_015",
            }),
        ],
    },
]

# ── Navigation ─────────────────────────────────────────────────────────────
def nav(page, word=""):
    st.session_state["page"] = page
    st.session_state["dict_word"] = word
    st.rerun()

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ◬ DBT Gaua")
    st.caption("Digital Boasian Trilogy")
    st.divider()
    cur = st.session_state["page"]
    for icon, label, pid in [
        ("🏠", "Home", "home"),
        ("📐", "Comparative Grammar", "grammar"),
        ("📚", "Archived Texts", "texts"),
        ("📖", "Dictionary", "dictionary"),
    ]:
        t = "primary" if cur == pid else "secondary"
        if st.button(f"{icon}  {label}", use_container_width=True, type=t, key=f"nav_{pid}"):
            nav(pid)
    st.divider()
    st.markdown("**Languages (East → West)**")
    for lang in ["Nume", "Dorig", "Koro", "Olrat", "Lakon"]:
        c = LANG_COLORS[lang]
        st.markdown(
            f'<span style="color:{c};font-size:1rem;">●</span> '
            f'<span style="color:#e0cdb5;font-family:Georgia,serif;">{lang}</span>',
            unsafe_allow_html=True,
        )
    st.divider()
    st.caption(
        "LACITO / Pangloss Collection · CNRS  \n"
        "Documentation: Alexandre François  \n"
        "Gaua Island, Banks Islands, Vanuatu"
    )

# ── Helpers ─────────────────────────────────────────────────────────────────
def gloss_html(data):
    lang      = data["language"]
    color     = LANG_COLORS.get(lang, "#888")
    morphemes = data["morphemes"]
    glosses   = data["glosses"]
    dkeys     = data.get("dict_keys", morphemes)
    n         = data.get("n", "")

    mtds = "".join(
        f'<td class="morph-cell"><a href="?page=dictionary&word={dk}">{m}</a></td>'
        for m, dk in zip(morphemes, dkeys)
    )
    gtds = "".join(f'<td class="gloss-cell">{g}</td>' for g in glosses)
    src  = (f'<div class="gloss-source">Source: {data["source"]}</div>'
            if "source" in data else "")

    return f"""
<div class="ex-wrap">
  <div class="ex-num">({n})</div>
  <div class="gloss-box">
    <span class="lang-chip" style="background:{color};">{lang}</span><br>
    <table class="gloss-table">
      <tr>{mtds}</tr>
      <tr>{gtds}</tr>
    </table>
    <div class="gloss-transl">'{data["translation"]}'</div>
    {src}
  </div>
</div>"""


def table_html(data):
    cap  = (f'<caption>{data["caption"]}</caption>' if data.get("caption") else "")
    ths  = "".join(f"<th>{h}</th>" for h in data["headers"])
    rows = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>"
        for row in data["rows"]
    )
    return f'<table class="ling-table">{cap}<thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table>'


# ── Page: Home ──────────────────────────────────────────────────────────────
def show_home():
    st.markdown('<div class="main-title">Digital Boasian Trilogy</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Gaua Languages &nbsp;·&nbsp; Banks Islands, Vanuatu &nbsp;·&nbsp; Oceanic · Austronesian</div>',
        unsafe_allow_html=True,
    )

    # ── Triangle ────────────────────────────────────────────────────────────
    triangle = """
<div style="display:flex;justify-content:center;margin:1.5rem 0 2.5rem 0;">
<svg viewBox="0 0 580 470" width="520" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#c9b99a"/>
    </marker>
  </defs>

  <!-- Edges -->
  <line x1="290" y1="100" x2="105" y2="395" stroke="#c9b99a" stroke-width="2"
        marker-end="url(#ah)" marker-start="url(#ah)"/>
  <line x1="290" y1="100" x2="475" y2="395" stroke="#c9b99a" stroke-width="2"
        marker-end="url(#ah)" marker-start="url(#ah)"/>
  <line x1="120"  y1="405" x2="460" y2="405" stroke="#c9b99a" stroke-width="2"
        marker-end="url(#ah)" marker-start="url(#ah)"/>

  <!-- Edge labels -->
  <text font-family="Georgia,serif" font-style="italic" font-size="11.5" fill="#a08060">
    <textPath href="#el1" startOffset="50%" text-anchor="middle">morphosyntactic properties</textPath>
  </text>
  <defs>
    <path id="el1" d="M 105,395 L 290,100"/>
    <path id="el2" d="M 290,100 L 475,395"/>
    <path id="el3" d="M 460,405 L 120,405"/>
  </defs>
  <text font-family="Georgia,serif" font-style="italic" font-size="11.5" fill="#a08060">
    <textPath href="#el2" startOffset="50%" text-anchor="middle">textual evidence</textPath>
  </text>
  <text font-family="Georgia,serif" font-style="italic" font-size="11.5" fill="#a08060">
    <textPath href="#el3" startOffset="50%" text-anchor="middle">lexical apparatus</textPath>
  </text>

  <!-- Grammar node (top) -->
  <a href="?page=grammar" style="cursor:pointer;">
    <circle cx="290" cy="85" r="65" fill="#1c0f06"/>
    <circle cx="290" cy="85" r="65" fill="none" stroke="#a07850" stroke-width="1.5"/>
    <text x="290" y="78" text-anchor="middle" font-family="Georgia,serif" font-size="18"
          font-weight="bold" fill="#f2e5cc">Grammar</text>
    <text x="290" y="97" text-anchor="middle" font-family="Georgia,serif" font-size="11"
          fill="#c9a870" font-style="italic">comparative</text>
  </a>

  <!-- Dictionary node (bottom-left) -->
  <a href="?page=dictionary" style="cursor:pointer;">
    <circle cx="95" cy="405" r="65" fill="#2a0a3a"/>
    <circle cx="95" cy="405" r="65" fill="none" stroke="#a07850" stroke-width="1.5"/>
    <text x="95" y="398" text-anchor="middle" font-family="Georgia,serif" font-size="18"
          font-weight="bold" fill="#f2e5cc">Dictionary</text>
    <text x="95" y="417" text-anchor="middle" font-family="Georgia,serif" font-size="11"
          fill="#c9a870" font-style="italic">lexicon</text>
  </a>

  <!-- Texts node (bottom-right) -->
  <a href="?page=texts" style="cursor:pointer;">
    <circle cx="485" cy="405" r="65" fill="#4a0a0a"/>
    <circle cx="485" cy="405" r="65" fill="none" stroke="#a07850" stroke-width="1.5"/>
    <text x="485" y="398" text-anchor="middle" font-family="Georgia,serif" font-size="18"
          font-weight="bold" fill="#f2e5cc">Texts</text>
    <text x="485" y="417" text-anchor="middle" font-family="Georgia,serif" font-size="11"
          fill="#c9a870" font-style="italic">Pangloss archive</text>
  </a>

  <!-- Centre label -->
  <text x="290" y="248" text-anchor="middle" font-family="Georgia,serif"
        font-size="12" fill="#c9a870" font-style="italic" opacity="0.75">Digital Boasian Trilogy</text>
</svg>
</div>"""
    st.markdown(triangle, unsafe_allow_html=True)

    # ── Intro ────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="dbt-intro">
Named after the American anthropologist Franz Boas, the <em>Boasian Trilogy</em> holds that a comprehensive
language documentation should comprise three main components: a <strong>grammar</strong>, a
<strong>dictionary</strong>, and a <strong>corpus of texts</strong>. Rather than producing three separate
outputs, the Digital Boasian Trilogy reconceives this schema as an interactive, persistently interconnected
resource — one in which every grammatical claim is traceable to its textual evidence, every lexical item is
linked to its morphosyntactic properties, and every archived text is navigable through the grammatical and
lexical apparatus that describes it.
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Component cards ───────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        st.markdown("""
<div class="component-card" style="border-top:4px solid #1c0f06;">
  <h3>📐 Comparative Grammar</h3>
  <p>A systematic comparative description of grammatical structures across all five Gaua languages.
  Every claim is illustrated with interlinear glossed examples — click any morpheme to look it up
  in the dictionary.</p>
</div>""", unsafe_allow_html=True)
        st.write("")
        if st.button("Open Grammar →", key="hbtn_g"):
            nav("grammar")

    with col2:
        st.markdown("""
<div class="component-card" style="border-top:4px solid #4a0a0a;">
  <h3>📚 Archived Texts</h3>
  <p>A curated index of natural language texts recorded across all five languages — myths, procedural
  texts, personal narratives, and ritual speech. Each title links to its archived item in the
  LACITO/Pangloss Collection.</p>
</div>""", unsafe_allow_html=True)
        st.write("")
        if st.button("Open Texts →", key="hbtn_t"):
            nav("texts")

    with col3:
        st.markdown("""
<div class="component-card" style="border-top:4px solid #2a0a3a;">
  <h3>📖 Dictionary</h3>
  <p>A comparative lexicon giving each form across all five languages, with grammatical category,
  semantic gloss, and usage notes. Entries are linked bidirectionally from the glossed grammatical
  examples.</p>
</div>""", unsafe_allow_html=True)
        st.write("")
        if st.button("Open Dictionary →", key="hbtn_d"):
            nav("dictionary")

    st.divider()

    # ── Language strip ────────────────────────────────────────────────────────
    st.markdown(
        '<span style="font-family:\'Fira Sans\',sans-serif;font-size:0.78rem;'
        'letter-spacing:0.1em;text-transform:uppercase;color:#8a6f52;">'
        'The Five Languages (East → West)</span>',
        unsafe_allow_html=True,
    )
    lang_cols = st.columns(5, gap="small")
    descs = {
        "Nume":  "eastern",
        "Dorig": "east-central",
        "Koro":  "central",
        "Olrat": "west-central",
        "Lakon": "western",
    }
    for i, lang in enumerate(["Nume", "Dorig", "Koro", "Olrat", "Lakon"]):
        with lang_cols[i]:
            c = LANG_COLORS[lang]
            st.markdown(f"""
<div style="background:{c};border-radius:8px;padding:0.9rem 0.5rem;
            text-align:center;color:white;">
  <div style="font-family:'EB Garamond',serif;font-size:1.25rem;font-weight:500;">
    {lang}</div>
  <div style="font-family:'Fira Sans',sans-serif;font-size:0.65rem;
              opacity:0.85;margin-top:3px;letter-spacing:0.05em;">
    {descs[lang]}</div>
</div>""", unsafe_allow_html=True)


# ── Page: Grammar ───────────────────────────────────────────────────────────
def show_grammar():
    st.markdown('<div class="main-title">Comparative Grammar</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Gaua Languages · Oceanic, Austronesian · Gaua Island, Banks Islands, Vanuatu</div>',
        unsafe_allow_html=True,
    )
    st.markdown("""
<div class="body-text">
This grammar provides a comparative description of the five languages of Gaua Island: Nume, Dorig, Koro,
Olrat, and Lakon, ordered from east to west. All five are closely related Oceanic languages of the
Austronesian family. The description follows established typological categories, and every grammatical claim
is illustrated by interlinear glossed text examples. <strong>Click any morpheme in a glossed example to
look it up in the Dictionary.</strong>
</div>
""", unsafe_allow_html=True)

    # TOC
    with st.expander("📋 Table of Contents", expanded=False):
        for sec in GRAMMAR_SECTIONS:
            st.markdown(f"- {sec['title']}")

    for sec in GRAMMAR_SECTIONS:
        st.markdown(f'<div class="section-header">{sec["title"]}</div>', unsafe_allow_html=True)
        for kind, data in sec["body"]:
            if kind == "p":
                st.markdown(f'<div class="body-text">{data}</div>', unsafe_allow_html=True)
            elif kind == "ex":
                st.markdown(gloss_html(data), unsafe_allow_html=True)
            elif kind == "table":
                st.markdown(table_html(data), unsafe_allow_html=True)


# ── Page: Texts ─────────────────────────────────────────────────────────────
def show_texts():
    st.markdown('<div class="main-title">Archived Texts</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">LACITO / Pangloss Collection · CNRS · pangloss.cnrs.fr</div>',
        unsafe_allow_html=True,
    )
    st.markdown("""
<div class="body-text">
The texts listed below have been recorded, transcribed, and archived as part of the documentation of the
five Gaua languages. Each title links directly to its archived item in the LACITO Pangloss Collection,
where recordings, transcriptions, and translations are freely accessible. Documentation was carried out by
Alexandre François (LACITO, CNRS / Australian National University).
</div>
""", unsafe_allow_html=True)

    selected = st.multiselect(
        "Filter by language",
        options=["Nume", "Dorig", "Koro", "Olrat", "Lakon"],
        default=["Nume", "Dorig", "Koro", "Olrat", "Lakon"],
    )

    all_genres = sorted({t["genre"] for texts in TEXTS_DATA.values() for t in texts})
    selected_genres = st.multiselect("Filter by genre", options=all_genres, default=all_genres)

    st.divider()

    total = sum(
        len([t for t in TEXTS_DATA[l] if t["genre"] in selected_genres])
        for l in selected
    )
    st.caption(f"Showing {total} text(s) across {len(selected)} language(s)")

    for lang in ["Nume", "Dorig", "Koro", "Olrat", "Lakon"]:
        if lang not in selected:
            continue
        filtered = [t for t in TEXTS_DATA[lang] if t["genre"] in selected_genres]
        if not filtered:
            continue
        c = LANG_COLORS[lang]
        st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin:1.8rem 0 0.6rem 0;">
  <div style="width:14px;height:14px;border-radius:50%;background:{c};flex-shrink:0;"></div>
  <span style="font-family:'EB Garamond',serif;font-size:1.45rem;font-weight:500;color:#1c0f06;">{lang}</span>
  <span style="font-family:'Fira Sans',sans-serif;font-size:0.72rem;color:#9a856a;">
    ({len(filtered)} text{"s" if len(filtered)!=1 else ""})</span>
</div>""", unsafe_allow_html=True)

        for text in filtered:
            st.markdown(f"""
<div class="text-card">
  <div class="text-title">
    <a href="{text['url']}" target="_blank">📄 {text['title']}</a>
  </div>
  <div class="text-meta">
    <span class="genre-badge">{text['genre']}</span>
    <span>Recorded by {text['recorder']}</span>
    <span>·</span>
    <span>{text['year']}</span>
    <span>·</span>
    <a href="{text['url']}" target="_blank"
       style="color:#a07850;font-family:'Fira Sans',sans-serif;font-size:0.72rem;">
      Open in Pangloss ↗</a>
  </div>
</div>""", unsafe_allow_html=True)


# ── Page: Dictionary ────────────────────────────────────────────────────────
def show_dictionary():
    target = st.session_state.get("dict_word", "")

    st.markdown('<div class="main-title">Dictionary</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Comparative Lexicon · Five Gaua Languages</div>',
        unsafe_allow_html=True,
    )

    col_s, col_f = st.columns([3, 1])
    with col_s:
        query = st.text_input(
            "🔍 Search",
            value=target,
            placeholder="Search by form or meaning…",
            label_visibility="collapsed",
        )
    with col_f:
        pos_filter = st.selectbox(
            "Part of speech",
            ["All"] + sorted({v["pos"] for v in DICTIONARY.values()}),
            label_visibility="collapsed",
        )

    st.markdown(f"""
<div class="body-text">
Each entry shows the form across all five languages, grammatical category, semantic gloss, and usage notes.
Entries are linked from interlinear examples in the
<a href="?page=grammar" style="color:#a07850;border-bottom:1px solid #c9a870;">Comparative Grammar</a>.
<em>Currently showing {len(DICTIONARY)} entries.</em>
</div>""", unsafe_allow_html=True)

    st.divider()

    entries = {
        k: v for k, v in DICTIONARY.items()
        if (not query or query.lower() in k.lower() or query.lower() in v["gloss"].lower())
        and (pos_filter == "All" or v["pos"] == pos_filter)
    }

    if not entries:
        st.info(f"No entries found for '{query}'.")
        return

    for hw, entry in sorted(entries.items()):
        hl = "highlighted" if hw == target else ""
        langs_html = "".join(
            f'<span class="dict-lang-chip"><b>{ln}:</b> {form}</span>'
            for ln, form in entry["langs"].items()
        )
        st.markdown(f"""
<div id="dict-{hw}" class="dict-entry {hl}">
  <span class="dict-headword">{hw}</span>
  <span class="dict-pos">{entry['pos']}</span>
  <div class="dict-gloss">{entry['gloss']}</div>
  <div class="dict-langs">{langs_html}</div>
  <div class="dict-notes">{entry['notes']}</div>
</div>""", unsafe_allow_html=True)

    # Scroll to highlighted entry via JS (best-effort)
    if target and target in entries:
        st.markdown(f"""
<script>
  window.addEventListener('load', function() {{
    var el = document.getElementById('dict-{target}');
    if(el) el.scrollIntoView({{behavior:'smooth', block:'center'}});
  }});
</script>""", unsafe_allow_html=True)


# ── Router ──────────────────────────────────────────────────────────────────
dispatch = {
    "home":       show_home,
    "grammar":    show_grammar,
    "texts":      show_texts,
    "dictionary": show_dictionary,
}
dispatch.get(st.session_state["page"], show_home)()
