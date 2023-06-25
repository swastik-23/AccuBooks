from flask.views import MethodView
from flask_login import login_required, current_user
from flask import request, render_template, redirect, url_for
from ..database import get_db
from datetime import date,datetime
from .. import models
from sqlalchemy import extract
import matplotlib.pyplot as plt
import os
import numpy as np

import matplotlib.ticker as ticker



class DashboardView(MethodView):
    decorators = [login_required]
    def get(self):
        now = datetime.now()
        month = now.month
        year = now.year

        db = get_db()
        today={"sales":0,"purchases":0,"date":date.today()}
        user = db.session.query(models.User).filter(models.User.id==current_user.id).first()
        today_purchases=(db.session.query(models.Purchase).filter(models.Purchase.user_id==user.id,models.Purchase.date==date.today()).order_by(models.Purchase.date.desc(),models.Purchase.id.desc()).all())
        today["purchases"]=sum([purchase.price * purchase.quantity for purchase in today_purchases])
        today_sales=(db.session.query(models.Sales).filter(models.Sales.user_id==user.id,models.Sales.date==date.today()).order_by(models.Sales.date.desc(),models.Sales.id.desc()).all())
        today["sales"]=sum([sale.price * sale.quantity for sale in today_sales])
        products = db.session.query(models.Product).filter(models.Product.user_id==user.id).order_by(models.Product.name).all()
        latest_purchases = db.session.query(models.Purchase).filter(models.Purchase.user_id==user.id).order_by(models.Purchase.date.desc(),models.Purchase.id.desc()).limit(10).all()
        latest_sales = db.session.query(models.Sales).filter(models.Sales.user_id==user.id).order_by(models.Sales.date.desc(), models.Sales.id.desc()).limit(10).all()

        monthly_purchases = db.session.query(models.Purchase).filter(models.Purchase.user_id==user.id, extract('month', models.Purchase.date) == month, extract('year', models.Purchase.date) == year).order_by(models.Purchase.date.desc(), models.Purchase.id.desc()).all()
        monthly_sales = db.session.query(models.Sales).filter(models.Sales.user_id==user.id, extract('month', models.Sales.date) == month, extract('year', models.Sales.date) == year).order_by(models.Sales.date.desc(), models.Sales.id.desc()).all()



        x_ticks = np.arange(1, 32, 5)
        fig, ax = plt.subplots(figsize=(10, 4))

        if monthly_purchases is not None:
            purchase_prices = [(purchase.price*purchase.quantity) for purchase in monthly_purchases]
            purchase_dates = [purchase.date.day for purchase in monthly_purchases]
            if len(purchase_dates) > 1:
                ax.plot(purchase_dates, purchase_prices, color='green', label='Monthly Purchases')
            else:
                ax.scatter(purchase_dates, purchase_prices, color='green', label='Monthly Purchases')

        if monthly_sales is not None:
            sales_dates = [sale.date.day for sale in monthly_sales]
            sales_prices = [(sale.price*sale.quantity) for sale in monthly_sales]
            if len(sales_dates) > 1:
                ax.plot(sales_dates, sales_prices, color='red', label='Monthly Sales')
            else:
                ax.scatter(sales_dates, sales_prices, color='red', label='Monthly Sales')

        def fmt(x, pos):
            return '{:.0f}'.format(x)

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(fmt))

        ax.set_xticks(x_ticks)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.set_title('Monthly Purchases and Sales')
        ax.legend()
        image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'assets', f'monthly_graph_{user.id}.png')
        plt.savefig(image_path)

        return render_template('dashboard.html', latest_purchases=latest_purchases, latest_sales=latest_sales, products=products,today=today)

    def post(self):
        pass