import os
import uuid
import json
import base64
import numpy as np

# Try to import DeepFace; if unavailable, fall back to OpenCV-based simple embeddings
_HAS_DEEPFACE = False
try:
    from deepface import DeepFace
    _HAS_DEEPFACE = True
except Exception:
    _HAS_DEEPFACE = False

import cv2
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOADS, exist_ok=True)

# DeepFace model settings
MODEL_NAME = 'Facenet'
MODEL = None


def load_model():
    global MODEL
    if not _HAS_DEEPFACE:
        return None
    if MODEL is None:
        MODEL = DeepFace.build_model(MODEL_NAME)
    return MODEL


def save_base64_image(b64data, prefix='img'):
    header, _, data = b64data.partition(',')
    if not data:
        data = header
    img_bytes = base64.b64decode(data)
    filename = f"{prefix}_{uuid.uuid4().hex}.jpg"
    path = os.path.join(UPLOADS, filename)
    with open(path, 'wb') as f:
        f.write(img_bytes)
    return path


def _detect_and_crop_face_opencv(image_path, target_size=(160, 160)):
    # Use Haar cascade to detect the largest face and return a resized grayscale array
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError('Could not read image for opencv fallback')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector = cv2.CascadeClassifier(cascade_path)
    faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
    if len(faces) == 0:
        # fallback: use center crop
        h, w = gray.shape[:2]
        cx, cy = w // 2, h // 2
        s = min(w, h) // 2
        x1 = max(0, cx - s // 2)
        y1 = max(0, cy - s // 2)
        crop = gray[y1:y1 + s, x1:x1 + s]
    else:
        # pick the largest face
        faces = sorted(faces, key=lambda r: r[2] * r[3], reverse=True)
        x, y, w, h = faces[0]
        crop = gray[y:y + h, x:x + w]
    resized = cv2.resize(crop, target_size)
    # normalize to 0-1
    arr = resized.astype(np.float32) / 255.0
    return arr.flatten()


def get_embedding_from_file(image_path):
    """Return embedding vector (numpy array) for an image file.
    Uses DeepFace if available; otherwise a simple OpenCV-based flattened face crop.
    """
    if _HAS_DEEPFACE:
        # Some DeepFace versions do not accept a 'model' kwarg for represent(); call with model_name only
        # load_model() will still ensure weights are available if needed
        _ = load_model()
        reps = DeepFace.represent(img_path=image_path, model_name=MODEL_NAME, enforce_detection=True)
        # DeepFace.represent may return different shapes across versions: a dict with 'embedding',
        # a list of dicts, or a simple list/ndarray. Handle common cases robustly.
        if isinstance(reps, dict) and 'embedding' in reps:
            emb = np.array(reps['embedding'], dtype=np.float32)
        elif isinstance(reps, list) and len(reps) > 0 and isinstance(reps[0], dict) and 'embedding' in reps[0]:
            emb = np.array(reps[0]['embedding'], dtype=np.float32)
        elif isinstance(reps, list) and len(reps) > 0 and isinstance(reps[0], (list, np.ndarray)):
            emb = np.array(reps[0], dtype=np.float32)
        elif isinstance(reps, (list, np.ndarray)):
            emb = np.array(reps, dtype=np.float32)
        else:
            raise ValueError('Unexpected embedding format from DeepFace')
        return emb
    else:
        vec = _detect_and_crop_face_opencv(image_path)
        return np.array(vec, dtype=np.float32)


def get_embedding_from_base64(b64data):
    path = save_base64_image(b64data, prefix='tmp')
    try:
        emb = get_embedding_from_file(path)
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
    return emb


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    if a.size == 0 or b.size == 0:
        return 0.0
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_best_match(embedding, candidates, threshold=0.5):
    """
    candidates: iterable of tuples (id, name, embedding_np)
    returns best candidate dict or None
    threshold is cosine similarity threshold (higher == stricter match)
    """
    best = None
    best_score = -1.0
    for cid, name, emb in candidates:
        try:
            score = cosine_similarity(embedding, np.array(emb, dtype=np.float32))
        except Exception:
            continue
        if score > best_score:
            best_score = score
            best = (cid, name, emb, score)

    if best and best_score >= threshold:
        return {"id": best[0], "name": best[1], "score": float(best[3])}
    return None
