from flask import Blueprint, request, jsonify
import sys
if '..' not in sys.path:
    sys.path.append('..')
import settings
from opensearch_client import OpenSearchClient

main = Blueprint('main', __name__)

client = OpenSearchClient()

@main.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'Hello world!'}), 200

@main.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    # The client must send a JSON payload with a Content-Type header set to application/json.
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    id = data.get('id')
    content = data.get('content')

    if not id or not content:
        return jsonify({'error': 'Required fields: "id" and "content"'}), 400
    
    response = client.ingest_data_bulk(content)
    if not response:
        return jsonify({'error': "Failed to upload data"}), 400

    return jsonify({'status': 'Data uploaded successfully'}), 200 

@main.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()
    # The client must send a JSON payload with a Content-Type header set to application/json.
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    id = data.get('id')
    filename = data.get('filename')

    if not id or not filename:
        return jsonify({'error': 'Required fields: "id" and "filename"'}), 400
    
    response = client.delete_document(id, filename)
    if not response:
        return jsonify({'error': "Failed to delete document"}), 400

    return jsonify({'status': 'Document deleted successfully'}), 200

@main.route('/search', methods=['GET'])
def search():
    data = request.get_json()
    # The client must send a JSON payload with a Content-Type header set to application/json.
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400

    id = data.get('id')
    query = data.get('query')

    if not id or not query:
        return jsonify({'error': 'Required fields: "id" and "query"'}), 400
    
    response = client.semantic_search(id, query)
    if not response:
        return jsonify({'error': "Error occured while performing semantic search"}), 400

    return jsonify(response), 200
