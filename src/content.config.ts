import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/**
 * The site's content is a LOKF bundle: a directory of markdown concept files
 * whose frontmatter keys bind to public web vocabularies (schema.org, DCAT,
 * PROV-O, and — for employment — the W3C Organization ontology). This schema
 * is the site's LOKF *profile*: it mirrors the term bindings in
 * ../lokf/lokf.yaml and adds a `Role` type that lokf v0.1 lacks.
 *
 * `Role` reuses established vocabulary (no new terms invented):
 *   Role         -> schema:OrganizationRole  (close: org:Role, vivo:Position)
 *   roleName     -> schema:roleName
 *   startDate    -> schema:startDate          (RDF layer: org:memberDuring)
 *   endDate      -> schema:endDate
 *   memberOf     -> schema:memberOf           (close: org:organization)
 *   holder       -> org:member                (the Person holding the role)
 *
 * LOKF `id` (the RDF subject IRI) is intentionally NOT a frontmatter field:
 * per the LOKF default it derives from `base_iri` + the concept's path, which
 * also avoids Astro's glob-loader reserved-`id` collision. External identity
 * (ORCID, DOI, ROR, homepages) is carried on `sameAs` / `resource`.
 */

const iri = z.string().url();
const iris = z.array(iri);

// LOKF core typed relations (lokf.yaml Concept) — every link carries meaning.
const relations = {
  isPartOf: iris.optional(),    // dcterms:isPartOf
  hasPart: iris.optional(),     // schema:hasPart
  references: iris.optional(),  // dcterms:references
  dependsOn: iris.optional(),   // dcterms:requires
  derivedFrom: iris.optional(), // prov:wasDerivedFrom
  about: iris.optional(),       // schema:about
  sameAs: iris.optional(),      // schema:sameAs / owl:sameAs
  relatedTo: iris.optional(),   // dcterms:relation
  definedBy: iris.optional(),   // rdfs:isDefinedBy
  source: iris.optional(),      // dcterms:source
};

const knowledge = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/knowledge' }),
  schema: z.object({
    // --- OKF/LOKF core (lokf.yaml Concept) ------------------------------
    type: z.enum([
      'Person',
      'Organization',
      'Role',
      'Reference',
      'Document',
      'KnowledgeBundle',
    ]),
    title: z.string(),                      // schema:name
    description: z.string().optional(),     // schema:description
    resource: iri.optional(),               // schema:url — the underlying asset
    tags: z.array(z.string()).optional(),   // schema:keywords
    timestamp: z.coerce.date().optional(),  // schema:dateModified
    created: z.coerce.date().optional(),    // schema:dateCreated
    featured: z.boolean().optional(),       // site-only: promote on home/index

    ...relations,

    // --- Person (schema:Person / foaf:Person) ---------------------------
    name: z.string().optional(),
    headline: z.string().optional(),
    email: z.string().optional(),           // schema:email
    orcid: iri.optional(),
    github: iri.optional(),
    linkedin: iri.optional(),
    image: z.string().optional(),           // schema:image

    // --- Organization (schema:Organization) -----------------------------
    url: iri.optional(),                     // schema:url (org homepage)
    location: z.string().optional(),         // schema:location / locality

    // --- Role (schema:OrganizationRole + org:Role) — LOKF extension ------
    roleType: z.enum(['employment', 'education']).optional(), // CV bucket: worksFor vs alumniOf
    roleName: z.string().optional(),         // schema:roleName
    startDate: z.string().optional(),        // schema:startDate (YYYY | YYYY-MM)
    endDate: z.string().optional(),          // schema:endDate (omit = current)
    memberOf: iris.optional(),               // schema:memberOf -> Organization
    holder: iris.optional(),                 // org:member -> Person

    // --- Reference (publications -> schema:ScholarlyArticle) -------------
    doi: z.string().optional(),
    venue: z.string().optional(),            // periodical / publisher
    year: z.number().optional(),             // schema:datePublished (year)
    authors: z.array(z.string()).optional(), // schema:author

    // --- Bundle root (index.md; lokf.yaml KnowledgeBundle) --------------
    lokf_version: z.string().optional(),
    okf_version: z.string().optional(),
    base_iri: iri.optional(),
    context: iri.optional(),
    license: iri.optional(),
  }),
});

// Blog posts render as schema:BlogPosting; `about` can link a post back into
// the knowledge bundle so writing and concepts share one graph.
const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.coerce.date(),                   // schema:datePublished
    updated: z.coerce.date().optional(),     // schema:dateModified
    category: z.string().optional(),
    tags: z.array(z.string()).optional(),
    about: iris.optional(),
    draft: z.boolean().optional(),
  }),
});

export const collections = { knowledge, blog };
