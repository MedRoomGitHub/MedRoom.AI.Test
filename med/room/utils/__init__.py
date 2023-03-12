from .colorize import Colorize
from .logger import logger

from .custom_requests import RequestObjects
from .validate_key import validate_key


def filter_empty(column):
    return (column.notnull())


def debugger(
    df, message='>>>>Debugger<<<<', show=True, save_df=True, save_name='debugger.parquet', limit=20, is_truncated=True
):
    """
    Display and save a parquet from a running processor

    :param df: {DataFrame} Input Data Frame.
    :message: (opt) Message to display in console
    :show: (opt) Control console message
    :is_truncated: (opt) Show full log
    :limit: (opt) Limit rows on display message
    :save_df: (opt) Control save a parquet file
    :save_name: (opt) Customize name of output file
    """
    if message:
        print(f'\x1b[1;32m ------------------- {message} --------------------\x1b[0m')
