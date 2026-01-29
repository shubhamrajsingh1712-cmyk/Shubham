from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
import jwt
from enum import Enum
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'boat-my-career-secret-key-2024')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# Security
security = HTTPBearer()

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Enums
class UserRole(str, Enum):
    STUDENT = "student"
    ADMIN = "admin"

class TestStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: str
    class_level: Optional[str] = None
    school_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    full_name: str
    phone: str
    role: UserRole = UserRole.STUDENT
    class_level: Optional[str] = None
    school_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class PaymentCreate(BaseModel):
    user_id: str
    program_type: str  # "psychometric_test" or "extended_program"
    amount: float
    utr_number: Optional[str] = None
    payment_screenshot: Optional[str] = None

class Payment(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    program_type: str
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    utr_number: Optional[str] = None
    payment_screenshot: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None

class TestResponse(BaseModel):
    question_id: str
    response: Any

class TestSubmission(BaseModel):
    user_id: str
    test_type: str  # "orientation", "interest", "personality", "aptitude", "eq"
    responses: List[TestResponse]

class TestResult(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    test_type: str
    responses: List[Dict[str, Any]]
    scores: Dict[str, float]
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AssessmentReport(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    test_results: List[str]  # List of test result IDs
    overall_scores: Dict[str, Any]
    career_recommendations: List[str]
    strengths: List[str]
    development_areas: List[str]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    report_file_path: Optional[str] = None

class CounsellingSession(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    counsellor_name: str = "Shubham Raj Singh"
    scheduled_date: Optional[datetime] = None
    status: str = "pending"  # pending, scheduled, completed, cancelled
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Helper functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user_data = await db.users.find_one({"id": user_id}, {"_id": 0})
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

async def get_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Scoring algorithms
def calculate_orientation_scores(responses: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate orientation scores with weighted scientific algorithm"""
    scores = {
        "creative": 0,
        "analytical": 0,
        "people_centric": 0,
        "administrative": 0
    }
    
    for response in responses:
        question_id = response.get("question_id")
        answer = response.get("response")
        
        # Weighted scoring based on question mapping
        if "creative" in question_id.lower():
            scores["creative"] += answer * 1.2
        elif "analytical" in question_id.lower() or "logical" in question_id.lower():
            scores["analytical"] += answer * 1.2
        elif "people" in question_id.lower() or "social" in question_id.lower():
            scores["people_centric"] += answer * 1.2
        elif "admin" in question_id.lower() or "organized" in question_id.lower():
            scores["administrative"] += answer * 1.2
    
    # Normalize scores to 0-100
    max_score = max(scores.values()) if max(scores.values()) > 0 else 1
    normalized_scores = {k: round((v / max_score) * 100, 2) for k, v in scores.items()}
    return normalized_scores

def calculate_personality_scores(responses: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate personality trait scores"""
    traits = {
        "decision_making": 0,
        "perseverance": 0,
        "integrity": 0,
        "leadership": 0,
        "teamwork": 0,
        "emotional_stability": 0,
        "risk_appetite": 0,
        "self_discipline": 0
    }
    
    count = {k: 0 for k in traits.keys()}
    
    for response in responses:
        question_id = response.get("question_id")
        answer = response.get("response")
        
        for trait in traits.keys():
            if trait.replace("_", "") in question_id.lower().replace("_", ""):
                traits[trait] += answer
                count[trait] += 1
    
    # Calculate average and normalize
    normalized_scores = {}
    for trait, score in traits.items():
        if count[trait] > 0:
            avg_score = score / count[trait]
            normalized_scores[trait] = round((avg_score / 5) * 100, 2)
        else:
            normalized_scores[trait] = 50.0
    
    return normalized_scores

def calculate_aptitude_scores(responses: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate aptitude scores"""
    abilities = {
        "verbal_reasoning": 0,
        "numerical_ability": 0,
        "logical_reasoning": 0,
        "abstract_thinking": 0,
        "spatial_visualization": 0,
        "technological_understanding": 0,
        "perceptual_speed": 0
    }
    
    count = {k: 0 for k in abilities.keys()}
    
    for response in responses:
        question_id = response.get("question_id")
        is_correct = response.get("response")
        
        for ability in abilities.keys():
            if ability.replace("_", "") in question_id.lower().replace("_", ""):
                abilities[ability] += 1 if is_correct else 0
                count[ability] += 1
    
    # Calculate percentage correct
    normalized_scores = {}
    for ability, correct_count in abilities.items():
        if count[ability] > 0:
            percentage = (correct_count / count[ability]) * 100
            normalized_scores[ability] = round(percentage, 2)
        else:
            normalized_scores[ability] = 50.0
    
    return normalized_scores

def calculate_eq_scores(responses: List[Dict[str, Any]]) -> Dict[str, float]:
    """Calculate emotional intelligence scores"""
    eq_factors = {
        "emotional_awareness": 0,
        "emotional_regulation": 0,
        "empathy": 0,
        "motivation": 0,
        "conflict_management": 0,
        "social_responsibility": 0
    }
    
    count = {k: 0 for k in eq_factors.keys()}
    
    for response in responses:
        question_id = response.get("question_id")
        answer = response.get("response")
        
        for factor in eq_factors.keys():
            if factor.replace("_", "") in question_id.lower().replace("_", ""):
                eq_factors[factor] += answer
                count[factor] += 1
    
    # Calculate average and normalize
    normalized_scores = {}
    for factor, score in eq_factors.items():
        if count[factor] > 0:
            avg_score = score / count[factor]
            normalized_scores[factor] = round((avg_score / 5) * 100, 2)
        else:
            normalized_scores[factor] = 50.0
    
    return normalized_scores

def generate_career_recommendations(overall_scores: Dict[str, Any]) -> List[str]:
    """Generate career recommendations based on scores"""
    recommendations = []
    
    # Orientation-based recommendations
    orientation_data = overall_scores.get("orientation", {})
    if orientation_data:
        orientation = orientation_data.get('normalized_scores', {})
        if orientation:
            max_orientation = max(orientation, key=orientation.get)
            if max_orientation == "creative":
                recommendations.extend([
                    "Graphic Designer", "Architect", "Content Creator", 
                    "UX/UI Designer", "Filmmaker", "Animator"
                ])
            elif max_orientation == "analytical":
                recommendations.extend([
                    "Data Scientist", "Software Engineer", "Research Scientist", 
                    "Financial Analyst", "Systems Analyst", "Actuary"
                ])
            elif max_orientation == "people_centric":
                recommendations.extend([
                    "Psychologist", "HR Manager", "Teacher", 
                    "Social Worker", "Sales Manager", "Counselor"
                ])
            elif max_orientation == "administrative":
                recommendations.extend([
                    "Project Manager", "Operations Manager", "Business Analyst", 
                    "Administrator", "Management Consultant", "Event Manager"
                ])
    
    # Aptitude-based additions
    aptitude_data = overall_scores.get("aptitude", {})
    if aptitude_data:
        aptitude = aptitude_data.get('normalized_scores', {})
        if aptitude:
            if aptitude.get("technological_understanding", 0) > 70:
                recommendations.extend([
                    "Software Developer", "Cybersecurity Analyst", 
                    "AI/ML Engineer", "DevOps Engineer"
                ])
            if aptitude.get("numerical_ability", 0) > 70:
                recommendations.extend([
                    "Chartered Accountant", "Economist", 
                    "Statistician", "Investment Banker"
                ])
    
    # Interest-based additions
    interest_data = overall_scores.get("interest", {})
    if interest_data:
        interest = interest_data.get('normalized_scores', {})
        if interest:
            if interest.get("stem", 0) > 70:
                recommendations.extend([
                    "Research Scientist", "Engineer", 
                    "Biotechnologist", "Data Analyst"
                ])
            if interest.get("healthcare", 0) > 70:
                recommendations.extend([
                    "Doctor", "Nurse", "Pharmacist", 
                    "Physiotherapist", "Medical Researcher"
                ])
    
    return list(set(recommendations[:15]))  # Return unique top 15

def generate_pdf_report(user_data: dict, overall_scores: Dict[str, Any], report_id: str) -> str:
    """Generate a comprehensive PDF report with charts"""
    filename = f"report_{report_id}.pdf"
    filepath = f"/tmp/{filename}"
    
    # Create PDF
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                           rightMargin=50, leftMargin=50,
                           topMargin=50, bottomMargin=50)
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1A2B4B'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1A2B4B'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1A1A1A'),
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("Career Discovery Report", title_style))
    story.append(Paragraph("BoatMyCareer.com", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Student Info
    story.append(Paragraph("Student Profile", heading_style))
    student_data = [
        ["Name:", user_data.get('full_name', 'N/A')],
        ["Class:", user_data.get('class_level', 'N/A')],
        ["School:", user_data.get('school_name', 'N/A')],
        ["Report Date:", datetime.now(timezone.utc).strftime('%B %d, %Y')]
    ]
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#4A4A4A')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1A1A1A')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(student_table)
    story.append(Spacer(1, 30))
    
    # Orientation Scores
    if 'orientation' in overall_scores:
        story.append(Paragraph("Work Orientation", heading_style))
        orientation_data = [["Dimension", "Score"]]
        for key, value in overall_scores['orientation'].items():
            orientation_data.append([key.replace('_', ' ').title(), f"{value}%"])
        
        orientation_table = Table(orientation_data, colWidths=[3*inch, 2*inch])
        orientation_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ]))
        story.append(orientation_table)
        story.append(Spacer(1, 20))
    
    # Personality Traits
    if 'personality' in overall_scores:
        story.append(Paragraph("Personality Profile", heading_style))
        personality_data = [["Trait", "Score"]]
        for key, value in overall_scores['personality'].items():
            personality_data.append([key.replace('_', ' ').title(), f"{value}%"])
        
        personality_table = Table(personality_data, colWidths=[3*inch, 2*inch])
        personality_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5D7A68')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ]))
        story.append(personality_table)
        story.append(Spacer(1, 20))
    
    story.append(PageBreak())
    
    # Career Recommendations
    if 'career_recommendations' in overall_scores:
        story.append(Paragraph("Recommended Career Paths", heading_style))
        for idx, career in enumerate(overall_scores['career_recommendations'], 1):
            story.append(Paragraph(f"{idx}. {career}", body_style))
        story.append(Spacer(1, 20))
    
    # Strengths
    if 'strengths' in overall_scores:
        story.append(Paragraph("Key Strengths", heading_style))
        for strength in overall_scores['strengths']:
            story.append(Paragraph(f"• {strength}", body_style))
        story.append(Spacer(1, 20))
    
    # Development Areas
    if 'development_areas' in overall_scores:
        story.append(Paragraph("Areas for Development", heading_style))
        for area in overall_scores['development_areas']:
            story.append(Paragraph(f"• {area}", body_style))
        story.append(Spacer(1, 20))
    
    # Footer
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>Disclaimer:</b> This report is a guidance tool based on your responses. It should be used in conjunction with professional counselling and personal reflection.", styles['Normal']))
    story.append(Spacer(1, 20))
    story.append(Paragraph("For counselling: Call/WhatsApp 6200488068 | Email: shubhamrajsingh1712@gmail.com", styles['Normal']))
    
    doc.build(story)
    return filepath

# Routes
@api_router.get("/")
async def root():
    return {"message": "BoatMyCareer API", "version": "1.0"}

# Authentication Routes
@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_pw = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        phone=user_data.phone,
        class_level=user_data.class_level,
        school_name=user_data.school_name,
        role=UserRole.STUDENT
    )
    
    user_dict = user.model_dump()
    user_dict['password'] = hashed_pw
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    
    await db.users.insert_one(user_dict)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
    
    user_response = user.model_dump()
    return TokenResponse(access_token=access_token, user=user_response)

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    user_data = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not verify_password(credentials.password, user_data['password']):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        data={"sub": user_data['id'], "email": user_data['email'], "role": user_data['role']}
    )
    
    user_data.pop('password', None)
    return TokenResponse(access_token=access_token, user=user_data)

@api_router.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user

# Payment Routes
@api_router.post("/payments", response_model=Payment)
async def create_payment(payment_data: PaymentCreate, current_user: dict = Depends(get_current_user)):
    payment = Payment(**payment_data.model_dump())
    payment_dict = payment.model_dump()
    payment_dict['created_at'] = payment_dict['created_at'].isoformat()
    
    await db.payments.insert_one(payment_dict)
    return payment

@api_router.get("/payments/user/{user_id}", response_model=List[Payment])
async def get_user_payments(user_id: str, current_user: dict = Depends(get_current_user)):
    payments = await db.payments.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for payment in payments:
        if isinstance(payment.get('created_at'), str):
            payment['created_at'] = datetime.fromisoformat(payment['created_at'])
        if payment.get('verified_at') and isinstance(payment['verified_at'], str):
            payment['verified_at'] = datetime.fromisoformat(payment['verified_at'])
    return payments

@api_router.patch("/payments/{payment_id}/verify")
async def verify_payment(payment_id: str, admin_user: dict = Depends(get_admin_user)):
    result = await db.payments.update_one(
        {"id": payment_id},
        {"$set": {
            "status": PaymentStatus.COMPLETED,
            "verified_at": datetime.now(timezone.utc).isoformat(),
            "verified_by": admin_user['id']
        }}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment verified successfully"}

# Test Routes
@api_router.post("/tests/submit", response_model=TestResult)
async def submit_test(test_data: TestSubmission, current_user: dict = Depends(get_current_user)):
    from scoring_engine import ScoringEngine
    
    responses_list = [r.model_dump() for r in test_data.responses]
    
    # Use advanced scoring engine
    scoring_engine = ScoringEngine()
    scoring_result = scoring_engine.calculate_scores(test_data.test_type, responses_list)
    
    # Extract normalized scores for storage
    scores = scoring_result.get('normalized_scores', {})
    
    test_result = TestResult(
        user_id=test_data.user_id,
        test_type=test_data.test_type,
        responses=responses_list,
        scores=scores
    )
    
    result_dict = test_result.model_dump()
    result_dict['completed_at'] = result_dict['completed_at'].isoformat()
    
    # Store full scoring result for report generation
    result_dict['scoring_details'] = scoring_result
    
    await db.test_results.insert_one(result_dict)
    return test_result

@api_router.get("/tests/user/{user_id}", response_model=List[TestResult])
async def get_user_tests(user_id: str, current_user: dict = Depends(get_current_user)):
    tests = await db.test_results.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for test in tests:
        if isinstance(test.get('completed_at'), str):
            test['completed_at'] = datetime.fromisoformat(test['completed_at'])
    return tests

# Report Routes
@api_router.post("/reports/generate/{user_id}")
async def generate_report(user_id: str, current_user: dict = Depends(get_current_user)):
    from report_generator import ComprehensiveReportGenerator
    
    # Get all test results for user
    test_results = await db.test_results.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    
    if not test_results:
        raise HTTPException(status_code=404, detail="No test results found for user")
    
    # Get user data
    user_data = await db.users.find_one({"id": user_id}, {"_id": 0, "password": 0})
    
    # Compile overall scores and analysis
    overall_scores = {}
    for test in test_results:
        overall_scores[test['test_type']] = test.get('scoring_details', {})
    
    # Generate career recommendations
    career_recommendations = generate_career_recommendations(overall_scores)
    
    # Identify strengths and development areas
    strengths = []
    development_areas = []
    
    for test_type, scores_data in overall_scores.items():
        scores = scores_data.get('normalized_scores', {})
        for key, value in scores.items():
            if value >= 75:
                strengths.append(f"Strong {key.replace('_', ' ').title()} ({test_type})")
            elif value < 50:
                development_areas.append(f"Develop {key.replace('_', ' ').title()} ({test_type})")
    
    # Create report
    report = AssessmentReport(
        user_id=user_id,
        test_results=[t['id'] for t in test_results],
        overall_scores=overall_scores,
        career_recommendations=career_recommendations,
        strengths=strengths[:10],
        development_areas=development_areas[:5]
    )
    
    # Generate comprehensive PDF using new generator
    try:
        report_gen = ComprehensiveReportGenerator()
        pdf_path = report_gen.generate_report(user_data, test_results, report.id)
        report.report_file_path = pdf_path
    except Exception as e:
        print(f"Error generating report: {e}")
        # Fallback to basic report if comprehensive fails
        pdf_path = generate_pdf_report(user_data, overall_scores, report.id)
        report.report_file_path = pdf_path
    
    report_dict = report.model_dump()
    report_dict['generated_at'] = report_dict['generated_at'].isoformat()
    
    await db.reports.insert_one(report_dict)
    
    return {"report_id": report.id, "message": "Comprehensive report generated successfully"}

@api_router.get("/reports/user/{user_id}", response_model=List[AssessmentReport])
async def get_user_reports(user_id: str, current_user: dict = Depends(get_current_user)):
    reports = await db.reports.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for report in reports:
        if isinstance(report.get('generated_at'), str):
            report['generated_at'] = datetime.fromisoformat(report['generated_at'])
    return reports

@api_router.get("/reports/download/{report_id}")
async def download_report(report_id: str, current_user: dict = Depends(get_current_user)):
    report = await db.reports.find_one({"id": report_id}, {"_id": 0})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not report.get('report_file_path'):
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        report['report_file_path'],
        media_type='application/pdf',
        filename=f"career_report_{report_id}.pdf"
    )

# Counselling Routes
@api_router.post("/counselling/book", response_model=CounsellingSession)
async def book_counselling(user_id: str, preferred_date: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    session = CounsellingSession(
        user_id=user_id,
        scheduled_date=datetime.fromisoformat(preferred_date) if preferred_date else None
    )
    
    session_dict = session.model_dump()
    session_dict['created_at'] = session_dict['created_at'].isoformat()
    if session_dict.get('scheduled_date'):
        session_dict['scheduled_date'] = session_dict['scheduled_date'].isoformat()
    
    await db.counselling_sessions.insert_one(session_dict)
    return session

@api_router.get("/counselling/user/{user_id}", response_model=List[CounsellingSession])
async def get_user_counselling_sessions(user_id: str, current_user: dict = Depends(get_current_user)):
    sessions = await db.counselling_sessions.find({"user_id": user_id}, {"_id": 0}).to_list(100)
    for session in sessions:
        if isinstance(session.get('created_at'), str):
            session['created_at'] = datetime.fromisoformat(session['created_at'])
        if session.get('scheduled_date') and isinstance(session['scheduled_date'], str):
            session['scheduled_date'] = datetime.fromisoformat(session['scheduled_date'])
    return sessions

# Admin Routes
@api_router.get("/admin/users", response_model=List[User])
async def get_all_users(admin_user: dict = Depends(get_admin_user)):
    users = await db.users.find({"role": UserRole.STUDENT}, {"_id": 0, "password": 0}).to_list(1000)
    for user in users:
        if isinstance(user.get('created_at'), str):
            user['created_at'] = datetime.fromisoformat(user['created_at'])
    return users

@api_router.get("/admin/payments")
async def get_all_payments(admin_user: dict = Depends(get_admin_user)):
    payments = await db.payments.find({}, {"_id": 0}).to_list(1000)
    for payment in payments:
        if isinstance(payment.get('created_at'), str):
            payment['created_at'] = datetime.fromisoformat(payment['created_at'])
        if payment.get('verified_at') and isinstance(payment['verified_at'], str):
            payment['verified_at'] = datetime.fromisoformat(payment['verified_at'])
    return payments

@api_router.get("/admin/reports")
async def get_all_reports(admin_user: dict = Depends(get_admin_user)):
    reports = await db.reports.find({}, {"_id": 0}).to_list(1000)
    for report in reports:
        if isinstance(report.get('generated_at'), str):
            report['generated_at'] = datetime.fromisoformat(report['generated_at'])
    return reports

@api_router.get("/admin/counselling")
async def get_all_counselling_sessions(admin_user: dict = Depends(get_admin_user)):
    sessions = await db.counselling_sessions.find({}, {"_id": 0}).to_list(1000)
    for session in sessions:
        if isinstance(session.get('created_at'), str):
            session['created_at'] = datetime.fromisoformat(session['created_at'])
        if session.get('scheduled_date') and isinstance(session['scheduled_date'], str):
            session['scheduled_date'] = datetime.fromisoformat(session['scheduled_date'])
    return sessions

# Test Questions Endpoints
@api_router.get("/questions/{test_type}")
async def get_test_questions(test_type: str):
    """Get questions for a specific test type"""
    from question_bank import get_questions_by_type
    
    questions = get_questions_by_type(test_type)
    if questions is None:
        raise HTTPException(status_code=404, detail="Test type not found")
    
    return questions

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
