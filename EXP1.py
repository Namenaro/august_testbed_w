import matplotlib.pyplot as plt
from matplotlib.pyplot import text

# один шаг распознавания: заранее поставлени одна точка и предсказана для нее вторая связанная.
# Задача построить парето кандидатов на распознавание этой второй точки.


def eval_w(bassin_vals, index_1, index_predicted, val_predicted):
    return w

def eval_k(bassin_vals, index_1, index_predicted, val_predicted):
    return k



def one_step_recognision():
    bassin_vals = [0, 1, 2, 4, 2, 1, 0, -1.2, 1, 1.5, 0, 0, 1,0, 0, -1, 1.5, 2]
    index_1 = 3

    index_predicted = 6
    val_predicted = 0
    # ----------------------------------------------------------
    # ЧАСТЬ_1: генератор точек-кандидатов на оценку. Самое тупое - бруофорс, то есть перебор всех координат в допустимой области
    # ЧАСТЬ_2: для каждой точки оценка по 2 параметрам: w, k. Кто попадет в парето? Визуализация парето.

    for real_index in range(index_1, len(bassin_vals)):
        w = eval_w(bassin_vals, index_1, index_predicted, val_predicted)
        k = eval_k(bassin_vals, index_1, index_predicted, val_predicted)





if __name__ == '__main__':
    one_step_recognision()

