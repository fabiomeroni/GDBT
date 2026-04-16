// ============================================================
//  Digital Boasian Trilogy — Gaua Languages  ·  data.js
// ============================================================

const LANG_COLORS = {
  Nume:  "#2e5c8a",
  Dorig: "#c07820",
  Koro:  "#922810",
  Olrat: "#267040",
  Lakon: "#5c2878",
};

const LANG_ABBR = {
  Nume:  "Num",
  Dorig: "Drg",
  Koro:  "Kro",
  Olrat: "Olr",
  Lakon: "Lkn",
};

// ── Dictionary ────────────────────────────────────────────────
// Exactly 8 entries — one per morpheme column in the negation example.
// langs{} gives the surface form in each language.
// gloss = plain text for tooltip; glossRich = HTML for entry page.
const DICTIONARY = [
  {
    id: "3pl",
    hw: "nɪr",          // Koro form as headword
    pos: "pro.",
    domain: "Grammar",
    gloss: "3PL — third person plural subject",
    glossRich: "3PL — third person plural subject",
    notes: "Free subject pronoun referring to a plural group not including the speaker. The form varies considerably across the dialect chain, with Lakon showing the most divergent reflex.",
    langs: { Nume:"nir", Dorig:"nɪr", Koro:"nɪr", Olrat:"nɪj", Lakon:"ɣɪː" },
  },
  {
    id: "nondum1",
    hw: "tɪ",           // Koro/Olrat shared form
    pos: "part.",
    domain: "Grammar",
    gloss: "NONDUM₁ — pre-verbal negator ('not yet')",
    glossRich: "NONDUM₁ — pre-verbal negator <em>('not yet')</em>",
    notes: "The pre-verbal component of the discontinuous negation construction. Occupies the position immediately before the subject–verb complex. Forms diverge across the chain: Dorig retains an older bisyllabic shape, while central and western varieties show reduction.",
    langs: { Nume:"βitis", Dorig:"sɔwsɛ", Koro:"tɪ", Olrat:"tɪ", Lakon:"atɪ" },
  },
  {
    id: "know",
    hw: "rɔŋ",          // shared Koro/Olrat/Lakon form
    pos: "v.tr.",
    domain: "Cognition",
    gloss: "know, be familiar with",
    glossRich: "know, be familiar with",
    notes: "Transitive verb of knowledge. The eastern languages (Nume, Dorig) retain fuller forms with more syllables, while central and western varieties show convergence on a monosyllabic root.",
    langs: { Nume:"ɣil", Dorig:"βrɪɣɪl", Koro:"rɔŋ", Olrat:"rɔŋ", Lakon:"rɔŋ" },
  },
  {
    id: "properly",
    hw: "taβul",        // Dorig/Koro form
    pos: "adv.",
    domain: "Manner",
    gloss: "properly, well, thoroughly",
    glossRich: "properly, well, thoroughly",
    notes: "Manner adverb expressing the thoroughness or quality of an action. Placed after the verb and before the post-verbal negator. Exhibits significant cross-linguistic variation across the five varieties.",
    langs: { Nume:"liŋliŋi", Dorig:"taβul", Koro:"taβul", Olrat:"βɪlɪː", Lakon:"kɛrɛ" },
  },
  {
    id: "nondum2",
    hw: "wʊsmɛlɛ",      // Koro/Olrat form
    pos: "part.",
    domain: "Grammar",
    gloss: "NONDUM₂ — post-verbal negator (bound, discontinuous)",
    glossRich: "NONDUM₂ — post-verbal negator <em>(bound, discontinuous)</em>",
    notes: "The post-verbal component of the discontinuous negation construction. May be suffixed to the final verb or to a post-verbal particle. Can be omitted in casual registers. Together with NONDUM₁ it forms a split-negation pattern typologically parallel to the Jespersen cycle.",
    langs: { Nume:"mi", Dorig:"tɛ", Koro:"wʊsmɛlɛ", Olrat:"wʊsmɛlɛ", Lakon:"aβʊh.malɛ" },
  },
  {
    id: "art",
    hw: "ɔ",            // Koro form
    pos: "det.",
    domain: "Grammar",
    gloss: "ART — article (nominal determiner)",
    glossRich: "ART — article (nominal determiner)",
    notes: "Nominal article preceding the head noun. Absent in Olrat and Lakon in this construction, either due to grammatical differences or ellipsis in context.",
    langs: { Nume:"u", Dorig:"na", Koro:"ɔ", Olrat:"—", Lakon:"—" },
  },
  {
    id: "speech",
    hw: "βalβalaw",     // Koro form
    pos: "n.",
    domain: "Language",
    gloss: "speech, language, word",
    glossRich: "speech, language, word",
    notes: "Noun denoting spoken language or speech in general. All five languages show distinct forms, reflecting the high rate of lexical differentiation across the Gaua dialect chain.",
    langs: { Nume:"luwluw", Dorig:"lŋa", Koro:"βalβalaw", Olrat:"ususraː", Lakon:"ɛlŋa" },
    etym: {
      label: "POc *[qa]liŋa- 'voice'",
      tlopo:  "https://tlopo.clld.org/parameters/5-3-4-14-138-POc-qalia-a#6/-5.859/152.761",
      etymograph: "https://evosem.huma-num.fr/etymograph.html?etym=Oceanic/qali%C5%8Ba-&node1=voice",
    },
  },
  {
    id: "poss",
    hw: "namɪɣɪn",      // Koro form
    pos: "poss.",
    domain: "Grammar",
    gloss: "POSS:1INCL.PL — 1st person inclusive plural possessive",
    glossRich: "POSS:1INCL.PL — 1st person inclusive plural possessive",
    notes: "Possessive marker encoding the 1st person inclusive plural possessor (speaker + addressee + others). Appears as a suffix or clitic on the possessed noun. The inclusive/exclusive distinction in possessives is a well-preserved Oceanic feature across all five languages.",
    langs: { Nume:"namɣin", Dorig:"‑ɣɪn", Koro:"namɪɣɪn", Olrat:"mʊʧ", Lakon:"‑nɣɪʧ" },
  },
];

// ── Texts ─────────────────────────────────────────────────────
const TEXTS = [
  { lang:"Nume",  title:"The origin of fire",           url:"https://pangloss.cnrs.fr/corpus/Nume?lang=en",  genre:"Myth",                year:"2000", rec:"A. François" },
  { lang:"Nume",  title:"How the sea became salt",       url:"https://pangloss.cnrs.fr/corpus/Nume?lang=en",  genre:"Myth",                year:"2001", rec:"A. François" },
  { lang:"Nume",  title:"Fishing with nets",             url:"https://pangloss.cnrs.fr/corpus/Nume?lang=en",  genre:"Procedural",          year:"2000", rec:"A. François" },
  { lang:"Nume",  title:"The orphan and the chief",      url:"https://pangloss.cnrs.fr/corpus/Nume?lang=en",  genre:"Narrative",           year:"2002", rec:"A. François" },
  { lang:"Dorig", title:"Qat and his brothers",          url:"https://pangloss.cnrs.fr/corpus/Dorig?lang=en", genre:"Myth",                year:"2001", rec:"A. François" },
  { lang:"Dorig", title:"Building a canoe",              url:"https://pangloss.cnrs.fr/corpus/Dorig?lang=en", genre:"Procedural",          year:"2002", rec:"A. François" },
  { lang:"Dorig", title:"The flying fox and the rat",    url:"https://pangloss.cnrs.fr/corpus/Dorig?lang=en", genre:"Fable",               year:"2001", rec:"A. François" },
  { lang:"Dorig", title:"A feast in the village",        url:"https://pangloss.cnrs.fr/corpus/Dorig?lang=en", genre:"Personal narrative",  year:"2003", rec:"A. François" },
  { lang:"Koro",  title:"The origin of the coconut",     url:"https://pangloss.cnrs.fr/corpus/Koro?lang=en",  genre:"Myth",                year:"2003", rec:"A. François" },
  { lang:"Koro",  title:"A journey to Santo",            url:"https://pangloss.cnrs.fr/corpus/Koro?lang=en",  genre:"Personal narrative",  year:"2004", rec:"A. François" },
  { lang:"Koro",  title:"Kava ceremonies",               url:"https://pangloss.cnrs.fr/corpus/Koro?lang=en",  genre:"Procedural",          year:"2003", rec:"A. François" },
  { lang:"Koro",  title:"The jealous brother",           url:"https://pangloss.cnrs.fr/corpus/Koro?lang=en",  genre:"Narrative",           year:"2005", rec:"A. François" },
  { lang:"Koro",  title:"Preparing a garden",            url:"https://pangloss.cnrs.fr/corpus/Koro?lang=en",  genre:"Procedural",          year:"2004", rec:"A. François" },
  { lang:"Olrat", title:"The woman who became stone",    url:"https://pangloss.cnrs.fr/corpus/Olrat?lang=en", genre:"Myth",                year:"2004", rec:"A. François" },
  { lang:"Olrat", title:"Garden magic spells",           url:"https://pangloss.cnrs.fr/corpus/Olrat?lang=en", genre:"Ritual speech",       year:"2004", rec:"A. François" },
  { lang:"Olrat", title:"Childhood memories",            url:"https://pangloss.cnrs.fr/corpus/Olrat?lang=en", genre:"Personal narrative",  year:"2005", rec:"A. François" },
  { lang:"Lakon", title:"Origin of the Lakon dances",   url:"https://pangloss.cnrs.fr/corpus/Lakon?lang=en", genre:"Myth",                year:"2006", rec:"A. François" },
  { lang:"Lakon", title:"A day of fishing",              url:"https://pangloss.cnrs.fr/corpus/Lakon?lang=en", genre:"Personal narrative",  year:"2007", rec:"A. François" },
  { lang:"Lakon", title:"The seven brothers",            url:"https://pangloss.cnrs.fr/corpus/Lakon?lang=en", genre:"Traditional narrative",year:"2006",rec:"A. François" },
  { lang:"Lakon", title:"Healing plants of Gaua",        url:"https://pangloss.cnrs.fr/corpus/Lakon?lang=en", genre:"Ethnobotanical",      year:"2007", rec:"A. François" },
];

// ── Slug helper ───────────────────────────────────────────────
function textSlug(lang, title) {
  return ('text-' + lang + '-' + title)
    .toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}

// ── Negation example ─────────────────────────────────────────
// dictId on each column links each form to its dictionary entry.
// Rows list every language with its surface forms.
const NEGATION_EXAMPLE = {
  textLang: "Koro",
  textTitle: "Preparing a garden",
  cols: [
    { gl:"3PL",          dictId:"3pl"      },
    { gl:"NONDUM₁",      dictId:"nondum1"  },
    { gl:"know",         dictId:"know"     },
    { gl:"properly",     dictId:"properly" },
    { gl:"NONDUM₂",      dictId:"nondum2"  },
    { gl:"ART",          dictId:"art"      },
    { gl:"speech",       dictId:"speech"   },
    { gl:"POSS:1INCL.PL",dictId:"poss"    },
  ],
  rows: [
    { lang:"Nume",  abbr:"Num", forms:["nir",  "βitis",  "ɣil",    "liŋliŋi","mi",        "u",  "luwluw",   "namɣin"]  },
    { lang:"Dorig", abbr:"Drg", forms:["nɪr",  "sɔwsɛ",  "βrɪɣɪl", "taβul",  "tɛ",        "na", "lŋa",      "‑ɣɪn"]   },
    { lang:"Koro",  abbr:"Kro", forms:["nɪr",  "tɪ",     "rɔŋ",    "taβul",  "wʊsmɛlɛ",   "ɔ",  "βalβalaw", "namɪɣɪn"] },
    { lang:"Olrat", abbr:"Olr", forms:["nɪj",  "tɪ",     "rɔŋ",    "βɪlɪː",  "wʊsmɛlɛ",   "",   "ususraː",  "mʊʧ"]    },
    { lang:"Lakon", abbr:"Lkn", forms:["ɣɪː",  "atɪ",    "rɔŋ",    "kɛrɛ",   "aβʊh.malɛ", "",   "ɛlŋa",     "‑nɣɪʧ"]  },
  ],
  translation: "'They don't know our language very well yet.'",
};

// ── Grammar sections (one only) ───────────────────────────────
const GRAMMAR = [
  {
    id: "s1", num: "1", title: "Negation",
    subsections: [],
    body: `<p>Verbal negation across the five Gaua languages can involve a split construction in which a
pre-verbal negator and a post-verbal bound morpheme together express sentential negation, in a
discontinuous pattern. </p>
<p>An example of this is nondumitive ("not yet" negation"). The pre-verbal negator (glossed <strong>NONDUM₁</strong>) 
occupies the position immediately before the verb complex. The post-verbal element (<strong>NONDUM₂</strong>) is suffixed to the final verb or
a post-verbal particle and can be omitted in casual registers, particularly in Lakon and Olrat.
Together the two components convey the meaning <em>'not yet'</em>.</p>
<negation-example></negation-example>`
  },
];
