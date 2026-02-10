"""
PDF Text Extraction Module
Handles PDF text extraction for resume processing
"""

import io
from typing import Optional
import streamlit as st

# Try to import PyPDF2, provide fallback if not available
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

class PDFExtractor:
    """PDF text extraction utility"""
    
    @staticmethod
    def is_available() -> bool:
        """Check if PDF extraction is available"""
        return PYPDF2_AVAILABLE
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Optional[str]:
        """
        Extract text from PDF file
        
        Args:
            pdf_file: Uploaded PDF file
            
        Returns:
            Extracted text or None if extraction fails
        """
        if not PYPDF2_AVAILABLE:
            st.error("PyPDF2 is not installed. Please install it using: pip install PyPDF2")
            return None
        
        try:
            # Read PDF file
            pdf_bytes = pdf_file.read()
            pdf_stream = io.BytesIO(pdf_bytes)
            
            # Create PDF reader
            pdf_reader = PyPDF2.PdfReader(pdf_stream)
            
            # Extract text from all pages
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text += page_text + "\n"
            
            return text.strip()
            
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    @staticmethod
    def extract_text_from_uploaded_file(uploaded_file) -> Optional[str]:
        """
        Extract text from uploaded file (PDF or text)
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Extracted text or None if extraction fails
        """
        if uploaded_file is None:
            return None
        
        # Check file type
        file_type = uploaded_file.type
        
        if file_type == "application/pdf":
            return PDFExtractor.extract_text_from_pdf(uploaded_file)
        elif file_type in ["text/plain", "text/csv"]:
            # For text files, read directly
            try:
                # Handle different encodings
                text = uploaded_file.read().decode('utf-8')
                return text
            except UnicodeDecodeError:
                try:
                    text = uploaded_file.read().decode('latin-1')
                    return text
                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
                    return None
        else:
            st.error(f"Unsupported file type: {file_type}. Please upload PDF or text files.")
            return None
