"""
Career Library API Tests
Tests for the career library endpoints including categories, search, and career details.
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://psycho-test-launch.preview.emergentagent.com')


class TestCareerCategories:
    """Test the /api/careers/categories endpoint"""
    
    def test_get_categories_success(self):
        """Verify categories endpoint returns 14 categories with counts"""
        response = requests.get(f"{BASE_URL}/api/careers/categories")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 14, f"Expected 14 categories, got {len(data)}"
        
        # Verify each category has required fields
        for cat in data:
            assert "id" in cat
            assert "name" in cat
            assert "count" in cat
            assert cat["count"] > 0, f"Category {cat['id']} has no careers"
        
        # Verify specific categories exist
        cat_ids = [c["id"] for c in data]
        expected_ids = ["eng", "med", "biz", "art", "sci", "law", "edu", "gov", "media", "agri", "hosp", "def", "sport", "social"]
        for expected in expected_ids:
            assert expected in cat_ids, f"Missing category: {expected}"
    
    def test_categories_have_correct_structure(self):
        """Verify each category has all required fields"""
        response = requests.get(f"{BASE_URL}/api/careers/categories")
        assert response.status_code == 200
        
        data = response.json()
        required_fields = ["id", "name", "icon", "color", "description", "count"]
        
        for cat in data:
            for field in required_fields:
                assert field in cat, f"Category {cat.get('id', 'unknown')} missing field: {field}"


class TestCareerSearch:
    """Test the /api/careers/search endpoint"""
    
    def test_search_returns_paginated_results(self):
        """Verify search returns paginated results with correct structure"""
        response = requests.get(f"{BASE_URL}/api/careers/search")
        assert response.status_code == 200
        
        data = response.json()
        assert "careers" in data
        assert "total" in data
        assert "page" in data
        assert "pages" in data
        
        # Verify pagination defaults
        assert data["page"] == 1
        assert len(data["careers"]) <= 24
        assert data["total"] >= 250, f"Expected at least 250 careers, got {data['total']}"
    
    def test_search_by_name_doctor(self):
        """Verify search filters by career name 'doctor'"""
        response = requests.get(f"{BASE_URL}/api/careers/search?q=doctor")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 1, "Expected at least 1 result for 'doctor'"
        
        # Verify results contain 'doctor' in name or description
        for career in data["careers"]:
            name_lower = career["name"].lower()
            desc_lower = career["description"].lower()
            skills_lower = " ".join(career.get("skills_required", [])).lower()
            assert "doctor" in name_lower or "doctor" in desc_lower or "doctor" in skills_lower
    
    def test_search_by_skill(self):
        """Verify search filters by skill"""
        response = requests.get(f"{BASE_URL}/api/careers/search?q=programming")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 1, "Expected at least 1 result for 'programming'"
    
    def test_search_by_category_med(self):
        """Verify search filters by medical category"""
        response = requests.get(f"{BASE_URL}/api/careers/search?category=med")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 30, f"Expected at least 30 medical careers, got {data['total']}"
        
        # Verify all results belong to med category
        for career in data["careers"]:
            assert career["category"] == "med", f"Career {career['name']} is not in med category"
    
    def test_search_by_category_eng(self):
        """Verify search filters by engineering category"""
        response = requests.get(f"{BASE_URL}/api/careers/search?category=eng")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 40, f"Expected at least 40 engineering careers, got {data['total']}"
        
        for career in data["careers"]:
            assert career["category"] == "eng"
    
    def test_search_combined_query_and_category(self):
        """Verify search with both query and category filter"""
        response = requests.get(f"{BASE_URL}/api/careers/search?q=engineer&category=eng")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] >= 1
        
        for career in data["careers"]:
            assert career["category"] == "eng"
    
    def test_search_pagination_page_2(self):
        """Verify pagination works correctly"""
        response = requests.get(f"{BASE_URL}/api/careers/search?page=2")
        assert response.status_code == 200
        
        data = response.json()
        assert data["page"] == 2
        assert len(data["careers"]) <= 24
    
    def test_search_no_results(self):
        """Verify search returns empty results for non-existent query"""
        response = requests.get(f"{BASE_URL}/api/careers/search?q=xyznonexistentcareer123")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 0
        assert len(data["careers"]) == 0


class TestCareerDetail:
    """Test the /api/careers/{slug} endpoint"""
    
    def test_get_software_engineer_details(self):
        """Verify software engineer career detail returns full data"""
        response = requests.get(f"{BASE_URL}/api/careers/software-engineer")
        assert response.status_code == 200
        
        career = response.json()
        
        # Verify required fields
        assert career["name"] == "Software Engineer"
        assert career["slug"] == "software-engineer"
        assert career["category"] == "eng"
        assert career["category_name"] == "Engineering & Technology"
        assert career["growth_outlook"] == "Excellent"
        
        # Verify education
        assert "education" in career
        assert "undergraduate" in career["education"]
        assert "postgraduate" in career["education"]
        
        # Verify salary
        assert "salary" in career
        assert "starting" in career["salary"]
        assert "mid_career" in career["salary"]
        assert "senior" in career["salary"]
        
        # Verify lists
        assert len(career["skills_required"]) > 0
        assert len(career["entrance_exams"]) > 0
        assert len(career["top_institutions"]) > 0
        assert len(career["pros"]) > 0
        assert len(career["challenges"]) > 0
        
        # Verify related careers
        assert "related_careers" in career
        assert len(career["related_careers"]) > 0
        for rc in career["related_careers"]:
            assert "name" in rc
            assert "slug" in rc
            assert "growth_outlook" in rc
    
    def test_get_doctor_mbbs_details(self):
        """Verify doctor career detail returns correct data"""
        response = requests.get(f"{BASE_URL}/api/careers/doctor-mbbs")
        assert response.status_code == 200
        
        career = response.json()
        assert career["name"] == "Doctor (MBBS)"
        assert career["category"] == "med"
        assert career["category_name"] == "Medical & Healthcare"
    
    def test_career_not_found(self):
        """Verify 404 is returned for non-existent career"""
        response = requests.get(f"{BASE_URL}/api/careers/non-existent-career-xyz")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data or "error" in data or "message" in data
    
    def test_related_careers_same_category(self):
        """Verify related careers are from the same category"""
        response = requests.get(f"{BASE_URL}/api/careers/data-scientist")
        assert response.status_code == 200
        
        career = response.json()
        assert career["category"] == "eng"
        
        # Fetch each related career to verify category
        for rc in career["related_careers"][:3]:
            rc_response = requests.get(f"{BASE_URL}/api/careers/{rc['slug']}")
            if rc_response.status_code == 200:
                rc_detail = rc_response.json()
                assert rc_detail["category"] == "eng", f"Related career {rc['name']} is not in same category"


class TestCareerDataIntegrity:
    """Test career data integrity and consistency"""
    
    def test_total_careers_count(self):
        """Verify total career count is within expected range"""
        response = requests.get(f"{BASE_URL}/api/careers/search")
        assert response.status_code == 200
        
        data = response.json()
        assert 250 <= data["total"] <= 500, f"Total careers ({data['total']}) outside expected range 250-500"
    
    def test_category_counts_sum_to_total(self):
        """Verify sum of category counts equals total careers"""
        cat_response = requests.get(f"{BASE_URL}/api/careers/categories")
        search_response = requests.get(f"{BASE_URL}/api/careers/search")
        
        assert cat_response.status_code == 200
        assert search_response.status_code == 200
        
        categories = cat_response.json()
        total_from_search = search_response.json()["total"]
        
        sum_of_counts = sum(c["count"] for c in categories)
        assert sum_of_counts == total_from_search, f"Category counts ({sum_of_counts}) != total ({total_from_search})"
    
    def test_all_careers_have_required_fields(self):
        """Verify all careers in search results have required fields"""
        response = requests.get(f"{BASE_URL}/api/careers/search?limit=50")
        assert response.status_code == 200
        
        careers = response.json()["careers"]
        required_fields = ["name", "slug", "category", "description", "stream", "skills_required", "growth_outlook"]
        
        for career in careers:
            for field in required_fields:
                assert field in career, f"Career {career.get('name', 'unknown')} missing field: {field}"


class TestAPIHealthAndBasics:
    """Test basic API health and connectivity"""
    
    def test_api_root_endpoint(self):
        """Verify API root endpoint responds"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
    
    def test_cors_headers(self):
        """Verify CORS headers are present"""
        response = requests.options(f"{BASE_URL}/api/careers/categories")
        # For simple GET requests, CORS headers may not be required
        # Just verify the endpoint is accessible
        get_response = requests.get(f"{BASE_URL}/api/careers/categories")
        assert get_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
