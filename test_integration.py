#!/usr/bin/env python3
"""
Integration test script for Document Management System
Tests key functionality without requiring a running database
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from app.routers import auth, documents, admin, profile
        from app.models import User, Document, Letterhead
        from app.services.pdf_service import generate_pdf
        from app.services.docx_service import generate_docx
        from app.utils.doc_number import generate_doc_number
        from app.utils.security import hash_password, verify_password
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_password_hashing():
    """Test password hashing functionality"""
    print("\nTesting password hashing...")
    try:
        from app.utils.security import hash_password, verify_password
        
        password = "test_password_123"
        hashed = hash_password(password)
        
        # Verify correct password
        assert verify_password(password, hashed), "Password verification failed"
        
        # Verify wrong password fails
        assert not verify_password("wrong_password", hashed), "Wrong password should not verify"
        
        print("✓ Password hashing works correctly")
        return True
    except Exception as e:
        print(f"✗ Password hashing failed: {e}")
        return False

def test_filename_sanitization():
    """Test filename sanitization"""
    print("\nTesting filename sanitization...")
    try:
        from app.routers.admin import sanitize_filename
        
        # Test directory traversal prevention
        result = sanitize_filename("../../etc/passwd")
        assert ".." not in result and "/" not in result, f"Directory traversal not prevented: {result}"
        
        # Test normal filename
        assert sanitize_filename("document.pdf") == "document.pdf"
        
        # Test special characters removed/replaced
        result = sanitize_filename("my document (1).pdf")
        # Should not contain parentheses or spaces (converted to underscores)
        assert "(" not in result and ")" not in result
        
        print("✓ Filename sanitization works correctly")
        return True
    except Exception as e:
        print(f"✗ Filename sanitization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_jwt_functions():
    """Test JWT token creation and verification"""
    print("\nTesting JWT functions...")
    try:
        from app.routers.auth import get_password_hash
        import jwt
        from datetime import datetime, timedelta
        
        # Test password hash generation
        hashed = get_password_hash("testpass")
        assert hashed, "Hash generation failed"
        
        # Test JWT creation
        SECRET_KEY = "test_secret"
        payload = {
            "sub": 1,
            "role": "admin",
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        # Test JWT decoding
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        assert decoded["sub"] == 1
        assert decoded["role"] == "admin"
        
        print("✓ JWT functions work correctly")
        return True
    except Exception as e:
        print(f"✗ JWT functions failed: {e}")
        return False

def test_file_structure():
    """Test that all necessary files exist"""
    print("\nTesting file structure...")
    try:
        required_files = [
            "backend/app/main.py",
            "backend/app/database.py",
            "backend/requirements.txt",
            "frontend/ui/login.html",
            "frontend/ui/admin.html",
            "frontend/ui/user.html",
            "frontend/ui/user_create.html",
            "frontend/ui/history.html",
            "frontend/ui/profile.html",
            "frontend/ui/js/common.js",
            "frontend/ui/js/admin.js",
            "frontend/ui/css/style.css",
            "sql/init.sql",
            "docker-compose.yml",
        ]
        
        missing = []
        for filepath in required_files:
            if not os.path.exists(filepath):
                missing.append(filepath)
        
        if missing:
            print(f"✗ Missing files: {', '.join(missing)}")
            return False
        
        print("✓ All required files exist")
        return True
    except Exception as e:
        print(f"✗ File structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Document Management System - Integration Tests")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_imports,
        test_password_hashing,
        test_filename_sanitization,
        test_jwt_functions,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED - Application is ready!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
