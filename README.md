# ❤️ Lucy's Valentine Proposal Website

A beautiful Django-based Valentine's proposal website for Lucy featuring interactive buttons, romantic animations, and confetti celebration!

## 🌐 How to Access

### Local Development (Recommended for testing)
The site is best viewed running locally with Django:

1. **Prerequisites:**
   - Python 3.8+
   - Git

2. **Setup:**
```bash
# Clone the repository
git clone https://github.com/Peter-Kagai5/Ruby.git
cd Ruby

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On Mac/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
cd valentine
python manage.py runserver
```

3. **Access the site:**
   - Home: http://localhost:8000/
   - Valentine Proposal: http://localhost:8000/valentine-proposal/

### Deploy to Free Hosting Platforms

**Option 1: Deploy to Railway (Recommended)**
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect Django and deploy
4. Your site will be live in minutes!

**Option 2: Deploy to Heroku**
1. Create a `Procfile` in the root:
```
web: cd valentine && gunicorn valentine.wsgi
```
2. Create a `runtime.txt`:
```
python-3.9.19
```
3. Push to Heroku

**Option 3: Deploy to PythonAnywhere**
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your files
3. Configure a Python web app pointing to the Django project

## 📁 Project Structure

```
Ruby/
├── valentine/                 # Django project folder
│   ├── valentine/            # Main Django app config
│   ├── kagai/                # App with views and models
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS, images
│   │   └── images/           # Valentine images
│   ├── manage.py
│   └── requirements.txt
├── index.html               # GitHub Pages landing page
└── README.md
```

## 🎨 Features

✨ **Beautiful & Romantic Design**
- Gradient backgrounds
- Valentine's themed colors
- Smooth animations

💕 **Interactive Elements**
- YES/NO buttons for the proposal
- Confetti celebration animation
- Heartbeat animation on images
- Playful NO button that runs away

📝 **5-Paragraph Love Message**
- Appears when she clicks "YES"
- Romantic and heartfelt
- Scrolls into view with animation

🖼️ **Beautiful Images**
- Lucy's photo as main image
- Valentine background images
- Professional styling

## 🚀 Getting Started Quickly

**Quick Start (Local):**
```bash
cd valentine
python manage.py runserver
# Visit http://localhost:8000/
```

**For Public Access:**
- Use Railway, Heroku, or PythonAnywhere (see Deploy section above)
- GitHub Pages alone cannot run Django apps

## 📞 Questions?

This is a Django application that requires a Python runtime to operate. It works perfectly on:
- Local machine with `python manage.py runserver`
- Railway, Heroku, PythonAnywhere
- Any hosting with Python/Django support

## 💝 Special Features

- 🎉 Confetti animation on "YES"
- 💗 Heartbeat animation on images
- 📱 Fully responsive design
- 🎨 Valentine's Day themed styling
- ❤️ 5 paragraphs of romantic messages

---

Made with ❤️ for Lucy. Good luck with your proposal! 💕
