import inline_keyboard
import json_functions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import TOKEN


import variables_managment
import classes
import functions
# -------------------------------------------

# -------------------------------------------
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# -------------------------------------------



@dp.message_handler(text=['/start'])
async def get_start_message(message: types.Message):
    if message.from_user.id not in variables_managment.users_id:
        variables_managment.users_id.append(message.from_user.id)
        variables_managment.users_role[message.from_user.id] = 0

        json_functions.convert_to_json(variables_managment.users_role, "users_role")
        json_functions.convert_to_json(variables_managment.users_id, "users_id")

        await bot.send_message(message.from_user.id, "Hi! Nice to meet you) You need to registrate. "
                                                     "Select the role, which you want to choose",
                               reply_markup=inline_keyboard.inline_start_registration)
    else:
        await bot.send_message(message.from_user.id, "My functions:")


@dp.message_handler(state=classes.Answer.message_age_interval)
async def get_age_interval(message: types.Message, state: FSMContext):
    text = message.text
    age_interval = functions.read_age_interval(text)
    if age_interval == "0":
        await bot.send_message(message.from_user.id, "Incorrect input")
        await classes.Answer.message_age_interval.set()
    else:
        users_registration_form = json_functions.read_json("users_registration_form")
        users_registration_form[message.from_user.id].append(age_interval)
        json_functions.convert_to_json(users_registration_form, "users_registration_form")
        await bot.send_message(message.from_user.id, "Write how many percentage do you have Man. Write only number")
        await state.finish()
        await classes.Answer.message_sex_stats()



@dp.message_handler(state=classes.Answer.message_country)
async def get_country(message: types.Message, state: FSMContext):
    text = message.text
    countries = functions.read_countries(text)
    if len(countries) == 0:
        await bot.send_message(message.from_user.id, "Incorrect input")
        await classes.Answer.message_country.set()
    else:
        users_registration_form = json_functions.read_json("users_registration_form")
        users_registration_form[message.from_user.id].appedn(countries)
        json_functions.convert_to_json(users_registration_form, "users_registration_form")
        await state.finish()
        await bot.send_message(message.from_user.id, "Write age interval of your target audience (e.g. 18-24)")
        await classes.Answer.message_age_interval.set()


@dp.message_handler(state=classes.Answer.message_stats)
async def get_stats(message: types.Message, state: FSMContext):
    text = message.text
    if not functions.check_number(text):
        await bot.send_message(message.from_user.id, "Wrong amount. "
                                                     "Write amount without any other symbols. Only digits")
        await classes.Answer.message_stats.set()
    else:
        users_registration_form = json_functions.read_json("users_registration_form")
        users_registration_form[message.from_user.id].append(int(text))
        json_functions.convert_to_json(users_registration_form, "users_registration_form")
        await bot.send_message(message.from_user.id, "Write down the countries where your target audience is from ")
        await state.finish()
        await classes.Answer.message_country.set()

@dp.message_handler(state=classes.Answer.message_subscribers)
async def get_subscribers(message: types.Message, state: FSMContext):
    text = message.text
    if not functions.check_number(text):
        await bot.send_message(message.from_user.id, "Wrong amount. "
                                                     "Write amount without any other symbols. Only digits")
        await classes.Answer.message_subscribers.set()
    else:
        users_registration_form = json_functions.read_json("users_registration_form")
        users_registration_form[message.from_user.id].append(int(text))
        if users_registration_form[message.from_user.id][1] == "youtube":
            await bot.send_message(message.from_user.id, "Enter average views for the last 3 videos "
                                                         "( total views of 3 videos divide 3 ). "
                                                         "Write this amount just number")
            await classes.Answer.message_stats.set()
        elif users_registration_form[message.from_user.id][1] == "instagram":
            await bot.send_message(message.from_user.id, "Enter average coverage for the last month"
                                                         "Write this amount just number")

            await classes.Answer.message_stats.set()
        elif users_registration_form[message.from_user.id][1] == "telegram":
            await bot.send_message(message.from_user.id, "Enter average amount of views on publication"
                                                         "Write this amount just number")

            await classes.Answer.message_stats.set()
        elif users_registration_form[message.from_user.id][1] == "facebook":
            await bot.send_message(message.from_user.id, "Enter average coverage for the last month"
                                                         "Write this amount just number")

            await classes.Answer.message_stats.set()

        json_functions.convert_to_json(users_registration_form, "users_registration_form")




@dp.message_handler(state=classes.Answer.message_link)
async def get_link(message: types.Message, state: FSMContext):
    text = message.text
    if not functions.check_link(text):
        await bot.send_message(message.from_user.id, "Wrong link. Try again")
        await classes.Answer.message_link.set()
    else:
        await bot.send_message(message.from_user.id, "How many subscriber do you have? Please write full amount")
        users_registration_form = json_functions.read_json("users_registration_form")
        users_registration_form[message.from_user.id].append(text)
        json_functions.convert_to_json(users_registration_form, "users_registration_form")
        await state.finish()
        await classes.Answer.message_subscribers()


@dp.message_handler(state=classes.Answer.message_network)
async def get_network(message: types.Message, state: FSMContext):
    text = message.text.lower()

    if text in variables_managment.networks:
        # add network by user_id
        await bot.send_message(message.from_user.id, "Send link on your account")

        users_registration_form = json_functions.read_json("users_registration_form")
        users_registration_form[message.from_user.id].append(text)
        json_functions.convert_to_json(users_registration_form, "users_registration_form")

        await state.finish()
        await classes.Answer.message_link.set()

    else:
        await bot.send_message(message.from_user.id, "Unknown network, try again",
                               reply_markup=inline_keyboard.keyboard_network)
        await classes.Answer.message_network.set()


@dp.callback_query_handler(lambda c: c.data)
async def get_callback(callback_query: types.CallbackQuery):
    cb_data = callback_query.data
    user_id = callback_query.from_user.id

    users_registration_form = json_functions.read_json("users_registration_form")

    await bot.delete_message(user_id, message_id=callback_query.message.message_id)

    if cb_data == "buyer":
        users_registration_form[user_id].append("2")
    if cb_data == "seller":
        users_registration_form[user_id].append("1")

    json_functions.convert_to_json(users_registration_form, "users_registration_form")
    await bot.send_message(user_id, "Select network", reply_markup=inline_keyboard.keyboard_network)




if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
