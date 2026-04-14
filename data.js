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

// Abbreviations shown in the left-hand column of every example
const LANG_ABBR = {
  Nume:  "Num",
  Dorig: "Drg",
  Koro:  "Kro",
  Olrat: "Olr",
  Lakon: "Lkn",
};

// ── Dictionary ────────────────────────────────────────────────
// gloss      = plain text (used in tooltip)
// glossRich  = HTML (used in dict entry)
const DICTIONARY = [
  {
    id:"are", hw:"are", pos:"det.", domain:"Grammar",
    gloss:"proximal demonstrative — this, these",
    glossRich:"proximal demonstrative — <em>this, these</em>",
    notes:"Post-nominal, invariant across all five languages. Contrasts with distal <em>ēnē</em>.",
    langs:{ Nume:"are", Dorig:"are", Koro:"are", Olrat:"are", Lakon:"are" },
    // Comparative examples: cols = morpheme columns; rows = one per language
    examples:[
      {
        cols:[{ids:["gor"],gl:"man"},{ids:["are"],gl:"DEM"}],
        rows:[
          {lang:"Nume",  forms:["gōr","are"]},
          {lang:"Dorig", forms:["gōr","are"]},
          {lang:"Koro",  forms:["gōr","are"]},
          {lang:"Olrat", forms:["gōr","are"]},
          {lang:"Lakon", forms:["gōr","are"]},
        ],
        translation:"this man",
      }
    ]
  },
  {
    id:"egel", hw:"ēgēl", pos:"n.", domain:"Society",
    gloss:"village, inhabited settlement",
    glossRich:"village, inhabited settlement",
    notes:"Central concept in social organisation. Locative constructions place a motion verb before this noun with no overt preposition.",
    langs:{ Nume:"ēgēl", Dorig:"ēgēl", Koro:"ēgēl", Olrat:"ēgēl", Lakon:"ēgēl" },
    examples:[
      {
        cols:[{ids:["o","lo"],gl:"3SG=go"},{ids:["egel"],gl:"village"}],
        rows:[
          {lang:"Nume",  forms:["o=lō","ēgēl"]},
          {lang:"Dorig", forms:["o=lō","ēgēl"]},
          {lang:"Koro",  forms:["o=lō","ēgēl"]},
          {lang:"Olrat", forms:["o=lō","ēgēl"]},
          {lang:"Lakon", forms:["o=lō","ēgēl"]},
        ],
        translation:"She went to the village.",
      }
    ]
  },
  {
    id:"gor", hw:"gōr", pos:"n.", domain:"Human",
    gloss:"man; (generic) person, human being",
    glossRich:"man; (generic) person, human being",
    notes:"Refers specifically to an adult male; used generically for 'person' in some contexts. Minimal pair with <em>gor</em> 'to call' (short vowel).",
    langs:{ Nume:"gōr", Dorig:"gōr", Koro:"gōr", Olrat:"gōr", Lakon:"gōr" },
    examples:[
      {
        cols:[{ids:["gor"],gl:"man"},{ids:["are"],gl:"DEM"},{ids:["o","wer"],gl:"3SG=big"}],
        rows:[
          {lang:"Nume",  forms:["gōr","are","o=wer"]},
          {lang:"Dorig", forms:["gōr","are","o=wer"]},
          {lang:"Koro",  forms:["gōr","are","o=wer"]},
          {lang:"Olrat", forms:["gōr","are","o=wer"]},
          {lang:"Lakon", forms:["gōr","are","o=wer"]},
        ],
        translation:"That man is big.",
      }
    ]
  },
  {
    id:"kan", hw:"kan", pos:"v.tr.", domain:"Food",
    gloss:"eat (something)",
    glossRich:"eat (something)",
    notes:"Transitive verb requiring a direct object. Subject agreement expressed through proclitic <em>no=kan</em> '1sg eats'.",
    langs:{ Nume:"kan", Dorig:"kan", Koro:"kan", Olrat:"kan", Lakon:"kan" },
    examples:[
      {
        cols:[{ids:["no","kan"],gl:"1SG=eat"},{ids:["qet"],gl:"COMPL"}],
        rows:[
          {lang:"Nume",  forms:["no=kan","qēt"]},
          {lang:"Dorig", forms:["no=kan","qēt"]},
          {lang:"Koro",  forms:["no=kan","qēt"]},
          {lang:"Olrat", forms:["no=kan","qēt"]},
          {lang:"Lakon", forms:["no=kan","qēt"]},
        ],
        translation:"I have already eaten.",
      }
    ]
  },
  {
    id:"lo", hw:"lō", pos:"v.intr.", domain:"Motion",
    gloss:"go",
    glossRich:"go",
    notes:"Intransitive motion verb. Often followed by a directional verb specifying orientation (e.g. <em>lō tar</em> 'go up', <em>lō van</em> 'go away').",
    langs:{ Nume:"lō", Dorig:"lō", Koro:"lō", Olrat:"lō", Lakon:"lō" },
    examples:[
      {
        cols:[{ids:["o","lo"],gl:"3SG=go"},{ids:["qet"],gl:"COMPL"}],
        rows:[
          {lang:"Nume",  forms:["o=lō","qēt"]},
          {lang:"Dorig", forms:["o=lō","qēt"]},
          {lang:"Koro",  forms:["o=lō","qēt"]},
          {lang:"Olrat", forms:["o=lō","qēt"]},
          {lang:"Lakon", forms:["o=lō","qēt"]},
        ],
        translation:"She/He has already gone.",
      }
    ]
  },
  {
    id:"moto", hw:"mōtō", pos:"n.", domain:"Food / Botany",
    gloss:"taro (Colocasia esculenta)",
    glossRich:"taro (<em>Colocasia esculenta</em>)",
    notes:"Staple food crop throughout Gaua. Takes the consumable-class possessive classifier <em>no-</em>.",
    langs:{ Nume:"mōtō", Dorig:"mōtō", Koro:"mōtō", Olrat:"mōto", Lakon:"mōtō" },
    examples:[
      {
        cols:[{ids:["no","kan"],gl:"1SG=eat"},{ids:["moto"],gl:"taro"}],
        rows:[
          {lang:"Nume",  forms:["no=kan","mōtō"]},
          {lang:"Dorig", forms:["no=kan","mōtō"]},
          {lang:"Koro",  forms:["no=kan","mōtō"]},
          {lang:"Olrat", forms:["no=kan","mōto"]},
          {lang:"Lakon", forms:["no=kan","mōtō"]},
        ],
        translation:"I eat taro.",
      }
    ]
  },
  {
    id:"no", hw:"no", pos:"pro.", domain:"Grammar",
    gloss:"I — 1st person singular subject",
    glossRich:"I — 1st person singular subject",
    notes:"Free pronoun and subject proclitic <em>no=</em> prefixed to the verb.",
    langs:{ Nume:"no", Dorig:"no", Koro:"no", Olrat:"no", Lakon:"no" },
    examples:[
      {
        cols:[{ids:["no"],gl:"1SG"},{ids:["to"],gl:"NEG"},{ids:["no","kan"],gl:"1SG=eat"},{ids:["qet"],gl:"COMPL"}],
        rows:[
          {lang:"Nume",  forms:["no","tō","no=kan","qēt"]},
          {lang:"Dorig", forms:["no","tō","no=kan","qēt"]},
          {lang:"Koro",  forms:["no","tō","no=kan","qēt"]},
          {lang:"Olrat", forms:["no","tō","no=kan","qēt"]},
          {lang:"Lakon", forms:["no","tō","no=kan","qēt"]},
        ],
        translation:"I have not eaten yet.",
      }
    ]
  },
  {
    id:"o", hw:"o", pos:"pro.", domain:"Grammar",
    gloss:"she/he/it — 3rd person singular subject",
    glossRich:"she/he/it — 3rd person singular subject",
    notes:"3sg subject proclitic <em>o=</em>; homophonous with 2sg in most languages.",
    langs:{ Nume:"o", Dorig:"o", Koro:"o", Olrat:"o", Lakon:"o" },
    examples:[
      {
        cols:[{ids:["o","wer"],gl:"3SG=big"}],
        rows:[
          {lang:"Nume",  forms:["o=wer"]},
          {lang:"Dorig", forms:["o=wer"]},
          {lang:"Koro",  forms:["o=wer"]},
          {lang:"Olrat", forms:["o=wer"]},
          {lang:"Lakon", forms:["o=wer"]},
        ],
        translation:"It/he/she is big.",
      }
    ]
  },
  {
    id:"qet", hw:"qēt", pos:"part.", domain:"Grammar",
    gloss:"COMPL — completive / perfective aspect marker",
    glossRich:"COMPL — completive / perfective aspect marker",
    notes:"Post-verbal particle signalling that an action has been completed. Invariant across all five languages — a remarkable isogloss.",
    langs:{ Nume:"qēt", Dorig:"qēt", Koro:"qēt", Olrat:"qēt", Lakon:"qēt" },
    examples:[
      {
        cols:[{ids:["no","kan"],gl:"1SG=eat"},{ids:["qet"],gl:"COMPL"}],
        rows:[
          {lang:"Nume",  forms:["no=kan","qēt"]},
          {lang:"Dorig", forms:["no=kan","qēt"]},
          {lang:"Koro",  forms:["no=kan","qēt"]},
          {lang:"Olrat", forms:["no=kan","qēt"]},
          {lang:"Lakon", forms:["no=kan","qēt"]},
        ],
        translation:"I have already eaten.",
      }
    ]
  },
  {
    id:"qol", hw:"qōl", pos:"v.tr.", domain:"Agriculture",
    gloss:"plant, cultivate",
    glossRich:"plant, cultivate",
    notes:"Used with garden produce and agricultural activities.",
    langs:{ Nume:"qōl", Dorig:"qōl", Koro:"qōl", Olrat:"qōl", Lakon:"qōl" },
    examples:[
      {
        cols:[{ids:["no","qol"],gl:"1SG=plant"},{ids:["moto"],gl:"taro"}],
        rows:[
          {lang:"Nume",  forms:["no=qōl","mōtō"]},
          {lang:"Dorig", forms:["no=qōl","mōtō"]},
          {lang:"Koro",  forms:["no=qōl","mōtō"]},
          {lang:"Olrat", forms:["no=qōl","mōto"]},
          {lang:"Lakon", forms:["no=qōl","mōtō"]},
        ],
        translation:"I am planting taro.",
      }
    ]
  },
  {
    id:"to", hw:"tō", pos:"part.", domain:"Grammar",
    gloss:"NEG — negation particle",
    glossRich:"NEG — negation particle",
    notes:"Pre-verbal negation; also functions as prohibitive in 2nd-person commands.",
    langs:{ Nume:"tō", Dorig:"tō", Koro:"tō", Olrat:"tō", Lakon:"tō" },
    examples:[
      {
        cols:[{ids:["to"],gl:"NEG"},{ids:["u","lo"],gl:"2SG=go"}],
        rows:[
          {lang:"Nume",  forms:["tō","u=lō"]},
          {lang:"Dorig", forms:["tō","u=lō"]},
          {lang:"Koro",  forms:["tō","u=lō"]},
          {lang:"Olrat", forms:["tō","u=lō"]},
          {lang:"Lakon", forms:["tō","u=lō"]},
        ],
        translation:"Don't go!",
      }
    ]
  },
  {
    id:"u", hw:"u", pos:"pro.", domain:"Grammar",
    gloss:"you — 2nd person singular subject",
    glossRich:"you — 2nd person singular subject",
    notes:"Free pronoun and subject proclitic <em>u=</em>.",
    langs:{ Nume:"u", Dorig:"u", Koro:"u", Olrat:"u", Lakon:"u" },
    examples:[
      {
        cols:[{ids:["u","kan"],gl:"2SG=eat"},{ids:["moto"],gl:"taro"},{ids:["are"],gl:"DEM"}],
        rows:[
          {lang:"Nume",  forms:["u=kan","mōtō","are"]},
          {lang:"Dorig", forms:["u=kan","mōtō","are"]},
          {lang:"Koro",  forms:["u=kan","mōtō","are"]},
          {lang:"Olrat", forms:["u=kan","mōto","are"]},
          {lang:"Lakon", forms:["u=kan","mōtō","are"]},
        ],
        translation:"You eat this taro.",
      }
    ]
  },
  {
    id:"wer", hw:"wer", pos:"v.stat.", domain:"Property",
    gloss:"be big, be large",
    glossRich:"be big, be large",
    notes:"Stative predicate verb; also used attributively in post-nominal position.",
    langs:{ Nume:"wer", Dorig:"wer", Koro:"wer", Olrat:"wer", Lakon:"wer" },
    examples:[
      {
        cols:[{ids:["gor"],gl:"man"},{ids:["are"],gl:"DEM"},{ids:["o","wer"],gl:"3SG=big"}],
        rows:[
          {lang:"Nume",  forms:["gōr","are","o=wer"]},
          {lang:"Dorig", forms:["gōr","are","o=wer"]},
          {lang:"Koro",  forms:["gōr","are","o=wer"]},
          {lang:"Olrat", forms:["gōr","are","o=wer"]},
          {lang:"Lakon", forms:["gōr","are","o=wer"]},
        ],
        translation:"That man is big.",
      }
    ]
  },
  {
    id:"wia", hw:"wia", pos:"v.tr.", domain:"Perception",
    gloss:"see, look at; (extended) find, discover",
    glossRich:"see, look at; (extended) find, discover",
    notes:"Transitive visual perception verb. Takes a direct object; the subject proclitic is obligatory.",
    langs:{ Nume:"wia", Dorig:"wia", Koro:"wia", Olrat:"wia", Lakon:"wia" },
    examples:[
      {
        cols:[{ids:["no","wia"],gl:"1SG=see"},{ids:["gor"],gl:"man"},{ids:["are"],gl:"DEM"}],
        rows:[
          {lang:"Nume",  forms:["no=wia","gōr","are"]},
          {lang:"Dorig", forms:["no=wia","gōr","are"]},
          {lang:"Koro",  forms:["no=wia","gōr","are"]},
          {lang:"Olrat", forms:["no=wia","gōr","are"]},
          {lang:"Lakon", forms:["no=wia","gōr","are"]},
        ],
        translation:"I see that man.",
      }
    ]
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

// ── Slug helper (texts.html deep-link anchor) ─────────────────
function textSlug(lang, title) {
  return ('text-' + lang + '-' + title)
    .toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-+/g,'-').replace(/^-|-$/g,'');
}

// ── Grammar sections ──────────────────────────────────────────
// Grammar example data uses the same comparative structure as dictionary examples.
// Stored separately so grammar.html can call buildGlossTable() on them.
// Each grammar example = { id, textLang, textTitle, cols, rows, translation }
const GRAMMAR_EXAMPLES = {
  ex1: {
    textLang:"Koro", textTitle:"The origin of the coconut",
    cols:[{ids:["gor"],gl:"man"},{ids:["are"],gl:"DEM"},{ids:["o","wer"],gl:"3SG=big"}],
    rows:[
      {lang:"Nume",  forms:["gōr","are","o=wer"]},
      {lang:"Dorig", forms:["gōr","are","o=wer"]},
      {lang:"Koro",  forms:["gōr","are","o=wer"]},
      {lang:"Olrat", forms:["gōr","are","o=wer"]},
      {lang:"Lakon", forms:["gōr","are","o=wer"]},
    ],
    translation:"That man is big.",
  },
  ex2: {
    textLang:"Koro", textTitle:"Kava ceremonies",
    cols:[{ids:["no","kan"],gl:"1SG=eat"},{ids:["are"],gl:"DEM"},{ids:["moto"],gl:"taro"}],
    rows:[
      {lang:"Nume",  forms:["no=kan","are","mōtō"]},
      {lang:"Dorig", forms:["no=kan","are","mōtō"]},
      {lang:"Koro",  forms:["no=kan","are","mōtō"]},
      {lang:"Olrat", forms:["no=kan","are","mōto"]},
      {lang:"Lakon", forms:["no=kan","are","mōtō"]},
    ],
    translation:"I am eating this taro.",
  },
  ex3: {
    textLang:"Lakon", textTitle:"A day of fishing",
    cols:[{ids:["o","lo"],gl:"3SG=go"},{ids:["egel"],gl:"village"}],
    rows:[
      {lang:"Nume",  forms:["o=lō","ēgēl"]},
      {lang:"Dorig", forms:["o=lō","ēgēl"]},
      {lang:"Koro",  forms:["o=lō","ēgēl"]},
      {lang:"Olrat", forms:["o=lō","ēgēl"]},
      {lang:"Lakon", forms:["o=lō","ēgēl"]},
    ],
    translation:"She/He went to the village.",
  },
  ex4: {
    textLang:"Nume", textTitle:"The orphan and the chief",
    cols:[{ids:["no","kan"],gl:"1SG=eat"},{ids:["qet"],gl:"COMPL"}],
    rows:[
      {lang:"Nume",  forms:["no=kan","qēt"]},
      {lang:"Dorig", forms:["no=kan","qēt"]},
      {lang:"Koro",  forms:["no=kan","qēt"]},
      {lang:"Olrat", forms:["no=kan","qēt"]},
      {lang:"Lakon", forms:["no=kan","qēt"]},
    ],
    translation:"I have already eaten.",
  },
  ex5: {
    textLang:"Dorig", textTitle:"Qat and his brothers",
    cols:[{ids:["o","lo"],gl:"3SG=go"},{ids:["qet"],gl:"COMPL"}],
    rows:[
      {lang:"Nume",  forms:["o=lō","qēt"]},
      {lang:"Dorig", forms:["o=lō","qēt"]},
      {lang:"Koro",  forms:["o=lō","qēt"]},
      {lang:"Olrat", forms:["o=lō","qēt"]},
      {lang:"Lakon", forms:["o=lō","qēt"]},
    ],
    translation:"She/He has already gone.",
  },
  ex6: {
    textLang:"Koro", textTitle:"The jealous brother",
    cols:[{ids:["no","wia"],gl:"1SG=see"},{ids:["gor"],gl:"man"},{ids:["are"],gl:"DEM"}],
    rows:[
      {lang:"Nume",  forms:["no=wia","gōr","are"]},
      {lang:"Dorig", forms:["no=wia","gōr","are"]},
      {lang:"Koro",  forms:["no=wia","gōr","are"]},
      {lang:"Olrat", forms:["no=wia","gōr","are"]},
      {lang:"Lakon", forms:["no=wia","gōr","are"]},
    ],
    translation:"I see that man.",
  },
  ex7: {
    textLang:"Koro", textTitle:"Preparing a garden",
    cols:[{ids:["no"],gl:"1SG"},{ids:["to"],gl:"NEG"},{ids:["no","kan"],gl:"1SG=eat"},{ids:["qet"],gl:"COMPL"}],
    rows:[
      {lang:"Nume",  forms:["no","tō","no=kan","qēt"]},
      {lang:"Dorig", forms:["no","tō","no=kan","qēt"]},
      {lang:"Koro",  forms:["no","tō","no=kan","qēt"]},
      {lang:"Olrat", forms:["no","tō","no=kan","qēt"]},
      {lang:"Lakon", forms:["no","tō","no=kan","qēt"]},
    ],
    translation:"I have not eaten yet.",
  },
  ex8: {
    textLang:"Lakon", textTitle:"Origin of the Lakon dances",
    cols:[{ids:["to"],gl:"NEG"},{ids:["u","lo"],gl:"2SG=go"}],
    rows:[
      {lang:"Nume",  forms:["tō","u=lō"]},
      {lang:"Dorig", forms:["tō","u=lō"]},
      {lang:"Koro",  forms:["tō","u=lō"]},
      {lang:"Olrat", forms:["tō","u=lō"]},
      {lang:"Lakon", forms:["tō","u=lō"]},
    ],
    translation:"Don't go!",
  },
};

// ── Raw comparative example: negation (real IPA data) ─────────
// No dictionary links — plain IPA forms; rendered by buildRawGlossTable()
const NEGATION_EXAMPLE = {
  textLang:"Koro", textTitle:"Preparing a garden",
  cols:[
    {gl:"3PL"},
    {gl:"NONDUM₁"},
    {gl:"know"},
    {gl:"properly"},
    {gl:"NONDUM₂"},
    {gl:"ART"},
    {gl:"speech"},
    {gl:"POSS:1INCL.PL"},
  ],
  rows:[
    {lang:"Nume",  abbr:"Num", forms:["nir",   "βitis",  "ɣil",    "liŋliŋi","mi",         "u",  "luwluw",   "namɣin"]},
    {lang:"Dorig", abbr:"Drg", forms:["nɪr",   "sɔwsɛ",  "βrɪɣɪl", "taβul",  "tɛ",         "na", "lŋa",      "‑ɣɪn"]},
    {lang:"Koro",  abbr:"Kro", forms:["nɪr",   "tɪ",     "rɔŋ",    "taβul",  "wʊsmɛlɛ",    "ɔ",  "βalβalaw", "namɪɣɪn"]},
    {lang:"Olrat", abbr:"Olr", forms:["nɪj",   "tɪ",     "rɔŋ",    "βɪlɪː",  "wʊsmɛlɛ",    "",   "ususraː",  "mʊʧ"]},
    {lang:"Lakon", abbr:"Lkn", forms:["ɣɪː",   "atɪ",    "rɔŋ",    "kɛrɛ",   "aβʊh.malɛ",  "",   "ɛlŋa",     "‑nɣɪʧ"]},
  ],
  translation:"'They don't know our language very well yet.'",
};

// ── Grammar narrative sections (only 2) ───────────────────────
const GRAMMAR = [
  {
    id:"s1", num:"1", title:"Phoneme inventory",
    subsections:[],
    body:`<p>The five languages of Gaua share a consonant inventory inherited from Proto-Oceanic, though each
has developed distinct local innovations. All five possess a series of prenasalised stops
(<em>mb, nd, ngg</em>), contrasting with plain stops. A uvular stop /q/ and a mid-back rounded vowel /ō/ —
both rare in the wider Oceanic family — are nonetheless consistent across the entire Gaua dialect chain.</p>
<table class="gram-table">
  <caption>Table 1 — Consonant inventory (shared across all five languages)</caption>
  <thead><tr><th></th><th>Labial</th><th>Alveolar</th><th>Velar</th><th>Uvular</th></tr></thead>
  <tbody>
    <tr><td>Plain stop</td><td>p, b</td><td>t, d</td><td>k, g</td><td>q</td></tr>
    <tr><td>Prenasalised</td><td>mb</td><td>nd</td><td>ngg</td><td>—</td></tr>
    <tr><td>Nasal</td><td>m</td><td>n</td><td>ng</td><td>—</td></tr>
    <tr><td>Fricative</td><td>β, v</td><td>s</td><td>ɣ</td><td>—</td></tr>
    <tr><td>Lateral / Rhotic</td><td>—</td><td>l, r</td><td>—</td><td>—</td></tr>
    <tr><td>Glide</td><td>w</td><td>—</td><td>—</td><td>—</td></tr>
  </tbody>
</table>
<table class="gram-table">
  <caption>Table 2 — Vowel inventory</caption>
  <thead><tr><th></th><th>Front</th><th>Central</th><th>Back</th></tr></thead>
  <tbody>
    <tr><td>High</td><td>i, iː</td><td>—</td><td>u, uː</td></tr>
    <tr><td>Mid</td><td>e, ɛ</td><td>—</td><td>o, ɔ, ō</td></tr>
    <tr><td>Low</td><td>—</td><td>a, aː</td><td>—</td></tr>
  </tbody>
</table>
<p>Vowel length is phonemically distinctive across all five languages. Stress is generally penultimate,
but shifts to the final syllable in verb stems followed by post-verbal aspect particles.</p>`
  },
  {
    id:"s2", num:"2", title:"Negation",
    subsections:[],
    body:`<p>Verbal negation across the five Gaua languages involves a split construction in which a
pre-verbal negator and a post-verbal bound morpheme together express sentential negation. This discontinuous
pattern is highly stable across the dialect chain, though the specific forms of each component vary from language to language.</p>
<p>The pre-verbal negator occupies the position immediately before the subject–verb complex. The post-verbal
element (glossed <strong>NONDUM₂</strong> below) may be suffixed to the final verb or to a post-verbal
particle, and can be omitted in casual registers, particularly in Lakon and Olrat. The example below
illustrates the full construction across all five languages:</p>
<negation-example></negation-example>`
  },
];
