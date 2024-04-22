from flask import Blueprint, render_template, url_for, request, session, flash, redirect
from .models import Product, Category, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)
main_bp.secret_key = 'some_secret'

@main_bp.route('/')
def getAllProduct():
    products = Product.query.order_by(Product.id).all()
    categories = Category.query.order_by(Category.id).all()
    #statusnew = Product.query.filter(Product.status == 'new')
    return render_template('index.html', products=products, categories=categories)


#getProductByCategory
@main_bp.route('/products/<int:categoryid>')
def getByCategory(categoryid):
    categories = Category.query.order_by(Category.id).all()
    products = Product.query.filter(Product.category_id == categoryid)
    return render_template('productList.html', categories=categories, products=products)
#getProductDetail
@main_bp.route('/productDetail/<int:productid>')
def getProduct(productid):
    products = Product.query.filter(Product.id == productid )
    categories = Category.query.order_by(Category.id).all()
    return render_template('productDetail.html', categories=categories,products=products)


# Referred to as "Basket" to the user
@main_bp.route('/order', methods=['POST','GET'])
def order():
    categories = Category.query.order_by(Category.id).all()
    product_id = request.values.get('product_id')

    # retrieve order if there is one
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
        # order will be None if order_id stale
    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order( firstname='', lastname='', email='', phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('failed at creating a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for product in order.products:
            totalprice = totalprice + product.price
    
    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.products:
            try:
                order.products.append(product)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your basket'
            return redirect(url_for('main.order'))
        else:
            flash('This item already in basket')
            return redirect(url_for('main.order'))
    return render_template('order.html', order = order, totalprice=totalprice,categories=categories)

# Delete specific basket items
@main_bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.products.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@main_bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.getAllProduct'))

@main_bp.route('/checkout', methods=['POST','GET'])
def checkout():
    categories = Category.query.order_by(Category.id).all()
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
       
        if form.validate_on_submit():
            order.firstname = form.firstname.data
            order.lastname = form.lastname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for product in order.products:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for ordering!')
                return redirect(url_for('main.getAllProduct'))
            except:
                return 'There was an issue completing your order'
    return render_template('checkout.html', form=form, categories=categories)

@main_bp.route('/products')
def search():
    categories = Category.query.order_by(Category.id).all()
    search = request.args.get('search')
    search = '%{}%'.format(search) 
    products = Product.query.filter(Product.name.like(search)).all()
    return render_template('productList.html', products=products,categories=categories)
