"""
Enhanced Donation Form Application - Docker Ready
Features: Environment Variables Support, Production Ready
"""

from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os
from datetime import datetime

app = Flask(__name__)

# Comprehensive Country-State-City Data
COUNTRIES_DATA = {
    "India": {
        "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Tirupati", "Kurnool", "Rajahmundry", "Eluru", "Ongole", "Anantapur"],
        "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang", "Ziro"],
        "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tezpur", "Tinsukia", "Bongaigaon"],
        "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga", "Purnia", "Ara", "Begusarai"],
        "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Jagdalpur", "Ambikapur", "Rajnandgaon"],
        "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"],
        "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Junagadh", "Anand", "Nadiad"],
        "Haryana": ["Chandigarh", "Gurgaon", "Faridabad", "Panipat", "Ambala", "Hisar", "Karnal", "Rohtak", "Sonipat"],
        "Himachal Pradesh": ["Shimla", "Dharamshala", "Solan", "Mandi", "Kullu", "Una", "Hamirpur", "Bilaspur"],
        "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh", "Giridih", "Ramgarh", "Chaibasa"],
        "Karnataka": ["Bangalore", "Mysore", "Hubli", "Dharwad", "Mangalore", "Belgaum", "Bellary", "Tumkur", "Shimoga", "Udupi"],
        "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Alappuzha", "Palakkad", "Kannur"],
        "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Rewa", "Satna", "Ratlam", "Dewas", "Katni", "Singrauli", "Burhanpur", "Khandwa", "Chhindwara", "Shivpuri", "Vidisha", "Sehore", "Hoshangabad", "Itarsi", "Betul", "Harda", "Seoni", "Balaghat", "Raisen"],
        "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Thane", "Solapur", "Kolhapur", "Amravati", "Akola"],
        "Manipur": ["Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Ukhrul"],
        "Meghalaya": ["Shillong", "Tura", "Nongstoin", "Jowai", "Baghmara"],
        "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Serchhip", "Kolasib"],
        "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha"],
        "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri", "Sambalpur", "Balasore", "Baripada", "Jharsuguda"],
        "Punjab": ["Chandigarh", "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Hoshiarpur", "Mohali"],
        "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Alwar", "Sikar", "Bharatpur"],
        "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan", "Rangpo"],
        "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Erode", "Vellore", "Tirunelveli", "Thoothukudi"],
        "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar", "Mahbubnagar", "Adilabad"],
        "Tripura": ["Agartala", "Dharmanagar", "Udaipur", "Kailashahar", "Belonia"],
        "Uttar Pradesh": ["Lucknow", "Kanpur", "Ghaziabad", "Agra", "Varanasi", "Prayagraj", "Noida", "Meerut", "Aligarh", "Bareilly"],
        "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Nainital", "Rudrapur", "Haldwani", "Rishikesh"],
        "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Kharagpur", "Malda", "Bardhaman"],
        "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi"],
        "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Udhampur"],
        "Ladakh": ["Leh", "Kargil"],
        "Puducherry": ["Puducherry", "Karaikal", "Mahe", "Yanam"],
        "Chandigarh": ["Chandigarh"],
        "Andaman and Nicobar Islands": ["Port Blair", "Diglipur", "Car Nicobar"],
        "Lakshadweep": ["Kavaratti", "Agatti", "Minicoy"],
        "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"]
    },
    "United States": {
        "Alabama": ["Birmingham", "Montgomery", "Mobile", "Huntsville", "Tuscaloosa"],
        "Alaska": ["Anchorage", "Fairbanks", "Juneau", "Sitka", "Ketchikan"],
        "Arizona": ["Phoenix", "Tucson", "Mesa", "Chandler", "Scottsdale"],
        "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose", "Oakland", "Fresno"],
        "Colorado": ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood"],
        "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville", "Fort Lauderdale", "Tallahassee"],
        "Georgia": ["Atlanta", "Augusta", "Columbus", "Savannah", "Athens"],
        "Illinois": ["Chicago", "Aurora", "Naperville", "Joliet", "Rockford"],
        "New York": ["New York City", "Buffalo", "Rochester", "Albany", "Syracuse"],
        "Texas": ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "El Paso"],
        "Washington": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue"]
    },
    "United Kingdom": {
        "England": ["London", "Manchester", "Birmingham", "Liverpool", "Leeds", "Sheffield", "Bristol"],
        "Scotland": ["Edinburgh", "Glasgow", "Aberdeen", "Dundee", "Inverness"],
        "Wales": ["Cardiff", "Swansea", "Newport", "Wrexham", "Barry"],
        "Northern Ireland": ["Belfast", "Derry", "Lisburn", "Newry", "Armagh"]
    },
    "Canada": {
        "Alberta": ["Calgary", "Edmonton", "Red Deer", "Lethbridge", "Medicine Hat"],
        "British Columbia": ["Vancouver", "Victoria", "Kelowna", "Kamloops", "Nanaimo"],
        "Ontario": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London", "Windsor"],
        "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau", "Sherbrooke"],
        "Manitoba": ["Winnipeg", "Brandon", "Steinbach", "Thompson", "Portage la Prairie"]
    },
    "Australia": {
        "New South Wales": ["Sydney", "Newcastle", "Wollongong", "Central Coast", "Maitland"],
        "Victoria": ["Melbourne", "Geelong", "Ballarat", "Bendigo", "Shepparton"],
        "Queensland": ["Brisbane", "Gold Coast", "Sunshine Coast", "Townsville", "Cairns"],
        "Western Australia": ["Perth", "Mandurah", "Bunbury", "Kalgoorlie", "Geraldton"],
        "South Australia": ["Adelaide", "Mount Gambier", "Whyalla", "Murray Bridge", "Port Augusta"]
    },
    "Germany": {
        "Bavaria": ["Munich", "Nuremberg", "Augsburg", "Regensburg", "Ingolstadt"],
        "Berlin": ["Berlin"],
        "Hamburg": ["Hamburg"],
        "Hesse": ["Frankfurt", "Wiesbaden", "Kassel", "Darmstadt", "Offenbach"],
        "North Rhine-Westphalia": ["Cologne", "Düsseldorf", "Dortmund", "Essen", "Duisburg"]
    },
    "France": {
        "Île-de-France": ["Paris", "Versailles", "Boulogne-Billancourt", "Saint-Denis", "Nanterre"],
        "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Toulon", "Aix-en-Provence", "Cannes"],
        "Auvergne-Rhône-Alpes": ["Lyon", "Grenoble", "Saint-Étienne", "Villeurbanne", "Clermont-Ferrand"],
        "Nouvelle-Aquitaine": ["Bordeaux", "Limoges", "Poitiers", "Pau", "La Rochelle"]
    },
    "Japan": {
        "Tokyo": ["Tokyo", "Hachioji", "Machida", "Fuchu", "Chofu"],
        "Osaka": ["Osaka", "Sakai", "Higashiosaka", "Toyonaka", "Suita"],
        "Kyoto": ["Kyoto", "Uji", "Kameoka", "Joyo", "Muko"],
        "Hokkaido": ["Sapporo", "Asahikawa", "Hakodate", "Kushiro", "Obihiro"]
    },
    "China": {
        "Beijing": ["Beijing"],
        "Shanghai": ["Shanghai"],
        "Guangdong": ["Guangzhou", "Shenzhen", "Dongguan", "Foshan", "Zhuhai"],
        "Zhejiang": ["Hangzhou", "Ningbo", "Wenzhou", "Jinhua", "Shaoxing"]
    },
    "Brazil": {
        "São Paulo": ["São Paulo", "Campinas", "Santos", "Ribeirão Preto", "Sorocaba"],
        "Rio de Janeiro": ["Rio de Janeiro", "Niterói", "Duque de Caxias", "Nova Iguaçu", "Belford Roxo"],
        "Minas Gerais": ["Belo Horizonte", "Uberlândia", "Contagem", "Juiz de Fora", "Betim"],
        "Bahia": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Camaçari", "Itabuna"]
    },
    "South Africa": {
        "Gauteng": ["Johannesburg", "Pretoria", "Soweto", "Benoni", "Boksburg"],
        "Western Cape": ["Cape Town", "Stellenbosch", "George", "Paarl", "Worcester"],
        "KwaZulu-Natal": ["Durban", "Pietermaritzburg", "Richards Bay", "Newcastle", "Port Shepstone"]
    },
    "Mexico": {
        "Mexico City": ["Mexico City"],
        "Jalisco": ["Guadalajara", "Zapopan", "Tlaquepaque", "Tonalá", "Puerto Vallarta"],
        "Nuevo León": ["Monterrey", "San Nicolás de los Garza", "Guadalupe", "Apodaca", "San Pedro Garza García"],
        "Puebla": ["Puebla", "Tehuacán", "San Martín Texmelucan", "Atlixco", "Cholula"]
    }
}

# Email Configuration - Support Environment Variables
EMAIL_CONFIG = {
    'sender_email': os.getenv('SENDER_EMAIL', 'amanpandit4756@gmail.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', 'agyb kiry rorx wroq'),
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    'smtp_port': int(os.getenv('SMTP_PORT', 465))
}

def validate_mobile(mobile):
    """Validate 10-digit mobile number"""
    return bool(re.match(r'^\d{10}$', mobile))

def validate_email(email):
    """Validate email format"""
    if not email:
        return True
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def send_confirmation_email(name, email, amount, donation_for, donation_type):
    """Send confirmation email to donor"""
    if not email:
        return True, "No email provided"
    
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Thank You for Your Donation"
        message["From"] = EMAIL_CONFIG['sender_email']
        message["To"] = email
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #4CAF50; border-bottom: 3px solid #4CAF50; padding-bottom: 10px;">
                        Thank You for Your Generous Donation!
                    </h2>
                    <p style="font-size: 16px; color: #333;">Dear <strong>{name}</strong>,</p>
                    
                    <p style="font-size: 16px; color: #333; line-height: 1.6;">
                        We sincerely thank you for your generous donation. Your contribution will make 
                        a significant difference in the lives of those we serve.
                    </p>
                    
                    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #333; margin-top: 0;">Donation Details:</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Amount:</strong></td>
                                <td style="padding: 8px 0; color: #333;">₹{amount}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Donation For:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{donation_for}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Payment Method:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{donation_type}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; color: #666;"><strong>Date:</strong></td>
                                <td style="padding: 8px 0; color: #333;">{datetime.now().strftime('%B %d, %Y')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p style="font-size: 16px; color: #333; line-height: 1.6;">
                        Your support helps us continue our mission and make a positive impact in the community.
                    </p>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                        <p style="color: #666; margin-bottom: 5px;">Warm regards,</p>
                        <p style="color: #333; font-weight: bold; margin-top: 5px;">The Donation Team</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        with smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.sendmail(EMAIL_CONFIG['sender_email'], email, message.as_string())
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"

@app.route('/')
def index():
    """Render donation form"""
    return render_template('index.html', countries=sorted(list(COUNTRIES_DATA.keys())))

@app.route('/api/states/<country>')
def get_states(country):
    """API endpoint to get states for a country"""
    if country in COUNTRIES_DATA:
        return jsonify(sorted(list(COUNTRIES_DATA[country].keys())))
    return jsonify([])

@app.route('/api/cities/<country>/<state>')
def get_cities(country, state):
    """API endpoint to get cities for a state"""
    if country in COUNTRIES_DATA and state in COUNTRIES_DATA[country]:
        return jsonify(sorted(COUNTRIES_DATA[country][state]))
    return jsonify([])

@app.route('/submit', methods=['POST'])
def submit_donation():
    """Process donation form submission"""
    try:
        data = request.form
        
        name = data.get('name', '').strip()
        mobile = data.get('mobile', '').strip()
        email = data.get('email', '').strip()
        address = data.get('address', '').strip()
        country = data.get('country', '').strip()
        state = data.get('state', '').strip()
        city = data.get('city', '').strip()
        donation_for = data.get('donation_for', '').strip()
        amount = data.get('amount', '').strip()
        donation_type = data.get('donation_type', '').strip()
        
        errors = []
        
        if not name:
            errors.append("Name is required")
        
        if not mobile:
            errors.append("Mobile number is required")
        elif not validate_mobile(mobile):
            errors.append("Mobile number must be 10 digits")
        
        if email and not validate_email(email):
            errors.append("Invalid email format")
        
        if not country:
            errors.append("Country is required")
        
        if not state:
            errors.append("State is required")
        
        if not city:
            errors.append("City is required")
        
        if not donation_for:
            errors.append("Donation purpose is required")
        
        if not amount:
            errors.append("Donation amount is required")
        else:
            try:
                amount_float = float(amount)
                if amount_float <= 0:
                    errors.append("Donation amount must be greater than 0")
            except ValueError:
                errors.append("Donation amount must be a valid number")
        
        if not donation_type:
            errors.append("Donation type is required")
        
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        email_sent, email_message = send_confirmation_email(
            name, email, amount, donation_for, donation_type
        )
        
        return jsonify({
            'success': True,
            'message': f'Thank you {name}! Your donation of ₹{amount} has been registered successfully.',
            'email_sent': email_sent,
            'email_message': email_message
        })
        
    except Exception as e:
        return jsonify({'success': False, 'errors': [str(e)]}), 500

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Donation Platform on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(debug=debug, host=host, port=port)
