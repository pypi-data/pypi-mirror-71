## geoparsepy project

geoparsepy is a Python geoparsing library that will extract and disambiguate locations from text. It uses a local OpenStreetMap database which allows very high and unlimited geoparsing throughput, unlike approaches that use a third-party geocoding service (e.g.  Google Geocoding API).

Geoparsing is based on named entity matching against OpenStreetMap (OSM) locations. All locations with names that match tokens will be selected from a target text sentence. This will result in a set of OSM locations, all with a common name or name variant, for each token in the text. Geoparsing included the following features :
* **token expansion** using location name variants (i.e. OSM multi-lingual names, short names and acronyms)
* **token expansion** using location type variants (e.g. street, st.)
* **token filtering** of single token location names against WordNet (non-nouns), language specific stoplists and peoples first names (nltk.corpus.names.words()) to reduce false positive matches
* **prefix checking** when matching in case a first name prefixes a location token(s) to avoid matching peoples full names as locations (e.g. Victoria Derbyshire != Derbyshire)

Location disambiguation is the process of choosing which of a set of possible OSM locations, all with the same name, is the best match. Location disambiguation is based on an evidential approach, with evidential features detailed below in order of importance:
* **token subsumption**, rejecting smaller phrases over larger ones (e.g. 'New York' will prefer [New York, USA] to [York, UK])
* **nearby parent region**, preferring locations with a parent region also appearing within a semantic distance (e.g. 'New York in USA' will prefer [New York, USA] to [New York, BO, Sierra Leone])
* **nearby locations**, preferring locations with closeby or overlapping locations within a semantic distance (e.g. 'London St and Commercial Road' will select from road name choices with the same name based on spatial proximity)
* **nearby geotag**, preferring locations that are closeby or overlapping a geotag
* **general before specific**, rejecting locations with a higher admin level (or no admin level at all) compared to locations with a lower admin level (e.g. 'New York' will prefer [New York, USA] to [New York, BO, Sierra Leone]

Currently the following languages are supported:
* English, French, German, Italian, Portuguese, Russian, Ukrainian
* All other languages will work but there will be no language specific token expansion available

geoparsepy works with Python 3.7 and has been tested on Windows 10, Ubuntu 18.04 LTS.

This geoparsing algorithm uses a large memory footprint (e.g. 12 Gbytes RAM for global cities), RAM size proportional to the number of cached locations, to maximize matching speed. It can be naively parallelized, with multiple geoparse processes loaded with different sets of locations and the geoparse results aggregated in a last process where location disambiguation is applied. This approach has been validated across an APACHE Storm cluster.

Feature suggestions and/or bug reports can be sent to {sem03}@soton.ac.uk. We do not however offer any software support beyond the examples and API documentation already provided.

The software is copyright 2020 University of Southampton. It was created over a multi-year period under EU FP7 projects TRIDEC (258723), REVEAL (610928), InnovateUK project LPLP (104875) and ESRC project FloraGuard (ES/R003254/1). This software can only be used for research, education or evaluation purposes. A free commercial license is available on request to {sem03}@soton.ac.uk. The University of Southampton is open to discussions regarding collaboration in future research projects relating to this work.


## Scientific publications

Middleton, S.E. Middleton, L. Modafferi, S. "Real-time Crisis Mapping of Natural Disasters using Social Media", Intelligent Systems, IEEE , vol.29, no.2, pp.9,17, Mar.-Apr. 2014

Middleton, S.E. Krivcovs, V. "Geoparsing and Geosemantics for Social Media: Spatio-Temporal Grounding of Content Propagating Rumours to support Trust and Veracity Analysis during Breaking News", ACM Transactions on Information Systems (TOIS), 34, 3, Article 16 (April 2016), 26 pages. DOI=10.1145/2842604 

Middleton, S.E. Kordopatis-Zilos, G. Papadopoulos, S. Kompatsiaris, Y. "Location Extraction from Social Media: Geoparsing, Location Disambiguation, and Geotagging", ACM Transactions on Information Systems (TOIS) 36, 4, Article 40 (June 2018), 27 pages. DOI: https://doi.org/10.1145/3202662. Presented at SIGIR 2019

A benchmark geoparse dataset is also available for free from the University of Southampton on request via email to {sem03}@soton.ac.uk


## geoparsepy user documentation

<https://github.com/stuartemiddleton/geoparsepy>

## geoparsepy license

<https://github.com/stuartemiddleton/geoparsepy/blob/master/LICENSE.txt>


## Python libs needed (earlier versions may be suitable but are untested)

```
Python libs: psycopg2 >= 2.8, nltk >= 3.4, numpy >= 1.18, shapely >= 1.6, setuptools >= 46
Database: PostgreSQL >= 11.3, PostGIS >= 2.5
```

