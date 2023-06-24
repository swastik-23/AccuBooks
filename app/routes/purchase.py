from flask.views import MethodView
from flask_login import login_required, current_user
from flask import request, render_template, redirect, url_for
from ..database import get_db
from .. import models
from .. import schemas



class PurchaseView(MethodView):
    decorators = [login_required]
    def get(self):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        purchases = db.session.query(models.Purchase).filter(models.Purchase.user_id==user.id).order_by(models.Purchase.date.desc(), models.Purchase.id.desc()).all()
        products = db.session.query(models.Product).filter(models.Product.user_id==user.id).order_by(models.Product.name).all()
        return render_template('purchase.html',  purchases=purchases, products=products)

    def post(self):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        form_data = request.form.to_dict()
        action = form_data.get('action')
        if action == 'update':
            return(self.update(form_data))
        if action == 'delete':
            return(self.delete(form_data))
        try:
            purchase = schemas.PurchaseCreate(**form_data)
        except schemas.ValidationError:
            return redirect(url_for('purchase'))

        new_purchase = models.Purchase(
            product_id = purchase.product_id,
            quantity = purchase.quantity,
            date = purchase.date,
            price = purchase.price,
            user_id=user.id
        )
        db.session.add(new_purchase)
        new_product = db.session.query(models.Product).filter(models.Product.id==purchase.product_id, models.Product.user_id==user.id ).first()
        if new_product:
            new_product.quantity+=purchase.quantity
        db.session.commit()
        return redirect(url_for('purchase'))

    def update(self, form_data):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        try:
            purchase_update = schemas.PurchaseUpdate(**form_data)
        except schemas.ValidationError:
            return redirect(url_for('purchase'))

        purchase = db.session.query(models.Purchase).filter(models.Purchase.id==purchase_update.purchase_id, models.Purchase.user_id==user.id).first()
        if purchase is None:
            return redirect(url_for('purchase'))

        purchase.product_id = purchase_update.product_id
        purchase.quantity = purchase_update.quantity
        purchase.date = purchase_update.date
        purchase.price = purchase_update.price
        db.session.commit()
        return redirect(url_for('purchase'))
        
    def delete(self, form_data):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        purchase_id = form_data.get('purchase_id')
        purchase = db.session.query(models.Purchase).filter(models.Purchase.id==purchase_id, models.Purchase.user_id==user.id).first()
        if purchase is None:
            return redirect(url_for('purchase'))
        db.session.delete(purchase)
        db.session.commit()
        return redirect(url_for('purchase'))