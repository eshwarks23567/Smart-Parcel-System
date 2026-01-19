"""
Generate demo data for the Smart Parcel System
Creates synthetic users and parcels with realistic tracking info
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import get_session, User, Parcel
import uuid
import random
from datetime import datetime, timedelta
import json
import numpy as np

# Demo names for users
DEMO_NAMES = [
    "John Smith", "Emma Johnson", "Michael Brown", "Sophia Davis",
    "James Wilson", "Olivia Martinez", "William Anderson", "Ava Thomas",
    "Robert Garcia", "Isabella Rodriguez"
]

# Demo tracking codes
TRACKING_PREFIXES = ["TRK", "PKG", "SHP", "DHL", "FDX", "UPS"]

# Storage locations
STORAGE_LOCATIONS = [
    "Shelf A-1", "Shelf A-2", "Shelf A-3", "Shelf B-1", "Shelf B-2",
    "Locker 10", "Locker 11", "Locker 12", "Locker 13", "Locker 14",
    "Bay C-1", "Bay C-2", "Bay D-1", "Bay D-2", "Zone E"
]

def generate_random_embedding():
    """Generate a random face embedding (128-dim vector)"""
    return np.random.randn(128).astype(np.float32).tolist()

def generate_demo_users(count=5):
    """Create demo users with synthetic face data"""
    session = get_session()
    created_users = []
    
    for i in range(count):
        if i >= len(DEMO_NAMES):
            name = f"Demo User {i+1}"
        else:
            name = DEMO_NAMES[i]
        
        # Generate unique face_uuid
        face_uuid = uuid.uuid4().hex[:6].upper()
        
        # Generate random embedding
        embedding = generate_random_embedding()
        
        # Create user
        user = User(
            name=name,
            phone=f"555-{random.randint(1000, 9999)}",
            face_uuid=face_uuid,
            embedding_json=json.dumps(embedding),
            photo_path=f"demo_user_{face_uuid}.jpg"
        )
        
        session.add(user)
        session.commit()
        created_users.append(user)
        print(f"✓ Created user: {name} (ID: {face_uuid})")
    
    return created_users

def generate_demo_parcels(users, parcels_per_user=2):
    """Create demo parcels for users"""
    session = get_session()
    created_parcels = []
    
    for user in users:
        for j in range(parcels_per_user):
            # Generate tracking code
            prefix = random.choice(TRACKING_PREFIXES)
            tracking_code = f"{prefix}{random.randint(100000, 999999)}"
            
            # Random slot
            slot = str(random.randint(1, 50))
            
            # Random storage location
            storage_location = random.choice(STORAGE_LOCATIONS)
            
            # Random delivery estimate (1-10 days)
            delivery_days = random.randint(1, 10)
            
            # Random arrival time (within last 5 days)
            arrival_offset = timedelta(days=random.randint(0, 5), hours=random.randint(0, 23))
            arrival_time = datetime.utcnow() - arrival_offset
            
            # Random status (mostly stored, some collected)
            status = 'stored' if random.random() > 0.3 else 'collected'
            
            # Notes
            notes = [
                "Fragile - Handle with care",
                "Signature required",
                "Contains electronics",
                "Keep refrigerated",
                "Express delivery",
                None
            ]
            note = random.choice(notes)
            
            parcel = Parcel(
                tracking_code=tracking_code,
                owner_id=user.id,
                status=status,
                slot=slot,
                storage_location=storage_location,
                estimated_delivery_days=delivery_days if status == 'stored' else None,
                arrival_time=arrival_time,
                collected_time=datetime.utcnow() if status == 'collected' else None,
                note=note
            )
            
            session.add(parcel)
            session.commit()
            created_parcels.append(parcel)
            print(f"  ✓ Parcel {tracking_code} → {storage_location} (Est: {delivery_days} days)")
    
    return created_parcels

def main():
    print("=" * 60)
    print("  GENERATING DEMO DATA FOR SMART PARCEL SYSTEM")
    print("=" * 60)
    print()
    
    # Ask user
    response = input("Generate demo data? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Cancelled.")
        return
    
    num_users = input("Number of demo users to create (default 5): ").strip()
    num_users = int(num_users) if num_users.isdigit() else 5
    
    parcels_per_user = input("Parcels per user (default 2): ").strip()
    parcels_per_user = int(parcels_per_user) if parcels_per_user.isdigit() else 2
    
    print()
    print("Creating demo users...")
    users = generate_demo_users(num_users)
    
    print()
    print("Creating demo parcels...")
    parcels = generate_demo_parcels(users, parcels_per_user)
    
    print()
    print("=" * 60)
    print(f"✅ DEMO DATA CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"  Users created: {len(users)}")
    print(f"  Parcels created: {len(parcels)}")
    print()
    print("Demo User IDs (for testing):")
    for user in users:
        print(f"  • {user.name}: {user.face_uuid}")
    print()
    print("You can now test the tracking system with these IDs!")
    print("=" * 60)

if __name__ == '__main__':
    main()
