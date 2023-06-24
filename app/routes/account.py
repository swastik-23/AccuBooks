from flask.views import MethodView
from flask_login import login_required, current_user
from flask import session, render_template
from ..database import get_db
from .. import models
import datetime
from sqlalchemy import extract



class AccountView(MethodView):
    decorators = [login_required]
    def get(self, month=None, year=None):
        if not month or not year:
            now = datetime.datetime.now()
            month = now.month
            year = now.year
        month=int(month)
        year=int(year)
        db = get_db()
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        monthly_purchases = db.session.query(models.Purchase).filter(models.Purchase.user_id==user.id, extract('month', models.Purchase.date) == month, extract('year', models.Purchase.date) == year).order_by(models.Purchase.date.desc(), models.Purchase.id.desc()).all()
        monthly_sales = db.session.query(models.Sales).filter(models.Sales.user_id==user.id, extract('month', models.Sales.date) == month, extract('year', models.Sales.date) == year).order_by(models.Sales.date.desc(), models.Sales.id.desc()).all()
        total_purchase_cost = sum([purchase.price * purchase.quantity for purchase in monthly_purchases])
        total_sales_income = sum([sale.price * sale.quantity for sale in monthly_sales])
        products = db.session.query(models.Product).filter(models.Product.user_id==user.id).order_by(models.Product.name).all()
        session['month'] = month 
        session['year'] = year
        return render_template('account.html', monthly_purchases=monthly_purchases, monthly_sales=monthly_sales, expenditure= total_purchase_cost, income = total_sales_income, products=products)

    def post(self):
        pass