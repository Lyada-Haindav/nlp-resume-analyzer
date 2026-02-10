"""
Simplified Streamlit app for Streamlit Community Cloud
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

# Simple page config without problematic options
st.set_page_config(
    page_title="Resume Skill Analyzer",
    page_icon="📊",
    layout="wide"
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

st.title("🚀 Resume Skill Analyzer")
st.write("Simplified deployment for Streamlit Community Cloud")

# Basic functionality test
if st.button("Test Core Functionality"):
    try:
        # Test basic imports
        skill_extractor = SkillExtractor(os.path.join(current_dir, 'data', 'job_skills.json'))
        job_roles = skill_extractor.get_all_job_roles()
        st.success(f"✅ Core functionality working! Found {len(job_roles)} job roles.")
    except Exception as e:
        st.error(f"❌ Core test failed: {e}")

st.write("---")
st.write("This simplified version should deploy successfully to Streamlit Community Cloud.")
