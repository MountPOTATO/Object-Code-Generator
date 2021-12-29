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
    """
    用于打印的列表更新（show list存放将要打印的字符串）此处专门处理RVALUE和AVALUE的打印
    """
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
    """
    打印函数，按顺序打印中间代码列表，汇编代码列表，RVALUE列表，AVALUE列表
    """
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
    """
    更新AVALUE值，即对每个四元式中原本存在于内存的变量的AVALUE进行更新
    """

    src_set=set()
    # 自动生成原本存在内存的变量值
    qua_list=[info_list.QUA for info_list in active_info_list]
    for qua in qua_list:
        if qua.src1 not in des_set:
            src_set.add(qua.src1)
        if qua.src2 not in des_set:
            src_set.add(qua.src2)

    diff_set = src_set
    diff_set.discard("")

    print("已经存在内存中的值：", diff_set)

    #更新AVALUE
    for var in diff_set:
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

        # add: 对unary情况的处理
        if active_info_list[i].QUA.isUnary():
            qua= active_info_list[i].QUA
            #1.对A:=B的处理
            if qua.op=='':
                B=qua.src1
                isInReg=False
                for reg in RVALUE.keys():
                    if B in RVALUE[reg]:
                        #把Ri同时分配给B和A
                        RVALUE[reg].add(qua.des)
                        #存疑
                        AVALUE[qua.des].add(reg)
                        isInReg=True
                if not isInReg:
                    command_show_list.append('ST ' + register + ' ' + qua.src1)
                    RVALUE[register]={B}
                    AVALUE[B]={register}

            # 2.对A:=op B的处理
            else:
                B = qua.src1
                B_reg=""
                for reg in RVALUE.keys():
                    if B in RVALUE[reg]:
                        B_reg=reg
                #如果B的现行值也在R中，不生成LD语句
                if B_reg!=register:
                    command_show_list.append('LD ' + register + ' ' + qua.src1)
                    RVALUE[register] = {B}
                    AVALUE[B] = {register}
                command_show_list.append(operator_conversion(qua.op) +'1 '+register + ' ' + register)



        else:
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
            operator = operator_conversion(op)
            if operator != 'none':
                if src1_address != register:
                    # print('LD' + ' ' + register + ' ' + src1_address)
                    command_show_list.append('LD' + ' ' + register + ' ' + src1_address)
                    # print(operator + ' ' + register + ' ' + src2_address)
                    command_show_list.append(operator + ' ' + register + ' ' + src2_address)
                    #TODO: 正确性检查
                else:
                    # print(operator + ' ' + register + ' ' + src2_address)
                    command_show_list.append(operator + ' ' + register + ' ' + src2_address)

            #如果B'或C'为R，则删除对应的AVALUE中的寄存器
            if src1_address == register:
                AVALUE[src1].discard(register)
            if src2_address == register:
                AVALUE[src2].discard(register)

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


        if i==len(active_info_list)-1:
            # 6. 出基本块时，将除基本块仍然活跃的值存入内存
            for active_var in active_var_set:
                for register in RVALUE:
                    if active_var in RVALUE[register]:
                        AVALUE[active_var].add(active_var)
                        command_show_list.append('ST ' + register + ' ' + active_var)

        #打印一个中间代码对应表格一行的信息
        RVALUE_AVALUE_add_to_show_list(RVALUE_show_list, AVALUE_show_list, RVALUE, AVALUE)
        object_code_print_line(qua_show_list, command_show_list, RVALUE_show_list, AVALUE_show_list)



def obj_code_test(tac_path, sym_path):



    # 获取活跃信息和变量集合
    active_info_list, var_set, active_var_set = generate_active_info_list(tac_path, sym_path)
    active_info_list.reverse()

    # 初始化AVALUE 和 RVALUE
    RVALUE, AVALUE = RVALUE_and_AVALUE_init(var_set)

    # 输入上一个基本块已经存在于内存中的值
    # AVALUE = update_AVALUE(var_set, AVALUE)
    AVALUE = update_AVALUE_initial(active_info_list, AVALUE)

    # print('需要转换为目标代码的四元式有：')
    # print('==========')
    # for active_info in active_info_list:
    #     print(active_info.QUA)
    # print('==========')

    print("=========算法6.2和6.3生成寄存器分配结果和目标代码生成结果=========")
    print("{:<9} {:<10} {:<12} {:<15} ".format('中间代码',
                                               '目标代码',
                                               'RVALUE',
                                               'AVALUE'))

    obj_code_generate(active_info_list, RVALUE, AVALUE, active_var_set)
    print("==========================================================")




# obj_code_test("../tac.txt", "../symbol.txt")
