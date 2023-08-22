from utils import get_signal, HtmlLogger, Pareto2d, Slayter2d, Distr, get_distr_of_min_statistics, mix_list, make_arrows, ExtremumFinder, get_mini_ECG, draw_ECG,  draw_vertical_line
from scene import Scene

import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy

def get_prediction_for_2dn_point():
    # берем вручную из картинок EXP1
    val = -75
    u = 36-25
    return val, u

class Situation:
    def __init__(self, bassin, index1, val_pred, coord_pred):
        self.bassin_vals = bassin

    def draw(self, log):
        # расчитываем w,k -мн-во
        # для него слейтер-листья

        # риуем ЭКГ с дано и листьями  (первая fig )
        fig, ax = plt.subplots()
        log.add_fig()
        # рисуем парето плоскость      (вторая fig)
        fig, ax = plt.subplots()
        log.add_fig()

def get_coords_1st_points(signal, N):
    coords = ExtremumFinder(signal).get_top_N_maxes(N)
    return coords

if __name__ == '__main__':
    val_pred, u_pred = get_prediction_for_2dn_point()

    # загуржаем полный сигнал экг
    bassin_vals = get_signal()

    # получаем стартовые точки распознавания
    coords1sts = get_coords_1st_points(bassin_vals, N=5)

    #  для каждой  точки отрисовываем ситуацию с распознаванием шага из нее
    log = HtmlLogger("EXP2-res")
    for index1 in coords1sts:
        left_pad = 25
        right_pad = 119 - 36

        bassin = bassin_vals[index1 - left_pad, index1 + right_pad]
        situation = Situation(bassin, index1=left_pad, val_pred=val_pred, coord_pred=val_pred + u_pred)
        situation.draw(log)






