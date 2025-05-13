from flask import Blueprint, request, jsonify
import sys
if '..' not in sys.path:
    sys.path.append('..')
from opensearch_client import OpenSearchClient
from utils import get_logger
from app.decorators import require_request_params

main = Blueprint('main', __name__)

client = OpenSearchClient()

logger = get_logger("routes", stdout=True)

@main.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'Hello world!'}), 200

@main.route('/upload', methods=['POST'])
@require_request_params('id', 'content')
def upload():
    data = request.get_json()
    id = data.get('id')
    content = data.get('content')

    if not client.index_exists(index_name=id):
        client.create_index(index_name=id)

    response = client.ingest_data_bulk(content)
    if not response:
        return jsonify({'error': "Failed to upload data"}), 400

    return jsonify({'status': 'Data uploaded successfully'}), 200 

@main.route('/delete', methods=['DELETE'])
@require_request_params('id', 'filename')
def delete():
    data = request.get_json()
    id = data.get('id')
    filename = data.get('filename')

    if not client.index_exists(index_name=id):
        return jsonify({'error': f'User does not have an index'}), 400

    response = client.delete_document(id, filename)
    if not response:
        return jsonify({'error': "Failed to delete document"}), 400

    return jsonify({'status': 'Document deleted successfully'}), 200

@main.route('/search', methods=['GET'])
@require_request_params('id', 'query')
def search():
    data = request.get_json()
    id = data.get('id')
    query = data.get('query')
    
    response = client.semantic_search(id, query)
    if not response:
        return jsonify({'error': "Error occured while performing semantic search"}), 400

    return jsonify(response), 200

@main.route('/get-documents', methods=['GET'])
@require_request_params('id')
def get_documents():
    data = request.get_json()
    id = data.get('id')
    
    if not client.index_exists(index_name=id):
        client.create_index(index_name=id)
        return jsonify({"documents": []}), 200

    response = client.get_documents_from_index(index_name=id)
    if not response:
        return jsonify({'error': f"Error occured while getting documents from index {id}"}), 400
    
    logger.info("Documents fetched:")
    logger.info(response, indent=4)

    return jsonify({"documents": response})
