from datetime import datetime, timedelta
from typing import Optional


class Id:
    def __init__(
        self,
        time: Optional[datetime | int] = None,
        timezone_offset: Optional[timedelta | int] = timedelta(hours=0),
        channel_id: Optional[int] = None,
        channel_name: Optional[str] = None,
        message_id: Optional[int] = None,
        bot_id: Optional[int] = None,
        bot_name: Optional[str] = None,
        device_id: Optional[int] = None,
        device_name: Optional[str] = None,
    ):
        self.time = datetime.now() if time is None else time
        self.timezone_offset = timezone_offset
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.message_id = message_id
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.device_id = device_id
        self.device_name = device_name

    @property
    def time(self) -> datetime:
        return self.__time

    @time.setter
    def time(self, value):
        if isinstance(value, datetime):
            self.__time = value
        elif isinstance(value, int):
            self.__time = datetime.fromtimestamp(value)
        else:
            raise ValueError("Invalid type for 'time'. Expected datetime or int.")

    @property
    def timezone_offset(self) -> timedelta:
        return self.__timezone_offset

    @timezone_offset.setter
    def timezone_offset(self, value):
        if isinstance(value, timedelta):
            self.__timezone_offset = value
        elif isinstance(value, int):
            self.__timezone_offset = timedelta(seconds=value)
        else:
            raise ValueError("Invalid type for 'timezone_offset'. Expected timedelta or int.")

    def __str__(self):
        return (
            f"  time: {self.time}\n"
            f"  timezone_offset: {self.timezone_offset}\n"
            f"  channel_id: {self.channel_id}\n"
            f"  channel_name: {self.channel_name}\n"
            f"  message_id: {self.message_id}\n"
            f"  bot_id: {self.bot_id}\n"
            f"  bot_name: {self.bot_name}\n"
            f"  device_id: {self.device_id}\n"
            f"  device_name: {self.device_name}\n"
        )
