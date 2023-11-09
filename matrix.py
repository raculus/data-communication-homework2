import numpy as np


def matrix_list():
    """
    연산 결과를 저장할 10x10 크기의 행렬 6개 생성
    """
    matrixList = []
    for i in range(6):
        matrixList.append(np.empty((10, 10)))
    return matrixList


def random_matrix(rangeMin=0, rangeMax=100, row=10, col=10):
    """
    무작위 정수기반(0~100사이) 행렬을 생성
    """
    matrix = np.random.randint(rangeMin, rangeMax + 1, size=(row, col))
    return matrix


def extract_row(matrix, row_index: int):
    """
    행 1개를 1차원 배열로 반환
    """
    return matrix[row_index, :]


def extract_col(matrix, col_index: int):
    """
    열 1개를 1차원 배열로 반환
    """
    return matrix[:, col_index]


def arr_to_str(array):
    """
    1차원 배열을 문자열로 변환
    """
    return " ".join(map(str, array))


def str_to_arr(s):
    """
    문자열을 1차원 배열로 변환
    """
    return np.array(list(map(int, s.split())))
