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


# 将算符转换为对应的汇编指令
def operator_conversion(operator):
    if operator == '-':
        return 'SUB'
    elif operator == '+':
        return 'ADD'
    elif operator == '':
        return 'none'


# 更新AVALUE, 里面主要存储上一个基本块结束之后存在内存中的值
def update_AVALUE(var_set, AVALUE):
    while True:
        try:
            memory_var_list = input("请输入已经存在于内存中的值: ").split(" ")
            memory_var_set = set(memory_var_list)
            # 错误检测,判断活跃变量是不是已有变量
            memory_var_set.discard("")
            if len(memory_var_set):
                for var in memory_var_list:
                    if var not in var_set:
                        raise UserWarning
            break
        except ValueError:
            print("输入格式有误，请重试")
        except UserWarning:
            print("此变量不是活跃变量，请重试")

    for var in memory_var_list:
        AVALUE[var] = var

    return AVALUE


# 目标代码生成算法
def obj_code_generate(active_info_list, RVALUE, AVALUE, active_var_set):
    for i in range(0, len(active_info_list)):
        # 1. 获取目标寄存器 register
        register, store_set = GETREG(active_info_list, i + 1, RVALUE, AVALUE)
        # print('=====')
        # print(active_info_list[i].QUA)
        # print('=====')
        # 首先输出需要 ST 的指令
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
                if src1 in RVALUE[address]:
                    src1_address = address
                    break
            else:
                src1_address = address
        if src2 != '':
            for address in list(AVALUE[src2]):
                if address[0] == 'R':
                    src2_address = address
                    break
                else:
                    src2_address = address
        # 3. 生成代码
        operator = operator_conversion(op)
        if operator != 'none':
            if src1_address != register:
                print('LD' + ' ' + register + ' ' + src1_address)
                print(operator + ' ' + register + ' ' + src2_address)
            else:
                print(operator + ' ' + register + ' ' + src2_address)

        # 4. AVALUE[des] = {register}, RVALUE[register] = {des}

        AVALUE[des] = set()
        AVALUE[des].add(register)
        RVALUE[register] = set()
        RVALUE[register].add(des)

        # 5. 及时腾空不需要的src1 和 src2
        if active_info_list[i].LN.next == '^':
            for register_set in RVALUE:
                if src1 in RVALUE[register_set]:
                    RVALUE[register_set].remove(src1)
                    AVALUE[src1].remove(register_set)

        if active_info_list[i].RN is not None:
            if active_info_list[i].RN.next == '^':
                for register_set in RVALUE:
                    if src2 in RVALUE[register_set]:
                        RVALUE[register_set].remove(src2)
                        AVALUE[src2].remove(register_set)

        # 测试结果
        # print(RVALUE)
        # print(AVALUE)

    # 6. 出基本块时，将除基本块仍然活跃的值存入内存
    for active_var in active_var_set:
        for register in RVALUE:
            if active_var in RVALUE[register]:
                AVALUE[active_var].add(active_var)
                print('ST ' + register + ' ' + active_var)


def obj_code_test(tac_path, sym_path):
    # 获取活跃信息和变量集合
    active_info_list, var_set, active_var_set = generate_active_info_list(tac_path, sym_path)
    active_info_list.reverse()

    # 初始化AVALUE 和 RVALUE
    RVALUE, AVALUE = RVALUE_and_AVALUE_init(var_set)

    # 输入上一个基本块已经存在于内存中的值
    AVALUE = update_AVALUE(var_set, AVALUE)

    print('需要转换为目标代码的四元式有：')
    print('=====')
    for active_info in active_info_list:
        print(active_info.QUA)
    print('=====')

    print('目标代码如下:')
    obj_code_generate(active_info_list, RVALUE, AVALUE, active_var_set)

    # 测试结果
    # print('RVALUE:')
    # print(RVALUE)
    # print('AVALUE:')
    # print(AVALUE)
obj_code_test("../tac.txt", "../symbol.txt")
