"""
Home Page for AI Resume Skill Gap Analyzer
A beautiful landing page with features and navigation
"""

import streamlit as st
from utils.shared import set_custom_css, display_skill_cards

def show_home_page():
    """Display the home/landing page"""
    set_custom_css()
    
    # Hero Section
    st.markdown('<h1 class="main-header">🎯 AI Resume Skill Gap Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Transform your career with AI-powered skill analysis and personalized recommendations</p>', unsafe_allow_html=True)
    
    # Features Section
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
    
    # How It Works Section
    st.markdown('<h2 class="sub-header">📋 How It Works</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #60a5fa; margin-bottom: 1rem;">📄 Step 1</h3>
            <p style="color: #94a3b8; margin: 0;">Upload your resume in PDF or text format</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #60a5fa; margin-bottom: 1rem;">🎯 Step 2</h3>
            <p style="color: #94a3b8; margin: 0;">Select your target job role from our database</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #60a5fa; margin-bottom: 1rem;">🧠 Step 3</h3>
            <p style="color: #94a3b8; margin: 0;">AI analyzes your skills against requirements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #60a5fa; margin-bottom: 1rem;">📊 Step 4</h3>
            <p style="color: #94a3b8; margin: 0;">Get detailed insights and recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h2 style="color: #ffffff; margin-bottom: 1rem;">Ready to Transform Your Career?</h2>
            <p style="color: #94a3b8; margin-bottom: 2rem; font-size: 1.1rem;">
                Get personalized skill analysis and career recommendations in minutes
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            st.info("👆 Please navigate to the 'Analysis' page from the sidebar to begin your resume analysis.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="custom-footer">
        <strong>🎯 AI Resume Skill Gap Analyzer</strong><br>
        <span style="color: #94a3b8;">Powered by Advanced NLP Technology</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_home_page()
