# 🎯 AI-Powered Resume Skill Gap Analyzer

A comprehensive Python application that uses Natural Language Processing (NLP) to analyze resumes and identify skill gaps compared to job requirements. Built entirely with Python and Streamlit for a modern, professional dashboard experience.

## 🚀 Features

### Core Functionality
- **Resume Upload**: Support for PDF and text file formats
- **Skill Extraction**: Advanced NLP-based skill identification using:
  - Tokenization and stopword removal
  - Keyword-based extraction
  - TF-IDF and cosine similarity
  - Multi-word skill recognition
- **Job Role Analysis**: Compare against 9+ professional job roles
- **Gap Analysis**: Identify missing and matched skills with percentages
- **Visual Analytics**: Interactive charts and progress indicators
- **Smart Recommendations**: Personalized learning suggestions

### Technical Features
- **NLP Pipeline**: Complete text preprocessing with NLTK
- **Skill Matching**: Hybrid approach combining keyword and TF-IDF methods
- **Categorization**: Skills organized by technical domains
- **Export Options**: Download results as JSON or CSV reports
- **Professional UI**: Modern Streamlit dashboard with custom styling

## 📁 Project Structure

```
resume_skill_analyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── data/
│   └── job_skills.json            # Job roles and skills database
├── nlp_modules/
│   ├── __init__.py
│   ├── text_processor.py          # Text preprocessing utilities
│   └── skill_extractor.py         # Skill extraction engine
├── utils/
│   ├── __init__.py
│   ├── pdf_extractor.py           # PDF text extraction
│   └── skill_analyzer.py          # Gap analysis algorithms
└── samples/
    └── sample_resume.txt          # Sample resume for testing
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd resume_skill_analyzer

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📋 Dependencies

### Core Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualizations
- **nltk**: Natural language processing
- **scikit-learn**: Machine learning and TF-IDF
- **numpy**: Numerical computing

### PDF Processing
- **PyPDF2**: PDF text extraction (optional, for PDF support)

### Installation Commands
```bash
pip install streamlit pandas plotly nltk scikit-learn numpy PyPDF2
```

## 🎮 How to Use

### Step 1: Upload Your Resume
1. Click the file uploader in the sidebar
2. Choose your resume file (PDF or TXT format)
3. The system will automatically extract text

### Step 2: Select Job Role
1. Choose your target job role from the dropdown
2. View the job description and required skills
3. Available roles include:
   - Data Scientist
   - Software Engineer
   - Business Analyst
   - DevOps Engineer
   - Machine Learning Engineer
   - Full Stack Developer
   - Data Engineer
   - Product Manager
   - Cybersecurity Analyst

### Step 3: Analyze
1. Click the "Analyze Resume" button
2. Wait for the NLP processing to complete
3. View your comprehensive results

### Step 4: Review Results
The analysis includes:
- **Match Percentage**: Overall skill compatibility
- **Similarity Score**: TF-IDF based similarity
- **Proficiency Level**: Expert to Novice classification
- **Matched Skills**: Skills you have (green indicators)
- **Missing Skills**: Skills to learn (red indicators)
- **Category Analysis**: Breakdown by skill domains
- **Recommendations**: Personalized improvement suggestions

### Step 5: Export Results
- Download JSON report for detailed analysis
- Export CSV summary for spreadsheets

## 🔧 Technical Architecture

### NLP Pipeline
1. **Text Preprocessing**
   - Text cleaning and normalization
   - Tokenization using NLTK
   - Stopword removal with custom filters
   - N-gram extraction for multi-word skills

2. **Skill Extraction**
   - Keyword-based matching with variations
   - TF-IDF vectorization for semantic matching
   - Hybrid scoring combining both methods
   - Skill strength calculation

3. **Gap Analysis**
   - Percentage-based matching
   - Cosine similarity scoring
   - Category-wise breakdown
   - Proficiency level classification

### Data Sources
- **Job Skills Database**: 200+ skills across 9 job roles
- **Technical Categories**: 8 skill domains (programming, web, databases, etc.)
- **Skill Variations**: Common abbreviations and alternative names

## 📊 Sample Analysis

### Input Example
**Resume Text**: "Experienced Python developer with expertise in Django, React, PostgreSQL, and AWS cloud services. Strong knowledge of machine learning algorithms and data analysis using pandas."

**Target Role**: Data Scientist

### Output Results
- **Match Percentage**: 65%
- **Similarity Score**: 0.72
- **Proficiency Level**: Intermediate
- **Matched Skills**: Python, Machine Learning, Data Analysis, AWS
- **Missing Skills**: TensorFlow, PyTorch, Deep Learning, Statistics, NLP
- **Recommendations**: Focus on deep learning frameworks and statistical concepts

## 🎨 UI Features

### Dashboard Layout
- **Header**: Professional gradient design with app title
- **Sidebar**: Configuration panel with instructions
- **Main Area**: Results display with multiple sections
- **Footer**: Application information and credits

### Visual Elements
- **Progress Rings**: Circular indicators for metrics
- **Bar Charts**: Skill comparison visualization
- **Radar Charts**: Category coverage analysis
- **Skill Cards**: Color-coded skill indicators
- **Recommendation Boxes**: Actionable suggestions

### Interactive Features
- **Expandable Sections**: Detailed category analysis
- **File Upload**: Drag-and-drop support
- **Export Options**: Multiple format downloads
- **Responsive Design**: Works on all screen sizes

## 🔍 NLP Techniques Used

### 1. Text Processing
- **Tokenization**: Word and sentence segmentation
- **Normalization**: Case conversion and term standardization
- **Stopword Removal**: Custom filter for resume-specific terms
- **N-gram Generation**: Bigrams and trigrams for multi-word skills

### 2. Feature Extraction
- **TF-IDF Vectorization**: Term frequency-inverse document frequency
- **N-gram Range**: 1-3 grams for comprehensive coverage
- **Vocabulary Control**: Limited to relevant technical terms

### 3. Similarity Matching
- **Cosine Similarity**: Vector space similarity calculation
- **Hybrid Scoring**: Combined keyword and TF-IDF approaches
- **Skill Weighting**: Frequency and confidence-based scoring

## 🚀 Future Enhancements

### Planned Features
1. **Advanced NLP**
   - Named Entity Recognition (NER)
   - BERT-based skill extraction
   - Experience level detection

2. **Expanded Database**
   - More job roles and industries
   - Regional skill requirements
   - Salary correlation analysis

3. **Interactive Features**
   - Skill learning recommendations
   - Course suggestions integration
   - Resume improvement tips

4. **Advanced Analytics**
   - Career path suggestions
   - Market demand analysis
   - Skill trend tracking

### Technical Improvements
1. **Performance Optimization**
   - Caching mechanisms
   - Parallel processing
   - Database integration

2. **User Experience**
   - User accounts and history
   - Resume templates
   - Batch analysis

## 🐛 Troubleshooting

### Common Issues

#### PDF Extraction Problems
**Problem**: "PyPDF2 is not installed" error
**Solution**: Install PyPDF2 using `pip install PyPDF2`

**Problem**: Poor text extraction from scanned PDFs
**Solution**: Use OCR tools or convert to text format first

#### NLP Processing Issues
**Problem**: NLTK data not found
**Solution**: The application auto-downloads required NLTK data

**Problem**: Low skill extraction accuracy
**Solution**: Ensure resume contains clear skill keywords and technical terms

#### Performance Issues
**Problem**: Slow analysis on large resumes
**Solution**: The application processes text efficiently, but very large files may take time

### Error Messages
- **"Unsupported file type"**: Use only PDF or TXT files
- **"Error extracting text"**: Try a different file format
- **"No skills found"**: Ensure resume contains technical terms

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Ensure you're using Python 3.8+
4. Test with the provided sample resume

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Streamlit**: For the excellent web framework
- **NLTK**: For comprehensive NLP tools
- **Scikit-learn**: For machine learning utilities
- **Plotly**: For interactive visualizations

---

**Built with ❤️ using Python and Streamlit**
