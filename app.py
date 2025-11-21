from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Item
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus-marketplace-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Routes
@app.route('/')
def index():
    items = Item.query.filter_by(sold=False).order_by(Item.created_at.desc()).limit(8).all()
    return render_template('index.html', items=items)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered! Please use a different email.')
            return redirect(url_for('register'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login to continue.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password! Please try again.')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully!')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access your dashboard.')
        return redirect(url_for('login'))
    
    user_items = Item.query.filter_by(seller_id=session['user_id']).order_by(Item.created_at.desc()).all()
    return render_template('dashboard.html', items=user_items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        flash('Please login to add items.')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']
        
        # Basic validation
        if not title or not description or not price:
            flash('Please fill in all required fields.')
            return redirect(url_for('add_item'))
        
        try:
            price = float(price)
            if price <= 0:
                flash('Price must be greater than 0.')
                return redirect(url_for('add_item'))
        except ValueError:
            flash('Please enter a valid price.')
            return redirect(url_for('add_item'))
        
        item = Item(
            title=title,
            description=description,
            price=price,
            category=category,
            seller_id=session['user_id']
        )
        
        db.session.add(item)
        db.session.commit()
        flash('Item listed successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html')

@app.route('/marketplace')
def marketplace():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    query = Item.query.filter_by(sold=False)
    
    if search:
        query = query.filter(Item.title.contains(search) | Item.description.contains(search))
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    items = query.order_by(Item.created_at.desc()).all()
    
    categories = ['books', 'electronics', 'furniture', 'clothing', 'other']
    
    return render_template('marketplace.html', items=items, category=category, categories=categories, search=search)

@app.route('/buy_item/<int:item_id>')
def buy_item(item_id):
    if 'user_id' not in session:
        flash('Please login to purchase items.')
        return redirect(url_for('login'))
    
    item = Item.query.get(item_id)
    if item:
        if item.sold:
            flash('This item has already been sold!')
        elif item.seller_id == session['user_id']:
            flash('You cannot buy your own item!')
        else:
            item.sold = True
            db.session.commit()
            flash('Item purchased successfully! Thank you for your purchase.')
    else:
        flash('Item not found!')
    
    return redirect(url_for('marketplace'))

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    item = Item.query.get(item_id)
    if item and item.seller_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database created successfully!")
        print("Starting Campus Marketplace...")
        print("Visit: http://127.0.0.1:5000")
    
    app.run(debug=True, host='127.0.0.1', port=5000)