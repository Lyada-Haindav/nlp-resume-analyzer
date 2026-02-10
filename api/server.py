import os
import sys
from flask import Flask, Response, request, render_template_string
import json
import base64
import io
from typing import Dict, List

app = Flask(__name__)

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import your modules
try:
    from nlp_modules.skill_extractor import SkillExtractor
    from utils.skill_analyzer import SkillAnalyzer
    from utils.shared import create_progress_ring, create_skill_bar_chart, create_skill_radar_chart, display_skill_cards
    import plotly.utils
except ImportError as e:
    print(f"Import error: {e}")

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Skill Analyzer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
            animation: fadeIn 0.6s ease-out forwards;
        }
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .glass-effect {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .skill-match {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }
        .skill-missing {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
        }
    </style>
</head>
<body class="gradient-bg min-h-screen">
    <!-- Navigation -->
    <nav class="glass-effect shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <span class="text-2xl font-bold text-white">📊 Resume Skill Analyzer</span>
                </div>
                <div class="flex items-center space-x-4">
                    <button onclick="showSection('home')" class="nav-btn text-white hover:text-gray-200 px-3 py-2 rounded-md text-sm font-medium">Home</button>
                    <button onclick="showSection('analyzer')" class="nav-btn text-white hover:text-gray-200 px-3 py-2 rounded-md text-sm font-medium">Analyzer</button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Home Section -->
    <div id="home-section" class="section">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <!-- Hero -->
            <div class="text-center mb-12 animate-fade-in">
                <h1 class="text-5xl font-bold text-white mb-4">AI Resume Skill Gap Analyzer</h1>
                <p class="text-xl text-gray-200 mb-8">Upload your resume, pick a role, and get actionable insights in seconds.</p>
                <button onclick="showSection('analyzer')" class="bg-white text-purple-600 px-8 py-3 rounded-full font-semibold hover:bg-gray-100 transition duration-300">
                    Start Analysis
                </button>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
                <div class="glass-effect rounded-lg p-6 text-center animate-fade-in">
                    <div class="text-3xl font-bold text-purple-600">15+</div>
                    <div class="text-gray-600">Job Roles</div>
                </div>
                <div class="glass-effect rounded-lg p-6 text-center animate-fade-in" style="animation-delay: 0.1s">
                    <div class="text-3xl font-bold text-purple-600">200+</div>
                    <div class="text-gray-600">Skills</div>
                </div>
                <div class="glass-effect rounded-lg p-6 text-center animate-fade-in" style="animation-delay: 0.2s">
                    <div class="text-3xl font-bold text-purple-600">95%</div>
                    <div class="text-gray-600">Accuracy</div>
                </div>
                <div class="glass-effect rounded-lg p-6 text-center animate-fade-in" style="animation-delay: 0.3s">
                    <div class="text-3xl font-bold text-purple-600">Free</div>
                    <div class="text-gray-600">Forever</div>
                </div>
            </div>

            <!-- Features -->
            <div class="grid md:grid-cols-3 gap-8">
                <div class="glass-effect rounded-lg p-6 animate-fade-in" style="animation-delay: 0.4s">
                    <div class="text-4xl mb-4">📄</div>
                    <h3 class="text-xl font-semibold mb-2">Upload Resume</h3>
                    <p class="text-gray-600">PDF or text format. We extract and analyze your skills automatically.</p>
                </div>
                <div class="glass-effect rounded-lg p-6 animate-fade-in" style="animation-delay: 0.5s">
                    <div class="text-4xl mb-4">🎯</div>
                    <h3 class="text-xl font-semibold mb-2">Choose Role</h3>
                    <p class="text-gray-600">Select from 15+ job roles with salary ranges and growth potential.</p>
                </div>
                <div class="glass-effect rounded-lg p-6 animate-fade-in" style="animation-delay: 0.6s">
                    <div class="text-4xl mb-4">📊</div>
                    <h3 class="text-xl font-semibold mb-2">Get Insights</h3>
                    <p class="text-gray-600">Match rate, missing skills, and personalized recommendations.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Analyzer Section -->
    <div id="analyzer-section" class="section hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="glass-effect rounded-lg p-8 mb-8">
                <h2 class="text-3xl font-bold text-gray-800 mb-6">Resume Analysis</h2>
                
                <!-- Upload Section -->
                <div class="grid md:grid-cols-2 gap-6 mb-8">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Upload Resume</label>
                        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-purple-500 transition-colors">
                            <input type="file" id="resume-file" accept=".pdf,.txt" class="hidden" onchange="handleFileUpload(event)">
                            <label for="resume-file" class="cursor-pointer">
                                <div class="text-4xl mb-2">📁</div>
                                <p class="text-gray-600">Click to upload PDF or TXT</p>
                                <p class="text-sm text-gray-500 mt-1">Maximum file size: 10MB</p>
                            </label>
                        </div>
                        <div id="file-info" class="mt-2 text-sm text-gray-600"></div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Target Role</label>
                        <select id="job-role" class="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                            <option value="">Select a job role...</option>
                            {{JOB_ROLES}}
                        </select>
                        <div id="role-info" class="mt-2 text-sm text-gray-600"></div>
                    </div>
                </div>

                <!-- Analyze Button -->
                <div class="text-center mb-8">
                    <button onclick="analyzeResume()" class="bg-purple-600 text-white px-8 py-3 rounded-full font-semibold hover:bg-purple-700 transition duration-300 disabled:opacity-50" id="analyze-btn">
                        Analyze Resume
                    </button>
                </div>

                <!-- Results Section -->
                <div id="results" class="hidden">
                    <h3 class="text-2xl font-bold text-gray-800 mb-6">Analysis Results</h3>
                    
                    <!-- Metrics -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                        <div class="bg-purple-50 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-purple-600" id="match-rate">-</div>
                            <div class="text-sm text-gray-600">Match Rate</div>
                        </div>
                        <div class="bg-blue-50 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-blue-600" id="similarity-score">-</div>
                            <div class="text-sm text-gray-600">Similarity</div>
                        </div>
                        <div class="bg-green-50 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-green-600" id="proficiency-level">-</div>
                            <div class="text-sm text-gray-600">Proficiency</div>
                        </div>
                        <div class="bg-yellow-50 rounded-lg p-4 text-center">
                            <div class="text-2xl font-bold text-yellow-600" id="skills-matched">-</div>
                            <div class="text-sm text-gray-600">Skills Matched</div>
                        </div>
                    </div>

                    <!-- Charts -->
                    <div class="grid md:grid-cols-2 gap-6 mb-8">
                        <div class="bg-white rounded-lg p-6 shadow-lg">
                            <h4 class="text-lg font-semibold text-gray-800 mb-4">Skill Match Chart</h4>
                            <div id="skill-chart"></div>
                        </div>
                        <div class="bg-white rounded-lg p-6 shadow-lg">
                            <h4 class="text-lg font-semibold text-gray-800 mb-4">Skill Radar</h4>
                            <div id="radar-chart"></div>
                        </div>
                    </div>

                    <!-- Skills Breakdown -->
                    <div class="grid md:grid-cols-2 gap-6 mb-8">
                        <div>
                            <h4 class="text-lg font-semibold text-gray-800 mb-3">Matched Skills</h4>
                            <div id="matched-skills" class="space-y-2"></div>
                        </div>
                        <div>
                            <h4 class="text-lg font-semibold text-gray-800 mb-3">Missing Skills</h4>
                            <div id="missing-skills" class="space-y-2"></div>
                        </div>
                    </div>

                    <!-- Recommendations -->
                    <div>
                        <h4 class="text-lg font-semibold text-gray-800 mb-3">Recommendations</h4>
                        <div id="recommendations" class="space-y-2"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let analysisData = null;

        function showSection(section) {
            document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
            document.getElementById(section + '-section').classList.remove('hidden');
        }

        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                document.getElementById('file-info').textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
            }
        }

        async function analyzeResume() {
            const file = document.getElementById('resume-file').files[0];
            const role = document.getElementById('job-role').value;
            
            if (!file || !role) {
                alert('Please upload a resume and select a job role.');
                return;
            }

            // Show loading state
            document.getElementById('analyze-btn').disabled = true;
            document.getElementById('analyze-btn').textContent = 'Analyzing...';

            // Read file
            const fileContent = await readFileContent(file);
            
            // Send to backend
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        resume_text: fileContent,
                        job_role: role
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    displayResults(data.results);
                } else {
                    alert('Analysis failed: ' + data.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }

            document.getElementById('analyze-btn').disabled = false;
            document.getElementById('analyze-btn').textContent = 'Analyze Resume';
        }

        function readFileContent(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = (e) => resolve(e.target.result);
                reader.onerror = reject;
                reader.readAsText(file);
            });
        }

        function displayResults(data) {
            analysisData = data;
            
            // Update metrics
            document.getElementById('match-rate').textContent = data.match_percentage + '%';
            document.getElementById('similarity-score').textContent = Math.round(data.similarity_score * 100) + '%';
            document.getElementById('proficiency-level').textContent = data.proficiency_level;
            document.getElementById('skills-matched').textContent = `${data.total_matched_skills}/${data.total_required_skills}`;

            // Display charts
            if (data.skill_chart) {
                Plotly.newPlot('skill-chart', data.skill_chart.data, data.skill_chart.layout);
            }
            if (data.radar_chart) {
                Plotly.newPlot('radar-chart', data.radar_chart.data, data.radar_chart.layout);
            }

            // Display matched skills
            const matchedContainer = document.getElementById('matched-skills');
            matchedContainer.innerHTML = Object.entries(data.matched_skills || {}).map(([skill, level]) => 
                `<div class="bg-green-100 text-green-800 px-3 py-2 rounded-lg">
                    <div class="font-semibold">${skill}</div>
                    <div class="text-sm">Level: ${level}</div>
                </div>`
            ).join('');

            // Display missing skills
            const missingContainer = document.getElementById('missing-skills');
            missingContainer.innerHTML = (data.missing_skills || []).map(skill => 
                `<div class="bg-red-100 text-red-800 px-3 py-2 rounded-lg">
                    <div class="font-semibold">${skill}</div>
                </div>`
            ).join('');

            // Display recommendations
            const recommendationsContainer = document.getElementById('recommendations');
            recommendationsContainer.innerHTML = (data.recommendations || []).map(rec => 
                `<div class="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                    <p class="text-sm text-gray-700">${rec}</p>
                </div>`
            ).join('');

            // Show results
            document.getElementById('results').classList.remove('hidden');
        }

        // Initialize
        showSection('home');
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main page"""
    try:
        # Get job roles for the dropdown
        job_skills_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_skills.json')
        skill_extractor = SkillExtractor(job_skills_path)
        job_roles = skill_extractor.get_all_job_roles()
        
        job_options = ''.join([f'<option value="{role}">{role}</option>' for role in job_roles])
        
        return render_template_string(HTML_TEMPLATE, JOB_ROLES=job_options)
    except Exception as e:
        return f"Error loading page: {str(e)}", 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze resume"""
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_role = data.get('job_role', '')
        
        if not resume_text or not job_role:
            return {'success': False, 'error': 'Missing resume text or job role'}
        
        # Initialize components
        job_skills_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_skills.json')
        skill_extractor = SkillExtractor(job_skills_path)
        skill_analyzer = SkillAnalyzer()
        
        # Extract skills
        resume_skills = skill_extractor.extract_skills_combined(resume_text)
        required_skills = skill_extractor.get_job_role_skills(job_role)
        
        # Analyze
        analysis_results = skill_analyzer.analyze_skill_gaps(resume_skills, required_skills)
        
        # Create charts
        skill_chart = create_skill_bar_chart(analysis_results['matched_skills'], analysis_results['missing_skills'])
        radar_chart = create_skill_radar_chart(analysis_results, analysis_results.get('category_analysis', {}))
        
        # Convert charts to JSON
        skill_chart_json = json.loads(skill_chart.to_json())
        radar_chart_json = json.loads(radar_chart.to_json())
        
        return {
            'success': True,
            'results': {
                **analysis_results,
                'skill_chart': skill_chart_json,
                'radar_chart': radar_chart_json
            }
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Handler for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
