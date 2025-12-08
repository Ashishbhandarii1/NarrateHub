import os

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

# Secret key for Flask sessions
SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

# Admin password - only checked on backend, never exposed to frontend
ADMIN_PASSWORD = "admin123"

# Content categories
CONTENT_CATEGORIES = ['story', 'news', 'poem', 'dialogue', 'life', 'history']

# Category display names
CATEGORY_DISPLAY_NAMES = {
    'story': 'Stories',
    'news': 'News',
    'poem': 'Poems',
    'dialogue': 'Dialogues',
    'life': 'Life Stories',
    'history': 'History Bites'
}
