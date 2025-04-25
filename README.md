# DB service

Provides a low-level OpenSearch Python client with wrapper methods for the OpenSearch REST API so that you can interact with your cluster more naturally in Python.

* upload documents in bulk and automatically embed text with an ingest pipeline  
* perform semantic (k‑NN) search against your own per‑user indices  
* list or delete stored documents and indices

The service is fully containerised and includes a GitHub Actions workflow to publish a new Docker image on every push to `main`.

---

## Tech stack

| Layer          | Technology                                       |
|----------------|--------------------------------------------------|
| Language       | **Python 3.12**                                  |
| Web API        | **Flask 3** + `flask-cors`                       |
| Search backend | **OpenSearch** (2.x)                             |
| ML             | HuggingFace model *paraphrase-multilingual-MiniLM‑L12‑v2* |
| Infrastructure | **Docker** / **GitHub Actions**                  |
| Config / misc  | `python-dotenv`, `Jinja2`, `Werkzeug`            |

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
git clone git@github.com:document-manager-idp/db-service.git
python -m venv env && source env/bin/activate
pip install -r requirements.txt
# start app on http://localhost:5700
python src/run.py
```

---

### 3. Run with Docker

```bash
# Build the image
docker build -t db-service .

# Start container
docker run --rm -p 5700:5700 db-service
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
* To re‑initialise the ML ingest pipeline manually, run `python src/init.py` after the cluster is up.
