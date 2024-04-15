from flask import Blueprint, render_template, request, redirect, flash, jsonify, url_for, session
from .models import add_users, check_exist_username, delete_user_by_id, get_all_users, get_user_by_id, update_user,get_all_products, get_all_orders, get_order_details_by_order_id
import sqlite3
web_api = Blueprint('web_api',__name__)
@web_api.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users_list = get_all_users()
        return jsonify(users_list), 200
    elif request.method == 'POST':
        user_data = request.json
        if user_data and 'username' in user_data and 'email' in user_data and 'password' in user_data:
            username = user_data['username']
            email = user_data['email']
            password = user_data['password']
            full_name = user_data.get('full_name', '') # Tránh lỗi nếu 'full_name' không tồn tại trong dữ liệu
            if check_exist_username(username):
                return jsonify({"message": "Người dùng đã tồn tại"}), 400
            else:
                add_users(full_name, email, username, password)
                return jsonify({"message": "Thêm người dùng thành công"}), 201
        else:
            return jsonify({'error': 'Dữ liệu người dùng không hợp lệ hoặc thiếu thông tin!'}), 400
            
@web_api.route('/users/<int:id>', methods= ['GET', 'DELETE', 'PUT'])
def user(id):
    if request.method == "GET":
        user = get_user_by_id(id)
        if user:
            return jsonify(user),200
        else:
            return jsonify({'error': 'Khong tim thay nguoi dung'}), 404
    if request.method == "DELETE":
        user = get_user_by_id(id)
        if user:
            delete_user_by_id(id)
            return jsonify({'message': 'Xoa thanh cong'}), 200
        else:
            return jsonify({'error': 'Khong tim thay nguoi dung'}), 404
    if request.method == 'PUT':
        user = get_user_by_id(id)
        if user:
            new_data = request.json
            # Kiểm tra xem có mật khẩu mới được cung cấp không
            if 'password' in new_data and 'full_name' in new_data and 'email' in new_data and 'username' in new_data:
                # Cập nhật mật khẩu cho người dùng
                update_user(id,new_data['full_name'], new_data['email'], new_data['username'], new_data['password'])
                return jsonify({'message': 'Cập nhật thành công'}), 200
            else:
                return jsonify({'error': 'Yêu cầu phải chứa thong tin'}), 400
        else:
            return jsonify({'error': 'Không tìm thấy người dùng'}), 404
@web_api.route('/products', methods = ['GET'])
def get_products():
    products = get_all_products()
    return jsonify(products), 200
@web_api.route('/products', methods = ['POST'])
def add_product():
    product = request.json
    if not product:
        return jsonify({"error": "No data provided"}), 404

    # Kiểm tra xem các trường cần thiết có đầy đủ không
    required_fields = ['product_code', 'category', 'name', 'price', 'image_path','description']
    for field in required_fields:
        if field not in product or not product[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400
    
    # Tiếp tục thêm sản phẩm vào cơ sở dữ liệu
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    cursor.execute('''
                INSERT INTO products (product_code, category, name, price, image_path,description)
                VALUES (?, ?, ?, ?, ?,?)
            ''', (product["product_code"], product['category'], product['name'], product['price'], product['image_path'],product['description']))   
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Product add successfully"}), 201
@web_api.route('/products', methods=['DELETE'])
def delete_product():
    product_code = request.json.get('product_code')
    conn = sqlite3.connect('tiny.db')
    cursor = conn.cursor()
    
    # Kiểm tra xem sản phẩm tồn tại không
    cursor.execute('''SELECT * FROM products WHERE product_code = ?''', (product_code,))
    product = cursor.fetchone()
    if product is None:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    # Nếu sản phẩm tồn tại, thực hiện xóa
    cursor.execute('''DELETE FROM products WHERE product_code = ?''', (product_code,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product deleted successfully"}), 200
@web_api.route('/orders',methods = ['GET'])
def get_orders():
    orders = get_all_orders()
    orders_list = []
    for order in orders:
        order_dict = {}
        order_dict['order_id'] = order[0]
        order_dict['user_id'] = order[1]
        order_dict['user_address'] = order[2]
        order_dict['product'] = get_order_details_by_order_id(order[0])
        order_dict['total_price'] = order[4]
        order_dict['order_day'] = order[3]
        orders_list.append(order_dict)
    return jsonify(orders_list), 200