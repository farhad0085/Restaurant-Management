from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, expose, AdminIndexView
from app import app, db, bcrypt
from app.models import User, MenuItem, MenuOrder, Category, Settings
from flask_login import current_user, login_user
from flask import redirect, url_for, request

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        return super(MyAdminIndexView, self).index()


admin = Admin(app, name="Admin Panel",
			template_mode='bootstrap3',
			index_view=MyAdminIndexView())

class CustomModelView(ModelView):

	def __init__(self, model, *args, **kwargs):
		self.model = model
		super(CustomModelView, self).__init__(model, *args, **kwargs)

	def is_accessible(self):
		return current_user.is_authenticated

	def _handle_view(self, name):
		print(name)
		if not self.is_accessible():
			return redirect(url_for('main.login'))

	def on_model_change(self, form, model, is_created):
		if self.model == User:
			model.password = bcrypt.generate_password_hash(model.password)
		else:
			return None

	column_labels = {
		"weight": "Weight (gm)",
		"quantity": "Quantity (pieces)",
		"is_complete": "Completed",
		"is_ready": "Ready",
		"wait_time": "Time Remaining"
	}

	form_widget_args = {
		'password': {
			'type': 'password'
		}
	}

	column_exclude_list = ('password', )


admin.add_view(CustomModelView(User, db.session))
admin.add_view(CustomModelView(MenuItem, db.session, "Items"))
admin.add_view(CustomModelView(MenuOrder, db.session, "Orders"))
admin.add_view(CustomModelView(Category, db.session, "Categories"))
admin.add_view(CustomModelView(Settings, db.session))
