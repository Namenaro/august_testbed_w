from utils import Pareto2d, Distr, get_distr_of_min_statistics, mix_list, make_arrows, ExtremumFinder
from scene import Scene

import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy

# один шаг распознавания: заранее поставлени одна точка и предсказана для нее вторая связанная.
# Задача построить парето кандидатов на распознавание этой второй точки.


def eval_w_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, index_candidate):
    u_err = abs(index_predicted-index_candidate)
    prev_error = sum(list([abs(val) for val in bassin_vals]))
    interpolation_err = get_interpolation_error(index_1, index_candidate, bassin_vals)
    distr_bests = get_distr_of_mins_err(bassin_vals, index_fixed=index_1, u_err=u_err, segment_len=abs(index_1-index_candidate))
    if prev_error == interpolation_err:
        return 0

    if prev_error > interpolation_err:
        # w будет положительно
        w = 1 - distr_bests.get_p_of_event(0, interpolation_err)
        return w

    # w будет отрицательно:
    w = distr_bests.get_p_of_event(interpolation_err, distr_bests.get_max_val())
    return -w

def eval_k_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, index_candidate):
    u_err = abs(index_candidate - index_predicted)
    val_err = abs(val_predicted - bassin_vals[index_candidate])


    vals_side = max(bassin_vals) - min(bassin_vals)
    us_side = len(bassin_vals)
    err = val_err/vals_side + u_err/us_side

    return 1 - err


def get_distr_of_mins_err(bassin_, index_fixed, u_err, segment_len):
    bassin = deepcopy(bassin_)
    # исключаем из бассейна уже учтенныйэлемент
    fixed_val = bassin[index_fixed]
    del bassin[index_fixed]
    errs_sample = []
    for i in range(200):
        err_interpolation = get_random_interpolation_err(segment_len, bassin, fixed_val)
        errs_sample.append(err_interpolation)
    main_distr = Distr(errs_sample)
    distr_min_subs_statistic = get_distr_of_min_statistics(main_distr, u_err+1)
    return distr_min_subs_statistic

def get_random_interpolation_err(segment_len, bassin, fixed_val):
    # случайно переставляем элементы бассейна
    mixed_bassin = mix_list(bassin)
    mixed_bassin.append(fixed_val)
    scene = Scene(mixed_bassin)

    # конец интерполяции ставим в последнюю точку
    name1 = scene.add_point(len(mixed_bassin) - 1)

    # выбираем второй конец сегмента
    # TODO его можно выбрать случайно (и тогда эта статистика переиспользуется всем и кандидатами), или же на расстоянии segment_len от последней точки
    second_index = len(mixed_bassin) - 1 - segment_len

    name_2 = scene.add_point(coord=second_index)
    scene.add_parent(parent_name=name1, child_name=name_2)

    return scene.get_err_sum()


def get_interpolation_error(index1, index2, bassin_vals):
    scene = Scene(bassin_vals)
    name_1 = scene.add_point(coord=index1)
    name_2 = scene.add_point(coord=index2)
    scene.add_parent(parent_name=name_1, child_name=name_2)
    return scene.get_err_sum()



def visualise_on_signal(ws, ks, bassin_vals, index_1):
    fig, ax = plt.subplots(nrows=3, sharex=True)
    x = list(range(len(bassin_vals)))
    ax[0].plot(x, bassin_vals, '-o', color='black', label='bassin', alpha=0.5)
    ax[0].vlines(x=index_1, ymin=0, ymax=max(bassin_vals), colors='orange', lw=1, alpha=0.5)
    make_arrows(ax[0])


    indexes_of_maxes_w = ExtremumFinder(ws).get_coords_maxes()
    indexes_of_maxes_w = list([indexes_of_maxes_w[i] + index_1 for i in range(len(indexes_of_maxes_w))])
    for index in indexes_of_maxes_w:
        ax[0].scatter(index, bassin_vals[index], color='red',  s=60)
    ax[0].legend(frameon=False)

    x = list(range(index_1, len(bassin_vals)))
    ax[1].plot(x, ws, '-o', label='w (index2)')
    make_arrows(ax[1])
    ax[1].legend(frameon=False)


    ax[2].plot(x, ks, '-o', label='k (index2)')
    make_arrows(ax[2])
    ax[2].legend(frameon=False)

    plt.show()



def visualise_pareto(ws, ks, pareto_indexes, bassin_vals, index1):
    fig, ax = plt.subplots()
    x = list(range(len(bassin_vals)))
    ax.plot(x, bassin_vals)
    make_arrows(ax)
    for index in pareto_indexes:
        ax.vlines(x=index + index1 , ymin=0, ymax=max(bassin_vals), colors='green', lw=1, alpha=0.5)
        #text(index, max(bassin_vals) / 2, str(ws[index]), rotation=0, verticalalignment='center')
    plt.show()

    draw_pareto_on_plane(ws, ks, pareto_indexes)

def draw_pareto_on_plane(ws, ks, pareto_indexes):
    fig, ax = plt.subplots()
    for index in range(len(ws)):
        ax.scatter(ws[index], ks[index], color='blue',  alpha=0.5)

    for index in pareto_indexes:
        ax.scatter(ws[index], ks[index], c='red')
    ax.set_xlabel('w', fontsize=20)
    ax.set_ylabel('k', fontsize=20)
    plt.show()



def one_step_recognision():
    bassin_vals = [0, 1, 2, 4, 2, 1, 0, -1.2, 1, 1.5, 0, 0, 1,0, 0, -1, 1.5, 2]
    print("bassin_len = " +str(len(bassin_vals)))
    index_1 = 3

    index_predicted = 6
    val_predicted = 0
    # ----------------------------------------------------------
    # ЧАСТЬ_1: генератор точек-кандидатов на оценку. Самое тупое - бруофорс, то есть перебор всех координат в допустимой области
    # ЧАСТЬ_2: для каждой точки оценка по 2 параметрам: w, k. Кто попадет в парето? Визуализация парето.

    ws = []
    ks = []
    for real_index in range(index_1, len(bassin_vals)):
        if real_index == 12:
            print("!!")
        print(real_index)
        w = eval_w_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, real_index)
        k = eval_k_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, real_index)
        ws.append(w)
        ks.append(k)

    visualise_on_signal(ws, ks, bassin_vals, index_1)


    pareto = Pareto2d()
    pareto_indexes = pareto.process_ws_ks(ws_list=ws, ks_list=ks)
    visualise_pareto(ws, ks, pareto_indexes, bassin_vals, index_1)

if __name__ == '__main__':
    one_step_recognision()

