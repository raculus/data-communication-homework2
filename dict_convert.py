from ast import literal_eval


def str_to_dict(str: str):
    """
    문자열 타입을 딕셔너리 타입으로 반환
    """
    return literal_eval(str)
