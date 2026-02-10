"""
Main entry point for AI Resume Skill Gap Analyzer
Redirects to home page
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Resume Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# Redirect to home page
st.switch_page("pages/home.py")
