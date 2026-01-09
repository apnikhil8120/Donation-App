🌍 Global Donation Platform
A comprehensive, multi-country donation management system built with Flask, featuring dynamic country-state-city selection, email notifications, and beautiful animations.

📋 Table of Contents
Features
Technology Stack
Project Structure
Installation
Configuration
Usage
API Endpoints
Database Schema
Countries Supported
Security Features
Troubleshooting
✨ Features
Core Features
🌎 Global Coverage: Support for 15+ countries with complete state/city data
🔄 Dynamic Dropdowns: Cascading country → state → city selection
📧 Email Notifications: Automatic confirmation emails to donors
✅ Form Validation: Client-side and server-side validation
🎨 Beautiful UI: Modern gradient design with smooth animations
📱 Responsive Design: Works on all devices (mobile, tablet, desktop)
🎭 Multiple Themes: Light theme with animated elements
💳 Multiple Payment Methods: Cash, Online, Cheque, Bank Transfer
Animation Features
Fade-in animations on page load
Floating background circles
Shimmer effect on header
Smooth transitions on form interactions
Confetti celebration on successful submission
Loading spinner during form processing
Validation Features
10-digit mobile number validation
Email format validation
Required field checks
Amount validation (must be > 0)
Real-time error messages
🛠 Technology Stack
Backend
Python 3.8+
Flask 3.0.0 - Web framework
Werkzeug 3.0.1 - WSGI toolkit
smtplib - Email sending
Jinja2 3.1.2 - Template engine
Frontend
HTML5
CSS3 (Modern features: Grid, Flexbox, Animations)
Vanilla JavaScript (ES6+)
Fetch API - AJAX requests
Email Service
Gmail SMTP - Email delivery
SSL/TLS - Secure connection
📁 Project Structure
donation-platform/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── templates/
│   └── index.html             # Main donation form template
│
├── static/ (optional)
│   ├── css/
│   ├── js/
│   └── images/
│
└── docs/
    ├── API_DOCUMENTATION.md
    └── ARCHITECTURE.md
🚀 Installation
Prerequisites
Python 3.8 or higher
pip (Python package manager)
Gmail account for email notifications
Step 1: Clone or Download
bash
# Create project directory
mkdir donation-platform
cd donation-platform
Step 2: Create Virtual Environment
bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
requirements.txt:

Flask==3.0.0
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
Step 4: Create Templates Directory
bash
mkdir templates
Step 5: Add Files
Copy app.py to project root
Copy index.html to templates/ folder
⚙️ Configuration
Email Configuration
Enable Gmail App Password
Go to Google Account Settings
Security → 2-Step Verification → App Passwords
Generate new app password
Update Email Config in app.py
python
EMAIL_CONFIG = {
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',  # 16-character app password
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465
}
Port Configuration
python
# Default port is 5000
app.run(debug=True, host='0.0.0.0', port=5000)

# Change port if needed
app.run(debug=True, host='0.0.0.0', port=8080)
🎯 Usage
Starting the Application
bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the application
python app.py
Access the Application
Open your browser and navigate to:

http://localhost:5000
Using the Form
Personal Information
Enter full name (required)
Enter 10-digit mobile number (required)
Enter email (optional, for confirmation)
Enter complete address (optional)
Location Details
Select country (required)
Select state - auto-populated based on country
Select city - auto-populated based on state
Donation Details
Choose donation purpose (required)
Enter amount in rupees (required)
Select payment method (required)
Submit
Click "Submit Donation"
Wait for processing (loading animation)
Receive confirmation message
Email sent automatically if provided
🔌 API Endpoints
1. Main Route
GET /
Returns: Renders the main donation form
2. Get States
GET /api/states/<country>
Parameters:
  - country: string (URL encoded)
Returns: JSON array of states
Example: /api/states/India
Response: ["Andhra Pradesh", "Bihar", ...]
3. Get Cities
GET /api/cities/<country>/<state>
Parameters:
  - country: string (URL encoded)
  - state: string (URL encoded)
Returns: JSON array of cities
Example: /api/cities/India/Haryana
Response: ["Chandigarh", "Gurgaon", ...]
4. Submit Donation
POST /submit
Content-Type: application/x-www-form-urlencoded

Parameters:
  - name: string (required)
  - mobile: string (required, 10 digits)
  - email: string (optional, valid format)
  - address: string (optional)
  - country: string (required)
  - state: string (required)
  - city: string (required)
  - donation_for: string (required)
  - amount: number (required, > 0)
  - donation_type: string (required)

Success Response:
{
  "success": true,
  "message": "Thank you John! Your donation of ₹1000 has been registered.",
  "email_sent": true,
  "email_message": "Email sent successfully"
}

Error Response:
{
  "success": false,
  "errors": ["Name is required", "Mobile number must be 10 digits"]
}
🗄️ Database Schema
Currently using in-memory dictionary. For production, consider:

Donations Table
sql
CREATE TABLE donations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(10) NOT NULL,
    email VARCHAR(255),
    address TEXT,
    country VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    donation_for VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    donation_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_sent BOOLEAN DEFAULT FALSE
);
🌍 Countries Supported
Complete Coverage (15+ Countries)
India - 36 States/UTs with 200+ cities
United States - 11 States with major cities
United Kingdom - 4 Regions
Canada - 5 Provinces
Australia - 5 States
Germany - 5 States
France - 4 Regions
Japan - 4 Prefectures
China - 4 Provinces
Brazil - 4 States
South Africa - 3 Provinces
Mexico - 4 States
Total Coverage:

15+ Countries
100+ States/Provinces
500+ Cities
🔒 Security Features
Input Validation
python
# Mobile validation - exactly 10 digits
def validate_mobile(mobile):
    return bool(re.match(r'^\d{10}$', mobile))

# Email validation - proper format
def validate_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))
Server-Side Checks
Required field validation
Data type validation
Amount must be greater than 0
SQL injection prevention (using parameterized queries)
Email Security
SSL/TLS encryption
App-specific passwords
No plain text password storage
🐛 Troubleshooting
Issue: Email Not Sending
Solution:

Check Gmail app password is correct
Enable "Less secure app access" (if needed)
Check firewall isn't blocking port 465
Verify internet connection
python
# Test email configuration
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('your-email@gmail.com', 'your-app-password')
        print("Email configuration is correct!")
except Exception as e:
    print(f"Email error: {e}")
Issue: States/Cities Not Loading
Solution:

Check browser console for errors
Verify Flask server is running
Check network tab in browser DevTools
Ensure URL encoding is correct
javascript
// Debug in browser console
console.log('Country:', countrySelect.value);
fetch(`/api/states/${encodeURIComponent(countrySelect.value)}`)
    .then(r => r.json())
    .then(data => console.log('States:', data));
Issue: Port Already in Use
Solution:

bash
# Find process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Or change port in app.py
app.run(debug=True, port=8080)
Issue: Module Not Found
Solution:

bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
📈 Future Enhancements
 Add database (SQLite/PostgreSQL)
 User authentication
 Admin dashboard
 Payment gateway integration
 Receipt generation (PDF)
 Multi-language support
 Dark mode theme
 Export donations to Excel
 SMS notifications
 Recurring donations
📝 License
This project is open source and available under the MIT License.

👨‍💻 Developer
Created with ❤️ for making donations easier and more accessible worldwide.

📞 Support
For issues or questions:

Check the troubleshooting section
Review the API documentation
Check browser console for errors
Review Flask server logs
🙏 Acknowledgments
Flask framework team
Font Awesome for icons
Google Fonts
All contributors
Last Updated: January 2026 Version: 1.0.0


