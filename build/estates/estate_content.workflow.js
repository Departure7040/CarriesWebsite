export const meta = {
  name: 'estate-content',
  description: 'Generate captions + editorial copy for an estate microsite from its facts + photos',
  phases: [
    { title: 'Caption', detail: 'parallel photo captioners' },
    { title: 'Copy', detail: 'editorial copy grounded in facts + captions' },
  ],
}

const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const slug = A.slug
const dir = A.gallery_disk_dir
const count = A.count
const facts = A.facts
const FACTS_JSON = JSON.stringify(facts, null, 2)

function files(from, to) {
  const a = []
  for (let i = from; i <= to; i++) a.push(String(i).padStart(2, '0') + '.jpg')
  return a
}
const CAP_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['items'],
  properties: { items: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['file', 'alt'], properties: { file: { type: 'string' }, alt: { type: 'string' } } } } },
}
function capPrompt(fs) {
  return `You are a real-estate photo editor writing accessible ALT TEXT for a single-property listing site (${facts.address}, ${facts.city}, ${facts.state} — a ${facts.type_short}). Open each image on disk and write one concise descriptive alt line (room/space/architecture/materials/fixtures/pool/patio you actually see).
FILES (in ${dir}/): ${fs.join(', ')}
STRICT: describe ONLY what is visible; never people/demographics; never claim "waterfront"/water views unless an actual pond/lake/bayou is visible; under 45 words; exact filenames like "07.jpg".
Return items[] for every file.`
}

phase('Caption')
const half = Math.ceil(count / 2)
const s1 = agent(capPrompt(files(1, half)), { label: 'caption:a', phase: 'Caption', schema: CAP_SCHEMA, agentType: 'general-purpose' })
const s2 = half < count ? agent(capPrompt(files(half + 1, count)), { label: 'caption:b', phase: 'Caption', schema: CAP_SCHEMA, agentType: 'general-purpose' }) : Promise.resolve({ items: [] })
const [r1, r2] = await parallel([() => s1, () => s2])
const captions = [r1, r2].filter(Boolean).flatMap(r => r.items || [])
captions.sort((a, b) => parseInt(a.file) - parseInt(b.file))

phase('Copy')
const COPY_TOOL_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['hero_tagline', 'overview_heading', 'overview_paragraphs', 'pull_quote', 'feature_groups', 'location_paragraphs', 'location_points'],
  properties: {
    hero_tagline: { type: 'string' }, overview_heading: { type: 'string' },
    overview_paragraphs: { type: 'array', items: { type: 'string' } }, pull_quote: { type: 'string' },
    feature_groups: { type: 'array', items: { type: 'object', additionalProperties: false, required: ['title', 'items'], properties: { title: { type: 'string' }, items: { type: 'array', items: { type: 'string' } } } } },
    location_paragraphs: { type: 'array', items: { type: 'string' } },
    location_points: { type: 'array', items: { type: 'string' } },
  },
}
const capList = captions.map(c => '- ' + c.alt).join('\n')
const copy = await agent(
  `You are a luxury real-estate copywriter. Editorial, restrained, atmospheric. Write the copy for a single-property microsite.

FACTS:
${FACTS_JSON}

PHOTO CAPTIONS (what the photos actually show):
${capList}

HARD RULES:
- Ground every factual claim in the FACTS + CAPTIONS. Do NOT invent brands, materials, room counts, or measurements not supported by them.
- Never say "waterfront" unless a caption mentions a pond/lake/bayou.
- FAIR HOUSING: location copy describes geography/amenities/the property only — never demographics, never "family/safe/good schools" or who it "suits".
- feature_groups: exactly 3 groups; every item supported by a caption or a fact. overview_paragraphs: 2-3. location_points: 6-8 (geography/amenities near ${facts.city}, ${facts.state}).
- Match the tone to the property: this is a ${facts.price} ${facts.type_short} built ${facts.year_built} — do not oversell a mid-market home as an ultra-luxury estate; be tasteful and accurate.
Return the structured copy.`,
  { label: 'copy:write', phase: 'Copy', schema: COPY_TOOL_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)

return { slug, captions, copy }
