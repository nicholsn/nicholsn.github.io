---
type: Document
title: "LOKF — Linked Open Knowledge Format"
description: >-
  A semantic profile of Google's Open Knowledge Format that turns a directory of
  markdown files into a queryable knowledge graph. This website is its reference
  implementation.
resource: https://lokf.nolan-nichols.com/
definedBy: [https://lokf.nolan-nichols.com/]
sameAs: [https://github.com/nicholsn/lokf]
tags: [knowledge graph, json-ld, rdf, linkml, semantic web, schema.org]
timestamp: 2026-07-03
featured: true
---

# LOKF — Linked Open Knowledge Format

**LOKF** is a semantic profile of Google's Open Knowledge Format (OKF). It keeps
OKF's pleasant authoring model — a directory of markdown files, each with a
small YAML frontmatter block describing one concept — and binds every concept,
field, and relationship to established web vocabularies (schema.org, W3C DCAT,
W3C PROV-O). A bundle of markdown files is therefore *also* valid JSON-LD that
expands losslessly to RDF. The format is defined once in
[LinkML](https://linkml.io); the JSON-LD context, JSON Schema, SHACL shapes, and
OWL ontology are all generated from that single source.

> Write OKF markdown, get a queryable knowledge graph for free.

## This site runs on it

The website you're reading is LOKF's reference implementation. My career,
publications, and projects are authored as a LOKF bundle — the same markdown
files render these human-readable pages *and* project to the schema.org JSON-LD
embedded in each page. Building this CV also surfaced a gap in LOKF v0.1 (no way
to express a dated employment role), which motivated reusing schema.org
`OrganizationRole` and the W3C Organization ontology rather than inventing new
vocabulary.

Read the [documentation](https://lokf.nolan-nichols.com/) or browse the
[source on GitHub](https://github.com/nicholsn/lokf).
