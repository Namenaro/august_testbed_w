from utils import Pareto2d, Slayter2d, Distr, get_distr_of_min_statistics, mix_list, make_arrows, ExtremumFinder, get_mini_ECG, draw_ECG,  draw_vertical_line
from scene import Scene
from helpers import *

import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy

# один шаг распознавания: заранее поставлени одна точка и предсказана для нее вторая связанная.
# Задача построить парето кандидатов на распознавание этой второй точки.




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





def ECG_one_step_recognition_vis(): # ПОЛУЧЕНИЕ ЛИСТОВ ДЛЯ РОСТКА
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

    # ПЕРВИЧНЫЙ БЫСТРЫЙ ОТБОР КАНДИДАТОВ
    allowed_indexes = list(range(index_1, len(bassin_vals)))
    new_allowed_indexes = subselect_allowed_indexes(allowed_indexes, bassin_vals)

    # ВТОРЫИЧНЫЙ (МЕДЛЕННЫЙ) ОТБОР КАНДИДАТОВ  (ИЗ БЫСТРО ВЫБРАННЫХ)
    # ЭТАП 1: ОЦЕНКА  W, K
    ws = []
    ks = []
    for real_index in new_allowed_indexes:
        print(real_index)
        w = eval_w_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, real_index)
        k = eval_k_of_candidate(bassin_vals, index_1, index_predicted, val_predicted, real_index)
        ws.append(w)
        ks.append(k)

    visualise_on_signal(ws, ks, bassin_vals, new_allowed_indexes)

    # ЭТАП 2: ЧИСТОВОЙ ВЫБОР ТОПА КАНДИДАТОВ ИЗ ОЦЕНЕННЫХ (МНОГОКРИТЕРИАЛЬНАЯ ЗАДАЧА ПОИСКА ЛУЧШИХ КОМПРОМИССОВ)
    pareto = Slayter2d()
    pareto_indexes = pareto.process_ws_ks(ws_list=ws, ks_list=ks)
    scene_indexes = []
    for ind in pareto_indexes:
        scene_indexes.append( new_allowed_indexes[ind])

    visualise_pareto(ws, ks, global_pareto_indexes=scene_indexes, local_indexes_pareto=pareto_indexes, bassin_vals=bassin_vals)



if __name__ == '__main__':
    ECG_one_step_recognition_vis()

