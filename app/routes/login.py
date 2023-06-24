from flask import request, render_template, redirect, url_for
from flask.views import MethodView
from .. import schemas
from ..database import get_db, bcrypt
from .. import models
from flask_bcrypt import check_password_hash
from flask_login import login_user

class LoginView(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        form_data = request.form.to_dict()
        user_credentials = None
        try:
            user_credentials = schemas.UserLogin(**form_data)
        except schemas.ValidationError:
            return redirect(url_for('login'))

        db = get_db()
        user = db.session.query(models.User).filter(models.User.username == user_credentials.username).first()
        # implement hash checking
        if user is None or not check_password_hash(user.password,user_credentials.password):
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))
