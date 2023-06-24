from flask import redirect, url_for
from flask.views import MethodView
from flask_login import logout_user

class LogoutView(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('login'))
