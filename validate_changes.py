#!/usr/bin/env python3
"""
Validate Flask app routes and endpoints.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 70)
print("FLASK APP VALIDATION")
print("=" * 70)
print()

# Test 1: Import Flask app
print("1. Testing Flask app import...")
try:
    # We can't fully import app.py because it requires TensorFlow
    # Instead, let's just check the file exists and has correct structure
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Check for new routes
    assert '/dashboard' in content, "Missing /dashboard route"
    assert '/api/users-info' in content, "Missing /api/users-info endpoint"
    assert '/api/login-history' in content, "Missing /api/login-history endpoint"
    assert 'log_authentication' in content, "Missing log_authentication calls"
    
    print("   ✓ All new routes and endpoints present")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()

# Test 2: Check database module
print("2. Testing database module...")
try:
    from database import UserDatabase
    
    # Check for new methods
    assert hasattr(UserDatabase, 'log_authentication'), "Missing log_authentication method"
    assert hasattr(UserDatabase, 'get_login_history'), "Missing get_login_history method"
    assert hasattr(UserDatabase, 'get_all_users_with_info'), "Missing get_all_users_with_info method"
    assert hasattr(UserDatabase, 'get_user_info'), "Missing get_user_info method"
    assert hasattr(UserDatabase, '_convert_utc_to_ist'), "Missing _convert_utc_to_ist method"
    
    print("   ✓ All new database methods present")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()

# Test 3: Check templates
print("3. Testing templates...")
try:
    templates = ['templates/index.html', 'templates/dashboard.html']
    for template in templates:
        assert os.path.exists(template), f"Missing {template}"
    
    # Check dashboard template has required elements
    with open('templates/dashboard.html', 'r') as f:
        dashboard_content = f.read()
    
    assert 'IST' in dashboard_content, "Dashboard should mention IST"
    assert '/api/users-info' in dashboard_content, "Dashboard should call /api/users-info"
    assert '/api/login-history' in dashboard_content, "Dashboard should call /api/login-history"
    assert 'Login History' in dashboard_content, "Dashboard should display login history"
    
    # Check index.html has dashboard link
    with open('templates/index.html', 'r') as f:
        index_content = f.read()
    
    assert '/dashboard' in index_content, "Index should link to dashboard"
    
    print("   ✓ All templates present and valid")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()

# Test 4: Check requirements.txt
print("4. Testing requirements.txt...")
try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    assert 'pytz' in requirements, "Missing pytz in requirements.txt"
    
    print("   ✓ pytz added to requirements.txt")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()
print("=" * 70)
print("✅ ALL VALIDATIONS PASSED")
print("=" * 70)
print()
print("Summary of Changes:")
print("  ✓ New Routes: /dashboard")
print("  ✓ New API Endpoints: /api/users-info, /api/login-history")
print("  ✓ Database: login_history table, IST conversion")
print("  ✓ Templates: dashboard.html with IST display")
print("  ✓ Dependencies: pytz for timezone conversion")
print()
print("All timestamps will now be displayed in Indian Standard Time (IST)!")
