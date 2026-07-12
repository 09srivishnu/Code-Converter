"""
Flask server for C ↔ Python Code Converter
Main API endpoint for code conversion
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(backend_dir)

sys.path.insert(0, backend_dir)

from lexer.lexer import CLexer, PyLexer
from parser.parser import CParser, PyParser
from codegen.py_generator import PythonGenerator
from codegen.c_generator import CGenerator

# ============================================================
# Flask App Configuration
# ============================================================

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# ============================================================
# Error Handler Middleware
# ============================================================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'errors': ['Bad request'],
        'warnings': []
    }), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'errors': ['Internal server error'],
        'warnings': []
    }), 500

# ============================================================
# API Routes
# ============================================================

@app.route('/api/convert', methods=['POST'])
def convert():
    """
    Main conversion endpoint
    
    Request JSON:
    {
        "code": "int x = 5;",
        "source": "c",
        "target": "python"
    }
    
    Response JSON:
    {
        "success": true,
        "output": "x = 0",
        "errors": [],
        "warnings": []
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'errors': ['No JSON data provided'],
                'warnings': []
            }), 400
        
        code = data.get('code', '').strip()
        source_lang = data.get('source', '').lower()
        target_lang = data.get('target', '').lower()
        
        # Validate input
        if not code:
            return jsonify({
                'success': False,
                'errors': ['Code cannot be empty'],
                'warnings': []
            }), 400
        
        if source_lang not in ['c', 'python']:
            return jsonify({
                'success': False,
                'errors': [f'Invalid source language: {source_lang}. Must be "c" or "python"'],
                'warnings': []
            }), 400
        
        if target_lang not in ['c', 'python']:
            return jsonify({
                'success': False,
                'errors': [f'Invalid target language: {target_lang}. Must be "c" or "python"'],
                'warnings': []
            }), 400
        
        if source_lang == target_lang:
            return jsonify({
                'success': False,
                'errors': ['Source and target languages must be different'],
                'warnings': []
            }), 400
        
        # Perform conversion
        result = convert_code(code, source_lang, target_lang)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'errors': [f'Server error: {str(e)}'],
            'warnings': []
        }), 500

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """
    Get supported languages and conversion pairs
    
    Response JSON:
    {
        "languages": ["c", "python"],
        "pairs": [
            {"source": "c", "target": "python"},
            {"source": "python", "target": "c"}
        ]
    }
    """
    return jsonify({
        'languages': ['c', 'python'],
        'pairs': [
            {'source': 'c', 'target': 'python'},
            {'source': 'python', 'target': 'c'}
        ]
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Response JSON:
    {
        "status": "ok",
        "service": "C-Python Code Converter API"
    }
    """
    return jsonify({
        'status': 'ok',
        'service': 'C-Python Code Converter API'
    }), 200

# ============================================================
# Conversion Logic
# ============================================================

def convert_code(code, source_lang, target_lang):
    """
    Main conversion function
    
    Pipeline:
    C → Python: CLexer → CParser → PythonGenerator
    Python → C: PyLexer → PyParser → CGenerator
    
    Args:
        code (str): Source code to convert
        source_lang (str): "c" or "python"
        target_lang (str): "c" or "python"
    
    Returns:
        dict: {success, output, errors, warnings}
    """
    errors = []
    warnings = []
    output = ""
    
    try:
        if source_lang == 'c' and target_lang == 'python':
            # C to Python conversion
            try:
                # Step 1: Tokenize C code
                lexer = CLexer(code)
                tokens = lexer.tokenize()
                
                # Step 2: Parse tokens to AST
                parser = CParser(tokens)
                ast = parser.parse()
                
                # Step 3: Generate Python code
                generator = PythonGenerator(ast)
                output = generator.generate()
                
                return {
                    'success': True,
                    'output': output,
                    'errors': errors,
                    'warnings': warnings
                }
            except SyntaxError as e:
                errors.append(f"Parse Error: {str(e)}")
                return {
                    'success': False,
                    'output': "",
                    'errors': errors,
                    'warnings': warnings
                }
            except Exception as e:
                errors.append(f"Conversion Error: {str(e)}")
                return {
                    'success': False,
                    'output': "",
                    'errors': errors,
                    'warnings': warnings
                }
        
        elif source_lang == 'python' and target_lang == 'c':
            # Python to C conversion
            try:
                # Step 1: Tokenize Python code
                lexer = PyLexer(code)
                tokens = lexer.tokenize()
                
                # Step 2: Parse tokens to AST
                parser = PyParser(tokens)
                ast = parser.parse()
                
                # Step 3: Generate C code
                generator = CGenerator(ast)
                output = generator.generate()
                
                return {
                    'success': True,
                    'output': output,
                    'errors': errors,
                    'warnings': warnings
                }
            except SyntaxError as e:
                errors.append(f"Parse Error: {str(e)}")
                return {
                    'success': False,
                    'output': "",
                    'errors': errors,
                    'warnings': warnings
                }
            except Exception as e:
                errors.append(f"Conversion Error: {str(e)}")
                return {
                    'success': False,
                    'output': "",
                    'errors': errors,
                    'warnings': warnings
                }
        
        else:
            errors.append(f"Unsupported conversion: {source_lang} → {target_lang}")
            return {
                'success': False,
                'output': "",
                'errors': errors,
                'warnings': warnings
            }
    
    except Exception as e:
        errors.append(f"Fatal Error: {str(e)}")
        return {
            'success': False,
            'output': "",
            'errors': errors,
            'warnings': warnings
        }

# ============================================================
# Entry Point
# ============================================================

if __name__ == '__main__':
    print("=" * 60)
    print("C ↔ Python Code Converter API Server")
    print("=" * 60)
    print("Starting Flask server...")
    print("API available at: http://localhost:5000")
    print("Frontend available at: http://localhost:5173")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST /api/convert - Convert code")
    print("  GET  /api/languages - Get supported languages")
    print("  GET  /api/health - Health check")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Run Flask app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5001,
        use_reloader=True
    )