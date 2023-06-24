from flask.views import MethodView
from .. import schemas
from ..schemas import ValidationError
from flask import request, render_template, redirect, url_for
from ..database import get_db
from .. import models
from app import bcrypt

class SignupView(MethodView):
    
    def get(self):
        return render_template('signup.html')
    
    def post(self):
        form_data = request.form.to_dict()
        user_info = None
        try:
            user_info = schemas.User(**form_data)
        except schemas.ValidationError:
            return ({"error": "Invalid information"}), 400
        db = get_db()
        user = db.session.query(models.User).filter(models.User.username == user_info.username).first()

        if user:
            return ({"error": "User already exists"}), 400
        new_user = models.User(
                        username=user_info.username,
                        email=user_info.email,
                        password=bcrypt.generate_password_hash(user_info.password).decode('utf-8'),
                    )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))