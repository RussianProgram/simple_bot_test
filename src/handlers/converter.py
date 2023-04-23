import aiohttp

from aiogram import types
from aiogram.dispatcher import FSMContext


from bot import dp
from config import CONVERTER_API_KEY
from forms import CurrencyForm


"""
CURRENCY CONVERT
"""
# Handle the "/convert" command
@dp.message_handler(lambda message: message.text == "Convert currency")
async def create_convert_form(message: types.Message):
    await CurrencyForm.base_currency.set()
    await message.reply("Enter the input currency code (e.g. USD): ")

# Input codes like USD
@dp.message_handler(state=CurrencyForm.base_currency)
async def input_currency_codes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["base_currency"] = message.text.upper()

    await CurrencyForm.next()
    await message.reply("Enter the output currency code (e.g. EUR): ")


@dp.message_handler(state=CurrencyForm.output_currency)
async def input_currency_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["output_currency"] = message.text.upper()

    await CurrencyForm.next()
    await message.reply("Enter the amount to convert: ")


@dp.message_handler(state=CurrencyForm.amount_to_convert)
async def convert_currency(message: types.Message, state: FSMContext):
    amount = message.text

    async with state.proxy() as data:
        input_currency = data["base_currency"]
        output_currency = data["output_currency"]

    await state.finish()
    try:
        # Send a request to the freecurrencyapi API to get the conversion rate
        convert_api = (
            f"https://api.freecurrencyapi.com/v1/latest?apikey={CONVERTER_API_KEY}"
            f"&base_currency={input_currency}"
            f"&currencies={output_currency}"
        )
        async with aiohttp.ClientSession() as session:
            response = await session.get(url=convert_api)
            data = await response.json()

        # Calculate the converted amount and send it to the user
        conversion_rate = data["data"][output_currency]
        converted_amount = float(amount) * conversion_rate
        await message.reply(
            f"{amount} {input_currency} is {converted_amount:.2f} {output_currency}"
        )
    except:
        await message.reply("Error: Invalid input. Please try again.")
