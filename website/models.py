from flask import Flask, jsonify
import sqlite3
# User
def create_table_users():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print('Tao db thanh cong')
def check_exist_username(username):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        users = cursor.fetchall()
        return bool(users)  # True if users is not empty, False otherwise
    finally:
        conn.close()
    
def add_users(full_name, email, username, password):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    if not check_exist_username(username):
        cursor.execute('''Insert into users (full_name, email, username, password) values(?,?,?,?)''',(full_name, email, username, password) )
        print('Add user successfully')
    else:
        print('User has existed')
    conn.commit()
    conn.close()
def check_users(username, password):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from users where username=? and password =?',(username,password))
    user = cursor.fetchone()
    conn.close()
    return user

def delete_user_by_id(id):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Delete from users where id =?', (id,))
    conn.commit()
    conn.close()
def get_all_users():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from users')
    users = cursor.fetchall()
    users_list=[]
    for user in users:
        user_dict ={}
        user_dict['id'] = user[0]
        user_dict['full_name'] = user[1]
        user_dict['email'] = user[2]
        user_dict['password'] = user[4]
        user_dict['username'] = user[3]
        users_list.append(user_dict)
    return users_list
def get_user_by_id(id):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from users where id =?',(id,))
    user = cursor.fetchone()
    user_dict ={}
    user_dict['id'] = user[0]
    user_dict['full_name'] = user[1]
    user_dict['email'] = user[2]
    user_dict['password'] = user[4]
    user_dict['username'] = user[3]
    return user_dict
def update_user(id,full_name, email,username,password):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET full_name =?, email =?, username =?,password =?  WHERE id = ?', (full_name, email,username,password, id))
    conn.commit()
    conn.close()
# Products

def create_table_products():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_code TEXT PRIMARY KEY,
            category TEXT,
            name TEXT,
            price REAL,
            image_path TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print('Tao db thanh cong')
def check_exist_product(product_code):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM products WHERE product_code = ?', (product_code,))
        products = cursor.fetchall()
        return bool(products)  # True if products is not empty, False otherwise
    finally:
        conn.close()

def add_product(product_code, category, name, price, image_path, description):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    try:
        if not check_exist_product(product_code):
            cursor.execute('''
                INSERT INTO products (product_code, category, name, price, image_path, description)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_code, category, name, price, image_path, description))
            print('Add product successfully')
        else:
            print('Product has existed')
        conn.commit()
    finally:
        conn.close()
# add_product('CH04','CH','Chậu terrarrium',100,'sanphamchau4.jpg','Chậu terrarrium cấy xương rồng, sen đá, cây mini')
def search_product(search_text):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from products where name like ?',('%'+search_text+'%',))
    products = cursor.fetchall()
    conn.close()
    products_search_list = []
    for product in products:
        product_dict={}
        product_dict['product_code'] = product[0]
        product_dict['category'] = product[1]
        product_dict['name'] = product[2]
        product_dict['price'] = product[3]
        product_dict['image_path'] = product[4]
        product_dict['description'] = product[5]
        products_search_list.append(product_dict)
    return products_search_list
def get_all_products():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('Select * from products')
    products = cursor.fetchall()
    conn.close()
    products_search_list = []
    for product in products:
        product_dict={}
        product_dict['product_code'] = product[0]
        product_dict['category'] = product[1]
        product_dict['name'] = product[2]
        product_dict['price'] = product[3]
        product_dict['image_path'] = product[4]
        product_dict['description'] = product[5]
        products_search_list.append(product_dict)
    return products_search_list
def create_table_order():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()

    # Tạo bảng orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id INTEGER REFERENCES users(id),
            user_address TEXT NOT NULL,
            order_day TEXT NOT NULL,
            total_price REAL NOT NULL
        )
    ''')

    # Tạo bảng order_details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_details (
            order_id INTEGER REFERENCES orders(order_id),
            product_code TEXT REFERENCES products(product_code),
            quantity INTEGER NOT NULL,
            price_to_pay REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
create_table_order()
def drop_table_orders():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS orders')
    conn.commit()
    conn.close()
def drop_table_order_details():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS order_details')
    conn.commit()
    conn.close()
# Gọi hàm để xóa bảng khi cần
# drop_table_orders()
# drop_table_order_details()
def insert_orders(id, user_address, order_day, total_price):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (id, user_address, order_day, total_price)
        VALUES (?, ?, ?, ?)
    ''', (id, user_address, order_day, total_price))
    conn.commit()
    conn.close()
def insert_order_details(order_id, product_code, quantity, price_to_pay):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO order_details (order_id, product_code, quantity, price_to_pay)
        VALUES (?, ?, ?, ?)
    ''', (order_id, product_code, quantity, price_to_pay))
    conn.commit()
    conn.close()
def get_last_order_id():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(order_id) FROM orders')
    last_order_id = cursor.fetchone()[0]
    conn.close()
    return last_order_id
def get_all_orders():
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from orders')
    orders = cursor.fetchall()
    conn.close()
    return orders
def get_order_details_by_order_id(order_id):
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from order_details where order_id = ?',(order_id,))
    products_order = cursor.fetchall()
    products_order_list = []
    for product in products_order:
        product_dict ={}
        product_dict['product_code'] =  product[1]
        product_dict['quantity'] = product[2]
        product_dict['price_to_pay'] = product[3]
        products_order_list.append(product_dict)
    return products_order_list