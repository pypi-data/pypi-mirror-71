import re
from random import random


class Attribute:
    def __init__(self, attr_type, translation_required=False, null_proba=0, **kwargs_rd_gen):

        self.attr_type = attr_type
        self.kwargs_rd_gen = kwargs_rd_gen
        self.null_proba = null_proba
        self.translation_required = translation_required

        self._relation_types = [0, 1, 2]

    def get_random_value(self, fake_factory, translator, locale):

        if random() > self.null_proba:
            return self.attr_type.get_random(
                fake_factory,
                translator,
                locale,
                translation_required=self.translation_required,
                **self.kwargs_rd_gen
            )
        else:
            return None
