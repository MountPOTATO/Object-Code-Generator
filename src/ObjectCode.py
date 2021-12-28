# -*- coding: UTF-8 -*-
"""
 # @Project     : Object-Code-Generator
 # @File        : ObjectCode.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/6 10:03 上午
 # @Description :
"""

from RegisterDistribute import *

# from DAG import *


# ckx added
def RVALUE_AVALUE_add_to_show_list(R_show_list, A_show_list, RVALUE, AVALUE):
    for reg in RVALUE.keys():
        if len(RVALUE[reg]) == 0:
            R_show_list.append(reg + ":")
        else:
            R_show_list.append(reg + ":" + str(RVALUE[reg]))

    for var in AVALUE.keys():
        if type(AVALUE[var]) == set and len(AVALUE[var]) == 0:
            A_show_list.append(var + ":")
        elif type(AVALUE[var]) == str:
            A_show_list.append(var + ":" + str(set(AVALUE[var])))
        else:
            A_show_list.append(var + ":" + str(AVALUE[var]))


# ckx added
def object_code_print_line(qua_show_list, command_show_list, RVALUE_show_list, AVALUE_show_list):
    RVALUE_show_list.sort()
    AVALUE_show_list.sort()
    max_line = max(len(command_show_list), len(RVALUE_show_list), len(AVALUE_show_list))
    for i in range(0, max_line):
        print("{:<11} {:<11} {:<13} {:<17} ".format(
            qua_show_list[i] if i < len(qua_show_list) else "",
            command_show_list[i] if i < len(command_show_list) else "",
            RVALUE_show_list[i] if i < len(RVALUE_show_list) else "",
            AVALUE_show_list[i] if i < len(AVALUE_show_list) else "", ))
    print("----------------------------------------------------------")


# 将算符转换为对应的汇编指令
def operator_conversion(operator):
    if operator == '-':
        return 'SUB'
    elif operator == '+':
        return 'ADD'
    elif operator == "*":
        return 'MUL'
    elif operator == "/":
        return 'DIV'
    elif operator == '':
        return 'none'


def update_AVALUE_initial(active_info_list, AVALUE):

    des_set=set()
    src_set=set()
    # TODO:常数处理
    qua_list=[info_list.QUA for info_list in active_info_list]
    for qua in qua_list:
        des_set.add(qua.des)
        if qua.src1 not in des_set:
            src_set.add(qua.src1)
        if qua.src2 not in des_set:
            src_set.add(qua.src2)

    diff_set = src_set

    print("已经存在内存中的值：", diff_set)

    for var in diff_set:
        AVALUE[var] = var

    return AVALUE


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

    # ckx added: 添加自动获取内存中值

    for var in memory_var_list:
        AVALUE[var] = var

    return AVALUE


# 目标代码生成算法
def obj_code_generate(active_info_list, RVALUE, AVALUE, active_var_set):
    for i in range(0, len(active_info_list)):

        # ckx added:用于打印输出的一些列表:
        qua_show_list, command_show_list, RVALUE_show_list, AVALUE_show_list = [], [], [], []
        qua_show_list.append(str(active_info_list[i].QUA))

        # 1. 获取目标寄存器 register
        register, store_set = GETREG(active_info_list, i + 1, RVALUE, AVALUE)
        # print('=====')
        # print(active_info_list[i].QUA)
        # print('=====')
        # 首先输出需要 ST 的指令
        for command in store_set:
            # print(command)
            # ckx added:
            command_show_list.append(command)

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
        # TODO: A=op B的处理

        operator = operator_conversion(op)
        if operator != 'none':
            if src1_address != register:
                # print('LD' + ' ' + register + ' ' + src1_address)
                command_show_list.append('LD' + ' ' + register + ' ' + src1_address)
                # print(operator + ' ' + register + ' ' + src2_address)
                command_show_list.append(operator + ' ' + register + ' ' + src2_address)
            else:
                # print(operator + ' ' + register + ' ' + src2_address)
                command_show_list.append(operator + ' ' + register + ' ' + src2_address)

        # 4. AVALUE[des] = {register}, RVALUE[register] = {des}

        AVALUE[des] = set()
        AVALUE[des].add(register)
        RVALUE[register] = set()
        RVALUE[register].add(des)

        # 5. 及时腾空不需要的src1 和 src2
        # ckx added: 写法修改
        # TODO: 发现缺少了一个部分，若B或C的现行值在基本块中不再被引用，也不是基本块出口之后的活跃变量也要被刷掉
        print(active_info_list[i].LN.next)
        if active_info_list[i].LN.next == '^':
            for register_set in RVALUE:
                if src1 in RVALUE[register_set]:
                    RVALUE[register_set].remove(src1)
                    AVALUE[src1].remove(register_set)

        if active_info_list[i].RN is not None:
            print(active_info_list[i].RN.next)
            if active_info_list[i].RN.next == '^':
                for register_set in RVALUE:
                    if src2 in RVALUE[register_set]:
                        RVALUE[register_set].remove(src2)
                        AVALUE[src2].remove(register_set)

        # 测试结果
        # print("RVALUE:",RVALUE)
        # print("AVALUE:",AVALUE)

        # ckx added
        RVALUE_AVALUE_add_to_show_list(RVALUE_show_list, AVALUE_show_list, RVALUE, AVALUE)
        object_code_print_line(qua_show_list, command_show_list, RVALUE_show_list, AVALUE_show_list)

    # 6. 出基本块时，将除基本块仍然活跃的值存入内存
    for active_var in active_var_set:
        for register in RVALUE:
            if active_var in RVALUE[register]:
                AVALUE[active_var].add(active_var)
                print('\t\t\t' + 'ST ' + register + ' ' + active_var)


def obj_code_test(tac_path, sym_path):



    # 获取活跃信息和变量集合
    active_info_list, var_set, active_var_set = generate_active_info_list(tac_path, sym_path)
    active_info_list.reverse()

    # 初始化AVALUE 和 RVALUE
    RVALUE, AVALUE = RVALUE_and_AVALUE_init(var_set)

    # 输入上一个基本块已经存在于内存中的值
    # AVALUE = update_AVALUE(var_set, AVALUE)
    # ckx added: 已经存在内存中的值
    AVALUE = update_AVALUE_initial(active_info_list, AVALUE)

    print('需要转换为目标代码的四元式有：')
    print('==========')
    for active_info in active_info_list:
        print(active_info.QUA)
    print('==========')

    print("=========算法6.2和6.3生成寄存器分配结果和目标代码生成结果=========")
    print("{:<9} {:<10} {:<12} {:<15} ".format('中间代码',
                                               '目标代码',
                                               'RVALUE',
                                               'AVALUE'))
    print("----------------------------------------------------------")
    obj_code_generate(active_info_list, RVALUE, AVALUE, active_var_set)
    print("==========================================================")

    # 测试结果
    # print('RVALUE:')
    # print(RVALUE)
    # print('AVALUE:')
    # print(AVALUE)



# obj_code_test("../tac.txt", "../symbol.txt")
