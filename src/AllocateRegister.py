# -*- coding: UTF-8 -*-

"""
 @author : lxy
 @description : 根据获得的三地址代码列表，为四元式分配寄存器。
"""

from Common import *
from ActiveInfoList import *


def create_rvalue_and_avalue(active_info_list):
    """
     创建寄存器数组

     :return: 寄存器数组
    """
    while True:
        n = input("请输入寄存器数量：")
        try:
            n = int(n)
            print(n)
            break
        except ValueError:
            print("输入格式有误，请重试")
    Rvalue = []
    Avalue = []
    for i in range(n):
        rvalue_item = RvalueItem()
        rvalue_item.Index = i
        Rvalue.append(rvalue_item)
    return Rvalue, n, Avalue


def get_first_free_register(Rvalue):
    """
     获得第一个空闲的寄存器

     :param: 寄存器数组
     :return: 寄存器
    """
    for r in Rvalue:
        if len(r.valueItem) == 0:
            return r
    return None


def get_unfree_register(Rvalue, Avalue, info_chain_dict, n):
    next_used = n + 1
    latest_used_register = None
    for r in Rvalue:
        in_memory, avalue_item = check_avalue_in_memory(Avalue, r.Index)
        if in_memory:
            return r
        else:
            var_info = info_chain_dict[r.Index][len(info_chain_dict[r.Index]) - 1]
            if var_info.next == '^':
                next_used = -1
                latest_used_register = r
            elif var_info.next < next_used:
                next_used = var_info.next
                latest_used_register = r
            else:
                pass
    return r


def check_in_rvalue(Rvalue, src):
    """
     检查操作数是否在寄存器中，且寄存器中只有他一个

     :param: 寄存器数组
     :param: 操作数
     :return: 寄存器
    """
    for r in Rvalue:
        if src in r.valueItem and len(r.valueItem) == 1:
            return r
    return None


def check_is_used_after(LN):
    """
     :param: VarInfo
     :return: 接下来是否会用到
    """
    if LN.next == '^' and LN.active == '^':
        return True
    return False


# def preempt_unavaliable_register(registers, qua, active_var_set):
def check_avalue_in_memory(Avalue, src):
    for a in Avalue:
        if a.Index == src:
            if src in a.valueItem:
                return True, a
            else:
                return False, a

    avalue_src_item = AvalueItem()
    avalue_src_item.Index = src
    avalue_src_item.valueItem.append(src)
    Avalue.append(avalue_src_item)
    return True, avalue_src_item


def allocate_register(active_info, Avalue, Rvalue, n, info_chain_dict):
    quaternary_code = active_info.QUA
    src1 = quaternary_code.src1
    src2 = quaternary_code.src2
    des = quaternary_code.des
    LN = active_info.LN

    # 获得AVALUE[r]
    in_memo_src1, avalue_item_src1 = check_avalue_in_memory(Avalue, src1)
    in_memo_src2, avalue_item_src2 = check_avalue_in_memory(Avalue, src2)

    src1_rvalue_item = check_in_rvalue(Rvalue, src1)
    first_free_register = get_first_free_register(Rvalue)

    register_allocate_item = RegisterAllocateItem()
    register_allocate_item.QUA = quaternary_code

    if src1_rvalue_item or src1 == des or check_is_used_after(LN):
        return src1_rvalue_item
    elif first_free_register:
        return first_free_register
    else:
        return get_unfree_register(Rvalue, Avalue, info_chain_dict, n)


def control_allocate_register(tac_path, sym_path):
    # 获得寄存器数量与寄存器数组
    Rvalue, n, Avalue = create_rvalue_and_avalue()
    # 获得活跃列表
    active_info_list, active_var_set, info_chain_dict = generate_active_info_list(tac_path, sym_path)
    # 转置
    active_info_list = active_info_list.reverse()


if __name__ == '__main__':
    tac_path = "../tac.txt"
    sym_path = "../symbol.txt"
    allocate_register(tac_path, sym_path)
