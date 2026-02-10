import os
import sys
from flask import Flask, Response, request
import subprocess
import threading
import time

app = Flask(__name__)

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Global variable to store Streamlit process
streamlit_process = None

def start_streamlit():
    """Start Streamlit in background"""
    global streamlit_process
    try:
        # Change to the correct directory
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        
        # Start Streamlit
        streamlit_process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.headless', 'true',
            '--server.port', '8501',
            '--server.address', '0.0.0.0'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for Streamlit to start
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        return False

@app.route('/')
def index():
    """Serve the main page"""
    # Start Streamlit if not already running
    global streamlit_process
    if streamlit_process is None or streamlit_process.poll() is not None:
        threading.Thread(target=start_streamlit, daemon=True).start()
        time.sleep(3)  # Give it time to start
    
    # Return HTML that will redirect to Streamlit
    return Response('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Skill Analyzer</title>
        <meta http-equiv="refresh" content="2;url=/streamlit/">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container { 
                text-align: center; 
                background: white; 
                padding: 2rem; 
                border-radius: 10px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .spinner { 
                border: 4px solid #f3f3f3; 
                border-top: 4px solid #667eea; 
                border-radius: 50%; 
                width: 50px; 
                height: 50px; 
                animation: spin 1s linear infinite; 
                margin: 0 auto 1rem;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="spinner"></div>
            <h2>📊 Resume Skill Analyzer</h2>
            <p>Starting application...</p>
            <p><small>You will be redirected automatically</small></p>
        </div>
    </body>
    </html>
    ''', mimetype='text/html')

@app.route('/streamlit/')
def streamlit_proxy():
    """Proxy to Streamlit"""
    import requests
    try:
        response = requests.get('http://localhost:8501/', timeout=10)
        return Response(response.content, mimetype='text/html')
    except:
        return Response('Streamlit is starting... Please refresh in a moment.', mimetype='text/html')

@app.route('/streamlit/<path:path>')
def streamlit_proxy_path(path):
    """Proxy to Streamlit with path"""
    import requests
    try:
        response = requests.get(f'http://localhost:8501/{path}', timeout=10)
        return Response(response.content, mimetype=response.headers.get('content-type', 'text/html'))
    except:
        return Response('Streamlit is starting... Please refresh in a moment.', mimetype='text/html')

# Handler for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    # Start Streamlit in background
    start_streamlit()
    app.run(host='0.0.0.0', port=5000)
