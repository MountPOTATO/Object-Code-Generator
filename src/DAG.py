# -*- coding: UTF-8 -*-
"""
 # @Project     : Object-Code-Generator
 # @File        : DAG.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/9 1:48 下午
 # @Description :
"""
from Common import *
from src.ActiveInfoList import get_info_list_from_file, get_symbol_list_from_file, generate_var_set_and_qua_list
from collections import namedtuple


class OptimDAG:
    def __init__(self,tac_path,sym_path):
        self.nodes_list=[]
        self.new_qua=[]
        self.tac_path=tac_path
        self.sym_path=sym_path
        self.var_set={}
        self.qua_list=[]
        self.NODE = namedtuple("NODE", 'op ID signs leftNodeID rightNodeID')

    def optim_tac(self):
        # 生成四元式字符串的列表
        tac_list = get_info_list_from_file(self.tac_path)
        # 生成符号字符串列表
        sym_list = get_symbol_list_from_file(self.sym_path)
        # 生成变量集合和四元式集合(正序）
        self.var_set, self.qua_list = generate_var_set_and_qua_list(tac_list, sym_list)

        for qua in self.qua_list:
            if qua.op in self.var_set:
                if qua.isUnary():
                    idB=self.get_NODE(qua.src1)
                    self.delete_sym(qua.des)


    def get_NODE(self,sym,leftNodeID=None,rightNodeID=None):
        if sym in self.var_set:
            for node in reversed(self.nodes_list):
                if sym==node.op and (sym=="+" or sym=="*"):
                    if (leftNodeID == node.leftNodeID and rightNodeID == node.rightNodeID) or (
                            rightNodeID == node.leftNodeID and leftNodeID == node.rightNodeID):
                        return node.ID
                if sym==node.op:
                    if leftNodeID==node.leftNodeID and rightNodeID==node.rightNodeID:
                        return node.ID
            else:
                signs=[]
                self.nodes_list.append(self.NODE(sym,len(self.nodes_list),signs,leftNodeID,rightNodeID))
                return len(self.nodes_list)-1

        else:
            for node in reversed(self.nodes_list):
                if sym in node.signs:
                    return node.ID
            else:
                signs= [sym]
                self.nodes_list.append(self.NODE(sym,len(self.nodes_list),signs,None,None))
                return len(self.nodes_list)-1

    def delete_sym(self,A):
        for node in self.nodes_list:
            if A in node.signs and A!=node.signs[0]:
                node.signs.remove(A)
                return True
        else:
            return False

    def add_to_node(self,nodeID,sym):
        if len(self.nodes_list[nodeID].signs)!=0:
            tmp=self.nodes_list[nodeID].signs[0]
            self.nodes_list[nodeID].signs[0]=sym
            self.nodes_list[nodeID].append(tmp)
        else:
            self.nodes_list[nodeID].append(sym)








