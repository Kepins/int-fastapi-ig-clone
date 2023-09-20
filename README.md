# Simplified clone of Instagram created using FastAPI.

## Requirements:
1. user can create account
2. user can upload photo with description
3. user can see photos of other users
4. user can like photo of other user

## Running tests
```
docker compose --env-file=test.env -f=docker-compose-test.yml up --build --abort-on-container-exit && docker compose -f=docker-compose-test.yml rm -fv
```
