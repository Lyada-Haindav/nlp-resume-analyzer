import streamlit as st
import os
import sys

# Add modules to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'nlp_modules'))
sys.path.append(os.path.join(current_dir, 'utils'))

def main():
    st.set_page_config(
        page_title="Test Deployment",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("🧪 Test Deployment")
    st.write("This is a test to verify deployment functionality.")
    st.write(f"Current directory: {current_dir}")
    st.write("Python path: {sys.path}")
    
    # Test imports
    try:
        from nlp_modules.skill_extractor import SkillExtractor
        from utils.skill_analyzer import SkillAnalyzer
        st.success("✅ All imports successful!")
    except Exception as e:
        st.error(f"❌ Import error: {e}")
    
    # Test data access
    try:
        job_skills_path = os.path.join(current_dir, 'data', 'job_skills.json')
        if os.path.exists(job_skills_path):
            st.success("✅ Data files accessible!")
        else:
            st.error("❌ Data files not found!")
    except Exception as e:
        st.error(f"❌ Data access error: {e}")

if __name__ == "__main__":
    main()
