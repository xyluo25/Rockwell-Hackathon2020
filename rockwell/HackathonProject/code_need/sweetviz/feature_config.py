from typing import Tuple

from sweetviz.sv_types import FeatureType


class FeatureConfig:
    def __init__(self, skip: Tuple = None,
            force_cat: Tuple = None, force_text: Tuple = None,
            force_num: Tuple = None):
        def make_list(param):
            if type(param) == list or type(param) == tuple:
                return param
            elif type(param) == str:
                return [param]
            elif param is None:
                return list()
            raise ValueError("Invalid value passed in for FeatureConfig")

        self.skip = make_list(skip)
        self.force_cat = make_list(force_cat)
        self.force_text = make_list(force_text)
        self.force_num = make_list(force_num)

    def get_predetermined_type(self, feature_name: str):
        if feature_name in self.skip:
            return FeatureType.TYPE_SKIPPED
        elif feature_name in self.force_cat:
            return FeatureType.TYPE_CAT
        elif feature_name in self.force_text:
            return FeatureType.TYPE_TEXT
        elif feature_name in self.force_num:
            return FeatureType.TYPE_NUM
        else:
            return FeatureType.TYPE_UNKNOWN

    def get_all_mentioned_features(self):
        returned = list()
        returned.extend(self.skip)
        returned.extend(self.force_cat)
        returned.extend(self.force_text)
        returned.extend(self.force_num)
        return returned