# -*- coding: utf-8 -*-
import asyncio
import threading
import functions
import inline_keyboard
import json_functions
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from classes import Answer
from config import TOKEN

# ----------------------------------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# ----------------------------------------------------
# list of user_id we will save in .json
if os.stat("users_id.json").st_size != 0:
    users_id = json_functions.read_json("users_id")
else:
    users_id = []
    json_functions.list_to_json(users_id, "users_id")

# ----------------------------------------------------
# dict { user_id : {portfolio} } also we will save in .json

if os.stat("user_portfolio.json").st_size != 0:
    print("user_portfolio.json isn't empty")
    user_portfolio = json_functions.read_json("user_portfolio")
    # print(type(user_portfolio))
else:
    user_portfolio = {}
    for user_id in users_id:
        user_portfolio[str(user_id)] = {}
    json_functions.list_to_json(user_portfolio, "user_portfolio")
    print(user_portfolio)

# ----------------------------------------------------
# list of valid products
if os.stat("products.json").st_size != 0:
    products = json_functions.read_json("products")
else:
    products = []
    json_functions.list_to_json(products, "products")
# ----------------------------------------------------
if os.stat("user_watchlist.json").st_size != 0:
    user_watchlist = json_functions.read_json("user_watchlist")
else:
    user_watchlist = {}

# ----------------------------------------------------
if os.stat("user_watchlist.json").st_size != 0:
    user_signal = json_functions.read_json("user_watchlist")
else:
    user_signal = {}
    for user in users_id:
        user_signal[user] = []
# ----------------------------------------------------


async def send_signal(user_id, price, product, reached_price):
    print("send_signal")
    await bot.send_message(user_id, f"Price for {product} reached border: {price}."
                                    f"Border price: {reached_price}")


async def check_signal():
    user_signal = json_functions.read_json("user_signal")
    users_id = user_signal.keys()
    products = json_functions.read_json("products")

    for item in products:
        price = functions.get_price(item)
        print(f"check: price {price}")
        for user in users_id:
            for signal_list in user_signal[user]:
                print(signal_list)
                print(signal_list[0].upper())
                if item.upper() == signal_list[0].upper():
                    print("lol")
                    if price >= float(signal_list[2]):
                        print("high")
                        await send_signal(user, round(price, 2), item.upper(), signal_list[2])

                    if price <= float(signal_list[1]):
                        print("low")
                        await send_signal(user, round(price, 2), item.upper(), signal_list[1])

    print("check signal")

# ----------------------------------------------------


@dp.message_handler(text=["/start", "/functions"])
async def start_help_message(message: types.Message):

    if message.from_user.id not in users_id:
        users_id.append(message.from_user.id)
        user_portfolio[str(message.from_user.id)] = {}
        print(f"check2 {user_portfolio}")
        user_watchlist[str(message.from_user.id)] = []
        user_signal[str(message.from_user.id)] = []

        json_functions.list_to_json(user_portfolio, "user_portfolio")
        json_functions.list_to_json(users_id, "users_id")
        json_functions.list_to_json(user_watchlist, "user_watchlist")
        json_functions.list_to_json(user_signal, "user_signal")

        await bot.send_message(message.from_user.id, "Hello! Nice to meet you. My functions: ",
                               reply_markup=inline_keyboard.inline_commands)
    else:

        await bot.send_message(message.from_user.id, "My functions: ",
                               reply_markup=inline_keyboard.inline_commands)

@dp.callback_query_handler(lambda c: c.data)
async def get_callback(callback_query: types.CallbackQuery):
    cb_data = callback_query.data
    user_id = callback_query.from_user.id

    await bot.delete_message(user_id, message_id=callback_query.message.message_id)

    if cb_data == "balance":

        current_balance = functions.get_current_balance(user_id)
        real_balance = functions.get_real_balance(user_id)

        if current_balance >= 0 and real_balance >= 0:
            if real_balance == 0 and current_balance > 0:
                await bot.send_message(user_id, f"Your profit: +{current_balance}")
            elif current_balance == 0:
                await bot.send_message(user_id, f"Your balance: {real_balance}$\n")
            else:
                delta = round((current_balance/real_balance) * 100, 2)
                print(delta)
                delta_symbol = ""
                if delta > 100:
                    delta -= 100
                    delta_symbol = '+'
                else:
                    delta -= 100
                await bot.send_message(user_id,
                                       f"Your balance is: {round(current_balance, 3)}\nBalance changing:\n"
                                       f"{delta_symbol}{round(delta, 2)}%:"
                                       f" {delta_symbol}{round((current_balance - real_balance), 2)}")
        else:
            await bot.send_message(user_id, f"Your balance is: {current_balance}$\n")

    elif cb_data == "transaction":
        await bot.send_message(user_id,
                               "Enter product code, (+/-)amount and price for 1(e.g. AAPL 10 120 )")
        await Answer.message_transaction.set()
    elif cb_data == "watchlist":
        await bot.send_message(user_id, "Enter code of product or products, which you want to add to your Watchlist(e.g. TSLA AAPL ...)")
        await Answer.message_watchlist.set()
    elif cb_data == "signal":
        await bot.send_message(user_id, "Enter product code, lower и higher cost boundary"
                                        ", about which you want to receive signals(e.g. ```AAPL 100 150```)")
        await Answer.message_signal.set()


@dp.message_handler(state=Answer.message_transaction)
async def get_message_transaction(message: types.Message, state: FSMContext):
    check = functions.check_input_transaction(message.text)

    if type(check) == int:
        error_message = ""
        if check == -1:
            error_message = "Incorrect input, try again."
        elif check == -2:
            error_message = "Incorrect product code. This product doesn't exist. Try again"
        elif check == -3:
            error_message = "Incorrect amount. Try again"
        elif check == -4:
            error_message = "Incorrect price. Try again"

        await bot.send_message(message.from_user.id, error_message)
        await Answer.message_transaction.set()
    else:
        transaction_status = functions.add_transaction(message.from_user.id, check[0], check[1], check[2])
        if transaction_status == -1:
            await bot.send_message(message.from_user.id, "You want to sell more, than you have. Try again")
            await Answer.message_transaction.set()
        elif transaction_status == -2:
            await bot.send_message(message.from_user.id, "Error of adding to DataBase. Try again")
            await Answer.message_transaction.set()
        else:
            await bot.send_message(message.from_user.id, "Successful transaction!")
            await state.finish()


@dp.message_handler(state=Answer.message_watchlist)
async def get_message_watchlist(message: types.Message, state: FSMContext):
    watchlist = message.text
    watchlist = watchlist.split(" ")
    for item in watchlist:
        if item == " ":
            watchlist.remove(item)
        user_watchlist[str(message.from_user.id)].append(item)
    json_functions.list_to_json(user_watchlist, "user_watchlist")
    await bot.send_message(message.from_user.id, "Items were successfully added to your watchlist!")
    await state.finish()

@dp.message_handler(state=Answer.message_signal)
async def get_message_signal(message: types.Message, state: FSMContext):
    check = functions.check_input_signal(message.text)
    if type(check) == int:
        error_message = ""
        if check == -1:
            error_message = "Incorrect input, try again."
        elif check == -2:
            error_message = "Incorrect product code. This product doesn't exist. Try again"
        elif check == -3:
            error_message = "Min price can't be more than max price"
        await bot.send_message(message.from_user.id, error_message)
        await Answer.message_signal.set()
    else:
        user_signal[str(message.from_user.id)].append([check[0], check[1], check[2]])
        json_functions.list_to_json(user_signal, "user_signal")
        await bot.send_message(message.from_user.id, "Signal was successfully added!")
        await state.finish()


async def run_bot():
    await executor.start_polling(dp, skip_updates=True)


async def schedule_check_signals():
    while True:
        await asyncio.sleep(300)
        asyncio.create_task(check_signal())


async def run_check_signals():
    asyncio.create_task(schedule_check_signals())


if __name__ == '__main__':
    signal_thread = threading.Thread(target=asyncio.run, args=(run_check_signals(),))
    signal_thread.start()
    executor.start_polling(dp, skip_updates=True)
