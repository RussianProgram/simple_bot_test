from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import dp
from forms import PollForm


"""
POLL
"""
# Handle the poll command
@dp.message_handler(lambda message: message.text == "Create poll")
async def create_poll_form(message: types.Message):
    # Ask the user for the poll question
    await PollForm.question.set()
    await message.reply("Enter the poll question: ")


@dp.message_handler(state=PollForm.question)
async def set_poll_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = message.text
        data["options"] = []

    await PollForm.next()
    await message.reply("Enter a poll option or type 'done' to finish: ")


@dp.message_handler(state=PollForm.option)
async def get_poll_option(message: types.Message, state: FSMContext):
    option = message.text
    if option.lower() == "done":
        await finish_poll_form(message, state)

    else:
        async with state.proxy() as data:
            data["options"].append(option)

        await message.reply("Enter a poll option or type 'done' to finish: ")


async def finish_poll_form(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        question = data["question"]
        options = data["options"]

    # Create the poll and send it to the chat
    await state.finish()
    await message.answer_poll(question=question, options=options, is_anonymous=False)
