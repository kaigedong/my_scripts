# -*- coding: utf-8 -*-
"""
Created on 2019-05-05

@author: kaigedong
"""


# 将 circRNA 的相对坐标转为在基因组上的绝对坐标
# 比如给定环形RNA 第120 - 133 个坐标，将其转为基因组上的绝对坐标，可能为好几段，将这几段都输出来，以bed格式或者ref_flat格式。


'''
一个转录本表示成 bed 为上面，表示为 refFlat 为下面，两者等价的。

chr10	1085359	1102656	NM_001317955	0	-	1087126	1090083	0	6	2085,131,93,173,78,408,	0,3212,3881,4579,14748,16889,
IDI1	NM_001317955	chr10	-	1085359	1102656	1087126	1090083	6	1085359,1088571,1089240,1089938,1100107,1102248,	1087444,1088702,1089333,1090111,1100185,1102656,

提取某几个exon为circRNA的序列之后，有将在 circRNA 上的相对位置转化为绝对位置的需求。

要求：
输入为 refFlat 和 环形RNA上的坐标，输出为 绝对坐标。

比如：
输入为 refFlat的格式，环形RNA为exon 2 - 3，环形上的坐标为A-B，要求输出A-B转化为绝对坐标后是什么？

注意：
circ的相对坐标是左开右闭的，要想包括最后一个碱基，可对输入的坐标 手动+1

'''



def circPos_to_genomePos(exon_s, exon_e, circ_s, circ_e, circ_pos_s, circ_pose):

    # 将参数转为int类型：
    exon_s = [ int(i) for i in exon_s.split(',')[:-1:] ]
    exon_e = [ int(i) for i in exon_e.split(',')[:-1:] ]
    circ_s, circ_e, circ_pos_s, circ_pos_e = int(circ_s), int(circ_e), int(circ_pos_s), int(circ_pose)


    # 获取基因上 每个exon长度
    exon_len = [ j-i for i, j in zip(exon_s, exon_e) ]


    # 获取 circ 跨越的exon的位置
    circ_s_index = exon_s.index(circ_s)
    circ_e_index = exon_e.index(circ_e)

    print("exon 开始坐标：", exon_s)
    print("exon 结束坐标：", exon_e)
    print("基因的每个exon 长度为：", exon_len)
    print()

    print("circ exon的index为 跨第%d 个exon 到 第%d个exon", circ_s_index, circ_e_index)
    print()

    circ_s_in_chrome, circ_e_in_chrome = 0, 0

    # 对于 circ上的绝对坐标：
    for i, j in enumerate(exon_len[circ_s_index: circ_e_index + 1]):
        # print(i, j)
        if circ_pos_s // j == 0:
            # 则就在当前这个 exon 上：
            circ_s_in_chrome = exon_s[circ_s_index + i] + circ_pos_s
            break
        else:
            circ_pos_s = circ_pos_s - j

    for i, j in enumerate(exon_len[circ_s_index: circ_e_index + 1]):

        if circ_pos_e // j == 0:
            # 则就在当前这个 exon 上：
            circ_e_in_chrome = exon_s[circ_s_index + i] + circ_pos_e
            break
        else:
            circ_pos_e = circ_pos_e - j

    print("circ的绝对坐标是：(结束要不要+1？)",circ_s_in_chrome, circ_e_in_chrome)

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

exon_s = "1085359,1088571,1089240,1089938,1100107,1102248,"
exon_e = "1087444,1088702,1089333,1090111,1100185,1102656,"

circ_s = "1088571"
circ_e = "1100185"

circ_pos_s = "127"
circ_pos_e = "192"


a = circPos_to_genomePos(exon_s, exon_e, circ_s, circ_e, circ_pos_s, circ_pos_e)
print('a is: ', a)
