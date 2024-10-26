# insurance_claim_process
Dockerize, FastAPI, python, pandas, sqlite, sqlAlchemy ORM, claim process, and Top provider list

## Task
Your task is to create a **_dockerized_** service, **claim_process**  to process claims. 

## Requirements
1. **claim_process** transforms a JSON payload representing a single claim input with multiple lines and stores it into a RDB.
   - An example input (in CSV format) - *claim.csv* is provided. Note that the names are not consistent in capitalization.
2. **claim_process** generates a unique id per claim.
3. **claim_process** computes the *“net fee”* as a result per the formula below.
*“net fee” = “provider fees” + “member coinsurance” + “member copay” - “Allowed fees”* (note again that the names are not consistent in capitalization).
4. A downstream service, **payments**, will consume *“net fee”* computed by **claim_process**.
5. Implement an endpoint that returns the top 10 provider_npis by net fees generated. The endpoint should be optimized for performance, and the you should explain the data structure and algorithm used to compute the top 10 provider_npis. It would be good to have a rate limiter to this api probably 10 req/min.

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
