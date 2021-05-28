import datetime


class SystemInfo:
    """ A class to return system info """
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        if now.minute == 0:
            answer = f'The time is {now.hour}'
        else:
            answer = f'The time is {now.hour} {now.minute}'
        return answer