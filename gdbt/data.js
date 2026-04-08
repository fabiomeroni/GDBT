// ============================================================
//  Digital Boasian Trilogy — Gaua Languages
//  Shared data module
// ============================================================

const LANG_COLORS = {
  Nume:  "#2e5c8a",
  Dorig: "#c07820",
  Koro:  "#922810",
  Olrat: "#267040",
  Lakon: "#5c2878",
};

// ── Dictionary entries ───────────────────────────────────────
// Each entry: { pos, domain, gloss, notes, langs:{}, examples:[] }
const DICTIONARY = [
  {
    id: "are", hw: "are",
    pos: "det.", domain: "Grammar",
    gloss: "proximal demonstrative determiner — <em>this, these</em>",
    notes: "Post-nominal, invariant across all five languages. Contrasts with distal <em>ēnē</em>.",
    langs: { Nume:"are", Dorig:"are", Koro:"are", Olrat:"are", Lakon:"are" },
    examples: [
      { lang:"Koro", form:"gōr are", gloss:"man DEM", transl:"this man" },
      { lang:"Lakon", form:"ēgēl are", gloss:"village DEM", transl:"this village" }
    ]
  },
  {
    id: "egel", hw: "ēgēl",
    pos: "n.", domain: "Society",
    gloss: "village, inhabited settlement",
    notes: "Central concept in social organisation. Locative constructions place a motion verb before this noun with no overt preposition.",
    langs: { Nume:"ēgēl", Dorig:"ēgēl", Koro:"ēgēl", Olrat:"ēgēl", Lakon:"ēgēl" },
    examples: [
      { lang:"Lakon", form:"o=lō ēgēl", gloss:"3SG=go village", transl:"She went to the village." },
      { lang:"Koro",  form:"ēgēl are o=wer", gloss:"village DEM 3SG=big", transl:"This village is big." }
    ]
  },
  {
    id: "gor", hw: "gōr",
    pos: "n.", domain: "Human",
    gloss: "man; (generic) person, human being",
    notes: "Refers specifically to an adult male; used generically for 'person' in some contexts. Minimal pair with <em>gor</em> 'to call' (short vowel).",
    langs: { Nume:"gōr", Dorig:"gōr", Koro:"gōr", Olrat:"gōr", Lakon:"gōr" },
    examples: [
      { lang:"Koro",  form:"gōr are o=wer", gloss:"man DEM 3SG=big", transl:"That man is big." },
      { lang:"Dorig", form:"no=wia gōr", gloss:"1SG=see man", transl:"I see a man." }
    ]
  },
  {
    id: "kan", hw: "kan",
    pos: "v.tr.", domain: "Food",
    gloss: "eat (something)",
    notes: "Transitive verb requiring a direct object. Subject agreement expressed through proclitic <em>no=kan</em> '1sg eats'.",
    langs: { Nume:"kan", Dorig:"kan", Koro:"kan", Olrat:"kan", Lakon:"kan" },
    examples: [
      { lang:"Koro",  form:"no=kan are mōtō", gloss:"1SG=eat DEM taro", transl:"I am eating this taro." },
      { lang:"Nume",  form:"no=kan qēt", gloss:"1SG=eat COMPL", transl:"I have already eaten." }
    ]
  },
  {
    id: "lo", hw: "lō",
    pos: "v.intr.", domain: "Motion",
    gloss: "go",
    notes: "Intransitive motion verb. Often followed by a directional verb specifying orientation (e.g. <em>lō tar</em> 'go up', <em>lō van</em> 'go away').",
    langs: { Nume:"lō", Dorig:"lō", Koro:"lō", Olrat:"lō", Lakon:"lō" },
    examples: [
      { lang:"Lakon", form:"o=lō ēgēl", gloss:"3SG=go village", transl:"She went to the village." },
      { lang:"Dorig", form:"o=lō qēt", gloss:"3SG=go COMPL", transl:"She has already gone." }
    ]
  },
  {
    id: "moto", hw: "mōtō",
    pos: "n.", domain: "Food / Botany",
    gloss: "taro (<em>Colocasia esculenta</em>)",
    notes: "Staple food crop throughout Gaua. Takes the consumable-class possessive classifier <em>no-</em>.",
    langs: { Nume:"mōtō", Dorig:"mōtō", Koro:"mōtō", Olrat:"mōto", Lakon:"mōtō" },
    examples: [
      { lang:"Koro",  form:"no=kan mōtō", gloss:"1SG=eat taro", transl:"I eat taro." }
    ]
  },
  {
    id: "no", hw: "no",
    pos: "pro.", domain: "Grammar",
    gloss: "I — 1st person singular subject",
    notes: "Free pronoun and subject proclitic <em>no=</em> prefixed to the verb. The proclitic form loses its vowel before certain verb-initial consonants.",
    langs: { Nume:"no", Dorig:"no", Koro:"no", Olrat:"no", Lakon:"no" },
    examples: [
      { lang:"Koro",  form:"no=kan mōtō", gloss:"1SG=eat taro", transl:"I eat taro." },
      { lang:"Koro",  form:"no tō no=kan qēt", gloss:"1SG NEG 1SG=eat COMPL", transl:"I have not eaten." }
    ]
  },
  {
    id: "o", hw: "o",
    pos: "pro.", domain: "Grammar",
    gloss: "she/he/it — 3rd person singular subject",
    notes: "3sg subject proclitic <em>o=</em>; homophonous with 2sg in most languages. In Lakon a tonal distinction separates the two.",
    langs: { Nume:"o", Dorig:"o", Koro:"o", Olrat:"o", Lakon:"o" },
    examples: [
      { lang:"Koro",  form:"o=wer", gloss:"3SG=big", transl:"It/he/she is big." },
      { lang:"Lakon", form:"o=lō ēgēl", gloss:"3SG=go village", transl:"She went to the village." }
    ]
  },
  {
    id: "qet", hw: "qēt",
    pos: "part.", domain: "Grammar",
    gloss: "COMPL — completive / perfective aspect marker",
    notes: "Post-verbal particle signalling that an action has been completed. Invariant across all five languages — a remarkable isogloss and the strongest shared grammatical feature of the Gaua dialect chain.",
    langs: { Nume:"qēt", Dorig:"qēt", Koro:"qēt", Olrat:"qēt", Lakon:"qēt" },
    examples: [
      { lang:"Koro",  form:"no=kan qēt", gloss:"1SG=eat COMPL", transl:"I have already eaten." },
      { lang:"Dorig", form:"o=lō qēt", gloss:"3SG=go COMPL", transl:"She has already gone." }
    ]
  },
  {
    id: "qol", hw: "qōl",
    pos: "v.tr.", domain: "Agriculture",
    gloss: "plant, cultivate",
    notes: "Used with garden produce and agricultural activities. Subject-argument structure identical to other transitive verbs.",
    langs: { Nume:"qōl", Dorig:"qōl", Koro:"qōl", Olrat:"qōl", Lakon:"qōl" },
    examples: [
      { lang:"Koro", form:"no=qōl mōtō", gloss:"1SG=plant taro", transl:"I am planting taro." }
    ]
  },
  {
    id: "to", hw: "tō",
    pos: "part.", domain: "Grammar",
    gloss: "NEG — negation particle",
    notes: "Pre-verbal negation; part of a potentially discontinuous construction with post-verbal suffix <em>-(V)t</em>. Also functions as prohibitive in 2nd-person commands.",
    langs: { Nume:"tō", Dorig:"tō", Koro:"tō", Olrat:"tō", Lakon:"tō" },
    examples: [
      { lang:"Koro",  form:"no tō no=kan qēt", gloss:"1SG NEG 1SG=eat COMPL", transl:"I have not eaten yet." },
      { lang:"Lakon", form:"tō u=lō", gloss:"NEG 2SG=go", transl:"Don't go!" }
    ]
  },
  {
    id: "u", hw: "u",
    pos: "pro.", domain: "Grammar",
    gloss: "you — 2nd person singular subject",
    notes: "Free pronoun and subject proclitic <em>u=</em>. Historically distinct from 3sg *<em>o</em> but phonetically merged in some environments.",
    langs: { Nume:"u", Dorig:"u", Koro:"u", Olrat:"u", Lakon:"u" },
    examples: [
      { lang:"Koro", form:"u=kan mōtō are", gloss:"2SG=eat taro DEM", transl:"You eat this taro." }
    ]
  },
  {
    id: "wer", hw: "wer",
    pos: "v.stat.", domain: "Property",
    gloss: "be big, be large",
    notes: "Stative predicate verb; also used attributively in post-nominal position. Contrasts with <em>wer-wer</em> (reduplication) meaning 'very big'.",
    langs: { Nume:"wer", Dorig:"wer", Koro:"wer", Olrat:"wer", Lakon:"wer" },
    examples: [
      { lang:"Koro", form:"gōr are o=wer", gloss:"man DEM 3SG=big", transl:"That man is big." }
    ]
  },
  {
    id: "wia", hw: "wia",
    pos: "v.tr.", domain: "Perception",
    gloss: "see, look at; (extended) find, discover",
    notes: "Transitive visual perception verb. Takes a direct object; the subject proclitic is obligatory.",
    langs: { Nume:"wia", Dorig:"wia", Koro:"wia", Olrat:"wia", Lakon:"wia" },
    examples: [
      { lang:"Koro",  form:"no=wia gōr are", gloss:"1SG=see man DEM", transl:"I see that man." },
      { lang:"Dorig", form:"no=wia qēt", gloss:"1SG=see COMPL", transl:"I found it." }
    ]
  },
];

// ── Texts ────────────────────────────────────────────────────
const TEXTS = [
  { lang:"Nume",  title:"The origin of fire",           url:"https://pangloss.cnrs.fr/corpus/Nume", genre:"Myth",               year:"2000", rec:"A. François" },
  { lang:"Nume",  title:"How the sea became salt",       url:"https://pangloss.cnrs.fr/corpus/Nume", genre:"Myth",               year:"2001", rec:"A. François" },
  { lang:"Nume",  title:"Fishing with nets",             url:"https://pangloss.cnrs.fr/corpus/Nume", genre:"Procedural",         year:"2000", rec:"A. François" },
  { lang:"Nume",  title:"The orphan and the chief",      url:"https://pangloss.cnrs.fr/corpus/Nume", genre:"Narrative",          year:"2002", rec:"A. François" },
  { lang:"Dorig", title:"Qat and his brothers",          url:"https://pangloss.cnrs.fr/corpus/Dorig", genre:"Myth",              year:"2001", rec:"A. François" },
  { lang:"Dorig", title:"Building a canoe",              url:"https://pangloss.cnrs.fr/corpus/Dorig", genre:"Procedural",        year:"2002", rec:"A. François" },
  { lang:"Dorig", title:"The flying fox and the rat",    url:"https://pangloss.cnrs.fr/corpus/Dorig", genre:"Fable",             year:"2001", rec:"A. François" },
  { lang:"Dorig", title:"A feast in the village",        url:"https://pangloss.cnrs.fr/corpus/Dorig", genre:"Personal narrative", year:"2003", rec:"A. François" },
  { lang:"Koro",  title:"The origin of the coconut",     url:"https://pangloss.cnrs.fr/corpus/Koro_Gaua", genre:"Myth",         year:"2003", rec:"A. François" },
  { lang:"Koro",  title:"A journey to Santo",            url:"https://pangloss.cnrs.fr/corpus/Koro_Gaua", genre:"Personal narrative", year:"2004", rec:"A. François" },
  { lang:"Koro",  title:"Kava ceremonies",               url:"https://pangloss.cnrs.fr/corpus/Koro_Gaua", genre:"Procedural",   year:"2003", rec:"A. François" },
  { lang:"Koro",  title:"The jealous brother",           url:"https://pangloss.cnrs.fr/corpus/Koro_Gaua", genre:"Narrative",    year:"2005", rec:"A. François" },
  { lang:"Koro",  title:"Preparing a garden",            url:"https://pangloss.cnrs.fr/corpus/Koro_Gaua", genre:"Procedural",   year:"2004", rec:"A. François" },
  { lang:"Olrat", title:"The woman who became stone",    url:"https://pangloss.cnrs.fr/corpus/Olrat", genre:"Myth",             year:"2004", rec:"A. François" },
  { lang:"Olrat", title:"Garden magic spells",           url:"https://pangloss.cnrs.fr/corpus/Olrat", genre:"Ritual speech",    year:"2004", rec:"A. François" },
  { lang:"Olrat", title:"Childhood memories",            url:"https://pangloss.cnrs.fr/corpus/Olrat", genre:"Personal narrative",year:"2005", rec:"A. François" },
  { lang:"Lakon", title:"Origin of the Lakon dances",   url:"https://pangloss.cnrs.fr/corpus/Lakon", genre:"Myth",              year:"2006", rec:"A. François" },
  { lang:"Lakon", title:"A day of fishing",              url:"https://pangloss.cnrs.fr/corpus/Lakon", genre:"Personal narrative",year:"2007", rec:"A. François" },
  { lang:"Lakon", title:"The seven brothers",            url:"https://pangloss.cnrs.fr/corpus/Lakon", genre:"Traditional narrative",year:"2006", rec:"A. François" },
  { lang:"Lakon", title:"Healing plants of Gaua",        url:"https://pangloss.cnrs.fr/corpus/Lakon", genre:"Ethnobotanical",   year:"2007", rec:"A. François" },
];

// ── Grammar sections ─────────────────────────────────────────
// Used by grammar.html
const GRAMMAR = [
  {
    id:"s1", num:"1", title:"Introduction",
    subsections:[],
    body:`<p>This chapter provides a comparative grammatical description of the five languages of Gaua Island: <strong>Nume</strong>, <strong>Dorig</strong>, <strong>Koro</strong>, <strong>Olrat</strong>, and <strong>Lakon</strong>, distributed from east to west across the island. All five are closely related Oceanic languages of the Austronesian family. They share a common proto-language and form a coherent dialect chain — yet they are not mutually intelligible, and each has developed distinct phonological, morphological, and syntactic properties.</p>
<p>The description follows established typological and Oceanic-linguistic categories. All grammatical claims are illustrated by interlinear glossed text examples drawn from the archived corpora. <strong>Every morpheme in a glossed example is a hyperlink to its corresponding entry in the <a href="dictionary.html">Dictionary</a>.</strong> This bidirectional linking is the core innovation of the Digital Boasian Trilogy framework.</p>
<p>Glossing abbreviations follow the Leipzig Glossing Rules. Coloured labels identify the language of each example: <span class="chip" style="background:#2e5c8a">Nume</span> <span class="chip" style="background:#c07820">Dorig</span> <span class="chip" style="background:#922810">Koro</span> <span class="chip" style="background:#267040">Olrat</span> <span class="chip" style="background:#5c2878">Lakon</span>.</p>`
  },
  {
    id:"s2", num:"2", title:"Phonology",
    subsections:[
      { id:"s2-1", num:"2.1", title:"Phoneme inventory" },
      { id:"s2-2", num:"2.2", title:"Vowel length" },
      { id:"s2-3", num:"2.3", title:"Prenasalised stops" },
    ],
    body:`<h3 id="s2-1">2.1 Phoneme inventory <a href="#top" class="totop">↑</a></h3>
<p>The five languages of Gaua share a common phonological inventory inherited from Proto-Oceanic, though each has developed distinct local innovations. All five possess a series of prenasalised stops (<em>mb, nd, ngg</em>), contrasting with plain stops (<em>p, t, k</em>). The consonantal inventories are summarised in Table 1.</p>
<table class="gram-table">
  <caption>Table 1 — Consonant inventory (common to all five languages)</caption>
  <thead><tr><th></th><th>Labial</th><th>Alveolar</th><th>Velar</th><th>Uvular</th></tr></thead>
  <tbody>
    <tr><td>Plain stop</td><td>p</td><td>t</td><td>k</td><td>q</td></tr>
    <tr><td>Prenasalised</td><td>mb</td><td>nd</td><td>ngg</td><td>—</td></tr>
    <tr><td>Nasal</td><td>m</td><td>n</td><td>ng</td><td>—</td></tr>
    <tr><td>Fricative</td><td>v</td><td>s</td><td>—</td><td>—</td></tr>
    <tr><td>Lateral</td><td>—</td><td>l</td><td>—</td><td>—</td></tr>
    <tr><td>Rhotic</td><td>—</td><td>r</td><td>—</td><td>—</td></tr>
    <tr><td>Glide</td><td>w</td><td>—</td><td>—</td><td>—</td></tr>
  </tbody>
</table>
<h3 id="s2-2">2.2 Vowel length <a href="#top" class="totop">↑</a></h3>
<p>Vowel length is phonemically distinctive in all five languages, as illustrated by minimal pairs such as Koro <a class="lexlink" href="dictionary.html#gor"><em>gōr</em></a> 'man' (long <em>ō</em>) vs. <em>gor</em> 'to call' (short <em>o</em>). The languages also exhibit a uvular stop /q/ and a mid-back rounded vowel /ō/ — both rare in the wider Oceanic family yet consistent across the entire Gaua dialect chain.</p>
<h3 id="s2-3">2.3 Prenasalised stops <a href="#top" class="totop">↑</a></h3>
<p>A notable areal feature is the retention of Proto-Oceanic *R as a uvular trill in Koro and Lakon, which has merged with /r/ in Nume, Dorig, and Olrat. Stress is generally penultimate but shifts to the final syllable in verb stems followed by the completive aspect marker <a class="lexlink" href="dictionary.html#qet"><em>qēt</em></a>.</p>

<div class="example" id="ex1">
  <span class="ex-num">(1)</span>
  <span class="chip ex-lang" style="background:#922810">Koro</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#gor">gōr</a></td>
      <td><a class="lexlink" href="dictionary.html#are">are</a></td>
      <td><a class="lexlink" href="dictionary.html#o">o=</a><a class="lexlink" href="dictionary.html#wer">wer</a></td>
    </tr>
    <tr class="gloss-row">
      <td>man</td><td>DEM</td><td>3SG=big</td>
    </tr>
  </table>
  <div class="ex-transl">'That man is big.'</div>
  <div class="ex-source">Koro corpus, KOR_001</div>
</div>`
  },
  {
    id:"s3", num:"3", title:"Personal pronouns",
    subsections:[
      { id:"s3-1", num:"3.1", title:"Singular forms" },
      { id:"s3-2", num:"3.2", title:"Non-singular and clusivity" },
    ],
    body:`<p>The Gaua languages have a rich pronominal system with distinctions of person (1st, 2nd, 3rd), number (singular, dual, paucal, plural), and clusivity (inclusive vs. exclusive in non-singular 1st person). Subject pronouns function as proclitics attaching to the left edge of the verb, separated by the phonological boundary marker <strong>=</strong>.</p>

<h3 id="s3-1">3.1 Singular forms <a href="#top" class="totop">↑</a></h3>
<p>Remarkably, the singular forms are near-identical across all five languages, attesting to the conservative nature of this paradigm. Divergence emerges in the dual and plural, where Lakon shows the most pronounced differences from the eastern varieties.</p>
<table class="gram-table">
  <caption>Table 2 — Singular subject proclitics across all five languages</caption>
  <thead><tr><th>Person</th><th>Gloss</th><th>Nume</th><th>Dorig</th><th>Koro</th><th>Olrat</th><th>Lakon</th></tr></thead>
  <tbody>
    <tr><td>1sg</td><td>I</td><td>no=</td><td>no=</td><td>no=</td><td>no=</td><td>no=</td></tr>
    <tr><td>2sg</td><td>you</td><td>u=</td><td>u=</td><td>u=</td><td>u=</td><td>u=</td></tr>
    <tr><td>3sg</td><td>s/he/it</td><td>o=</td><td>o=</td><td>o=</td><td>o=</td><td>o=</td></tr>
  </tbody>
</table>

<div class="example" id="ex2">
  <span class="ex-num">(2)</span>
  <span class="chip ex-lang" style="background:#922810">Koro</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#no">no=</a><a class="lexlink" href="dictionary.html#kan">kan</a></td>
      <td><a class="lexlink" href="dictionary.html#are">are</a></td>
      <td><a class="lexlink" href="dictionary.html#moto">mōtō</a></td>
    </tr>
    <tr class="gloss-row">
      <td>1SG=eat</td><td>DEM</td><td>taro</td>
    </tr>
  </table>
  <div class="ex-transl">'I am eating this taro.'</div>
  <div class="ex-source">Koro corpus, KOR_012</div>
</div>

<div class="example" id="ex3">
  <span class="ex-num">(3)</span>
  <span class="chip ex-lang" style="background:#5c2878">Lakon</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#o">o=</a><a class="lexlink" href="dictionary.html#lo">lō</a></td>
      <td><a class="lexlink" href="dictionary.html#egel">ēgēl</a></td>
    </tr>
    <tr class="gloss-row">
      <td>3SG=go</td><td>village</td>
    </tr>
  </table>
  <div class="ex-transl">'She/He went to the village.'</div>
  <div class="ex-source">Lakon corpus, LAK_004</div>
</div>

<h3 id="s3-2">3.2 Non-singular and clusivity <a href="#top" class="totop">↑</a></h3>
<p>The dual, paucal, and plural series each require a separate proclitic paradigm. In all five languages, the 1st person non-singular distinguishes an <em>inclusive</em> form (speaker + addressee + others) from an <em>exclusive</em> form (speaker + others, addressee excluded). This four-way number distinction combined with clusivity gives the Gaua languages a pronominal system of considerable typological complexity.<sup><a href="#fn1">1</a></sup></p>`
  },
  {
    id:"s4", num:"4", title:"Verb morphology",
    subsections:[
      { id:"s4-1", num:"4.1", title:"Aspect marking" },
      { id:"s4-2", num:"4.2", title:"Transitivity" },
    ],
    body:`<p>Verbs in the Gaua languages are morphologically conservative: they do not inflect for tense, aspect, or mood through affixation. Instead, temporal and aspectual meaning is expressed through post-verbal particles. The subject proclitic agrees with the grammatical subject.</p>

<h3 id="s4-1">4.1 Aspect marking <a href="#top" class="totop">↑</a></h3>
<p>The completive aspect is marked by <a class="lexlink" href="dictionary.html#qet"><em>qēt</em></a>, found in identical form across all five languages. This particle follows the verb and signals that an action has been completed. It is one of the most remarkable isoglosses in the Gaua dialect chain.</p>

<div class="example" id="ex4">
  <span class="ex-num">(4)</span>
  <span class="chip ex-lang" style="background:#2e5c8a">Nume</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#no">no=</a><a class="lexlink" href="dictionary.html#kan">kan</a></td>
      <td><a class="lexlink" href="dictionary.html#qet">qēt</a></td>
    </tr>
    <tr class="gloss-row"><td>1SG=eat</td><td>COMPL</td></tr>
  </table>
  <div class="ex-transl">'I have already eaten.'</div>
  <div class="ex-source">Nume corpus, NUM_008</div>
</div>

<div class="example" id="ex5">
  <span class="ex-num">(5)</span>
  <span class="chip ex-lang" style="background:#c07820">Dorig</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#o">o=</a><a class="lexlink" href="dictionary.html#lo">lō</a></td>
      <td><a class="lexlink" href="dictionary.html#qet">qēt</a></td>
    </tr>
    <tr class="gloss-row"><td>3SG=go</td><td>COMPL</td></tr>
  </table>
  <div class="ex-transl">'She/He has already gone.'</div>
  <div class="ex-source">Dorig corpus, DOR_003</div>
</div>

<h3 id="s4-2">4.2 Transitivity <a href="#top" class="totop">↑</a></h3>
<p>Verbs are broadly divided into transitive and intransitive. Transitive verbs (<a class="lexlink" href="dictionary.html#kan"><em>kan</em></a> 'eat', <a class="lexlink" href="dictionary.html#wia"><em>wia</em></a> 'see', <a class="lexlink" href="dictionary.html#qol"><em>qōl</em></a> 'plant') require a direct object; intransitive verbs (<a class="lexlink" href="dictionary.html#lo"><em>lō</em></a> 'go', <a class="lexlink" href="dictionary.html#wer"><em>wer</em></a> 'be big') do not. Stative verbs form a sub-class of intransitives: they function as predicate adjectives when the subject proclitic is prefixed directly to the property concept root.</p>`
  },
  {
    id:"s5", num:"5", title:"Possessive constructions",
    subsections:[
      { id:"s5-1", num:"5.1", title:"Classifier classes" },
    ],
    body:`<p>Possession in the Gaua languages is encoded through a system of possessive classifiers — a well-known feature of Oceanic languages. Nouns are classified semantically according to the type of relationship they hold with their possessor.</p>

<h3 id="s5-1">5.1 Classifier classes <a href="#top" class="totop">↑</a></h3>
<p>Two main possession types are distinguished: <em>direct possession</em> (inalienable: body parts, kinship terms) and <em>indirect possession</em> (mediated by a classifier). The three main classifier classes are:</p>
<table class="gram-table">
  <caption>Table 3 — Possessive classifier classes</caption>
  <thead><tr><th>Form</th><th>Class</th><th>Nouns covered</th></tr></thead>
  <tbody>
    <tr><td><em>no-</em></td><td>Consumable</td><td>Food and drink consumed by the possessor</td></tr>
    <tr><td><em>me-</em></td><td>Locative</td><td>Items associated with possessor's dwelling/location</td></tr>
    <tr><td><em>ne-</em></td><td>Neutral</td><td>All other alienable objects</td></tr>
  </tbody>
</table>
<p>This tripartite distinction is preserved intact across all five languages, constituting one of the strongest shared structural features of the Gaua dialect chain.</p>

<div class="example" id="ex6">
  <span class="ex-num">(6)</span>
  <span class="chip ex-lang" style="background:#922810">Koro</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#no">no=</a><a class="lexlink" href="dictionary.html#wia">wia</a></td>
      <td><a class="lexlink" href="dictionary.html#gor">gōr</a></td>
      <td><a class="lexlink" href="dictionary.html#are">are</a></td>
    </tr>
    <tr class="gloss-row"><td>1SG=see</td><td>man</td><td>DEM</td></tr>
  </table>
  <div class="ex-transl">'I see that man.'</div>
  <div class="ex-source">Koro corpus, KOR_007</div>
</div>`
  },
  {
    id:"s6", num:"6", title:"Negation",
    subsections:[
      { id:"s6-1", num:"6.1", title:"The discontinuous construction" },
    ],
    body:`<p>Verbal negation in the Gaua languages follows a consistent pattern using the pre-verbal particle <a class="lexlink" href="dictionary.html#to"><em>tō</em></a>.</p>

<h3 id="s6-1">6.1 The discontinuous construction <a href="#top" class="totop">↑</a></h3>
<p>In some registers and languages, a post-verbal negation suffix <em>-(V)t</em> co-occurs with <em>tō</em>, creating a discontinuous negation pattern parallel to the Jespersen cycle found in French (<em>ne … pas</em>) and many other languages. In casual speech, the post-verbal element is frequently dropped, especially in Lakon and Olrat.</p>

<div class="example" id="ex7">
  <span class="ex-num">(7)</span>
  <span class="chip ex-lang" style="background:#922810">Koro</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#no">no</a></td>
      <td><a class="lexlink" href="dictionary.html#to">tō</a></td>
      <td><a class="lexlink" href="dictionary.html#no">no=</a><a class="lexlink" href="dictionary.html#kan">kan</a></td>
      <td><a class="lexlink" href="dictionary.html#qet">qēt</a></td>
    </tr>
    <tr class="gloss-row"><td>1SG</td><td>NEG</td><td>1SG=eat</td><td>COMPL</td></tr>
  </table>
  <div class="ex-transl">'I have not eaten yet.'</div>
  <div class="ex-source">Koro corpus, KOR_015</div>
</div>

<div class="example" id="ex8">
  <span class="ex-num">(8)</span>
  <span class="chip ex-lang" style="background:#5c2878">Lakon</span>
  <table class="gloss-table">
    <tr>
      <td><a class="lexlink" href="dictionary.html#to">tō</a></td>
      <td><a class="lexlink" href="dictionary.html#u">u=</a><a class="lexlink" href="dictionary.html#lo">lō</a></td>
    </tr>
    <tr class="gloss-row"><td>NEG</td><td>2SG=go</td></tr>
  </table>
  <div class="ex-transl">'Don't go!'</div>
  <div class="ex-source">Lakon corpus, LAK_011</div>
</div>`
  },
];
