# -*- coding: UTF-8 -*-
"""
 # @Project     : Object-Code-Generator
 # @File        : ObjectCode.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/6 10:03 上午
 # @Description :
"""

from RegisterDistribute import *

#你应该实现的：
#1. 算法6.3要求的，即调用6.1，6.2的相关内容实现输出

#2. 整合综合实验(只要完成1就很简单了）


#2中这里帮你处理好输入了，请自行对函数重命名
def obj_code_test(tac_path, sym_path):
    #active_info_list: 四元式列表: List<QuaternaryCode>
    #act_set: 活跃变量的集合: set<str>
    active_info_list,act_set=generate_active_info_list(tac_path,sym_path)

    #寄存器数量:int
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
