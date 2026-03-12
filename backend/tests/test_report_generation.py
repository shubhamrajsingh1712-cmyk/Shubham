"""
Report Generation API Tests
Tests for the comprehensive PDF report generation endpoints including generate, download, and PDF validation.
Target: 18-23 pages with trait-by-trait analysis (30 traits total across 5 dimensions).
"""
import pytest
import requests
import os
from io import BytesIO

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://psycho-test-launch.preview.emergentagent.com')
TEST_USER_ID = "2a7dbea5-0de8-43d0-ae36-0d0027f0ecff"
ADMIN_EMAIL = "admin@boatmycareer.com"
ADMIN_PASSWORD = "admin123"


@pytest.fixture(scope="module")
def auth_token():
    """Get admin authentication token"""
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    if response.status_code != 200:
        pytest.skip(f"Authentication failed: {response.status_code}")
    return response.json().get("access_token")


@pytest.fixture(scope="module")
def auth_headers(auth_token):
    """Return auth headers for API calls"""
    return {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}


class TestAdminLogin:
    """Test admin login functionality"""
    
    def test_admin_login_success(self):
        """Verify admin can login successfully"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["user"]["role"] == "admin"
        assert data["user"]["email"] == ADMIN_EMAIL
    
    def test_admin_login_wrong_password(self):
        """Verify login fails with wrong password"""
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": ADMIN_EMAIL, "password": "wrongpassword"}
        )
        assert response.status_code == 401


class TestUserTestResults:
    """Test that test user has required test results for report generation"""
    
    def test_user_has_all_test_types(self, auth_headers):
        """Verify test user has all 5 required test types completed"""
        response = requests.get(
            f"{BASE_URL}/api/tests/user/{TEST_USER_ID}",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        tests = response.json()
        assert len(tests) >= 5, f"Expected at least 5 test types, got {len(tests)}"
        
        # Verify all required test types are present
        test_types = [t["test_type"] for t in tests]
        required_types = ["orientation", "interest", "personality", "aptitude", "eq"]
        for req_type in required_types:
            assert req_type in test_types, f"Missing test type: {req_type}"
    
    def test_test_results_have_scores(self, auth_headers):
        """Verify test results have scores data"""
        response = requests.get(
            f"{BASE_URL}/api/tests/user/{TEST_USER_ID}",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        tests = response.json()
        for test in tests:
            assert "scores" in test, f"Test {test['test_type']} missing scores"
            assert len(test["scores"]) > 0, f"Test {test['test_type']} has empty scores"


class TestReportGeneration:
    """Test report generation endpoint"""
    
    def test_generate_report_success(self, auth_headers):
        """Verify report generation endpoint works and returns report_id"""
        response = requests.post(
            f"{BASE_URL}/api/reports/generate/{TEST_USER_ID}",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "report_id" in data, "Response missing report_id"
        assert "message" in data, "Response missing message"
        assert len(data["report_id"]) > 0, "report_id is empty"
    
    def test_generate_report_user_not_found(self, auth_headers):
        """Verify error when user has no test results"""
        response = requests.post(
            f"{BASE_URL}/api/reports/generate/nonexistent-user-id-12345",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_generate_report_without_auth(self):
        """Verify report generation requires authentication"""
        response = requests.post(f"{BASE_URL}/api/reports/generate/{TEST_USER_ID}")
        assert response.status_code in [401, 403]


class TestReportDownload:
    """Test report download endpoint"""
    
    @pytest.fixture
    def generated_report_id(self, auth_headers):
        """Generate a report and return its ID"""
        response = requests.post(
            f"{BASE_URL}/api/reports/generate/{TEST_USER_ID}",
            headers=auth_headers
        )
        assert response.status_code == 200
        return response.json()["report_id"]
    
    def test_download_report_returns_pdf(self, auth_headers, generated_report_id):
        """Verify report download returns a PDF file"""
        response = requests.get(
            f"{BASE_URL}/api/reports/download/{generated_report_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "application/pdf" in response.headers.get("Content-Type", "")
        assert len(response.content) > 10000, "PDF too small, likely empty or error"
    
    def test_download_report_not_found(self, auth_headers):
        """Verify error for non-existent report"""
        response = requests.get(
            f"{BASE_URL}/api/reports/download/nonexistent-report-id-xyz",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_download_report_without_auth(self, generated_report_id):
        """Verify report download requires authentication"""
        response = requests.get(f"{BASE_URL}/api/reports/download/{generated_report_id}")
        assert response.status_code in [401, 403]


class TestReportPDFContent:
    """Test PDF report content and page count"""
    
    def test_pdf_has_18_plus_pages(self, auth_headers):
        """Verify generated PDF has 18+ pages (no blank pages)"""
        # Generate fresh report
        gen_response = requests.post(
            f"{BASE_URL}/api/reports/generate/{TEST_USER_ID}",
            headers=auth_headers
        )
        assert gen_response.status_code == 200
        report_id = gen_response.json()["report_id"]
        
        # Download PDF
        dl_response = requests.get(
            f"{BASE_URL}/api/reports/download/{report_id}",
            headers=auth_headers
        )
        assert dl_response.status_code == 200
        
        # Count pages using PyPDF2
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(BytesIO(dl_response.content))
            page_count = len(reader.pages)
            print(f"PDF Page Count: {page_count}")
            
            # Target is 18-23 pages
            assert page_count >= 18, f"PDF has only {page_count} pages, expected 18+"
            assert page_count <= 30, f"PDF has {page_count} pages, expected max ~25"
            
            # Verify pages have content (not blank)
            blank_pages = 0
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if not text or len(text.strip()) < 50:
                    blank_pages += 1
                    print(f"Warning: Page {i+1} appears mostly blank")
            
            assert blank_pages <= 2, f"Too many blank pages: {blank_pages}"
            
        except ImportError:
            pytest.skip("PyPDF2 not installed - cannot verify page count")
    
    def test_pdf_contains_expected_sections(self, auth_headers):
        """Verify PDF contains all expected sections"""
        # Generate and download PDF
        gen_response = requests.post(
            f"{BASE_URL}/api/reports/generate/{TEST_USER_ID}",
            headers=auth_headers
        )
        report_id = gen_response.json()["report_id"]
        
        dl_response = requests.get(
            f"{BASE_URL}/api/reports/download/{report_id}",
            headers=auth_headers
        )
        
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(BytesIO(dl_response.content))
            
            # Extract all text
            all_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text.lower()
            
            # Verify expected sections exist
            expected_sections = [
                "career discovery report",
                "executive summary",
                "work orientation",
                "interest",
                "personality",
                "aptitude",
                "emotional intelligence",
                "career recommendations",
            ]
            
            for section in expected_sections:
                assert section in all_text, f"Missing section: {section}"
            
        except ImportError:
            pytest.skip("PyPDF2 not installed - cannot verify content")


class TestUserReportsListing:
    """Test user reports listing endpoint"""
    
    def test_get_user_reports(self, auth_headers):
        """Verify user reports listing works"""
        response = requests.get(
            f"{BASE_URL}/api/reports/user/{TEST_USER_ID}",
            headers=auth_headers
        )
        assert response.status_code == 200
        
        reports = response.json()
        assert isinstance(reports, list)
        
        # If reports exist, verify structure
        if len(reports) > 0:
            report = reports[0]
            assert "id" in report
            assert "user_id" in report
            assert report["user_id"] == TEST_USER_ID


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
