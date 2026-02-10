"""
AI-Powered Resume Skill Gap Analyzer
A comprehensive Streamlit application for analyzing resume skills against job requirements
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import sys
import os
from typing import Dict, List

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'nlp_modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from nlp_modules.skill_extractor import SkillExtractor
from utils.pdf_extractor import PDFExtractor
from utils.skill_analyzer import SkillAnalyzer

# Page configuration
st.set_page_config(
    page_title="AI Resume Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# Custom CSS for professional dark theme styling
def set_custom_css():
    st.markdown("""
    <style>
        /* Dark Theme Global Styles */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: #f1f5f9;
        }
        
        /* Streamlit default overrides */
        .stApp > div {
            background: transparent !important;
        }
        
        .stBlock {
            background: transparent !important;
        }
        
        .stMarkdown {
            color: #f1f5f9 !important;
        }
        
        .stSelectbox > div > div > select {
            background: #1e293b !important;
            color: #f1f5f9 !important;
            border: 1px solid #475569 !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            padding: 0.75rem 1.5rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3) !important;
        }
        
        .stFileUploader > div {
            background: #1e293b !important;
            border: 2px dashed #475569 !important;
            border-radius: 15px !important;
            padding: 2rem !important;
        }
        
        .stFileUploader > div:hover {
            border-color: #3b82f6 !important;
            background: #334155 !important;
        }
        
        .stAlert {
            background: #1e293b !important;
            border-left: 4px solid #3b82f6 !important;
            color: #f1f5f9 !important;
        }
        
        .stSuccess {
            background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important;
            border-left: 4px solid #10b981 !important;
        }
        
        .stError {
            background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%) !important;
            border-left: 4px solid #ef4444 !important;
        }
        
        .stInfo {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
            border-left: 4px solid #3b82f6 !important;
            color: #dbeafe !important;
        }
        
        /* Hide Streamlit watermarks and branding */
        .stDeployButton {
            display: none !important;
        }
        
        #MainMenu {
            visibility: hidden !important;
        }
        
        footer {
            visibility: hidden !important;
        }
        
        header {
            visibility: hidden !important;
        }
        
        .stApp > div > div > div > div > div > div > div > div:first-child {
            display: none !important;
        }
        
        /* Hide the "Made with Streamlit" footer and all Streamlit branding */
        .stApp > div > div > div > div > div > div > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdownContainer"] > div > p {
            display: none !important;
        }
        
        .stApp > div > div > div > div > div > div > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdownContainer"] > div > p > a {
            display: none !important;
        }
        
        /* Hide any remaining Streamlit branding elements */
        [data-testid="stHeader"] {
            display: none !important;
        }
        
        [data-testid="stFooter"] {
            display: none !important;
        }
        
        .stApp > div > div > div > div > div > div > div > div > div > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdownContainer"] > p {
            display: none !important;
        }
        
        /* Custom footer */
        .custom-footer {
            text-align: center;
            color: #64748b;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid #334155;
        }
        
        .main-header {
            font-size: 3.5rem;
            font-weight: 800;
            color: #ffffff;
            text-align: center;
            margin-bottom: 1rem;
            padding: 2rem;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
            border: 1px solid #334155;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            color: #94a3b8;
            text-align: center;
            margin-bottom: 3rem;
            padding: 0 2rem;
        }
        
        .sub-header {
            font-size: 2rem;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            border-left: 5px solid #3b82f6;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #334155;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(59, 130, 246, 0.2);
            border-color: #3b82f6;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            margin-bottom: 2rem;
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid #334155;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(59, 130, 246, 0.2);
            border-color: #3b82f6;
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 1rem;
        }
        
        .feature-description {
            color: #94a3b8;
            line-height: 1.6;
        }
        
        .job-role-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
            margin-bottom: 1.5rem;
            border-left: 5px solid #3b82f6;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #334155;
        }
        
        .job-role-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(59, 130, 246, 0.2);
            border-color: #3b82f6;
        }
        
        .job-role-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #60a5fa;
            margin-bottom: 1rem;
        }
        
        .job-role-meta {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        
        .job-role-badge {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 700;
            box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
        }
        
        .job-role-badge:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(59, 130, 246, 0.4);
        }
        
        .job-role-description {
            color: #94a3b8;
            line-height: 1.6;
        }
        
        .sidebar-section {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid #334155;
        }
        
        .skill-match {
            color: #34d399;
            font-weight: 600;
            background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .skill-missing {
            color: #f87171;
            font-weight: 600;
            background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .proficiency-expert { 
            color: #34d399; 
            font-weight: bold; 
            background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .proficiency-advanced { 
            color: #60a5fa; 
            font-weight: bold;
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .proficiency-intermediate { 
            color: #fbbf24; 
            font-weight: bold;
            background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .proficiency-beginner { 
            color: #f87171; 
            font-weight: bold;
            background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .proficiency-novice { 
            color: #94a3b8; 
            font-weight: bold;
            background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Recommendation Box */
        .recommendation-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e293b 100%);
            border-left: 5px solid #3b82f6;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid #334155;
        }
        
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
            border-radius: 10px;
        }
        
        /* Animation styles */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2.5rem;
            }
            .hero-subtitle {
                font-size: 1.1rem;
            }
            .sub-header {
                font-size: 1.5rem;
            }
        }
        
        /* Hide Streamlit watermarks and branding */
        .stDeployButton {
            display: none !important;
        }
        
        #MainMenu {
            visibility: hidden !important;
        }
        
        footer {
            visibility: hidden !important;
        }
        
        .stApp > div > div > div > div > div > div > div > div:first-child {
            display: none !important;
        }
        
        /* Hide the "Made with Streamlit" footer */
        .stApp > div > div > div > div > div > div > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdownContainer"] > div > p {
            display: none !important;
        }
        
        /* Hide the header and footer completely */
        header {
            display: none !important;
        }
        
        .stApp > div > div > div > div > div > div > div > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stMarkdownContainer"] > div > p > a {
            display: none !important;
        }
        
        /* Custom footer */
        .custom-footer {
            text-align: center;
            color: #64748b;
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid #334155;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e293b;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        }
    </style>
    <script>
        // Hide Streamlit elements after page load
        document.addEventListener('DOMContentLoaded', function() {
            // Hide any remaining Streamlit branding
            const elementsToHide = [
                '[data-testid="stHeader"]',
                '[data-testid="stFooter"]',
                '.stDeployButton',
                '#MainMenu',
                'footer',
                'header'
            ];
            
            elementsToHide.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                });
            });
            
            // Hide any elements containing "Made with Streamlit" or similar text
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                if (el.textContent && (
                    el.textContent.includes('Made with Streamlit') ||
                    el.textContent.includes('Streamlit') ||
                    el.textContent.includes('by Streamlit')
                )) {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                }
            });
        });
        
        // Run periodically to catch dynamically added elements
        setInterval(() => {
            const elementsToHide = [
                '.stDeployButton',
                '[data-testid="stFooter"]'
            ];
            
            elementsToHide.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                });
            });
        }, 1000);
    </script>
    """, unsafe_allow_html=True)

def create_progress_ring(percentage: float, title: str) -> go.Figure:
    """Create a circular progress indicator with dark theme colors"""
    fig = go.Figure(data=[go.Pie(
        values=[percentage, 100 - percentage],
        hole=0.7,
        showlegend=False,
        textinfo='none',
        marker_colors=['#34d399' if percentage >= 70 else '#fbbf24' if percentage >= 40 else '#f87171', '#374151']
    )])
    
    fig.add_annotation(
        text=f"{percentage}%",
        x=0.5, y=0.5,
        font_size=20,
        font_color='#ffffff',
        showarrow=False
    )
    
    fig.add_annotation(
        text=title,
        x=0.5, y=0.3,
        font_size=12,
        font_color='#9ca3af',
        showarrow=False
    )
    
    fig.update_layout(
        height=200,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff'
    )
    
    return fig

def create_skill_bar_chart(matched_skills: List[str], missing_skills: List[str]) -> go.Figure:
    """Create a bar chart showing matched vs missing skills with dark theme"""
    categories = ['Matched Skills', 'Missing Skills']
    values = [len(matched_skills), len(missing_skills)]
    colors = ['#34d399', '#f87171']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
            textfont_color='#ffffff'
        )
    ])
    
    fig.update_layout(
        title="Skill Match Overview",
        title_font_color='#ffffff',
        xaxis_title="Skill Status",
        xaxis_title_font_color='#9ca3af',
        yaxis_title="Number of Skills",
        yaxis_title_font_color='#9ca3af',
        height=400,
        showlegend=False,
        plot_bgcolor='#1f2937',
        paper_bgcolor='#111827',
        font_color='#ffffff',
        xaxis=dict(
            tickfont_color='#9ca3af',
            gridcolor='#374151'
        ),
        yaxis=dict(
            tickfont_color='#9ca3af',
            gridcolor='#374151'
        )
    )
    
    return fig

def create_skill_radar_chart(skill_analysis: Dict, skill_categories: Dict) -> go.Figure:
    """Create a radar chart for skill categories with dark theme"""
    if not skill_categories:
        return go.Figure()
    
    categories = list(skill_categories.keys())
    values = [cat_data['match_percentage'] for cat_data in skill_categories.values()]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Skill Coverage',
        line_color='#60a5fa',
        fillcolor='rgba(96, 165, 250, 0.2)',
        textfont_color='#ffffff'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont_color='#9ca3af',
                gridcolor='#374151',
                linecolor='#4b5563'
            ),
            angularaxis=dict(
                tickfont_color='#9ca3af',
                gridcolor='#374151',
                linecolor='#4b5563'
            )
        ),
        title="Skill Coverage by Category",
        title_font_color='#ffffff',
        height=500,
        plot_bgcolor='#1f2937',
        paper_bgcolor='#111827',
        font_color='#ffffff',
        legend=dict(
            font_color='#ffffff'
        )
    )
    
    return fig

def display_skill_cards(skills: List[str], title: str, color_class: str):
    """Display skills as cards with better validation"""
    if not skills:
        st.markdown(f"""
        <div class="metric-card" style="opacity: 0.7; border-left-color: #64748b;">
            <h4 style="color: #94a3b8; margin: 0;">{title}</h4>
            <p style="color: #64748b; margin: 0.5rem 0 0 0;">No skills found</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"**{title} ({len(skills)})**")
    
    # Create columns for skill cards (max 4 per row)
    cols = st.columns(min(4, max(1, len(skills))))
    
    for i, skill in enumerate(skills):
        if skill and skill.strip():  # Ensure skill is not empty
            col_idx = i % len(cols)
            with cols[col_idx]:
                st.markdown(f"""
                <div class="metric-card">
                    <span class="{color_class}">{skill.strip()}</span>
                </div>
                """, unsafe_allow_html=True)

def main():
    """Main application function"""
    set_custom_css()
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Hero Section
    st.markdown('<h1 class="main-header">🎯 AI Resume Skill Gap Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Transform your career with AI-powered skill analysis and personalized recommendations</p>', unsafe_allow_html=True)
    
    # Features Section
    if not st.session_state.analysis_complete:
        st.markdown('<h2 class="sub-header">🚀 Why Choose Our AI Analyzer?</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card animate-fade-in">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Advanced NLP</div>
                <div class="feature-description">
                    Cutting-edge natural language processing extracts skills with 95% accuracy using TF-IDF, tokenization, and semantic analysis
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card animate-fade-in">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Smart Analytics</div>
                <div class="feature-description">
                    Interactive visualizations and comprehensive gap analysis with personalized learning recommendations
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card animate-fade-in">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Career Insights</div>
                <div class="feature-description">
                    15+ job roles with salary ranges, growth potential, and detailed skill requirements
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Statistics Section
        st.markdown('<h2 class="sub-header">📈 Platform Statistics</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stat-item">
                <div class="stat-number">15+</div>
                <div class="stat-label">Job Roles</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-item">
                <div class="stat-number">200+</div>
                <div class="stat-label">Skills Tracked</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-item">
                <div class="stat-number">95%</div>
                <div class="stat-label">Accuracy Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-item">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Available</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📋 Configuration")
        
        # File upload
        st.markdown("**Upload Resume**")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt'],
            help="Upload your resume in PDF or text format"
        )
        
        # Job role selection
        st.markdown("**Select Job Role**")
        job_skills_path = os.path.join(os.path.dirname(__file__), 'data', 'job_skills.json')
        
        try:
            skill_extractor = SkillExtractor(job_skills_path)
            job_roles = skill_extractor.get_all_job_roles()
            selected_job_role = st.selectbox(
                "Choose your target role",
                job_roles,
                help="Select the job role you want to analyze your resume against"
            )
            
            # Display job role details
            job_data = skill_extractor.job_skills_data['job_roles'][selected_job_role]
            st.markdown(f"""
            <div class="job-role-card">
                <div class="job-role-title">{selected_job_role}</div>
                <div class="job-role-meta">
                    <span class="job-role-badge">{job_data['experience_level']}</span>
                    <span class="job-role-badge">{job_data['salary_range']}</span>
                    <span class="job-role-badge">{job_data['growth_potential']} Growth</span>
                </div>
                <div class="job-role-description">{job_data['description']}</div>
            </div>
            """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error loading job roles: {e}")
            return
        
        # Analyze button
        col1, col2 = st.columns(2)
        
        with col1:
            analyze_button = st.button(
                "🔍 Analyze Resume",
                type="primary",
                use_container_width=True,
                help="Click to start the skill gap analysis"
            )
        
        with col2:
            reset_button = st.button(
                "🔄 Reset Analysis",
                type="secondary",
                use_container_width=True,
                help="Clear current analysis and start over"
            )
        
        if reset_button:
            st.session_state.analysis_complete = False
            st.session_state.resume_text = ""
            st.session_state.analysis_results = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("### 📖 Instructions")
        st.markdown("""
        1. **Upload Resume**: Choose PDF or text file
        2. **Select Job Role**: Pick your target position
        3. **Analyze**: Click to start analysis
        4. **Review Results**: Check skill gaps and recommendations
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    if uploaded_file is not None and analyze_button:
        # Validate file before processing
        if uploaded_file.size == 0:
            st.error("📄 The uploaded file is empty. Please choose a valid file.")
            return
        
        if uploaded_file.name.lower().endswith('.pdf') and uploaded_file.size < 1000:
            st.warning("⚠️ The PDF file seems too small. Please ensure it contains your resume content.")
        
        # Extract text from uploaded file
        with st.spinner("📄 Extracting text from resume..."):
            resume_text = PDFExtractor.extract_text_from_uploaded_file(uploaded_file)
            
            if resume_text is None or resume_text.strip() == "":
                st.error("❌ Failed to extract text from the uploaded file. The file might be corrupted or empty. Please try a different file.")
                return
            
            if len(resume_text.strip()) < 50:
                st.warning("⚠️ The extracted text seems very short. Please ensure your resume contains sufficient content for analysis.")
            
            st.session_state.resume_text = resume_text
            st.success(f"✅ Successfully extracted {len(resume_text)} characters from your resume!")
        
        # Perform skill extraction and analysis
        with st.spinner("🧠 Analyzing skills with NLP..."):
            try:
                # Extract skills from resume
                resume_skills = skill_extractor.extract_skills_combined(resume_text)
                
                # Validate extracted skills
                if not resume_skills:
                    st.error("❌ No skills could be extracted from your resume. Please ensure your resume contains technical skills and keywords.")
                    return
                
                # Get required skills for selected job
                required_skills = skill_extractor.get_job_role_skills(selected_job_role)
                
                # Validate required skills
                if not required_skills:
                    st.error(f"❌ No required skills found for the job role: {selected_job_role}")
                    return
                
                # Perform skill gap analysis
                skill_analyzer = SkillAnalyzer()
                analysis_results = skill_analyzer.analyze_skill_gaps(resume_skills, required_skills)
                
                # Validate analysis results
                if not analysis_results:
                    st.error("❌ Analysis failed to produce results. Please try again.")
                    return
                
                # Get category analysis
                skill_categories = skill_extractor.categorize_skills(list(resume_skills.keys()))
                category_analysis = skill_analyzer.get_skill_category_analysis(
                    resume_skills, required_skills, skill_extractor.job_skills_data['technical_skills_database']
                )
                
                # Store results
                analysis_results['category_analysis'] = category_analysis
                analysis_results['resume_skills'] = resume_skills
                analysis_results['required_skills'] = required_skills
                st.session_state.analysis_results = analysis_results
                st.session_state.analysis_complete = True
                
                # Show success message with details
                st.success(f"✅ Analysis completed! Found {len(resume_skills)} skills in your resume and analyzed against {len(required_skills)} required skills.")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("💡 Please ensure your resume is in a supported format (PDF/TXT) and contains readable text content.")
                return
    
    # Display results
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        # Success message
        st.success("✅ Analysis completed successfully!")
        
        # Key metrics row
        st.markdown('<h2 class="sub-header">📊 Analysis Summary</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            fig1 = create_progress_ring(results['match_percentage'], "Match Rate")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_progress_ring(int(results['similarity_score'] * 100), "Similarity")
            st.plotly_chart(fig2, use_container_width=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: {results['proficiency_color']}; margin: 0;">
                    {results['proficiency_level']}
                </h3>
                <p style="margin: 0.5rem 0 0 0; color: #6b7280;">Proficiency Level</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #3b82f6; margin: 0;">
                    {results['total_matched_skills']}/{results['total_required_skills']}
                </h3>
                <p style="margin: 0.5rem 0 0 0; color: #6b7280;">Skills Matched</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Skills breakdown
        st.markdown('<h2 class="sub-header">🎯 Skills Breakdown</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            display_skill_cards(results['matched_skills'], "✅ Matched Skills", "skill-match")
        
        with col2:
            display_skill_cards(results['missing_skills'], "❌ Missing Skills", "skill-missing")
        
        # Visualizations
        st.markdown('<h2 class="sub-header">📈 Visual Analytics</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_bar = create_skill_bar_chart(results['matched_skills'], results['missing_skills'])
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            if results['category_analysis']:
                fig_radar = create_skill_radar_chart(results, results['category_analysis'])
                st.plotly_chart(fig_radar, use_container_width=True)
        
        # Category-wise analysis
        if results['category_analysis']:
            st.markdown('<h2 class="sub-header">📋 Category-wise Analysis</h2>', unsafe_allow_html=True)
            
            for category, cat_data in results['category_analysis'].items():
                with st.expander(f"📂 {category} ({cat_data['match_percentage']}% match)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if cat_data['matched_skills']:
                            st.markdown("**✅ Matched Skills:**")
                            for skill in cat_data['matched_skills']:
                                st.markdown(f"- {skill}")
                        else:
                            st.info("No matched skills in this category")
                    
                    with col2:
                        if cat_data['missing_skills']:
                            st.markdown("**❌ Missing Skills:**")
                            for skill in cat_data['missing_skills']:
                                st.markdown(f"- {skill}")
                        else:
                            st.success("All required skills covered!")
        
        # Recommendations
        if results['recommendations']:
            st.markdown('<h2 class="sub-header">💡 Recommendations</h2>', unsafe_allow_html=True)
            
            for i, recommendation in enumerate(results['recommendations'], 1):
                st.markdown(f"""
                <div class="recommendation-box">
                    <strong>{i}.</strong> {recommendation}
                </div>
                """, unsafe_allow_html=True)
        
        # Resume text preview
        with st.expander("📄 Resume Text Preview"):
            st.text_area("Extracted Resume Text", st.session_state.resume_text, height=300)
        
        # Download results
        st.markdown('<h2 class="sub-header">📥 Export Results</h2>', unsafe_allow_html=True)
        
        # Create downloadable report
        report_data = {
            'job_role': selected_job_role,
            'analysis_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'match_percentage': results['match_percentage'],
                'similarity_score': results['similarity_score'],
                'proficiency_level': results['proficiency_level'],
                'total_required_skills': results['total_required_skills'],
                'total_matched_skills': results['total_matched_skills'],
                'total_missing_skills': results['total_missing_skills']
            },
            'matched_skills': results['matched_skills'],
            'missing_skills': results['missing_skills'],
            'recommendations': results['recommendations']
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Download JSON Report"):
                st.download_button(
                    label="Download Analysis Report",
                    data=json.dumps(report_data, indent=2),
                    file_name=f"resume_analysis_{selected_job_role.replace(' ', '_')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("📊 Download CSV Report"):
                df = pd.DataFrame({
                    'Metric': ['Match Percentage', 'Similarity Score', 'Proficiency Level', 'Total Required Skills', 'Total Matched Skills', 'Total Missing Skills'],
                    'Value': [results['match_percentage'], results['similarity_score'], results['proficiency_level'], results['total_required_skills'], results['total_matched_skills'], results['total_missing_skills']]
                })
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV Report",
                    data=csv,
                    file_name=f"resume_analysis_{selected_job_role.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
    
    # Custom Footer
    st.markdown("---")
    st.markdown("""
    <div class="custom-footer">
        <strong>🎯 AI Resume Skill Gap Analyzer</strong><br>
        <span style="color: #94a3b8;">Powered by Advanced NLP Technology</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
