# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'lynne'
# Created by lynne on 2021/1/13.

from random import Random
import lottery_utils
from lottery_utils import logger,logger_fmt_component

class LotteryRandom(object):
    def __init__(self, _candidates = {}, _pre_winner = {}, _seed = None,
                 _rule_config_file = "rule.json", _status_config_file = "status.json"):
        self.candidates = _candidates
        self.candidates_size = len(self.candidates)
        self.pre_winner = _pre_winner
        logger.info(logger_fmt_component(["_seed", str(_seed)]))
        self.rander = Random(_seed) if(_seed) else Random
        self.rule_config = lottery_utils.json.load(open(_rule_config_file, "r"))
        self.status_config = lottery_utils.json.load(open(_status_config_file, "r"))
        self.status_stage_file = _status_config_file + ".lottery_random.stage"
        self.KEY_LEVEL = "level"
        self.KEY_LOTTERY_ALL_COUNT = "lottery_all_count"
        self.KEY_LOTTERY_MAX_TIMES = "lottery_max_times"
        self.KEY_LOTTERY_COUNT = "lottery_count"
        self.KEY_LOTTERY_CUR_TIMES = "lottery_cur_times"


    def _rander_perm(self):
        self.random_candidates = [x for x in self.candidates]
        for (idx, candidate) in enumerate(self.random_candidates):
            cur_idx = idx
            tail_idx = self.rander.randrange(0, self.candidates_size - idx) + idx
            (self.random_candidates[cur_idx], self.random_candidates[tail_idx]) = \
                (self.random_candidates[tail_idx], self.random_candidates[cur_idx])
        return self.random_candidates

    def _read_rules(self):
        self.level_rules = self.rule_config.get("levels",{
            "level0": { "lottery_all_count":4, "lottery_max_times": 4, "lottery_count":1},
            "level1": { "lottery_all_count":6, "lottery_max_times": 1, "lottery_count":6},
            "level2": { "lottery_all_count":8, "lottery_max_times": 2, "lottery_count":4},
            "level3": { "lottery_all_count":10, "lottery_max_times": 2, "lottery_count":5},
            "level4": { "lottery_all_count":20, "lottery_max_times": 2, "lottery_count":10},
            "level5": { "lottery_all_count":40, "lottery_max_times": 2, "lottery_count":20},
            "level6": { "lottery_all_count":60, "lottery_max_times": 3, "lottery_count":20},
            "level7": { "lottery_all_count":80, "lottery_max_times": 4, "lottery_count":20},
            "level8": { "lottery_all_count":100, "lottery_max_times": 5, "lottery_count":20},
        })
        self.__dict__.update(self.level_rules)
        return self.level_rules

    def _read_status(self):
        self.status_stage = self.status_config.get("status")


    def rander_perm(self):
        self.random_candidates = self._rander_perm()

if __name__ == '__main__':
    candidate_list = open("./input.uid", "r").read().split("\n")
    pre_winner = {}
    lr = LotteryRandom(candidate_list, pre_winner, 1096)
    print(lr._rander_perm())
