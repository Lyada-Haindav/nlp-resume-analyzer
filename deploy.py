"""
Minimal Streamlit app for deployment testing
"""

import streamlit as st
import os
import sys

# Add modules to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'nlp_modules'))
sys.path.append(os.path.join(current_dir, 'utils'))

from nlp_modules.skill_extractor import SkillExtractor
from utils.pdf_extractor import PDFExtractor
from utils.skill_analyzer import SkillAnalyzer
from utils.shared import set_custom_css

# Page configuration
st.set_page_config(
    page_title="Resume Skill Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar
hide_sidebar_style = """
<style>
[data-testid="stSidebar"] { display: none !important; }
.stMain { max-width: 100%; margin: 0 auto; padding: 1rem 1.5rem; }
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Set custom styling
set_custom_css()

# Simple test
st.title("🧪 Resume Skill Analyzer - Deploy Test")
st.write("This is a minimal test for Streamlit Community Cloud deployment.")

# Test basic functionality
if st.button("Test Import"):
    try:
        skill_extractor = SkillExtractor(os.path.join(current_dir, 'data', 'job_skills.json'))
        st.success("✅ Import test successful!")
    except Exception as e:
        st.error(f"❌ Import failed: {e}")

if st.button("Test Data Access"):
    try:
        job_skills_path = os.path.join(current_dir, 'data', 'job_skills.json')
        if os.path.exists(job_skills_path):
            st.success("✅ Data access successful!")
        else:
            st.error("❌ Data files not found!")
    except Exception as e:
        st.error(f"❌ Data access failed: {e}")

st.write("---")
st.write("If this works, the main app should work on Streamlit Community Cloud.")
