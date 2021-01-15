# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'lynne'
# Created by lynne on 2021/1/13.

import lottery_utils
import time
import argparse
from lottery_random import LotteryRandom

class LotteryEntrance(object):
    def __init__(self, _seed = 61833404L, _input_uid_file = "./input.uid", _restart_flag = False):
        self.seed = _seed
        self.input_uid_file = _input_uid_file
        self.candidate_list = open(self.input_uid_file, "r").read().split("\n")
        self.pre_winner = set()
        self.lottery_rander = LotteryRandom(self.candidate_list, self.pre_winner, self.seed)
        if(_restart_flag):
            self.lottery_rander.stage_cleansing()
            self.lottery_rander.reinit(self.candidate_list, self.pre_winner, self.seed)

    def rand_perm(self, _level):
        self.cur_lottery_result = self.lottery_rander.rander_perm(_level=_level)
        print(self.cur_lottery_result)
        self.pre_winner.update(set(self.cur_lottery_result))
        return self.cur_lottery_result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='random lottery entrance. ')
    parser.add_argument('-f', '--input_uid_file', default="./input.uid", dest='input_uid_file', type=str,
                        help='input_uid_file.')
    parser.add_argument("-s", '--seed', dest='seed', type=str, default=long(time.time()),
                        help="random seed.")
    parser.add_argument("-l", '--level', dest='level', type=int, default=8,
                        help="lottery level.")

    parser.add_argument("-c", "--stage_cleansing", action = "store_true", default=False, dest='stage_cleansing',
                        help='stage cleansing. ')
    sys_argv = lottery_utils.sys.argv
    if(len(sys_argv) < 2):
        sys_argv.append("-h")
    args = parser.parse_args(sys_argv)

    le = LotteryEntrance(_seed=args.seed, _input_uid_file=args.input_uid_file, _restart_flag=args.stage_cleansing)
    print(le.rand_perm(args.level))

