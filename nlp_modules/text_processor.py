"""
Text Processing Module for Resume Skill Extraction
Handles tokenization, stopword removal, and text preprocessing
"""

import re
import string
from typing import List, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required NLTK data (only once)
# punkt_tab is required by newer NLTK versions for word_tokenize/sent_tokenize
for resource in ('punkt', 'punkt_tab', 'stopwords'):
    try:
        if resource == 'stopwords':
            nltk.data.find('corpora/stopwords')
        else:
            nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

class TextProcessor:
    """Advanced text processing for resume analysis"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # Add custom stopwords relevant to resumes
        custom_stopwords = {
            'experience', 'work', 'project', 'projects', 'team', 'teams',
            'company', 'companies', 'job', 'jobs', 'position', 'positions',
            'role', 'roles', 'responsibility', 'responsibilities', 'skill',
            'skills', 'ability', 'abilities', 'knowledge', 'knowledgeable',
            'year', 'years', 'month', 'months', 'period', 'duration',
            'including', 'include', 'included', 'various', 'multiple', 'several',
            'different', 'various', 'etc', 'also', 'well', 'good', 'excellent',
            'strong', 'solid', 'deep', 'extensive', 'hands', 'on', 'hand'
        }
        self.stop_words.update(custom_stopwords)
        
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text input
            
        Returns:
            Cleaned text
        """
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\+\#\/]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Convert to lowercase
        text = text.lower().strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        tokens = word_tokenize(text)
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from tokens
        
        Args:
            tokens: List of tokens
            
        Returns:
            Filtered tokens
        """
        filtered_tokens = [
            token for token in tokens 
            if token.lower() not in self.stop_words 
            and len(token) > 1  # Remove single characters
        ]
        return filtered_tokens
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        sentences = sent_tokenize(text)
        return [sent.strip() for sent in sentences if sent.strip()]
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Complete text preprocessing pipeline
        
        Args:
            text: Raw text input
            
        Returns:
            Processed tokens
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Remove stopwords
        filtered_tokens = self.remove_stopwords(tokens)
        
        return filtered_tokens
    
    def extract_ngrams(self, tokens: List[str], n: int = 2) -> List[str]:
        """
        Extract n-grams from tokens
        
        Args:
            tokens: List of tokens
            n: N-gram size
            
        Returns:
            List of n-grams
        """
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        return ngrams
    
    def normalize_skill_terms(self, text: str) -> str:
        """
        Normalize skill-related terms
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Common skill term variations
        normalizations = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine learning',
            'dl': 'deep learning',
            'nlp': 'natural language processing',
            'cv': 'computer vision',
            'ai': 'artificial intelligence',
            'ci/cd': 'ci/cd',
            'devops': 'devops',
            'ui/ux': 'ui ux',
            'fullstack': 'full stack',
            'full-stack': 'full stack',
            'back end': 'backend',
            'back-end': 'backend',
            'front end': 'frontend',
            'front-end': 'frontend',
        }
        
        normalized_text = text.lower()
        for old, new in normalizations.items():
            normalized_text = re.sub(r'\b' + re.escape(old) + r'\b', new, normalized_text)
        
        return normalized_text
