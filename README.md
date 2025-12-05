# Data Normalization for Brazilian Open Data

This is code for getting and ingesting data from different open data sources and importing them into databases.

## Databases

### SQLite

A extremely popular database, this is the database used for relational data. The reasons are
* Popularity: this platform is extremely familiar to a very large number of people and has a great tooling ecosystem
* Portability: the database is stored as a single ".db" file, which makes it trivial to share with others.

### Neo4j

A graph database written in Java. This is used to more easily look at relationships between data