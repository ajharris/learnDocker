#!/usr/bin/env python3
"""
Simple Flask application for Docker learning.
Demonstrates API endpoints, environment variables, and containerization.
"""

import os
import platform
from datetime import datetime
from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

# Global visit counter
visit_count = 0

@app.route('/')
def home():
    """Home page with basic information."""
    global visit_count
    visit_count += 1
    
    return jsonify({
        'message': '🐳 Welcome to the Python Flask Docker App!',
        'visit_count': visit_count,
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/': 'This home page',
            '/api/info': 'System information',
            '/api/health': 'Health check endpoint'
        }
    })

@app.route('/api/info')
def info():
    """Return system and environment information."""
    return jsonify({
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'hostname': platform.node(),
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true',
        'flask_version': getattr(Flask, '__version__', 'unknown'),
        'container_info': {
            'is_containerized': os.path.exists('/.dockerenv'),
            'working_directory': os.getcwd(),
            'process_id': os.getpid()
        }
    })

@app.route('/api/health')
def health():
    """Health check endpoint for container monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'Container is running'
    })

@app.route('/api/visit')
def visit():
    """Increment and return visit counter."""
    global visit_count
    visit_count += 1
    
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    
    return jsonify({
        'visit_count': visit_count,
        'client_ip': client_ip,
        'timestamp': datetime.now().isoformat(),
        'message': f'Thank you for visit #{visit_count}!'
    })

if __name__ == '__main__':
    # Configuration from environment variables
    debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"🚀 Starting Flask app on {host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    print(f"🌍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    
    app.run(host=host, port=port, debug=debug_mode)