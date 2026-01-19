"""
Add database indexes for performance optimization
This script adds indexes to frequently queried columns
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from models import DATABASE_URL

def add_indexes():
    """Add indexes to improve query performance"""
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    
    with engine.connect() as conn:
        print("Adding database indexes for performance optimization...")
        
        try:
            # Add index on users.face_uuid (if not exists)
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_face_uuid ON users(face_uuid)
            """))
            print("✓ Added index on users.face_uuid")
            
            # Add index on parcels.tracking_code
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_parcels_tracking_code ON parcels(tracking_code)
            """))
            print("✓ Added index on parcels.tracking_code")
            
            # Add index on parcels.owner_id
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_parcels_owner_id ON parcels(owner_id)
            """))
            print("✓ Added index on parcels.owner_id")
            
            # Add index on parcels.status
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_parcels_status ON parcels(status)
            """))
            print("✓ Added index on parcels.status")
            
            # Add index on parcels.arrival_time
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_parcels_arrival_time ON parcels(arrival_time)
            """))
            print("✓ Added index on parcels.arrival_time")
            
            # Add index on face_samples.user_id
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_face_samples_user_id ON face_samples(user_id)
            """))
            print("✓ Added index on face_samples.user_id")
            
            # Add index on face_samples.face_uuid
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_face_samples_face_uuid ON face_samples(face_uuid)
            """))
            print("✓ Added index on face_samples.face_uuid")
            
            conn.commit()
            print("\n✅ All indexes added successfully!")
            print("📈 Database queries will now be significantly faster!")
            
        except Exception as e:
            print(f"❌ Error adding indexes: {e}")
            conn.rollback()

if __name__ == '__main__':
    add_indexes()
