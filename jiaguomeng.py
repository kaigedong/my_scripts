#!/usr/bin/env python3
# -*- coding: utf-8 -*-#

# -----------------------------------------------------------------------------
# Name:         jiaguomeng.py
# Description:  
# Author:       bobo
# Date:         2019/10/1
# -----------------------------------------------------------------------------

import os
import time
import cv2
import numpy as np
import logging
# import uiautomator2 as u2


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Jianguomeng:
    def __init__(self, current_building):
        # 获取截图路径
        # self.d = u2.connect()
        # time.sleep(2)
        # self.sess = self.d.session("com.tencent.jgm")
        # time.sleep(20)

        self.screen_path = self.get_screen_shot()


        # (建筑、货物、建筑稀有度)
        self.all_goods_on_train = {
            '木屋': ('桌子', 0),
            '钢结构房': ('沙发', 0),
            '平房': ('花盆', 0),
            '小型公寓': ('衣柜', 0),
            '居民楼': ('礼盒', 0),
            '人才公寓': ('笔记本', 1),
            '花园洋房': ('狗粮', 1),
            '中式小楼': ('棉被', 1),
            '空中别墅': ('台灯', 2),
            '复兴公馆': ('红毯', 2),

            '便利店': ('汽水', 0),
            '学校': ('书包', 0),
            '服装店': ('衬衫', 0),
            '五金店': ('螺丝', 0),
            '菜市场': ('青菜', 0),
            '图书城': ('书本', 1),
            '商贸中心': ('红皮鞋', 1),
            '加油站': ('绿包', 1),
            '追梦快递': ('推车', 1),
            '民食斋': ('鸡腿', 2),
            '媒体之声': ('话筒', 2),


            '木材厂': ('木头', 0),
            '造纸厂': ('稻草', 0),
            '水厂': ('水箱', 0),
            '电厂': ('煤炭', 0),
            '食品厂': ('大米', 0),
            '钢铁厂': ('煤炭', 1),
            '纺织厂': ('棉花', 1),
            '零件厂': ('钢板', 1),
            '企鹅机械': ('零件', 2),
            '人民石油': ('石油', 2),
            '强国煤业': ('安全帽', 2),
        }

        # 9个建筑的位置
        self.building_pos = (
            (215, 440), (384, 360), (533, 233),
            (215, 600), (384, 535), (533, 460),
            (215, 788), (384, 711), (533, 621),
        )
        # 火车三个格子的位置
        # self.goods_pos = ((666, 1827), (807, 1776), (972, 1660))

        self.current_building = current_building

    def loads_goods(self, threshold=0.9):

        for build_index, a_build in enumerate(self.current_building):

            # if self.all_goods_on_train[a_build][1] != 2:
            #     # 只拉金色货物！
            #     continue

            logging.info('正在检查{}'.format(self.all_goods_on_train[a_build][0]))
            a_good = 'goods_onmumu/' + self.all_goods_on_train[a_build][0] + '_small.png'
            res = cv2.matchTemplate(
                cv2.imread(a_good), cv2.imread(self.screen_path), cv2.TM_CCOEFF_NORMED
            )
            loc = np.where(res >= threshold)
            try:
                pos = (int(loc[1][0]), int(loc[0][0]))
                logging.info('发现 {}'.format(self.all_goods_on_train[a_build][0]))
                for i in range(4):
                    logging.info('移动{}到{}, 从{}到{}'.format(self.all_goods_on_train[a_build][0], a_build,
                                                          pos, self.building_pos[build_index]))
                    self.swap_a_to_b(pos, self.building_pos[build_index])
            except:
                continue

    def swap_a_to_b(self, point1, point2):
        '''
        从A点滑到B点
        :param point1:
        :param point2:
        :return:
        '''
        os.system('adb shell input swipe {} {} {} {} 600'.format(
            point1[0], point1[1], point2[0], point2[1]
        ))

    # 截图并返回图片路径
    def get_screen_shot(self):
        get_screen_shot = 'adb shell screencap -p /sdcard/screen1.png && ' \
                          'adb pull /sdcard/screen1.png'
        os.system(get_screen_shot)
        time.sleep(1)  # 留个pull照片的时间
        logging.info('截图完成')
        return 'screen1.png'

    def collect_and_update(self, n):
        '''
        收集金币，并升级一个建筑(第n个建筑,1 base)
        :return: None
        '''
        for i in self.building_pos:
            self.click(i)

        # n == 0时，不升级建筑
        if n == 0:
            return
        self.click((981, 1344))  # 点击升级按钮
        time.sleep(0.5)
        self.click(self.building_pos[n-1])  # 点击建筑
        self.click((870, 2076))   # 升级建筑
        self.click((981, 1344))  # 点击升级按钮，返回初始状态。

    # 左右切换一下标签
    def switch_label(self):
        # 切换一下标签页
        self.click((320, 1234))
        time.sleep(0.5)
        self.click((57, 1238))
        time.sleep(1)

    def click(self, point):
        os.system('adb shell input tap {0} {1}'.format(point[0], point[1]))


if __name__ == '__main__':
    current_building = ['企鹅机械',  '强国煤业', '人民石油', '商贸中心',
                        '追梦快递', '民食斋', '小型公寓', '花园洋房', '复兴公馆']
    # current_building = ['企鹅机械', '人民石油', '零件厂',  '商贸中心', '媒体之声',
    #                     '民食斋', '复兴公馆', '花园洋房', '小型公寓']
    while True:
        a_run = Jianguomeng(current_building)
        a_run.loads_goods()
        # for i in range(5):
        #     a_run.collect_and_update(0)  # 升级第2号建筑，n==0不升级
        #     time.sleep(6)
        print('='*80)
        time.sleep(8)
        a_run.switch_label()
