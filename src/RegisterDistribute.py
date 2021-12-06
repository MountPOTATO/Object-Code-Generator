# -*- coding: UTF-8 -*-
"""
 # @Project     : Object-Code-Generator
 # @File        : RegisterDistribute.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/6 9:56 上午
 # @Description :
"""

from ActiveInfoList import *

#你应该在这里实现：
#(优先完成)1. GETREG的方法：按照算法6.3要求对每个四元式分配寄存器，即GETREG(i: A:=B op C),返回一个寄存器Ri,供6.3调用
#在题目要求的基础上，你可以自行添加输入参数，但需要与ObjectCode.py的同学商讨

#2. 寄存器分配算法的测试类，即按照6.2算法的输入输出规范，输入四元式列表，活跃变量列表，寄存器个数，输出文档中要求的东西

#2中帮你处理好输入了，请自行对函数重命名
def reg_test(tac_path, sym_path):
    #active_info_list: 四元式列表: List<QuaternaryCode>
    #act_set: 活跃变量的集合: set<str>
    active_info_list,act_set=generate_active_info_list(tac_path,sym_path)

    # 寄存器数量:int
    reg_num=0
    while True:
        try:
            reg_num=int(input("请输入寄存器个数:"))
            if reg_num <=0:
                raise ValueError
            else:
                break
        except ValueError:
            print("应输入一个大于0的整数为寄存器个数，请重试")


# reg_test("../tac.txt","../symbol.txt")
