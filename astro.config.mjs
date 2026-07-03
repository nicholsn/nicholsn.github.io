// @ts-check
import { defineConfig } from 'astro/config';
import remarkLokfLinks from './remark-lokf-links.mjs';
import remarkStripLeadingTitle from './remark-strip-leading-title.mjs';

// The site is a static build of a LOKF bundle (src/content/knowledge) plus a
// blog (src/content/blog). Custom apex domain is served from GitHub Pages, so
// `base` stays '/'. `site` is used to mint absolute IRIs / canonical URLs and
// the schema.org JSON-LD @id values. The remark plugin rewrites LOKF's relative
// `.md` concept links to their site routes.
export default defineConfig({
  site: 'https://www.nolan-nichols.com',
  markdown: {
    remarkPlugins: [remarkLokfLinks, remarkStripLeadingTitle],
  },
});
