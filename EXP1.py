from utils import Pareto2d

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

    ws = []
    ks = []
    for real_index in range(index_1, len(bassin_vals)):
        w = eval_w(bassin_vals, index_1, index_predicted, val_predicted)
        k = eval_k(bassin_vals, index_1, index_predicted, val_predicted)
        ws.append(w)
        ks.append(k)
    pareto = Pareto2d()
    pareto_indexes = pareto.process_ws_ks(ws_list=ws, ks_list=ks)

    fig , ax = plt.subplots()
    ax.plot(bassin_vals)
    for index in pareto_indexes:
        ax.vlines(x=index, ymin=0, ymax=max(bassin_vals), colors='orange', lw=1, alpha=0.5)
        text(index, max(bassin_vals) / 2, str(ws[index]), rotation=0, verticalalignment='center')
    plt.show()


if __name__ == '__main__':
    one_step_recognision()

