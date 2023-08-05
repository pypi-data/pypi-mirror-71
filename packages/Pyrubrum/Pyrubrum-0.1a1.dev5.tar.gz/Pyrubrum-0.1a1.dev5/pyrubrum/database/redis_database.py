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

from typing import Optional

from .base_database import BaseDatabase
from .base_database import Expire
from .errors import DeleteError
from .errors import ExpireError
from .errors import SetError

try:
    import redis
except (ImportError, ModuleNotFoundError):
    pass


class RedisDatabase(BaseDatabase):
    """Implementation of a database using a Redis server.

    Attributes:
        encoding (Optional[str]): The encoding format which shall be used to
            decode the content that is retrieved from the Redis server.
            Defaults to "utf-8".
        default_expire (Optional[Expire]): The expire which is set by default.
            If it is ``False``, no expire shall be set. Defaults to 86400
            seconds (i.e. a day).
        server (redis.Redis): The Redis instance which is being used.
    """

    encoding: Optional[str] = "utf-8"
    default_expire: Optional[Expire] = 86400
    server: "redis.Redis"

    def __init__(
        self,
        server: "redis.Redis",
        encoding: Optional[str] = "utf-8",
        default_expire: Optional[Expire] = 86400,
    ):
        """Initialize the database.

        Args:
            server (redis.Redis): The Redis instance which is being used.
            encoding (Optional[str]): The encoding format which shall be used
                to decode the content that is retrieved from the Redis server.
                Defaults to "utf-8".
            default_expire (Expire): The expire which is set by default. If it
                is ``False``, no expire shall be set. Defaults to 86400 seconds
                (i.e. a day).
        """
        self.default_expire = default_expire
        self.encoding = encoding
        self.server = server

    def get(self, key: str) -> Optional[str]:
        """Get the value which is stored with a certain key inside the database,
        if any. Otherwise, it will just return ``None``.

        This method will query the key using `redis.Redis.get`.

        Args:
            key (str): The key you are retrieving the value of from the
                Redis database.

        Returns:
            Optional[str]: The value which is associated to the key in the
                database, if any. Otherwise, it is set to be ``None``.
        """
        content = self.server.get(key)
        return content.decode(self.encoding) if content else None

    def set(self, key: str, value: str, expire: Expire = None):
        """Assign a value to a certain key inside the database. If no expire is
        provided, it will automatically provide one from `default_expire`. If
        the expire is set to be ``False``, no expire flag will be assigned.

        This method will assign the provided value to the key using
        `redis.Redis.set` and mark the expire flag with `redis.Redis.expire`.

        Args:
            key (str): The key you are adding or updating the value of.
            value (str): The value which is being assigned to the key.
            expire (Optional[Expire]): The expire in seconds or as a
                `timedelta` object. A key is set not to expire if ``False`` is
                provided for this argument. Defaults to ``None``, which
                automatically provides a default expire from `default_expire`.

        Raises:
            ExpireError: If an error occured while setting the expire for the
                key.
            SetError: If an error occured while inserting the key into the
                database.
        """
        if not self.server.set(key, value):
            raise SetError

        if expire and not self.server.expire(key, expire):
            raise ExpireError
        elif (
            expire is not False
            and self.default_expire
            and not self.server.expire(key, self.default_expire)
        ):
            raise ExpireError

    def delete(self, key: str):
        """Delete a certain key from the database, together with its stored value.

        This method will delete the provided key from the database using
        `redis.Redis.delete`.

        Args:
            key (str): The key which is being deleted from the database,
                together with its linked data.

        Raises:
            DeleteError: If an error occured while deleting the key.
        """
        try:
            self.server.delete(key)
        except redis.RedisError:
            raise DeleteError
