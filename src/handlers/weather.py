import logging
import aiohttp

from aiogram import types
from aiogram.dispatcher import FSMContext

from datetime import datetime

from bot import dp
from forms import WeatherForm


"""
WEATHER
"""
# Get weather command handler
@dp.message_handler(lambda message: message.text == "Get weather")
async def create_weather_form(message: types.Message):
    """Handle the 'Get weather' command"""
    try:
        # Get city name from user input
        await WeatherForm.latitude.set()
        await message.answer("Please enter the latitude:")

    except Exception as e:
        logging.error(e)
        await message.answer(
            "Sorry, I couldn't retrieve the weather information. Please try again later."
        )

# Input latitude and longitude
@dp.message_handler(state=WeatherForm.latitude)
async def longitude_form(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["latutide"] = message.text

    await WeatherForm.next()
    await message.answer("Please enter the longitude:")


# 55.75, 37.62
# Get weather command handler
@dp.message_handler(state=WeatherForm.longitude)
async def get_weather_command_handler(message: types.Message, state: FSMContext):
    """Handle the 'Get weather' command"""
    try:
        # Get city name from user input
        async with state.proxy() as data:
            lat = data["latutide"]
            long = message.text

        # Call open-meteo API to get weather data
        weather_api = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
        await state.finish()

        async with aiohttp.ClientSession() as session:
            response = await session.get(url=weather_api)
            data = await response.json()

        # Extract relevant weather information
        current_weather = data["current_weather"]
        temperature = current_weather["temperature"]
        windspeed = current_weather["windspeed"]

        time = datetime.fromisoformat(current_weather["time"])

        # Format and send weather information to user
        weather_info = f"Temperature of {temperature} \nWindspeed is {windspeed} \nDateTime is {time}"
        await message.answer(weather_info)

    except Exception as e:
        logging.error(e)
        await message.answer(
            "Sorry, I couldn't retrieve the weather information. Please try again later."
        )
