"""
AI Resume Skill Gap Analyzer
Single-page application with home and analysis sections
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
from utils.shared import set_custom_css, create_progress_ring, create_skill_bar_chart, create_skill_radar_chart, display_skill_cards

# Page configuration
st.set_page_config(
    page_title="AI Resume Skill Gap Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={}
)

# Hide sidebar and set main content width
hide_sidebar_style = """
<style>
    [data-testid="stSidebar"] { display: none !important; }
    .stMain {
        max-width: 1000px !important;
        margin: 0 auto !important;
        padding: 2rem 2.5rem !important;
    }
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'home'

if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# Set custom styling
set_custom_css()

# Navigation
if st.session_state.current_section == 'home':
    # HOME PAGE
    st.markdown('<h1 class="main-header">Resume Skill Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">AI-powered skill gap analysis. Upload your resume, pick a role, and get actionable insights in seconds.</p>', unsafe_allow_html=True)
    
    # Stats row - compact
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("15+", "Job Roles"),
        ("200+", "Skills"),
        ("95%", "Accuracy"),
        ("Free", "Forever"),
    ]
    for i, (num, label) in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="stat-item animate-fade-in">
                <div class="stat-number">{num}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features - cleaner 3-column
    st.markdown('<h2 class="sub-header">How it works</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card animate-fade-in">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Upload Resume</div>
            <div class="feature-description">
                PDF or text format. We extract and analyze your skills automatically.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card animate-fade-in">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Choose Role</div>
            <div class="feature-description">
                Select from 15+ job roles with salary ranges and growth potential.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card animate-fade-in">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Get Insights</div>
            <div class="feature-description">
                Match rate, missing skills, and personalized recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <p style="color: #94a3b8; margin-bottom: 1.25rem; font-size: 1rem;">Ready to see how you match?</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Analysis", type="primary", use_container_width=True):
            st.session_state.current_section = 'analysis'
            st.rerun()

else:
    # ANALYSIS PAGE
    col_nav, col_title = st.columns([1, 5])
    with col_nav:
        if st.button("← Home", use_container_width=True):
            st.session_state.current_section = 'home'
            st.rerun()
    with col_title:
        st.markdown('<h1 class="main-header" style="text-align: left; margin-bottom: 0.25rem;">Analysis</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle" style="text-align: left; margin-bottom: 1.5rem;">Upload your resume and select a target role</p>', unsafe_allow_html=True)
    
    # Configuration Section
    st.markdown('<h2 class="sub-header">Setup</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;">Resume</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload PDF or TXT",
            type=['pdf', 'txt'],
            help="Your resume in PDF or text format"
        )
    
    with col2:
        st.markdown('<p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;">Target Role</p>', unsafe_allow_html=True)
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
            selected_job_role = None
    
    # Analyze button
    if uploaded_file is not None and selected_job_role:
        analyze_button = st.button(
            "Analyze Resume",
            type="primary",
            use_container_width=True,
            help="Start skill gap analysis"
        )
        
        if analyze_button:
            # Validate file before processing
            if uploaded_file.size == 0:
                st.error("📄 The uploaded file is empty. Please choose a valid file.")
            elif uploaded_file.name.lower().endswith('.pdf') and uploaded_file.size < 1000:
                st.warning("⚠️ The PDF file seems too small. Please ensure it contains your resume content.")
            else:
                # Extract text from uploaded file
                with st.spinner("📄 Extracting text from resume..."):
                    resume_text = PDFExtractor.extract_text_from_uploaded_file(uploaded_file)
                    
                    if resume_text is None or resume_text.strip() == "":
                        st.error("❌ Failed to extract text from the uploaded file. The file might be corrupted or empty. Please try a different file.")
                    elif len(resume_text.strip()) < 50:
                        st.warning("⚠️ The extracted text seems very short. Please ensure your resume contains sufficient content for analysis.")
                    else:
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
                                else:
                                    # Get required skills for selected job
                                    required_skills = skill_extractor.get_job_role_skills(selected_job_role)
                                    
                                    # Validate required skills
                                    if not required_skills:
                                        st.error(f"❌ No required skills found for the job role: {selected_job_role}")
                                    else:
                                        # Perform skill gap analysis
                                        skill_analyzer = SkillAnalyzer()
                                        analysis_results = skill_analyzer.analyze_skill_gaps(resume_skills, required_skills)
                                        
                                        # Validate analysis results
                                        if not analysis_results:
                                            st.error("❌ Analysis failed to produce results. Please try again.")
                                        else:
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
    
    # Display results
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        # Key metrics row
        st.markdown('<h2 class="sub-header">Summary</h2>', unsafe_allow_html=True)
        
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
        st.markdown('<h2 class="sub-header">Skills</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            display_skill_cards(results['matched_skills'], "Matched", "skill-match")
        
        with col2:
            display_skill_cards(results['missing_skills'], "Missing", "skill-missing")
        
        # Visualizations
        st.markdown('<h2 class="sub-header">Analytics</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_bar = create_skill_bar_chart(results['matched_skills'], results['missing_skills'])
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            if results['category_analysis']:
                fig_radar = create_skill_radar_chart(results, results['category_analysis'])
                st.plotly_chart(fig_radar, use_container_width=True)
        
        # Recommendations
        if results['recommendations']:
            st.markdown('<h2 class="sub-header">Recommendations</h2>', unsafe_allow_html=True)
            
            for i, recommendation in enumerate(results['recommendations'], 1):
                st.markdown(f"""
                <div class="recommendation-box">
                    <strong>{i}.</strong> {recommendation}
                </div>
                """, unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div class="custom-footer">
    Resume Skill Analyzer · Powered by NLP
</div>
""", unsafe_allow_html=True)
