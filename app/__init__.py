from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import settings
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login' 
    create_user_loader()
    create_router(app)
    return app

def create_user_loader():
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(int(user_id))

def create_router(app):
    from .routes import login, signup, dashboard, products, product, account, purchase, sales, profile, logout
    from flask import redirect, url_for
    
    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))
    
    app.add_url_rule('/login', view_func=login.LoginView.as_view('login'))
    app.add_url_rule('/signup', view_func=signup.SignupView.as_view('signup'))
    app.add_url_rule('/dashboard', view_func=dashboard.DashboardView.as_view('dashboard'))
    app.add_url_rule('/products', view_func=products.ProductsView.as_view('products'))
    app.add_url_rule('/product/<int:product_id>', view_func=product.ProductView.as_view('product'))
    app.add_url_rule('/account', view_func=account.AccountView.as_view('account'))
    app.add_url_rule('/purchase', view_func=purchase.PurchaseView.as_view('purchase'))
    app.add_url_rule('/sales', view_func=sales.SalesView.as_view('sales'))
    app.add_url_rule('/changepassword', view_func=profile.ProfileView.as_view('change_password'))
    app.add_url_rule('/logout', view_func=logout.LogoutView.as_view('logout'))
    # app.add_url_rule('/notification',view_func=notification.Notificationview.as_view('notification'
    # ))
    