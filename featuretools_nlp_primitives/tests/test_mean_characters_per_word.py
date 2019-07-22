import numpy as np
import pandas as pd

from ..utils import TestTransform, find_applicable_primitives, valid_dfs
from .mean_characters_per_word import MeanCharactersPerWord


class TestMeanCharactersPerWord(TestTransform):
    primitive = MeanCharactersPerWord

    def test_sentences(self):
        x = pd.Series(['This is a test file',
                       'This is second line',
                       'third line $1,000',
                       'and subsequent lines',
                       'and more'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([3.0, 4.0, 5.0, 6.0, 3.5])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_punctuation(self):
        x = pd.Series(['This: is a test file',
                       'This, is second line?',
                       'third/line $1,000;',
                       'and--subsequen\'t lines...',
                       '*and, more..'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([3.0, 4.0, 8.0, 10.5, 4.0])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_multiline(self):
        x = pd.Series(['This is a test file',
                       'This is second line\nthird line $1000;\nand subsequent lines',
                       'and more'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([3.0, 4.8, 3.5])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_nans(self):
        x = pd.Series([np.nan,
                       '',
                       'third line'])
        primitive_func = self.primitive().get_function()
        answers = pd.Series([np.nan, np.nan, 4.5])
        pd.testing.assert_series_equal(primitive_func(x), answers, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
