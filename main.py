import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort
from models import db, User, Content, UserFavorite, ReadingHistory
from config import SECRET_KEY, DATABASE_URL, ADMIN_PASSWORD, CONTENT_CATEGORIES, CATEGORY_DISPLAY_NAMES

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            abort(404)
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def utility_processor():
    return {
        'categories': CONTENT_CATEGORIES,
        'category_names': CATEGORY_DISPLAY_NAMES
    }

@app.route('/')
def index():
    latest_content = Content.query.order_by(Content.created_at.desc()).limit(6).all()
    stories = Content.query.filter_by(category='story').order_by(Content.created_at.desc()).limit(4).all()
    poems = Content.query.filter_by(category='poem').order_by(Content.created_at.desc()).limit(4).all()
    life_stories = Content.query.filter_by(category='life').order_by(Content.created_at.desc()).limit(4).all()
    history = Content.query.filter_by(category='history').order_by(Content.created_at.desc()).limit(4).all()
    
    return render_template('index.html',
                         latest_content=latest_content,
                         stories=stories,
                         poems=poems,
                         life_stories=life_stories,
                         history=history)

@app.route('/content/<int:content_id>')
def content_detail(content_id):
    from datetime import datetime
    content = Content.query.get_or_404(content_id)
    
    related = Content.query.filter(
        Content.id != content_id,
        Content.category == content.category
    ).order_by(Content.created_at.desc()).limit(3).all()
    
    is_favorite = False
    if 'user_id' in session:
        favorite = UserFavorite.query.filter_by(
            user_id=session['user_id'],
            content_id=content_id
        ).first()
        is_favorite = favorite is not None
        
        history = ReadingHistory.query.filter_by(
            user_id=session['user_id'],
            content_id=content_id
        ).first()
        
        if history:
            history.read_at = datetime.utcnow()
            history.read_count += 1
        else:
            history = ReadingHistory(user_id=session['user_id'], content_id=content_id)
            db.session.add(history)
        db.session.commit()
    
    return render_template('content_detail.html', 
                         content=content, 
                         related=related,
                         is_favorite=is_favorite)

@app.route('/explore')
def explore():
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    language = request.args.get('language', '')
    tag = request.args.get('tag', '')
    
    query = Content.query
    
    if category and category in CONTENT_CATEGORIES:
        query = query.filter_by(category=category)
    
    if language:
        query = query.filter_by(language=language)
    
    if tag:
        query = query.filter(Content.tags.ilike(f'%{tag}%'))
    
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Content.title.ilike(search_term),
                Content.body.ilike(search_term),
                Content.tags.ilike(search_term)
            )
        )
    
    content = query.order_by(Content.created_at.desc()).all()
    
    languages = db.session.query(Content.language).distinct().all()
    languages = sorted([l[0] for l in languages if l[0]])
    
    all_tags = set()
    all_content = Content.query.all()
    for c in all_content:
        for t in c.get_tags_list():
            all_tags.add(t)
    popular_tags = sorted(list(all_tags))[:12]
    
    return render_template('explore.html', 
                         content=content, 
                         current_category=category,
                         current_language=language,
                         current_tag=tag,
                         search_term=search,
                         languages=languages,
                         popular_tags=popular_tags)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        errors = []
        
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('signup.html', name=name, email=email)
        
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash('Account created successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/my-library')
@login_required
def my_library():
    favorites = UserFavorite.query.filter_by(user_id=session['user_id']).order_by(UserFavorite.created_at.desc()).all()
    recent_history = ReadingHistory.query.filter_by(user_id=session['user_id']).order_by(ReadingHistory.read_at.desc()).limit(10).all()
    return render_template('my_library.html', favorites=favorites, recent_history=recent_history)

@app.route('/reading-history')
@login_required
def reading_history():
    history = ReadingHistory.query.filter_by(user_id=session['user_id']).order_by(ReadingHistory.read_at.desc()).all()
    return render_template('reading_history.html', history=history)

@app.route('/clear-history', methods=['POST'])
@login_required
def clear_history():
    ReadingHistory.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash('Reading history cleared.', 'success')
    return redirect(url_for('reading_history'))

@app.route('/toggle-favorite/<int:content_id>', methods=['POST'])
@login_required
def toggle_favorite(content_id):
    content = Content.query.get_or_404(content_id)
    
    existing = UserFavorite.query.filter_by(
        user_id=session['user_id'],
        content_id=content_id
    ).first()
    
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'status': 'removed', 'message': 'Removed from favorites'})
    else:
        favorite = UserFavorite(user_id=session['user_id'], content_id=content_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added', 'message': 'Added to favorites'})

@app.route('/secret-admin-login', methods=['GET', 'POST'])
def secret_admin_login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        
        if password == ADMIN_PASSWORD:
            session['is_admin'] = True
            flash('Admin access granted.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin password.', 'error')
    
    return render_template('secret_admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    content = Content.query.order_by(Content.created_at.desc()).all()
    return render_template('admin_dashboard.html', content=content)

@app.route('/admin/content/new', methods=['GET', 'POST'])
@admin_required
def admin_new_content():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '')
        language = request.form.get('language', 'English').strip()
        tags = request.form.get('tags', '').strip()
        body = request.form.get('body', '').strip()
        
        errors = []
        if not title:
            errors.append('Title is required.')
        if not category or category not in CONTENT_CATEGORIES:
            errors.append('Valid category is required.')
        if not body:
            errors.append('Content body is required.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin_edit_content.html', 
                                 content=None, 
                                 is_new=True,
                                 title=title,
                                 category=category,
                                 language=language,
                                 tags=tags,
                                 body=body)
        
        content = Content(
            title=title,
            category=category,
            language=language,
            tags=tags,
            body=body
        )
        db.session.add(content)
        db.session.commit()
        
        flash('Content created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_content.html', content=None, is_new=True)

@app.route('/admin/content/<int:content_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_content(content_id):
    content = Content.query.get_or_404(content_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '')
        language = request.form.get('language', 'English').strip()
        tags = request.form.get('tags', '').strip()
        body = request.form.get('body', '').strip()
        
        errors = []
        if not title:
            errors.append('Title is required.')
        if not category or category not in CONTENT_CATEGORIES:
            errors.append('Valid category is required.')
        if not body:
            errors.append('Content body is required.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('admin_edit_content.html', 
                                 content=content, 
                                 is_new=False)
        
        content.title = title
        content.category = category
        content.language = language
        content.tags = tags
        content.body = body
        db.session.commit()
        
        flash('Content updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_content.html', content=content, is_new=False)

@app.route('/admin/content/<int:content_id>/delete', methods=['POST'])
@admin_required
def admin_delete_content(content_id):
    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    flash('Content deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Admin session ended.', 'success')
    return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
