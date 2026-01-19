import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User, Parcel, get_session

session = get_session()

users = session.query(User).all()
parcels = session.query(Parcel).all()

print(f"\n=== DATABASE STATUS ===")
print(f"Total Users: {len(users)}")
print(f"Total Parcels: {len(parcels)}")

if users:
    print("\n=== USERS ===")
    for u in users:
        print(f"ID: {u.face_uuid} | Name: {u.name} | Phone: {u.phone}")

if parcels:
    print("\n=== PARCELS ===")
    for p in parcels[:10]:  # Show first 10
        print(f"ID: {p.tracking_code} | Owner: {p.owner_id} | Location: {p.storage_location} | Estimated: {p.estimated_delivery_days} days | Status: {p.status}")
