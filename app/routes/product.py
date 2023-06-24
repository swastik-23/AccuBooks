from flask.views import MethodView
from flask_login import login_required, current_user
from flask import render_template
from ..database import get_db
from .. import models



class ProductView(MethodView):
    decorators = [login_required]
    def get(self, product_id):
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        product = db.session.query(models.Product).filter(models.Product.id == product_id, models.Product.user_id==user.id).first()
        if not product:
                    return ({"error": "Product Not Found"}), 404
        purchases = db.session.query(models.Purchase).filter(models.Purchase.product_id == product.id, models.Purchase.user_id==user.id).order_by(models.Purchase.date.desc()).all()
        sales = db.session.query(models.Sales).filter(models.Sales.product_id == product.id, models.Sales.user_id==user.id).order_by(models.Sales.date.desc()).all()
        return render_template('product.html', product=product, purchases=purchases, sales= sales)

    def post(self):
        pass