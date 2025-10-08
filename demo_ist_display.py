#!/usr/bin/env python3
"""
Simple demonstration of IST timezone display functionality.
This script shows how timestamps are converted and displayed.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import UserDatabase
import numpy as np
from datetime import datetime, timedelta
import pytz

print("=" * 70)
print("FACE AUTHENTICATION SYSTEM - IST TIMEZONE DEMONSTRATION")
print("=" * 70)
print()

# Create a test database
db = UserDatabase('demo_ist.db')

print("📝 SCENARIO: Adding users and logging authentication attempts")
print("-" * 70)
print()

# Add some demo users
print("1. Registering users...")
users = ['alice', 'bob', 'charlie']
for username in users:
    embedding = np.random.rand(1280)
    if db.user_exists(username):
        print(f"   ✓ User '{username}' already exists")
    else:
        db.add_user(username, embedding)
        print(f"   ✓ Registered user: {username}")

print()

# Show registered users with IST timestamps
print("2. Viewing registered users (with IST registration times):")
print()
users_info = db.get_all_users_with_info()
for user in users_info:
    print(f"   👤 {user['username']:10} | Registered: {user['created_at']}")

print()

# Log some authentication attempts
print("3. Simulating authentication attempts...")
attempts = [
    ('alice', True, 0.92),
    ('bob', True, 0.88),
    ('charlie', False, 0.45),
    ('alice', True, 0.95),
    ('bob', False, 0.52),
]

for username, success, similarity in attempts:
    db.log_authentication(username, success, similarity)
    status = "✅ Success" if success else "❌ Failed"
    print(f"   {status} | {username:10} | Similarity: {similarity*100:.1f}%")

print()

# Show login history
print("4. Login history (all users, with IST timestamps):")
print()
history = db.get_login_history(limit=10)

print(f"   {'#':<3} {'User':<12} {'Time (IST)':<25} {'Status':<15} {'Similarity':<10}")
print(f"   {'-'*3} {'-'*12} {'-'*25} {'-'*15} {'-'*10}")

for i, entry in enumerate(history, 1):
    status = "✅ Success" if entry['success'] else "❌ Failed"
    similarity = f"{entry['similarity']*100:.1f}%" if entry['similarity'] else "N/A"
    print(f"   {i:<3} {entry['username']:<12} {entry['login_time']:<25} {status:<15} {similarity:<10}")

print()

# Show user-specific history
print("5. Login history for 'alice' only:")
print()
alice_history = db.get_login_history(username='alice', limit=10)

for i, entry in enumerate(alice_history, 1):
    status = "✅ Success" if entry['success'] else "❌ Failed"
    similarity = f"{entry['similarity']*100:.1f}%" if entry['similarity'] else "N/A"
    print(f"   {i}. {entry['login_time']:<25} | {status:<15} | Similarity: {similarity}")

print()
print("=" * 70)
print("✅ DEMONSTRATION COMPLETE")
print("=" * 70)
print()
print("Key Points:")
print("  • All timestamps are displayed in Indian Standard Time (IST)")
print("  • IST is UTC+5:30 (5 hours and 30 minutes ahead of UTC)")
print("  • Registration times and login times are tracked and shown in IST")
print("  • Login history includes success/failure status and similarity scores")
print()
print("To view this in the web dashboard:")
print("  1. Run: python app.py")
print("  2. Open: http://localhost:5000/dashboard")
print("  3. View login history and user registration times in IST format")
print()

# Clean up
import os
if os.path.exists('demo_ist.db'):
    os.remove('demo_ist.db')
    print("🗑️  Demo database cleaned up")
