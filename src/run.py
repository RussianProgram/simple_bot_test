from aiogram.utils import executor

from bot import dp
from handlers import base, weather, poll, converter

# docker build -t bot:test .
# docker run --name bot bot:test
# docker stop bot
# docker start bot

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
