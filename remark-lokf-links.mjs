import path from 'node:path';

/**
 * LOKF concept bodies link to peers with relative `.md` paths (e.g.
 * `../roles/head-of-platform.md`). Rewrite those to their site routes
 * (`/roles/head-of-platform`). Links outside the knowledge bundle, or
 * absolute/external links, are left untouched.
 */
const KNOWLEDGE_ROOT = path.join(process.cwd(), 'src', 'content', 'knowledge');

function walk(node, fn) {
  if (!node || typeof node !== 'object') return;
  if (node.type === 'link') fn(node);
  if (Array.isArray(node.children)) for (const c of node.children) walk(c, fn);
}

export default function remarkLokfLinks() {
  return (tree, file) => {
    const filePath = file.path || (file.history && file.history[0]);
    if (!filePath) return;
    const dir = path.dirname(filePath);
    walk(tree, (node) => {
      const url = node.url || '';
      if (!url.endsWith('.md') || /^(https?:|mailto:|#|\/)/.test(url)) return;
      const abs = path.resolve(dir, url);
      const rel = path.relative(KNOWLEDGE_ROOT, abs).replace(/\.md$/, '');
      if (rel.startsWith('..')) return;
      node.url = '/' + rel.split(path.sep).join('/');
    });
  };
}
