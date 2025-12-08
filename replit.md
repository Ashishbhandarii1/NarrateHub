# NarrateHub - Narrated Content Library

## Overview
A full-stack web application that hosts multiple types of written content (stories, news, poems, dialogues, life stories, history bites) with text-to-speech narration using the Web Speech API.

## Tech Stack
- **Backend**: Python Flask
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Theme**: Strictly black, white, and grayscale with smooth animations

## Project Structure
```
├── main.py              # Flask app entrypoint with all routes
├── config.py            # Configuration (DB, secrets, admin password)
├── models.py            # SQLAlchemy database models
├── seed_content.py      # Script to populate sample content
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── content_detail.html
│   ├── explore.html
│   ├── login.html
│   ├── signup.html
│   ├── my_library.html
│   ├── secret_admin_login.html
│   ├── admin_dashboard.html
│   └── admin_edit_content.html
└── static/
    ├── css/style.css    # Full styling with animations
    └── js/
        ├── main.js      # General functionality
        ├── animations.js # Scroll/intersection animations
        └── tts.js       # Text-to-speech functionality
```

## Features

### Public Features
- Browse content by category (Stories, News, Poems, Dialogues, Life Stories, History Bites)
- Read full content with metadata (title, category, language, tags, date)
- Text-to-Speech narration with female voice preference
- Search and filter content
- User registration and login
- Save content to personal library (favorites)

### Admin Features (Hidden)
- Access via `/secret-admin-login` (password: `admin123`)
- Dashboard to view all content
- Add, edit, and delete content
- Never linked from public UI

## Running the Application
The app runs on port 5000. Start with:
```bash
python main.py
```

## Database
Uses PostgreSQL with these tables:
- `users` - User accounts with hashed passwords
- `content` - All content items with categories
- `user_favorites` - Saved content per user

## Security Notes
- Passwords are hashed using werkzeug.security
- Admin password is only checked server-side
- Session-based authentication
- Admin routes protected with decorator
