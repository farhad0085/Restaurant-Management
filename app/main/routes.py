from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.main.forms import LoginForm
from app.models import User, Category, MenuItem, Settings
from app import bcrypt, db

main = Blueprint('main', __name__)

settings = Settings.query.first()

@main.route('/')
def index():
	categories = Category.query.all()
	foods = MenuItem.query.filter_by(available=1).all()
	food_ids = []

	for food in foods:
		food_ids.append(food.id)

	return render_template("index.html",
							foods=foods,
							categories=categories,
							settings=settings,
							food_ids=food_ids)

@main.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.index'))
		else:
			flash("Login Failed! Please check your Email and Password", 'danger')
	return render_template("login.html", title="User Login", form=form)

@main.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))