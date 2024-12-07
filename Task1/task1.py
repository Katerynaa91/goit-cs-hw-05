import sys
import argparse
import asyncio
import aiopath
import aioshutil
import logging

# Скрипт для парсингу аргументів командного рядка
parser = argparse.ArgumentParser(description="The names of source and destination folders to copy files")
parser.add_argument("-f", "--from", required=True, help="Sorce directory")
parser.add_argument("-t", "--to", help="Destination directory", default="Dest_dir")
args = vars(parser.parse_args())

src_dir = aiopath.AsyncPath(args["from"])
dst_dir = aiopath.AsyncPath(args["to"])


async def read_folder(path: aiopath.AsyncPath):
    """Функція для рекурсивного обходу каталогу та його підкаталогів для знаходження 
    усіх розміщених у них файлів та подальшого копіювання цих файлів"""
    async for file in path.iterdir():
        if await file.is_dir():
            await read_folder(file)
        else:
            await copy_file(file)


async def copy_file(file: aiopath.AsyncPath):
    """Функція для копіювання файлів з вихідної директорії до директорії призначення.
    Включає:
    - створення директорії призначення, якщо не передана в аргументах командного рядка,
    та піддиректорій у ній з назвами, що відповідають розширенням файлів.
    - копіювання файлів за допомогою модуля aioshutil - асинхронного аналога модуля shutil"""
    folder = dst_dir / file.suffix[1:]
    try:
        await folder.mkdir(parents=True, exist_ok=True)
        await aioshutil.copyfile(file, folder / file.name)
    except OSError as e:
        logging.error(e)

def create_log(logfile):
    """Функція для логування"""
    format = "%(asctime)s %(levelname)s: %(message)s"
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(logfile, mode="a")
    console_handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    handlers = [file_handler, console_handler]
    logging.basicConfig(format=format, level=logging.INFO, 
                        datefmt="%H:%M:%S", handlers=handlers)
    

if __name__ == "__main__":
    
    create_log("logs.log")
    
    try:
        asyncio.run(read_folder(src_dir))
        logging.info(f"Files copied from directory '{src_dir}' to '{dst_dir}'.")
    except Exception as e:
        logging.error(f"An error occured: {e}", exc_info=True)
    