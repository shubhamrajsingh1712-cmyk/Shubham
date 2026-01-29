"""
Advanced Scoring Engine for Psychometric Assessment
Implements sophisticated scoring with interpretive bands and analysis
"""

from typing import Dict, List, Any, Tuple
import statistics

class ScoringEngine:
    """Advanced scoring engine with interpretive analysis"""
    
    # Interpretive bands
    BAND_LOW = "Low"
    BAND_MODERATE = "Moderate" 
    BAND_HIGH = "High"
    
    # Band thresholds (percentage)
    LOW_THRESHOLD = 40
    HIGH_THRESHOLD = 70
    
    def __init__(self):
        self.category_weights = {
            "orientation": {
                "creative": 1.2,
                "analytical": 1.2,
                "people_centric": 1.1,
                "administrative": 1.0
            },
            "interest": {
                "stem": 1.0,
                "arts_humanities": 1.0,
                "business_commerce": 1.0,
                "healthcare": 1.0,
                "social_service": 1.0
            },
            "personality": {
                "decision_making": 1.2,
                "perseverance": 1.2,
                "integrity": 1.3,
                "leadership": 1.1,
                "teamwork": 1.1,
                "emotional_stability": 1.2,
                "risk_appetite": 1.0,
                "self_discipline": 1.2
            },
            "aptitude": {
                "verbal_reasoning": 1.0,
                "numerical_ability": 1.0,
                "logical_reasoning": 1.1,
                "abstract_thinking": 1.0,
                "spatial_visualization": 1.0,
                "technological_understanding": 1.0,
                "perceptual_speed": 1.0
            },
            "eq": {
                "emotional_awareness": 1.2,
                "emotional_regulation": 1.2,
                "empathy": 1.1,
                "social_skills": 1.0,
                "motivation": 1.1,
                "conflict_management": 1.1
            }
        }
    
    def calculate_scores(self, test_type: str, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive scores for a test
        Returns: {
            'raw_scores': {},
            'normalized_scores': {},
            'interpretive_bands': {},
            'dominant_traits': [],
            'analysis': {}
        }
        """
        if test_type == "orientation":
            return self._score_orientation(responses)
        elif test_type == "interest":
            return self._score_interest(responses)
        elif test_type == "personality":
            return self._score_personality(responses)
        elif test_type == "aptitude":
            return self._score_aptitude(responses)
        elif test_type == "eq":
            return self._score_eq(responses)
        else:
            return {}
    
    def _score_orientation(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Score orientation assessment"""
        categories = ["creative", "analytical", "people_centric", "administrative"]
        raw_scores = {cat: [] for cat in categories}
        
        # Collect scores by category
        for response in responses:
            question_id = response.get("question_id", "")
            score = response.get("response", 3)
            
            for category in categories:
                if category.replace("_", "") in question_id.lower().replace("_", ""):
                    # Apply weight
                    weighted_score = score * self.category_weights["orientation"].get(category, 1.0)
                    raw_scores[category].append(weighted_score)
                    break
        
        # Calculate averages and normalize
        normalized_scores = {}
        for category, scores in raw_scores.items():
            if scores:
                avg_score = statistics.mean(scores)
                # Normalize to 0-100 scale (5-point scale max = 5, weighted max ~6)
                normalized = (avg_score / 6.0) * 100
                normalized_scores[category] = round(min(normalized, 100), 2)
            else:
                normalized_scores[category] = 50.0
        
        # Get interpretive bands
        bands = self._get_interpretive_bands(normalized_scores)
        
        # Identify dominant traits
        dominant = self._identify_dominant_traits(normalized_scores, top_n=2)
        
        # Detect conflicts
        conflicts = self._detect_conflicts(normalized_scores)
        
        return {
            "raw_scores": {k: round(statistics.mean(v) if v else 0, 2) for k, v in raw_scores.items()},
            "normalized_scores": normalized_scores,
            "interpretive_bands": bands,
            "dominant_traits": dominant,
            "conflicts": conflicts,
            "analysis": self._generate_orientation_analysis(normalized_scores, dominant)
        }
    
    def _score_interest(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Score interest assessment"""
        categories = ["stem", "arts_humanities", "business_commerce", "healthcare", "social_service"]
        raw_scores = {cat: [] for cat in categories}
        
        for response in responses:
            question_id = response.get("question_id", "")
            score = response.get("response", 3)
            
            for category in categories:
                if category.replace("_", "") in question_id.lower().replace("_", ""):
                    raw_scores[category].append(score)
                    break
        
        normalized_scores = {}
        for category, scores in raw_scores.items():
            if scores:
                avg_score = statistics.mean(scores)
                normalized = (avg_score / 5.0) * 100
                normalized_scores[category] = round(normalized, 2)
            else:
                normalized_scores[category] = 50.0
        
        bands = self._get_interpretive_bands(normalized_scores)
        dominant = self._identify_dominant_traits(normalized_scores, top_n=3)
        
        return {
            "raw_scores": {k: round(statistics.mean(v) if v else 0, 2) for k, v in raw_scores.items()},
            "normalized_scores": normalized_scores,
            "interpretive_bands": bands,
            "dominant_traits": dominant,
            "analysis": self._generate_interest_analysis(normalized_scores, dominant)
        }
    
    def _score_personality(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Score personality assessment"""
        traits = [
            "decision_making", "perseverance", "integrity", "leadership",
            "teamwork", "emotional_stability", "risk_appetite", "self_discipline"
        ]
        raw_scores = {trait: [] for trait in traits}
        
        for response in responses:
            question_id = response.get("question_id", "")
            score = response.get("response", 3)
            
            for trait in traits:
                if trait.replace("_", "") in question_id.lower().replace("_", ""):
                    weighted_score = score * self.category_weights["personality"].get(trait, 1.0)
                    raw_scores[trait].append(weighted_score)
                    break
        
        normalized_scores = {}
        for trait, scores in raw_scores.items():
            if scores:
                avg_score = statistics.mean(scores)
                # Account for weights (max ~6.5 for integrity)
                normalized = (avg_score / 6.5) * 100
                normalized_scores[trait] = round(min(normalized, 100), 2)
            else:
                normalized_scores[trait] = 50.0
        
        bands = self._get_interpretive_bands(normalized_scores)
        dominant = self._identify_dominant_traits(normalized_scores, top_n=3)
        conflicts = self._detect_conflicts(normalized_scores)
        
        return {
            "raw_scores": {k: round(statistics.mean(v) if v else 0, 2) for k, v in raw_scores.items()},
            "normalized_scores": normalized_scores,
            "interpretive_bands": bands,
            "dominant_traits": dominant,
            "conflicts": conflicts,
            "analysis": self._generate_personality_analysis(normalized_scores, dominant)
        }
    
    def _score_aptitude(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Score aptitude assessment"""
        abilities = [
            "verbal_reasoning", "numerical_ability", "logical_reasoning",
            "abstract_thinking", "spatial_visualization", 
            "technological_understanding", "perceptual_speed"
        ]
        raw_scores = {ability: [] for ability in abilities}
        
        for response in responses:
            question_id = response.get("question_id", "")
            score = response.get("response", 3)
            
            for ability in abilities:
                if ability.replace("_", "") in question_id.lower().replace("_", ""):
                    raw_scores[ability].append(score)
                    break
        
        normalized_scores = {}
        for ability, scores in raw_scores.items():
            if scores:
                avg_score = statistics.mean(scores)
                normalized = (avg_score / 5.0) * 100
                normalized_scores[ability] = round(normalized, 2)
            else:
                normalized_scores[ability] = 50.0
        
        bands = self._get_interpretive_bands(normalized_scores)
        dominant = self._identify_dominant_traits(normalized_scores, top_n=3)
        
        return {
            "raw_scores": {k: round(statistics.mean(v) if v else 0, 2) for k, v in raw_scores.items()},
            "normalized_scores": normalized_scores,
            "interpretive_bands": bands,
            "dominant_traits": dominant,
            "analysis": self._generate_aptitude_analysis(normalized_scores, dominant)
        }
    
    def _score_eq(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Score emotional intelligence assessment"""
        factors = [
            "emotional_awareness", "emotional_regulation", "empathy",
            "social_skills", "motivation", "conflict_management"
        ]
        raw_scores = {factor: [] for factor in factors}
        
        for response in responses:
            question_id = response.get("question_id", "")
            score = response.get("response", 3)
            
            for factor in factors:
                if factor.replace("_", "") in question_id.lower().replace("_", ""):
                    weighted_score = score * self.category_weights["eq"].get(factor, 1.0)
                    raw_scores[factor].append(weighted_score)
                    break
        
        normalized_scores = {}
        for factor, scores in raw_scores.items():
            if scores:
                avg_score = statistics.mean(scores)
                normalized = (avg_score / 6.0) * 100
                normalized_scores[factor] = round(min(normalized, 100), 2)
            else:
                normalized_scores[factor] = 50.0
        
        bands = self._get_interpretive_bands(normalized_scores)
        dominant = self._identify_dominant_traits(normalized_scores, top_n=3)
        
        return {
            "raw_scores": {k: round(statistics.mean(v) if v else 0, 2) for k, v in raw_scores.items()},
            "normalized_scores": normalized_scores,
            "interpretive_bands": bands,
            "dominant_traits": dominant,
            "analysis": self._generate_eq_analysis(normalized_scores, dominant)
        }
    
    def _get_interpretive_bands(self, scores: Dict[str, float]) -> Dict[str, str]:
        """Convert scores to interpretive bands"""
        bands = {}
        for key, score in scores.items():
            if score < self.LOW_THRESHOLD:
                bands[key] = self.BAND_LOW
            elif score < self.HIGH_THRESHOLD:
                bands[key] = self.BAND_MODERATE
            else:
                bands[key] = self.BAND_HIGH
        return bands
    
    def _identify_dominant_traits(self, scores: Dict[str, float], top_n: int = 3) -> List[Dict[str, Any]]:
        """Identify top N dominant traits"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        dominant = []
        for i in range(min(top_n, len(sorted_scores))):
            trait, score = sorted_scores[i]
            dominant.append({
                "trait": trait,
                "score": score,
                "band": self._get_band(score),
                "rank": i + 1
            })
        return dominant
    
    def _get_band(self, score: float) -> str:
        """Get band for a single score"""
        if score < self.LOW_THRESHOLD:
            return self.BAND_LOW
        elif score < self.HIGH_THRESHOLD:
            return self.BAND_MODERATE
        else:
            return self.BAND_HIGH
    
    def _detect_conflicts(self, scores: Dict[str, float]) -> List[str]:
        """Detect conflicting tendencies"""
        conflicts = []
        
        # Example conflict patterns
        conflict_pairs = [
            ("creative", "administrative"),
            ("risk_appetite", "emotional_stability"),
            ("leadership", "teamwork")
        ]
        
        for trait1, trait2 in conflict_pairs:
            if trait1 in scores and trait2 in scores:
                score1, score2 = scores[trait1], scores[trait2]
                # High scores in both conflicting traits
                if score1 > 70 and score2 > 70:
                    conflicts.append(f"High {trait1.replace('_', ' ')} combined with high {trait2.replace('_', ' ')}")
                # Very different scores in related traits
                elif abs(score1 - score2) > 40:
                    higher = trait1 if score1 > score2 else trait2
                    lower = trait2 if score1 > score2 else trait1
                    conflicts.append(f"Strong {higher.replace('_', ' ')} but weak {lower.replace('_', ' ')}")
        
        return conflicts
    
    def _generate_orientation_analysis(self, scores: Dict[str, float], dominant: List[Dict]) -> Dict[str, str]:
        """Generate analysis text for orientation"""
        analysis = {}
        
        if dominant:
            top_trait = dominant[0]["trait"]
            analysis["primary_orientation"] = f"Your primary work orientation is {top_trait.replace('_', ' ').title()}"
            
            if top_trait == "creative":
                analysis["work_style"] = "You thrive in environments that allow creative expression and innovation. You prefer tasks that require imagination and original thinking."
            elif top_trait == "analytical":
                analysis["work_style"] = "You excel in structured, data-driven environments. You prefer systematic problem-solving and logical analysis."
            elif top_trait == "people_centric":
                analysis["work_style"] = "You are naturally drawn to roles involving people interaction and collaboration. You find fulfillment in helping and working with others."
            elif top_trait == "administrative":
                analysis["work_style"] = "You excel in organized, systematic environments. You prefer clear processes and well-defined structures."
        
        return analysis
    
    def _generate_interest_analysis(self, scores: Dict[str, float], dominant: List[Dict]) -> Dict[str, str]:
        """Generate analysis text for interests"""
        analysis = {}
        
        if dominant:
            top_interests = [d["trait"] for d in dominant[:2]]
            analysis["primary_interests"] = f"Your strongest interests lie in {', '.join([i.replace('_', ' ').title() for i in top_interests])}"
            
            interest_descriptions = {
                "stem": "Science, Technology, Engineering, and Mathematics fields that involve technical problem-solving and innovation.",
                "arts_humanities": "Creative expression, literature, culture, and human experiences.",
                "business_commerce": "Business operations, finance, marketing, and commercial activities.",
                "healthcare": "Medical sciences, patient care, and health-related fields.",
                "social_service": "Community work, education, and helping professions."
            }
            
            if top_interests:
                top = top_interests[0]
                analysis["interest_description"] = interest_descriptions.get(top, "")
        
        return analysis
    
    def _generate_personality_analysis(self, scores: Dict[str, float], dominant: List[Dict]) -> Dict[str, str]:
        """Generate analysis text for personality"""
        analysis = {}
        
        if dominant:
            top_traits = [d["trait"] for d in dominant]
            analysis["key_traits"] = f"Your most prominent personality traits are {', '.join([t.replace('_', ' ').title() for t in top_traits])}"
            
            # Overall personality summary
            high_scores = [k for k, v in scores.items() if v > 70]
            if len(high_scores) >= 5:
                analysis["overall"] = "You demonstrate a well-rounded personality with strength across multiple dimensions."
            elif len(high_scores) >= 3:
                analysis["overall"] = "You show strong development in several key personality areas."
            else:
                analysis["overall"] = "You have distinctive strengths in specific personality dimensions."
        
        return analysis
    
    def _generate_aptitude_analysis(self, scores: Dict[str, float], dominant: List[Dict]) -> Dict[str, str]:
        """Generate analysis text for aptitude"""
        analysis = {}
        
        if dominant:
            top_abilities = [d["trait"] for d in dominant]
            analysis["cognitive_strengths"] = f"Your strongest cognitive abilities are in {', '.join([a.replace('_', ' ').title() for a in top_abilities])}"
            
            # Learning style implications
            if "verbal_reasoning" in top_abilities[:2]:
                analysis["learning_style"] = "You are likely to excel in language-based learning and verbal communication."
            elif "numerical_ability" in top_abilities[:2]:
                analysis["learning_style"] = "You are well-suited for quantitative analysis and mathematical problem-solving."
            elif "spatial_visualization" in top_abilities[:2]:
                analysis["learning_style"] = "You have strong visual-spatial abilities, beneficial for design and engineering."
        
        return analysis
    
    def _generate_eq_analysis(self, scores: Dict[str, float], dominant: List[Dict]) -> Dict[str, str]:
        """Generate analysis text for emotional intelligence"""
        analysis = {}
        
        if dominant:
            top_factors = [d["trait"] for d in dominant]
            analysis["eq_strengths"] = f"Your emotional intelligence strengths are in {', '.join([f.replace('_', ' ').title() for f in top_factors])}"
            
            # Overall EQ assessment
            avg_eq = statistics.mean(scores.values())
            if avg_eq > 70:
                analysis["overall_eq"] = "You demonstrate high emotional intelligence, which is a strong foundation for interpersonal success."
            elif avg_eq > 50:
                analysis["overall_eq"] = "You show good emotional intelligence with room for further development."
            else:
                analysis["overall_eq"] = "Developing your emotional intelligence will enhance your personal and professional relationships."
        
        return analysis
