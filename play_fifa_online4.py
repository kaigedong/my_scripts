# -*- coding: utf-8 -*-
"""
Created on 2019-06-14
@author: kaigedong
"""

import os, time, logging

command3 = "adb shell input tap 648 1989"  # 点击开始
command4 = "adb shell input tap 662 2126"  # 点击结束
a_play_time = 195   
times_to_play = 5  # 假设连续玩10局游戏

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

for i in range(times_to_play):
    logger.info('点击开始按钮')
    os.system(command3)
    logger.info('等待本轮游戏结束。正在进行第'+ str(i+1) + "轮...")
    time.sleep(a_play_time)
    logger.info('点击确定(总结比分的页面)')
    os.system(command4)
    time.sleep(2)
    
logger.info("游戏结束！")
