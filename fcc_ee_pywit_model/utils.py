from typing import Union
from pathlib import Path
import pyoptics as opt

import numpy as np
from scipy.interpolate import interp1d


def compute_betas_and_lengths(twiss_table,
                              layout_dict: dict) -> dict[str, dict[str, float]]:
    all_s = twiss_table.s
    _, ind = np.unique(all_s, return_index=True)
    all_s = all_s[ind]
    all_betax = twiss_table.betx[ind]
    all_betay = twiss_table.bety[ind]
    # interpolating functions
    fx = interp1d(all_s, all_betax, kind='cubic')
    fy = interp1d(all_s, all_betay, kind='cubic')

    dict_betas_lengths = {}

    for name in layout_dict['betas_lengths_names']:

        length = 0
        betax = 0
        betay = 0

        for the_beg, the_end_ in zip(layout_dict['sbeg'][name],
                                     layout_dict['send'][name]):
            if the_end_ > twiss_table.summary.length:
                the_end = twiss_table.summary.length
            else:
                the_end = the_end_

            length += the_end - the_beg
            the_s = np.arange(the_beg, the_end_, 0.01)
            if the_end not in the_s:
                the_s = np.hstack((the_s, [the_end]))
            # average beta (through trapz integration)
            betax += np.trapz(fx(the_s), x=the_s)
            betay += np.trapz(fy(the_s), x=the_s)

        if length != 0:
            betax /= length
            betay /= length

        dict_betas_lengths[name] = {
            'beta_x': betax,
            'beta_y': betay,
            'length': length
        }

    return dict_betas_lengths
