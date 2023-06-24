from flask.views import MethodView
from flask_login import login_required, current_user
from flask import request, render_template, redirect, url_for
from ..database import get_db
from .. import models
from .. import schemas



class ProductsView(MethodView):
    decorators = [login_required]
    def get(self):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        products = db.session.query(models.Product).filter(models.Product.user_id==user.id).order_by(models.Product.name).all()
        return render_template('products.html', products=products)

    def post(self):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        form_data = request.form.to_dict()
        action = form_data.get('action')
        if action == 'delete':
            return(self.delete(form_data))
        try:
            product = schemas.Product(**form_data)
        except schemas.ValidationError:
            return ({"error": "Invalid information"}), 400
        product_exists = db.session.query(models.Product).filter(models.Product.name==product.name,models.Product.user_id==user.id).first()
        if product_exists:
            return ({"error": "Product already exists"}), 400
            
        new_product = models.Product(
            name = product.name,
            user_id=user.id
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('products'))
    
    def delete(self, form_data):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        product_id = form_data.get('product_id')
        product = db.session.query(models.Product).filter(models.Product.id==product_id, models.Product.user_id==user.id).first()
        if product is None:
            return {"error": "Product not found"}, 404
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('products'))