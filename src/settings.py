from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# OpenSearch configuration
ADMIN_PASSWD = os.environ.get('OPENSEARCH_INITIAL_ADMIN_PASSWORD')
INDEX_NAME = 'knn-index'
PIPELINE_NAME = "ingest-pipeline"
MODEL_URL = "huggingface/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_GROUP_ID = None
MODEL_ID = None
OPENSEARCH_ADDRESS=os.environ.get('OPENSEARCH_ADDRESS')

# Define paths dynamically relative to this file
SRC_DIR = Path(__file__).resolve().parent
BASE_DIR = SRC_DIR.parent

DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OPENSEARCH_CONFIG_DIR = BASE_DIR / "opensearch-config"
OCR_DIR = DATA_DIR / "_ocr"
CONTENT_DIR = DATA_DIR / "content"
ARTICLES_DIR = BASE_DIR / "articles"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
OCR_DIR.mkdir(parents=True, exist_ok=True)
CONTENT_DIR.mkdir(parents=True, exist_ok=True)
