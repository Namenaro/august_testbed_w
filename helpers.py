from utils import Pareto2d, Slayter2d, Distr, get_distr_of_min_statistics, mix_list, make_arrows, ExtremumFinder, get_mini_ECG, draw_ECG,  draw_vertical_line
from scene import Scene

from copy import deepcopy

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


def get_interpolation_error(index1, index2, bassin_vals):
    scene = Scene(bassin_vals)
    name_1 = scene.add_point(coord=index1)
    name_2 = scene.add_point(coord=index2)
    scene.add_parent(parent_name=name_1, child_name=name_2)
    return scene.get_err_sum()


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


