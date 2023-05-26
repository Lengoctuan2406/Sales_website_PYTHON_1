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
UPLOAD_FOLDER = os.path.join(path, 'staticFiles\\assets\\img\\avatars')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
 
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
@app.route('/_users/product_detail/<product_id>')
def product_detail(product_id):
    msg = request.args.get('message', '')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    arrays_all_product = base_user_1_arrays_all_product(cursor)
    arrays_carts = base_user_1_arrays_carts(cursor)

    prepare_query = 'product_id, products.product_type_id, product_name, product_quantity, product_price, product_description, product_image_1, product_image_2, product_image_3, discount, product_type_name'
    query_product_detail = "SELECT " + prepare_query + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND product_id=" + str(product_id) + ";"
    cursor.execute(query_product_detail, ())
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
        orders_1 = get_all_order_by_status(cursor, 1)
        orders_2 = get_all_order_by_status(cursor, 2)
        return render_template('_users/account_order.html', orders_1=orders_1, orders_2=orders_2, msg=msg)
    else:
        msg = 'You must be login first!'
        return redirect(url_for('login', message = msg))
@app.route('/_users/account_purchase_history')
def account_purchase_history():
    msg = request.args.get('message', '')
    if(check_login()):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        order_history = get_all_order_by_status(cursor, 3)
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

        return render_template('_admin/index.html', array1=array1, list_products=list_products, list_order=list_order, msg=msg)
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
            file_old = request.form['file_old']
            avatar = request.files['avatar']
            if avatar.filename == '':
                cursor.execute("UPDATE accounts SET account_name=% s, date_of_birth=% s, account_address=% s, avatar=% s, phone=% s, gender=% s, update_date_account=% s WHERE account_id=% s;"
                            , (account_name, date_of_birth, account_address, file_old, phone, gender, currentTime, session['account_id'], ))
                mysql.connection.commit()
                msg = 'Update account successful!'
            else:
                # os.remove(app.config['UPLOAD_FOLDER'] + '\\' + secure_filename(avatar.filename))
                avatar.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(avatar.filename)))
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
        msg = 'Successful logout!'
        return redirect(url_for('login', message = msg))
    else:
        msg = 'You must be login first!'
        return redirect(url_for('login', message = msg))
@app.route('/_users/product_detail_add_cart', methods = ['POST', 'GET'])
def product_detail_add_cart():
    if(check_login()):
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
        return redirect(url_for('page_carts', message = msg))
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
            session['account_id'] = account['account_id']
            session['account_name'] = account['account_name']
            session['avatar'] = account['avatar']
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