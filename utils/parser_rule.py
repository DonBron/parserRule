import logging
import re

log = logging.getLogger(__name__)


def get_web_category_id(row_data: str) -> str:
    web_category_id = re.findall(r'СГ\(9001\) like .*?\)|СГ\(9001\) = .*?\)', row_data)
    return ', '.join(
        [_.replace('СГ(9001) like ', '').replace('СГ(9001) = ', '').replace(')', '') for _ in web_category_id]
    )


def get_master_web_category_id(row_data: str) -> str:
    master_web_category_id = re.findall(r'СГ\(10001\) like .*?\)|СГ\(10001\) = .*?\)', row_data)
    return ', '.join(
        [_.replace('СГ(10001) like ', '').replace('СГ(10001) = ', '').replace(')', '') for _ in master_web_category_id]
    )


def get_like_cat_level_data(row_data: str) -> str:
    like_cat_level_data = re.findall(r'СГ\(9001\) like .*?\)', row_data)
    like_cat_level_data = [
        _.replace('СГ(9001) like ', '').replace('СГ(9001) = ', '').replace(')', '') for _ in like_cat_level_data
    ]
    like_cat_level = []
    for value in like_cat_level_data:
        match len(value):
            case 12:
                like_cat_level.append('6')
            case 11:
                like_cat_level.append('6')
            case 10:
                like_cat_level.append('5')
            case 9:
                like_cat_level.append('5')
            case 8:
                like_cat_level.append('4')
            case 7:
                like_cat_level.append('4')
            case 6:
                like_cat_level.append('3')
            case 5:
                like_cat_level.append('3')
            case 4:
                like_cat_level.append('2')
            case 3:
                like_cat_level.append('2')
            case _:
                like_cat_level.append('X')
    return ', '.join(like_cat_level)


def check_web_category(row_data: str) -> bool:
    return any(
        [
            True if row_data.count('Идентификатор родителя СГ') > 0 else False,
            True if row_data.count('Идентификатор СГ') > 0 else False,
            True if row_data.count('Имя СГ') > 0 else False,
            True if row_data.count('Идентификатор корневой категории') > 0 else False,
            True if row_data.count('Имя корневой категории') > 0 else False,
        ]
    )


def proverit(row_data: str) -> list[str]:
    like_cat_level_data = re.findall(r'СГ\(9001\) like .*?\)', row_data)
    like_cat_level_data = [
        _.replace('СГ(9001) like ', '').replace('СГ(9001) = ', '').replace(')', '') for _ in like_cat_level_data
    ]
    like_cat_level = []
    for value in like_cat_level_data:
        if len(value) == 16:
            like_cat_level.append(value)
    return like_cat_level
