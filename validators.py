"""
Just an example right now.
"""
from typing import List, Callable

import functools
import pandas as pd

def has_index(dataframe: pd.DataFrame):
    return True

class Validator():
    """
    Just a composition of validator functions
    """
    def __init__(self,functions: List[Callable[[pd.DataFrame],bool]]):
        self.functions = functions

    def __call__(self, data:pd.DataFrame):
        valid = True
        for fn in self.functions:
            valid &= fn(data)
            if not valid:
                break
        return valid

validate_pgm = Validator([
        has_index
    ])
