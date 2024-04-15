from datetime import datetime
import requests
from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for, session
from .models import add_product,check_exist_product, search_product, insert_orders, get_last_order_id, insert_order_details
import sqlite3

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('index.html')
@views.route('/about')
def about():
    return render_template('aboutus.html')
@views.route('/shop', methods=['POST','GET'])
def shop():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from products')
    products = cursor.fetchall()
    conn.close()
    products_list = []
    for product in products:
        product_dict={}
        product_dict['product_code'] = product[0]
        product_dict['category'] = product[1]
        product_dict['name'] = product[2]
        product_dict['price'] = product[3]
        product_dict['image_path'] = product[4]
        product_dict['description'] = product[5]
        products_list.append(product_dict)
    products_search_list = []
    if request.method == "POST":
        products_search_list = []
        search_text = request.form.get("search_text")
        products_search_list = search_product(search_text)
    return render_template('shop.html', products = products_list, products_search_list=products_search_list)

@views.route('/detail/<string:product_code>')
def detail(product_code):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from products where product_code =?',(product_code,))
    product = cursor.fetchone()
    conn.close()
    product_dict={}
    product_dict['product_code'] = product[0]
    product_dict['category'] = product[1]
    product_dict['name'] = product[2]
    product_dict['price'] = product[3]
    product_dict['image_path'] = product[4]
    product_dict['description'] = product[5]

    return render_template('details.html',product=product_dict)
@views.route('/add_to_cart', methods=['POST', 'GET'])
def add_to_cart():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        product_price = float(request.form.get('product_price'))
        product_code = request.form.get('product_code')
        
        # Kiểm tra xem giỏ hàng đã được khởi tạo chưa
        cart ={}
        if 'cart' in session:
            cart = session.get('cart',{})
        
        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        if product_code in cart:
            # Nếu có, cập nhật thông tin sản phẩm
            cart[product_code]['quantity'] += 1
            cart[product_code]['price_to_pay'] += product_price
        else:
            # Nếu không, thêm sản phẩm vào giỏ hàng
           cart[product_code] = {
                'product_name': product_name,
                'product_price': product_price,
                'quantity': 1,
                'price_to_pay': product_price
            }
        session['cart'] = cart
    
    return redirect(url_for('views.shop'))


@views.route('/cart')
def cart():
    # Lấy thông tin giỏ hàng từ session
    cart_items = session.get('cart', {})
    total_price = sum(item['price_to_pay'] for item in cart_items.values())
    
    # In ra giỏ hàng để kiểm tra
    print(cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)
@views.route('/delete_from_cart', methods=['POST'])
def delete_from_cart():
    if request.method == 'POST':
        product_code = request.form.get('product_code')
        cart = session.get('cart',{})
        if product_code in cart:
            del cart[product_code]
        session['cart'] = cart
    return redirect(url_for('views.cart'))
@views.route('/payment')
def payment():
    if 'users' not in session:
        flash("Login to order", category='error')
        return redirect(url_for('auth.login'))  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
    else: 
        cart_items = session.get('cart', {})
        total_price = sum(item['price_to_pay'] for item in cart_items.values())

    return render_template('payment.html',cart_items=cart_items, total_price=total_price)
@views.route('/tips')
def tips():
    return render_template("tips.html")
@views.route('/tips/care_cactus')
def care_cactus():
    return render_template("care_cactus.html")
@views.route('/tips/care_senda')
def care_senda():
    return render_template("care_senda.html")
@views.route('/submit_order', methods= ['POST'])
def submit_order():
    if request.method== 'POST':
        id = request.form.get("user_id")
        user_address = request.form.get("address")
        total_price = request.form.get('total_price')
        current_date = datetime.now()
        order_day = current_date.strftime('%d %m %Y')
        insert_orders(id,user_address,order_day,total_price)
        order_id = get_last_order_id()
        
        # Lấy thông tin sản phẩm từ form
        product_codes = request.form.getlist("product_code[]")
        quantities = request.form.getlist("quantity[]")
        prices_to_pay = request.form.getlist("price_to_pay[]")
        
        # Thêm thông tin sản phẩm vào bảng order_details cho từng sản phẩm trong giỏ hàng
        for product_code, quantity, price_to_pay in zip(product_codes, quantities, prices_to_pay):
            insert_order_details(order_id, product_code, quantity, price_to_pay)
        
        flash("Order placed successfully!")
        session.pop('cart', None)
        return redirect(url_for("views.home"))