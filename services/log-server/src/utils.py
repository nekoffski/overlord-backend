import os
import datetime
import shutil
import aiofiles


from aiofiles.os import wrap


LOG_DIRECTORY = f'{os.getcwd()}/log'
LOG_FILE = f'{LOG_DIRECTORY}/logs.txt'


copy_file = wrap(shutil.copyfile)


async def clear_file(path: str):
    async with aiofiles.open(path, 'w'):
        pass


async def rotate_log_file():
    current_time = str(datetime.datetime.now()).replace(' ', '_')
    archive_log_file = f'{LOG_DIRECTORY}/{current_time}.txt'

    await copy_file(LOG_FILE, archive_log_file)
    await clear_file(LOG_FILE)


def tail_log_file(file_content: str, lines: int) -> str:
    file_lines = list(filter(lambda x: len(x) > 0, file_content.split('\n')))
    return '\n'.join(file_lines[-lines:])
