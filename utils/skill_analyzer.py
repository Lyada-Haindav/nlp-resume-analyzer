"""
Skill Gap Analysis Module
Handles skill matching, gap analysis, and similarity calculations
"""

from typing import Dict, List, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class SkillAnalyzer:
    """Skill gap analysis and matching engine"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True
        )
    
    def calculate_skill_match_percentage(self, resume_skills: List[str], 
                                       required_skills: List[str]) -> float:
        """
        Calculate the percentage of required skills found in resume
        
        Args:
            resume_skills: Skills extracted from resume
            required_skills: Skills required for the job
            
        Returns:
            Match percentage (0-100)
        """
        if not required_skills:
            return 0.0
        
        # Convert to lowercase for comparison
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        # Count matches
        matches = 0
        for req_skill in required_skills_lower:
            if req_skill in resume_skills_lower:
                matches += 1
        
        # Calculate percentage
        match_percentage = (matches / len(required_skills)) * 100
        return round(match_percentage, 2)
    
    def find_matched_skills(self, resume_skills: List[str], 
                          required_skills: List[str]) -> List[str]:
        """
        Find skills that match between resume and job requirements
        
        Args:
            resume_skills: Skills extracted from resume
            required_skills: Skills required for the job
            
        Returns:
            List of matched skills
        """
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        matched = []
        for req_skill in required_skills_lower:
            if req_skill in resume_skills_lower:
                # Find the original case version
                original_skill = next(
                    (skill for skill in required_skills if skill.lower() == req_skill),
                    req_skill
                )
                matched.append(original_skill)
        
        return matched
    
    def find_missing_skills(self, resume_skills: List[str], 
                           required_skills: List[str]) -> List[str]:
        """
        Find required skills that are missing from the resume
        
        Args:
            resume_skills: Skills extracted from resume
            required_skills: Skills required for the job
            
        Returns:
            List of missing skills
        """
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        missing = []
        for req_skill in required_skills_lower:
            if req_skill not in resume_skills_lower:
                # Find the original case version
                original_skill = next(
                    (skill for skill in required_skills if skill.lower() == req_skill),
                    req_skill
                )
                missing.append(original_skill)
        
        return missing
    
    def calculate_skill_similarity_score(self, resume_skills: Dict[str, float], 
                                       required_skills: List[str]) -> float:
        """
        Calculate similarity score using TF-IDF and cosine similarity
        
        Args:
            resume_skills: Dictionary of skills and their scores
            required_skills: List of required skills
            
        Returns:
            Similarity score (0-1)
        """
        if not resume_skills or not required_skills:
            return 0.0
        
        # Create text representations
        resume_text = ' '.join([skill * int(score * 5) for skill, score in resume_skills.items()])
        required_text = ' '.join(required_skills)
        
        if not resume_text.strip() or not required_text.strip():
            return 0.0
        
        try:
            # Calculate TF-IDF vectors
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([resume_text, required_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
            
        except Exception:
            return 0.0
    
    def analyze_skill_gaps(self, resume_skills: Dict[str, float], 
                          required_skills: List[str]) -> Dict:
        """
        Perform comprehensive skill gap analysis
        
        Args:
            resume_skills: Dictionary of skills and their scores
            required_skills: List of required skills
            
        Returns:
            Dictionary containing analysis results
        """
        # Convert resume skills dict to list
        resume_skill_list = list(resume_skills.keys())
        
        # Calculate metrics
        match_percentage = self.calculate_skill_match_percentage(resume_skill_list, required_skills)
        matched_skills = self.find_matched_skills(resume_skill_list, required_skills)
        missing_skills = self.find_missing_skills(resume_skill_list, required_skills)
        similarity_score = self.calculate_skill_similarity_score(resume_skills, required_skills)
        
        # Calculate skill strength for matched skills
        skill_strengths = {}
        for skill in matched_skills:
            if skill.lower() in [s.lower() for s in resume_skills.keys()]:
                # Find the skill in resume_skills (case-insensitive)
                resume_skill = next(
                    (s for s in resume_skills.keys() if s.lower() == skill.lower()),
                    skill
                )
                skill_strengths[skill] = resume_skills.get(resume_skill, 0.0)
        
        # Determine proficiency level
        if match_percentage >= 80:
            proficiency_level = "Expert"
            proficiency_color = "#10b981"  # Green
        elif match_percentage >= 60:
            proficiency_level = "Advanced"
            proficiency_color = "#3b82f6"  # Blue
        elif match_percentage >= 40:
            proficiency_level = "Intermediate"
            proficiency_color = "#f59e0b"  # Orange
        elif match_percentage >= 20:
            proficiency_level = "Beginner"
            proficiency_color = "#ef4444"  # Red
        else:
            proficiency_level = "Novice"
            proficiency_color = "#6b7280"  # Gray
        
        return {
            'match_percentage': match_percentage,
            'similarity_score': similarity_score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'skill_strengths': skill_strengths,
            'total_required_skills': len(required_skills),
            'total_matched_skills': len(matched_skills),
            'total_missing_skills': len(missing_skills),
            'proficiency_level': proficiency_level,
            'proficiency_color': proficiency_color,
            'recommendations': self._generate_recommendations(missing_skills, match_percentage)
        }
    
    def _generate_recommendations(self, missing_skills: List[str], match_percentage: float) -> List[str]:
        """
        Generate personalized recommendations based on skill gaps
        
        Args:
            missing_skills: List of missing skills
            match_percentage: Current match percentage
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if match_percentage < 30:
            recommendations.append("Consider taking foundational courses in your target field")
            recommendations.append("Focus on learning the core technologies first")
        elif match_percentage < 50:
            recommendations.append("You have some relevant skills - build on them")
            recommendations.append("Consider intermediate-level courses for missing skills")
        elif match_percentage < 70:
            recommendations.append("Good progress! Focus on advanced topics")
            recommendations.append("Work on projects that combine multiple skills")
        else:
            recommendations.append("Excellent match! Consider specializing further")
            recommendations.append("Look into leadership or architectural roles")
        
        # Specific skill recommendations
        if len(missing_skills) > 0:
            top_missing = missing_skills[:3]  # Top 3 missing skills
            recommendations.append(f"Priority skills to learn: {', '.join(top_missing)}")
        
        return recommendations
    
    def get_skill_category_analysis(self, resume_skills: Dict[str, float], 
                                  required_skills: List[str],
                                  skill_categories: Dict[str, List[str]]) -> Dict:
        """
        Analyze skills by category
        
        Args:
            resume_skills: Dictionary of skills and their scores
            required_skills: List of required skills
            skill_categories: Dictionary of skill categories
            
        Returns:
            Category-wise analysis
        """
        category_analysis = {}
        
        for category, category_skills in skill_categories.items():
            # Find required skills in this category
            required_in_category = [skill for skill in required_skills if skill in category_skills]
            
            if required_in_category:
                # Find matched skills in this category
                resume_skill_list = list(resume_skills.keys())
                matched_in_category = self.find_matched_skills(resume_skill_list, required_in_category)
                
                # Calculate category match percentage
                category_match = self.calculate_skill_match_percentage(
                    matched_in_category, required_in_category
                )
                
                category_analysis[category] = {
                    'required_skills': required_in_category,
                    'matched_skills': matched_in_category,
                    'missing_skills': self.find_missing_skills(matched_in_category, required_in_category),
                    'match_percentage': category_match,
                    'total_required': len(required_in_category),
                    'total_matched': len(matched_in_category)
                }
        
        return category_analysis
