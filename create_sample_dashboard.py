#!/usr/bin/env python3
"""
Create sample data and show what the dashboard will display.
This generates realistic test data to demonstrate the IST timezone feature.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import UserDatabase
import numpy as np
from datetime import datetime, timedelta
import pytz

# Create a test database
db = UserDatabase('sample_dashboard.db')

print("\n" + "="*80)
print("CREATING SAMPLE DATA FOR DASHBOARD DEMONSTRATION")
print("="*80 + "\n")

# Add sample users
print("📝 Creating sample users...")
sample_users = [
    ('john_doe', np.random.rand(1280)),
    ('jane_smith', np.random.rand(1280)),
    ('bob_wilson', np.random.rand(1280)),
    ('alice_kumar', np.random.rand(1280)),
    ('raj_patel', np.random.rand(1280)),
]

for username, embedding in sample_users:
    if not db.user_exists(username):
        db.add_user(username, embedding)
        print(f"   ✓ Created user: {username}")

print()

# Add sample login history with various timestamps
print("🔐 Creating sample authentication history...")
import random

auth_attempts = [
    ('john_doe', True, 0.92),
    ('jane_smith', True, 0.88),
    ('bob_wilson', False, 0.45),
    ('alice_kumar', True, 0.95),
    ('raj_patel', True, 0.87),
    ('john_doe', True, 0.91),
    ('jane_smith', False, 0.52),
    ('bob_wilson', True, 0.85),
    ('alice_kumar', True, 0.93),
    ('raj_patel', False, 0.48),
    ('john_doe', True, 0.94),
    ('alice_kumar', True, 0.96),
]

for username, success, similarity in auth_attempts:
    db.log_authentication(username, success, similarity)
    status = "✅" if success else "❌"
    print(f"   {status} {username:15} - Similarity: {similarity*100:.1f}%")

print()
print("="*80)
print("DASHBOARD PREVIEW - WHAT USERS WILL SEE")
print("="*80)
print()

# Show what the dashboard will display
print("┌─────────────────────────────────────────────────────────────────────────────┐")
print("│                     FACE AUTHENTICATION SYSTEM - DASHBOARD                  │")
print("│                        (All times shown in IST)                             │")
print("└─────────────────────────────────────────────────────────────────────────────┘")
print()

# Statistics
users_info = db.get_all_users_with_info()
history = db.get_login_history(limit=100)
total_users = len(users_info)
total_logins = len(history)
success_count = sum(1 for h in history if h['success'])
success_rate = (success_count / total_logins * 100) if total_logins > 0 else 0

print("╔═══════════════════════════╗  ╔═══════════════════════════╗  ╔═══════════════╗")
print("║    TOTAL USERS            ║  ║   TOTAL LOGIN ATTEMPTS    ║  ║ SUCCESS RATE  ║")
print(f"║         {total_users:2}                ║  ║          {total_logins:2}               ║  ║    {success_rate:5.1f}%     ║")
print("╚═══════════════════════════╝  ╚═══════════════════════════╝  ╚═══════════════╝")
print()

# Registered Users
print("┌─────────────────────────────────────────────────────────────────────────────┐")
print("│                           REGISTERED USERS                                  │")
print("├────┬─────────────────────┬──────────────────────────────────────────────────┤")
print("│ #  │ Username            │ Registration Time (IST)                          │")
print("├────┼─────────────────────┼──────────────────────────────────────────────────┤")

for i, user in enumerate(users_info, 1):
    print(f"│ {i:<2} │ {user['username']:<19} │ {user['created_at']:<48} │")

print("└────┴─────────────────────┴──────────────────────────────────────────────────┘")
print()

# Login History
print("┌─────────────────────────────────────────────────────────────────────────────┐")
print("│                            LOGIN HISTORY                                    │")
print("├────┬──────────────┬──────────────────────────┬──────────────┬──────────────┤")
print("│ #  │ Username     │ Login Time (IST)         │ Status       │ Similarity   │")
print("├────┼──────────────┼──────────────────────────┼──────────────┼──────────────┤")

for i, entry in enumerate(history[:10], 1):  # Show first 10
    status = "✅ Success" if entry['success'] else "❌ Failed"
    similarity = f"{entry['similarity']*100:.1f}%" if entry['similarity'] else "N/A"
    # Shorten the timestamp for display
    time_parts = entry['login_time'].split()
    short_time = f"{time_parts[0]} {time_parts[1]}"
    print(f"│ {i:<2} │ {entry['username']:<12} │ {short_time:<24} │ {status:<12} │ {similarity:<12} │")

if len(history) > 10:
    print(f"│    │              │ ... and {len(history)-10} more entries │              │              │")

print("└────┴──────────────┴──────────────────────────┴──────────────┴──────────────┘")
print()

# Key insights
print("┌─────────────────────────────────────────────────────────────────────────────┐")
print("│                              KEY INSIGHTS                                   │")
print("├─────────────────────────────────────────────────────────────────────────────┤")

# Find most active user
from collections import Counter
user_logins = Counter(h['username'] for h in history)
if user_logins:
    most_active = user_logins.most_common(1)[0]
    print(f"│ Most Active User: {most_active[0]:<20} ({most_active[1]} logins)                    │")

# Calculate individual success rates
print("│                                                                             │")
print("│ Success Rates by User:                                                      │")
for username in sorted(set(h['username'] for h in history)):
    user_history = [h for h in history if h['username'] == username]
    user_success = sum(1 for h in user_history if h['success'])
    user_rate = (user_success / len(user_history) * 100) if user_history else 0
    print(f"│   • {username:<15}: {user_rate:5.1f}% ({user_success}/{len(user_history)} successful){'':20}│")

print("└─────────────────────────────────────────────────────────────────────────────┘")
print()

print("="*80)
print("✅ SAMPLE DATA CREATED SUCCESSFULLY")
print("="*80)
print()
print("To view this dashboard in your browser:")
print("  1. Start the application: python app.py")
print("  2. Open: http://localhost:5000/dashboard")
print("  3. All timestamps will be displayed in IST format")
print()
print("The dashboard features:")
print("  ✓ Real-time statistics")
print("  ✓ User registration times in IST")
print("  ✓ Complete login history with IST timestamps")
print("  ✓ Success/failure tracking")
print("  ✓ Similarity scores for each attempt")
print("  ✓ Filter by specific user")
print()

# Show timezone conversion example
print("Example Timezone Conversion:")
print("-" * 80)
utc_now = datetime.utcnow()
utc_aware = pytz.utc.localize(utc_now)
ist_time = utc_aware.astimezone(pytz.timezone('Asia/Kolkata'))
print(f"  Current UTC Time: {utc_now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
print(f"  Current IST Time: {ist_time.strftime('%Y-%m-%d %H:%M:%S')} IST")
print(f"  Time Difference:  +5 hours 30 minutes")
print("="*80)
print()

# Clean up
print("Note: Sample database 'sample_dashboard.db' has been created.")
print("You can delete it after viewing if needed.")
print()
