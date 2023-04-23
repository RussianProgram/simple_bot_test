import logging
import requests

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot import dp


# Start command handler
@dp.message_handler(commands=["start"])
async def start_command_handler(message: types.Message):
    """Handle the /start command"""
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_markup.add(types.KeyboardButton("Get weather"))
    keyboard_markup.add(types.KeyboardButton("Convert currency"))
    keyboard_markup.add(types.KeyboardButton("Cute animal pic"))
    keyboard_markup.add(types.KeyboardButton("Create poll"))
    keyboard_markup.add(types.KeyboardButton("Cancel"))
    await message.answer(
        "Hi there! What would you like me to do?", reply_markup=keyboard_markup
    )


# Cancel form input
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    # Cancel state and inform user about it
    await state.finish()

    # And remove keyboard (just in case)
    await message.reply("Cancelled.")


"""
ANIMALS
"""
# Handle the "/animal" command
@dp.message_handler(lambda message: message.text == "Cute animal pic")
async def random_animal(message: types.Message):
    # Send a request to the random animal picture API to get a random picture URL
    url = "https://some-random-api.ml/animal/cat"
    response = requests.get(url)
    data = response.json()
    animal_url = data["image"]

    # Send the picture to the user
    await message.answer_photo(animal_url)

