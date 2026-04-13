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

// ── Grammar narrative sections ────────────────────────────────
// <gloss id="ex1"/> placeholders are replaced at runtime with
// buildGlossTable(GRAMMAR_EXAMPLES.ex1).
const GRAMMAR = [
  {
    id:"s1", num:"1", title:"Introduction", subsections:[],
    body:`<p>This chapter provides a comparative grammatical description of the five languages of Gaua Island:
<strong>Nume</strong>, <strong>Dorig</strong>, <strong>Koro</strong>, <strong>Olrat</strong>, and
<strong>Lakon</strong>, distributed from east to west. All five are closely related Oceanic languages of the
Austronesian family, forming a coherent dialect chain.</p>
<p>All grammatical claims are illustrated by comparative interlinear glossed examples. Each example shows all
five languages stacked vertically, sharing a single gloss line at the bottom.
<strong>Hover over any form</strong> to see its definition; <strong>click</strong> to open its full entry in
the <a href="dictionary.html">Dictionary</a>. Each example also links to its source text in the
<a href="texts.html">Texts</a> archive.</p>
<p>Language abbreviations: <b>Num</b> Nume · <b>Drg</b> Dorig · <b>Kro</b> Koro · <b>Olr</b> Olrat · <b>Lkn</b> Lakon.</p>`
  },
  {
    id:"s2", num:"2", title:"Phonology",
    subsections:[
      {id:"s2-1",num:"2.1",title:"Phoneme inventory"},
      {id:"s2-2",num:"2.2",title:"Vowel length"},
    ],
    body:`<h3 id="s2-1">2.1 Phoneme inventory <a href="#top" class="totop">↑</a></h3>
<p>The five languages share a consonant inventory inherited from Proto-Oceanic, including prenasalised stops
(<em>mb, nd, ngg</em>), a uvular stop /q/, and a mid-back rounded vowel /ō/ — both rare in the wider Oceanic
family yet consistent across the entire dialect chain.</p>
<table class="gram-table">
  <caption>Table 1 — Consonant inventory (shared across all five languages)</caption>
  <thead><tr><th></th><th>Labial</th><th>Alveolar</th><th>Velar</th><th>Uvular</th></tr></thead>
  <tbody>
    <tr><td>Plain stop</td><td>p</td><td>t</td><td>k</td><td>q</td></tr>
    <tr><td>Prenasalised</td><td>mb</td><td>nd</td><td>ngg</td><td>—</td></tr>
    <tr><td>Nasal</td><td>m</td><td>n</td><td>ng</td><td>—</td></tr>
    <tr><td>Fricative</td><td>v</td><td>s</td><td>—</td><td>—</td></tr>
    <tr><td>Lateral / Rhotic</td><td>—</td><td>l, r</td><td>—</td><td>—</td></tr>
    <tr><td>Glide</td><td>w</td><td>—</td><td>—</td><td>—</td></tr>
  </tbody>
</table>
<h3 id="s2-2">2.2 Vowel length <a href="#top" class="totop">↑</a></h3>
<p>Vowel length is phonemically distinctive in all five languages, as illustrated by minimal pairs such as
<a class="lexlink" href="dictionary.html#gor"><em>gōr</em></a> 'man' (long <em>ō</em>) vs.
<em>gor</em> 'to call' (short <em>o</em>). Stress is penultimate, shifting to the final syllable before
the completive particle <a class="lexlink" href="dictionary.html#qet"><em>qēt</em></a>.</p>
<gloss id="ex1"></gloss>`
  },
  {
    id:"s3", num:"3", title:"Personal pronouns",
    subsections:[
      {id:"s3-1",num:"3.1",title:"Singular forms"},
      {id:"s3-2",num:"3.2",title:"Non-singular and clusivity"},
    ],
    body:`<p>The Gaua languages have a rich pronominal system with distinctions of person (1st, 2nd, 3rd),
number (singular, dual, paucal, plural), and clusivity (inclusive vs. exclusive in non-singular 1st person).
Subject pronouns function as proclitics attaching to the left edge of the verb, marked by <strong>=</strong>.</p>
<h3 id="s3-1">3.1 Singular forms <a href="#top" class="totop">↑</a></h3>
<p>The singular forms are near-identical across all five languages, attesting to the conservative nature of
this paradigm within the Gaua dialect chain.</p>
<table class="gram-table">
  <caption>Table 2 — Singular subject proclitics</caption>
  <thead><tr><th>Person</th><th>Gloss</th><th>Num</th><th>Drg</th><th>Kro</th><th>Olr</th><th>Lkn</th></tr></thead>
  <tbody>
    <tr><td>1sg</td><td>I</td><td>no=</td><td>no=</td><td>no=</td><td>no=</td><td>no=</td></tr>
    <tr><td>2sg</td><td>you</td><td>u=</td><td>u=</td><td>u=</td><td>u=</td><td>u=</td></tr>
    <tr><td>3sg</td><td>s/he/it</td><td>o=</td><td>o=</td><td>o=</td><td>o=</td><td>o=</td></tr>
  </tbody>
</table>
<gloss id="ex2"></gloss>
<gloss id="ex3"></gloss>
<h3 id="s3-2">3.2 Non-singular and clusivity <a href="#top" class="totop">↑</a></h3>
<p>The dual, paucal, and plural series each require a separate proclitic paradigm. The 1st person non-singular
distinguishes <em>inclusive</em> (speaker + addressee + others) from <em>exclusive</em> (speaker + others)
forms in all five languages.<sup><a href="#fn1">1</a></sup></p>`
  },
  {
    id:"s4", num:"4", title:"Verb morphology",
    subsections:[
      {id:"s4-1",num:"4.1",title:"Aspect marking"},
      {id:"s4-2",num:"4.2",title:"Transitivity"},
    ],
    body:`<p>Verbs do not inflect for tense, aspect, or mood through affixation; these meanings are expressed
through post-verbal particles.</p>
<h3 id="s4-1">4.1 Aspect marking <a href="#top" class="totop">↑</a></h3>
<p>The completive aspect is marked by
<a class="lexlink" href="dictionary.html#qet"><em>qēt</em></a>,
found in identical form across all five languages — one of the most remarkable isoglosses of the Gaua dialect
chain.</p>
<gloss id="ex4"></gloss>
<gloss id="ex5"></gloss>
<h3 id="s4-2">4.2 Transitivity <a href="#top" class="totop">↑</a></h3>
<p>Transitive verbs (<a class="lexlink" href="dictionary.html#kan"><em>kan</em></a> 'eat',
<a class="lexlink" href="dictionary.html#wia"><em>wia</em></a> 'see',
<a class="lexlink" href="dictionary.html#qol"><em>qōl</em></a> 'plant') require a direct object; intransitive
verbs (<a class="lexlink" href="dictionary.html#lo"><em>lō</em></a> 'go',
<a class="lexlink" href="dictionary.html#wer"><em>wer</em></a> 'be big') do not.</p>`
  },
  {
    id:"s5", num:"5", title:"Possessive constructions",
    subsections:[{id:"s5-1",num:"5.1",title:"Classifier classes"}],
    body:`<p>Possession is encoded through possessive classifiers, a well-known feature of Oceanic languages.</p>
<h3 id="s5-1">5.1 Classifier classes <a href="#top" class="totop">↑</a></h3>
<table class="gram-table">
  <caption>Table 3 — Possessive classifier classes</caption>
  <thead><tr><th>Form</th><th>Class</th><th>Nouns covered</th></tr></thead>
  <tbody>
    <tr><td><em>no-</em></td><td>Consumable</td><td>Food and drink consumed by the possessor</td></tr>
    <tr><td><em>me-</em></td><td>Locative</td><td>Items associated with possessor's location</td></tr>
    <tr><td><em>ne-</em></td><td>Neutral</td><td>All other alienable objects</td></tr>
  </tbody>
</table>
<p>This tripartite distinction is preserved intact across all five languages.</p>
<gloss id="ex6"></gloss>`
  },
  {
    id:"s6", num:"6", title:"Negation",
    subsections:[{id:"s6-1",num:"6.1",title:"The discontinuous construction"}],
    body:`<p>Verbal negation uses the pre-verbal particle
<a class="lexlink" href="dictionary.html#to"><em>tō</em></a>.</p>
<h3 id="s6-1">6.1 The discontinuous construction <a href="#top" class="totop">↑</a></h3>
<p>In some registers a post-verbal suffix <em>-(V)t</em> co-occurs with <em>tō</em>, creating a
discontinuous pattern parallel to the Jespersen cycle. In casual speech the post-verbal element is
frequently dropped, especially in Lakon and Olrat.</p>
<gloss id="ex7"></gloss>
<gloss id="ex8"></gloss>`
  },
];
