from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import bold, code, text, italic, link
import sqlite3
from links_to_coins import coins, exch

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
    """Функция, которая генерирует базу данных 'Crypto_base.db' с двумя ячейками: user_id, crypto.
    На вход ничего не принимает.
    Ничего не возвращает"""
    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("Base Version", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("connection is closed")

    #####################################################

    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        sqlite_create_table_query = '''CREATE TABLE users_data (
                                    user_id INTEGER UNIQUE NOT NULL,
                                    crypto text NOT NULL);'''

        cursor = sqliteConnection.cursor()
        print("connected")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("table created")
        cursor.close()

    except sqlite3.Error as error:
        print("Error", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("connection is closed")

def insert_value(user_id: int, crypto: str) -> str:
    """Функция вставляет в базу данных две ячейки: user_id, crypto.
    На вход принимает user_id и строку из любимой криптовалюты.
    return string"""
    ret_msg = ""
    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected")

        sqlite_insert_with_param = """INSERT INTO users_data
                          (user_id, crypto) 
                          VALUES (?, ?);"""

        data_tuple = (user_id, crypto)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("inserted successfully")
        ret_msg = "Success"
        cursor.close()

    except sqlite3.Error as error:
        print("Failed", error)
        ret_msg = "Failed"
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("connection is closed")
    return ret_msg

def get_crypto_from_id(user_id) -> str:
    """Функция получает из ячейки базы данных user_id[user_id] список любимой криптовалюты и возвращает его.
    На вход получает user_id.
    return string"""
    try:
        list_of_crypto = ""
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected")

        sql_select_query = """select * from users_data where user_id = ?"""
        cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        for row in records:
            list_of_crypto += row[1]
            # print("Favourite crypto = ", row[1])
        cursor.close()
        return list_of_crypto

    except sqlite3.Error as error:
        print("Failed", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("connection is closed")

def updateSqliteTable(user_id, crypto) -> str:
    """Функция обновляет ячейку user_id базы данных новым списком любимой криптовалюты crypto.
    На вход принимает user_id и список любимой криптовалюты.
    return string"""
    ret_msg = ""
    try:
        sqliteConnection = sqlite3.connect('Crypto_base.db')
        cursor = sqliteConnection.cursor()
        print("Connected")

        cursor.execute("SELECT crypto FROM users_data WHERE user_id = ?", (user_id,))
        check_data = cursor.fetchone()
        if check_data is None:
            ret_msg = "Not found"
        else:
            ret_msg = "Success"

        sql_update_query = """Update users_data set crypto = ? where user_id = ?"""
        data = (crypto, user_id)
        cursor.execute(sql_update_query, data)
        sqliteConnection.commit()
        print("Record Updated successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update", error)
        ret_msg = "Failed"
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The sqlite connection is closed")
    return ret_msg


@dp.message_handler(commands = ["start"])
async def cmd_start(message: types.Message):
    """Бот отвечает приветствием на команду /start"""
    msg_text = text("Доброе время суток\nНапишите команду " + bold("/help") + " для получения помощи по работе с ботом")
    await message.answer(msg_text, parse_mode="MarkdownV2")

@dp.message_handler(commands = ["help"])
async def cmd_help(message: types.Message):
    """Бот отвечает на команду /help списком доступных функций бота"""
    msg_text = text(italic("Команды бота записываются без слэша. Аргументы записываются и перечисляются через пробел\n\n") +
                    bold("list") + " \\- посмотреть список доступной криптовалюты\\. " +
                                   "Возможна фильтрация по первой букве\n" +
                    "\tПример 1:\t" + code("list") +
                    "\n\tПример 2:\t" + code("list b\n\n") +
                    bold("cr") + " \\- узнать курс конкретной валюты по названию\n" +
                    "\tПример:\t" + code("cr bitcoin\n\n") +
                    bold("bp") + " \\- узнать n лучших мест для покупки и n лучших мест для продажи криптовалюты\n" +
                    "\tПример:\t" + code("bp btc 5\n\n") +
                    bold("af") + " \\- создать список любимой криптовалюты по названиям\n" +
                    "\tПример:\t" + code("af bitcoin dogecoin ethereum\n\n") +
                    bold("uf") + " \\- обновить список любимой криптовалюты \\(записывает новый вместо имеющегося\\)\n\n" +
                    bold("gf") + " \\- для каждой криптовалюты из списка любимых вывести текущий курс")
    await message.answer(msg_text, parse_mode="MarkdownV2")

@dp.message_handler()
async def pseudo_commands_parser(msg: types.Message):
    """Бот обрабатывает все сообщения на наличие в них команд и если они присутствуют, то выполняет их"""
    spl_text = msg.text.split(" ")
    if spl_text[0] == "list":
        filter_flag = True
        if len(spl_text) == 1:
            filter_flag = False
            first_char = "#"
        else:
            first_char = spl_text[1].lower()
        if len(first_char) > 1:
            await msg.answer(text(italic("После команды list должно быть записано не более одной первой буквы")),
                             parse_mode="MarkdownV2")
        else:
            msg_text = text("Список доступных криптовалют:\n")
            list_of_crypto = get_list_of_crypto().split("\n")
            list_of_crypto.pop(-1)
            flag = True
            for i in range(len(list_of_crypto)):
                crypto = list_of_crypto[i].split(" ")[0]
                if not filter_flag or crypto[0] == first_char:
                    crypto_symbol = list_of_crypto[i].split(" ")[1]
                    msg_text += text(link(crypto, coins.get(crypto, "https://www.google.com/")) + " " + bold(crypto_symbol) + "\n")
                    if i == len(list_of_crypto) // 2 and flag:
                        await msg.answer(msg_text, parse_mode="MarkdownV2")
                        msg_text = ""
                        flag = False
            await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "cr":
        crypto = spl_text[1].lower()
        if crypto in name_from_symbol:
            crypto = name_from_symbol[crypto]
        cur_rate = get_current_price_of_crypto(crypto).split(" ")
        msg_text = ""
        if cur_rate[0] == "Not":
            msg_text = "Криптовалюта не найдена"
        else:
            msg_text = text("Курс " + bold(crypto) + ":\nТекущая цена: " + bold('{:.5f}'.format(float(cur_rate[0]))) +
                            "\nИзменение за 24 часа: " + bold('{:.5f}'.format(float(cur_rate[1]))))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "bp":
        crypto = spl_text[1].lower()
        if len(spl_text) != 3:
            await msg.answer(text(italic("У данной команды должно быть 2 аргумента")), parse_mode="MarkdownV2")
        elif not spl_text[2].isdigit():
            await msg.answer(text(italic("Второй аргумент должен быть числом")), parse_mode="MarkdownV2")
        else:
            num = int(spl_text[2])
            if check_valid_crypto(crypto, symbol_from_name, name_from_symbol):
                if crypto in name_from_symbol:
                    crypto = name_from_symbol[crypto]
                bp = best_place_to_buy_or_sell_crypto(crypto)
                msg_text = text(bold(crypto + ":\n\tПокупка:\n"))
                for i in range(num):
                    if i == len(bp):
                        break
                    msg_text += text("\t\t" + link(bp[i][0], exch.get(bp[i][0], "https://www.google.com/")) + ": " +
                                     code('{:.5f}'.format(float(bp[i][1]))) + "\n")
                msg_text += text(bold("\tПродажа:\n"))
                for i in range(num):
                    if i == len(bp):
                        break
                    msg_text += text("\t\t" +
                        link(bp[len(bp) - i - 1][0], exch.get(bp[len(bp) - i - 1][0], "https://www.google.com/"))
                        + ": " + code('{:.5f}'.format(float(bp[len(bp) - i - 1][1]))) + "\n")
                await msg.answer(msg_text, parse_mode="MarkdownV2")
            else:
                msg_text = text(italic("Криптовалюта не найдена"))
                await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "af":
        fav_cryptos = ""
        spl_text.pop(0)
        if len(spl_text) == 0:
            await msg.answer(text(italic("В списке должна быть криптовалюта")), parse_mode="MarkdownV2")
        else:
            for i in range(len(spl_text)):
                spl_text[i] = spl_text[i].lower()
                if spl_text[i] in name_from_symbol:
                    spl_text[i] = name_from_symbol[spl_text[i]]
            spl_text = list(set(spl_text))
            for i in range(len(spl_text)):
                fav_cryptos += spl_text[i].lower() + " "
            msg_text = ""

            correct_crypto = True
            for i in range(len(spl_text)):
                if not check_valid_crypto(spl_text[i], symbol_from_name, name_from_symbol):
                    correct_crypto = False
                    break
            if correct_crypto:
                rm = insert_value(msg.from_user.id, fav_cryptos.lower())
                if rm == "Success":
                    msg_text = text(italic("Ваша любимая криптовалюта успешно записана"))
                else:
                    msg_text = text(italic("У вас уже есть любимая криптовалюта\nПопробуйте изменить список"))
                await msg.answer(msg_text, parse_mode="MarkdownV2")
            else:
                msg_text = text(italic("Среди списка криптовалюты есть некорректные значения"))
                await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "uf":
        fav_cryptos = ""
        spl_text.pop(0)
        if len(spl_text) == 0:
            await msg.answer(text(italic("В списке должна быть криптовалюта")), parse_mode="MarkdownV2")
        else:
            for i in range(len(spl_text)):
                spl_text[i] = spl_text[i].lower()
                if spl_text[i] in name_from_symbol:
                    spl_text[i] = name_from_symbol[spl_text[i]]
            spl_text = list(set(spl_text))
            for i in range(len(spl_text)):
                fav_cryptos += spl_text[i].lower() + " "
            msg_text = ""
            correct_crypto = True
            for i in range(len(spl_text)):
                if not check_valid_crypto(spl_text[i].lower(), symbol_from_name, name_from_symbol):
                    correct_crypto = False
                    break
            if correct_crypto:
                rm = updateSqliteTable(msg.from_user.id, fav_cryptos)
                if rm == "Success":
                    msg_text = text(italic("Список вашей любимой криптовалюты успешно обновлён"))
                elif rm == "Not found":
                    msg_text = text(italic("Не удалось обновить список вашей любимой криптовалюты\n" +
                                           "Видимо, у вас нет списка любимой криптовалюты. Попробуйте создать его"))
                else:
                    msg_text = text(italic("Произошла обшибка при обращении к базе данных"))
                await msg.answer(msg_text, parse_mode="MarkdownV2")
            else:
                msg_text = text(italic("Среди списка криптовалюты есть некорректные значения"))
                await msg.answer(msg_text, parse_mode="MarkdownV2")

    elif spl_text[0] == "gf":
        fav_cryptos = get_crypto_from_id(msg.from_user.id).split(" ")
        if fav_cryptos[-1] == "":
            fav_cryptos.pop(-1)
        msg_text = ""
        if len(fav_cryptos) == 0:
            msg_text = text(italic("Судя по всему у вас нет списка любимой криптовалюты.\n" +
                                   "Попробуйте его создать"))
        else:
            msg_text = text(bold("Ваша любимая криптовалюта:\n"))
            for i in range(len(fav_cryptos)):
                cur_rate = get_current_price_of_crypto(fav_cryptos[i]).split(" ")
                if cur_rate[0] == "Not":
                    msg_text += text(bold(fav_cryptos[i]) + ":\nКриптовалюта не найдена\n")
                else:
                    msg_text += text("Курс " + bold(fav_cryptos[i]) + ":\nТекущая цена: " +
                                     bold('{:.5f}'.format(float(cur_rate[0]))) +
                                    "\nИзменение за 24 часа: " + bold('{:.5f}'.format(float(cur_rate[1]))) + "\n")
        await msg.answer(msg_text, parse_mode="MarkdownV2")

    else:
        msg_text = text(italic("Извините, я не понимаю, что вы от меня хотите..."+
                               "\nДля помощи введите команду ") + bold("/help"))
        await msg.answer(msg_text, parse_mode="MarkdownV2")

if __name__ == '__main__':
    gen_base()
    symbol_from_name = name_to_symbol()
    name_from_symbol = symbol_to_name()
    executor.start_polling(dp)
