from flask import Flask, redirect, url_for, render_template, request, session
from bs4 import BeautifulSoup
import re

def check_login():
    if 'account_id' in session:
        return True
    else:
        return False

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    
def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[!@#$%^&*()_+=\-{}[\]|:;"\'<>,.?/~`]', password):
        return False
    return True

def base_user_1_arrays_all_product(cursor):
    query_all_product = 'SELECT product_type_id, product_type_name FROM product_types;'
    cursor.execute(query_all_product)
    return cursor.fetchall()

def base_user_1_arrays_carts(cursor):
    list = ()
    if 'account_id' in session:
        account_id = str(session['account_id'])
        infor_cart = "products.product_id, product_name, product_price, product_image_1, discount, cart_quantity"
        table = "products, count_sales, product_types, coupons, carts"
        link = "products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND count_sales.product_id=products.product_id AND carts.product_id=products.product_id"
        query_cart = "SELECT " + infor_cart + " FROM " + table + " WHERE " + link + " AND account_id=" + account_id + ";"                  
        cursor.execute(query_cart)
        arrays_carts = cursor.fetchall()
        for x in arrays_carts:
            array = {"product_id": x['product_id']
                 , "product_name": x['product_name'][0:25]
                 , "product_image_1": x['product_image_1']
                 , "cart_quantity": x['cart_quantity']
                 , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)}
            list += (array,)
    return list

def convert_html_to_text(html_code):
    soup = BeautifulSoup(html_code, 'html.parser')
    text = soup.get_text()
    return text

def top_3_product(cursor):
    prepare_query = 'products.product_id, product_name, product_price, product_image_1, discount'
    query_product_hot_detail = "SELECT " + prepare_query + " FROM products, count_sales, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND count_sales.product_id=products.product_id ORDER BY count_sale DESC LIMIT 3;"
    cursor.execute(query_product_hot_detail, ())
    arrays_product_hot_detail = cursor.fetchall()
    list = ()
    for x in arrays_product_hot_detail:
        array = {"product_id": x['product_id']
                 , "product_name": x['product_name'][0:25]
                 , "product_image_1": x['product_image_1']
                 , "product_price": round(x['product_price'],2)
                 , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)}
        list += (array,)
    return list

def get_product_cart_by_account(cursor):
    infor_product = 'products.product_id, product_name, product_price, product_image_1, discount, cart_quantity, product_quantity'
    table = 'products, product_types, coupons, carts'
    link = "products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND carts.product_id=products.product_id"
    query_product_cart_all = "SELECT " + infor_product + " FROM " + table + " WHERE " + link + " AND account_id=% s;"
    cursor.execute(query_product_cart_all, (session['account_id'], ))
    arrays_product_cart_all = cursor.fetchall()
    list = ()
    total = 0
    order_product_all_id = ''
    order_all_quantity = ''
    for x in arrays_product_cart_all:
        array = {"product_id": x['product_id']
                    , "product_name": x['product_name'][0:25]
                    , "product_image_1": x['product_image_1']
                    , "discount": x['discount']
                    , "cart_quantity": x['cart_quantity']
                    , "product_quantity": x['product_quantity']
                    , "product_price": round(x['product_price'],2)
                    , "product_price_total": round(x['product_price'] - (x['product_price'] * (x['discount'] / 100)), 2)
                    , "product_price_total_cart": round((x['product_price'] - (x['product_price'] * (x['discount'] / 100))) * x['cart_quantity'], 2)}
        list += (array,)
        total += ((x['product_price'] - (x['product_price'] * (x['discount'] / 100))) * x['cart_quantity'])

        order_product_all_id += str(x['product_id']) + ','
        order_all_quantity += str(x['cart_quantity']) + ','
    order_product_all_id = order_product_all_id[:-1]
    order_all_quantity = order_all_quantity[:-1]
    return list, total, order_product_all_id, order_all_quantity

def get_account(cursor):
    query_customer = "SELECT * FROM accounts WHERE account_id=% s;"
    cursor.execute(query_customer, (session['account_id'], ))
    customer = cursor.fetchone()
    return customer

def remove_special_characters(string):
    pattern = r'[^a-zA-Z0-9\s]'
    return re.sub(pattern, '', string)

def get_all_order_by_status(cursor, order_status_id):
    query_order = "SELECT order_id, account_id, order_product_all_id, order_all_quantity, order_name, order_address, order_phone, order_notes, date_invoice_order, order_status_id FROM orders WHERE account_id=% s AND order_status_id=% s;"
    cursor.execute(query_order, (session['account_id'],order_status_id, ))
    arrays_orders = cursor.fetchall()
    list = ()
    for x in arrays_orders:
        total = 0
        order_product_all_id = x['order_product_all_id'].split(',')
        order_all_quantity = x['order_all_quantity'].split(',')
        count = 1
        array1 = ()
        list1 = ()
        for item in order_product_all_id:
            info_product = "products.product_id, product_name, product_price, product_image_1, discount"
            query_each_product = "SELECT " + info_product + " FROM products, product_types, coupons WHERE products.product_type_id=product_types.product_type_id AND product_types.coupon_id=coupons.coupon_id AND products.product_id=% s;"
            cursor.execute(query_each_product, (item, ))
            arrays_each_order = cursor.fetchone()
            if arrays_each_order:
                array1 = {"count": count     
                        ,"product_id": arrays_each_order['product_id']
                        , "product_name": arrays_each_order['product_name']
                        , "product_price": arrays_each_order['product_price']
                        , "product_image_1": arrays_each_order['product_image_1']
                        , "discount": arrays_each_order['discount']
                        , "order_all_quantity": order_all_quantity[count-1]
                        , "product_price_total": round(arrays_each_order['product_price'] - (arrays_each_order['product_price'] * (arrays_each_order['discount'] / 100)), 2)
                        , "product_price_total_quantity": round((arrays_each_order['product_price'] - (arrays_each_order['product_price'] * (arrays_each_order['discount'] / 100))) * int(order_all_quantity[count-1]), 2)
                        }
                list1 += (array1,)
                total += ((arrays_each_order['product_price'] - (arrays_each_order['product_price'] * (arrays_each_order['discount'] / 100))) * int(order_all_quantity[count-1]))
            count += 1
            
        array = {"order_id": x['order_id']
                 , "account_id": x['account_id']
                 , "order_name": x['order_name']
                 , "order_address": x['order_address']
                 , "order_phone": x['order_phone']
                 , "order_notes": x['order_notes']
                 , "date_invoice_order": str(x['date_invoice_order'])[0:9]
                 , "order_status_id": x['order_status_id']
                 , "total": total
                 , "detail_order": list1}
        list += (array,)
    return list

def get_count_order(cursor):
    query = "SELECT count_other FROM count_others WHERE count_other_name='products';"
    cursor.execute(query)
    arrays_count_order = cursor.fetchone()

    query = "SELECT SUM(count_sale) AS count FROM count_sales;"
    cursor.execute(query)
    arrays_count_sale = cursor.fetchone()

    query = "SELECT count_other FROM count_others WHERE count_other_name='customers';"
    cursor.execute(query)
    arrays_count_customer = cursor.fetchone()

    query = "SELECT count_other FROM count_others WHERE count_other_name='employees';"
    cursor.execute(query)
    arrays_count_employees = cursor.fetchone()

    array = {"arrays_count_order": arrays_count_order['count_other']
            , "arrays_count_sale": arrays_count_sale['count']
            , "arrays_count_customer": arrays_count_customer['count_other']
            , "arrays_count_employees": arrays_count_employees['count_other']}
    return array