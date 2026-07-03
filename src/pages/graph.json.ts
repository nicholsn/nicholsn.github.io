import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { loadBundle, iriOf, hrefOf, RELATION_SLOTS } from '../lib/lokf';

/**
 * The bundle as a cytoscape elements document — the same shape `lokf export`
 * emits for the LOKF graph explorer: nodes are concepts (plus blog posts,
 * which join the graph through their `about` links), edges are the typed
 * relations whose subject AND object both live in this bundle. External
 * targets (ORCID, DOIs, …) stay in the JSON-LD projection but are not drawn.
 */
export const GET: APIRoute = async () => {
  const { concepts, byIri } = await loadBundle();
  const posts = (await getCollection('blog')).filter((p) => !p.data.draft);

  const nodes = [
    ...concepts.map((c) => ({
      data: {
        id: iriOf(c),
        label: c.data.title,
        type: c.data.type,
        concept_id: c.id,
        href: hrefOf(c),
      },
    })),
    ...posts.map((p) => ({
      data: {
        id: `https://www.nolan-nichols.com/blog/${p.id}`,
        label: p.data.title,
        type: 'Post',
        concept_id: `blog/${p.id}`,
        href: `/blog/${p.id}`,
      },
    })),
  ];

  const known = new Set(nodes.map((n) => n.data.id));
  const edges: { data: Record<string, string> }[] = [];
  const addEdges = (sourceIri: string, data: Record<string, unknown>) => {
    for (const slot of [...RELATION_SLOTS, 'memberOf', 'holder']) {
      for (const target of (data[slot] as string[] | undefined) ?? []) {
        if (!known.has(target) || target === sourceIri) continue;
        edges.push({
          data: {
            id: `${slot}:${sourceIri}->${target}`,
            source: sourceIri,
            target,
            predicate: slot,
          },
        });
      }
    }
  };
  concepts.forEach((c) => addEdges(iriOf(c), c.data as Record<string, unknown>));
  posts.forEach((p) =>
    addEdges(`https://www.nolan-nichols.com/blog/${p.id}`, p.data as Record<string, unknown>),
  );

  return new Response(JSON.stringify({ nodes, edges }, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
