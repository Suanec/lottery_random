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
        self.reinit(_candidates=_candidates, _pre_winner=_pre_winner, _seed=_seed,
                    _rule_config_file=_rule_config_file, _status_config_file=_status_config_file)

    def reinit(self, _candidates = {}, _pre_winner = {}, _seed = None,
                 _rule_config_file = "rule.json", _status_config_file = "status.json"):
        self.candidates = _candidates
        self.candidates_size = len(self.candidates)
        self.pre_winner = _pre_winner
        logger.info(logger_fmt_component(["_seed", str(_seed)]))
        self.rander = Random(_seed) if(_seed) else Random
        self.rule_config = lottery_utils.json.load(open(_rule_config_file, "r"))
        self.status_config = lottery_utils.json.load(open(_status_config_file, "r"))
        self.status_stage_file = _status_config_file + ".lottery_random.stage"
        self._init_stage_file()
        self.KEY_LEVEL = "level"
        self.KEY_STATUS = "status"
        self.KEY_LOTTERY_ALL_COUNT = "lottery_all_count"
        self.KEY_LOTTERY_MAX_TIMES = "lottery_max_times"
        self.KEY_LOTTERY_COUNT = "lottery_count"
        self.KEY_LOTTERY_CUR_TIMES = "lottery_cur_times"
        self.KEY_LOTTERY_WINNER_LIST = "lottery_winner_list"
        self.KEY_WINNERS = "winners"

    def _init_stage_file(self):
        try:
            lottery_utils.json.load(open(self.status_stage_file, "r"))
        except Exception as e:
            lottery_utils.json.dump(self.status_config, open(self.status_stage_file, "w"))


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
        self._read_rules()
        self.status_stage = self.status_config.get(self.KEY_STATUS)
        self.stage_config = lottery_utils.json.load(open(self.status_stage_file, "r"))
        self.lottery_winner = self.stage_config.get(self.KEY_WINNERS)
        self.lottery_winner_id = set(self.lottery_winner.keys())

    def _stage_winners(self):
        self.stage_config[self.KEY_STATUS][self.level_key][self.KEY_LOTTERY_CUR_TIMES] = self.level_cur_times + 1
        for winner_id in self.rander_perm_result:
            self.lottery_winner[winner_id] = self.level_key
        self.lottery_winner_str = lottery_utils.json.dump(self.stage_config, open(self.status_stage_file, "w"))

    def stage_cleansing(self):
        lottery_utils.os.remove(self.status_stage_file)

    def rander_perm(self, _level = 8):
        self.random_candidates = self._rander_perm()
        self._read_status()
        self.level_key = self.KEY_LEVEL + str(_level)
        self.level_rule = self.level_rules.get(self.level_key)

        self.level_count = self.level_rule.get(self.KEY_LOTTERY_COUNT)
        self.level_max_times = self.level_rule.get(self.KEY_LOTTERY_MAX_TIMES)
        self.level_cur_times = self.stage_config.get(self.KEY_STATUS).get(self.level_key).get(self.KEY_LOTTERY_CUR_TIMES)
        if(self.level_cur_times < self.level_max_times):
            self.rander_perm_result = [x for x in self.random_candidates if (x not in self.lottery_winner_id)]
            self.rander_perm_result = self.rander_perm_result[:self.level_count]
            assert len(self.rander_perm_result) == self.level_count
            [ self.lottery_winner.update({x: self.level_key}) for x in self.rander_perm_result ]
            lottery_utils.logger.info(self.level_key + "\t|\t" + ",".join(self.rander_perm_result))
            return self.rander_perm_result
        else:
            lottery_utils.logger.error(self.level_key + "has been finished.")
            return []


if __name__ == '__main__':
    candidate_list = open("./input.uid", "r").read().split("\n")
    pre_winner = set()
    lr81 = LotteryRandom(candidate_list, pre_winner, 1096)
    # lr81.stage_cleansing()
    lr81 = LotteryRandom(candidate_list, pre_winner, 1096)
    lr81_winner = lr81.rander_perm()
    print(lr81_winner)
    pre_winner.update(set(lr81_winner))
    lr82 = LotteryRandom(candidate_list, pre_winner, 1096)
    lr82_winner = lr82.rander_perm()
    print(lr82_winner)
    pre_winner.update(set(lr82_winner))
    print(pre_winner)
