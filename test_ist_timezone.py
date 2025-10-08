#!/usr/bin/env python3
"""
Test script to verify IST timezone conversion and database functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import UserDatabase
import numpy as np
from datetime import datetime
import pytz

def test_timezone_conversion():
    """Test timezone conversion functionality."""
    print("=" * 50)
    print("Testing Timezone Conversion")
    print("=" * 50)
    
    db = UserDatabase(':memory:')  # Use in-memory database for testing
    
    # Test UTC to IST conversion
    utc_timestamp = "2024-01-15 10:30:00"
    ist_timestamp = db._convert_utc_to_ist(utc_timestamp)
    
    print(f"UTC Time: {utc_timestamp}")
    print(f"IST Time: {ist_timestamp}")
    
    # Verify conversion
    utc_time = datetime.strptime(utc_timestamp, '%Y-%m-%d %H:%M:%S')
    utc_time = pytz.utc.localize(utc_time)
    ist_time = utc_time.astimezone(pytz.timezone('Asia/Kolkata'))
    expected = ist_time.strftime('%Y-%m-%d %H:%M:%S IST')
    
    assert ist_timestamp == expected, f"Expected {expected}, got {ist_timestamp}"
    print("✓ Timezone conversion working correctly!")
    print()
    
def test_database_functionality():
    """Test database with login history."""
    print("=" * 50)
    print("Testing Database Functionality")
    print("=" * 50)
    
    # Use a temporary file database instead of :memory: to ensure proper initialization
    import tempfile
    db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    db = UserDatabase(db_file.name)
    
    # Add test users
    print("Adding test users...")
    embedding1 = np.random.rand(1280)
    embedding2 = np.random.rand(1280)
    
    success1 = db.add_user('test_user1', embedding1)
    success2 = db.add_user('test_user2', embedding2)
    assert success1 and success2, "Failed to add users"
    print("✓ Users added successfully!")
    
    # Get users with info
    users_info = db.get_all_users_with_info()
    print(f"\nRegistered Users (with IST timestamps):")
    for user in users_info:
        print(f"  - {user['username']}: {user['created_at']}")
    print("✓ User info retrieval working!")
    
    # Log authentication attempts
    print("\nLogging authentication attempts...")
    db.log_authentication('test_user1', True, 0.85)
    db.log_authentication('test_user2', True, 0.92)
    db.log_authentication('test_user1', False, 0.45)
    db.log_authentication('test_user2', True, 0.88)
    print("✓ Authentication logging working!")
    
    # Get login history
    print("\nLogin History (all users):")
    history = db.get_login_history(limit=10)
    for entry in history:
        status = "✅ Success" if entry['success'] else "❌ Failed"
        similarity = f"{entry['similarity']*100:.1f}%" if entry['similarity'] else "N/A"
        print(f"  - {entry['username']}: {status} ({similarity}) at {entry['login_time']}")
    print("✓ Login history retrieval working!")
    
    # Get login history for specific user
    print("\nLogin History (test_user1 only):")
    user1_history = db.get_login_history(username='test_user1', limit=10)
    for entry in user1_history:
        status = "✅ Success" if entry['success'] else "❌ Failed"
        similarity = f"{entry['similarity']*100:.1f}%" if entry['similarity'] else "N/A"
        print(f"  - {entry['username']}: {status} ({similarity}) at {entry['login_time']}")
    print("✓ User-specific history working!")
    
    # Clean up
    import os
    os.unlink(db_file.name)
    
    print()

def test_ist_format():
    """Test that IST timestamps have correct format."""
    print("=" * 50)
    print("Testing IST Format")
    print("=" * 50)
    
    # Use a temporary file database
    import tempfile
    db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    db = UserDatabase(db_file.name)
    
    # Add user
    embedding = np.random.rand(1280)
    db.add_user('format_test_user', embedding)
    
    # Get user info
    user_info = db.get_user_info('format_test_user')
    timestamp = user_info['created_at']
    
    print(f"Timestamp: {timestamp}")
    
    # Check format
    assert 'IST' in timestamp, "Timestamp should contain 'IST' suffix"
    assert len(timestamp.split()) == 3, "Timestamp should have format: YYYY-MM-DD HH:MM:SS IST"
    
    print("✓ IST format is correct!")
    
    # Clean up
    import os
    os.unlink(db_file.name)
    
    print()

def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("IST TIMEZONE CONVERSION TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        test_timezone_conversion()
        test_database_functionality()
        test_ist_format()
        
        print("=" * 50)
        print("ALL TESTS PASSED! ✅")
        print("=" * 50)
        print("\nSummary:")
        print("  ✓ Timezone conversion (UTC → IST)")
        print("  ✓ Database login history")
        print("  ✓ User registration timestamps")
        print("  ✓ IST format verification")
        print("\nAll timestamps are now displayed in Indian Standard Time (IST)!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
