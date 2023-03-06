from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
                          KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_seller = InlineKeyboardButton("Become a seller", callback_data="seller")
inline_buyer = InlineKeyboardButton("Become a buyer", callback_data="buyer")

inline_start_registration = InlineKeyboardMarkup(row_width=1, resize_keyboard=True,
                                                 one_time_keyboard=True)
inline_start_registration.add(inline_seller, inline_buyer)

keyboard_telegram = KeyboardButton("Telegram")
keyboard_youtube = KeyboardButton("YouTube")
keyboard_instagram = KeyboardButton("Instagram")
keyboard_facebook = KeyboardButton("Facebook")

keyboard_network = InlineKeyboardMarkup()
keyboard_network.add(keyboard_youtube, keyboard_instagram, keyboard_telegram, keyboard_facebook)
