# -*- coding: UTF-8 -*-
"""
 # @Project     : myCompilerStudy
 # @File        : ActiveInfoList.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/5 4:20 下午
 # @Description :
"""

from Common import *


def get_info_list_from_file(path):
    """
    读取一个存放四元式代码的文件，输出四元式代码字符串组成的列表
    :param path: 文件路径
    :return: 四元式字符串列表，如["W:=V+U","V:=T+U",....]
    """
    tac_list = []
    with open(path, mode='r', encoding="utf-8") as tac_file:
        for line in tac_file:
            tac_list.append(line.rstrip())
    return tac_list


def get_symbol_list_from_file(path):
    """
    读取一个存放符号表的文件，输出符号表字符串组成的列表
    :param path: 文件路径
    :return: 符号字符串列表，如["+","-",...]
    """
    symbol_list = []
    with open(path, mode='r', encoding="utf-8") as sym_file:
        for line in sym_file:
            symbol_list.append(line.rstrip())
    return symbol_list


def generate_var_set_and_qua_list(tac_list, symbol_list):
    """
    根据前面两个函数生成的四元式代码字符串列表，和符号字符串列表，生成变量集合和四元式列表
    :param tac_list: 四元式字符串列表，如["W:=V+U","V:=T+U",....]
    :param symbol_list: 符号字符串列表，如["+","-",...]
    :return: 一个set(),里面是所有四元式字符串列表的信息
             一个list<QuaternaryCode>，里面是每个四元式的分解信息项QuaternaryCode
    """
    var_set = set()
    qua_list = list()
    for sentence in tac_list:
        sentence = sentence.replace(":=", " ")
        op = ""
        for symbol in symbol_list:
            if symbol in sentence:
                op = symbol
            sentence = sentence.replace(symbol, " ")

        var_list = sentence.split(" ")
        if op == "":
            qua_list.append(QuaternaryCode(var_list[0], var_list[1]))
        elif len(var_list) == 2:
            qua_list.append(QuaternaryCode(var_list[0], var_list[1], op))
        elif len(var_list) == 3:
            qua_list.append(QuaternaryCode(var_list[0], var_list[1], op, var_list[2]))
        else:
            print("错误：该代码不符合三地址代码")
            exit(1)

        for i in var_list:
            var_set.add(i)

    return var_set, qua_list


def output_info_chain_dict(info_chain_dict):
    """
    打印变量名-信息链的字典
    :param info_chain_dict: 字典，key为变量，value为信息链，如C: (^,^)->(2,y)
    """
    print("=========变量名-信息链===========")
    print("{:<7} {:<7}".format('变量名', "初始状态->信息链"))
    print("-------------------------------")
    for var_key in list(info_chain_dict.keys()):
        str_list = [str(var_info) for var_info in info_chain_dict[var_key]]
        print("{:<9} {:<7}".format(var_key,
                                   "->".join(str_list)))
    print("===============================")


def output_active_info_list(act_info_list):
    """
    打印存放ActiveInfoItem的列表，对里面的ActiveInfoItem按顺序打印
    :param act_info_list: 列表，每个表项是一个ActiveInfoItem,包含四元式，左值，左操作数，右操作数
    """
    print("====================算法6.1的四元式列表======================")
    print("{:<7} {:<13} {:<10} {:<10} {:<10}".format('序号',
                                                     '四元式',
                                                     '左值',
                                                     '左操作数',
                                                     '右操作数'))
    print("----------------------------------------------------------")
    for index, item in enumerate(act_info_list):
        print("{:<8} {:<15} {:<11} {:<13} {:<10}".format("(" + str(len(act_info_list) - index) + ")",
                                                         str(item.QUA),
                                                         str(item.LV),
                                                         str(item.LN),
                                                         str(item.RN)))
    print("==========================================================")


def generate_active_info_list(tac_path, sym_path):
    """
    读取存放四元式代码的文件和存放符号表的文件
    运用三地址代码的待用、活跃信息表生成算法，生成任务要求输出的四元式列表
    :param tac_path: 存放四元式代码的文件路径
    :param sym_path: 存放符号表的文件路径
    :return: list<ActiveInfoItem>类型列表，即四元式列表
             set()活跃变量集合
    """

    # 生成四元式字符串的列表
    tac_list = get_info_list_from_file(tac_path)
    # 生成符号字符串列表
    sym_list = get_symbol_list_from_file(sym_path)
    # 生成变量集合和四元式集合(正序）
    var_set, qua_list = generate_var_set_and_qua_list(tac_list, sym_list)

    # 输入活跃变量，生成活跃变量集合
    while True:
        try:
            active_var_list = input("请输入活跃变量列表(变量间以空格隔开):").split(" ")
            active_var_set = set(active_var_list)
            # 错误检测,判断活跃变量是不是已有变量
            active_var_set.discard("")
            if len(active_var_set):
                for act_var in active_var_set:
                    if act_var not in var_set:
                        raise UserWarning
            break
        except ValueError:
            print("输入格式有误，请重试")
        except UserWarning:
            print("活跃变量不在四元式变量中，请重试")

    # 变量名-信息链 字典,dict[str]=list<VarInfo>
    info_chain_dict = dict()

    # 非待用初始状态和活跃状态（视输入的活跃变量决定)
    for var in var_set:
        info_chain_dict[var] = [VarInfo("^", "y")] if var in active_var_set else [VarInfo("^", "^")]

    # 最终要输出的四元式列表：list<QuaternaryCode>
    active_info_list = list()
    # 倒序遍历
    for index, qua in enumerate(list(reversed(qua_list))):
        active_info_item = ActiveInfoItem()

        # 四元式附加
        active_info_item.QUA = qua

        # 把符号表中des目标变量的待用信息和活跃信息附加到当前四元式.LV上
        left_value = qua.des
        active_info_item.LV = info_chain_dict[left_value][-1]
        # 把符号表中des目标变量的待用信息和活跃信息分别置为“非待用”和“非活跃”；
        info_chain_dict[qua.des].append(VarInfo("^", "^"))

        # TODO:求证A:=B和A:=op B的情况怎么处理

        # 把符号表中src1源变量和src2源变量的待用信息和活跃信息附加到四元式.LN和.RN上
        left_number, right_number = qua.src1, qua.src2
        active_info_item.LN = info_chain_dict[left_number][-1]
        if right_number != "":
            active_info_item.RN = info_chain_dict[right_number][-1]

        # 把符号表中src1源变量和src2源变量的待用信息设为当前四元式序号,活跃信息设为y
        info_chain_dict[qua.src1].append(VarInfo(str(len(qua_list) - index), "y"))
        info_chain_dict[qua.src2].append(VarInfo(str(len(qua_list) - index), "y"))

        active_info_list.append(active_info_item)

    # 输出查看结果
    output_info_chain_dict(info_chain_dict)
    output_active_info_list(active_info_list)

    return active_info_list, active_var_set, info_chain_dict


generate_active_info_list("../tac.txt", "../symbol.txt")
