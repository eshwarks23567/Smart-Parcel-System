import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User, FaceSample, get_session

session = get_session()
users = session.query(User).all()

print(f"\n{'='*60}")
print(f"DATABASE CHECK - USERS & FACE SAMPLES")
print(f"{'='*60}\n")

print(f"Total Users: {len(users)}")

if users:
    print("\nUSER DETAILS:")
    for u in users:
        print(f"\n  ID: {u.face_uuid}")
        print(f"  Name: {u.name}")
        print(f"  Phone: {u.phone}")
        print(f"  Photo: {u.photo_path}")
        print(f"  Has Embedding: {u.embedding_json is not None and len(u.embedding_json) > 0}")
        
        # Check face samples
        samples = session.query(FaceSample).filter_by(user_id=u.id).all()
        print(f"  Face Samples: {len(samples)}")
        if samples:
            for s in samples:
                print(f"    - Sample: {s.sample_uuid}, Has Embedding: {s.embedding_json is not None}")
else:
    print("\n⚠️  NO USERS REGISTERED!")
    print("\nPlease register first:")
    print("1. Go to http://127.0.0.1:5000")
    print("2. Start Camera")
    print("3. Enter name and phone")
    print("4. Click 'Register & Get My ID'")

print(f"\n{'='*60}\n")
