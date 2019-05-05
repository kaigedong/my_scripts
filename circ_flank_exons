# -*- coding: utf-8 -*-
"""
Created on 2019-05-05

@author: kaigedong
"""


# 获取circ两侧的exon的坐标：
# 结果为 [[1085359, 1087444], [1102248, 1102656]] 或某一侧包含None的数组：[['None'],['None']]

def get_flank_exons(exon_s, exon_e, circ_s, circ_e):
    # 将参数转为int类型：
    exon_s = [int(i) for i in exon_s.split(',')[:-1:]]
    exon_e = [int(i) for i in exon_e.split(',')[:-1:]]

    circ_s, circ_e = int(circ_s), int(circ_e)

    circ_s_index = exon_s.index(circ_s)
    circ_e_index = exon_e.index(circ_e)

    if circ_s_index == 0:
        left = ['None']
    else:
        left = [exon_s[circ_s_index-1], exon_e[circ_s_index-1]]

    if circ_e_index == len(exon_s)-1:
        right = ['None']
    else:
        right = [exon_s[circ_e_index+1], exon_e[circ_e_index+1]]

    return [left, right]


# 获取circ内的每个exon的坐标：
# 返回类似 [1088571, 1088702, 1089240, 1089333, 1089938, 1090111, 1100107, 1100185]
def get_circ_exons(exon_s, exon_e, circ_s, circ_e):
    # 将参数转为int类型：
    exon_s = [int(i) for i in exon_s.split(',')[:-1:]]
    exon_e = [int(i) for i in exon_e.split(',')[:-1:]]

    circ_s, circ_e = int(circ_s), int(circ_e)

    exon_bound = exon_s + exon_e
    exon_bound.sort()

    return exon_bound[exon_bound.index(circ_s): exon_bound.index(circ_e)+1]


if __name__ == "__main__":
    exon_s = "1085359,1088571,1089240,1089938,1100107,1102248,"
    exon_e = "1087444,1088702,1089333,1090111,1100185,1102656,"

    circ_s = "1088571"
    circ_e = "1100185"

    print(get_flank_exons(exon_s, exon_e, circ_s, circ_e))

    print(list(get_circ_exons(exon_s, exon_e, circ_s, circ_e)))
