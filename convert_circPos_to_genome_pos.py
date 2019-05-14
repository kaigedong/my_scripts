# -*- coding: utf-8 -*-
"""
Created on 2019-05-05

@author: kaigedong
"""

# 将 circRNA 的相对坐标转为在基因组上的绝对坐标
# 比如在某个环形RNA 第120 - 133 个坐标，将其转为基因组上的绝对坐标，可能为好几段，将这几段都输出来，以bed格式或者ref_flat格式。
# 输入结果是 TargetScan的坐标

'''
从 ref_all.txt 的注释：
IDI1	NM_001317955	chr10	-	1085359	1102656	1087126	1090083	6	1085359,1088571,1089240,1089938,1100107,1102248,	1087444,1088702,1089333,1090111,1100185,1102656,
提取：
exon_s： 1085359,1088571,1089240,1089938,1100107,1102248,
exon_e:  1087444,1088702,1089333,1090111,1100185,1102656,

从circ的info，提取：
circ_s: circ的开始坐标 比如 1088571
circ_e: circ的结束坐标 比如 1100185

circ_pos_s: 在circ上的起始坐标 比如在circ的第100个碱基
circ_pos_e：在circ上的结束坐标 比如在circ的第120个碱基

strand：circ是位于正链还是负链？如果是正链，则circ_pos 从左往右数；如果是负链，则circ_pos从右往左数
strand = '+' or strand = '-'
'''


def circPos_to_genomePos(exon_s, exon_e, circ_s, circ_e, circ_pos_s, circ_pos_e, strand):

    # 将参数转为int类型：
    exon_s = [ int(i) for i in exon_s.rstrip(',').split(',')]
    exon_e = [ int(i) for i in exon_e.rstrip(',').split(',')]
    circ_s, circ_e, circ_pos_s, circ_pos_e = int(circ_s), int(circ_e), int(circ_pos_s)-1, int(circ_pos_e) # miRNA 结合位置是1-base的，所以减去个1

    # 获取基因上 每个exon长度
    exon_len = [ j-i for i, j in zip(exon_s, exon_e) ]

    # 获取 circ 跨越的exon的位置
    circ_s_index = exon_s.index(circ_s)
    circ_e_index = exon_e.index(circ_e)

    circ_total_len = sum(exon_len[circ_s_index:circ_e_index+1])

    # print("参数为：", exon_s, exon_e, circ_s, circ_e, circ_pos_s, circ_pos_e)
    # print("基因上每个exon长度为：", exon_len)
    # print("circ_exon的index为",circ_s_index, circ_e_index)
    # print("circ的长度为：", circ_total_len)

    if strand == '-':
        # 这里注意第一步已经改变了circ_pos_s, 如果分开写则第二个结果是错的。
        circ_pos_s, circ_pos_e = circ_total_len - circ_pos_e, circ_total_len - circ_pos_s

    circ_s_in_chrome, circ_e_in_chrome = 0, 0

    # 将相对于circ的坐标转化为在基因组上的绝对坐标：
    for i, j in enumerate(exon_len[circ_s_index: circ_e_index + 1]):

        if circ_pos_s // j == 0:
            # 则就在当前这个 exon 上：
            circ_s_in_chrome = exon_s[circ_s_index + i] + circ_pos_s
            break
        else:
            circ_pos_s = circ_pos_s - j

    for i, j in enumerate(exon_len[circ_s_index: circ_e_index + 1]):

        if circ_pos_e // j == 0 or (circ_pos_e // j == 1 and circ_pos_e % j == 0):
            # 则就在当前这个 exon 上：
            circ_e_in_chrome = exon_s[circ_s_index + i] + circ_pos_e
            break
        else:
            circ_pos_e = circ_pos_e - j


    # print("相对于circ的坐标转化为基因组上的绝对坐标是",circ_s_in_chrome, circ_e_in_chrome)

    # 获取开始、结束之间的坐标：
    # 首先插入开始结束，排序，然后取出开始、结束之间的：
    exon_pos = exon_s + exon_e
    if circ_s_in_chrome not in exon_pos:
        exon_pos.append(circ_s_in_chrome)
    if circ_e_in_chrome not in exon_pos:
        exon_pos.append(circ_e_in_chrome)
    exon_pos.sort()

    # 则相对坐标的区间为：
    circ_in_genome_pos = exon_pos[ exon_pos.index(circ_s_in_chrome) : exon_pos.index(circ_e_in_chrome) + 1]

    return(circ_in_genome_pos)

# 代码测试：
def test5():
    exon_s = '17594322,17595381,17596075,17596570,17597376,17599240,17600277,17600943,17601359,17602102,17602334,' \
             '17602499,17605220,17606156,17607992,17608148,17610467,17614104,17616190,17617221,17622441,17623623,17639240,17660643,17662672,'
    exon_e = '17594865,17595525,17596174,17596654,17597484,17599324,17600373,17601015,17601452,17602192,17602418,' \
             '17602592,17605313,17606247,17608027,17608327,17610606,17614258,17616309,17617374,17622564,17623772,17641173,17660720,17662878,'
    circ_s = '17639240'
    circ_e = '17660720'

    circ_pos_s = '1020,1050,1080,1110,1140,1170,1200,1230,1260,1290,1320,1350,1380,1410,1440,1470,1500,1530,1560,1590,1674,1734,1764,1914,661,690,750,780,960'
    circ_pos_e = '1027,1057,1087,1117,1147,1177,1207,1237,1267,1297,1327,1357,1387,1417,1447,1477,1507,1537,1567,1597,1681,1741,1770,1920,667,697,756,787,966'

    circ_pos_s = circ_pos_s.split(',')
    circ_pos_e = circ_pos_e.split(',')

    strands = '-'

    for i,j in zip(circ_pos_s, circ_pos_e):
        a = circPos_to_genomePos(exon_s, exon_e, circ_s, circ_e, i, j, strands)
        print(a)


if __name__ == "__main__":
    test5()
    
    
