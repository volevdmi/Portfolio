from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
                          KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

inline_balance = InlineKeyboardButton("Balance", callback_data="balance")
inline_transaction = InlineKeyboardButton("Add transaction", callback_data="transaction")
inline_watchlist = InlineKeyboardButton("Add to watchlist", callback_data="watchlist")
inline_signal = InlineKeyboardButton("Add signal", callback_data="signal")

inline_commands = InlineKeyboardMarkup(row_width=1,  resize_keyboard=True, one_time_keyboard=True)
inline_commands.add(inline_balance, inline_transaction, inline_watchlist, inline_signal)


empty_markup = InlineKeyboardMarkup().row()

