import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy

def draw_ws_ks_on_plane(ws, ks):
    fig, ax = plt.subplots()
    for index in range(len(ws)):
        ax.scatter(ws[index], ks[index], color='blue',  alpha=0.5)

    for index in range(len(ws)):
        ax.scatter(ws[index], ks[index], c='red')
    ax.set_xlabel('w', fontsize=20)
    ax.set_ylabel('k', fontsize=20)
    return fig

def visualise_leafs_on_signal(signal, leafs_coords, index_1, predicted_index, predicted_val):
    return fig