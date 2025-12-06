# Flask Microloans API + Postgres (Docker)

Minimal REST API for microloans, built with Flask, SQLAlchemy, Alembic, and PostgreSQL (via Docker Compose).

## Quick start

```bash
# 1) Build and start services
docker compose up -d --build

# 2) Run DB migrations
docker compose exec api alembic upgrade head

# 3) Seed dummy data (idempotent)
docker compose exec api python scripts/seed.py

# 4) Hit endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/loans
```

## Configuration
### 1. Create Certificate Directory
```bash
/certs
```

This folder stores:
- SSL Private Key
- Self-signed Certificate

Keeping them isolated avoids pollution inside the project tree.


### 2. Generate Private Key (Important Decision)
  - I generated the private key using:
```` 
openssl genrsa -out certs/branchloans.key 2048
````
### 3. Generate a Self-Signed SSL Certificate
````
 openssl req -new -x509 -key certs/branchloans.key \
 -out certs/branchloans.crt -days 365 \
 -subj "/C=IN/ST=MH/L=Mumbai/O=BranchLoansLocal/CN=branchloans.com"
````
This certificate works for:

- Local HTTPS
- Secure Docker internal communication
- Nginx TLS termination
Browsers may show a warning → ignore for local development.

### 4. Domain Not Resolving
Reason: Local DNS not configured.
I fixed it by editing: (My debian12 Machine)

````
sudo /etc/hosts
````
Added:

````
127.0.0.1   branchloans.com
````
### 6 How to Switch Environments (Important)
- Uses:
````
docker compose --env-file .env \
-f docker-compose.yml \
-f docker-compose.<ENV>.yml \
up -d --build
````

````
docker compose --env-file .env -f docker-compose.yml -f docker-compose.dev.yml up -d --build
docker compose --env-file .env -f docker-compose.yml -f docker-compose.staging.yml up -d --build
docker compose --env-file .env -f docker-compose.yml -f docker-compose.prod.yml up -d --build
````

### Viewing Metrics

````
https://branchloans.com.metrics
````

### Grafana
Open: 

````
http://localhost:3000/login
````
### Prometheus data source 
````
http://prometheus:9090
````

### Dasboard JSON

- Visit Grafana-Dashboard-Json.md