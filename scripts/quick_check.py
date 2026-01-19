import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import User, Parcel, get_session

session = get_session()
users = session.query(User).all()
print(f"Total Users: {len(users)}")
if users:
    for u in users:
        print(f"  - {u.face_uuid}: {u.name}")
