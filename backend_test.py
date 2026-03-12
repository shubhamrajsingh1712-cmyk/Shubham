#!/usr/bin/env python3
"""
BoatMyCareer Backend API Testing Suite
Tests all endpoints for the career counselling platform
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class BoatMyCareerAPITester:
    def __init__(self, base_url: str = "https://psycho-test-launch.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.token = None
        self.admin_token = None
        self.test_user_id = None
        self.test_payment_id = None
        self.test_report_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            self.failed_tests.append(f"{name}: {details}")

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    headers: Optional[Dict] = None, use_admin: bool = False) -> tuple:
        """Make HTTP request with proper headers"""
        url = f"{self.api_url}/{endpoint}"
        
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)
            
        # Add auth token if available
        token = self.admin_token if use_admin else self.token
        if token:
            request_headers['Authorization'] = f'Bearer {token}'

        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers, timeout=30)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=request_headers, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            return True, {
                "status_code": response.status_code,
                "data": response.json() if response.content else {},
                "headers": dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}
        except json.JSONDecodeError:
            return False, {"error": "Invalid JSON response"}

    def test_root_endpoint(self):
        """Test API root endpoint"""
        success, response = self.make_request('GET', '')
        if success and response['status_code'] == 200:
            self.log_test("API Root Endpoint", True)
            return True
        else:
            self.log_test("API Root Endpoint", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_student_registration(self):
        """Test student registration"""
        timestamp = datetime.now().strftime("%H%M%S")
        test_data = {
            "email": f"test_student_{timestamp}@example.com",
            "password": "TestPass123!",
            "full_name": f"Test Student {timestamp}",
            "phone": f"98765{timestamp[:5]}",
            "class_level": "X",
            "school_name": "Test High School"
        }

        success, response = self.make_request('POST', 'auth/register', test_data)
        if success and response['status_code'] == 200:
            self.token = response['data'].get('access_token')
            self.test_user_id = response['data'].get('user', {}).get('id')
            self.log_test("Student Registration", True)
            return True
        else:
            self.log_test("Student Registration", False, 
                         f"Status: {response.get('status_code', 'N/A')}, Error: {response.get('data', {}).get('detail', 'Unknown')}")
            return False

    def test_admin_login(self):
        """Test admin login"""
        admin_data = {
            "email": "admin@boatmycareer.com",
            "password": "admin123"
        }

        success, response = self.make_request('POST', 'auth/login', admin_data)
        if success and response['status_code'] == 200:
            self.admin_token = response['data'].get('access_token')
            self.log_test("Admin Login", True)
            return True
        else:
            self.log_test("Admin Login", False, 
                         f"Status: {response.get('status_code', 'N/A')}, Error: {response.get('data', {}).get('detail', 'Unknown')}")
            return False

    def test_student_login(self):
        """Test student login with registered user"""
        if not self.test_user_id:
            self.log_test("Student Login", False, "No test user available")
            return False

        # Use the same credentials from registration
        timestamp = datetime.now().strftime("%H%M%S")
        login_data = {
            "email": f"test_student_{timestamp}@example.com",
            "password": "TestPass123!"
        }

        success, response = self.make_request('POST', 'auth/login', login_data)
        if success and response['status_code'] == 200:
            self.log_test("Student Login", True)
            return True
        else:
            self.log_test("Student Login", False, 
                         f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_get_current_user(self):
        """Test get current user info"""
        if not self.token:
            self.log_test("Get Current User", False, "No auth token")
            return False

        success, response = self.make_request('GET', 'auth/me')
        if success and response['status_code'] == 200:
            self.log_test("Get Current User", True)
            return True
        else:
            self.log_test("Get Current User", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_create_payment(self):
        """Test payment creation"""
        if not self.test_user_id:
            self.log_test("Create Payment", False, "No test user available")
            return False

        payment_data = {
            "user_id": self.test_user_id,
            "program_type": "psychometric_test",
            "amount": 999.0,
            "utr_number": f"UTR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }

        success, response = self.make_request('POST', 'payments', payment_data)
        if success and response['status_code'] == 200:
            self.test_payment_id = response['data'].get('id')
            self.log_test("Create Payment", True)
            return True
        else:
            self.log_test("Create Payment", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_get_user_payments(self):
        """Test get user payments"""
        if not self.test_user_id:
            self.log_test("Get User Payments", False, "No test user available")
            return False

        success, response = self.make_request('GET', f'payments/user/{self.test_user_id}')
        if success and response['status_code'] == 200:
            self.log_test("Get User Payments", True)
            return True
        else:
            self.log_test("Get User Payments", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_verify_payment(self):
        """Test payment verification (admin only)"""
        if not self.test_payment_id or not self.admin_token:
            self.log_test("Verify Payment", False, "No payment ID or admin token")
            return False

        success, response = self.make_request('PATCH', f'payments/{self.test_payment_id}/verify', 
                                            use_admin=True)
        if success and response['status_code'] == 200:
            self.log_test("Verify Payment", True)
            return True
        else:
            self.log_test("Verify Payment", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_get_test_questions(self):
        """Test getting test questions for all test types"""
        test_types = ['orientation', 'personality', 'aptitude', 'eq']
        all_passed = True

        for test_type in test_types:
            success, response = self.make_request('GET', f'questions/{test_type}')
            if success and response['status_code'] == 200:
                questions = response['data'].get('questions', [])
                if len(questions) > 0:
                    self.log_test(f"Get {test_type.title()} Questions", True)
                else:
                    self.log_test(f"Get {test_type.title()} Questions", False, "No questions returned")
                    all_passed = False
            else:
                self.log_test(f"Get {test_type.title()} Questions", False, 
                             f"Status: {response.get('status_code', 'N/A')}")
                all_passed = False

        return all_passed

    def test_submit_test(self):
        """Test submitting a test"""
        if not self.test_user_id:
            self.log_test("Submit Test", False, "No test user available")
            return False

        # Submit orientation test
        test_data = {
            "user_id": self.test_user_id,
            "test_type": "orientation",
            "responses": [
                {"question_id": "orient_1", "response": 4},
                {"question_id": "orient_2", "response": 3},
                {"question_id": "orient_3", "response": 5},
                {"question_id": "orient_4", "response": 2}
            ]
        }

        success, response = self.make_request('POST', 'tests/submit', test_data)
        if success and response['status_code'] == 200:
            self.log_test("Submit Test", True)
            return True
        else:
            self.log_test("Submit Test", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_get_user_tests(self):
        """Test getting user test results"""
        if not self.test_user_id:
            self.log_test("Get User Tests", False, "No test user available")
            return False

        success, response = self.make_request('GET', f'tests/user/{self.test_user_id}')
        if success and response['status_code'] == 200:
            self.log_test("Get User Tests", True)
            return True
        else:
            self.log_test("Get User Tests", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_generate_report(self):
        """Test report generation"""
        if not self.test_user_id:
            self.log_test("Generate Report", False, "No test user available")
            return False

        success, response = self.make_request('POST', f'reports/generate/{self.test_user_id}')
        if success and response['status_code'] == 200:
            self.test_report_id = response['data'].get('report_id')
            self.log_test("Generate Report", True)
            return True
        else:
            self.log_test("Generate Report", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_get_user_reports(self):
        """Test getting user reports"""
        if not self.test_user_id:
            self.log_test("Get User Reports", False, "No test user available")
            return False

        success, response = self.make_request('GET', f'reports/user/{self.test_user_id}')
        if success and response['status_code'] == 200:
            self.log_test("Get User Reports", True)
            return True
        else:
            self.log_test("Get User Reports", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_book_counselling(self):
        """Test booking counselling session"""
        if not self.test_user_id:
            self.log_test("Book Counselling", False, "No test user available")
            return False

        success, response = self.make_request('POST', f'counselling/book?user_id={self.test_user_id}')
        if success and response['status_code'] == 200:
            self.log_test("Book Counselling", True)
            return True
        else:
            self.log_test("Book Counselling", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_get_user_counselling(self):
        """Test getting user counselling sessions"""
        if not self.test_user_id:
            self.log_test("Get User Counselling", False, "No test user available")
            return False

        success, response = self.make_request('GET', f'counselling/user/{self.test_user_id}')
        if success and response['status_code'] == 200:
            self.log_test("Get User Counselling", True)
            return True
        else:
            self.log_test("Get User Counselling", False, f"Status: {response.get('status_code', 'N/A')}")
            return False

    def test_admin_endpoints(self):
        """Test admin-only endpoints"""
        if not self.admin_token:
            self.log_test("Admin Endpoints", False, "No admin token")
            return False

        endpoints = [
            ('admin/users', 'Get All Users'),
            ('admin/payments', 'Get All Payments'),
            ('admin/reports', 'Get All Reports'),
            ('admin/counselling', 'Get All Counselling')
        ]

        all_passed = True
        for endpoint, name in endpoints:
            success, response = self.make_request('GET', endpoint, use_admin=True)
            if success and response['status_code'] == 200:
                self.log_test(name, True)
            else:
                self.log_test(name, False, f"Status: {response.get('status_code', 'N/A')}")
                all_passed = False

        return all_passed

    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting BoatMyCareer Backend API Tests")
        print("=" * 50)

        # Basic connectivity
        if not self.test_root_endpoint():
            print("❌ API is not accessible. Stopping tests.")
            return False

        # Authentication tests
        self.test_student_registration()
        self.test_admin_login()
        self.test_student_login()
        self.test_get_current_user()

        # Payment tests
        self.test_create_payment()
        self.test_get_user_payments()
        self.test_verify_payment()

        # Assessment tests
        self.test_get_test_questions()
        self.test_submit_test()
        self.test_get_user_tests()

        # Report tests
        self.test_generate_report()
        self.test_get_user_reports()

        # Counselling tests
        self.test_book_counselling()
        self.test_get_user_counselling()

        # Admin tests
        self.test_admin_endpoints()

        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for test in self.failed_tests:
                print(f"  - {test}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"✅ Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80  # Consider 80%+ as passing

def main():
    """Main test execution"""
    tester = BoatMyCareerAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())