#!/bin/bash

echo "🚀 Deploying Resume Skill Analyzer to Streamlit Community Cloud"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Installing..."
    pip install streamlit
fi

# Deploy to Streamlit Community Cloud
echo "📤 Deploying to Streamlit Community Cloud..."
echo "🌐 This will open your browser to complete the deployment"

# Open browser for deployment
open "https://share.streamlit.io/"

echo ""
echo "✅ Next steps:"
echo "1. Click 'Deploy an app' in your browser"
echo "2. Connect your GitHub repository"
echo "3. Select this repository"
echo "4. Your app will be deployed at: https://your-app-name.streamlit.app"
echo ""
echo "📋 Make sure your repository is pushed to GitHub first:"
echo "   git add ."
echo "   git commit -m 'Ready for Streamlit deployment'"
echo "   git push origin main"
