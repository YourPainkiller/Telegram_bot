from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bot_keyboards import bot_keyboard1

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
bot_condition = "start"

@dp.message_handler(commands = ["start"])
async def cmd_start(message: types.Message):
    await message.answer("Здарова ебать)))!",reply_markup=bot_keyboard1)

@dp.message_handler(lambda message: message.text == "Узнать курс")
async def check_rate(message: types.Message):
    bot_condition = "checking rate"
    await message.answer("Укажите название криптовалюты")

@dp.message_handler()
async def get_crypto_to_check(msg: types.Message):
    if bot_condition == "checking rate": #Разобраться с тем, как это делать нормально
        await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)