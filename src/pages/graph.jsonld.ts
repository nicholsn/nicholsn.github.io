import type { APIRoute } from 'astro';
import { loadBundle, conceptJsonLd } from '../lib/lokf';

/**
 * The whole bundle as one JSON-LD document (schema.org @graph) — the machine
 * view of the same concepts the site renders as pages. This is the LOKF
 * promise: markdown in, queryable knowledge graph out.
 */
export const GET: APIRoute = async () => {
  const { concepts, byIri } = await loadBundle();
  const graph = concepts.map((c) => {
    const node = conceptJsonLd(c, byIri) as Record<string, unknown>;
    delete node['@context'];
    return node;
  });
  const doc = { '@context': 'https://schema.org', '@graph': graph };
  return new Response(JSON.stringify(doc, null, 2), {
    headers: { 'Content-Type': 'application/ld+json; charset=utf-8' },
  });
};
