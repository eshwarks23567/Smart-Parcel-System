import os
import uuid
import json
import random
import argparse
from datetime import datetime

import cv2
import numpy as np

# Ensure project root is importable
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import get_session, User, FaceSample, init_db
from face_recog import get_embedding_from_file

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOADS = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOADS, exist_ok=True)


def augment_image(src_path, out_path, seed=None):
    # Simple augmentations: rotation, flip, brightness, noise
    img = cv2.imread(src_path)
    if img is None:
        raise ValueError(f'Could not read image: {src_path}')
    h, w = img.shape[:2]
    # random rotate -15..15
    angle = random.uniform(-15, 15)
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    # random flip
    if random.random() < 0.5:
        img = cv2.flip(img, 1)
    # brightness
    if random.random() < 0.6:
        factor = random.uniform(0.7, 1.3)
        img = np.clip(img * factor, 0, 255).astype(np.uint8)
    # noise
    if random.random() < 0.3:
        noise = np.random.normal(0, 8, img.shape).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    # small random crop and resize back
    if random.random() < 0.4:
        cx = int(w * random.uniform(0.05, 0.15))
        cy = int(h * random.uniform(0.05, 0.15))
        x1, y1 = cx, cy
        x2, y2 = w - cx, h - cy
        img = img[y1:y2, x1:x2]
        img = cv2.resize(img, (w, h))
    cv2.imwrite(out_path, img)
    return out_path


def generate_for_user(session, user, samples_per_user=5):
    if not user.photo_path or not os.path.exists(user.photo_path):
        print(f'Skipping user {user.id} - no photo')
        return 0
    # Determine face_uuid: reuse if existing samples present, else create new
    existing = session.query(FaceSample).filter(FaceSample.user_id == user.id).first()
    if existing:
        face_uuid = existing.face_uuid
    else:
        face_uuid = uuid.uuid4().hex[:6].upper()

    created = 0
    for i in range(samples_per_user):
        sample_uuid = uuid.uuid4().hex
        fname = f"synthetic_user{user.id}_{sample_uuid}.jpg"
        out_path = os.path.join(UPLOADS, fname)
        try:
            augment_image(user.photo_path, out_path)
            emb = None
            try:
                emb_arr = get_embedding_from_file(out_path)
                emb = json.dumps(list(map(float, emb_arr.tolist())))
            except Exception as e:
                print(f'Warning: failed to get embedding for {out_path}: {e}')
            fs = FaceSample(user_id=user.id, face_uuid=face_uuid, sample_uuid=sample_uuid, image_path=out_path, embedding_json=emb)
            session.add(fs)
            session.commit()
            created += 1
            print(f'Created sample {fname} for user {user.id}')
        except Exception as e:
            print(f'Failed generating sample for user {user.id}: {e}')
    return created


def main():
    parser = argparse.ArgumentParser(description='Generate synthetic face samples for each user')
    parser.add_argument('--n', type=int, default=5, help='Samples per user')
    args = parser.parse_args()

    init_db()
    session = get_session()
    users = session.query(User).all()
    total = 0
    for u in users:
        print(f'Generating for user {u.id} ({u.name})')
        total += generate_for_user(session, u, samples_per_user=args.n)
    print(f'Generated {total} samples in total')


if __name__ == '__main__':
    main()
