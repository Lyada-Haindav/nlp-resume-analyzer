# Deploy Resume Skill Analyzer to Vercel

## Prerequisites
- Vercel account
- GitHub repository (recommended)
- Vercel CLI installed (optional)

## Deployment Steps

### Option 1: Using Vercel CLI
1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy from project root:
   ```bash
   vercel --prod
   ```

### Option 2: Using Vercel Dashboard
1. Push your code to GitHub
2. Connect your GitHub account to Vercel
3. Import the repository
4. Vercel will auto-detect the Python framework
5. Deploy

## Project Structure
```
resume_skill_analyzer/
├── api/
│   ├── index.py              # Flask entry point
│   └── templates/
│       └── index.html        # Landing page
├── nlp_modules/              # NLP processing modules
├── utils/                    # Utility modules
├── data/                     # Job skills data
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
└── README_DEPLOY.md         # This file
```

## Important Notes
- The Flask wrapper serves as the entry point for Vercel
- Streamlit runs in the background when accessed via the API
- All dependencies are specified in requirements.txt
- The deployment includes a beautiful landing page

## Environment Variables
If needed, set environment variables in Vercel dashboard:
- `PYTHON_VERSION`: 3.9
- Any other required environment variables

## Post-Deployment
1. Test the deployed application
2. Monitor logs in Vercel dashboard
3. Set up custom domain if needed

## Troubleshooting
- Check Vercel function logs for errors
- Ensure all dependencies are in requirements.txt
- Verify file paths are correct for serverless environment
