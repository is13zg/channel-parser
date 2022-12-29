import gspread
from settings import config
from gspread.exceptions import APIError
import create_bot
import inspect


async def add_data_to_worksheet(worksheet_name: str, data: list):
    try:
        gc = gspread.service_account(filename=config.credentinals_full_file_name)
        sheet = gc.open_by_key(config.google_sheet_id)
        try:
            worksheet = sheet.add_worksheet(title=worksheet_name, rows=(len(data) + 100), cols=(len(data[0]) + 10))
        except APIError:
            worksheet = sheet.worksheet(worksheet_name)
            worksheet.clear()
        adress = 'A1:' + chr(ord("A") + len(data[0])) + str(len(data))
        worksheet.update(adress, data)
    except Exception as e:
        await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name, e)
