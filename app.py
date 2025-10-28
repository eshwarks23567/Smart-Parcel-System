import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from models import init_db, get_session, User, Parcel, FaceSample
import uuid
from face_recog import get_embedding_from_base64, find_best_match, save_base64_image, get_embedding_from_file
from notifications import send_sms
from datetime import datetime
from forecast import forecast_next_days
import cv2
import numpy as np
import random

app = Flask(__name__)
CORS(app)

UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize DB (creates file if not present)
init_db()


def augment_and_save(src_path, user_id, face_uuid, sample_num):
    """Create an augmented version of the image and save as FaceSample"""
    img = cv2.imread(src_path)
    if img is None:
        return None
    h, w = img.shape[:2]
    # Apply random augmentations
    angle = random.uniform(-15, 15)
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
    img = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    if random.random() < 0.5:
        img = cv2.flip(img, 1)
    if random.random() < 0.6:
        factor = random.uniform(0.8, 1.2)
        img = np.clip(img * factor, 0, 255).astype(np.uint8)
    
    # Save augmented image
    sample_uuid = uuid.uuid4().hex
    fname = f"synthetic_user{user_id}_{sample_uuid}.jpg"
    out_path = os.path.join(UPLOADS_DIR, fname)
    cv2.imwrite(out_path, img)
    
    # Get embedding
    try:
        emb_arr = get_embedding_from_file(out_path)
        emb_json = json.dumps(list(map(float, emb_arr.tolist())))
    except Exception as e:
        print(f'Warning: failed to get embedding for synthetic: {e}')
        emb_json = None
    
    return FaceSample(
        user_id=user_id,
        face_uuid=face_uuid,
        sample_uuid=sample_uuid,
        image_path=out_path,
        embedding_json=emb_json
    )


def generate_synthetic_samples(user_id, photo_path, face_uuid, num_samples=5):
    """Generate synthetic samples for a newly registered user"""
    session = get_session()
    created = 0
    for i in range(num_samples):
        try:
            sample = augment_and_save(photo_path, user_id, face_uuid, i)
            if sample:
                session.add(sample)
                session.commit()
                created += 1
        except Exception as e:
            print(f'Failed to create synthetic sample {i}: {e}')
    return created


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    name = data.get('name')
    phone = data.get('phone')
    image_b64 = data.get('image')
    if not name or not image_b64:
        return jsonify({'error': 'Missing name or image'}), 400

    # Save original image
    photo_path = save_base64_image(image_b64, prefix='user')

    # Compute embedding
    try:
        emb = get_embedding_from_base64(image_b64)
    except Exception as e:
        return jsonify({'error': f'Failed to get embedding: {str(e)}'}), 500

    session = get_session()
    # create or assign a stable face_uuid for this registered user (6 chars)
    user_face_uuid = uuid.uuid4().hex[:6].upper()
    user = User(name=name, phone=phone or '', face_uuid=user_face_uuid, embedding_json=json.dumps(list(map(float, emb.tolist()))), photo_path=photo_path)
    session.add(user)
    session.commit()
    
    # Generate synthetic samples automatically
    try:
        num_created = generate_synthetic_samples(user.id, photo_path, user_face_uuid, num_samples=5)
        print(f'Generated {num_created} synthetic samples for user {user.id}')
    except Exception as e:
        print(f'Warning: Failed to generate synthetic samples: {e}')
    
    return jsonify({'status': 'ok', 'user_id': user.id, 'face_uuid': user_face_uuid})


@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.get_json(force=True)
    image_b64 = data.get('image')
    if not image_b64:
        return jsonify({'error': 'Missing image'}), 400

    try:
        emb = get_embedding_from_base64(image_b64)
    except Exception as e:
        return jsonify({'error': f'Failed to get embedding: {str(e)}'}), 500

    session = get_session()
    users = session.query(User).all()
    candidates = []
    for u in users:
        try:
            ue = json.loads(u.embedding_json)
            candidates.append((u.id, u.name, ue))
        except Exception:
            continue

    # threshold: tune this value for your model. Higher -> stricter matching.
    threshold = float(request.args.get('threshold', 0.5))
    match = find_best_match(emb, candidates, threshold=threshold)
    if match:
        # include face_uuid for matched user
        session = get_session()
        u = session.query(User).filter(User.id == match['id']).first()
        if u and getattr(u, 'face_uuid', None):
            match['face_uuid'] = u.face_uuid
        return jsonify({'status': 'ok', 'match': match})
    else:
        return jsonify({'status': 'not_found'}), 404


@app.route('/parcel/add', methods=['POST'])
def parcel_add():
    """Add a parcel and assign a storage slot. Accepts JSON: tracking_code (optional), owner_id (optional), note.
    If owner_id not provided, parcel will be created without owner and can be assigned later.
    """
    data = request.get_json(force=True)
    tracking = data.get('tracking_code')
    owner_id = data.get('owner_id')
    note = data.get('note')

    session = get_session()
    # Simple slot assignment: next numeric slot
    last = session.query(Parcel).order_by(Parcel.id.desc()).first()
    next_slot = None
    if last and last.slot:
        try:
            # simple numeric increment if slot is numeric
            next_slot = str(int(last.slot) + 1)
        except Exception:
            next_slot = f"S{(last.id or 0) + 1}"
    else:
        next_slot = '1'

    p = Parcel(tracking_code=tracking, owner_id=owner_id, slot=next_slot, note=note)
    session.add(p)
    session.commit()
    return jsonify({'status': 'ok', 'parcel_id': p.id, 'slot': p.slot})


@app.route('/parcel/collect', methods=['POST'])
def parcel_collect():
    """Collect a parcel by recognizing a face. Request body: { image: base64, parcel_id: optional }
    If parcel_id not provided, returns list of stored parcels for matched user.
    On successful collection, stores collected_time and sends SMS (if configured).
    """
    data = request.get_json(force=True)
    img = data.get('image')
    parcel_id = data.get('parcel_id')
    if not img:
        return jsonify({'error': 'Missing image'}), 400

    try:
        emb = get_embedding_from_base64(img)
    except Exception as e:
        return jsonify({'error': f'Failed to get embedding: {str(e)}'}), 500

    session = get_session()
    users = session.query(User).all()
    candidates = []
    for u in users:
        try:
            ue = json.loads(u.embedding_json)
            candidates.append((u.id, u.name, ue))
        except Exception:
            continue

    match = find_best_match(emb, candidates, threshold=float(request.args.get('threshold', 0.5)))
    if not match:
        return jsonify({'status': 'not_found'}), 404

    user_id = match['id']
    # find parcels for user that are stored
    query = session.query(Parcel).filter(Parcel.owner_id == user_id, Parcel.status == 'stored')
    if parcel_id:
        query = query.filter(Parcel.id == int(parcel_id))

    parcels = query.all()
    if not parcels:
        return jsonify({'status': 'no_parcels', 'user': match})

    # If parcel_id provided, collect that one; otherwise return list
    if parcel_id:
        parcel = parcels[0]
        parcel.status = 'collected'
        parcel.collected_time = datetime.utcnow()
        # save a checkout photo
        photo_path = save_base64_image(img, prefix='checkout')
        session.add(parcel)
        session.commit()

        # Send SMS to owner if phone exists
        owner = session.query(User).filter(User.id == user_id).first()
        if owner and owner.phone:
            body = f'Your parcel (id={parcel.id}, slot={parcel.slot}) was collected.'
            send_sms(owner.phone, body)

        return jsonify({'status': 'collected', 'parcel_id': parcel.id, 'slot': parcel.slot, 'user': match})

    # If no parcel_id provided, return list of stored parcels for user
    short = [{'id': p.id, 'tracking': p.tracking_code, 'slot': p.slot, 'arrival_time': p.arrival_time.isoformat() if p.arrival_time else None} for p in parcels]
    return jsonify({'status': 'ok', 'user': match, 'parcels': short})


@app.route('/notify_test', methods=['POST'])
def notify_test():
    """Send a test SMS. Body: { phone: '+12345', body: 'message' }"""
    data = request.get_json(force=True)
    phone = data.get('phone')
    body = data.get('body')
    if not phone or not body:
        return jsonify({'error': 'Missing phone or body'}), 400
    ok = send_sms(phone, body)
    return jsonify({'status': 'ok' if ok else 'skipped'})


@app.route('/forecast', methods=['GET'])
def forecast():
    days = int(request.args.get('days', 7))
    session = get_session()
    preds = forecast_next_days(session, days=days)
    return jsonify({'status': 'ok', 'predictions': preds})


@app.route('/status', methods=['GET'])
def status():
    """Return a small health/status object with counts."""
    session = get_session()
    user_count = session.query(User).count()
    try:
        parcel_count = session.query(Parcel).count()
    except Exception:
        parcel_count = 0
    return jsonify({
        'status': 'ok',
        'users': user_count,
        'parcels': parcel_count,
    })


@app.route('/track/<face_uuid>', methods=['GET'])
def track_orders(face_uuid):
    """Track parcels by face_uuid. Returns user info and all their parcels."""
    session = get_session()
    user = session.query(User).filter(User.face_uuid == face_uuid).first()
    if not user:
        return jsonify({'error': 'Face UUID not found'}), 404
    
    # Get all parcels for this user
    parcels = session.query(Parcel).filter(Parcel.owner_id == user.id).all()
    parcel_list = []
    for p in parcels:
        parcel_list.append({
            'id': p.id,
            'tracking_code': p.tracking_code,
            'status': p.status,
            'slot': p.slot,
            'arrival_time': p.arrival_time.isoformat() if p.arrival_time else None,
            'collected_time': p.collected_time.isoformat() if p.collected_time else None,
            'note': p.note
        })
    
    return jsonify({
        'status': 'ok',
        'face_uuid': face_uuid,
        'user': {
            'id': user.id,
            'name': user.name,
            'phone': user.phone
        },
        'parcels': parcel_list,
        'total_parcels': len(parcel_list)
    })


if __name__ == '__main__':
    # Run without the debugger/reloader so we get a single process when started from scripts
    app.run(host='0.0.0.0', port=5000, debug=False)
