"""
Shared utilities for AI Resume Skill Gap Analyzer
Common functions and styling used across multiple pages
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List

def set_custom_css():
    """Apply attractive black theme styling"""
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --black: #000000;
            --black-soft: #050505;
            --black-card: #0d0d0d;
            --black-elevated: #141414;
            --black-border: #1a1a1a;
            --border: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(255, 255, 255, 0.15);
            --border-glow: rgba(255, 255, 255, 0.12);
            --text-primary: #ffffff;
            --text-secondary: #a3a3a3;
            --text-muted: #737373;
            --accent: #ffffff;
            --accent-subtle: rgba(255, 255, 255, 0.08);
            --success: #22c55e;
            --success-glow: rgba(34, 197, 94, 0.2);
            --warning: #eab308;
            --danger: #ef4444;
            --danger-glow: rgba(239, 68, 68, 0.2);
            --radius: 16px;
            --radius-sm: 10px;
            --shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
            --shadow-glow: 0 0 40px rgba(255, 255, 255, 0.03);
        }
        
        * {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }
        
        .stApp {
            background: var(--black) !important;
            color: var(--text-primary) !important;
        }
        
        .stApp > div { background: transparent !important; }
        .stBlock { background: transparent !important; }
        .stMarkdown { color: var(--text-primary) !important; }
        
        .stSelectbox > div > div > select {
            background: var(--black-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.65rem 1rem !important;
        }
        
        .stButton > button {
            background: var(--black-elevated) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            font-weight: 600 !important;
            border-radius: var(--radius-sm) !important;
            padding: 0.7rem 1.5rem !important;
            transition: all 0.25s ease !important;
        }
        
        .stButton > button:hover {
            background: var(--accent-subtle) !important;
            border-color: var(--border-hover) !important;
            box-shadow: var(--shadow-glow) !important;
        }
        
        .stButton > button[kind="primary"] {
            background: #ffffff !important;
            border: none !important;
            color: #000000 !important;
            font-weight: 700 !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: #e5e5e5 !important;
            color: #000000 !important;
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.15) !important;
        }
        
        .stFileUploader > div {
            background: var(--black-card) !important;
            border: 2px dashed var(--border) !important;
            border-radius: var(--radius) !important;
            padding: 2rem !important;
            transition: all 0.25s ease !important;
        }
        
        .stFileUploader > div:hover {
            border-color: var(--border-hover) !important;
            background: var(--black-elevated) !important;
        }
        
        .stSuccess { background: rgba(34, 197, 94, 0.1) !important; border-left: 4px solid var(--success) !important; }
        .stError { background: rgba(239, 68, 68, 0.1) !important; border-left: 4px solid var(--danger) !important; }
        .stInfo { background: var(--accent-subtle) !important; border-left: 4px solid var(--border-hover) !important; }
        
        .stDeployButton, #MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stFooter"] {
            display: none !important;
        }
        
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: 0.5rem;
            letter-spacing: -0.03em;
            line-height: 1.1;
            text-shadow: 0 2px 20px rgba(255, 255, 255, 0.05);
        }
        
        .hero-subtitle {
            font-size: 1.15rem;
            color: var(--text-secondary);
            text-align: center;
            margin-bottom: 3rem;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
            font-weight: 400;
        }
        
        .sub-header {
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1.25rem;
            letter-spacing: -0.02em;
        }
        
        .metric-card {
            background: var(--black-card);
            padding: 1.5rem;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            margin-bottom: 1rem;
            transition: all 0.25s ease;
            box-shadow: var(--shadow);
        }
        
        .metric-card:hover {
            border-color: var(--border-hover);
            box-shadow: var(--shadow-glow);
        }
        
        .feature-card {
            background: var(--black-card);
            padding: 2rem;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            margin-bottom: 1.5rem;
            text-align: center;
            transition: all 0.25s ease;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        }
        
        .feature-card:hover {
            border-color: var(--border-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow);
        }
        
        .feature-icon {
            font-size: 2.25rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        
        .feature-description {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.55;
        }
        
        .stat-item {
            background: var(--black-card);
            padding: 1.5rem;
            border-radius: var(--radius);
            text-align: center;
            border: 1px solid var(--border);
            transition: all 0.25s ease;
            box-shadow: var(--shadow);
        }
        
        .stat-item:hover {
            border-color: var(--border-hover);
        }
        
        .stat-number {
            font-size: 2.25rem;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.02em;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 500;
            margin-top: 0.25rem;
        }
        
        .job-role-card {
            background: var(--black-card);
            padding: 1.25rem;
            border-radius: var(--radius);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
        }
        
        .job-role-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
        }
        
        .job-role-meta { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
        
        .job-role-badge {
            background: var(--black-elevated);
            color: var(--text-secondary);
            padding: 0.25rem 0.65rem;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 500;
            border: 1px solid var(--border);
        }
        
        .job-role-description {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .skill-match { color: var(--success); font-weight: 600; }
        .skill-missing { color: var(--danger); font-weight: 600; }
        
        .recommendation-box {
            background: var(--black-card);
            border-left: 3px solid rgba(255,255,255,0.3);
            padding: 1rem 1.25rem;
            margin: 0.75rem 0;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
        }
        
        .custom-footer {
            text-align: center;
            color: var(--text-muted);
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid var(--border);
            font-size: 0.9rem;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in { animation: fadeIn 0.5s ease-out; }
        
        .skill-pill {
            display: inline-block;
            padding: 0.4rem 0.85rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            margin: 0.25rem;
            border: 1px solid transparent;
        }
        
        .skill-pill-match {
            background: rgba(34, 197, 94, 0.15);
            color: var(--success);
            border-color: rgba(34, 197, 94, 0.3);
        }
        
        .skill-pill-missing {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border-color: rgba(239, 68, 68, 0.25);
        }
        
        @media (max-width: 768px) {
            .main-header { font-size: 2.25rem; }
            .hero-subtitle { font-size: 1rem; margin-bottom: 2rem; }
            .sub-header { font-size: 1.1rem; }
            .stat-number { font-size: 1.75rem; }
            .feature-card, .metric-card { padding: 1.25rem; }
        }
        
        hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--black-soft); }
        ::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 4px; }

        /* Force-hide sidebar and navigation icons */
        [data-testid="stSidebar"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stPageLink"],
        [data-testid="stPageIcon"] {
            display: none !important;
        }

        /* Hide any heading/link icons that look like infinity symbols */
        h1 svg, h2 svg, h3 svg, h4 svg, h5 svg, h6 svg {
            display: none !important;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            ['[data-testid="stHeader"]', '[data-testid="stFooter"]', '.stDeployButton', '#MainMenu'].forEach(s => {
                document.querySelectorAll(s).forEach(el => { el.style.display = 'none'; });
            });
        });
    </script>
    """, unsafe_allow_html=True)

def create_progress_ring(percentage: float, title: str) -> go.Figure:
    """Create a circular progress indicator"""
    color = '#22c55e' if percentage >= 70 else '#eab308' if percentage >= 40 else '#ef4444'
    fig = go.Figure(data=[go.Pie(
        values=[percentage, 100 - percentage],
        hole=0.75,
        showlegend=False,
        textinfo='none',
        marker_colors=[color, 'rgba(13, 13, 13, 0.8)']
    )])
    
    fig.add_annotation(text=f"<b>{int(percentage)}%</b>", x=0.5, y=0.52, font_size=18, font_color='#ffffff', showarrow=False)
    fig.add_annotation(text=title, x=0.5, y=0.28, font_size=11, font_color='#a3a3a3', showarrow=False)
    
    fig.update_layout(
        height=180,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family='Outfit, sans-serif'
    )
    
    return fig

def create_skill_bar_chart(matched_skills: List[str], missing_skills: List[str]) -> go.Figure:
    """Create a bar chart for skills"""
    fig = go.Figure(data=[
        go.Bar(
            x=['Matched', 'Missing'],
            y=[len(matched_skills), len(missing_skills)],
            marker_color=['#22c55e', '#ef4444'],
            text=[len(matched_skills), len(missing_skills)],
            textposition='auto',
            textfont=dict(color='#ffffff', size=14)
        )
    ])
    
    fig.update_layout(
        title=dict(text="Skill Overview", font=dict(size=14, color='#ffffff')),
        height=350,
        showlegend=False,
        plot_bgcolor='#0d0d0d',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#a3a3a3',
        xaxis=dict(tickfont_color='#a3a3a3', gridcolor='rgba(255,255,255,0.06)'),
        yaxis=dict(tickfont_color='#a3a3a3', gridcolor='rgba(255,255,255,0.06)')
    )
    
    return fig

def create_skill_radar_chart(skill_analysis: Dict, skill_categories: Dict) -> go.Figure:
    """Create radar chart for skill categories"""
    if not skill_categories:
        return go.Figure()
    
    categories = list(skill_categories.keys())
    values = [cat_data['match_percentage'] for cat_data in skill_categories.values()]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Coverage',
        line_color='#ffffff',
        fillcolor='rgba(255, 255, 255, 0.12)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont_color='#a3a3a3', gridcolor='rgba(255,255,255,0.08)'),
            angularaxis=dict(tickfont_color='#a3a3a3', gridcolor='rgba(255,255,255,0.08)')
        ),
        title=dict(text="Category Coverage", font=dict(size=14, color='#ffffff')),
        height=350,
        plot_bgcolor='#0d0d0d',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#a3a3a3'
    )
    
    return fig

def display_skill_cards(skills: List[str], title: str, color_class: str):
    """Display skills as clean pills"""
    pill_class = "skill-pill-match" if "match" in color_class else "skill-pill-missing"
    
    if not skills:
        st.markdown(f"""
        <div class="metric-card" style="opacity: 0.8;">
            <p style="color: #737373; margin: 0; font-size: 0.9rem;">{title} — None found</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"<p style='font-weight: 600; color: #a3a3a3; margin-bottom: 0.75rem; font-size: 0.9rem;'>{title} ({len(skills)})</p>", unsafe_allow_html=True)
    
    pills_html = "".join([
        f'<span class="skill-pill {pill_class}">{s.strip()}</span>'
        for s in skills if s and s.strip()
    ])
    st.markdown(f'<div style="line-height: 2.2;">{pills_html}</div>', unsafe_allow_html=True)
