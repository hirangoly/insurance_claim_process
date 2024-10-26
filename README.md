# insurance_claim_process
Dockerize, FastAPI, python, pandas, sqlite, sqlAlchemy ORM, claim process, and Top provider list

1. ## Upstream Service (CSV Claims Processing): claims_process.py
Read the claims data from a CSV file.
Calculate the net fee for each claim.
Send the processed data to the downstream FastAPI service for storage.

2. ## Downstream Service (FastAPI + SQLite): payments.py
Receive the processed claims data from the upstream service.
Store the data in an SQLite database using SQLAlchemy.
Provide an API to retrieve the top 10 providers based on the total net fees.

3. ## Dockerizing Both Services:
Upstream has a claim_process.py, requirements.txt, Dockerfile
Downstream has payments.py, requirements.txt, Dockerfile
Build and run individual images and test output

## What's missing in the solution due to time constraint:
Input Validation
Docker Compose 
