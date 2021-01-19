# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'lynne'
# Created by lynne on 2021/1/13.

import lottery_utils
import random
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
    '''
    time for default init seed
    init_rander is a rander for all used in real_rander_seed
    
    init_rander random a step in [1,100] for step of init_rander choice a real_rander_seed.
    init_rander random a seed_rander_seed_max
    init_rander random a seed_rander_seed
    init_rander random a real_rander_max
    init_rander random a real_seed
    '''
    init_rander_seed = time.time()
    init_rander = random.Random(init_rander_seed)
    lottery_utils.logger.info(lottery_utils.logger_fmt_component(["init_rander seed", str(init_rander_seed)]))

    # step for random for seed_rander random a  rand seed
    random_step = init_rander.randint(1,100)
    lottery_utils.logger.info(lottery_utils.logger_fmt_component(["seed_rander step", str(random_step)]))
    # seed_rander_seed
    seed_rander_seed_max = init_rander.randint(1, long(time.time()))
    lottery_utils.logger.info(lottery_utils.logger_fmt_component(["seed_rander_seed_max ", str(seed_rander_seed_max)]))

    seed_rander_seed = init_rander.randint(1,seed_rander_seed_max)
    lottery_utils.logger.info(lottery_utils.logger_fmt_component(["seed_rander_seed ", str(seed_rander_seed)]))

    seed_rander = random.Random(seed_rander_seed)

    while(random_step > 0):
        seed_rander.randint(1, seed_rander_seed_max)
        random_step -= 1

    seed_length = 10
    default_seed = 0l
    while(seed_length > 0):
        default_seed += seed_rander.randint(0,9)
        seed_length -= 1
        if(seed_length > 0):
            default_seed *= 10
    default_seed = long(default_seed)
    lottery_utils.logger.info(lottery_utils.logger_fmt_component(["default_seed", str(default_seed)]))

    parser = argparse.ArgumentParser(
        description='random lottery entrance. ')
    parser.add_argument('-f', '--input_uid_file', default="./input.uid", dest='input_uid_file', type=str,
                        help='input_uid_file.')
    parser.add_argument("-s", '--seed', dest='seed', type=str, default=default_seed,
                        help="random seed.")
    parser.add_argument("-l", '--level', dest='level', type=int, default=8,
                        help="lottery level.")

    parser.add_argument("-c", "--stage_cleansing", action = "store_true", default=False, dest='stage_cleansing',
                        help='stage cleansing. ')
    sys_argv = lottery_utils.sys.argv[1:]
    if(len(sys_argv) < 1):
        sys_argv.append("-h")
    args = parser.parse_args(sys_argv)

    le = LotteryEntrance(_seed=args.seed, _input_uid_file=args.input_uid_file, _restart_flag=args.stage_cleansing)
    print(le.rand_perm(args.level))

