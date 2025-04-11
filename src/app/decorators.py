from functools import wraps
from flask import request, jsonify
import sys
if '..' not in sys.path: sys.path.append('..')
from utils import get_logger

logger = get_logger(__name__)

def require_request_params(*parameters):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON payload provided'}), 400

            missing_params = [param for param in parameters if not data.get(param)]
            if missing_params:
                return jsonify({'error': f'Missing required field(s): {missing_params}'}), 400

            return f(*args, **kwargs)
        return decorated_function
    return wrapper
