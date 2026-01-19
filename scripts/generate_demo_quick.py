"""
Quick demo data generation - no prompts
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

# Demo names
DEMO_NAMES = [
    "John Smith", "Emma Johnson", "Michael Brown", "Sophia Davis",
    "James Wilson", "Olivia Martinez", "William Anderson", "Ava Thomas",
    "Robert Garcia", "Isabella Rodriguez"
]

# Tracking prefixes
TRACKING_PREFIXES = ["TRK", "PKG", "SHP", "DHL", "FDX", "UPS"]

# Storage locations
STORAGE_LOCATIONS = [
    "Shelf A-1", "Shelf A-2", "Shelf A-3", "Shelf A-4", "Shelf A-5",
    "Shelf B-1", "Shelf B-2", "Shelf B-3", "Shelf B-4", "Shelf B-5",
    "Locker 10", "Locker 11", "Locker 12", "Locker 13", "Locker 14",
    "Bay C-1", "Bay C-2", "Bay C-3", "Bay D-1", "Bay D-2"
]

def generate_random_embedding():
    """Generate a random 128-dim embedding (for demo purposes only)"""
    return np.random.randn(128).astype(np.float32)

def generate_demo_users(count=5):
    """Generate demo users with synthetic face embeddings"""
    session = get_session()
    created_users = []
    
    names = random.sample(DEMO_NAMES, min(count, len(DEMO_NAMES)))
    
    for name in names:
        # Generate unique face_uuid
        face_uuid = str(uuid.uuid4())[:6].upper()
        
        # Generate random embedding
        embedding = generate_random_embedding()
        embedding_json = json.dumps(embedding.tolist())
        
        # Create user
        user = User(
            name=name,
            phone=f"555-{random.randint(1000, 9999)}",
            face_uuid=face_uuid,
            embedding_json=embedding_json,
            photo_path=None  # No actual photo for demo data
        )
        
        session.add(user)
        # Store the data before committing
        created_users.append((name, face_uuid))
    
    session.commit()
    return created_users

def generate_demo_parcels(users, parcels_per_user=2):
    """Generate demo parcels for users"""
    session = get_session()
    created_parcels = []
    
    for name, face_uuid in users:
        for i in range(parcels_per_user):
            # Generate tracking code
            prefix = random.choice(TRACKING_PREFIXES)
            tracking_code = f"{prefix}{random.randint(100000, 999999)}"
            
            # Random arrival time (within last 5 days)
            arrival_time = datetime.utcnow() - timedelta(days=random.randint(0, 5))
            
            # Random status (70% stored, 30% collected)
            status = "stored" if random.random() < 0.7 else "collected"
            collected_time = None
            if status == "collected":
                collected_time = arrival_time + timedelta(days=random.randint(1, 3))
            
            # Random storage location and estimated days
            storage_location = random.choice(STORAGE_LOCATIONS)
            estimated_delivery_days = random.randint(1, 10)
            
            # Optional note
            notes = [None, "Fragile", "Signature required", "Handle with care", "Express delivery"]
            note = random.choice(notes)
            
            parcel = Parcel(
                tracking_code=tracking_code,
                owner_id=face_uuid,
                status=status,
                slot=f"S{random.randint(1, 50):02d}",
                storage_location=storage_location,
                estimated_delivery_days=estimated_delivery_days,
                arrival_time=arrival_time,
                collected_time=collected_time,
                note=note
            )
            
            session.add(parcel)
            created_parcels.append(tracking_code)
    
    session.commit()
    return created_parcels

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  QUICK DEMO DATA GENERATION")
    print("="*60)
    
    # Generate 5 users with 2 parcels each
    print("\n📝 Creating 5 demo users...")
    users = generate_demo_users(5)
    
    print("\n✅ Created users:")
    for name, face_uuid in users:
        print(f"   {name} - ID: {face_uuid}")
    
    print("\n📦 Creating 2 parcels per user...")
    parcels = generate_demo_parcels(users, 2)
    
    print(f"\n✅ Created {len(parcels)} parcels")
    print("\n" + "="*60)
    print("  DEMO DATA READY!")
    print("="*60)
    print("\n💡 Try tracking with these user IDs:")
    for name, face_uuid in users:
        print(f"   {face_uuid} - {name}")
    print("\n")
