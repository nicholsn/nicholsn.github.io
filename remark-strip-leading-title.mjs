/**
 * Concept bodies open with a `# Title` (and roles add an `*italic date*`
 * subtitle) that duplicate the page chrome the layout already renders from
 * frontmatter. Strip that leading title, and a following emphasis-only
 * paragraph, so the body is just prose. Blog posts open at `##`, so they are
 * left untouched.
 */
export default function remarkStripLeadingTitle() {
  return (tree) => {
    const c = tree.children;
    if (c.length && c[0].type === 'heading' && c[0].depth === 1) {
      c.shift();
      if (
        c.length &&
        c[0].type === 'paragraph' &&
        c[0].children.length === 1 &&
        c[0].children[0].type === 'emphasis'
      ) {
        c.shift();
      }
    }
  };
}
