from flask import Flask, redirect, url_for, render_template, request, session
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
import MySQLdb.cursors
from datetime import date
from function import *
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.secret_key = "admin"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'meow_shop'
path = os.getcwd()

mysql = MySQL(app)

@app.route('/')
@app.route('/_users/index')
def index():
    msg = request.args.get('message', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    arrays_all_product = base_user_1_arrays_all_product(cursor)
    arrays_carts = base_user_1_arrays_carts(cursor)

    query_product_hot = 'SELECT product_types.product_type_id, product_type_name FROM count_sales, products, product_types WHERE count_sales.product_id=products.product_id AND products.product_type_id=product_types.product_type_id ORDER BY count_sale DESC LIMIT 3'
    cursor.execute(query_product_hot)
    arrays_product_hot = cursor.fetchall()

    list = top_3_product(cursor)

    return render_template('_users/index.html', arrays_all_product=arrays_all_product, arrays_carts=arrays_carts, arrays_product_hot=arrays_product_hot, arrays_product_hot_detail=list, msg=msg)
@app.route('/_users/login')
@app.route('/_admin/login')
def login():
    msg = request.args.get('message', '')
    return render_template('_users/login.html', msg=msg)
@app.route('/_users/register')
def register():
    msg = request.args.get('message', '')
    return render_template('_users/register.html', msg=msg)
@app.route('/_users/page_category/<product_type_id>')
def page_category(product_type_id):
    msg = request.args.get('message', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    arrays_all_product = base_user_1_arrays_all_product(cursor)
    arrays_carts = base_user_1_arrays_carts(cursor)

    prepare_query = 'product_id, product_name, product_price, product_image_1, discount'
    query_product_type_all = "SELECT " + prepare_query + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND product_types.product_type_id=" + product_type_id + ";"
    cursor.execute(query_product_type_all, ())
    arrays_product_type_all = cursor.fetchall()
    list = ()
    for x in arrays_product_type_all:
        array = {"product_id": x['product_id']
                 , "product_name": x['product_name'][0:25]
                 , "product_image_1": x['product_image_1']
                 , "product_price": round(x['product_price'],2)
                 , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)}
        list += (array,)

    return render_template('_users/page_category.html', arrays_all_product=arrays_all_product, arrays_carts=arrays_carts, arrays_product_type_all=list, msg=msg)
@app.route('/_users/product_detail/<int:product_id>')
def product_detail(product_id):
    msg = request.args.get('message', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    arrays_all_product = base_user_1_arrays_all_product(cursor)
    arrays_carts = base_user_1_arrays_carts(cursor)

    prepare_query = 'product_id, products.product_type_id, product_name, product_quantity, product_price, product_description, product_image_1, product_image_2, product_image_3, discount, product_type_name'
    query_product_detail = "SELECT " + prepare_query + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND product_id=% s;"
    cursor.execute(query_product_detail, (product_id, ))
    arrays_product_detail = cursor.fetchone()
    list = {}
    list1 = ()
    if arrays_product_detail:
        convert = convert_html_to_text(arrays_product_detail['product_description'])

        list = {"product_id": arrays_product_detail['product_id']
                 , "product_type_id": arrays_product_detail['product_type_id']
                 , "product_name": arrays_product_detail['product_name'][0:25]
                 , "product_quantity": arrays_product_detail['product_quantity']
                 , "product_description": convert[0:40]
                 , "product_description_all": convert
                 , "product_image_1": arrays_product_detail['product_image_1']
                 , "product_image_2": arrays_product_detail['product_image_2']
                 , "product_image_3": arrays_product_detail['product_image_3']
                 , "discount": arrays_product_detail['discount']
                 , "product_type_name": arrays_product_detail['product_type_name']
                 , "product_price": round(arrays_product_detail['product_price'],2)
                 , "product_price_total": round(arrays_product_detail['product_price'] - (arrays_product_detail['product_price'] * (arrays_product_detail['discount'] / 100)), 2)}

        prepare_query1 = 'product_id, product_name, product_price, product_image_1, discount'
        query_product_related = "SELECT " + prepare_query1 + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND products.product_type_id=" + str(arrays_product_detail['product_type_id']) + " AND product_id!=" + str(arrays_product_detail['product_id']) + " LIMIT 3;"
        cursor.execute(query_product_related, ())
        arrays_product_related = cursor.fetchall()
        for y in arrays_product_related:
            array1 = {"product_id": y['product_id']
                 , "product_name": y['product_name']
                 , "product_price": round(y['product_price'],2)
                 , "product_image_1": y['product_image_1']
                 , "discount": y['discount']
                 , "product_price_total": round(y['product_price'] - (y['product_price'] * (y['discount'] / 100)), 2)}
            list1 += (array1,)
        
    return render_template('_users/product_detail.html', arrays_all_product=arrays_all_product, arrays_carts=arrays_carts, arrays_product_detail=list, arrays_product_related=list1, msg=msg)
@app.route('/_users/page_product/<int:page>', methods = ['POST', 'GET'])
def page_product(page):
    page_convert = page
    msg = request.args.get('message', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    arrays_all_product = base_user_1_arrays_all_product(cursor)
    arrays_carts = base_user_1_arrays_carts(cursor)

    list = ()
    list_category = ()
    if request.method == 'POST' and 'search' in request.form and request.form['keyword'] != '':
        keyword = request.form['keyword']
        page_convert = -1
        prepare_query = 'product_id, product_name, product_price, product_image_1, discount'
        query_product_search = 'SELECT ' + prepare_query + ' FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND product_name LIKE % s;'
        cursor.execute(query_product_search, ("%" + keyword + "%",))
        arrays_product_search = cursor.fetchall()
        for x in arrays_product_search:
            array = {"product_id": x['product_id']
                 , "product_name": x['product_name'][0:25]
                 , "product_image_1": x['product_image_1']
                 , "product_price": round(x['product_price'],2)
                 , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)}
            list += (array,)
    elif request.method == 'POST' and 'search' in request.form and request.form['keyword'] == '':
        page_convert = 0
        prepare_query = 'product_id, product_name, product_price, product_image_1, discount'
        query_product_search = "SELECT " + prepare_query + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id LIMIT 9 OFFSET " + str(page * 9) + ";"
        cursor.execute(query_product_search, ())
        arrays_product_search = cursor.fetchall()
        for x in arrays_product_search:
            array = {"product_id": x['product_id']
                 , "product_name": x['product_name'][0:25]
                 , "product_image_1": x['product_image_1']
                 , "product_price": round(x['product_price'],2)
                 , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)}
            list += (array,)
    else:
        prepare_query = 'product_id, product_name, product_price, product_image_1, discount'
        query_product_search = "SELECT " + prepare_query + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id LIMIT 9 OFFSET " + str(page * 9) + ";"
        cursor.execute(query_product_search, ())
        arrays_product_search = cursor.fetchall()
        for x in arrays_product_search:
            array = {"product_id": x['product_id']
                 , "product_name": x['product_name'][0:25]
                 , "product_image_1": x['product_image_1']
                 , "product_price": round(x['product_price'],2)
                 , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)}
            list += (array,)
    list_top_3 = top_3_product(cursor)

    query_category_all = "SELECT product_type_id, product_type_name FROM product_types;"
    cursor.execute(query_category_all, ())
    arrays_category_all = cursor.fetchall()
    for x in arrays_category_all:
        array = {"product_type_id": x['product_type_id']
                 , "product_type_name": x['product_type_name']}
        list_category += (array,)
    return render_template('_users/page_product.html', page=page_convert, arrays_all_product=arrays_all_product, arrays_carts=arrays_carts, arrays_product_search=list, list_top_3=list_top_3, arrays_category_all=list_category, msg=msg)
@app.route('/_users/page_carts', methods = ['POST', 'GET'])
def page_carts():
    msg = request.args.get('message', '')
    total = 0
    order_product_all_id = 0
    order_all_quantity = 0
    list = ()
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        arrays_all_product = base_user_1_arrays_all_product(cursor)
        arrays_carts = base_user_1_arrays_carts(cursor)

        if arrays_carts == ():
            msg = 'You must purchase first!'
            return redirect(url_for('index', message = msg))

        if request.method == 'POST' and 'update_carts' in request.form:
            query_each_product_cart = "SELECT product_id FROM carts WHERE account_id=% s;"
            cursor.execute(query_each_product_cart, (session['account_id'], ))
            arrays_each_product_cart = cursor.fetchall()
            for u in arrays_each_product_cart:
                cursor.execute('UPDATE carts SET cart_quantity=% s WHERE account_id = % s AND product_id = % s;'
                           , (request.form['cart_quantity_' + str(u['product_id'])], session['account_id'], u['product_id'], ))
                mysql.connection.commit()
                msg = 'You have successfully updated!'

        list, total, order_product_all_id, order_all_quantity = get_product_cart_by_account(cursor)

        return render_template('_users/page_carts.html', arrays_all_product=arrays_all_product, arrays_carts=arrays_carts, arrays_product_cart_all=list, total=round(total, 2), msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/checkout', methods = ['POST', 'GET'])
def checkout():
    msg = request.args.get('message', '')
    total = 0
    order_product_all_id = 0
    order_all_quantity = 0
    list = ()
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        arrays_all_product = base_user_1_arrays_all_product(cursor)
        arrays_carts = base_user_1_arrays_carts(cursor)

        if arrays_carts == ():
            msg = 'You must purchase first!'
            return redirect(url_for('index', message = msg))

        customer = get_account(cursor)

        list, total, order_product_all_id, order_all_quantity = get_product_cart_by_account(cursor)

        return render_template('_users/checkout.html', arrays_all_product=arrays_all_product, arrays_carts=arrays_carts, arrays_product_cart_by_account=list, total=round(total, 2), order_product_all_id=order_product_all_id, order_all_quantity=order_all_quantity, customer=customer, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_page', methods = ['POST', 'GET'])
def account_page():
    msg = request.args.get('message', '')
    list = ()
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        customer = get_account(cursor)
        return render_template('_users/account_page.html', customer=customer, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_reset_pass')
def account_reset_pass():
    msg = request.args.get('message', '')
    if(check_login()):
        return render_template('_users/account_reset_pass.html', msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_order')
def account_order():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        orders_1 = get_all_order_by_status(cursor, 1, 'order_account')
        orders_2 = get_all_order_by_status(cursor, 2, 'order_account')
        return render_template('_users/account_order.html', orders_1=orders_1, orders_2=orders_2, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_purchase_history')
def account_purchase_history():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        order_history = get_all_order_by_status(cursor, 3, 'order_account')
        return render_template('_users/account_purchase_history.html', order_history=order_history, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/index')
@app.route('/_users/admin')
def admin():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        array1 = get_count_order(cursor)
        list_products = ()
        query_product_count = "SELECT product_name, product_quantity, count_sale FROM count_sales, products WHERE products.product_id=count_sales.product_id ORDER BY count_sale DESC LIMIT 5;"
        cursor.execute(query_product_count, ())
        arrays_product_count = cursor.fetchall()
        for x in arrays_product_count:
            array = {"product_name": x['product_name'][:30]
                    , "product_quantity": x['product_quantity']
                    , "count_sale": x['count_sale']
                    , "percentage": (x['count_sale'] / x['product_quantity']) * 100}
            list_products += (array,)

        list_order = ()
        query_order = "SELECT order_id, order_name, order_address, order_status_id FROM orders LIMIT 5;"
        cursor.execute(query_order, ())
        arrays_order = cursor.fetchall()
        for x in arrays_order:
            array = {"order_id": x['order_id']
                    , "order_name": x['order_name']
                    , "order_address": x['order_address'][:20]
                    , "order_status_id": x['order_status_id']}
            list_order += (array,)

        array_report = get_report(cursor, '', '')

        return render_template('_admin/index.html', array1=array1, list_products=list_products, list_order=list_order, array_report=array_report, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_customers')
def view_customers():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        list_customer = ()
        info_all_account = "accounts.account_id, account_name, phone, date_of_birth, block"
        query_all_account = "SELECT " + info_all_account + " FROM accounts WHERE role=0;"
        cursor.execute(query_all_account, ())
        arrays_customer = cursor.fetchall()
        for x in arrays_customer:
            array = {"account_id": x['account_id']
                    , "account_name": x['account_name']
                    , "phone": x['phone']
                    , "date_of_birth": x['date_of_birth']
                    , "block": x['block']}
            list_customer += (array,)
        
        return render_template('_admin/view_customers.html', list_customer=list_customer, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_customers/<int:account_id>')
def update_customers(account_id):
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_customer_detail = ()    
        info_account = "account_id, account_name, account_address, gender, phone, email, date_of_birth, block, avatar"
        query_account = "SELECT " + info_account + " FROM accounts WHERE account_id=% s;"
        cursor.execute(query_account, (account_id, ))
        arrays_customer = cursor.fetchone()
        if arrays_customer:
            array = {"account_id": arrays_customer['account_id']
                    , "account_name": arrays_customer['account_name']
                    , "account_address": arrays_customer['account_address']
                    , "gender": arrays_customer['gender']
                    , "phone": arrays_customer['phone']
                    , "email": arrays_customer['email']
                    , "date_of_birth": arrays_customer['date_of_birth']
                    , "block": arrays_customer['block']
                    , "avatar": arrays_customer['avatar']}
            list_customer_detail = array
        return render_template('_admin/update_customers.html', list_customer_detail=list_customer_detail, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_customers')
def add_customers():
    msg = request.args.get('message', '')
    if(check_login()):
        return render_template('_admin/add_customers.html', msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_employees')
def view_employees():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        list_employees = ()
        info_employees = "accounts.account_id, account_name, phone, date_of_birth"
        query_employees = "SELECT " + info_employees + " FROM accounts, employees WHERE accounts.account_id=employees.account_id AND role=0;"
        cursor.execute(query_employees, ())
        arrays_employees = cursor.fetchall()
        for x in arrays_employees:
            array = {"account_id": x['account_id']
                    , "account_name": x['account_name']
                    , "phone": x['phone']
                    , "date_of_birth": x['date_of_birth']}
            list_employees += (array,)
        
        return render_template('_admin/view_employees.html', list_employees=list_employees, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_employees/<int:account_id>')
def update_employees(account_id):
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_employee_detail = ()    
        info_employee = "accounts.account_id, account_name, account_address, gender, phone, email, date_of_birth, avatar, employee_position"
        query_employee = "SELECT " + info_employee + " FROM accounts, employees WHERE accounts.account_id=employees.account_id AND accounts.account_id=% s;"
        cursor.execute(query_employee, (account_id, ))
        arrays_employee = cursor.fetchone()
        if arrays_employee:
            array = {"account_id": arrays_employee['account_id']
                    , "account_name": arrays_employee['account_name']
                    , "account_address": arrays_employee['account_address']
                    , "gender": arrays_employee['gender']
                    , "phone": arrays_employee['phone']
                    , "email": arrays_employee['email']
                    , "date_of_birth": arrays_employee['date_of_birth']
                    , "avatar": arrays_employee['avatar']
                    , "employee_position": arrays_employee['employee_position']}
            list_employee_detail = array
        return render_template('_admin/update_employees.html', list_employee_detail=list_employee_detail, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_employees')
def add_employees():
    msg = request.args.get('message', '')
    if(check_login()):
        return render_template('_admin/add_employees.html', msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_suppliers')
def view_suppliers():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        list_suppliers = ()
        info_suppliers = "supplier_id, supplier_name, supplier_phone"
        query_suppliers = "SELECT " + info_suppliers + " FROM suppliers;"
        cursor.execute(query_suppliers, ())
        arrays_suppliers = cursor.fetchall()
        for x in arrays_suppliers:
            array = {"supplier_id": x['supplier_id']
                    , "supplier_name": x['supplier_name']
                    , "supplier_phone": x['supplier_phone']}
            list_suppliers += (array,)
        
        return render_template('_admin/view_suppliers.html', list_suppliers=list_suppliers, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_suppliers/<int:supplier_id>')
def update_suppliers(supplier_id):
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_suppliers_detail = ()    
        info_suppliers = "supplier_id, supplier_name, supplier_email, supplier_address, supplier_phone, supplier_avatar"
        query_suppliers = "SELECT " + info_suppliers + " FROM suppliers WHERE supplier_id=% s;"
        cursor.execute(query_suppliers, (supplier_id, ))
        arrays_suppliers = cursor.fetchone()
        if arrays_suppliers:
            array = {"supplier_id": arrays_suppliers['supplier_id']
                    , "supplier_name": arrays_suppliers['supplier_name']
                    , "supplier_email": arrays_suppliers['supplier_email']
                    , "supplier_address": arrays_suppliers['supplier_address']
                    , "supplier_phone": arrays_suppliers['supplier_phone']
                    , "supplier_avatar": arrays_suppliers['supplier_avatar']}
            list_suppliers_detail = array
        return render_template('_admin/update_suppliers.html', list_suppliers_detail=list_suppliers_detail, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_suppliers')
def add_suppliers():
    msg = request.args.get('message', '')
    if(check_login()):
        return render_template('_admin/add_suppliers.html', msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_categories')
def view_categories():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        list_categories = ()
        query_categories = "SELECT product_type_id, product_type_name, coupon_name FROM product_types, coupons WHERE product_types.coupon_id=coupons.coupon_id;"
        cursor.execute(query_categories, ())
        arrays_categories = cursor.fetchall()
        for x in arrays_categories:
            array = {"product_type_id": x['product_type_id']
                    , "product_type_name": x['product_type_name']
                    , "coupon_name": x['coupon_name']}
            list_categories += (array,)
        
        return render_template('_admin/view_categories.html', list_categories=list_categories, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_categories/<int:product_type_id>')
def update_categories(product_type_id):
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_categories_detail = ()    
        query_categories = "SELECT product_type_id, product_type_name, coupon_id FROM product_types WHERE product_type_id=% s;"
        cursor.execute(query_categories, (product_type_id, ))
        arrays_categories = cursor.fetchone()
        if arrays_categories:
            array = {"product_type_id": arrays_categories['product_type_id']
                    , "product_type_name": arrays_categories['product_type_name']
                    , "coupon_id": arrays_categories['coupon_id']}
            list_categories_detail = array
        
        list_coupon = get_list_coupon(cursor)    

        return render_template('_admin/update_categories.html', list_categories_detail=list_categories_detail, list_coupon=list_coupon, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_categories')
def add_categories():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_coupon = get_list_coupon(cursor)  
        return render_template('_admin/add_categories.html', list_coupon=list_coupon, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_coupons')
def view_coupons():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_coupons = get_list_coupon(cursor)  
        return render_template('_admin/view_coupons.html', list_coupons=list_coupons, msg=msg)
    else:
        msg = 'You must be login first!'
        return redirect(url_for('login', message = msg))
@app.route('/_admin/add_coupons')
def add_coupons():
    msg = request.args.get('message', '')
    if(check_login()):
        return render_template('_admin/add_coupons.html', msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_orders')
def view_orders():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_all_order = ()
        info_all_order = "order_id, order_name, order_address, date_invoice_order, order_status_id"
        query_all_order = "SELECT " + info_all_order + " FROM orders;"
        cursor.execute(query_all_order, ())
        arrays_all_order = cursor.fetchall()
        for x in arrays_all_order:
            array = {"order_id": x['order_id']
                    , "order_name": x['order_name']
                    , "order_address": x['order_address'][:20]
                    , "date_invoice_order": x['date_invoice_order']
                    , "order_status_id": x['order_status_id']}
            list_all_order += (array,)
        return render_template('_admin/view_orders.html', list_all_order=list_all_order, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_orders/<int:order_id>')
def update_orders(order_id):
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_order_detail = get_all_order_by_status(cursor, order_id, 'order_details_admin')
        list_status = get_list_status(cursor)    

        return render_template('_admin/update_orders.html', list_order_detail=list_order_detail, list_status=list_status, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/report_customers')
def report_customers():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        today = date.today()
        currentTime = today.strftime("%Y/%m/%d")
        total_price = 0
        total_order = 0
        table_customer = ()

        query_customer_each = "SELECT accounts.account_id, account_name, phone, COUNT(accounts.account_id) AS count, SUM(order_total) AS price FROM orders, accounts WHERE orders.account_id=accounts.account_id AND order_status_id=3 GROUP BY accounts.account_id, account_name, phone;"
        cursor.execute(query_customer_each, ())
        arrays_customer_each = cursor.fetchall()
        for x in arrays_customer_each:
            array = {"account_id": x['account_id']
                    , "account_name": x['account_name']
                    , "phone": x['phone']
                    , "count": x['count']
                    , "price": x['price']}
            total_order += x['count']
            total_price += x['price']
            table_customer += (array,)

        customer_each = {"currentTime": currentTime
                    , "total_price": total_price
                    , "total_order": total_order
                    , "table_customer": table_customer}

        return render_template('_admin/report_customers.html', customer_each=customer_each, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/report_products')
def report_products():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        today = date.today()
        currentTime = today.strftime("%Y/%m/%d")
        total_price = 0
        total_quantity = 0
        table_product = ()

        query_product_each = "SELECT product_id, product_name, product_type_name, product_quantity, product_price FROM products, product_types WHERE products.product_type_id=product_types.product_type_id;"
        cursor.execute(query_product_each, ())
        arrays_product_each = cursor.fetchall()
        for x in arrays_product_each:
            array = {"product_id": x['product_id']
                    , "product_name": x['product_name']
                    , "product_type_name": x['product_type_name']
                    , "product_quantity": x['product_quantity']
                    , "product_price": x['product_price']}
            total_quantity += x['product_quantity']
            total_price += x['product_quantity'] * x['product_price']
            table_product += (array,)

        product_each = {"currentTime": currentTime
                    , "total_price": round(total_price, 2)
                    , "total_quantity": total_quantity
                    , "table_product": table_product}

        return render_template('_admin/report_products.html', product_each=product_each, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/report_revenues', methods = ['POST', 'GET'])
def report_revenues():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        today = date.today()
        currentTime = today.strftime("%Y/%m/%d")
        count = 0
        total = 0
        if request.method == 'POST' and 'report' in request.form and request.form['start'] != '' and request.form['end'] != '':
            start = str(request.form['start'])
            end = str(request.form['end'])
        else:
            start = ''
            end = ''
        table_revenues, count, total = get_all_revenues(cursor, start, end)

        array_report = get_report(cursor, start, end)

        revenues_each = {"currentTime": currentTime
                    , "count": count
                    , "total": round(total, 2)
                    , "table_revenues": table_revenues}

        return render_template('_admin/report_revenues.html', revenues_each=revenues_each, array_report=array_report, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_products')
def view_products():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_products = ()
        info_product = "product_id, product_name, product_type_name, product_price, product_quantity"
        query_products = "SELECT " + info_product + " FROM products, product_types WHERE products.product_type_id=product_types.product_type_id;"
        cursor.execute(query_products, ())
        arrays_products = cursor.fetchall()
        for x in arrays_products:
            array = {"product_id": x['product_id']
                    , "product_name": x['product_name'][:30]
                    , "product_type_name": x['product_type_name']
                    , "product_price": x['product_price']
                    , "product_quantity": x['product_quantity']}
            list_products += (array,)
        return render_template('_admin/view_products.html', list_products=list_products, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_products/<int:product_id>')
def update_products(product_id):
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        list_product_detail = ()    
        query_product_detail = "SELECT * FROM products, product_types WHERE products.product_type_id=product_types.product_type_id AND product_id=% s;"
        cursor.execute(query_product_detail, (product_id, ))
        arrays_product_detail = cursor.fetchone()
        if arrays_product_detail:
            array = {"product_id": arrays_product_detail['product_id']
                    , "product_name": arrays_product_detail['product_name']
                    , "product_type_id": arrays_product_detail['product_type_id']
                    , "supplier_id": arrays_product_detail['supplier_id']
                    , "product_quantity": arrays_product_detail['product_quantity']
                    , "product_price": arrays_product_detail['product_price']
                    , "product_image_1": arrays_product_detail['product_image_1']
                    , "product_image_2": arrays_product_detail['product_image_2']
                    , "product_image_3": arrays_product_detail['product_image_3']
                    , "product_description": arrays_product_detail['product_description']
                    , "coupon_id": arrays_product_detail['coupon_id']}
            list_product_detail = array
        
        type_product = base_user_1_arrays_all_product(cursor)  

        suppliers = get_supplier_all(cursor)  

        return render_template('_admin/update_products.html', list_product_detail=list_product_detail, type_product=type_product, suppliers=suppliers, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_products')
def add_products():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        type_product = base_user_1_arrays_all_product(cursor)  
        suppliers = get_supplier_all(cursor)  

        return render_template('_admin/add_products.html', type_product=type_product, suppliers=suppliers, msg=msg)
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))































@app.route('/_admin/add_products_add', methods = ['POST', 'GET'])
def add_products_add():
    msg = request.args.get('message', '')
    if(check_login()):
        if request.method == 'POST' and 'add_product' in request.form:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\image_products')
            product_name = request.form['product_name']
            product_type_id = request.form['product_type_id']
            supplier_id = request.form['supplier_id']
            product_quantity = request.form['product_quantity']
            if product_quantity == '':
                product_quantity = 0
            product_price = request.form['product_price']
            product_image_1 = request.files['product_image_1']
            product_image_2 = request.files['product_image_2']
            product_image_3 = request.files['product_image_3']
            product_description = request.form['product_description']
            product_image_1_add = 'empty_product.png'
            product_image_2_add = 'empty_product.png'
            product_image_3_add = 'empty_product.png'
            if product_image_1.filename != '':
                product_image_1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(product_image_1.filename))))
                product_image_1_add = product_image_1.filename
            if product_image_2.filename != '':
                product_image_2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(product_image_2.filename))))
                product_image_2_add = product_image_2.filename
            if product_image_3.filename != '':
                product_image_3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(product_image_3.filename))))
                product_image_3_add = product_image_3.filename

            cursor.execute('INSERT INTO products (product_name, product_type_id, supplier_id, product_quantity, product_price, product_description, product_image_1, product_image_2, product_image_3) VALUES (% s,% s,% s,% s,% s,% s,% s,% s,% s);',
                                (product_name, product_type_id, supplier_id, product_quantity, product_price, product_description, product_image_1_add, product_image_2_add, product_image_3_add, ))
            mysql.connection.commit()

            msg = 'Add product successful!'
            return redirect(url_for('add_products', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_products_update', methods = ['POST', 'GET'])
def update_products_update():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update_product' in request.form:
            app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\image_products')
            product_id = request.form['product_id']
            product_name = request.form['product_name']
            product_type_id = request.form['product_type_id']
            supplier_id = request.form['supplier_id']
            product_quantity = request.form['product_quantity']
            if product_quantity == '':
                product_quantity = 0
            product_price = request.form['product_price']
            product_image_1 = request.files['product_image_1']
            product_image_2 = request.files['product_image_2']
            product_image_3 = request.files['product_image_3']
            product_description = request.form['product_description']
            if product_image_1.filename != '':
                product_image_1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(product_image_1.filename))))
                cursor.execute("UPDATE products SET product_image_1=% s WHERE product_id=% s;"
                                , (product_image_1.filename, product_id, ))
                mysql.connection.commit()
            if product_image_2.filename != '':
                product_image_2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(product_image_2.filename))))
                cursor.execute("UPDATE products SET product_image_2=% s WHERE product_id=% s;"
                                , (product_image_2.filename, product_id, ))
                mysql.connection.commit()
            if product_image_3.filename != '':
                product_image_3.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(product_image_3.filename))))
                cursor.execute("UPDATE products SET product_image_3=% s WHERE product_id=% s;"
                                , (product_image_3.filename, product_id, ))
                mysql.connection.commit()

            cursor.execute("UPDATE products SET product_name=% s, product_type_id=% s, supplier_id=% s, product_quantity=product_quantity+% s, product_price=% s, product_description=% s WHERE product_id=% s;"
                                , (product_name, product_type_id, supplier_id, product_quantity, product_price, product_description, product_id, ))
            mysql.connection.commit()

            msg = 'Update product successful!'
            return redirect(url_for('update_products', product_id = product_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_orders_update', methods = ['POST', 'GET'])
def update_orders_update():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update_order' in request.form:
            order_status_id = request.form['order_status_id']
            order_id = request.form['order_id']
            order_product_all_id = request.form['order_product_all_id']
            order_all_quantity = request.form['order_all_quantity']
            order_product_all_id_array = order_product_all_id.split(',')
            order_all_quantity_array = order_all_quantity.split(',')

            count = 0
            for array in order_product_all_id_array:
                cursor.execute('SELECT * FROM count_sales WHERE product_id=' + array, ())
                product = cursor.fetchone()
                if product:
                    cursor.execute("UPDATE count_sales SET count_sale=count_sale+" + order_all_quantity_array[count] + " WHERE product_id=" + array, ())
                    mysql.connection.commit()
                else:
                    cursor.execute('INSERT INTO count_sales (product_id, count_sale) VALUES ('+array+','+order_all_quantity_array[count]+');'
                                   , ())
                    mysql.connection.commit()
                if order_status_id == '3':
                    cursor.execute('UPDATE products SET product_quantity=product_quantity-'+order_all_quantity_array[count]+' WHERE product_id='+array+';'
                                , ())
                    mysql.connection.commit()
                count += 1

            cursor.execute("UPDATE orders SET order_status_id=% s WHERE order_id=% s;"
                                , (order_status_id, order_id, ))
            mysql.connection.commit()

            msg = 'Update order successful!'
            return redirect(url_for('update_orders', order_id = order_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_coupons_add', methods = ['POST', 'GET'])
def add_coupons_add():
    msg = request.args.get('message', '')
    if(check_login()):
        if request.method == 'POST' and 'add_coupons' in request.form:
            coupon_name = request.form['coupon_name']
            discount = request.form['discount']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO coupons (coupon_name, discount) VALUES (% s,% s);',
                                (coupon_name, discount, ))
            mysql.connection.commit()

            msg = 'Add coupon successfully!'
            return redirect(url_for('add_coupons', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_categories_add', methods = ['POST', 'GET'])
def add_categories_add():
    msg = request.args.get('message', '')
    if(check_login()):
        if request.method == 'POST' and 'add_categories' in request.form:
            product_type_name = request.form['product_type_name']
            coupon_id = request.form['coupon_id']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO product_types (product_type_name, coupon_id) VALUES (% s,% s);',
                                (product_type_name, coupon_id, ))
            mysql.connection.commit()

            msg = 'Add category successfully!'
            return redirect(url_for('add_categories', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_categories_update', methods = ['POST', 'GET'])
def update_categories_update():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update_categories' in request.form:
            product_type_id = request.form['product_type_id']
            product_type_name = request.form['product_type_name']
            coupon_id = request.form['coupon_id']
            cursor.execute("UPDATE product_types SET product_type_name=% s, coupon_id=% s WHERE product_type_id=% s;"
                                , (product_type_name, coupon_id, product_type_id, ))
            mysql.connection.commit()
            msg = 'Update category successful!'
            return redirect(url_for('update_categories', product_type_id = product_type_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_suppliers_add', methods = ['POST', 'GET'])
def add_suppliers_add():
    msg = request.args.get('message', '')
    if(check_login()):
        if request.method == 'POST' and 'add_suppliers' in request.form:
            supplier_name = request.form['supplier_name']
            supplier_email = request.form['supplier_email']
            supplier_address = request.form['supplier_address']
            supplier_phone = request.form['supplier_phone']
            avatar = request.files['avatar']
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM suppliers WHERE supplier_email= % s;', (supplier_email, ))
            supplier = cursor.fetchone()
            if not supplier:
                if not validate_email(supplier_email):
                    msg = 'Email or password arent allowed!'
                    return redirect(url_for('add_suppliers', message = msg))
                else:
                    if avatar.filename == '':
                        cursor.execute('INSERT INTO suppliers (supplier_name, supplier_email, supplier_address, supplier_phone, supplier_avatar) VALUES (% s,% s,% s,% s, % s);',
                                (supplier_name, supplier_email, supplier_address, supplier_phone, 'empty.png', ))
                        mysql.connection.commit()

                        msg = 'Create supplier account successfully!'
                    else:
                        app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                        cursor.execute('INSERT INTO suppliers (supplier_name, supplier_email, supplier_address, supplier_phone, supplier_avatar) VALUES (% s,% s,% s,% s, % s);',
                                (supplier_name, supplier_email, supplier_address, supplier_phone, avatar.filename, ))
                        mysql.connection.commit()

                        msg = 'Create supplier account successfully!'
                    cursor.execute("UPDATE count_others SET count_other=count_other+1 WHERE count_other_name='suppliers';", ())
                    mysql.connection.commit()
                    return redirect(url_for('add_suppliers', message = msg))
            else:
                msg = 'Email already exists!'
                return redirect(url_for('add_suppliers', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_suppliers_delete/<int:supplier_id>', methods = ['POST', 'GET'])
def update_suppliers_delete(supplier_id):
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM suppliers WHERE supplier_id=% s',
                            (supplier_id, ))
        mysql.connection.commit()

        cursor.execute("UPDATE count_others SET count_other=count_other-1 WHERE count_other_name='suppliers';", ())
        mysql.connection.commit()

        msg = 'Delete supplier successfully!'
        return redirect(url_for('view_suppliers', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_suppliers_update', methods = ['POST', 'GET'])
def update_suppliers_update():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update' in request.form:
            supplier_id = request.form['supplier_id']
            supplier_name = request.form['supplier_name']
            supplier_email = request.form['supplier_email']
            supplier_address = request.form['supplier_address']
            supplier_phone = request.form['supplier_phone']
            avatar = request.files['avatar']
            if not validate_phone_number(supplier_phone):
                msg = 'Invalid phone number!'
            else:
                if avatar.filename == '':
                    cursor.execute("UPDATE suppliers SET supplier_name=% s, supplier_email=% s, supplier_address=% s, supplier_phone=% s WHERE supplier_id=% s;"
                                , (supplier_name, supplier_email, supplier_address, supplier_phone, supplier_id, ))
                    mysql.connection.commit()

                    msg = 'Update supplier successful!'
                else:
                    app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                    avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                    cursor.execute("UPDATE suppliers SET supplier_name=% s, supplier_email=% s, supplier_address=% s, supplier_avatar=% s, supplier_phone=% s WHERE supplier_id=% s;"
                                , (supplier_name, supplier_email, supplier_address, avatar.filename, supplier_phone, supplier_id, ))
                    mysql.connection.commit()

                    msg = 'Update supplier successful!'
            return redirect(url_for('update_suppliers', supplier_id = supplier_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_employees_add', methods = ['POST', 'GET'])
def add_employees_add():
    msg = request.args.get('message', '')
    if(check_login()):
        if request.method == 'POST' and 'add_employees' in request.form:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            re_password = request.form['re-password']
            avatar = request.files['avatar']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email= % s;', (email, ))
            account = cursor.fetchone()
            if not account:
                if(not validate_email(email) or not validate_password(password) or not validate_password(re_password)):
                    msg = 'Email or password arent allowed!'
                    return redirect(url_for('add_employees', message = msg))
                elif(password != re_password):
                    msg = 'Password does not match!'
                    return redirect(url_for('add_employees', message = msg))
                else:
                    if avatar.filename == '':
                        cursor.execute('INSERT INTO accounts(account_name, email, password, avatar, role, block) VALUES \
                            (% s, % s, % s, % s, % s, % s)',
                                (name, email, password, 'empty.png', '0', '0', ))
                        mysql.connection.commit()

                        cursor.execute('SELECT account_id FROM accounts WHERE email= % s;', (email, ))
                        create_employee = cursor.fetchone()
                        if create_employee:
                            cursor.execute('INSERT INTO employees(account_id) VALUES \
                            (% s)',
                                (create_employee['account_id'], ))
                            mysql.connection.commit()

                        msg = 'Create employee account successfully!'
                    else:
                        app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                        cursor.execute('INSERT INTO accounts(account_name, email, password, avatar, role, block) VALUES \
                            (% s, % s, % s, % s, % s, % s)',
                                (name, email, password, avatar.filename, '0', '0', ))
                        mysql.connection.commit()

                        cursor.execute('SELECT account_id FROM accounts WHERE email= % s;', (email, ))
                        create_employee = cursor.fetchone()
                        if create_employee:
                            cursor.execute('INSERT INTO employees(account_id) VALUES \
                            (% s)',
                                (create_employee['account_id'], ))
                            mysql.connection.commit()

                        msg = 'Create employee account successfully!'
                    cursor.execute("UPDATE count_others SET count_other=count_other+1 WHERE count_other_name='customers';", ())
                    mysql.connection.commit()
                    return redirect(url_for('add_employees', message = msg))
            else:
                msg = 'Email already exists!'
                return redirect(url_for('add_employees', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_employees_delete/<int:account_id>', methods = ['POST', 'GET'])
def update_employees_delete(account_id):
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM accounts WHERE account_id=% s',
                            (account_id, ))
        mysql.connection.commit()

        cursor.execute('DELETE FROM employees WHERE account_id=% s',
                            (account_id, ))
        mysql.connection.commit()

        cursor.execute("UPDATE count_others SET count_other=count_other-1 WHERE count_other_name='employees';", ())
        mysql.connection.commit()

        msg = 'Delete employee successfully!'
        return redirect(url_for('view_employees', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_employees_update', methods = ['POST', 'GET'])
def update_employees_update():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update' in request.form:
            today = date.today()
            currentTime = today.strftime("%Y/%m/%d")
            account_id = request.form['account_id']
            account_name = request.form['account_name']
            account_address = request.form['account_address']
            gender = request.form['gender']
            phone = request.form['phone']
            date_of_birth = request.form['date_of_birth']
            employee_position = request.form['employee_position']
            avatar = request.files['avatar']
            if not validate_phone_number(phone):
                msg = 'Invalid phone number!'
            else:
                if avatar.filename == '':
                    cursor.execute("UPDATE accounts SET account_name=% s, account_address=% s, phone=% s, gender=% s, update_date_account=% s, date_of_birth=% s WHERE account_id=% s;"
                                , (account_name, account_address, phone, gender, currentTime, date_of_birth, account_id, ))
                    mysql.connection.commit()

                    cursor.execute("UPDATE employees SET employee_position=% s WHERE account_id=% s;"
                                , (employee_position, account_id, ))
                    mysql.connection.commit()

                    msg = 'Update customer successful!'
                else:
                    app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                    avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                    cursor.execute("UPDATE accounts SET account_name=% s, account_address=% s, avatar=% s, phone=% s, gender=% s, update_date_account=% s, date_of_birth=% s WHERE account_id=% s;"
                                , (account_name, account_address, avatar.filename, phone, gender, currentTime, date_of_birth, account_id, ))
                    mysql.connection.commit()

                    cursor.execute("UPDATE employees SET employee_position=% s WHERE account_id=% s;"
                                , (employee_position, account_id, ))
                    mysql.connection.commit()

                    msg = 'Update customer successful!'
            return redirect(url_for('update_employees', account_id = account_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/add_customers_add', methods = ['POST', 'GET'])
def add_customers_add():
    msg = request.args.get('message', '')
    if(check_login()):
        if request.method == 'POST' and 'add_customers' in request.form:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            re_password = request.form['re-password']
            avatar = request.files['avatar']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email= % s;', (email, ))
            account = cursor.fetchone()
            if not account:
                if(not validate_email(email) or not validate_password(password) or not validate_password(re_password)):
                    msg = 'Email or password arent allowed!'
                    return redirect(url_for('add_customers', message = msg))
                elif(password != re_password):
                    msg = 'Password does not match!'
                    return redirect(url_for('add_customers', message = msg))
                else:
                    if avatar.filename == '':
                        cursor.execute('INSERT INTO accounts(account_name, email, password, avatar, role, block) VALUES \
                            (% s, % s, % s, % s, % s, % s)',
                                (name, email, password, 'empty.png', '0', '0', ))
                        mysql.connection.commit()
                        msg = 'Account successfully created!'
                    else:
                        app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                        avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                        cursor.execute('INSERT INTO accounts(account_name, email, password, avatar, role, block) VALUES \
                            (% s, % s, % s, % s, % s, % s)',
                                (name, email, password, avatar.filename, '0', '0', ))
                        mysql.connection.commit()
                        msg = 'Account successfully created!'
                    cursor.execute("UPDATE count_others SET count_other=count_other+1 WHERE count_other_name='customers';", ())
                    mysql.connection.commit()
                    return redirect(url_for('add_customers', message = msg))
            else:
                msg = 'Email already exists!'
                return redirect(url_for('add_employees', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/update_customers_update', methods = ['POST', 'GET'])
def update_customers_update():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update' in request.form:
            today = date.today()
            currentTime = today.strftime("%Y/%m/%d")
            account_id = request.form['account_id']
            account_name = request.form['account_name']
            account_address = request.form['account_address']
            gender = request.form['gender']
            phone = request.form['phone']
            date_of_birth = request.form['date_of_birth']
            avatar = request.files['avatar']
            if not validate_phone_number(phone):
                msg = 'Invalid phone number!'
            else:
                if avatar.filename == '':
                    cursor.execute("UPDATE accounts SET account_name=% s, account_address=% s, phone=% s, gender=% s, update_date_account=% s, date_of_birth=% s WHERE account_id=% s;"
                                , (account_name, account_address, phone, gender, currentTime, date_of_birth, account_id, ))
                    mysql.connection.commit()
                    msg = 'Update customer successful!'
                else:
                    app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                    avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                    cursor.execute("UPDATE accounts SET account_name=% s, account_address=% s, avatar=% s, phone=% s, gender=% s, update_date_account=% s, date_of_birth=% s WHERE account_id=% s;"
                                , (account_name, account_address, avatar.filename, phone, gender, currentTime, date_of_birth, account_id, ))
                    mysql.connection.commit()
                    msg = 'Update customer successful!'
            return redirect(url_for('update_customers', account_id = account_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_customers_unblock/<int:account_id>', methods = ['POST', 'GET'])
def view_customers_unblock(account_id):
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET block=0 WHERE account_id=% s;"
                            , (account_id, ))
        mysql.connection.commit()
        msg = 'Unblock account successful!'
        return redirect(url_for('view_customers', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_admin/view_customers_block/<int:account_id>', methods = ['POST', 'GET'])
def view_customers_block(account_id):
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE accounts SET block=1 WHERE account_id=% s;"
                            , (account_id, ))
        mysql.connection.commit()
        msg = 'Block account successful!'
        return redirect(url_for('view_customers', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_order_delete/<int:order_id>', methods = ['POST', 'GET'])
def account_order_delete(order_id):
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE orders SET order_status_id=% s WHERE order_id=% s;"
                            , (4, order_id, ))
        mysql.connection.commit()
        msg = 'Product removed from order successfully!'
        return redirect(url_for('account_order', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/page_carts_delete/<int:product_id>', methods = ['POST', 'GET'])
def page_carts_delete(product_id):
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM carts WHERE account_id=% s AND product_id=% s',
                            (session['account_id'], product_id))
        mysql.connection.commit()
        msg = 'Product removed from cart successfully!'
        return redirect(url_for('page_carts', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_reset_pass_check', methods = ['POST', 'GET'])
def account_reset_pass_check():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update_pass' in request.form:
            current_password = request.form['current-password']
            new_password = request.form['new-password']
            verify_password = request.form['verify-password']
            # if not validate_email(current_password) or not validate_password(new_password) or not validate_password(verify_password):
            #     msg = 'Invalid password!'
            #     return redirect(url_for('account_reset_pass', message = msg))
            if new_password != verify_password:
                msg = 'Passwords do not match!'
                return redirect(url_for('account_reset_pass', message = msg))
            cursor.execute("UPDATE accounts SET password=% s WHERE account_id=% s;"
                            , (new_password, session['account_id'], ))
            mysql.connection.commit()
            msg = 'Password update successful!'
        return redirect(url_for('account_reset_pass', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_page_update_info', methods = ['POST', 'GET'])
def account_page_update_info():
    if(check_login()):
        msg = request.args.get('message', '')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST' and 'update' in request.form:
            today = date.today()
            currentTime = today.strftime("%Y/%m/%d")
            account_name = request.form['account_name']
            date_of_birth = request.form['date_of_birth']
            account_address = request.form['account_address']
            gender = request.form['gender']
            phone = request.form['phone']
            avatar = request.files['avatar']
            if not validate_phone_number(phone):
                msg = 'Invalid phone number!'
            else:
                if avatar.filename == '':
                    cursor.execute("UPDATE accounts SET account_name=% s, date_of_birth=% s, account_address=% s, phone=% s, gender=% s, update_date_account=% s WHERE account_id=% s;"
                                , (account_name, date_of_birth, account_address, phone, gender, currentTime, session['account_id'], ))
                    mysql.connection.commit()
                    msg = 'Update account successful!'
                else:
                    app.config['UPLOAD_FOLDER'] = os.path.join(path, 'staticFiles\\assets\\img\\avatars')
                    avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(avatar.filename))))
                    cursor.execute("UPDATE accounts SET account_name=% s, date_of_birth=% s, account_address=% s, avatar=% s, phone=% s, gender=% s, update_date_account=% s WHERE account_id=% s;"
                                , (account_name, date_of_birth, account_address, avatar.filename, phone, gender, currentTime, session['account_id'], ))
                    mysql.connection.commit()
                    msg = 'Update account successful!'
        return redirect(url_for('account_page', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/account_page_logout')
def account_page_logout():
    if(check_login()):
        msg = request.args.get('message', '')
        session.clear()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE count_others SET count_other=count_other-1 WHERE count_other_name='account_online';", ())
        mysql.connection.commit()
        msg = 'Successful logout!'
        return redirect(url_for('login', message = msg))
    else:
        msg = 'You must be login first!'
        return redirect(url_for('login', message = msg))
@app.route('/_users/product_detail_add_cart', methods = ['POST', 'GET'])
def product_detail_add_cart():
    if(check_login()):
        product_id = -1
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        msg = request.args.get('message', '')
        if request.method == 'POST' and 'add' in request.form:
            cart_quantity = int(request.form['cart_quantity'])
            product_id = request.form['product_id']

            query_number_product_exits = "SELECT cart_quantity FROM carts WHERE account_id=% s AND product_id=% s;"
            cursor.execute(query_number_product_exits, (session['account_id'], product_id, ))
            quantity = cursor.fetchone()
            if quantity:
                cart_quantity += quantity['cart_quantity']
                cursor.execute('UPDATE carts SET cart_quantity=% s WHERE account_id = % s AND product_id = % s;'
                           , (cart_quantity, session['account_id'], product_id, ))
                mysql.connection.commit()
                msg = 'The product already exists in cart, so will be added!'
            else:
                cursor.execute('INSERT INTO carts (account_id, product_id, cart_quantity) VALUES \
                            (% s, % s, % s)',
                                (session['account_id'], product_id, cart_quantity, ))
                mysql.connection.commit()
                msg = 'Add to cart successfully!'
        return redirect(url_for('product_detail', product_id=product_id, message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/checkout_check', methods = ['POST', 'GET'])
def checkout_check():
    if(check_login()):
        msg = request.args.get('message', '')
        if request.method == 'POST' and 'orders' in request.form:
            order_product_all_id = request.form['order_product_all_id']
            order_all_quantity = request.form['order_all_quantity']
            order_name = request.form['order_name']
            order_address = request.form['order_address']
            order_phone = request.form['order_phone']
            order_notes = request.form['order_notes']
            order_status_id = 1
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO orders (account_id, order_product_all_id, order_all_quantity, order_name, order_address, order_phone, order_notes, order_status_id) VALUES \
                        (% s, % s, % s, % s, % s, % s, % s, % s)',
                            (session['account_id'], order_product_all_id, order_all_quantity, order_name, order_address, order_phone, order_notes, order_status_id, ))
            mysql.connection.commit()

            cursor.execute('DELETE FROM carts WHERE account_id=% s',
                            (session['account_id'], ))
            mysql.connection.commit()
            #cần test lại
            msg = 'You have successfully order!'
            return redirect(url_for('index', message = msg))
    else:
        msg = 'You must be login first!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/login_check', methods = ['POST', 'GET'])
def login_check():
    msg = request.args.get('message', '')
    if request.method == 'POST' and 'login' in request.form:
        email = request.form['email']
        password = request.form['password']
            # if(not validate_email(email) or not validate_password(password)):
            #     msg = 'Email or password arent allowed!'
            #     return redirect(url_for('login', message = msg))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            if account['block'] == 1:
                msg = 'Your account is locked!'
                return redirect(url_for('login', message = msg))
            session['account_id'] = account['account_id']
            session['account_name'] = account['account_name']
            if account['avatar'] == '':
                session['avatar'] = 'empty.png'
            else:
                session['avatar'] = account['avatar']

            cursor.execute("UPDATE count_others SET count_other=count_other+1 WHERE count_other_name='account_online';", ())
            mysql.connection.commit()

            msg = 'Logged in successfully!'
            if account['role'] == 1:
                return redirect(url_for('admin', message = msg))
            return redirect(url_for('index', message = msg))
        else:
            msg = 'Incorrect email or password!'
    return redirect(url_for('login', message = msg))
@app.route('/_users/register_check', methods = ['POST', 'GET'])
def register_check():
    msg = request.args.get('message', '')
    if request.method == 'POST' and 'create_account' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['re-password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email= % s;', (email, ))
        account = cursor.fetchone()
        if not account:
            if(not validate_email(email) or not validate_password(password) or not validate_password(re_password)):
                msg = 'Email or password arent allowed!'
                return redirect(url_for('register', message = msg))
            elif(password != re_password):
                msg = 'Password does not match!'
                return redirect(url_for('register', message = msg))
            else:
                cursor.execute('INSERT INTO accounts(account_name, email, password, avatar, role, block) VALUES \
                    (% s, % s, % s, % s, % s, % s)',
                        (name, email, password, 'empty.png', '0', '0', ))
                mysql.connection.commit()
                msg = 'You have successfully registered!'
                return redirect(url_for('index', message = msg))
        else:
            msg = 'Email already exists!'
    return redirect(url_for('register', message = msg))


if __name__=='__main__':
    app.run(host='localhost', port=5000)