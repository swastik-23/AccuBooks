from flask import request, render_template, redirect, url_for
from flask.views import MethodView
from .. import schemas
from ..database import get_db, bcrypt
from .. import models
from flask_bcrypt import check_password_hash
from flask_login import login_user,login_required, current_user

class ProfileView(MethodView):
    decorators = [login_required]

    def get(self):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        return render_template('changepassword.html', user=user)

    def post(self):
        form_data = request.form.to_dict()
        user_credentials = None
        try:
            user_credentials = schemas.UserChangePassword(**form_data)
        except schemas.ValidationError:
            return ({"error": "Invalid information"}), 400

        db = get_db()
        user = db.session.query(models.User).filter(models.User.username == user_credentials.username).first()
        # implement hash checking
        if user is None or not check_password_hash(user.password,user_credentials.password):
            return ({"error": "Invalid credentials"}), 401

        user.password = bcrypt.generate_password_hash(user_credentials.new_password).decode('utf-8')
        db.session.commit()
        return redirect(url_for('logout'))
