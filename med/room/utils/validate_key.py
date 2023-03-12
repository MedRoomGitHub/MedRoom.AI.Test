def validate_key(dic: dict, key: str):
    """
    Validates if key exists in dict and if it is valid
    :param dic: {dict} the dict to analize
    :param key: {str} the key that will be validated
    """
    return key in dic and dic[key]


__all__ = ['validate_key']
