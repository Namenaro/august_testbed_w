from utils import get_signal, HtmlLogger, Pareto2d, Slayter2d, Distr, get_distr_of_min_statistics, mix_list, make_arrows, ExtremumFinder, get_mini_ECG, draw_ECG,  draw_vertical_line
from scene import Scene
from helpers import *
from helpers_visualise import *

import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from copy import deepcopy



class Situation:
    def __init__(self, bassin, index1, val_pred, coord_pred):
        self.bassin_vals = bassin
        self.index_1 = index1
        self.index_predicted = index1 + coord_pred
        self.val_predicted = val_pred

    def draw(self, log):
        # ПЕРВИЧНЫЙ БЫСТРЫЙ ОТБОР КАНДИДАТОВ  (ИХ ИЗБЫТОЧНОЕ КОЛ_ВО)
        fast_allowed_indexes = self._fast_candidates_select()

        # ВТОРЫИЧНЫЙ (МЕДЛЕННЫЙ) ОТБОР КАНДИДАТОВ  (ИЗ БЫСТРО ВЫБРАННЫХ)
        # ЭТАП 1: ОЦЕНКА  W, K
        ws, ks = self._get_ws_ks(fast_allowed_indexes)

        # ЭТАП 2: ЧИСТОВОЙ ВЫБОР ТОПА КАНДИДАТОВ ИЗ ОЦЕНЕННЫХ (МНОГОКРИТЕРИАЛЬНАЯ ЗАДАЧА ПОИСКА ЛУЧШИХ КОМПРОМИССОВ)
        global_leafs_indexes, leafs_ws, leafs_ks = self._select_top_wk_compromisses(fast_allowed_indexes, ws=ws, ks=ks)

        ###########   отрисовка   ###################################
        # # риуем ЭКГ с дано и листьями  (первая fig )
        fig, ax = plt.subplots()
        log.add_fig(fig)

        #рисуем парето плоскость      (вторая fig)
        fig = visualise_leafs_on_signal(signal=self.bassin_vals,
                                        leafs_coords=global_leafs_indexes,
                                        index_1=self.index_1,
                                        predicted_index=self.index_predicted,
                                        predicted_val=self.val_predicted)
        log.add_fig(fig)

    def _fast_candidates_select(self):
        allowed_indexes = list(range(len(self.bassin_vals)))
        new_allowed_indexes = subselect_allowed_indexes(allowed_indexes, self.bassin_vals)
        return new_allowed_indexes

    def _get_ws_ks(self, allowed_indexes):
        ws = []
        ks = []
        for real_index in allowed_indexes:
            print(real_index)
            w = eval_w_of_candidate(self.bassin_vals, self.index_1, self.index_predicted, self.val_predicted, real_index)
            k = eval_k_of_candidate(self.bassin_vals, self.index_1, self.index_predicted, self.val_predicted, real_index)
            ws.append(w)
            ks.append(k)
        return ws, ks

    def _select_top_wk_compromisses(self, indexes, ws, ks):
        pareto = Slayter2d()
        local_pareto_indexes = pareto.process_ws_ks(ws_list=ws, ks_list=ks)
        global_selected_indexes = []
        for ind in local_pareto_indexes:
            global_selected_indexes.append(indexes[ind])
        return global_selected_indexes, ws, ks




def get_coords_1st_points(signal, N):
    coords = ExtremumFinder(signal).get_top_N_maxes(N)
    return coords

def get_prediction_for_2dn_point():
    # берем вручную из картинок EXP1
    val = -75
    u = 36-25
    return val, u

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






