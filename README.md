# 📦 Smart Parcel Management System

An automated parcel management system powered by face recognition, AI/ML forecasting, and real-time inventory tracking. Users can register their face, receive a unique 6-character ID, and collect parcels using facial recognition or their ID.

## ✨ Features

- 🎯 **Face Registration** - Automatically generates 5 synthetic training samples
- 🔍 **Face Recognition** - DeepFace + FaceNet with OpenCV fallback
- 📦 **Parcel Management** - Add, track, and collect parcels
- 🆔 **Unique ID System** - 6-character IDs for easy tracking
- 📊 **AI Forecasting** - Parcel arrival predictions using Prophet
- 📱 **SMS Notifications** - Twilio integration for collection alerts
- 🌐 **Beautiful UI** - Modern, responsive web interface

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd CPI
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env with your Twilio credentials if you want SMS notifications
```

### 5. Initialize Database
```bash
python db_init.py
```

### 6. Run the Server
```bash
python app.py
```

### 7. Access the Application
Open http://127.0.0.1:5000 in your browser

## 📁 Project Structure

```
CPI/
├── app.py                  # Main Flask application
├── models.py               # Database models (User, Parcel, FaceSample)
├── face_recog.py          # Face recognition utilities
├── notifications.py       # SMS notification helpers
├── forecast.py            # Parcel arrival forecasting
├── db_init.py             # Database initialization
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Web UI
├── scripts/
│   ├── start_server.ps1   # Windows server start script
│   ├── stop_server.ps1    # Windows server stop script
│   ├── generate_synthetic.py  # Generate synthetic face samples
│   └── backfill_face_uuid.py  # Migrate existing users to UUID system
└── static/                # Static assets (if any)
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```env
# Twilio SMS (Optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM=+1234567890

# Flask
FLASK_ENV=development
HOST=0.0.0.0
PORT=5000
```

## 📖 Usage

### Register a New User
1. Click "Register & Get My ID"
2. Enter your name and phone (optional)
3. Look at the camera
4. Receive your unique 6-character ID
5. System automatically generates 5 synthetic face samples

### Track Parcels by ID
1. Enter your 6-character ID in the "Track by ID" section
2. View all your parcels (stored and collected)

### Collect a Parcel
1. Click "Show My Parcels"
2. Look at the camera for face recognition
3. Select a parcel from the dropdown
4. Click "Collect Selected Parcel"
5. System sends SMS notification (if configured)

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Face Recognition**: DeepFace, TensorFlow, OpenCV
- **Database**: SQLAlchemy + SQLite
- **Forecasting**: Prophet (optional)
- **Notifications**: Twilio SMS
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 🔐 Security Notes

- Never commit `.env` files or API keys
- All sensitive data is in `.gitignore`
- Use HTTPS in production
- Implement proper authentication for production use
- Store embeddings securely in production databases

## 📈 Production Considerations

- Use GPU-enabled instances for faster face recognition
- Switch to PostgreSQL or MongoDB for production database
- Implement rate limiting and authentication
- Use Gunicorn or uWSGI instead of Flask development server
- Deploy behind a reverse proxy (Nginx)
- Consider using a dedicated face recognition service

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as part of an automated parcel management system project.

## 🙏 Acknowledgments

- DeepFace library for face recognition
- OpenCV for image processing
- Flask for the web framework
