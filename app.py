import os
from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from sqlalchemy import or_, func

from config import Config
from models import db, User, Product, Cart, Order, OrderItem, Contact, Review, Wishlist
from forms import (LoginForm, RegistrationForm, ContactForm, CheckoutForm, ProductForm, 
                   SearchForm, ReviewForm, UpdateAccountForm, ChangePasswordForm)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)
    Bcrypt(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.context_processor
    def inject_global_data():
        if current_user.is_authenticated:
            cart_count = Cart.query.filter_by(user_id=current_user.id).count()
            wishlist_product_ids = {item.product_id for item in current_user.wishlist_items}
        else:
            cart_count = len(session.get('cart', {}))
            wishlist_product_ids = set()
        return dict(
            search_form=SearchForm(),
            cart_count=cart_count,
            wishlist_product_ids=wishlist_product_ids
        )

    # --- MAIN ROUTES ---
    @app.route('/')
    @app.route('/home')
    def home():
        featured_products = Product.query.order_by(Product.popularity.desc()).limit(8).all()
        return render_template('home.html', title='Home', featured_products=featured_products)

    @app.route('/catalog')
    def catalog():
        page = request.args.get('page', 1, type=int)
        query = Product.query
        category = request.args.get('category')
        if category and category != 'all':
            query = query.filter(Product.category == category)
        sort_by = request.args.get('sort_by', 'newest')
        if sort_by == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Product.price.desc())
        elif sort_by == 'popularity':
            query = query.order_by(Product.popularity.desc())
        else:
            query = query.order_by(Product.created_at.desc())
        products = query.paginate(page=page, per_page=9)
        return render_template('catalog.html', title='Catalog', products=products, category=category, sort_by=sort_by)

    @app.route('/product/<int:product_id>', methods=['GET', 'POST'])
    def product_detail(product_id):
        product = db.session.get(Product, product_id)
        if not product:
            return redirect(url_for('catalog'))
        form = ReviewForm()
        if form.validate_on_submit() and current_user.is_authenticated:
            existing_review = Review.query.filter_by(user_id=current_user.id, product_id=product.id).first()
            if existing_review:
                flash('You have already reviewed this product.', 'info')
                return redirect(url_for('product_detail', product_id=product.id))
            new_review = Review(rating=int(form.rating.data), comment=form.comment.data, author=current_user, product=product)
            db.session.add(new_review)
            db.session.commit()
            flash('Thank you for your review!', 'success')
            return redirect(url_for('product_detail', product_id=product.id))
        reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
        return render_template('product_detail.html', title=product.name, product=product, form=form, reviews=reviews)

    @app.route('/search')
    def search():
        search_query = request.args.get('search_query', '')
        if not search_query:
            return redirect(url_for('catalog'))
        page = request.args.get('page', 1, type=int)
        results = Product.query.filter(or_(Product.name.ilike(f'%{search_query}%'), Product.description.ilike(f'%{search_query}%'))).paginate(page=page, per_page=9)
        flash(f'Showing results for "{search_query}"', 'info')
        return render_template('catalog.html', title='Search Results', products=results)

    @app.route('/live_search')
    def live_search():
        query = request.args.get('query', '')
        if len(query) < 2: 
            return jsonify([])
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).limit(5).all()
        results = []
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'price': f"{product.price:.2f}",
                'url': url_for('product_detail', product_id=product.id),
                'image_url': product.image_url
            })
        return jsonify(results)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        form = ContactForm()
        if form.validate_on_submit():
            new_message = Contact(name=form.name.data, email=form.email.data, subject=form.subject.data, message=form.message.data)
            db.session.add(new_message)
            db.session.commit()
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        return render_template('contact.html', title='Contact Us', form=form)

    # --- AUTHENTICATION & PROFILE ROUTES ---
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                flash('Login Successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password.', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            login_user(user)
            return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))
        
    @app.route('/profile')
    @login_required
    def profile():
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return render_template('profile.html', title='My Profile', orders=orders)

    @app.route('/profile/edit', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = UpdateAccountForm()
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('edit_profile'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        return render_template('edit_profile.html', title='Edit Profile', form=form)

    @app.route('/profile/change_password', methods=['GET', 'POST'])
    @login_required
    def change_password():
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash('Your password has been changed successfully!', 'success')
                return redirect(url_for('change_password'))
            else:
                flash('Incorrect current password.', 'danger')
        return render_template('change_password.html', title='Change Password', form=form)

    # --- WISHLIST ROUTES ---
    @app.route('/profile/wishlist')
    @login_required
    def wishlist():
        return render_template('wishlist.html', title='My Wishlist')

    @app.route('/toggle_wishlist/<int:product_id>', methods=['POST'])
    @login_required
    def toggle_wishlist(product_id):
        item = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'status': 'removed', 'message': 'Removed from your wishlist!'})
        else:
            new_item = Wishlist(user_id=current_user.id, product_id=product_id)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({'status': 'added', 'message': 'Added to your wishlist!'})

    @app.route('/cart')
    def cart():
        cart_items = []
        total_price = 0
        if current_user.is_authenticated:
            user_cart_items = Cart.query.filter_by(user_id=current_user.id).all()
            for item in user_cart_items:
                cart_items.append({'product': item.product_details, 'quantity': item.quantity, 'item_id': item.id})
                total_price += item.product_details.price * item.quantity
        else:
            guest_cart = session.get('cart', {})
            for product_id, quantity in guest_cart.items():
                product = db.session.get(Product, int(product_id))
                if product:
                    cart_items.append({'product': product, 'quantity': quantity, 'item_id': product_id})
                    total_price += product.price * quantity
        return render_template('cart.html', title='Shopping Cart', cart_items=cart_items, total_price=total_price)

    @app.route('/add_to_cart/<int:product_id>', methods=['POST'])
    def add_to_cart(product_id):
        product = db.session.get(Product, product_id)
        if not product: return jsonify({'success': False, 'message': 'Product not found'}), 404
        quantity = int(request.form.get('quantity', 1))
        if product.stock < quantity:
            return jsonify({'success': False, 'message': 'Not enough stock!'})
        if current_user.is_authenticated:
            cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = Cart(user_id=current_user.id, product_id=product.id, quantity=quantity)
                db.session.add(cart_item)
            db.session.commit()
            cart_count = Cart.query.filter_by(user_id=current_user.id).count()
        else:
            cart = session.get('cart', {})
            cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
            session['cart'] = cart
            cart_count = len(cart)
        return jsonify({'success': True, 'message': f'{product.name} added to cart!', 'cart_count': cart_count})

    @app.route('/update_cart/<item_id>', methods=['POST'])
    def update_cart(item_id):
        new_quantity = int(request.form.get('quantity'))
        if new_quantity <= 0:
            return redirect(url_for('remove_from_cart', item_id=item_id))
        if current_user.is_authenticated:
            item = db.session.get(Cart, int(item_id))
            if not item or item.user_id != current_user.id:
                return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            item.quantity = new_quantity
            db.session.commit()
        else:
            cart = session.get('cart', {})
            if str(item_id) in cart:
                cart[str(item_id)] = new_quantity
                session['cart'] = cart
        return redirect(url_for('cart'))

    @app.route('/remove_from_cart/<item_id>')
    def remove_from_cart(item_id):
        if current_user.is_authenticated:
            item = db.session.get(Cart, int(item_id))
            if not item or item.user_id != current_user.id:
                return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            db.session.delete(item)
            db.session.commit()
        else:
            cart = session.get('cart', {})
            if str(item_id) in cart:
                del cart[str(item_id)]
                session['cart'] = cart
        flash('Item removed from cart.', 'success')
        return redirect(url_for('cart'))

    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        form = CheckoutForm()
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        if not cart_items:
            flash('Your cart is empty.', 'info')
            return redirect(url_for('catalog'))
        total_price = sum(item.product_details.price * item.quantity for item in cart_items)
        if form.validate_on_submit():
            order = Order(user_id=current_user.id, total_amount=total_price, shipping_address=f"{form.address.data}, {form.city.data}, {form.zipcode.data}, {form.country.data}")
            db.session.add(order)
            db.session.commit()
            for item in cart_items:
                order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.product_details.price)
                db.session.add(order_item)
                product = db.session.get(Product, item.product_id)
                product.stock -= item.quantity
                product.popularity += item.quantity
            Cart.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
            flash('Your order has been placed successfully!', 'success')
            return redirect(url_for('order_confirmation', order_id=order.id))
        return render_template('checkout.html', title='Checkout', form=form, cart_items=cart_items, total_price=total_price)

    @app.route('/order_confirmation/<int:order_id>')
    @login_required
    def order_confirmation(order_id):
        order = db.session.get(Order, order_id)
        if not order or order.user_id != current_user.id:
            return redirect(url_for('home'))
        return render_template('order_confirmation.html', title='Order Confirmation', order=order)

    # --- Admin Routes ---
    @app.route('/admin')
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        if not current_user.is_admin:
            flash('You do not have access to this page.', 'danger')
            return redirect(url_for('home'))
        total_sales = db.session.query(func.sum(Order.total_amount)).scalar() or 0
        total_orders = Order.query.count()
        total_products = Product.query.count()
        total_customers = User.query.filter_by(is_admin=False).count()
        sales_by_day = db.session.query(func.date(Order.created_at), func.sum(Order.total_amount)).group_by(func.date(Order.created_at)).order_by(func.date(Order.created_at).desc()).limit(7).all()
        sales_by_day.reverse()
        chart_labels = [d.strftime('%Y-%m-%d') if isinstance(d, date) else d for d, _ in sales_by_day]
        chart_data = [float(s) for _, s in sales_by_day]
        return render_template('admin/dashboard.html', title='Admin Dashboard', total_sales=total_sales, total_orders=total_orders, total_products=total_products, total_customers=total_customers, chart_labels=chart_labels, chart_data=chart_data)

    @app.route('/admin/products')
    @login_required
    def admin_products():
        if not current_user.is_admin:
            return redirect(url_for('home'))
        products = Product.query.all()
        return render_template('admin/products.html', title='Manage Products', products=products)

    @app.route('/admin/product/add', methods=['GET', 'POST'])
    @login_required
    def add_product():
        if not current_user.is_admin:
            return redirect(url_for('home'))
        form = ProductForm()
        if form.validate_on_submit():
            new_product = Product(name=form.name.data, description=form.description.data, price=float(form.price.data), category=form.category.data, stock=form.stock.data, image_url=form.image_url.data)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin/product_form.html', title='Add Product', form=form)

    @app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
    @login_required
    def edit_product(product_id):
        if not current_user.is_admin:
            return redirect(url_for('home'))
        product = db.session.get(Product, product_id)
        if not product:
            return redirect(url_for('admin_products'))
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.price = float(form.price.data)
            product.category = form.category.data
            product.stock = form.stock.data
            product.image_url = form.image_url.data
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin/product_form.html', title='Edit Product', form=form, product=product)

    @app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
    @login_required
    def delete_product(product_id):
        if not current_user.is_admin:
            return redirect(url_for('home'))
        product = db.session.get(Product, product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            flash('Product deleted successfully!', 'success')
        return redirect(url_for('admin_products'))
        
    @app.route('/admin/orders')
    @login_required
    def admin_orders():
        if not current_user.is_admin:
            return redirect(url_for('home'))
        page = request.args.get('page', 1, type=int)
        orders = Order.query.order_by(Order.created_at.desc()).paginate(page=page, per_page=15)
        return render_template('admin/orders.html', title='Manage Orders', orders=orders)

    @app.route('/admin/order/update_status/<int:order_id>', methods=['POST'])
    @login_required
    def update_order_status(order_id):
        if not current_user.is_admin:
            return redirect(url_for('home'))
        order = db.session.get(Order, order_id)
        if order:
            new_status = request.form.get('status')
            if new_status in ['Pending', 'Shipped', 'Delivered', 'Canceled']:
                order.status = new_status
                db.session.commit()
                flash(f'Order #{order.id} status has been updated to {new_status}.', 'success')
            else:
                flash('Invalid status.', 'danger')
        return redirect(url_for('admin_orders'))

    @app.route('/admin/customers')
    @login_required
    def admin_customers():
        if not current_user.is_admin:
            return redirect(url_for('home'))
        page = request.args.get('page', 1, type=int)
        customers = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).paginate(page=page, per_page=15)
        return render_template('admin/customers.html', title='Manage Customers', customers=customers)

    @app.route('/admin/customer/<int:customer_id>')
    @login_required
    def admin_customer_details(customer_id):
        if not current_user.is_admin:
            return redirect(url_for('home'))
        customer = db.session.get(User, customer_id)
        if not customer or customer.is_admin:
            flash('Customer not found.', 'danger')
            return redirect(url_for('admin_customers'))
        orders = Order.query.filter_by(user_id=customer.id).order_by(Order.created_at.desc()).all()
        return render_template('admin/customer_details.html', title=f'Details for {customer.username}', customer=customer, orders=orders)

    @app.route('/admin/reports')
    @login_required
    def admin_reports():
        if not current_user.is_admin:
            return redirect(url_for('home'))
        sales_by_category = db.session.query(Product.category, func.sum(OrderItem.price * OrderItem.quantity)).join(OrderItem, Product.id == OrderItem.product_id).group_by(Product.category).all()
        category_labels = [item[0] for item in sales_by_category]
        category_data = [float(item[1]) for item in sales_by_category]
        best_selling_products = db.session.query(Product.name, func.sum(OrderItem.quantity)).join(OrderItem, Product.id == OrderItem.product_id).group_by(Product.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()
        return render_template('admin/reports.html', title='Sales Reports', category_labels=category_labels, category_data=category_data, best_selling_products=best_selling_products)

    # --- ERROR HANDLERS ---
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

# --- RUN APP ---
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        
        if Product.query.count() == 0:
            print("Database is empty. Seeding initial data with correct image URLs...")
            
            # Membersihkan data lama
            Wishlist.query.delete()
            Review.query.delete()
            OrderItem.query.delete()
            Order.query.delete()
            Cart.query.delete()
            Product.query.delete()
            User.query.filter(User.is_admin == False).delete()
            db.session.commit()
            
            if User.query.filter_by(is_admin=True).first() is None:
                admin_user = User(username='admin', email='admin@atherz.com', is_admin=True)
                admin_user.set_password('admin123')
                db.session.add(admin_user)
            
            # ===== DATA GAMBAR FINAL YANG BENAR =====
            products_data = [
                {'name': 'Modern Cotton Hoodie', 'description': 'A comfortable and stylish hoodie made from 100% premium cotton.', 'price': 75.00, 'category': 'Baju', 'stock': 50, 'image_url': 'https://images.unsplash.com/photo-1556157382-97eda2d62296?q=80&w=870&auto=format&fit=crop'},
                {'name': 'Classic White Sneakers', 'description': 'Versatile and timeless white sneakers that match any outfit.', 'price': 120.00, 'category': 'Sepatu', 'stock': 30, 'image_url': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?q=80&w=774&auto=format&fit=crop'},
                {'name': 'Genuine Leather Belt', 'description': 'A fine, durable genuine leather belt to complete your look.', 'price': 45.00, 'category': 'Aksesoris', 'stock': 100, 'image_url': 'https://images.unsplash.com/photo-1605596330283-AC9de58509e5?q=80&w=870&auto=format&fit=crop'},
                {'name': 'Vintage Graphic T-Shirt', 'description': '100% soft cotton t-shirt with a unique, retro-inspired design.', 'price': 30.00, 'category': 'Baju', 'stock': 80, 'image_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?q=80&w=774&auto=format&fit=crop'},
                {'name': 'Pro-Series Running Shoes', 'description': 'Lightweight shoes, engineered for performance and comfort.', 'price': 95.00, 'category': 'Sepatu', 'stock': 40, 'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ab?q=80&w=870&auto=format&fit=crop'},
                {'name': 'Minimalist Silver Watch', 'description': 'An elegant and minimalist silver watch for any occasion.', 'price': 250.00, 'category': 'Aksesoris', 'stock': 20, 'image_url': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?q=80&w=774&auto=format&fit=crop'},
                {'name': 'Slim-Fit Denim Jacket', 'description': 'A timeless slim-fit denim jacket for a cool, layered look.', 'price': 110.00, 'category': 'Baju', 'stock': 35, 'image_url': 'https://images.unsplash.com/photo-1543076447-215ad9ba6923?q=80&w=774&auto=format&fit=crop'},
                {'name': 'Leather Ankle Boots', 'description': 'Stylish and durable leather ankle boots for your collection.', 'price': 180.00, 'category': 'Sepatu', 'stock': 25, 'image_url': 'https://images.unsplash.com/photo-1608256247732-0a14223d5345?q=80&w=774&auto=format&fit=crop'},
            ]
            for p_data in products_data:
                product = Product(**p_data)
                db.session.add(product)
            
            db.session.commit()
            print("Data seeding completed successfully.")

    app.run(debug=True)
