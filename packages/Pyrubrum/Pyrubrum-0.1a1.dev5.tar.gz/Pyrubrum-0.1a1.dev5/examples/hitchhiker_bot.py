# Pyrubrum - An intuitive framework for creating Telegram bots
# Copyright (C) 2020 Hearot <https://github.com/hearot>
#
# This file is part of Pyrubrum.
#
# Pyrubrum is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrubrum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrubrum. If not, see <http://www.gnu.org/licenses/>.

from environs import Env
from pyrogram import Client
from pyrogram import InputMediaPhoto

from pyrubrum import Handler
from pyrubrum import Menu
from pyrubrum import transform

answer_image_link = "https://i.imgur.com/ZsDhqqt.png"
forty_two_image_link = "https://i.imgur.com/q0mZf3z.png"


def main(
    api_hash: str,
    api_id: int,
    bot_token: str,
    media_chat_id: int,
    session_name: str,
):
    bot = Client(
        session_name, api_hash=api_hash, api_id=api_id, bot_token=bot_token
    )

    with bot:
        answer_image_id = InputMediaPhoto(
            bot.send_photo(media_chat_id, answer_image_link).photo.file_id
        )
        forty_two_image_id = InputMediaPhoto(
            bot.send_photo(media_chat_id, forty_two_image_link).photo.file_id
        )

    tree = transform(
        {
            Menu("Main", "main", answer_image_id): {
                Menu("🌌 Get the answer", "forty_two", forty_two_image_id),
            }
        }
    )

    handler = Handler(tree)
    handler.setup(bot)

    bot.run()


if __name__ == "__main__":
    env = Env()
    env.read_env()

    api_hash = env("API_HASH")
    api_id = env.int("API_ID")
    bot_token = env("BOT_TOKEN")
    media_chat_id = env.int("MEDIA_CHAT_ID")
    session_name = env("SESSION_NAME")

    main(api_hash, api_id, bot_token, media_chat_id, session_name)
