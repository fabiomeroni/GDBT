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
  { lang:"Lakon", title:"The seven brothers",            url:"https://pangloss.cnrs.fr/corpus/Lakon?lang=en", genre:"Traditional narrative",year:"2006", rec:"A. François" },
  { lang:"Lakon", title:"Healing plants of Gaua",        url:"https://pangloss.cnrs.fr/corpus/Lakon?lang=en", genre:"Ethnobotanical",      year:"2007", rec:"A. François" },
];

// ── Slug helper ───────────────────────────────────────────────
function textSlug(lang, title) {
  return ('text-' + lang + '-' + title)
    .toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}

// ── Negation example ──────────────────────────────────────────
// Used by dictionary.html for the example block in each entry.
// dictId on each column links each form to its dictionary entry.
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
