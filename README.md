# 🍎 FoodSave - Food Waste Tracker & Community Donation Platform

**Developed by Anthonia Othetheaso**

A comprehensive web-based application designed to combat food waste through intelligent inventory tracking, expiry monitoring, and community-driven food donation. FoodSave empowers users to reduce household food waste while contributing to **SDG 2: Zero Hunger** by facilitating food sharing within communities.

---

## 🌟 Overview

FoodSave is more than just a food tracking app—it's a complete ecosystem for managing food inventory, preventing waste, and connecting surplus food with those who need it. By combining personal food management with social impact features, FoodSave creates a sustainable solution to one of the world's most pressing challenges.

---

## ✨ Key Features

### 📊 Food Inventory Management
- **Smart Food Tracking**: Add and manage food items with detailed information (name, quantity, category, expiry date, storage location)
- **Expiry Alerts**: Automatic notifications for food items nearing expiration
- **Category Organization**: Organize items by type (Fruits, Vegetables, Dairy, Meat, Grains, Beverages, etc.)
- **Storage Tracking**: Monitor food across different storage locations (refrigerator, freezer, pantry)

### ❤️ Community Donation System
- **Create Donations**: Share surplus food with your community before it goes to waste
- **Browse Donations**: Discover available food donations in your area
- **Claim System**: Secure and claim food donations with pickup location details
- **Donation History**: Track your contributions as both donor and recipient
- **Real-time Updates**: See donation status changes (available, claimed, delivered)

### 📈 Analytics & Insights
- **Waste Tracking**: Monitor food waste patterns over time
- **Impact Metrics**: View meals saved, CO₂ emissions reduced, and water conservation
- **Visual Reports**: Interactive charts showing waste by category, trends, and statistics
- **Data Export**: Generate reports in multiple formats for analysis

### 🔐 User Management
- **Secure Authentication**: User registration and login with password encryption
- **Personal Dashboard**: Customized view of your food inventory and donation activity
- **Profile Management**: Track your contributions and community impact

---

## 🛠️ Technology Stack

### Backend
- **Flask 2.3+** - Python web framework
- **SQLAlchemy** - ORM for database management
- **Flask-Login** - User session management
- **Flask-Migrate** - Database migrations
- **SQLite/PostgreSQL** - Database storage

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Jinja2** - Template engine
- **Chart.js** - Data visualization
- **Custom CSS** - Enhanced animations and styling

### Core Dependencies
```
Flask==2.3.3
Werkzeug==2.3.7
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
Flask-Migrate==4.0.5
WTForms==3.0.1
python-dotenv==1.0.0
email-validator==2.0.0
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd Food_Waste_Tracker
```

#### 2. Create Virtual Environment (Windows)
```powershell
# Using PowerShell
python -m venv .venv
.\.venv\Scripts\Activate

# Using Command Prompt
python -m venv .venv
.venv\Scripts\activate.bat
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 5. Run the Application
```bash
python run.py
```

Visit `http://127.0.0.1:5000` in your browser to access FoodSave.

---

## 📱 Using FoodSave

### Getting Started
1. **Register**: Create your account with username, email, and password
2. **Login**: Access your personal dashboard
3. **Add Food Items**: Start tracking your food inventory
4. **Set Expiry Dates**: Get automatic alerts before food expires
5. **Create Donations**: Share surplus food with your community
6. **Browse & Claim**: Find and claim available donations near you

### Dashboard Features
- **Inventory Overview**: See all your tracked food items at a glance
- **Expiry Warnings**: Quick view of items expiring soon
- **Waste Statistics**: Monitor your waste reduction progress
- **Recent Activity**: Track your latest actions and donations

### Making a Donation
1. Navigate to **Donations → Create Donation**
2. Select a food item from your inventory
3. Specify quantity and pickup location
4. Add optional description
5. Submit to make it available to the community

### Claiming a Donation
1. Browse **Available Donations**
2. Use filters to find specific food items
3. Click **Claim This Donation**
4. Contact donor for pickup details
5. Mark as delivered when complete

---

## 📊 Project Structure

```
Food_Waste_Tracker/
├── app/
│   ├── __init__.py
│   ├── forms.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── donation.py
│   │   └── achievement.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── food.py
│   │   ├── donations.py
│   │   └── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── food_calculations.py
│   │   └── notifications.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   └── templates/
│       ├── base.html
│       ├── landing.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── add_food.html
│       ├── food_simple.html
│       ├── list.html
│       ├── donations.html
│       ├── create.html
│       ├── contact_donor.html
│       ├── my_donations.html
│       ├── my_claims.html
│       └── analytics_dashboard.html
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
├── .env
├── .gitignore
├── app.db
├── config.py
├── create_db.py
├── procfile
├── runtime.txt
├── requirements.txt
├── run.py
└── README.md
```

---

## 🎨 Features in Detail

### Smart Expiry Management
- Color-coded warnings (red: expired, yellow: expiring soon, green: fresh)
- Automatic calculation of days until expiry
- Email/in-app notifications (planned feature)

### Donation Workflow
```
Create → Available → Claimed → Delivered → Completed
```
Each stage is tracked with timestamps and user information.

### Analytics Dashboard
- **Waste by Category**: Pie chart showing distribution
- **Monthly Trends**: Line graph of waste over time
- **Impact Metrics**: Total meals saved, environmental impact
- **Top Wasted Items**: Identify patterns for improvement

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_food_tracking.py
```

### Test Structure
```
tests/
├── test_auth.py           # Authentication tests
├── test_food_tracking.py  # Food inventory tests
├── test_donations.py      # Donation system tests
└── test_analytics.py      # Analytics tests
```

---

## 🔧 Configuration

### Database Configuration
The app uses SQLite by default for development:

```python
# In config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
```

---

## 🌍 Environmental Impact

FoodSave helps users understand their positive impact:

- **Meals Saved**: Each donation prevents food waste and feeds someone in need
- **CO₂ Reduction**: Food waste in landfills produces methane; preventing waste reduces emissions
- **Water Conservation**: Growing food requires water; wasting food wastes water resources

### Impact Calculations
- 1kg of food waste = ~2.5kg CO₂ emissions prevented
- 1kg of produce = ~1000L water saved
- Average donation = 3 meals

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Reporting Issues
1. Check existing issues first
2. Create a detailed bug report with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Screenshots if applicable

### Submitting Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Update documentation as needed
6. Push to your fork and submit a pull request

### Code Style
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

---

## 🐛 Troubleshooting

### Common Issues

**Issue: Virtual environment not activating**
```bash
# Solution: Use execution policy bypass
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\Activate
```

**Issue: Database migration errors**
```bash
# Solution: Reset migrations
rm -rf migrations/
flask db init
flask db migrate
flask db upgrade
```

**Issue: Port 5000 already in use**
```bash
# Solution: Specify different port
flask run --port 5001
```

**Issue: Static files not loading**
- Clear browser cache (Ctrl + Shift + R)
- Check file paths in templates
- Verify Flask is serving static files correctly

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Anthonia Othetheaso**

- Project: FoodSave - Food Waste Tracker
- Purpose: SDG 2 (Zero Hunger) Initiative
- Year: 2025

---

## 🙏 Acknowledgments

- Built with Flask and Bootstrap
- Inspired by global food waste reduction initiatives
- Contributing to United Nations SDG 2: Zero Hunger
- Thanks to the open-source community

---

## 📞 Support & Contact

For questions, suggestions, or support:
- Open an issue in the repository
- Email: [your-email@example.com]
- Documentation: Check the `/docs` folder for detailed guides

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Mobile app (iOS/Android)
- [ ] Email notifications for expiry alerts
- [ ] Barcode scanning for quick item entry
- [ ] Recipe suggestions based on expiring items
- [ ] Community leaderboard for top donors
- [ ] Integration with food banks and charities
- [ ] Multi-language support
- [ ] Advanced analytics with ML predictions

---

## 📊 Statistics

*Track your impact with FoodSave:*
- Reduce food waste by up to 40%
- Save money on groceries
- Help fight hunger in your community
- Contribute to environmental sustainability

---

**Start your journey towards zero food waste today with FoodSave! 🌱**