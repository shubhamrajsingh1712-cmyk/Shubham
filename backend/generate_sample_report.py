"""Generate a sample PDF report for Prashant Shivam using the existing report generator."""
import sys
sys.path.insert(0, '/app/backend')

from report_generator import ComprehensiveReportGenerator

user_data = {
    "full_name": "Prashant Shivam",
    "email": "prashant.shivam@example.com",
    "class": "10th Standard",
    "school": "DAV Public School",
    "location": "Patna, Bihar",
}

# Simulated test results across all 5 dimensions with realistic scores
test_results = [
    {
        "test_type": "orientation",
        "scores": {
            "creative": 62,
            "analytical": 86,
            "people_centric": 55,
            "administrative": 48,
        },
        "scoring_details": {},
    },
    {
        "test_type": "interest",
        "scores": {
            "stem": 81,
            "arts_humanities": 42,
            "business_commerce": 65,
            "healthcare": 38,
            "social_service": 50,
        },
        "scoring_details": {},
    },
    {
        "test_type": "personality",
        "scores": {
            "decision_making": 74,
            "perseverance": 79,
            "integrity": 82,
            "leadership": 68,
            "teamwork": 71,
            "emotional_stability": 73,
            "risk_appetite": 60,
            "self_discipline": 79,
        },
        "scoring_details": {},
    },
    {
        "test_type": "aptitude",
        "scores": {
            "verbal_reasoning": 70,
            "numerical_ability": 82,
            "logical_reasoning": 84,
            "abstract_thinking": 76,
            "spatial_visualization": 72,
            "technological_understanding": 88,
            "perceptual_speed": 66,
        },
        "scoring_details": {},
    },
    {
        "test_type": "eq",
        "scores": {
            "emotional_awareness": 68,
            "emotional_regulation": 64,
            "empathy": 72,
            "social_skills": 70,
            "motivation": 76,
            "conflict_management": 62,
        },
        "scoring_details": {},
    },
]

generator = ComprehensiveReportGenerator()
output_path = generator.generate_report(user_data, test_results, "sample")
print(f"Generated: {output_path}")

# Copy to frontend public folder
import shutil
dest = "/app/frontend/public/sample_report.pdf"
shutil.copy2(output_path, dest)
print(f"Copied to: {dest}")
