"""
Skill Extraction Module for Resume Analysis
Uses keyword-based extraction and TF-IDF for skill identification
"""

import json
import re
from typing import List, Dict, Set, Tuple
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .text_processor import TextProcessor

class SkillExtractor:
    """Advanced skill extraction using NLP techniques"""
    
    def __init__(self, job_skills_path: str):
        """
        Initialize skill extractor with job skills database
        
        Args:
            job_skills_path: Path to job_skills.json file
        """
        self.text_processor = TextProcessor()
        self.job_skills_data = self._load_job_skills(job_skills_path)
        self.all_skills = self._extract_all_skills()
        
        # Initialize TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),  # Extract unigrams, bigrams, and trigrams
            max_features=1000,
            stop_words='english'
        )
        
    def _load_job_skills(self, path: str) -> Dict:
        """Load job skills database"""
        with open(path, 'r') as f:
            return json.load(f)
    
    def _extract_all_skills(self) -> Set[str]:
        """Extract all unique skills from job database"""
        all_skills = set()
        
        # Add skills from technical database
        for category, skills in self.job_skills_data['technical_skills_database'].items():
            all_skills.update(skills)
        
        # Add skills from job roles
        for role_data in self.job_skills_data['job_roles'].values():
            all_skills.update(role_data['required_skills'])
        
        return all_skills
    
    def extract_skills_keyword_based(self, text: str) -> Dict[str, int]:
        """
        Extract skills using keyword matching
        
        Args:
            text: Resume text
            
        Returns:
            Dictionary of skills and their frequencies
        """
        # Normalize text
        normalized_text = self.text_processor.normalize_skill_terms(text.lower())
        
        # Preprocess text
        tokens = self.text_processor.preprocess_text(normalized_text)
        
        # Create n-grams for multi-word skills
        bigrams = self.text_processor.extract_ngrams(tokens, 2)
        trigrams = self.text_processor.extract_ngrams(tokens, 3)
        
        # Combine all potential skill terms
        all_terms = tokens + bigrams + trigrams
        
        # Count skill occurrences
        skill_counts = {}
        
        for skill in self.all_skills:
            skill_lower = skill.lower()
            skill_variations = self._get_skill_variations(skill_lower)
            
            count = 0
            for variation in skill_variations:
                # Count exact matches
                count += sum(1 for term in all_terms if variation in term)
                
                # Count in original text (for cases where tokenization might miss)
                count += len(re.findall(r'\b' + re.escape(variation) + r'\b', normalized_text))
            
            if count > 0:
                skill_counts[skill] = count
        
        return skill_counts
    
    def _get_skill_variations(self, skill: str) -> List[str]:
        """Get variations of a skill term for better matching"""
        variations = [skill]
        
        # Common variations
        if 'python' in skill:
            variations.extend(['py', 'python3'])
        elif 'javascript' in skill:
            variations.extend(['js', 'javascript', 'ecmascript'])
        elif 'typescript' in skill:
            variations.extend(['ts', 'typescript'])
        elif 'machine learning' in skill:
            variations.extend(['ml', 'machine learning'])
        elif 'deep learning' in skill:
            variations.extend(['dl', 'deep learning'])
        elif 'react' in skill:
            variations.extend(['reactjs', 'react.js'])
        elif 'node' in skill:
            variations.extend(['nodejs', 'node.js'])
        elif 'aws' in skill:
            variations.extend(['amazon web services', 'amazon aws'])
        
        return variations
    
    def extract_skills_tfidf(self, text: str, top_k: int = 50) -> List[Tuple[str, float]]:
        """
        Extract skills using TF-IDF similarity
        
        Args:
            text: Resume text
            top_k: Number of top skills to return
            
        Returns:
            List of (skill, score) tuples
        """
        # Prepare documents
        documents = [text] + list(self.all_skills)
        
        # Fit TF-IDF
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
            
            # Calculate similarity between resume and each skill
            resume_vector = tfidf_matrix[0:1]
            skill_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(resume_vector, skill_vectors)[0]
            
            # Get top skills
            skill_scores = list(zip(self.all_skills, similarities))
            skill_scores.sort(key=lambda x: x[1], reverse=True)
            
            return skill_scores[:top_k]
            
        except Exception as e:
            print(f"TF-IDF extraction failed: {e}")
            return []
    
    def extract_skills_combined(self, text: str, min_frequency: int = 1) -> Dict[str, float]:
        """
        Combine keyword and TF-IDF methods for robust skill extraction
        
        Args:
            text: Resume text
            min_frequency: Minimum frequency for keyword-based extraction
            
        Returns:
            Dictionary of skills and combined scores
        """
        # Keyword-based extraction
        keyword_skills = self.extract_skills_keyword_based(text)
        
        # TF-IDF extraction
        tfidf_skills = self.extract_skills_tfidf(text)
        
        # Combine results
        combined_skills = {}
        
        # Add keyword-based skills with frequency weighting
        max_freq = max(keyword_skills.values()) if keyword_skills else 1
        for skill, freq in keyword_skills.items():
            if freq >= min_frequency:
                combined_skills[skill] = freq / max_freq
        
        # Add TF-IDF skills with similarity weighting
        for skill, score in tfidf_skills:
            if skill not in combined_skills:
                combined_skills[skill] = score * 0.5  # Lower weight for TF-IDF only
            else:
                # Boost existing skills with TF-IDF score
                combined_skills[skill] = min(1.0, combined_skills[skill] + score * 0.3)
        
        return combined_skills
    
    def get_job_role_skills(self, job_role: str) -> List[str]:
        """Get required skills for a specific job role"""
        if job_role in self.job_skills_data['job_roles']:
            return self.job_skills_data['job_roles'][job_role]['required_skills']
        return []
    
    def get_job_role_description(self, job_role: str) -> str:
        """Get description for a specific job role"""
        if job_role in self.job_skills_data['job_roles']:
            return self.job_skills_data['job_roles'][job_role]['description']
        return ""
    
    def get_all_job_roles(self) -> List[str]:
        """Get list of all available job roles"""
        return list(self.job_skills_data['job_roles'].keys())
    
    def categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """
        Categorize skills into technical categories
        
        Args:
            skills: List of skills to categorize
            
        Returns:
            Dictionary of categories and their skills
        """
        categorized = {}
        
        for category, category_skills in self.job_skills_data['technical_skills_database'].items():
            category_name = category.replace('_', ' ').title()
            matched_skills = [skill for skill in skills if skill in category_skills]
            if matched_skills:
                categorized[category_name] = matched_skills
        
        return categorized
