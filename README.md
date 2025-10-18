# Git setup
In terminal, clone the repository into local with:

git clone git@github.com:MarvinMui/jubilant-computing-machine.git

or download zip and unzip

Once installed, install libraries in terminal with:

pip install -r requirements.txt

then run the main.py either with IDE or with

python main.py

# Usage

Here are a few examples of API requests that can be made to the application through terminal


__Health check__

*check if the application is up and running*

curl http://127.0.0.1:5000


__Ingest__

*first step to do, run this to spin up the duckdb database and load in data from the preset JSON file I created with*
*example records*

curl -X POST http://127.0.0.1:5000/ingest \
     -F "file=@data/test/hardware.json"


__Data__

*basic request to check all the records in a table. if you run this after the previous ingesting request*
*you should see all the json records loaded into the database*

curl http://127.0.0.1:5000/data

curl "http://127.0.0.1:5000/data?table=devices"


__Reset__

*clears all the records in the tables, mainly used for development*

curl -X POST http://127.0.0.1:5000/reset


__Natural langauge AI query__

*basic implementation of AI query with natural spoken words as a mockup. This would later be down with an api key to*
*openAi but i thought it would be outside of the scope of this project*
*the following queries are the two that are accepted currently with the mock:*
*Which users have no encryption?*
*Which users have a macos?*

curl -X POST http://127.0.0.1:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "Which users have no encryption?"}'

curl -X POST http://127.0.0.1:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "Which users have a macos?"}'



# Model, Database, Architecture Overview

Flask

Duckdb

pandas dataframe


The system uses a modular Flask server application backend with a DuckDB local database for lightweight, serverless data
management. It also very easily integrates with python and allows direct SQL queries on a local file without a server as
a separate service, all making it simple to implement quickly. This would be a close mimic of a real world client application,
database server architecture. Uploaded JSON data is ingested with Pandas for preprocessing,
normalized using AI field standardization, and then stored in relational tables with a predefined schema.

For the purpose of this assessment, I elected to implement a mock AI to handle a few exemplary natural language queries,
mapping simple user requests to SQL queries for retrieval as a simple but extensible feature for a MVP.
I used Flask for fast spinup of a RESTful API while DuckDB avoids external DB dependencies and Pandas + AI
normalization is a basic utilization of intelligent data cleaning and normalization.

Data cleaning:
Deduplication is handled with primary key constraints of the schema. Null values are handled by converting to string
values representing "unknown". The value normalization is handled with AI described later. Unstructured Json field names
are mapped to standardized schema field with a simple string dictionary, but can also be handled like the field values
in the AI section.

Given a more fleshed out implementation of a project like this, these would be a planned next steps for data cleaning and
integration

## Planned steps
Normalization:

Enrich missing or inconsistent fields

Merge and reconcile conflicting attributes (device names, IPs)

Detect anomalies or configuration drift

Suggest data corrections or improvements


Data Quality:

Correct data typing and entry inconsistencies

Enforce referential integrity and schema conformity

Identify and resolve duplicate or contradictory records

Apply heuristic filters for noisy or invalid inputs

More robust correction of unstandardized or misapplied field conventions


Data analytics

Generate basic statistics (e.g., most common OS, device counts)

Implement interactive dashboards, search functions, data visualisation

# AI usage description
sentence transformer


This project employs a SentenceTransformers to vectorize the short string values of the json fields and categorize the
inconsistent field values into field values that are allowed. For example OS names and locations are
semantically compared to the preset "canonical" values by converting them to word embedding vectors and their relatedness is measured
using cosine similarity. The closest correct value is chosen to replace it, and the standardized value is ingested.

This method allows flexible handling of noisy or variant data. For example, mapping “Win10 Pro” and
“Windows 10 Professional” to “Windows 10 Pro.” By using this AI vectorization and domain similarity measuring instead of
fixed rules, the system generalizes well to messy data and reduces manual standardization logic. This is both easier to
implement, generalizable and accurate without seeing all outliers beforehand.