# 💕 Kagai - Love Notes App

A beautiful, responsive Django web application for sharing love notes and connecting with people around the world!

## ✨ Features

### Authentication
- 🔐 User Registration with validation
- 🔑 Secure Login/Logout
- 📝 Profile Management
- 👤 User Profiles with extended information

### Core Features
- 💌 Send and receive anonymous love notes
- 👥 Connect and friend with other users
- 💬 View and respond to messages
- ⭐ Favorite your favorite notes
- 🔍 Browse users with filters and search
- 📱 Fully responsive mobile-friendly design

### User Management
- 👨‍👩‍👧‍👦 Connection requests and acceptance
- 📊 Dashboard with statistics
- 🎯 User discovery and recommendations
- 🔒 Privacy controls for anonymous notes

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd c:\Users\hp\Valentine\valentine
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📝 Usage

### For Users

1. **Register**: Create a new account on the registration page
2. **Set up Profile**: Edit your profile with bio, interests, location, etc.
3. **Browse Users**: Discover other users and view their profiles
4. **Send Notes**: Send love notes to people you like (can be anonymous!)
5. **Connect**: Send connection requests to build your network
6. **Dashboard**: View statistics and recent activity

### For Admins

1. Access the admin panel at `/admin/`
2. Manage users, profiles, notes, and connections
3. View user activity and moderate content

## 🎨 Design

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Bootstrap 5**: Modern responsive UI framework
- **Custom CSS**: Beautiful gradient designs and smooth animations
- **Font Awesome**: 6000+ icons
- **Dark Mode Support**: Automatic dark mode support

## 📁 Project Structure

```
valentine/
├── kagai/                    # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
├── valentine/               # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── includes/            # Template includes
│   └── kagai/               # App templates
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       └── main.js          # JavaScript
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## 🗂️ Database Models

### UserProfile
- Extended Django User model
- Bio, avatar, interests, location
- Gender, date of birth
- Website and phone

### LoveNote
- From user to user
- Title and content
- Status tracking (draft, sent, opened, liked)
- Anonymous option
- Timestamps for sent/opened

### Connection
- User to user relationships
- Status (pending, accepted, blocked)
- Created/updated timestamps

### Favorite
- Bookmark favorite notes
- User-note relationships
- Self-referential many-to-many

## 🔐 Security Features

- CSRF protection on all forms
- Password validation
- Session management
- Permission-based access control
- Anonymous note privacy

## 📱 Responsive Breakpoints

- **Mobile**: < 576px
- **Tablet**: 576px - 992px
- **Desktop**: > 992px
- **Large Screen**: > 1200px

## 🎯 Future Enhancements

- [ ] Real-time notifications
- [ ] Message threading/conversations
- [ ] Image uploads in notes
- [ ] Emoji reactions
- [ ] Social sharing
- [ ] Advanced search filters
- [ ] User recommendations
- [ ] Mobile app
- [ ] Email notifications
- [ ] Comment systems

## 🤝 Contributing

Feel free to fork this project and submit pull requests!

## 📞 Support

For issues and questions, please open an issue on the project repository.

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips

- **Disable Debug Mode**: Set `DEBUG = False` in settings.py for production
- **Set Secure Cookies**: Add `SECURE_BROWSER_XSS_FILTER = True` in settings.py
- **Use Environment Variables**: Store sensitive data in .env files
- **Static Files**: Run `python manage.py collectstatic` for production

## 🎉 Made with ❤️

Thank you for using Kagai! Share the love! 💕

---

**Version**: 1.0.0  
**Last Updated**: February 2026
