#!/usr/bin/env python3
"""
End-to-End Test Script for AI Cover Letter Generator
"""

import requests
import json
import time

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get("http://localhost:8003/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health: {data['status']} - {data['service']}")
            return True
        else:
            print(f"❌ Backend Health Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Health Error: {e}")
        return False

def test_frontend_health():
    """Test frontend health"""
    print("🔍 Testing Frontend Health...")
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend Health: OK")
            return True
        else:
            print(f"❌ Frontend Health Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend Health Error: {e}")
        return False

def test_cover_letter_generation():
    """Test cover letter generation"""
    print("🔍 Testing Cover Letter Generation...")
    
    test_data = {
        "job_posting": {
            "job_posting_text": "We are looking for a Python developer with FastAPI experience and knowledge of machine learning."
        },
        "cv_data": {
            "cv_text": "I am a software developer with 3 years of experience in Python, FastAPI, and React. I have basic knowledge of machine learning."
        },
        "company_name": "Test Company",
        "position_title": "Python Developer",
        "years_of_experience": "3 years",
        "key_achievements": "Led development of multiple web applications",
        "tone": "formal",
        "variants": 1
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/api/generate-cover-letter",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Cover Letter Generation: Success")
            if 'analysis' in data:
                print(f"   - Position: {data['analysis'].get('position_title', 'N/A')}")
                print(f"   - Skills Extracted: {len(data['analysis'].get('extracted_skills', []))}")
            if 'skill_matches' in data:
                print(f"   - Skill Matches: {len(data['skill_matches'])}")
            if 'recommendations' in data:
                print(f"   - Recommendations: {len(data['recommendations'])}")
            return True
        else:
            print(f"❌ Cover Letter Generation Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Cover Letter Generation Error: {e}")
        return False

def test_pdf_export():
    """Test PDF export functionality"""
    print("🔍 Testing PDF Export...")
    
    test_data = {
        "cover_letter": "This is a test cover letter for PDF export functionality.",
        "company_name": "Test Company",
        "position_title": "Test Position"
    }
    
    try:
        response = requests.post(
            "http://localhost:8003/api/export-pdf",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            print("✅ PDF Export: Success")
            return True
        else:
            print(f"❌ PDF Export Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ PDF Export Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting End-to-End Tests for AI Cover Letter Generator")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Frontend Health", test_frontend_health),
        ("Cover Letter Generation", test_cover_letter_generation),
        ("PDF Export", test_pdf_export),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
