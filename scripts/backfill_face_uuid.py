import os
import sqlite3
import uuid

# ensure imports work
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import DB_PATH, get_session, FaceSample, User, init_db

DB = DB_PATH

def ensure_column():
    # Add face_uuid column if it doesn't exist
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(users)")
    cols = [r[1] for r in cur.fetchall()]
    if 'face_uuid' in cols:
        print('face_uuid already present on users table')
    else:
        print('Adding face_uuid column to users table')
        cur.execute('ALTER TABLE users ADD COLUMN face_uuid TEXT')
        conn.commit()
    conn.close()


def backfill():
    session = get_session()
    users = session.query(User).all()
    for u in users:
        # If user already has face_uuid, skip
        if getattr(u, 'face_uuid', None):
            print(f'User {u.id} already has face_uuid {u.face_uuid}')
            continue
        # Try to find a FaceSample for user
        sample = session.query(FaceSample).filter(FaceSample.user_id == u.id).first()
        if sample and sample.face_uuid:
            print(f'Backfilling user {u.id} with face_uuid from sample: {sample.face_uuid}')
            u.face_uuid = sample.face_uuid
        else:
            new_uuid = uuid.uuid4().hex[:6].upper()
            print(f'Generating new face_uuid for user {u.id}: {new_uuid}')
            u.face_uuid = new_uuid
        session.add(u)
        session.commit()

if __name__ == '__main__':
    init_db()
    ensure_column()
    backfill()
    print('Backfill complete')
