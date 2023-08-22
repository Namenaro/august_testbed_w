from utils import Pareto2d, Slayter2d, Distr, get_distr_of_min_statistics, mix_list, make_arrows, ExtremumFinder, get_mini_ECG, draw_ECG,  draw_vertical_line
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



def visualise_on_signal(ws, ks, bassin_vals, new_allowed_indexes):
    fig, ax = plt.subplots(nrows=3, sharex=True)
    x = list(range(len(bassin_vals)))
    ax[0].plot(x, bassin_vals, '-o', color='black', label='bassin', alpha=0.5)

    make_arrows(ax[0])


    for i in range(len(ws)):
        index = new_allowed_indexes[i]
        w = ws[i]
        ax[1].scatter(index, w, color='red',  s=60)
    ax[1].legend(frameon=False)

    for i in range(len(ks)):
        index = new_allowed_indexes[i]
        k = ks[i]
        ax[2].scatter(index, k, color='green', s=60)

    ax[2].legend(frameon=False)

    plt.show()



def visualise_pareto(ws, ks, global_pareto_indexes, local_indexes_pareto, bassin_vals):
    fig, ax = plt.subplots()
    x = list(range(len(bassin_vals)))
    ax.plot(x, bassin_vals)
    make_arrows(ax)
    for index in global_pareto_indexes:
        ax.vlines(x=index , ymin=0, ymax=max(bassin_vals), colors='green', lw=1, alpha=0.5)
        #text(index, max(bassin_vals) / 2, str(ws[index]), rotation=0, verticalalignment='center')
    plt.show()

    draw_pareto_on_plane(ws, ks, local_indexes_pareto)

def draw_pareto_on_plane(ws, ks, pareto_indexes):
    fig, ax = plt.subplots()
    for index in range(len(ws)):
        ax.scatter(ws[index], ks[index], color='blue',  alpha=0.5)

    for index in pareto_indexes:
        ax.scatter(ws[index], ks[index], c='red')
    ax.set_xlabel('w', fontsize=20)
    ax.set_ylabel('k', fontsize=20)
    plt.show()





def ECG_one_step_recognition_vis():
    fig, ax = plt.subplots()
    bassin_vals = get_mini_ECG()
    draw_ECG(ax, bassin_vals)



    print("bassin_len = " + str(len(bassin_vals)))

    index_1 = 25
    draw_vertical_line(x=index_1, y=max(bassin_vals), ax=ax, label='index1', color='black')

    index_predicted_ideal = 36
    val_predicted_ideal = bassin_vals[index_predicted_ideal]
    print("val -pred - ideal = " + str(val_predicted_ideal))
    ax. scatter(index_predicted_ideal, val_predicted_ideal, color='orange', label='ideal prediction')

    index_predicted = index_predicted_ideal+7
    val_predicted = val_predicted_ideal+5
    ax.scatter(index_predicted, val_predicted, color='blue', label='jittered_prediction')
    plt.show()
    # ----------------------------------------------------------


    ws = []
    ks = []
    allowed_indexes = list(range(index_1, len(bassin_vals)))
    new_allowed_indexes = subselect_allowed_indexes(allowed_indexes, bassin_vals)
    for real_index in new_allowed_indexes:
        print(real_index)
        w = eval_w_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, real_index)
        k = eval_k_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, real_index)
        ws.append(w)
        ks.append(k)

    visualise_on_signal(ws, ks, bassin_vals, new_allowed_indexes)

    pareto = Slayter2d()
    pareto_indexes = pareto.process_ws_ks(ws_list=ws, ks_list=ks)
    scene_indexes = []
    for ind in pareto_indexes:
        scene_indexes.append( new_allowed_indexes[ind])

    visualise_pareto(ws, ks, global_pareto_indexes=scene_indexes, local_indexes_pareto=pareto_indexes, bassin_vals=bassin_vals)

def subselect_allowed_indexes(allowed_indexes, bassin):
    # вариант 1: ищем экстремумы сигнала в разрешенной области и возвращаем их индексы (визуализируем их на сигнале)
    extrs = ExtremumFinder(bassin).get_coords_extremums()
    allowed_extrs = []
    for coord in extrs:
        if coord in allowed_indexes:
            allowed_extrs.append(coord)
    #fig, axs = plt.subplots()
    #draw_ECG(axs, bassin)
    #for coord in extrs:
    #    axs.scatter(coord, 0, color='red')
    #plt.show()

    return allowed_extrs

if __name__ == '__main__':
    ECG_one_step_recognition_vis()

