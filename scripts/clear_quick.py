"""
Quick clear - no prompts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import get_session, User, Parcel, FaceSample, TrackingVariation

session = get_session()

# Delete all records
session.query(TrackingVariation).delete()
session.query(FaceSample).delete()
session.query(Parcel).delete()
session.query(User).delete()
session.commit()

print("✅ Database cleared!")

# Quick check
users = session.query(User).all()
print(f"Users remaining: {len(users)}")
