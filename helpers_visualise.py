from utils import make_arrows, draw_ECG, draw_vertical_line

import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy

def draw_ws_ks_on_plane(ws, ks, leafs_ws, leafs_ks):
    fig, ax = plt.subplots()
    max_ws = max(1, max(ws))
    min_ws = min(-1, min(ws))
    max_ks = max(1, max(ks))

    ax.set_xlabel('w', fontsize=20)
    ax.set_ylabel('k', fontsize=20)

    ax.set_xlim([min_ws-0.2, max_ws+0.2])
    ax.set_ylim([-0.2, max_ks+0.2])

    for index in range(len(ws)):
        ax.scatter(ws[index], ks[index], color='blue')

    for index in range(len(leafs_ws)):
        ax.scatter(leafs_ws[index], leafs_ks[index], c='red', alpha=0.5)


    return fig

def visualise_leafs_on_signal(signal, leafs_coords, index_1, predicted_index, predicted_val):
    fig, ax = plt.subplots()

    #рисуем сигнал
    draw_ECG(ax, signal)


    # рисуем интекс1 и предсказание
    draw_vertical_line(color='red', label="index1", ax=ax, x=index_1, y=max(signal))
    ax.scatter(predicted_index, predicted_val, color='orange', label='ideal prediction')

    # рисуем листья
    for index in leafs_coords:
        ax.vlines(x=index , ymin=0, ymax=max(signal), colors='green', lw=1, alpha=0.5)


    return fig