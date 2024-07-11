import sqlite3


def create_users_table():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    create table if not exists users(
        user_id integer primary key autoincrement,
        full_name text,
        telegram_id bigint not null unique,
        phone text
    );
    ''')
    database.commit()
    database.close()

# create_users_table()


def create_carts_table():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    create table if not exists carts(
        cart_id integer primary key autoincrement,
        user_id integer references users(user_id),
        total_price decimal(12, 2 ) default 0,
        total_products integer default 0
    );
    ''')
    database.commit()
    database.close()

# create_carts_table()


def create_cart_products_table():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
        create table if not exists cart_products(
            cart_products_id integer primary key autoincrement,
            product_name varchar(30),
            quantity integer not null,
            final_price decimal(12, 2 ) not null,
            cart_id integer references carts(cart_id),
            
            unique(product_name, cart_id)
        );
    ''')

    database.commit()
    database.close()


# create_cart_products_table()


def create_categories_table():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    create table if not exists categories(
        category_id integer primary key autoincrement,
        category_name varchar(20) not null unique
    );
''')
    database.commit()
    database.close()

# create_categories_table()


def insert_categories():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    insert into categories(category_name) values
    ('Lavash 🌯'),
    ('Burger 🍔'),
    ('Pizza 🍕'),
    ('Xot-dog 🌭'),
    ('Sneks 🍟'),
    ('Napitki 🥤'),
    ('Desert 🍩')
    ''')
    database.commit()
    database.close()

# insert_categories()


def create_products_table():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    create table if not exists products(
        product_id integer primary key autoincrement,
        category_id integer not null,
        product_name varchar(30) not null unique,
        price decimal(12, 2 ) not null,
        description varchar(100),
        image text,
    
        foreign key(category_id) references categories(category_id)
        );
        ''')
    database.commit()
    database.close()

# create_products_table()

def insert_products_table():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    insert into products(category_id, product_name, price, description, image) values
    (1, 'Lavash fitter', 20000, 'otli lavash', 'media/lavash/fitter_lavash.jpg'),
    (1, 'Lavash achchiq-mol', 28000, 'mol goshtli va achchiq lavash', 'media/lavash/mol_achchiq_lavash.jpg'),
    (1, 'Lavash mol-sirli', 29000, 'mol goshtidan sirli lavash', 'media/lavash/mol_sirli_lavash.jpg'),
    (1, 'Lavash tovuq-achchiq', 27000, 'tovuq goshtli achchiq lavash', 'media/lavash/tovuq_achchiq_lavash.jpg'),
    (1, 'Lavash tovuq-sirli', 28000, 'tovuq goshtli sirli lavash', 'media/lavash/tovuq_sirli_lavash.jpg'),
    (1, 'Lavash tovuqli', 27000, 'tovuq goshtli', 'media/lavash/tovuqli_lavash.jpg'),
    (2, 'Burger kotletli', 25000, 'Oddiy original burger', 'media/burger/Burger.jpg'),
    (2, 'ChizBurger', 27000, 'Sirli original burger', 'media/burger/Chizburger.jpg'),
    (2, 'DublBurger', 33000, 'ikki qavatli original burger', 'media/burger/Dublburger.jpg'),
    (2, 'Burger original', 35000, 'ikki qavatli sirli original burger', 'media/burger/Dublchizburger.jpg'),
    (3, 'Amerikano', 55000, 'Kalbasa va sirli', 'media/pizza/amerikano.png'),
    (3, 'Gribnoy', 50000, 'Qoziqorin va sirli', 'media/pizza/gribnoy.png'),
    (3, 'Milano', 50000, 'sirli va sousli', 'media/pizza/milano.png'),
    (3, 'Goshtli', 60000, 'Goshtli va sirli', 'media/pizza/myasnoy.png'),
    (3, 'Ovoshnoy', 45000, 'sabzavot mix', 'media/pizza/ovoshnoy.png'),
    (4, 'Xot-dog detskiy', 18000, 'bolalarga moljallangan xot-dog', 'media/xot-dog/detskiy.jpg'),
    (4, 'Xot-dog dubl', 25000, 'katta xot-dog', 'media/xot-dog/dubl_xot-dog.jpg'),
    (4, 'Xot-dog mini', 20000, 'kichkina moljallangan xot-dog', 'media/xot-dog/mini-xotdog.jpg'),
    (4, 'Xot-dog', 22000, 'oddiy moljallangan xot-dog', 'media/xot-dog/xot-dog.jpg'),
    (5, 'Fri', 7000, 'qovurilgan kartoshka', 'media/sneki/fri.png'),
    (5, 'Nagetsi', 15000, 'qovurilgan tovuq filesi', 'media/sneki/nagetsi.png'),
    (5, 'Nojki', 12000, 'qovurilgan tovuq oyoqchalari', 'media/sneki/nojki.png'),
    (5, 'Strips', 15000, 'qovurilgan tovuq filesi', 'media/sneki/stripsi.png'),
    (6, 'Suv', 3000, 'gazsiz oddiy suv', 'media/colddrink/bez-gaz suv.jpg'),
    (6, 'Bliss', 10000, 'gazsiz oddiy suv', 'media/colddrink/bliss sok.jpg'),
    (6, 'Limon choy', 10000, 'limonli choy', 'media/colddrink/choylimon.png'),
    (6, 'Coffee', 10000, 'qora achchiq coffee', 'media/colddrink/coffe.png'),
    (6, 'Fanta', 15000, 'fanta', 'media/colddrink/fanta_PNG4.png'),
    (6, 'Pepsi 1.5l', 15000, 'pepsi', 'media/colddrink/pepsi 1.5.jpg'),
    (6, 'Pepsi razliv', 10000, 'pepsi', 'media/colddrink/pepsi-razliv.jpg'),
    (7, 'Cheescake', 20000, 'pirog', 'media/desert/cheezcake.png'),
    (7, 'Donat', 5000, 'kulcha karamelli', 'media/desert/donat.png'),
    (7, 'Muzqaymoq', 10000, 'pirog', 'media/desert/marojni.png'),
    (7, 'Medovik', 15000, 'mevali kulcha', 'media/desert/medovik.png'),
    (7, 'Pichenye', 8000, 'mevali kulcha', 'media/desert/pechenye.png'),
    (7, 'Tort', 20000, 'mevali kulcha', 'media/desert/tort.png')
    ''')
    database.commit()
    database.close()

# insert_products_table()





def first_select_user(chat_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select * from users where telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


def first_register_user(chat_id, full_name):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    insert into users(telegram_id, full_name) values(?, ?)
    ''', (chat_id, full_name))
    database.commit()
    database.close()


def update_user_to_finish_register(chat_id, phone):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
        update users
        set phone = ?
        where telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def insert_to_cart(chat_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    insert into carts(user_id) values
    (
    (select user_id from users where telegram_id = ?)
    )
    ''', (chat_id,))
    database.commit()
    database.close()


def get_all_categories():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select * from categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories

def get_products_by_category_id(category_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select product_id, product_name
    from products where category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products

def get_product_detail(product_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select * from products
    where product_id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product

def get_user_cart_id(chat_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute(''' 
    select cart_id from carts
    where user_id = (select user_id from users where telegram_id = ?)
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id

def insert_or_update_cart_product(cart_id, product, quantity, final_price):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()

    try:
        cursor.execute('''
        insert into cart_products(cart_id, product_name, quantity, final_price)
        values(?, ?, ?, ?)
        ''', (cart_id, product, quantity, final_price))
        database.commit()
        return True
    except:
        cursor.execute('''
        update cart_products
        set quantity = ?,
        final_price = ?
        where product_name = ? and cart_id = ?
        ''', (quantity, final_price, product, cart_id))
        database.commit()
        return False
    finally:
        database.close()

def update_total_product_total_price(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    update carts
    set total_products = (
    select sum(quantity) from cart_products
    where cart_id = :cart_id
    ),
    total_price = (
    select sum(final_price) from cart_products
    where cart_id = :cart_id
    )
    where cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_cart_products(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select product_name, quantity, final_price
    from cart_products
    where cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products

def get_total_products_price(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select total_products, total_price from carts where cart_id = ?
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price


def get_cart_product_for_delete(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select cart_products_id, product_name
    from cart_products
    where cart_id = ?
    ''', (cart_id,))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products

def delete_cart_product_from_database(cart_products_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    delete from cart_products where cart_products_id = ?
    ''', (cart_products_id,))
    database.commit()
    database.close()

def drop_cart_products_default(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    delete from cart_products
    where cart_id = ?
    ''', (cart_id,))
    database.commit()
    database.close()


def orders_check():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    create table if not exists orders_check(
    order_check_id integer primary key autoincrement,
    cart_id integer references carts(cart_id),
    total_price decimal(12, 2) default 0,
    total_products integer default 0,
    time_order text,
    data_order text
    );
    ''')

# orders_check()


def order():
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    create table if not exists orders(
        order_id integer primary key autoincrement,
        order_check_id integer references orders_check(order_check_id),
        product_name varchar(100) not null,
        quantity integer not null,
        final_price decimal(12, 2) not null
    );
    ''')
    database.commit()
    database.close()

# order()


def save_order_check(cart_id, total_products, total_price, time_order, data_order):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    insert into orders_check(cart_id, total_products, total_price, time_order, data_order)
    values(?, ?, ?, ?, ?)
    ''', (cart_id, total_products, total_price, time_order, data_order))
    database.commit()
    database.close()

def get_order_check_id(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select order_check_id from orders_check
    where cart_id = ?
    ''', (cart_id,))
    orders_check_id = cursor.fetchall()[-1][0]
    database.close()
    return orders_check_id


def save_order(order_check_id, product_name, quantity, final_price):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    insert into orders(order_check_id, product_name, quantity, final_price)
    values(?, ?, ?, ?)
    ''', (order_check_id, product_name, quantity, final_price))
    database.commit()
    database.close()


def get_order_check(cart_id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
    select * from orders_check
    where cart_id = ?
    ''', (cart_id,))
    orders_check_info = cursor.fetchall()
    database.close()
    return orders_check_info

def get_detail_order(id):
    database = sqlite3.connect('havchik.db')
    cursor = database.cursor()
    cursor.execute('''
        select product_name, quantity, final_price from orders
        where order_check_id = ?
    ''', (id,))
    detail_order = cursor.fetchall()
    database.close()
    return detail_order



















