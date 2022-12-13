#https://t.me/CryptoIS_bot - ссылка на бота
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import bold, code, text, italic
import sqlite3

from requests_f import symbol_to_name
from requests_f import name_to_symbol
from requests_f import get_list_of_crypto
from requests_f import get_current_price_of_crypto
from requests_f import best_place_to_buy_or_sell_crypto
from requests_f import check_valid_crypto

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def gen_base():
    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

    #####################################################

    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        sqlite_create_table_query = '''CREATE TABLE users_data (
                                    user_id INTEGER UNIQUE NOT NULL,
                                    crypto text NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")

def insert_value(user_id: int, crypto: str) -> str:
    ret_msg = ""
    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO users_data
                          (user_id, crypto) 
                          VALUES (?, ?);"""

        data_tuple = (user_id, crypto)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")
        ret_msg = "Success"
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        ret_msg = "Failed"
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return ret_msg

def get_crypto_from_id(user_id) -> str:
    try:
        list_of_crypto = ""
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_select_query = """select * from users_data where user_id = ?"""
        cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        for row in records:
            list_of_crypto += row[1]
            # print("Favourite crypto = ", row[1])
        cursor.close()
        return list_of_crypto

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def updateSqliteTable(user_id, crypto) -> str:
    ret_msg = ""
    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_update_query = """Update users_data set crypto = ? where user_id = ?"""
        data = (crypto, user_id)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        ret_msg = "Success"
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
        ret_msg = "Failed"
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The sqlite connection is closed")
    return ret_msg

#Вывести все функции и лист всей крипты
@dp.message_handler(commands = ["start"])
async def cmd_start(message: types.Message):
    msg_text = text("Доброе время суток\nНапишите команду " + bold("/help") + " для получения помощи по работе с ботом")
    await message.answer(msg_text, parse_mode="MarkdownV2")

@dp.message_handler(commands = ["help"])
async def cmd_help(message: types.Message):
    msg_text = text(italic("Команды бота записываются без слэша. Аргументы записываются и перечисляются через пробел\n\n") +
                    bold("list") + " \\- посмотреть список доступной криптовалюты\n\n" +
                    bold("cr") + " \\- узнать курс конкретной валюты по названию\n" +
                    "\tПример:\t" + code("cr bitcoin\n\n") +
                    bold("bp") + " \\- узнать лучшее место для продажи и лучшее место для " +
                                 "покупки конкретной криптовалюты по названию\n\n" +
                    bold("af") + " \\- создать список любимой криптовалюты по названиям\n" +
                    "\tПример:\t" + code("af bitcoin dogecoin ethereum\n\n") +
                    bold("uf") + " \\- обновить список любимой криптовалюты \\(записывает новый вместо имеющегося\\)\n\n" +
                    bold("gf") + " \\- для каждой криптовалюты из списка любимых вывести текущий курс")
    await message.answer(msg_text, parse_mode="MarkdownV2")

"""
Функции:
Лист крипты +
Стоимость крипты по названию
Лучшие места для покупки/продажи по названию
Добавить любимую крипту
Вывести стоимость любимой крипты
Обновить любимую крипту
"""

@dp.message_handler()
async def pseudo_commands_parser(msg: types.Message):
    spl_text = msg.text.split(" ")
    if spl_text[0] == "list":
        msg_text = text("Список доступных криптовалют:\n" + bold(get_list_of_crypto()))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "cr":
        cur_rate = get_current_price_of_crypto(spl_text[1]).split(" ")
        msg_text = ""
        if cur_rate[0] == "Not":
            msg_text = "Криптовалюта не найдена"
        else:
            msg_text = text("Курс " + bold(spl_text[1]) + ":\nТекущая цена: " + bold(cur_rate[0]) +
                            "\nИзменение за 24 часа: " + bold(cur_rate[1]))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "bp":
        bp = best_place_to_buy_or_sell_crypto(spl_text[1])
        msg_text = ""
        if bp[0] == "Not found":
            msg_text = "Криптовалюта не найдена"
        else:
            place_to_sell = bp[0][1]
            rate_to_sell = bp[0][0]
            place_to_buy = bp[1][1]
            rate_to_buy = bp[1][0]
            msg_text = text("Лучшее место для продажи \\- " + bold(place_to_sell) +
                            ": " + code(str(rate_to_sell)) + "\nЛучшее место для покупки \\- " +
                            bold(place_to_buy) + ": " + code(str(rate_to_buy)))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "af":
        fav_cryptos = ""
        for i in range(1, len(spl_text)):
            fav_cryptos += spl_text[i] + " "
        msg_text = ""
        rm = insert_value(msg.from_user.id, fav_cryptos)
        if rm == "Success":
            msg_text = text(italic("Ваша любимая криптовалюта успешно записана"))
        else:
            msg_text = text(italic("У вас уже есть любимая криптовалюта\nПопробуйте изменить список"))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "uf":
        fav_cryptos = ""
        for i in range(1, len(spl_text)):
            fav_cryptos += spl_text[i] + " "
        """
        msg_text = ""
        rm = updateSqliteTable(msg.from_user.id, fav_cryptos)
        if rm == "Success":
            msg_text = text(italic("Список вашей любимой криптовалюты успешно обновлён"))
        else:
            msg_text = text(italic("Не удалось обновить список вашей любимой криптовалюты\n" +
                                   "Видимо, у вас нет списка любимой криптовалюты. Попробуйте создать его"))
        await msg.answer(msg_text, parse_mode="MarkdownV2")
        """
        rm = updateSqliteTable(msg.from_user.id, fav_cryptos)
        msg_text = text(italic("Список вашей любимой криптовалюты успешно обновлён"))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "gf":
        fav_cryptos = get_crypto_from_id(msg.from_user.id).split(" ")
        if fav_cryptos[-1] == "":
            fav_cryptos.pop(-1)
        msg_text = text(bold("Ваша любимая криптовалюта:\n"))
        for i in range(len(fav_cryptos)):
            cur_rate = get_current_price_of_crypto(fav_cryptos[i]).split(" ")
            if cur_rate[0] == "Not":
                msg_text += text(bold(fav_cryptos[i]) + ":\nКриптовалюта не найдена\n")
            else:
                msg_text += text("Курс " + bold(fav_cryptos[i]) + ":\nТекущая цена: " + bold(cur_rate[0]) +
                                "\nИзменение за 24 часа: " + bold(cur_rate[1]) + "\n")
        await msg.answer(msg_text, parse_mode="MarkdownV2")

if __name__ == '__main__':
    gen_base()
    symbol_from_name = name_to_symbol()
    name_from_symbol = symbol_to_name()
    executor.start_polling(dp)
