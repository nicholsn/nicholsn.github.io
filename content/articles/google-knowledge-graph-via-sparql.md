Title: RDFizing Results from the Google Knowledge Graph API
Date: 2016-01-12
Category: Semantic Web
Tags: semantic web, owl, rdf,
Slug: knowledge-graph-via-sparql
Author: Nolan Nichols
Summary: How to access the Google Knowledge Graph API as RDF using SPARQL

## Introduction

The Google Knowledge Graph Search API was recently made
publicly [available](https://developers.google.com/knowledge-graph/). This API allows
for the use of [Schema.org](http://schema.org/) types to limit the scope of search
results to entities that have been categorized as a given type.

For example, a search may be limited to the schema.org type of "Person" or "TVSeries" to
enhance the quality of search results. Interestingly, the format of the data that is
returned is [JSON-LD/(http://json-ld.org/) that provides a mapping between the JSON keys
and URI's that include a unique and dereferencible identifier for clarifying the meaning
of a given key.

Further, JSON-LD (the LD is for Linked Data) is interoperable with the Resource
Description Framework ([RDF](https://www.w3.org/RDF/)) that offers a graph-based
representation of knowledge based on subject-predicate-object "triples." For an API
called 'Knowledge Graph" it makes sense to use a format that is compatible with
this [W3C](https://www.w3.org/) standard that underlies the Web's knowledge
representation formalism: the Web Ontology
Language ([OWL](https://www.w3.org/TR/owl-features/))

What this buys us is the ability to use other W3C standards for working with the results
of the Knowledge Graph, such as the [SPARQL](https://www.w3.org/TR/sparql11-query/)
Protocol and RDF Query Language. In this post, I am going to demonstrate how we can use
a couple Python libraries to:

- access the Knowledge Graph API
- convert the JSON-LD results into RDF as a [Turtle](https://www.w3.org/TR/turtle/)
  document
- query the RDF graph using SPARQL

## Python Libraries

First we need a few libraries for handling requests to the Knowledge Graoh API (
requests), converting the JSON-LD results into RDF (pyld), and parsing the RDF into a
queryable graph (rdflib). You can fnd these libraries at the links below:

- PyLD: https://github.com/digitalbazaar/pyld
- RDFLib: https://github.com/RDFLib/rdflib
- Requests: https://github.com/kennethreitz/requests

```python
import os
import json

import pyld
import rdflib
import requests
```

## Accessing the Knowledge Graph API

Here we first need to obtain a key from
the [Google Developers Console](https://console.developers.google.com) and enable
access. You won't see the Knowledge Graph API show up in the list of popular APIS, so
you'll need to search for it in the API Manager. Once you enable the API and generate a
key, you may need to add your IP address to the section on "Accept requests from these
server IP addresses".

Below, I've saved my key and read it in. For fun here, I am just searching the
schema.org type of "TVSeries" for a cartoon series called "Archer" - of course you can
search for something more serious, but one thing I found is that many of the schema.org
types are not supported. For example, an error was raised when I searched for the
schema.org type for "Drug", "Anatomical Structure", and "MedicalStudy".

```python
kg_key = open(os.path.join(os.path.expanduser('~'), '.knowledge-graph-key')).read()
r = requests.get("https://kgsearch.googleapis.com/v1/entities:search",
                 params=dict(query="Archer", key=kg_key, types="TVSeries"))
```

## Parsing the and Examining the Results

This is pretty straight forward. We just parse the returned JSON-LD using the standard
json library - note that JSON-LD can be treated as just plain old JSON.

You can see in the results that the initial section includes an `@context` indicating
the mapping between different vocabularies and a "key". There are a number of returned '
hits' and that each hit has associated with it a score. Here, the top score of '
43.221546' is the TV Show we are interested in - Archer.

```python
jsonld = json.loads(r.text)
print(r.text)
```

    {
      "@context": {
        "@vocab": "http://schema.org/",
        "goog": "http://schema.googleapis.com/",
        "EntitySearchResult": "goog:EntitySearchResult",
        "detailedDescription": "goog:detailedDescription",
        "resultScore": "goog:resultScore",
        "kg": "http://g.co/kg"
      },
      "@type": "ItemList",
      "itemListElement": [
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/06_wvhl",
            "name": "Archer",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "American animated series",
            "image": {
              "contentUrl": "http://t3.gstatic.com/images?q=tbn:ANd9GcQwUXmJt_InhAr39HEyyv8l4CIiom0RvTvNYcf-JoCN8cpXOyon",
              "url": "https://en.wikipedia.org/wiki/Archer_(TV_series)",
              "license": "http://creativecommons.org/licenses/by/2.0"
            },
            "detailedDescription": {
              "articleBody": "Archer is an American adult animated television series created by Adam Reed for the FX network. A preview of the series aired on September 17, 2009. The first season premiered on January 14, 2010. ",
              "url": "http://en.wikipedia.org/wiki/Archer_(TV_series)",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            },
            "url": "http://www.fxnetworks.com/archer"
          },
          "resultScore": 43.221546
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/02qcfrx",
            "name": "Spanish Archer",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "TV show",
            "detailedDescription": {
              "articleBody": "Spanish Archer was a talent show hosted by Rhodri Williams and occasionally Ruth Madoc. It was produced by L!VE TV and filmed at the station's headquarters at Canary Wharf in London.\n",
              "url": "http://en.wikipedia.org/wiki/Spanish_Archer",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 16.060818
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/07cggr0",
            "name": "Archer (1975)",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "TV series"
          },
          "resultScore": 14.106644
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/06w21l8",
            "name": "Meet Corliss Archer",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "American sitcom",
            "image": {
              "contentUrl": "http://t2.gstatic.com/images?q=tbn:ANd9GcRqPkGi1_Rselb-ijqy_-5of6WsEkhDmoU036ZsvXBS83XZsWGb",
              "url": "http://en.wikipedia.org/wiki/Meet_Corliss_Archer_(TV_series)"
            },
            "detailedDescription": {
              "articleBody": "Meet Corliss Archer is an American sitcom that aired in syndication from April to December 1954. The series stars Ann Baker in the title role. ",
              "url": "http://en.wikipedia.org/wiki/Meet_Corliss_Archer_(TV_series)",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 12.145683
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0gfds00",
            "name": "Jeffrey Archer: The Truth",
            "@type": [
              "TVSeries",
              "Movie",
              "Thing"
            ],
            "description": "2002 film",
            "detailedDescription": {
              "articleBody": "Jeffrey Archer: The Truth is a 2002 BBC satirical comedy drama on the life of Jeffrey Archer, with the title role played by Damian Lewis. Its duration was 90 minutes and its premiere occurred on 1 December 2002. It was written and directed by Guy Jenkin.",
              "url": "http://en.wikipedia.org/wiki/Jeffrey_Archer:_The_Truth",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 11.167856
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/g/11cknytgw6",
            "name": "Cassius &amp; Clay",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "detailedDescription": {
              "articleBody": "Cassius &amp; Clay is an upcoming American animated television series created by Adam Reed to be aired in 2016 alongside Archer on FXX. The show follows two women, Cassius and Clay living as bandits in a futuristic, post-apocalyptic America. ",
              "url": "http://en.wikipedia.org/wiki/Cassius_%26_Clay",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.67782
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0bcr8s",
            "name": "Robin Hood",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "British television programme",
            "detailedDescription": {
              "articleBody": "Robin Hood is a British television programme, produced by independent production company Tiger Aspect Productions for BBC One, with co-funding from the BBC America cable television channel in the United States. ",
              "url": "http://en.wikipedia.org/wiki/Robin_Hood_(2006_TV_series)",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            },
            "url": "http://www.robin-hood.tv/"
          },
          "resultScore": 1.573618
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0cv8fbn",
            "name": "Violet Tendencies",
            "@type": [
              "Movie",
              "TVSeries",
              "Thing"
            ],
            "description": "2010 film",
            "detailedDescription": {
              "articleBody": "Violet Tendencies is a 2010 romantic comedy film directed by Casper Andreas, written by Jesse Archer, and starring Mindy Cohn and Marcus Patrick. ",
              "url": "http://en.wikipedia.org/wiki/Violet_Tendencies",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.50758
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0hzp2zq",
            "name": "Animation Salvation",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "Television Program",
            "detailedDescription": {
              "articleBody": "Animation Salvation is an Australian television Sunday night-time animation block aired on Fox8 on Sunday 7:30 pm to 10:30 pm from 7 March 2010.",
              "url": "http://en.wikipedia.org/wiki/Animation_Salvation",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.371247
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0kfwmt7",
            "name": "The Pirate",
            "@type": [
              "TVSeries",
              "Movie",
              "Thing"
            ],
            "description": "1978 film",
            "detailedDescription": {
              "articleBody": "The Pirate is a 1978 American TV movie directed by Ken Annakin. It is based on the novel with the same title written by Harold Robbins.\nIt was broadcast by ABC in two parts November 21–22, 1978.",
              "url": "http://en.wikipedia.org/wiki/The_Pirate_(1978_film)",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.225814
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0522jn",
            "name": "Major Dad",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "American sitcom",
            "detailedDescription": {
              "articleBody": "Major Dad is an American sitcom created by Richard C. Okie and John G. Stephens, developed by Earl Pomerantz, that originally ran from 1989 to 1993 on CBS, starring Gerald McRaney as Major John D. MacGillis and Shanna Reed as his wife Polly. ",
              "url": "http://en.wikipedia.org/wiki/Major_Dad",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.142771
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0264z1w",
            "name": "The Dame Edna Experience",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "British television show",
            "detailedDescription": {
              "articleBody": "The Dame Edna Experience is a British television comedy talk-show hosted by Dame Edna Everage. It ran for twelve regular episodes on ITV, plus two Christmas specials.",
              "url": "http://en.wikipedia.org/wiki/The_Dame_Edna_Experience",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.123545
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/02qcyy2",
            "name": "Footy Classified",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "Australian television program",
            "detailedDescription": {
              "articleBody": "Footy Classified, is an Australian television program broadcast on the Nine Network which discusses pressing issues relating to AFL football. It debuted on Monday 2 April 2007. ",
              "url": "http://en.wikipedia.org/wiki/Footy_Classified",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            },
            "url": "http://wwos.ninemsn.com.au/afl/classified/"
          },
          "resultScore": 1.105602
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/04q8zth",
            "name": "The Californians",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "Television Series",
            "image": {
              "contentUrl": "http://t3.gstatic.com/images?q=tbn:ANd9GcSQ0FvOFyPFq3qLlZsbr4UTcIef_WZFGTqQfVum3VzCxpykLMhK",
              "url": "http://en.wikipedia.org/wiki/The_Californians_(TV_series)"
            },
            "detailedDescription": {
              "articleBody": "The Californians is a 54-episode half-hour Western television series, set in the San Francisco gold rush of the 1850s, which aired on NBC from September 24, 1957, to May 26, 1959. ",
              "url": "http://en.wikipedia.org/wiki/The_Californians_(TV_series)",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 1.043589
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0y5gfz0",
            "name": "Roald Dahl's Esio Trot",
            "@type": [
              "TVSeries",
              "Thing",
              "Movie"
            ],
            "description": "Television film",
            "detailedDescription": {
              "articleBody": "Roald Dahl's Esio Trot is a British comedy television film that was first broadcast as part of BBC One's 2014 Christmas programming. ",
              "url": "http://en.wikipedia.org/wiki/Roald_Dahl's_Esio_Trot",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 0.963223
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/07ch475",
            "name": "Seventh Avenue",
            "@type": [
              "TVSeries",
              "Movie",
              "Thing"
            ],
            "description": "American television miniseries",
            "detailedDescription": {
              "articleBody": "Seventh Avenue is a six-part American television miniseries broadcast in 1977. It is based on the 1967 Norman Bogner novel of the same name. ",
              "url": "http://en.wikipedia.org/wiki/Seventh_Avenue_(miniseries)",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 0.930134
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0k2dng7",
            "name": "Help! My Supply Teacher's Magic",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "TV Show",
            "detailedDescription": {
              "articleBody": "Help! My Supply Teacher's Magic is a CBBC show which shows magicians in schools, tricking children into thinking they are supply teachers. It is presented by Iain Stirling. ",
              "url": "http://en.wikipedia.org/wiki/Help!_My_Supply_Teacher's_Magic",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 0.871172
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/0863kh",
            "name": "Storefront Lawyers",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "American drama series",
            "detailedDescription": {
              "articleBody": "Storefront Lawyers is an American legal drama that ran from September 1970 to April 1971 on CBS. The series stars Robert Foxworth, Sheila Larken, David Arkin, and A Martinez.",
              "url": "http://en.wikipedia.org/wiki/Storefront_Lawyers",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 0.871042
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/02rp2_",
            "name": "The Big Read",
            "@type": [
              "TVSeries",
              "Thing"
            ],
            "description": "Television Programme",
            "detailedDescription": {
              "articleBody": "The Big Read was a survey on books carried out by the BBC in the United Kingdom in 2003, where over three quarters of a million votes were received from the British public to find the nation's best-loved novel of all time. ",
              "url": "http://en.wikipedia.org/wiki/The_Big_Read",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 0.817672
        },
        {
          "@type": "EntitySearchResult",
          "result": {
            "@id": "kg:/m/076vrw4",
            "name": "Standing on the Edge of the Noise",
            "@type": [
              "Movie",
              "TVSeries",
              "Thing"
            ],
            "description": "TV programme",
            "detailedDescription": {
              "articleBody": "Standing on the Edge of the Noise is a unique, intimate look at Oasis performing in their own space, instead of the huge stadium stages on which they are more often seen. The programme includes a mix of classics and new tracks from Dig Out Your Soul. ",
              "url": "http://en.wikipedia.org/wiki/Standing_on_the_Edge_of_the_Noise",
              "license": "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License"
            }
          },
          "resultScore": 0.806576
        }
      ]
    }

## Conversion to RDF

Now, we can of course just parse the JSON object above using Python or test out our
javascript skills, which is actually what makes JSON-LD nice - you can encode these
Semantic Web ideas into an API without forcing developers to know anything about
the [Semantic Web Technology Stack](http://bnode.org/blog/2009/07/08/the-semantic-web-not-a-piece-of-cake),
shown below:

<img src="http://bnode.org/media/2009/07/08/semantic_web_technology_stack.png"> 

To convert to RDF, we use the PyLD library and convert to a format called nquads that
can include an additional URI in each RDF triple that indicates the graph that the
triples belong to. Here there is no such graph, so only ntriples or n3 is output.

```python
normalized = pyld.jsonld.normalize(jsonld, {'algorithm': 'URDNA2015',
                                            'format': 'application/nquads'})
print(normalized)
```

    <http://g.co/kg/g/11cknytgw6> <http://schema.googleapis.com/detailedDescription> _:c14n4 .
    <http://g.co/kg/g/11cknytgw6> <http://schema.org/name> "Cassius &amp; Clay" .
    <http://g.co/kg/g/11cknytgw6> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/g/11cknytgw6> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0264z1w> <http://schema.googleapis.com/detailedDescription> _:c14n35 .
    <http://g.co/kg/m/0264z1w> <http://schema.org/description> "British television show" .
    <http://g.co/kg/m/0264z1w> <http://schema.org/name> "The Dame Edna Experience" .
    <http://g.co/kg/m/0264z1w> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0264z1w> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/02qcfrx> <http://schema.googleapis.com/detailedDescription> _:c14n20 .
    <http://g.co/kg/m/02qcfrx> <http://schema.org/description> "TV show" .
    <http://g.co/kg/m/02qcfrx> <http://schema.org/name> "Spanish Archer" .
    <http://g.co/kg/m/02qcfrx> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/02qcfrx> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/02qcyy2> <http://schema.googleapis.com/detailedDescription> _:c14n21 .
    <http://g.co/kg/m/02qcyy2> <http://schema.org/description> "Australian television program" .
    <http://g.co/kg/m/02qcyy2> <http://schema.org/name> "Footy Classified" .
    <http://g.co/kg/m/02qcyy2> <http://schema.org/url> "http://wwos.ninemsn.com.au/afl/classified/" .
    <http://g.co/kg/m/02qcyy2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/02qcyy2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/02rp2_> <http://schema.googleapis.com/detailedDescription> _:c14n8 .
    <http://g.co/kg/m/02rp2_> <http://schema.org/description> "Television Programme" .
    <http://g.co/kg/m/02rp2_> <http://schema.org/name> "The Big Read" .
    <http://g.co/kg/m/02rp2_> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/02rp2_> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/04q8zth> <http://schema.googleapis.com/detailedDescription> _:c14n25 .
    <http://g.co/kg/m/04q8zth> <http://schema.org/description> "Television Series" .
    <http://g.co/kg/m/04q8zth> <http://schema.org/image> _:c14n1 .
    <http://g.co/kg/m/04q8zth> <http://schema.org/name> "The Californians" .
    <http://g.co/kg/m/04q8zth> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/04q8zth> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0522jn> <http://schema.googleapis.com/detailedDescription> _:c14n29 .
    <http://g.co/kg/m/0522jn> <http://schema.org/description> "American sitcom" .
    <http://g.co/kg/m/0522jn> <http://schema.org/name> "Major Dad" .
    <http://g.co/kg/m/0522jn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0522jn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/06_wvhl> <http://schema.googleapis.com/detailedDescription> _:c14n31 .
    <http://g.co/kg/m/06_wvhl> <http://schema.org/description> "American animated series" .
    <http://g.co/kg/m/06_wvhl> <http://schema.org/image> _:c14n18 .
    <http://g.co/kg/m/06_wvhl> <http://schema.org/name> "Archer" .
    <http://g.co/kg/m/06_wvhl> <http://schema.org/url> "http://www.fxnetworks.com/archer" .
    <http://g.co/kg/m/06_wvhl> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/06_wvhl> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/06w21l8> <http://schema.googleapis.com/detailedDescription> _:c14n24 .
    <http://g.co/kg/m/06w21l8> <http://schema.org/description> "American sitcom" .
    <http://g.co/kg/m/06w21l8> <http://schema.org/image> _:c14n40 .
    <http://g.co/kg/m/06w21l8> <http://schema.org/name> "Meet Corliss Archer" .
    <http://g.co/kg/m/06w21l8> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/06w21l8> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/076vrw4> <http://schema.googleapis.com/detailedDescription> _:c14n19 .
    <http://g.co/kg/m/076vrw4> <http://schema.org/description> "TV programme" .
    <http://g.co/kg/m/076vrw4> <http://schema.org/name> "Standing on the Edge of the Noise" .
    <http://g.co/kg/m/076vrw4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Movie> .
    <http://g.co/kg/m/076vrw4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/076vrw4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/07cggr0> <http://schema.org/description> "TV series" .
    <http://g.co/kg/m/07cggr0> <http://schema.org/name> "Archer (1975)" .
    <http://g.co/kg/m/07cggr0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/07cggr0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/07ch475> <http://schema.googleapis.com/detailedDescription> _:c14n26 .
    <http://g.co/kg/m/07ch475> <http://schema.org/description> "American television miniseries" .
    <http://g.co/kg/m/07ch475> <http://schema.org/name> "Seventh Avenue" .
    <http://g.co/kg/m/07ch475> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Movie> .
    <http://g.co/kg/m/07ch475> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/07ch475> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0863kh> <http://schema.googleapis.com/detailedDescription> _:c14n38 .
    <http://g.co/kg/m/0863kh> <http://schema.org/description> "American drama series" .
    <http://g.co/kg/m/0863kh> <http://schema.org/name> "Storefront Lawyers" .
    <http://g.co/kg/m/0863kh> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0863kh> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0bcr8s> <http://schema.googleapis.com/detailedDescription> _:c14n42 .
    <http://g.co/kg/m/0bcr8s> <http://schema.org/description> "British television programme" .
    <http://g.co/kg/m/0bcr8s> <http://schema.org/name> "Robin Hood" .
    <http://g.co/kg/m/0bcr8s> <http://schema.org/url> "http://www.robin-hood.tv/" .
    <http://g.co/kg/m/0bcr8s> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0bcr8s> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0cv8fbn> <http://schema.googleapis.com/detailedDescription> _:c14n22 .
    <http://g.co/kg/m/0cv8fbn> <http://schema.org/description> "2010 film" .
    <http://g.co/kg/m/0cv8fbn> <http://schema.org/name> "Violet Tendencies" .
    <http://g.co/kg/m/0cv8fbn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Movie> .
    <http://g.co/kg/m/0cv8fbn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0cv8fbn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0gfds00> <http://schema.googleapis.com/detailedDescription> _:c14n6 .
    <http://g.co/kg/m/0gfds00> <http://schema.org/description> "2002 film" .
    <http://g.co/kg/m/0gfds00> <http://schema.org/name> "Jeffrey Archer: The Truth" .
    <http://g.co/kg/m/0gfds00> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Movie> .
    <http://g.co/kg/m/0gfds00> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0gfds00> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0hzp2zq> <http://schema.googleapis.com/detailedDescription> _:c14n5 .
    <http://g.co/kg/m/0hzp2zq> <http://schema.org/description> "Television Program" .
    <http://g.co/kg/m/0hzp2zq> <http://schema.org/name> "Animation Salvation" .
    <http://g.co/kg/m/0hzp2zq> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0hzp2zq> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0k2dng7> <http://schema.googleapis.com/detailedDescription> _:c14n33 .
    <http://g.co/kg/m/0k2dng7> <http://schema.org/description> "TV Show" .
    <http://g.co/kg/m/0k2dng7> <http://schema.org/name> "Help! My Supply Teacher's Magic" .
    <http://g.co/kg/m/0k2dng7> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0k2dng7> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0kfwmt7> <http://schema.googleapis.com/detailedDescription> _:c14n17 .
    <http://g.co/kg/m/0kfwmt7> <http://schema.org/description> "1978 film" .
    <http://g.co/kg/m/0kfwmt7> <http://schema.org/name> "The Pirate" .
    <http://g.co/kg/m/0kfwmt7> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Movie> .
    <http://g.co/kg/m/0kfwmt7> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0kfwmt7> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    <http://g.co/kg/m/0y5gfz0> <http://schema.googleapis.com/detailedDescription> _:c14n12 .
    <http://g.co/kg/m/0y5gfz0> <http://schema.org/description> "Television film" .
    <http://g.co/kg/m/0y5gfz0> <http://schema.org/name> "Roald Dahl's Esio Trot" .
    <http://g.co/kg/m/0y5gfz0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Movie> .
    <http://g.co/kg/m/0y5gfz0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/TVSeries> .
    <http://g.co/kg/m/0y5gfz0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Thing> .
    _:c14n0 <http://schema.googleapis.com/resultScore> "1.2145683E1"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n0 <http://schema.org/result> <http://g.co/kg/m/06w21l8> .
    _:c14n0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n1 <http://schema.org/contentUrl> "http://t3.gstatic.com/images?q=tbn:ANd9GcSQ0FvOFyPFq3qLlZsbr4UTcIef_WZFGTqQfVum3VzCxpykLMhK" .
    _:c14n1 <http://schema.org/url> "http://en.wikipedia.org/wiki/The_Californians_(TV_series)" .
    _:c14n10 <http://schema.googleapis.com/resultScore> "1.142771E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n10 <http://schema.org/result> <http://g.co/kg/m/0522jn> .
    _:c14n10 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n11 <http://schema.googleapis.com/resultScore> "8.065760000000000E-01"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n11 <http://schema.org/result> <http://g.co/kg/m/076vrw4> .
    _:c14n11 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n12 <http://schema.org/articleBody> "Roald Dahl's Esio Trot is a British comedy television film that was first broadcast as part of BBC One's 2014 Christmas programming. " .
    _:c14n12 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n12 <http://schema.org/url> "http://en.wikipedia.org/wiki/Roald_Dahl's_Esio_Trot" .
    _:c14n13 <http://schema.googleapis.com/resultScore> "8.176720000000000E-01"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n13 <http://schema.org/result> <http://g.co/kg/m/02rp2_> .
    _:c14n13 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n14 <http://schema.googleapis.com/resultScore> "1.123545E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n14 <http://schema.org/result> <http://g.co/kg/m/0264z1w> .
    _:c14n14 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n15 <http://schema.org/itemListElement> _:c14n0 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n10 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n11 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n13 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n14 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n16 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n2 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n23 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n27 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n28 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n3 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n30 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n32 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n34 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n36 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n37 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n39 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n41 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n7 .
    _:c14n15 <http://schema.org/itemListElement> _:c14n9 .
    _:c14n15 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/ItemList> .
    _:c14n16 <http://schema.googleapis.com/resultScore> "1.573618E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n16 <http://schema.org/result> <http://g.co/kg/m/0bcr8s> .
    _:c14n16 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n17 <http://schema.org/articleBody> "The Pirate is a 1978 American TV movie directed by Ken Annakin. It is based on the novel with the same title written by Harold Robbins.\nIt was broadcast by ABC in two parts November 21–22, 1978." .
    _:c14n17 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n17 <http://schema.org/url> "http://en.wikipedia.org/wiki/The_Pirate_(1978_film)" .
    _:c14n18 <http://schema.org/contentUrl> "http://t3.gstatic.com/images?q=tbn:ANd9GcQwUXmJt_InhAr39HEyyv8l4CIiom0RvTvNYcf-JoCN8cpXOyon" .
    _:c14n18 <http://schema.org/license> "http://creativecommons.org/licenses/by/2.0" .
    _:c14n18 <http://schema.org/url> "https://en.wikipedia.org/wiki/Archer_(TV_series)" .
    _:c14n19 <http://schema.org/articleBody> "Standing on the Edge of the Noise is a unique, intimate look at Oasis performing in their own space, instead of the huge stadium stages on which they are more often seen. The programme includes a mix of classics and new tracks from Dig Out Your Soul. " .
    _:c14n19 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n19 <http://schema.org/url> "http://en.wikipedia.org/wiki/Standing_on_the_Edge_of_the_Noise" .
    _:c14n2 <http://schema.googleapis.com/resultScore> "1.371247E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n2 <http://schema.org/result> <http://g.co/kg/m/0hzp2zq> .
    _:c14n2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n20 <http://schema.org/articleBody> "Spanish Archer was a talent show hosted by Rhodri Williams and occasionally Ruth Madoc. It was produced by L!VE TV and filmed at the station's headquarters at Canary Wharf in London.\n" .
    _:c14n20 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n20 <http://schema.org/url> "http://en.wikipedia.org/wiki/Spanish_Archer" .
    _:c14n21 <http://schema.org/articleBody> "Footy Classified, is an Australian television program broadcast on the Nine Network which discusses pressing issues relating to AFL football. It debuted on Monday 2 April 2007. " .
    _:c14n21 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n21 <http://schema.org/url> "http://en.wikipedia.org/wiki/Footy_Classified" .
    _:c14n22 <http://schema.org/articleBody> "Violet Tendencies is a 2010 romantic comedy film directed by Casper Andreas, written by Jesse Archer, and starring Mindy Cohn and Marcus Patrick. " .
    _:c14n22 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n22 <http://schema.org/url> "http://en.wikipedia.org/wiki/Violet_Tendencies" .
    _:c14n23 <http://schema.googleapis.com/resultScore> "8.710420000000000E-01"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n23 <http://schema.org/result> <http://g.co/kg/m/0863kh> .
    _:c14n23 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n24 <http://schema.org/articleBody> "Meet Corliss Archer is an American sitcom that aired in syndication from April to December 1954. The series stars Ann Baker in the title role. " .
    _:c14n24 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n24 <http://schema.org/url> "http://en.wikipedia.org/wiki/Meet_Corliss_Archer_(TV_series)" .
    _:c14n25 <http://schema.org/articleBody> "The Californians is a 54-episode half-hour Western television series, set in the San Francisco gold rush of the 1850s, which aired on NBC from September 24, 1957, to May 26, 1959. " .
    _:c14n25 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n25 <http://schema.org/url> "http://en.wikipedia.org/wiki/The_Californians_(TV_series)" .
    _:c14n26 <http://schema.org/articleBody> "Seventh Avenue is a six-part American television miniseries broadcast in 1977. It is based on the 1967 Norman Bogner novel of the same name. " .
    _:c14n26 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n26 <http://schema.org/url> "http://en.wikipedia.org/wiki/Seventh_Avenue_(miniseries)" .
    _:c14n27 <http://schema.googleapis.com/resultScore> "9.301340000000000E-01"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n27 <http://schema.org/result> <http://g.co/kg/m/07ch475> .
    _:c14n27 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n28 <http://schema.googleapis.com/resultScore> "1.1167856E1"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n28 <http://schema.org/result> <http://g.co/kg/m/0gfds00> .
    _:c14n28 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n29 <http://schema.org/articleBody> "Major Dad is an American sitcom created by Richard C. Okie and John G. Stephens, developed by Earl Pomerantz, that originally ran from 1989 to 1993 on CBS, starring Gerald McRaney as Major John D. MacGillis and Shanna Reed as his wife Polly. " .
    _:c14n29 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n29 <http://schema.org/url> "http://en.wikipedia.org/wiki/Major_Dad" .
    _:c14n3 <http://schema.googleapis.com/resultScore> "9.632230000000001E-01"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n3 <http://schema.org/result> <http://g.co/kg/m/0y5gfz0> .
    _:c14n3 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n30 <http://schema.googleapis.com/resultScore> "1.6060818E1"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n30 <http://schema.org/result> <http://g.co/kg/m/02qcfrx> .
    _:c14n30 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n31 <http://schema.org/articleBody> "Archer is an American adult animated television series created by Adam Reed for the FX network. A preview of the series aired on September 17, 2009. The first season premiered on January 14, 2010. " .
    _:c14n31 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n31 <http://schema.org/url> "http://en.wikipedia.org/wiki/Archer_(TV_series)" .
    _:c14n32 <http://schema.googleapis.com/resultScore> "1.225814E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n32 <http://schema.org/result> <http://g.co/kg/m/0kfwmt7> .
    _:c14n32 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n33 <http://schema.org/articleBody> "Help! My Supply Teacher's Magic is a CBBC show which shows magicians in schools, tricking children into thinking they are supply teachers. It is presented by Iain Stirling. " .
    _:c14n33 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n33 <http://schema.org/url> "http://en.wikipedia.org/wiki/Help!_My_Supply_Teacher's_Magic" .
    _:c14n34 <http://schema.googleapis.com/resultScore> "1.043589E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n34 <http://schema.org/result> <http://g.co/kg/m/04q8zth> .
    _:c14n34 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n35 <http://schema.org/articleBody> "The Dame Edna Experience is a British television comedy talk-show hosted by Dame Edna Everage. It ran for twelve regular episodes on ITV, plus two Christmas specials." .
    _:c14n35 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n35 <http://schema.org/url> "http://en.wikipedia.org/wiki/The_Dame_Edna_Experience" .
    _:c14n36 <http://schema.googleapis.com/resultScore> "4.3221546E1"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n36 <http://schema.org/result> <http://g.co/kg/m/06_wvhl> .
    _:c14n36 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n37 <http://schema.googleapis.com/resultScore> "8.711719999999999E-01"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n37 <http://schema.org/result> <http://g.co/kg/m/0k2dng7> .
    _:c14n37 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n38 <http://schema.org/articleBody> "Storefront Lawyers is an American legal drama that ran from September 1970 to April 1971 on CBS. The series stars Robert Foxworth, Sheila Larken, David Arkin, and A Martinez." .
    _:c14n38 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n38 <http://schema.org/url> "http://en.wikipedia.org/wiki/Storefront_Lawyers" .
    _:c14n39 <http://schema.googleapis.com/resultScore> "1.50758E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n39 <http://schema.org/result> <http://g.co/kg/m/0cv8fbn> .
    _:c14n39 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n4 <http://schema.org/articleBody> "Cassius &amp; Clay is an upcoming American animated television series created by Adam Reed to be aired in 2016 alongside Archer on FXX. The show follows two women, Cassius and Clay living as bandits in a futuristic, post-apocalyptic America. " .
    _:c14n4 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n4 <http://schema.org/url> "http://en.wikipedia.org/wiki/Cassius_%26_Clay" .
    _:c14n40 <http://schema.org/contentUrl> "http://t2.gstatic.com/images?q=tbn:ANd9GcRqPkGi1_Rselb-ijqy_-5of6WsEkhDmoU036ZsvXBS83XZsWGb" .
    _:c14n40 <http://schema.org/url> "http://en.wikipedia.org/wiki/Meet_Corliss_Archer_(TV_series)" .
    _:c14n41 <http://schema.googleapis.com/resultScore> "1.4106644E1"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n41 <http://schema.org/result> <http://g.co/kg/m/07cggr0> .
    _:c14n41 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n42 <http://schema.org/articleBody> "Robin Hood is a British television programme, produced by independent production company Tiger Aspect Productions for BBC One, with co-funding from the BBC America cable television channel in the United States. " .
    _:c14n42 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n42 <http://schema.org/url> "http://en.wikipedia.org/wiki/Robin_Hood_(2006_TV_series)" .
    _:c14n5 <http://schema.org/articleBody> "Animation Salvation is an Australian television Sunday night-time animation block aired on Fox8 on Sunday 7:30 pm to 10:30 pm from 7 March 2010." .
    _:c14n5 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n5 <http://schema.org/url> "http://en.wikipedia.org/wiki/Animation_Salvation" .
    _:c14n6 <http://schema.org/articleBody> "Jeffrey Archer: The Truth is a 2002 BBC satirical comedy drama on the life of Jeffrey Archer, with the title role played by Damian Lewis. Its duration was 90 minutes and its premiere occurred on 1 December 2002. It was written and directed by Guy Jenkin." .
    _:c14n6 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n6 <http://schema.org/url> "http://en.wikipedia.org/wiki/Jeffrey_Archer:_The_Truth" .
    _:c14n7 <http://schema.googleapis.com/resultScore> "1.105602E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n7 <http://schema.org/result> <http://g.co/kg/m/02qcyy2> .
    _:c14n7 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .
    _:c14n8 <http://schema.org/articleBody> "The Big Read was a survey on books carried out by the BBC in the United Kingdom in 2003, where over three quarters of a million votes were received from the British public to find the nation's best-loved novel of all time. " .
    _:c14n8 <http://schema.org/license> "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" .
    _:c14n8 <http://schema.org/url> "http://en.wikipedia.org/wiki/The_Big_Read" .
    _:c14n9 <http://schema.googleapis.com/resultScore> "1.67782E0"^^<http://www.w3.org/2001/XMLSchema#double> .
    _:c14n9 <http://schema.org/result> <http://g.co/kg/g/11cknytgw6> .
    _:c14n9 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.googleapis.com/EntitySearchResult> .

## Parse the RDF into a Queryable Graph

Next, we use the RDFLib library to parse this N3 data into a graph that we can then
serialize into any of the RDF formats. In this case, I show an example of serializing
into the Turtle format that is a bit easier to read. Note that RDF does not maintain any
order of the triples that are output, so we no longer have our show listed as the first
element. Also, you will see that the `@context` section is gone, being replaced
with `@prefix` declarations for identifying the namespace from which terms come.

```python
g = rdflib.Graph()
g.parse(data=normalized, format='n3')
print(g.serialize(format='turtle'))
```

    @prefix ns1: <http://schema.org/> .
    @prefix ns2: <http://schema.googleapis.com/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    <http://g.co/kg/g/11cknytgw6> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Cassius &amp; Clay is an upcoming American animated television series created by Adam Reed to be aired in 2016 alongside Archer on FXX. The show follows two women, Cassius and Clay living as bandits in a futuristic, post-apocalyptic America. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Cassius_%26_Clay" ] ;
        ns1:name "Cassius &amp; Clay" .
    
    <http://g.co/kg/m/0264z1w> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "The Dame Edna Experience is a British television comedy talk-show hosted by Dame Edna Everage. It ran for twelve regular episodes on ITV, plus two Christmas specials." ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/The_Dame_Edna_Experience" ] ;
        ns1:description "British television show" ;
        ns1:name "The Dame Edna Experience" .
    
    <http://g.co/kg/m/02qcfrx> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody """Spanish Archer was a talent show hosted by Rhodri Williams and occasionally Ruth Madoc. It was produced by L!VE TV and filmed at the station's headquarters at Canary Wharf in London.
    """ ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Spanish_Archer" ] ;
        ns1:description "TV show" ;
        ns1:name "Spanish Archer" .
    
    <http://g.co/kg/m/02qcyy2> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Footy Classified, is an Australian television program broadcast on the Nine Network which discusses pressing issues relating to AFL football. It debuted on Monday 2 April 2007. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Footy_Classified" ] ;
        ns1:description "Australian television program" ;
        ns1:name "Footy Classified" ;
        ns1:url "http://wwos.ninemsn.com.au/afl/classified/" .
    
    <http://g.co/kg/m/02rp2_> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "The Big Read was a survey on books carried out by the BBC in the United Kingdom in 2003, where over three quarters of a million votes were received from the British public to find the nation's best-loved novel of all time. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/The_Big_Read" ] ;
        ns1:description "Television Programme" ;
        ns1:name "The Big Read" .
    
    <http://g.co/kg/m/04q8zth> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "The Californians is a 54-episode half-hour Western television series, set in the San Francisco gold rush of the 1850s, which aired on NBC from September 24, 1957, to May 26, 1959. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/The_Californians_(TV_series)" ] ;
        ns1:description "Television Series" ;
        ns1:image [ ns1:contentUrl "http://t3.gstatic.com/images?q=tbn:ANd9GcSQ0FvOFyPFq3qLlZsbr4UTcIef_WZFGTqQfVum3VzCxpykLMhK" ;
                ns1:url "http://en.wikipedia.org/wiki/The_Californians_(TV_series)" ] ;
        ns1:name "The Californians" .
    
    <http://g.co/kg/m/0522jn> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Major Dad is an American sitcom created by Richard C. Okie and John G. Stephens, developed by Earl Pomerantz, that originally ran from 1989 to 1993 on CBS, starring Gerald McRaney as Major John D. MacGillis and Shanna Reed as his wife Polly. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Major_Dad" ] ;
        ns1:description "American sitcom" ;
        ns1:name "Major Dad" .
    
    <http://g.co/kg/m/06_wvhl> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Archer is an American adult animated television series created by Adam Reed for the FX network. A preview of the series aired on September 17, 2009. The first season premiered on January 14, 2010. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Archer_(TV_series)" ] ;
        ns1:description "American animated series" ;
        ns1:image [ ns1:contentUrl "http://t3.gstatic.com/images?q=tbn:ANd9GcQwUXmJt_InhAr39HEyyv8l4CIiom0RvTvNYcf-JoCN8cpXOyon" ;
                ns1:license "http://creativecommons.org/licenses/by/2.0" ;
                ns1:url "https://en.wikipedia.org/wiki/Archer_(TV_series)" ] ;
        ns1:name "Archer" ;
        ns1:url "http://www.fxnetworks.com/archer" .
    
    <http://g.co/kg/m/06w21l8> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Meet Corliss Archer is an American sitcom that aired in syndication from April to December 1954. The series stars Ann Baker in the title role. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Meet_Corliss_Archer_(TV_series)" ] ;
        ns1:description "American sitcom" ;
        ns1:image [ ns1:contentUrl "http://t2.gstatic.com/images?q=tbn:ANd9GcRqPkGi1_Rselb-ijqy_-5of6WsEkhDmoU036ZsvXBS83XZsWGb" ;
                ns1:url "http://en.wikipedia.org/wiki/Meet_Corliss_Archer_(TV_series)" ] ;
        ns1:name "Meet Corliss Archer" .
    
    <http://g.co/kg/m/076vrw4> a ns1:Movie,
            ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Standing on the Edge of the Noise is a unique, intimate look at Oasis performing in their own space, instead of the huge stadium stages on which they are more often seen. The programme includes a mix of classics and new tracks from Dig Out Your Soul. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Standing_on_the_Edge_of_the_Noise" ] ;
        ns1:description "TV programme" ;
        ns1:name "Standing on the Edge of the Noise" .
    
    <http://g.co/kg/m/07cggr0> a ns1:TVSeries,
            ns1:Thing ;
        ns1:description "TV series" ;
        ns1:name "Archer (1975)" .
    
    <http://g.co/kg/m/07ch475> a ns1:Movie,
            ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Seventh Avenue is a six-part American television miniseries broadcast in 1977. It is based on the 1967 Norman Bogner novel of the same name. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Seventh_Avenue_(miniseries)" ] ;
        ns1:description "American television miniseries" ;
        ns1:name "Seventh Avenue" .
    
    <http://g.co/kg/m/0863kh> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Storefront Lawyers is an American legal drama that ran from September 1970 to April 1971 on CBS. The series stars Robert Foxworth, Sheila Larken, David Arkin, and A Martinez." ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Storefront_Lawyers" ] ;
        ns1:description "American drama series" ;
        ns1:name "Storefront Lawyers" .
    
    <http://g.co/kg/m/0bcr8s> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Robin Hood is a British television programme, produced by independent production company Tiger Aspect Productions for BBC One, with co-funding from the BBC America cable television channel in the United States. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Robin_Hood_(2006_TV_series)" ] ;
        ns1:description "British television programme" ;
        ns1:name "Robin Hood" ;
        ns1:url "http://www.robin-hood.tv/" .
    
    <http://g.co/kg/m/0cv8fbn> a ns1:Movie,
            ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Violet Tendencies is a 2010 romantic comedy film directed by Casper Andreas, written by Jesse Archer, and starring Mindy Cohn and Marcus Patrick. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Violet_Tendencies" ] ;
        ns1:description "2010 film" ;
        ns1:name "Violet Tendencies" .
    
    <http://g.co/kg/m/0gfds00> a ns1:Movie,
            ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Jeffrey Archer: The Truth is a 2002 BBC satirical comedy drama on the life of Jeffrey Archer, with the title role played by Damian Lewis. Its duration was 90 minutes and its premiere occurred on 1 December 2002. It was written and directed by Guy Jenkin." ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Jeffrey_Archer:_The_Truth" ] ;
        ns1:description "2002 film" ;
        ns1:name "Jeffrey Archer: The Truth" .
    
    <http://g.co/kg/m/0hzp2zq> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Animation Salvation is an Australian television Sunday night-time animation block aired on Fox8 on Sunday 7:30 pm to 10:30 pm from 7 March 2010." ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Animation_Salvation" ] ;
        ns1:description "Television Program" ;
        ns1:name "Animation Salvation" .
    
    <http://g.co/kg/m/0k2dng7> a ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Help! My Supply Teacher's Magic is a CBBC show which shows magicians in schools, tricking children into thinking they are supply teachers. It is presented by Iain Stirling. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Help!_My_Supply_Teacher's_Magic" ] ;
        ns1:description "TV Show" ;
        ns1:name "Help! My Supply Teacher's Magic" .
    
    <http://g.co/kg/m/0kfwmt7> a ns1:Movie,
            ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody """The Pirate is a 1978 American TV movie directed by Ken Annakin. It is based on the novel with the same title written by Harold Robbins.
    It was broadcast by ABC in two parts November 21–22, 1978.""" ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/The_Pirate_(1978_film)" ] ;
        ns1:description "1978 film" ;
        ns1:name "The Pirate" .
    
    <http://g.co/kg/m/0y5gfz0> a ns1:Movie,
            ns1:TVSeries,
            ns1:Thing ;
        ns2:detailedDescription [ ns1:articleBody "Roald Dahl's Esio Trot is a British comedy television film that was first broadcast as part of BBC One's 2014 Christmas programming. " ;
                ns1:license "https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License" ;
                ns1:url "http://en.wikipedia.org/wiki/Roald_Dahl's_Esio_Trot" ] ;
        ns1:description "Television film" ;
        ns1:name "Roald Dahl's Esio Trot" .
    
    [] a ns1:ItemList ;
        ns1:itemListElement [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.214568e+01 ;
                ns1:result <http://g.co/kg/m/06w21l8> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.142771e+00 ;
                ns1:result <http://g.co/kg/m/0522jn> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 8.06576e-01 ;
                ns1:result <http://g.co/kg/m/076vrw4> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 8.17672e-01 ;
                ns1:result <http://g.co/kg/m/02rp2_> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.123545e+00 ;
                ns1:result <http://g.co/kg/m/0264z1w> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.573618e+00 ;
                ns1:result <http://g.co/kg/m/0bcr8s> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.371247e+00 ;
                ns1:result <http://g.co/kg/m/0hzp2zq> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 8.71042e-01 ;
                ns1:result <http://g.co/kg/m/0863kh> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 9.30134e-01 ;
                ns1:result <http://g.co/kg/m/07ch475> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.116786e+01 ;
                ns1:result <http://g.co/kg/m/0gfds00> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 9.63223e-01 ;
                ns1:result <http://g.co/kg/m/0y5gfz0> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.606082e+01 ;
                ns1:result <http://g.co/kg/m/02qcfrx> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.225814e+00 ;
                ns1:result <http://g.co/kg/m/0kfwmt7> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.043589e+00 ;
                ns1:result <http://g.co/kg/m/04q8zth> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 4.322155e+01 ;
                ns1:result <http://g.co/kg/m/06_wvhl> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 8.71172e-01 ;
                ns1:result <http://g.co/kg/m/0k2dng7> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.50758e+00 ;
                ns1:result <http://g.co/kg/m/0cv8fbn> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.410664e+01 ;
                ns1:result <http://g.co/kg/m/07cggr0> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.105602e+00 ;
                ns1:result <http://g.co/kg/m/02qcyy2> ],
            [ a ns2:EntitySearchResult ;
                ns2:resultScore 1.67782e+00 ;
                ns1:result <http://g.co/kg/g/11cknytgw6> ] .

## Querying the Knowlege Graph with SPARQL

Now that we have our graph loaded into RDFLib, we can issue a SPARQL query against it.
Now this query is only being issued againts the results we returned from the API and not
the entire Knowledge Graph, but it will give you a flavor for the query syntax.

To break this down a little, We have four keywords to parse: SELECT, WHERE, ORDER BY
DESC, and LIMIT. SELECT is simuilar to SQL and contains our, unituitively named, '
Projection' criteria or what we want returned to us as a table. The real meat is in the
WHERE clause that provides our 'Selection' criteria using graph pattern matching on the
triples in the graph. Here I am first looking up the the score of all the search
results, then gathering the name, url, and an associated image. ORDER BY DESC allows us
to sort our results with the highest score at the top and LIMIT just grabs the top
results.

```python
q = """SELECT ?name ?description ?url ?score ?image
       WHERE {?b a ns2:EntitySearchResult ;
                 ns2:resultScore ?score ;
                 ns1:result ?result .
              ?result ns1:description ?description ;
                      ns1:name ?name ;
                      ns1:url  ?url ;
                      ns1:image ?b_image .
              ?b_image ns1:contentUrl ?image .}
       ORDER BY DESC(?score)
       LIMIT 1
"""
print(g.query(q).serialize(format='csv'))
```

    name,description,url,score,image
    Archer,American animated series,http://www.fxnetworks.com/archer,43.221546,http://t3.gstatic.com/images?q=tbn:ANd9GcQwUXmJt_InhAr39HEyyv8l4CIiom0RvTvNYcf-JoCN8cpXOyon

## Summary

So here I've shown how you can get started with converting data from the knowledge graph
into RDF and query it using the SPARQL query language. This is only scratching the
surface, as the real power of these technologies are to integrate data from external
sources. For example, as a next step we may want to query dbpedia using the URL we
acquired here to gain additional information about actors or episodes and further
explore the information retrieved as linked data. Of course here we are only looking at
a TV Show, but as additional schema.org types are supported by the Knowledge Grpah API,
I imagine that there will be links and hooks that enable searching across Drug databases
and interoperating the data retrieved from Google, with more traditional sources of
Linked Data from bioinformatics databases and forming a Giant Global Graph of linked
data.

<img src="http://lod-cloud.net/versions/2014-08-30/lod-cloud.svg">

```python

```
