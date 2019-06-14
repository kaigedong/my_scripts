# -*- coding: utf-8 -*-
"""
Created on 2019-05-05
@author: kaigedong
"""

import re, sys


def get_flank_exons(exon_s, exon_e, circ_s, circ_e):
    """
    获取circ两侧的exon的坐标：
    :param exon_s: "1085359,1088571,1089240,1089938,1100107,1102248,"
    :param exon_e: "1087444,1088702,1089333,1090111,1100185,1102656,"
    :param circ_s: "1088571"
    :param circ_e: "1100185"
    :return: [[1085359, 1087444], [1102248, 1102656]] or [['None'],['None']]
    """

    exon_s = [int(i) for i in exon_s.strip(',').split(',')]
    exon_e = [int(i) for i in exon_e.strip(',').split(',')]

    circ_s, circ_e = int(circ_s), int(circ_e)

    circ_s_index = exon_s.index(circ_s)
    circ_e_index = exon_e.index(circ_e)

    left = ['None'] if circ_s_index == 0 else [exon_s[circ_s_index-1], exon_e[circ_s_index-1]]
    right = ['None'] if circ_e_index == len(exon_s)-1 else [exon_s[circ_e_index+1], exon_e[circ_e_index+1]]

    return [left, right]


def get_circ_exons(exon_s, exon_e, circ_s, circ_e):
    """
    获取circ内的每个exon的坐标：
    :param exon_s: "1085359,1088571,1089240,1089938,1100107,1102248,"
    :param exon_e: "1087444,1088702,1089333,1090111,1100185,1102656,"
    :param circ_s: "1088571"
    :param circ_e: "1100185"
    :return: [[1088571, 1089240, 1089938, 1100107], [1088702, 1089333, 1090111, 1100185]]
    """

    exon_s = [int(i) for i in exon_s.strip(',').split(',')]
    exon_e = [int(i) for i in exon_e.strip(',').split(',')]

    circ_s, circ_e = int(circ_s), int(circ_e)

    exon_bound = exon_s + exon_e
    exon_bound.sort()

    exons = exon_bound[exon_bound.index(circ_s): exon_bound.index(circ_e)+1]

    return [[exons[2*i] for i in range(int(len(exons)/2))], [exons[2*i+1] for i in range(int(len(exons)/2))]]


def get_refanno_from_circpos(f_anno, circ_pos):
    """
    根据 circRNA 的位置获得其注释

    :param f_anno: 读入注释文件，获得的列表，每个元素是ref_all的一行组成的列表：
    "IDI1    NM_001317955    chr10   -       1085359 1102656 1087126 1090083 6       1085359,1088571,1089240,1089938,1100107,1102248,        1087444,1088702,1089333,1090111,1100185,1102656,"
    :param circ_pos: "chr1:123-321"
    :return:
    """

    circ_pos = re.split(":|-", circ_pos)

    for a_item in f_anno:
        if circ_pos[0] == a_item[2] and circ_pos[1] in a_item[9] and circ_pos[2] in a_item[10]:  # 表示找到了这个环形RNA对应的注释

            # print(a_item)

            circ_exons = get_circ_exons(a_item[9], a_item[10], circ_pos[1], circ_pos[2])

            block_len = ','.join([str(j-i) for i,j in zip(circ_exons[0], circ_exons[1])])
            block_start = ','.join([str(i-circ_exons[0][0]) for i in circ_exons[0]])

            circ_bed12 = '\t'.join((a_item[2], str(circ_exons[0][0]), str(circ_exons[1][-1]), 'circular_RNA', '0',
                                    a_item[3], str(circ_exons[0][0]), str(circ_exons[0][0]), '0,0,0',
                                    str(len(circ_exons[0])), block_len, block_start))

            flank_exons = get_flank_exons(a_item[9], a_item[10], circ_pos[1], circ_pos[2])
            left_exon = "None" if 'None' in flank_exons[0] else a_item[2] + ":" + str(flank_exons[0][0]) + '-' + \
                                                                str(flank_exons[0][1])
            right_exon = "None" if 'None' in flank_exons[1] else a_item[2] + ":" + str(flank_exons[1][0]) + '-' + \
                                                                  str(flank_exons[1][1])

            circ_bed15 = "\t".join(
                circ_bed12, a_item[0], a_item[1], left_exon + "|" + right_exon
            )

            return circ_bed15


if __name__ == "__main__":

    print("!!!注意：最后一列是flank exon的坐标，而不是flank intron！flank intron可由circRNA位置及flank exon位置得到。")

    f_anno = []  # 读取所有的ref_all，放到这个列表中
    with open(sys.argv[1], 'r') as fin:
        for aline in fin:
            items = aline.strip().split()
            f_anno.append(items)

    with open(sys.argv[2], 'r') as fin:  # 读取所有的circRNA位置 (每行都是 "chr1:123-345" 的类型)
        for aline in fin:
            aline = aline.strip()
            print(get_refanno_from_circpos(aline))


    # 测试通过。
    test1 = get_refanno_from_circpos(f_anno, "chrY:345515-347693")
    test2 = get_refanno_from_circpos(f_anno, "chrX:10567001-10567603")
    print(test1)
    print(test2)
    # 实际circRNA注释:
    # test1: chrY    345515  347693  circular_RNA/1  0       -       345515  345515  0,0,0   5       157,87,75,103,
    # 104       0,658,1185,1718,2074    1       circRNA PPP2R3B ENST00000390665.8_PAR_Y      7,6,5,4,3       chrY:341931-345515|chrY:347693-361404
    # test2: chrX    10567001        10567603        circular_RNA/1  0       -       10567001        10567001        0,0,0   1       602     0       1       circRNA MID1    ENST00000610939.1       1       chrX:10523187-10567001|None


