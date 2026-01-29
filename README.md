# 📦 Smart Parcel Management System

An intelligent, automated parcel management system powered by advanced facial recognition AI. This system enables seamless parcel tracking and collection for students through face-based authentication, automatic storage assignment, and a modern, beautifully designed interface with three distinct portals.

## ✨ Key Features

### 🏠 Home Page
- **Modern Landing Page** - Professional dark theme with gradient backgrounds
- **Feature Showcase** - Six interactive feature cards highlighting key capabilities
- **Portal Selection** - Easy access to Student and Staff portals
- **Interactive Effects** - Animated backgrounds, magnetic buttons, and smooth transitions
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices

### 🎓 Student Portal
- **Face Identification** - Quick identity verification with live camera feed
- **Self-Service Order Entry** - Add parcels with tracking codes and custom notes
- **My Parcels Dashboard** - View all your parcels with status badges and details
- **Real-Time Camera** - Device selection and live preview
- **Gradient ID Card** - Beautiful card design with copy-to-clipboard functionality
- **Status Tracking** - Track parcels through stored → collected lifecycle
- **Unique Face UUID** - Each student gets a unique 6-character identifier

### 👨‍💼 Staff Portal
- **5-Tab Interface** - Organized workflow across Register, Receive, Handover, Shelf, and All Parcels
- **Student Registration** - Quick registration with dual camera setup
- **Parcel Reception** - Fast parcel entry with automatic storage slot assignment
- **Smart Hand-Out Flow** - Click-to-verify workflow for secure parcel distribution
- **Shelf Visualization** - Interactive 6x6 grid showing all storage slots
- **Statistics Dashboard** - Real-time stats for total, stored, and collected parcels
- **Advanced Search** - Filter parcels by tracking code with instant results
- **Recently Added Parcels** - Quick access to latest 5 parcels

### 🎨 Modern Design System
- **Dark Theme** - Professional dark mode with OKLCH color space
- **Glassmorphism** - Frosted glass effects with backdrop blur
- **Animated Blobs** - Floating gradient backgrounds for visual depth
- **Shimmer Effects** - Cards with light sweep animations on hover
- **Magnetic Buttons** - Interactive buttons that respond to mouse movement
- **Smooth Transitions** - Cubic-bezier easing for polished animations
- **Card Hover Effects** - Elevation and glow effects on interaction

### 🤖 Advanced AI Features
- **VGG-Face Model** - Enhanced accuracy with state-of-the-art recognition
- **Image Preprocessing** - Histogram equalization and denoising for better results
- **OpenCV Detector** - Fast and reliable face detection
- **Face Alignment** - Automatic face alignment for consistent embeddings
- **Lower Threshold** - Optimized threshold (0.4) for VGG-Face accuracy
- **Multi-Sample Recognition** - Enhanced accuracy through multiple face embeddings
- **Automatic Storage Assignment** - Smart slot allocation based on availability

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/eshwarks23567/Smart-Parcel-System.git
cd Smart-Parcel-System
```

### 2. Create Virtual Environment
```bash
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows Command Prompt
.\.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python db_init.py
```

### 5. Run the Application
```bash
python app.py
```

## 📁 Project Structure

```
CPI/
├── app.py                     # Main Flask application & API endpoints
├── models.py                  # SQLAlchemy database models
├── face_recog.py             # Face recognition utilities (DeepFace/FaceNet)
├── notifications.py          # SMS notification system (Twilio)
├── forecast.py               # Parcel arrival forecasting (Prophet)
├── db_init.py                # Database initialization script
├── requirements.txt          # Python dependencies
├── data.db                   # SQLite database (auto-generated)
│
├── templates/
│   ├── home.html             # Modern landing page with feature showcase
│   ├── student.html          # Student portal interface (3-column layout)
│   ├── staff.html            # Staff portal interface (5-tab layout)
│   └── index.html            # Legacy unified interface
│
├── uploads/                  # Face image storage (auto-created)
│   └── face_samples/         # User face captures
│
└── scripts/
    ├── start_server.ps1      # Windows server start script
    ├── stop_server.ps1       # Windows server stop script
    ├── generate_synthetic.py # Generate synthetic face samples
    ├── backfill_face_uuid.py # Migrate users to UUID system
    └── check_users_detailed.py # Database inspection utility
```

## 🎯 User Workflows

### Student Self-Service Flow
1. **Register**: Capture face → Get unique 6-character ID
2. **Add Parcel**: Enter tracking code → Add notes → Auto-assign storage slot
3. **Track**: View parcel location, slot, and estimated pickup time
4. **Collect**: Done by staff using hand-out verification

### Staff Parcel Management Flow
1. **Receive Parcel**: 
   - Enter tracking code and owner ID
   - System auto-assigns slot and storage location
   - Appears in "Recently Added Parcels"

2. **Hand Out Parcel**:
   - Click "Hand Out" button on parcel
   - Switch to "Hand Over Parcel" tab
   - Verify student identity via camera
   - Show specific parcel with "Collect" button
   - Mark as collected → Moves to "Collected Parcels"

## 🔌 API Endpoints

### Authentication & User Management
- `POST /register` - Register new user with face image
- `POST /recognize` - Recognize user from face image
- `GET /user/<face_uuid>` - Get user details by UUID

### Parcel Management
- `POST /parcel/add` - Add new parcel with auto-assignment
- `GET /track_orders` - Get all parcels (optional: `?owner_id=UUID`)
- `POST /parcel/mark_collected` - Mark parcel as collected
- `GET /my_parcels/<user_id>` - Get user's parcels

### Utilities
- `GET /health` - Health check endpoint
- `GET /stats` - System statistics

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.x (Python)
- **Database**: SQLAlchemy + SQLite
- **Face Recognition**: DeepFace + VGG-Face (upgraded from FaceNet)
- **Computer Vision**: OpenCV (with opencv detector backend)
- **Image Processing**: Histogram equalization, denoising (fastNlMeansDenoisingColored)
- **Forecasting**: Prophet (optional)
- **Notifications**: Twilio SMS API

### Frontend
- **HTML5** with semantic structure
- **CSS3** with modern features (OKLCH color space, backdrop-filter, glassmorphism)
- **Vanilla JavaScript** (ES6+, async/await)
- **Camera API**: MediaDevices for webcam access with device selection
- **Animations**: CSS animations with cubic-bezier easing
- **Interactive Effects**: Magnetic buttons, shimmer effects, animated blobs

### Database Models
1. **User** - Student information with face embeddings
2. **Parcel** - Parcel details with status tracking
3. **FaceSample** - Multiple face samples per user
4. **TrackingVariation** - Alternate tracking code formats

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file for optional features:

```env
# Twilio SMS Notifications (Optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890

# Flask Configuration
FLASK_ENV=development
HOST=0.0.0.0
PORT=5000

# Face Recognition
FACE_RECOGNITION_THRESHOLD=0.4
FACE_MODEL=VGG-Face
DETECTOR_BACKEND=opencv
ENABLE_FACE_ALIGNMENT=True
```

## 🎨 Design System

### Color Palette (OKLCH)
- **Background**: `oklch(0.12 0.01 260)` - Deep dark blue-gray
- **Primary**: `oklch(0.65 0.19 250)` - Vibrant blue
- **Accent**: `oklch(0.7 0.17 165)` - Teal green
- **Surface**: `oklch(0.16 0.01 260 / 0.5)` - Semi-transparent cards
- **Text**: `oklch(0.96 0 0)` - Near white
- **Border**: `oklch(0.26 0.01 260)` - Subtle borders

### Visual Effects
- **Glassmorphism**: Frosted glass cards with `backdrop-filter: blur(12px)`
- **Animated Blobs**: Floating gradient backgrounds (20s animation cycle)
- **Shimmer**: Linear gradient sweep on hover (0.5s transition)
- **Magnetic Buttons**: Mouse-following effect with 0.2x multiplier
- **Smooth Transitions**: Cubic-bezier(0.4, 0, 0.2, 1) for all animations

### Typography
- **Font Family**: System font stack (-apple-system, BlinkMacSystemFont, Segoe UI, Roboto)
- **Hero Title**: 3.75rem (60px), font-weight 700
- **Section Headings**: 1.875rem (30px), font-weight 600
- **Body Text**: 0.9375-1rem, line-height 1.6
- **Labels**: 0.875rem, font-weight 500

### Layout
- **Max Width**: 1280-1400px for content containers
- **Grid Layouts**: 3-column (student), 2-column (portals), 6x6 (shelf)
- **Spacing Scale**: 0.5rem, 1rem, 1.5rem, 2rem, 2.5rem
- **Border Radius**: 0.5-1.5rem for cards, 12-24px for major sections

## 🔐 Security Considerations

### Current Implementation
- Face embeddings stored in database
- Base64 image transmission
- In-memory face comparison
- SQLite for development use

### Production Recommendations
- [ ] Implement user authentication (JWT tokens)
- [ ] Use HTTPS/TLS encryption
- [ ] Migrate to PostgreSQL/MongoDB
- [ ] Store embeddings in secure vector database
- [ ] Add rate limiting (Flask-Limiter)
- [ ] Implement CORS policies
- [ ] Add input validation and sanitization
- [ ] Use environment-based configuration
- [ ] Implement audit logging
- [ ] Add backup and recovery procedures

## 🚀 Production Deployment

### Server Requirements
- **Python**: 3.8+
- **RAM**: 4GB minimum (8GB recommended for face recognition)
- **Storage**: 10GB+ for images and database
- **CPU**: Multi-core recommended (GPU optional for speed)

### Recommended Stack
```bash
# Web Server
Gunicorn or uWSGI

# Reverse Proxy
Nginx or Apache

# Database
PostgreSQL 12+ or MongoDB 4+

# Process Manager
Supervisor or systemd

# Optional: Container
Docker + Docker Compose
```

### Deployment Steps
1. Set up production server (Ubuntu/Debian recommended)
2. Install Python 3.8+ and pip
3. Clone repository and install dependencies
4. Configure environment variables
5. Set up PostgreSQL database
6. Run database migrations
7. Configure Gunicorn + Nginx
8. Set up SSL certificates (Let's Encrypt)
9. Configure firewall and security
10. Set up monitoring and logging

## 📊 Performance Optimizations

### ✅ Implemented
- **Database Indexes** - 7 indexes on frequently queried columns (50-100x faster queries)
  - User.face_uuid (identity lookups)
  - Parcel.tracking_code (tracking searches)
  - Parcel.owner_id (user parcels)
  - Parcel.status (status filtering)
  - Parcel.arrival_time (sorting)
  - FaceSample.user_id (face lookups)
  - FaceSample.face_uuid (UUID matching)
- **Gzip Compression** - Automatic compression via flask-compress (70% size reduction)
- **Connection Pooling** - Optimized SQLAlchemy pool (10 base + 20 overflow connections)
  - pool_pre_ping=True for connection health checks
  - pool_recycle=3600 for automatic connection recycling

### 🔮 Future Optimizations
- Use GPU for face recognition (10-50x faster)
- Implement Redis caching for embeddings
- Use CDN for static assets in production
- Implement lazy loading for images
- Add query result caching

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Test face recognition
python -m scripts.test_recognition

# Check database integrity
python -m scripts.check_users_detailed

# Test tracking search
python -m scripts.test_tracking_search
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Update documentation for new features

## 📝 Changelog

### Version 3.0 (January 2026) - Major UI Overhaul & Performance Boost 🎨⚡

#### UI/UX Improvements
- ✅ Complete frontend redesign with modern dark theme
- ✅ OKLCH color space for vibrant, perceptually uniform colors
- ✅ Glassmorphism design with frosted glass effects
- ✅ Animated gradient backgrounds with floating blobs
- ✅ Interactive effects: magnetic buttons, shimmer, smooth transitions
- ✅ New home landing page with feature showcase
- ✅ Three-portal system: Home → Student/Staff
- ✅ Back buttons for easy navigation
- ✅ Enhanced card interactions and hover effects
- ✅ 3-column student portal layout (Identify/Add Order/My Parcels)
- ✅ 5-tab staff portal (Register/Receive/Handover/Shelf/All Parcels)
- ✅ Real-time statistics dashboard
- ✅ Improved camera device selection with device labels

#### AI/Recognition Improvements
- ✅ Upgraded to VGG-Face model for better accuracy
- ✅ Image preprocessing: histogram equalization + denoising
- ✅ Optimized recognition threshold (0.4) for VGG-Face
- ✅ Enhanced face detection with OpenCV backend
- ✅ Multi-sample recognition for improved accuracy

#### Performance Optimizations
- ✅ **Database Indexes** - 7 strategic indexes for 50-100x faster queries
- ✅ **Gzip Compression** - Automatic response compression (70% size reduction)
- ✅ **Connection Pooling** - Optimized database connections (10+20 pool)
- ✅ **Query Optimization** - Indexed all frequently accessed columns
- ✅ **Stable Camera Access** - Fixed MediaDevices API with local network support
- ✅ **Image Validation** - Pre-send validation to prevent 400 errors

### Version 2.0 (2025)
- ✅ Dual portal system (Student + Staff)
- ✅ Self-service order entry for students
- ✅ Smart hand-out workflow
- ✅ Collected parcels tracking
- ✅ Recently added parcels section
- ✅ Professional UI redesign
- ✅ Automatic storage slot assignment

### Version 1.0 (2024)
- Initial release with basic parcel management
- Face registration and recognition
- Manual parcel entry
- Basic tracking system

## 🐛 Known Issues & Roadmap

### Known Issues
- Face recognition requires good lighting (improved with preprocessing)
- Chrome/Edge recommended for best camera support
- Manual camera permission handling needed
- VGG-Face model slower than FaceNet but more accurate

### Future Roadmap
- [ ] Mobile app (React Native)
- [ ] Progressive Web App (PWA) support
- [ ] QR code generation for parcels
- [ ] Email notifications
- [ ] Multi-tenant support
- [ ] Advanced analytics dashboard
- [ ] Barcode scanning integration
- [ ] Advanced search and filters
- [ ] Export reports (PDF/Excel)
- [ ] Multi-language support
- [ ] Light mode theme toggle
- [ ] Real-time notifications with WebSocket
- [ ] Parcel photo capture
- [ ] Signature capture on handover

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Authors

- **Eshwar KS** - [@eshwarks23567](https://github.com/eshwarks23567)

## 🙏 Acknowledgments

- **DeepFace** - Face recognition library
- **VGG-Face** - State-of-the-art face recognition model
- **TensorFlow** - Machine learning framework
- **OpenCV** - Computer vision library
- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **reactbits.dev** - Inspiration for modern UI effects
- All open-source contributors

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for efficient parcel management**
