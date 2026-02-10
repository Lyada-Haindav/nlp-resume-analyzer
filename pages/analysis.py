"""
Analysis Page for AI Resume Skill Gap Analyzer
Main analysis functionality with resume upload and skill analysis
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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'nlp_modules'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from nlp_modules.skill_extractor import SkillExtractor
from utils.pdf_extractor import PDFExtractor
from utils.skill_analyzer import SkillAnalyzer
from utils.shared import set_custom_css, create_progress_ring, create_skill_bar_chart, create_skill_radar_chart, display_skill_cards

def show_analysis_page():
    """Display the analysis page"""
    set_custom_css()
    
    # Page header
    st.markdown('<h1 class="main-header">🎯 Resume Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Upload your resume and get AI-powered skill analysis</p>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🏠 Home", use_container_width=True):
            st.info("👆 Navigate to 'Home' page from the sidebar to return to the main page.")
    
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.analysis_complete = False
            st.session_state.resume_text = ""
            st.session_state.analysis_results = None
            st.rerun()
    
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
        job_skills_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'job_skills.json')
        
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
        analyze_button = st.button(
            "🔍 Analyze Resume",
            type="primary",
            use_container_width=True,
            help="Click to start the skill gap analysis"
        )
        
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="custom-footer">
        <strong>🎯 AI Resume Skill Gap Analyzer</strong><br>
        <span style="color: #94a3b8;">Powered by Advanced NLP Technology</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_analysis_page()
