# DB service

Provides a low-level OpenSearch Python client with wrapper methods for the OpenSearch REST API so that you can interact with your cluster more naturally in Python.

* upload documents in bulk and automatically embed text with an ingest pipeline  
* perform semantic (k‑NN) search against your own per‑user indices  
* list or delete stored documents and indices

The service is fully containerised and includes a GitHub Actions workflow to publish a new Docker image on every push to `main`.

---

## Tech stack

| Layer          | Technology                                       | Notes |
|----------------|--------------------------------------------------|-------|
| Language       | **Python 3.12**                                  | Alpine image |
| Web API        | **Flask 3** + `flask-cors`                       | Blueprint mounted at `/db-service` |
| Search backend | **OpenSearch** (2.x)                             | Ingest pipeline, k‑NN vector index |
| ML             | HF model *paraphrase-multilingual-MiniLM‑L12‑v2* | Deployed via ML Commons |
| Infrastructure | **Docker** / **GitHub Actions**                  | Multi‑arch build & push to GHCR |
| Config / misc  | `python-dotenv`, `Jinja2`, `Werkzeug`            | Dynamic templates & logging |

---

## Running the service

### 1. Environment variables

| Variable | Purpose |
|----------|---------|
| `OPENSEARCH_ADDRESS` | Hostname of your OpenSearch node (e.g. `https://opensearch:9200`) |
| `OPENSEARCH_INITIAL_ADMIN_PASSWORD` | Admin password used for HTTP basic auth |
| `HOSTNAME` *(opt.)* | Bind address for Flask (default `0.0.0.0`) |
| `PORT` *(opt.)* | Exposed port (default `5700`) |

Create a `.env` file or export them from your shell.

---

### 2. Run locally (Python)

```bash
git clone <repo>
cd db-service                         # project root
python -m venv env && source env/bin/activate
pip install -r requirements.txt
export $(grep -v '^#' .env | xargs)   # or set vars manually
python src/run.py                     # starts on http://localhost:5700
```

---

### 3. Run with Docker

```bash
# Build the image
docker build -t db-service .

# Start the container (pass env vars or --env-file .env)
docker run --rm -p 5700:5700 \
  -e OPENSEARCH_ADDRESS=https://opensearch.local:9200 \
  -e OPENSEARCH_INITIAL_ADMIN_PASSWORD=admin \
  db-service
```

The container’s default command is `python3 src/run.py`.

---

### 4. Using the API (quick reference)

| Method & path | Body (JSON) | Description                                     |
|---------------|-------------|-------------------------------------------------|
| `POST /db-service/upload` | `{ "id": "<index>", "content": [...] }` | Bulk‑upload documents (creates index if absent) |
| `GET /db-service/search` | `{ "id": "<index>", "query": "…" }` | Semantic search (k results, default 3)          |
| `GET /db-service/get-documents` | `{ "id": "<index>" }` | List distinct file names stored in an index     |
| `DELETE /db-service/delete` | `{ "id": "<index>", "filename": "file.pdf" }` | Delete all docs from a given file               |

All endpoints expect `Content‑Type: application/json`.

---

## Continuous delivery

* **build-and-push.yml** uses Docker Buildx to build a multi‑architecture image and push it to **GHCR**.
* A follow‑up job updates the `db-service` image tag inside an external Kubernetes manifests repository.

---

## Development tips

* Logging goes to `logs/<module>.log`; enable stderr streaming via `get_logger(..., stderr=True)`.
* Configuration files in **`opensearch-config/`** are Jinja2 templates and rendered at runtime.
* To re‑initialise the ML ingest pipeline manually, run `python src/init.py` after the cluster is up.

---

## License

Distributed under the terms of your project’s license (add one if missing).
```