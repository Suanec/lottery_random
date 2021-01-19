### lottery_random
#### 主要特性
- 本组脚本实现了一个抽奖程序主逻辑
- 强随机性保证
- 不放回采样逻辑，避免重复中奖
- shell交互，方便与各种页面整合
- 完整的日志信息记录
- 复验过程中，强一致性保证
- 基本完整的测试结论
- 可视化随机性报告

#### 使用方法
##### 推荐用法
- 随机生成种子
- 日志简化并重定向，只输出结果
- `-l`代表抽奖等级，0代表特等奖，1代表一等奖，以此类推。
- `input.uid`为默认id候选池，可通过`-f`指定候选池文件。
```
python lottery_entrance.py -l 0 2>&1 | grep level0
[INFO] : 2021-01-19 20:15:07,118 lottery_random.py[line:97]  level0	|	nb203513
```

##### 定制用法（不推荐）
- 通过`-s`指定随机种子，同样的种子，随机序列不变
- 通过`-c`清楚本地缓存，相当于重置所有中奖信息
```
 python lottery_entrance.py -l 0 -f input.uid -s 61833404 -c 2>&1 | grep level0
[INFO] : 2021-01-19 20:19:12,584 lottery_random.py[line:97]  level0	|	nb201036
[0][lynne@bj-m-207415a:lottery_random]$ python lottery_entrance.py -l 0 -f input.uid -s 61833404 -c 2>&1 | grep level0
[INFO] : 2021-01-19 20:19:14,476 lottery_random.py[line:97]  level0	|	nb201036
```

##### lottery_entrance.py help 信息
```
[0][lynne@bj-m-207415a:lottery_random]$ python lottery_entrance.py -h
usage: lottery_entrance.py [-h] [-f INPUT_UID_FILE] [-s SEED] [-l LEVEL] [-c]

random lottery entrance.

optional arguments:
  -h, --help            show this help message and exit
  -f INPUT_UID_FILE, --input_uid_file INPUT_UID_FILE
                        input_uid_file.
  -s SEED, --seed SEED  random seed.
  -l LEVEL, --level LEVEL
                        lottery level.
  -c, --stage_cleansing
                        stage cleansing.
```

#### 抽奖逻辑
##### 默认模式（推荐流程）
- 1. 先由当前时间戳，生成一个随机数生成器`init_render`
- 2. 随后利用`init_render`生成，种子采样步数`step`（不同步数，得到的抽奖种子不同），为照顾效率采样步数`step`被限定在[1,100]的范围
- 3. 其次利用`init_render`生成，抽奖种子采样器种子范围 seed_rander_seed_max，取值范围为[1, 当前时间戳]
- 4. 随后在`seed_rander_seed_max`的限制下，随机得到抽奖种子采样器种子：`seed_rander_seed`
- 5. 利用`seed_rander_seed`，生成抽奖种子采样器。
- 6. 得到采样器后，先基于前期随机得到的种子采样步数`step`，利用抽奖种子采样器进行预采样。
- 7. 预采样完毕后，使用抽奖种子采样器进行[0,9]的实际种子采样，采样10次，得到一枚长度为10 的抽奖种子`default_seed`。（参考北京小客车指标系统随机采样逻辑）
- 8. 得到抽奖种子`default_seed`后，利用`default_seed`生成抽奖随机采样器`LotteryRandom`。
- 9. 读取候选池id，默认`input.uid`，可自定义文件名，内容字符串即可。
- 10. 基于`LotteryRandom`，利用[随机洗牌算法(Knuth-Durstenfeld Shuffle)](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)，进行候选池随机打乱。
- 11. 创建本地状态文件`status.json.lottery_random.stage`进行不同级别奖项的记录，分别记录：所有奖项已抽奖次数、各奖项获奖id、所有已获奖id名单。
- 12. 基于本地状态文件`status.json.lottery_random.stage`在步骤10生成的序列中，进行排除已中奖id。结合规则文件`rule.json`、当前所抽奖项级别，取的序列头部不同数量id作为中奖名单。
- 13. 所有种子文件、状态信息、获奖信息均写入日志文件，由日志文件，可对中奖结果进行复验和review。
- 14. 若已运行过程序，需要加带`-c`参数，清除本地缓存文件，手动删除亦可。
##### 复验模式（指定seed，进行结果回溯）
- 1. 利用`-s`指定抽奖随机器种子，生成抽奖随机采样器`LotteryRandom`。
- 2. 跳转至默认模式，步骤9。后续逻辑一致。

#### 代码构成
```
README.md                                  本说明文档，介绍整个抽奖器使用方式与逻辑
input.uid                                  候选池文件
lottery_entrance.py                        抽奖器入口文件、默认种子生成文件
lottery_random.py                          抽奖器核心采样组件，随机洗牌算法(Knuth-Durstenfeld Shuffle)，实现
lottery_utils.py                           一些预定义变量、日志操作、时间、json、系统等杂项配置
lottery_validation.py                      一键验证组件，待实现
lynne_lottery_randperm.log                 抽奖器行为日志
random_test_result                         随机性测试结果目录，代码自测结果与统计、分析。
rule.json                                  规则配置文件
rule.json.bak                              规则配置文件备份
status.json                                状态协议描述文件
status.json.bak                            状态协议描述文件备份
status.json.lottery_random.stage           状态缓存文件
```

#### 测试结果文件介绍
```
test.level0.1000times.log                         特等奖抽奖1000次，日志文件
test.level0.1000times.sh                          特等奖抽奖1000次，脚本文件
test.level0.100times.log                          特等奖抽奖100次，日志文件
test.level0.100times.sh                           特等奖抽奖100次，脚本文件
test.level8.1000times.log                         八等奖抽奖1000次，日志文件
test.level8.1000times.sh                          八等奖抽奖1000次，脚本文件
test.level8.100times.log                          八等奖抽奖100次，日志文件
test.level8.100times.sh                           八等奖抽奖100次，脚本文件
抽奖随机性统计.xlsx                                 基于日志文件的随机性数据分析制图

```
#### 测试结果描述
##### 分别进行特等奖和八等奖的功能测试
- 特等奖 结果：在候选池数量为6665的情况下，采样100次，未见重复中奖id，且分号段分析，未见明显偏袒。各组号段分布满足随机性
- 八等奖 结果：在候选池数量为6665的情况下，采样100次，未见重复中奖id，且分号段分析，未见明显偏袒。各组号段分布满足随机性
- 详情参阅测试结果文件中`抽奖随机性统计.xlsx`各统计tab。