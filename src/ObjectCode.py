# -*- coding: UTF-8 -*-
"""
 # @Project     : Object-Code-Generator
 # @File        : ObjectCode.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/6 10:03 上午
 # @Description :
"""

from RegisterDistribute import *
from AllocateRegister import *

#你应该实现的：
#1. 算法6.3要求的，即调用6.1，6.2的相关内容实现输出

#2. 整合综合实验(只要完成1就很简单了）

# 活跃变量内容 A B Y Z U V W T  A B U V W T

#2中这里帮你处理好输入了，请自行对函数重命名
def obj_code_test(tac_path, sym_path):

    # 获取活跃信息和变量集合
    active_info_list, var_set = generate_active_info_list(tac_path, sym_path)
    active_info_list.reverse()
    # 获取AVALUE 和 RVALUE
    RVALUE, AVALUE = RVALUE_and_AVALUE_init(var_set)
    print('要开始生成目标代码了！')
    for temp in active_info_list:
        print(temp.QUA)
        print(temp.LV)
        print(temp.LN)
        print(temp.RN)
    for i in range(0, len(active_info_list)):
        # 1. 获取目标寄存器 register
        register, store_set = GETREG(active_info_list, i + 1, RVALUE, AVALUE)
        print('=====')
        print(active_info_list[i].QUA)
        print('=====')
        # 1.5 首先输出需要 ST 的指令
        for command in store_set:
            print(command)

        src1 = active_info_list[i].QUA.src1
        src2 = active_info_list[i].QUA.src2
        op = active_info_list[i].QUA.op
        des = active_info_list[i].QUA.des

        src1_address = ''
        src2_address = ''
        # 2. 确定src1 和 src2 的地址，如果在寄存器中，优先选择寄存器
        # 这里可以封装成一个函数
        for address in list(AVALUE[src1]):
            if address[0] == 'R':
                src1_address = address
                break
            else:
                src1_address = address

        for address in list(AVALUE[src2]):
            if address[0] == 'R':
                src2_address = address
                break
            else:
                src2_address = address
        # 3. 生成代码
        if src1_address != register :
            print('LD' + ' ' + register + ' ' + src1_address)
            print(op + ' ' + register + ' ' + src2_address)
        else:
            print(op + ' ' + register + ' ' + src2_address)

        # 4. AVALUE[des] = {register}, RVALUE[register] = {des}

        AVALUE[des] = set()
        AVALUE[des].add(register)
        RVALUE[register] = set()
        RVALUE[register].add(des)

        # 仅做测试
        for register_set in RVALUE:
            print('!!!!')
            print(register_set)
            print(RVALUE[register_set])
            print('!!!')

        # 5. 及时腾空不需要的src1 和 src2
        # 这里可以写成一个函数
        if active_info_list[i].LN.next == '^':
            tag = False
            register_temp = ''
            for register_set in RVALUE:
                if src1 in RVALUE[register_set]:
                    RVALUE[register_set].remove(src1)
                    register_temp = register_set
                    tag = True
                    break
            if tag:
                AVALUE[src1].remove(register_temp)

        if active_info_list[i].RN.next == '^':
            tag = False
            register_temp = ''
            for register_set in RVALUE:
                if src2 in RVALUE[register_set]:
                    RVALUE[register_set].remove(src2)
                    register_temp = register_set
                    tag = True
                    break
            if tag:
                AVALUE[src2].remove(register_temp)



obj_code_test("../tac.txt", "../symbol.txt")
