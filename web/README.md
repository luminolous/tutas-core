# Tutas Learning Platform

A dark-themed multi-page website for connecting students and tutors, built with Next.js frontend and Python Flask backend.

## 🌟 Features

- **Registration Form**: Students and tutors can register with their preferences
- **Available Pairs**: View matched 1-on-1 student-tutor pairs
- **Tutas Circle**: Browse study groups with up to 5 students and 1 tutor
- **Dark Theme**: Professional black and white design
- **Mobile Responsive**: Works on all device sizes
- **Real-time Data**: Connects to Flask backend for live data

## 🚀 Quick Start

### Backend Setup (Python Flask)

1. **Navigate to backend directory**:
   \`\`\`bash
   cd backend
   \`\`\`

2. **Install Python dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run the Flask server**:
   \`\`\`bash
   python app.py
   \`\`\`

   The backend will start on `http://localhost:5000`

### Frontend Setup (Next.js)

1. **Install dependencies** (if not already installed):
   \`\`\`bash
   npm install
   \`\`\`

2. **Run the development server**:
   \`\`\`bash
   npm run dev
   \`\`\`

   The frontend will start on `http://localhost:3000`

## 📡 API Endpoints

### Backend (Flask) - `http://localhost:5000`

- `POST /submit` - Submit registration form
- `GET /available` - Get matched 1-on-1 pairs
- `GET /tutas-circle` - Get study groups
- `GET /registrations` - Get all registrations (admin)
- `GET /health` - Health check

### Example API Usage

**Submit Registration**:
\`\`\`bash
curl -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "John Doe",
    "whatsappNumber": "+6281234567890",
    "status": "Student",
    "courseName": "Mathematics",
    "topicSubtopic": "Calculus basics",
    "preferredDate": "2024-01-15",
    "preferredTime": "14:00",
    "flexibleSchedule": "Yes",
    "learningStyle": "Visual Learning",
    "learningMode": "Online",
    "matchingType": "1-on-1"
  }'
\`\`\`

**Get Available Pairs**:
\`\`\`bash
curl http://localhost:5000/available
\`\`\`

**Get Study Groups**:
\`\`\`bash
curl http://localhost:5000/tutas-circle
\`\`\`

## 📁 Project Structure

\`\`\`
tutas-platform/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Home page (registration form)
│   ├── available/         # Available pairs page
│   ├── tutas-circle/      # Study groups page
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── registration-form.tsx
│   ├── available-users-table.tsx
│   ├── tutas-circle-view.tsx
│   └── navigation.tsx
├── backend/               # Flask backend
│   ├── app.py            # Main Flask application
│   ├── requirements.txt  # Python dependencies
│   └── data/             # JSON data storage
│       ├── registrations.json
│       ├── matched_pairs.json
│       └── study_groups.json
└── README.md
\`\`\`

## 🎨 Design Features

- **Dark Theme**: Black background with white text
- **Responsive Design**: Mobile-friendly layout
- **Interactive Forms**: Real-time validation and feedback
- **Contact Integration**: WhatsApp buttons for easy communication
- **Loading States**: Smooth user experience with loading indicators
- **Error Handling**: Graceful error messages and retry options

## 🔧 Development

### Adding New Features

1. **Frontend**: Add new components in `/components` and pages in `/app`
2. **Backend**: Add new routes in `backend/app.py`
3. **Data**: Modify JSON structure in `backend/data/` files

### Customization

- **Colors**: Modify `app/globals.css` for theme changes
- **API URLs**: Update fetch URLs in components to match your backend
- **Data Structure**: Modify JSON schemas in Flask app and TypeScript interfaces

## 🚀 Deployment

### Frontend (Vercel/Netlify)
1. Build the Next.js app: `npm run build`
2. Deploy to your preferred platform

### Backend (Heroku/Railway/DigitalOcean)
1. Update CORS settings for production domain
2. Use environment variables for configuration
3. Consider using a proper database (PostgreSQL/MongoDB) instead of JSON files

## 📞 Support

For issues or questions:
- Check the console for error messages
- Ensure both frontend and backend are running
- Verify CORS is enabled on the Flask backend
- Check network connectivity between frontend and backend

## 🔄 Sample Data

The backend automatically creates sample data on first run:
- 3 matched pairs in `/available`
- 3 study groups in `/tutas-circle`
- Empty registrations file for new submissions

You can modify this sample data in `backend/app.py` in the `initialize_sample_data()` function.
\`\`\`

Finally, let's update the Tailwind config:
