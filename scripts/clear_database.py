"""
Script to clear all user data and start fresh.
Deletes all users, face samples, parcels, and tracking variations.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import get_session, User, Parcel, FaceSample, TrackingVariation
import shutil

def clear_database():
    session = get_session()
    
    # Delete all records
    session.query(TrackingVariation).delete()
    session.query(FaceSample).delete()
    session.query(Parcel).delete()
    session.query(User).delete()
    session.commit()
    
    print("✓ Deleted all database records")
    
    # Clear uploads folder
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        print("✓ Cleared uploads folder")
    
    print("\n✅ Database cleared! You can now start fresh.")

if __name__ == '__main__':
    confirm = input("⚠️  This will delete ALL users, faces, and parcels. Continue? (yes/no): ")
    if confirm.lower() == 'yes':
        clear_database()
    else:
        print("Cancelled.")
