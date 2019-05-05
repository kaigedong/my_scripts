# -*- coding: utf-8 -*-
"""
Created on 2019-05-05

@author: kaigedong
"""

# 将 circRNA 的相对坐标转为在基因组上的绝对坐标
# 比如给定环形RNA 第120 - 133 个坐标，将其转为基因组上的绝对坐标，可能为好几段，将这几段都输出来，以bed格式或者ref_flat格式。
# 输入类似于：

# exon_s = "1085359,1088571,1089240,1089938,1100107,1102248,"
# exon_e = "1087444,1088702,1089333,1090111,1100185,1102656,"
# circ_s = "1088571"
# circ_e = "1100185"
# circ_pos_s = "127"
# circ_pos_e = "192"

# 调用：a = circPos_to_genomePos(exon_s, exon_e, circ_s, circ_e, circ_pos_s, circ_pos_e)
# 返回结果：a is:  [1088698, 1088702, 1089240, 1089301]
# 从前向后每两个一组表示一个block：区间1：[1088698, 1088702], 区间2：[1089240, 1089301]

# 注意：circ_s, circ_e 是左闭右开区间，如表示第一个碱基则 circ_s = 0, circ_e = 1

def circPos_to_genomePos(exon_s, exon_e, circ_s, circ_e, circ_pos_s, circ_pos_e):
    # 将参数转为int类型：
    exon_s = [int(i) for i in exon_s.split(',')[:-1:]]
    exon_e = [int(i) for i in exon_e.split(',')[:-1:]]
    circ_s, circ_e, circ_pos_s, circ_pos_e = int(circ_s), int(circ_e), int(circ_pos_s), int(circ_pos_e)

    # 获取基因上每个exon长度
    exon_len = [j - i for i, j in zip(exon_s, exon_e)]

    # 获取 circ 跨越的 exon 的位置
    circ_s_index = exon_s.index(circ_s)
    circ_e_index = exon_e.index(circ_e)

    # print("[当前的参数信息为：]")
    # print("[exon起始坐标：]", exon_s)
    # print("[exon结束坐标：]", exon_e)
    # print("[exon的长度时：]", exon_len)
    # print()

    # 将相对circ的坐标转为基因组上的绝对坐标：

    def get_abso_pos(pos_in_circ, exon_s, exon_len, circ_s_index, circ_e_index):
        for i, a_exon_len in enumerate(exon_len[circ_s_index: circ_e_index + 1]):
            if pos_in_circ // a_exon_len == 0:
                # 当前长度取商，为0时，则表示就在当前exon上
                pos_in_chr = exon_s[circ_s_index + i] + pos_in_circ
                return pos_in_chr
            else:
                # 否则，判断是不是在下一个exon上之前，要减去当前exon长度
                pos_in_circ = pos_in_circ - a_exon_len

    circ_s_in_chr = get_abso_pos(circ_pos_s, exon_s, exon_len, circ_s_index, circ_e_index)
    circ_e_in_chr = get_abso_pos(circ_pos_e, exon_s, exon_len, circ_s_index, circ_e_index)

    # 获取开始、结束之间的坐标：
    # 首先插入开始结束，排序，然后取出开始、结束之间的：
    exon_pos = exon_s + exon_e
    if circ_s_in_chr not in exon_pos:
        exon_pos.append(circ_s_in_chr)

    if circ_e_in_chr not in exon_pos:
        exon_pos.append(circ_e_in_chr)
    exon_pos.sort()

    # 则相对坐标的区间为：
    circ_in_genome_pos = exon_pos[exon_pos.index(circ_s_in_chr): exon_pos.index(circ_e_in_chr) + 1]

    return (circ_in_genome_pos)

