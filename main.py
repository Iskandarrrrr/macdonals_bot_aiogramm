from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, LabeledPrice, ContentType
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keyboards import *
from database import *
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

load_dotenv()


TOKEN = os.getenv('TOKEN')
PAYMENT = os.getenv('PAYMENT')

bot = Bot(TOKEN, parse_mode='html')

db = Dispatcher(bot)

@db.message_handler(commands=['start'])
async def command_start(message: Message):
    full_name = message.from_user.full_name
    await message.answer(f'Привет! <b>{full_name}</b>\n'
                         f'Добро пожаловать в fast-food!🍔')
    await register_user(message)

async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = first_select_user(chat_id)
    if user:
        await message.answer('Вы успешно зарегистрировались!📑')
        await show_main_menu(message)
    else:
        first_register_user(chat_id, full_name)
        await message.answer('Чтобы регистрироваться нажмите на кнопку! 👇', reply_markup=phone_button())


@db.message_handler(content_types=['contact'])
async def finish_register(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    update_user_to_finish_register(chat_id, phone)
    await create_cart_for_user(message)
    await message.answer('Вы успешно зарегистрировались 📰')
    await show_main_menu(message)

async def create_cart_for_user(message: Message):
    chat_id = message.chat.id
    try:
        insert_to_cart(chat_id)
    except:
        pass

async def show_main_menu(message: Message):
    await message.answer('Чтобы посмотреть меню нажмите на кнопку заказать! 🍱', reply_markup=generate_main_menu())

@db.message_handler(lambda message: 'Заказать ✅' in message.text)
async def make_order(message: Message):
    await message.answer('Выберите категорию', reply_markup=generate_category_menu())

@db.callback_query_handler(lambda call: 'category' in call.data)
async def show_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')
    category_id = int(category_id)
    await bot.edit_message_text('Выбери продукту 🫓!', chat_id, message_id, reply_markup=products_by_category(category_id))

@db.callback_query_handler(lambda call: 'main_menu' in call.data)
async def return_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Выберите категорию 🫓',
                                reply_markup=generate_category_menu())

@db.callback_query_handler(lambda call: 'product' in call.data)
async def show_detail_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, product_id = call.data.split('_')
    product_id = int(product_id)

    product = get_product_detail(product_id)
    await bot.delete_message(chat_id, message_id)
    with open(product[-1], mode='rb') as img:
        await bot.send_photo(chat_id, photo=img, caption=f'''{product[2]}
Состав: {product[4]}

Цена: {product[3]}
''', reply_markup=generate_product_detail_menu(product_id=product_id, category_id=product[1]))

@db.callback_query_handler(lambda call: 'back' in call.data)
async def return_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')
    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Выберите продукту 🫓!', reply_markup=products_by_category(category_id))


@db.callback_query_handler(lambda call: 'cart' in call.data)
async def add_product_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split('_')
    product_id, quantity = int(product_id), int(quantity)

    cart_id = get_user_cart_id(chat_id)
    product = get_product_detail(product_id)


    final_price = quantity * product[3]


    if insert_or_update_cart_product(cart_id, product[2], quantity, final_price):
        await bot.answer_callback_query(call.id, 'Продукт добавлен!')
    else:
        await bot.answer_callback_query(call.id, 'Изменен количество!')

@db.message_handler(regexp='Корзина 🛒')
async def show_cart(message: Message, edit_message: bool = False):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)

    try:
        update_total_product_total_price(cart_id)
    except Exception as e:
        print(e)
        await message.answer('Корзина пуст!')
        return

    cart_products = get_cart_products(cart_id)
    total_products, total_price = get_total_products_price(cart_id)

    if total_products and total_price:
        text = 'Ваша корзина 🛒: \n\n'
        i = 0
        for product_name, quantity, final_price, in cart_products:
            i += 1
            text += f'''{i}, {product_name}
    Количество: {quantity}
    Общая сумма: {final_price}\n\n'''

        text += f'''Выбранные продукты: {total_products}
    К оплате: {total_price} сум!'''

        if edit_message:
            await bot.edit_message_text(text, chat_id, message.message_id, reply_markup=generate_cart_menu(cart_id))
        else:
            await bot.send_message(chat_id, text, reply_markup=generate_cart_menu(cart_id))
    else:
        await bot.delete_message(chat_id, message.message_id)
        await bot.send_message(chat_id, 'Корзина пуст 🤷‍♂!')

@db.callback_query_handler(lambda call: 'delete' in call.data)
async def delete_cart_product(call: CallbackQuery):
    _, cart_products_id = call.data.split('_')
    message = call.message
    cart_products_id = int(cart_products_id)

    delete_cart_product_from_database(cart_products_id)

    await bot.answer_callback_query(call.id, text='Продукт удален!')
    await show_cart(message, edit_message=True)


@db.callback_query_handler(lambda call: 'order' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id

    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)
    time_order = datetime.now().strftime('%H:%M')
    data_order = datetime.now().strftime('%d.%m.%Y')



    cart_products = get_cart_products(cart_id)
    total_products, total_price = get_total_products_price(cart_id)


    save_order_check(cart_id, total_products, total_price, time_order, data_order)
    order_check_id = get_order_check_id(cart_id)
    if total_products and total_price:
        text = 'Ваша корзина 🛒: \n\n'
        i = 0
        for product_name, quantity, final_price, in cart_products:
            i += 1
            text += f'''{i}, {product_name}
        Количество: {quantity}
        Общая сумма: {final_price}\n\n'''
            save_order(order_check_id, product_name, quantity, final_price)

        text += f'''Выбранные продукты: {total_products}
        К оплате: {total_price} сум!'''

        await bot.send_invoice(
            chat_id=chat_id,
            title=f'Заказ №{cart_id}',
            description=text,
            payload='bot_defined invoice payload',
            provider_token=PAYMENT,
            currency='UZS',
            prices=[
                LabeledPrice(label='Общая сумма!', amount=int(total_price * 100)),
                LabeledPrice(label='Доставка', amount=1000000)
            ],
            start_parameter='start_parameter'
        )


@db.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query):
    await bot.answer_pre_checkout_query(pre_checkout_query.id,
                                        ok=True,
                                        error_message='Карта недоступен!🤷‍♂')

@db.message_handler(content_types=['successful_payment'])
async def get_payment(message):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)
    await bot.send_message(chat_id, 'Оплата прошло успешно!👍')
    drop_cart_products_default(cart_id)

@db.message_handler(lambda message: 'История 📜' in message.text)
async def show_history_order(message: Message):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)
    orders_check_info = get_order_check(cart_id)

    for i in orders_check_info:
        text = f'''Дата заказа {i[-1]}
Время Заказа: {i[-2]}
Общая количество: {i[3]}
К оплате: {i[2]}\n\n'''
        detail_order = get_detail_order(i[0])

        for j in detail_order:
            text += f'''Продукт: {j[0]}
Количество: {j[1]}
Общая сумма: {j[2]}\n\n'''
            await bot.send_message(chat_id, text)




executor.start_polling(db)
