from typing import Tuple, List

import numpy as np
import torch

from allrank_mod.click_models.base import ClickModel
from allrank_mod.data.dataset_loading import PADDED_Y_VALUE


def click_on_slates(slates: Tuple[torch.Tensor, torch.Tensor], click_model: ClickModel, include_empty: bool) \
        -> Tuple[List[torch.Tensor], List[List[int]]]:
    """
    This metod runs a click model on a list of slates and returns new slates with `y` taken from clicks

    :param slates: a Tuple of X, y:
        X being a list of slates represented by document vectors
        y being a list of slates represented by document relevancies
    :param click_model: a click model to be applied to every slate
    :param include_empty: if True - will return even slates that didn't get any click
    :return: Tuple of X, clicks, X representing the same document vectors as input 'X', clicks representing click mask for every slate
    """
    X, y = slates
    clicks = [MaskedRemainMasked(click_model).click(slate) for slate in zip(X, y)]
    X_with_clicks = [[X, slate_clicks] for X, slate_clicks in list(zip(X, clicks)) if
                     (np.sum(slate_clicks > 0) > 0 or include_empty)]
    return_X, clicks = map(list, zip(*X_with_clicks))
    return return_X, clicks  # type: ignore


class MaskedRemainMasked(ClickModel):
    """
    This click model wraps another click model and:
      1. ensures inner click model do not get documents that were padded
      2. ensures padded documents get '-1' in 'clicked' vector
    """

    def __init__(self, inner_click_model: ClickModel):
        """

        :param inner_click_model: a click model that is run on the list of non-padded documents
        """
        self.inner_click_model = inner_click_model

    def click(self, documents: Tuple[torch.Tensor, torch.Tensor]):
        X, y = documents
        padded_values_mask = y == PADDED_Y_VALUE
        real_X = X[~padded_values_mask]
        real_y = y[~padded_values_mask]
        clicks = self.inner_click_model.click((real_X, real_y))
        final_clicks = np.zeros_like(y)
        final_clicks[padded_values_mask] = PADDED_Y_VALUE
        final_clicks[~padded_values_mask] = clicks
        return final_clicks
