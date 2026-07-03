import { getCollection, type CollectionEntry } from 'astro:content';

/**
 * Helpers that treat the `knowledge` collection as a LOKF bundle: resolve
 * concept IRIs to entries, and project concepts into schema.org JSON-LD.
 * The concept IRI is `base_iri` + the entry's path id (the LOKF default),
 * which is exactly how the relation frontmatter references peers.
 */

export const BASE = 'https://www.nolan-nichols.com/';
export const ORCID = 'https://orcid.org/0000-0003-1099-3328';

export type Concept = CollectionEntry<'knowledge'>;

export const RELATION_SLOTS = [
  'isPartOf', 'hasPart', 'references', 'dependsOn', 'derivedFrom',
  'about', 'sameAs', 'relatedTo', 'definedBy', 'source',
] as const;

export const REL_LABEL: Record<string, string> = {
  isPartOf: 'Part of', hasPart: 'Has part', references: 'References',
  dependsOn: 'Depends on', derivedFrom: 'Derived from', about: 'About',
  sameAs: 'Same as', relatedTo: 'Related to', definedBy: 'Defined by',
  source: 'Source', memberOf: 'Member of', holder: 'Held by', measures: 'Measures',
};

export const iriOf = (e: Concept) => BASE + e.id;
export const hrefOf = (e: Concept) => '/' + e.id;

export async function loadBundle() {
  const all = await getCollection('knowledge');
  const concepts = all.filter((e) => e.data.type !== 'KnowledgeBundle');
  const byIri = new Map<string, Concept>();
  for (const e of concepts) byIri.set(iriOf(e), e);
  return { all, concepts, byIri };
}

const nameOf = (e?: Concept) => (e?.data as any)?.name ?? e?.data.title;

/** Sort roles most-recent first by startDate (YYYY or YYYY-MM strings). */
export function byStartDesc(a: Concept, b: Concept) {
  return String((b.data as any).startDate ?? '').localeCompare(
    String((a.data as any).startDate ?? ''));
}

/** A reified schema.org OrganizationRole node (dates + nested Organization). */
function orgRoleNode(r: Concept, byIri: Map<string, Concept>) {
  const d = r.data as any;
  const orgIri = (d.memberOf ?? [])[0];
  const org = orgIri ? byIri.get(orgIri) : undefined;
  const node: any = { '@type': 'OrganizationRole', roleName: d.roleName };
  if (d.startDate) node.startDate = String(d.startDate);
  if (d.endDate) node.endDate = String(d.endDate);
  if (org) {
    node.worksFor = { '@type': 'Organization', name: nameOf(org) };
    if ((org.data as any).url) node.worksFor.url = (org.data as any).url;
  }
  return node;
}

/** schema.org Person, with employment as OrganizationRole and education as alumniOf. */
export function personJsonLd(person: Concept, roles: Concept[], byIri: Map<string, Concept>) {
  const d = person.data as any;
  const employment = roles.filter((r) => ((r.data as any).roleType ?? 'employment') === 'employment');
  const education = roles.filter((r) => (r.data as any).roleType === 'education');
  const node: any = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': iriOf(person),
    name: d.name ?? d.title,
    url: BASE,
    sameAs: d.sameAs ?? [],
  };
  if (d.headline) node.jobTitle = d.headline;
  if (d.description) node.description = d.description;
  if (d.email) node.email = 'mailto:' + d.email;
  if (d.image) node.image = new URL(d.image, BASE).href;
  node.worksFor = employment.map((r) => orgRoleNode(r, byIri));
  node.alumniOf = education.map((r) => {
    const orgIri = ((r.data as any).memberOf ?? [])[0];
    const org = orgIri ? byIri.get(orgIri) : undefined;
    const o: any = { '@type': 'EducationalOrganization', name: nameOf(org) };
    if (org && (org.data as any).url) o.url = (org.data as any).url;
    return o;
  });
  return node;
}

const SCHEMA_TYPE: Record<string, string> = {
  Person: 'Person', Organization: 'Organization', Role: 'OrganizationRole',
  Reference: 'CreativeWork', Document: 'CreativeWork',
};

/** Generic per-concept JSON-LD for the concept (catch-all) pages and the graph. */
export function conceptJsonLd(e: Concept, byIri: Map<string, Concept>) {
  const d = e.data as any;
  const node: any = {
    '@context': 'https://schema.org',
    '@type': d.type === 'Reference' && d.doi ? 'ScholarlyArticle' : (SCHEMA_TYPE[d.type] ?? 'CreativeWork'),
    '@id': iriOf(e),
    name: d.title,
    url: d.resource ?? iriOf(e),
  };
  if (d.description) node.description = d.description;
  if (d.sameAs?.length) node.sameAs = d.sameAs;
  if (d.type === 'Reference') {
    node.author = { '@type': 'Person', '@id': ORCID, name: 'Nolan Nichols' };
    if (d.year) node.datePublished = String(d.year);
    if (d.venue) node.isPartOf = { '@type': 'Periodical', name: d.venue };
    if (d.doi) node.identifier = 'https://doi.org/' + d.doi;
  }
  if (d.type === 'Role') {
    node.roleName = d.roleName;
    if (d.startDate) node.startDate = String(d.startDate);
    if (d.endDate) node.endDate = String(d.endDate);
    const org = (d.memberOf ?? [])[0];
    if (org && byIri.get(org)) node.worksFor = { '@type': 'Organization', name: nameOf(byIri.get(org)) };
  }
  if (d.type === 'Organization') {
    if (d.url) node.url = d.url;
    if (d.location) node.location = d.location;
  }
  return node;
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

/** "2026-02" -> "Feb 2026"; "2009" -> "2009". */
export function fmtDate(s?: string) {
  if (!s) return '';
  const m = /^(\d{4})-(\d{2})$/.exec(s);
  return m ? `${MONTHS[+m[2] - 1]} ${m[1]}` : s;
}

export function fmtRange(start?: string, end?: string) {
  const s = fmtDate(start);
  const e = end ? fmtDate(end) : 'Present';
  return s ? `${s} – ${e}` : e;
}
