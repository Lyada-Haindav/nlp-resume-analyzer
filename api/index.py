from flask import Flask, render_template, request, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/run-streamlit')
def run_streamlit():
    try:
        # Run Streamlit app
        result = subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            '../app.py', '--server.headless', 'true', '--server.port', '8501'
        ], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        
        return jsonify({
            'status': 'success',
            'message': 'Streamlit app started successfully'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
