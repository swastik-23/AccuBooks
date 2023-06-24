from flask.views import MethodView
from flask_login import login_required, current_user
from flask import request, render_template, redirect, url_for
from ..database import get_db
from .. import models
from .. import schemas



class SalesView(MethodView):
    decorators = [login_required]
    def get(self):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        sales = db.session.query(models.Sales).filter(models.Sales.user_id==user.id).order_by(models.Sales.date.desc(), models.Sales.id.desc()).all()
        products = db.session.query(models.Product).filter(models.Product.user_id==user.id).order_by(models.Product.name).all()
        return render_template('sales.html',  sales=sales, products=products)

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
            sale = schemas.SalesCreate(**form_data)
        except schemas.ValidationError:
            return redirect(url_for('sales'))

        new_product = db.session.query(models.Product).filter(models.Product.id==sale.product_id, models.Product.user_id==user.id).first()

        if not new_product or sale.quantity>new_product.quantity:
            return redirect(url_for('sales'))

            
        new_sale = models.Sales(
            product_id = sale.product_id,
            quantity = sale.quantity,
            date = sale.date,
            price = sale.price,
            user_id=user.id
        )
        db.session.add(new_sale)
        new_product.quantity-=sale.quantity
        db.session.commit()
        return redirect(url_for('sales'))

    def update(self, form_data):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        try:
            sales_update = schemas.SalesUpdate(**form_data)
        except schemas.ValidationError:
            return redirect(url_for('sales'))
        sale = db.session.query(models.Sales).filter(models.Sales.user_id==user.id, models.Sales.id==sales_update.sales_id).first()
        if sale is None:
            return redirect(url_for('sales'))
        sale.product_id = sales_update.product_id
        sale.quantity = sales_update.quantity
        sale.date = sales_update.date
        sale.price = sales_update.price
        db.session.commit()
        return redirect(url_for('sales'))
        
    def delete(self, form_data):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        sales_id = form_data.get('sales_id')
        sale = db.session.query(models.Sales).filter(models.Sales.user_id==user.id, models.Sales.id==sales_id).first()
        if sale is None:
            return redirect(url_for('sales'))
        db.session.delete(sale)
        db.session.commit()
        return redirect(url_for('sales'))