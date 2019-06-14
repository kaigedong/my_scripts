# -*- coding: utf-8 -*-
"""
Created on 2019-05-05
@author: kaigedong
"""

import sys

# 将 circRNA 的相对坐标转为在基因组上的绝对坐标
# 比如在某个环形RNA 第120 - 133 个坐标，将其转为基因组上的绝对坐标，可能为好几段，将这几段都输出来，以bed格式或者ref_flat格式。
# 输入结果是 TargetScan的坐标

# def circPos_to_genomePos2(circ_anno_line, miRNA_sites_line):
def circPos_to_genomePos2(circ_anno_line, circ_pos_s, circ_pos_e):

    circ_items = circ_anno_line.strip().split()
    circ_exon_lens = [int(i) for i in circ_items[10].split(',')]
    circ_total_len = sum(circ_exon_lens)

    circ_exon_s = [int(circ_items[1]) + int(i) for i in circ_items[11].split(',')]
    circ_exon_e = [i+j for i, j in zip(circ_exon_s, circ_exon_lens)]

    # miRNA_sites_items = miRNA_sites_line.strip().split()
    #
    # circ_pos_s, circ_pos_e = int(miRNA_sites_items[3]), int(miRNA_sites_items[4])
    circ_pos_s, circ_pos_e = int(circ_pos_s)-1, int(circ_pos_e)  # miRNA 结合位置是1-base的，所以减去个1

    if circ_items[5] == '-':
        # 这里注意第一步已经改变了circ_pos_s, 如果分开写则第二个结果是错的。
        circ_pos_s, circ_pos_e = circ_total_len - circ_pos_e, circ_total_len - circ_pos_s

    circ_s_in_chrome, circ_e_in_chrome = 0, 0

    # 将相对于circ的坐标转化为在基因组上的绝对坐标：
    for i, j in enumerate(circ_exon_lens):
        if circ_pos_s // j == 0:  # 则就在当前这个 exon 上：
            circ_s_in_chrome = circ_exon_s[i] + circ_pos_s
            break
        else:
            circ_pos_s = circ_pos_s - j

    for i, j in enumerate(circ_exon_lens):
        if circ_pos_e // j == 0 or (circ_pos_e // j == 1 and circ_pos_e % j == 0):  # 则就在当前这个 exon 上：
            circ_e_in_chrome = circ_exon_s[i] + circ_pos_e
            break
        else:
            circ_pos_e = circ_pos_e - j

    # 获取开始、结束之间的坐标：
    # 首先插入开始结束，排序，然后取出开始、结束之间的：
    exon_pos = circ_exon_s + circ_exon_e
    if circ_s_in_chrome not in exon_pos: exon_pos.append(circ_s_in_chrome)
    if circ_e_in_chrome not in exon_pos: exon_pos.append(circ_e_in_chrome)
    exon_pos.sort()

    # 则相对坐标的区间为：
    circ_in_genome_pos = exon_pos[ exon_pos.index(circ_s_in_chrome): exon_pos.index(circ_e_in_chrome) + 1]

    return [circ_items[0], circ_items[1], circ_items[2], circ_items[5]] + circ_in_genome_pos


def run1():
    with open(sys.argv[1], 'r') as fin:
    # with open("/Users/kaigedong/Documents/picb/phone.1", 'r') as fin:
        for aline in fin:
            aline = aline.strip()
            items = aline.split()
            circ_pos_s = items[-2].split(',')
            circ_pos_e = items[-1].split(',')

            for i, j in zip(circ_pos_s, circ_pos_e):
                a = circPos_to_genomePos2(aline, i, j)
                a = "\t".join([str(i) for i in a])
                print(a)


if __name__ == "__main__":
    """
    读入文件：每一行都是这样的：
    chr20	17639240	17660720	RRBP1%ENST00000377813	0	-	17639240	17660720	0	2	1933,77	0,21403	1020,1050,1080,1110,1140,1170,1200,1230,1260,1290,1320,1350,1380,1410,1440,1470,1500,1530,1560,1590,1674,1734,1764,1914,661,690,750,780,960	1027,1057,1087,1117,1147,1177,1207,1237,1267,1297,1327,1357,1387,1417,1447,1477,1507,1537,1567,1597,1681,1741,1770,1920,667,697,756,787,966
    
    结果：
    chr20	17639240	17660720	-	17640223	17640231
    chr20	17639240	17660720	-	17640193	17640201
    chr20	17639240	17660720	-	17640163	17640171
    chr20	17639240	17660720	-	17640133	17640141
    chr20	17639240	17660720	-	17640103	17640111
    chr20	17639240	17660720	-	17640073	17640081
    chr20	17639240	17660720	-	17640043	17640051
    """
    run1()

    
