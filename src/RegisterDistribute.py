# -*- coding: UTF-8 -*-
"""
 # @Project     : Object-Code-Generator
 # @File        : RegisterDistribute.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/6 9:56 上午
 # @Description :
"""

from ActiveInfoList import *

"""
你应该在这里实现：
(优先完成)
GETREG的方法：按照算法6.3要求对每个四元式分配寄存器，即GETREG(i: A:=B op C),返回一个寄存器Ri,供6.3调用
在题目要求的基础上，你可以自行添加输入参数，但需要与ObjectCode.py的同学商讨
"""


def RVALUE_and_AVALUE_init(var_set):
    """
    初始化RVALUE和AVALUE
    :return: RVALUE(寄存器使用情况字典)，AVALUE(变量存储位置情况字典)
    """
    RVAlUE = dict()
    AVALUE = dict()
    while True:
        try:
            register_amount = int(input("请设置寄存器数量："))
            if register_amount <= 0:
                raise UserWarning
            break
        except ValueError:
            print("请输入整数！")
        except UserWarning:
            print("寄存器的数量至少为1！")

    for i in range(0, register_amount):
        RVAlUE["R"+str(i)] = set()
    for var in var_set:
        AVALUE[var] = set()

    return RVAlUE,AVALUE


def check_lonely_in_rvalue(RVALUE, variate):
    """
     检查操作数是否在寄存器中，且寄存器中只有他一个
     :param RVALUE: 寄存器使用情况字典
     :param variate: (左)操作数
     :return: 寄存器
    """
    for reg in RVALUE:
        if variate in RVALUE[reg] and len(RVALUE[reg]) == 1:
            return reg
    return ''


def find_first_free_register(RVALUE):
    """
    检查是否有空寄存器中
    :param RVALUE: 寄存器使用情况字典
    :return: 寄存器
    """
    for reg in RVALUE:
        if len(RVALUE[reg]) == 0:
            return reg
    return ''


def generate_ST_code(reg,var):
    """
    生成store代码，因为抢占寄存器时可能会有store某寄存器的值到某个变量的必要性
    :param reg: 寄存器
    :param var: 变量
    :return store_code: store指令
    """
    store_code = "ST " + reg + "," + var
    return store_code


def not_be_used_later(var,active_info_list,n):
    """
    检查var变量是否会在之后被用到
    """
    # 记录var在此后是否还活跃
    var_active = "^"
    for i in range(n-2, -1, -1):
        # 只检查当前四元式前面的四元式
        activeInfoItem = active_info_list[i]
        quaternary_code = activeInfoItem.QUA
        # 从左值开始比对,比对上了就停止向前探索
        if var == quaternary_code.des:
            var_active = activeInfoItem.LV.active
            break
        elif var == quaternary_code.src1:
            var_active = activeInfoItem.LN.active
            break
        elif var == quaternary_code.src2:
            var_active = activeInfoItem.RN.active
            break

    if var_active == "^":
        return True
    return False


def used_furthest(RVALUE,active_info_list,n):
    """
    选择一个其中变量最久后才会被使用的寄存器
    :param RVALUE: 寄存器使用情况字典---dict<set>:{'R0':{'A','B'},'R1':{'C','D'},...}
    :param active_info_list: 待用/活跃信息表
    :param n: 标识等待被分配寄存器的四元式是第几个
    :return robbed_register: 被抢占的寄存器
    """
    robbed_register = "R0"
    # 记录寄存器中所存变量将来被使用的时间{'R0':12,'R1':7,......}
    used_time_list = dict()
    # 暂时初始化为都不会在将来用到，对于之后不会用到的，就设置为1000
    for i in range(0,len(RVALUE)):
        used_time_list['R'+str(i)] = 1000
    for reg in RVALUE:
        used_time = 1000
        for var in RVALUE[reg]:
            var_time = 1000
            for j in range(n-2,-1,-1):
                # 只检查当前四元式前面的四元式
                activeInfoItem = active_info_list[j]
                quaternary_code = activeInfoItem.QUA
                # 从左值开始比对,比对上了就停止向前探索
                if var == quaternary_code.des:
                    var_time = 500 if activeInfoItem.LV.next == "^" else int(activeInfoItem.LV.next)
                    break
                elif var == quaternary_code.src1:
                    var_time = 500 if activeInfoItem.LN.next == "^" else int(activeInfoItem.LN.next)
                    break
                elif var == quaternary_code.src2:
                    var_time = 500 if activeInfoItem.RN.next == "^" else int(activeInfoItem.RN.next)
                    break
            used_time = var_time if var_time <= used_time else used_time
        used_time_list[reg] = used_time
    # 找到最就久之后才会被用到的寄存器
    max_time = used_time_list["R0"]
    for reg in used_time_list:
        if used_time_list[reg] > max_time:
            max_time = used_time_list[reg]
            robbed_register = reg

    return robbed_register


def refresh_RVALUE_And_AVALUE(RVALUE,AVALUE,active_info_item,robbed_register):
    """
    选择一个最适合被抢占的寄存器之后，需要对RVALUE、AVALUE进行相关更新
    :param RVALUE: 寄存器使用情况字典---dict<set>:{'R0':{'A','B'},'R1':{'C','D'},...}
    :param AVALUE: 变量所在寄存器/主存情况字典---dict<set>:{'A':{'R0','A'},'B':{'R0'},...}
    :param active_info_item: 待用/活跃信息表项，是当前等待分配寄存器的项
    :param robbed_register: 被抢占的寄存器
    :return to_storage_code_set: 需要执行的刷到内存的指令集合
    """
    to_storage_code_set = set()

    # 四元式左值、左操作数、右操作数
    A = active_info_item.QUA.des
    B = active_info_item.QUA.src1
    C = active_info_item.QUA.src2
    # 检查寄存器中的每一个变量
    need_to_be_removed = set()
    for M in RVALUE[robbed_register]:
        # 如果M不是A，或者如果M是A又是C，但不是B并且B也不在RVALUE[Ri]中
        if M != A or (M == A and M == C and M != B and B not in RVALUE[robbed_register]):
            if M not in AVALUE[M]:
                to_storage_code_set.add("ST "+robbed_register+","+M)

            if M == B or (M == C and B in RVALUE[robbed_register]):
                AVALUE[M] = {M,robbed_register}
            else :
                AVALUE[M] = {M}
            need_to_be_removed.add(M)
            # RVALUE[robbed_register].remove(M)
            # print("ok")
    for M in need_to_be_removed:
        RVALUE[robbed_register].remove(M)
    # print("breakPoint:")
    # print(to_storage_code_set)
    return to_storage_code_set


def find_robbed_register(active_info_list,n,RVALUE, AVLAUE):
    """
    选择一个最适合被抢占的寄存器
    :param active_info_list: 待用/活跃信息表
    :param n: 表示第几个待用/活跃信息项
    :param RVALUE: 寄存器使用情况字典---dict<set>:{'R0':{'A','B'},'R1':{'C','D'},...}
    :param AVALUE: 变量所在寄存器/主存情况字典---dict<set>:{'A':{'R0','A'},'B':{'R0'},...}
    :return: 被抢占的寄存器,需要刷到内存的指令(set<str>)
    """
    to_storage_code_set = set()
    robbed_register = ""
    # 1.优先选择寄存器中的所有变量都有内存副本或者之后不活跃的寄存器
    for reg in RVALUE:
        number = 0
        for var in RVALUE[reg]:
            # 内存中有副本或者在此之后不活跃
            if var in AVLAUE[var] or not_be_used_later(var,active_info_list,n):
                number += 1
            else:
                break
        # 如果寄存器中的所有变量都有内存副本或者之后不活跃，那么就可以被抢占，而且不需要刷到内存
        if number == len(RVALUE[reg]):
            robbed_register = reg
    # 2.如果上面的方法没有找到合适的寄存器，那就只能退而求其次，选择一个里面的变量很久之后才会被用到的寄存器了
    if robbed_register == "":
        # 选择一个里面的变量很久之后才会被用到的寄存器
        robbed_register = used_furthest(RVALUE,active_info_list,n)
        to_storage_code_set = refresh_RVALUE_And_AVALUE(RVALUE,AVLAUE,active_info_list[n-1],robbed_register)
    return robbed_register,to_storage_code_set


def GETREG(active_info_list,n, RVALUE, AVALUE):
    """
    为输入的四元式返回一个存放左值的寄存器
    :param active_info_list: 待用/活跃信息表(list<ActiveInfoItem>)
    :param n: 说明是第几个待用/活跃信息项
    :param RVALUE: 寄存器使用情况字典---dict<set>:{'R0':{'A','B'},'R1':{'C','D'},...}
    :param AVALUE: 变量所在寄存器/主存情况字典---dict<set>:{'A':{'R0','A'},'B':{'R0'},...}
    :return: 一个寄存器编号（str类型），比如"R1"、"R7"等
    :return: 需要刷到内存的代码的集合，比如{"ST R1,A","ST R1,B"}
    """
    # 为了方便先把RVALUE和AVALUE作为参数使用了，后面有需要的话可以改为全局变量，而不用传参
    # 四元式
    quaternaryCode = active_info_list[n-1].QUA
    # 左值
    des = quaternaryCode.des
    # 左操作数
    leftNumber = quaternaryCode.src1
    # 尝试寻找左操作数是否有独占的寄存器
    reg = check_lonely_in_rvalue(RVALUE, leftNumber)
    if reg != '' and (leftNumber == des or active_info_list[n-1].LN.active == "^"):
        # 之后不会被使用，或者左值==左操作数
        return reg,set()
    # 尝试寻找空寄存器
    empty_reg = find_first_free_register(RVALUE)
    if empty_reg != '':
        return empty_reg,set()
    # 没办法，只能准备抢寄存器
    return find_robbed_register(active_info_list,n,RVALUE,AVALUE)


def reg_test(tac_path, sym_path):
    # 测试函数
    # active_info_list: 四元式列表(List<QuaternaryCode>)
    # var_set: 变量的集合:(set<str>)
    active_info_list, var_set = generate_active_info_list(tac_path, sym_path)
    active_info_list.reverse()
    # init
    RVALUE,AVALUE = RVALUE_and_AVALUE_init(var_set)
    for i in range(0,len(active_info_list)):
        print(GETREG(active_info_list,i+1,RVALUE,AVALUE))
        print(RVALUE)
        print(AVALUE)


# reg_test("../tac.txt", "../symbol.txt")
