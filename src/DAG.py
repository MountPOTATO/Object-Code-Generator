# -*- coding: UTF-8 -*-
'''
 # @Project     : Object-Code-Generator
 # @File        : DAG.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/28 7:36 下午
 # @Description :
'''

# -*- coding: UTF-8 -*-

from Common import *
from ActiveInfoList import get_info_list_from_file, get_symbol_list_from_file, generate_var_set_and_qua_list
from collections import namedtuple


class OptimDAG:
    def __init__(self,tac_path,sym_path):
        self.nodes_list=[]      #DAG节点列表
        self.new_qua=[]         #新的四元式列表
        self.tac_path=tac_path  #三地址代码
        self.sym_path=sym_path  #符号表
        self.var_set={}         #变量集合
        self.qua_list=[]        #四元式列表
        self.NODE = namedtuple("NODE", 'op ID signs leftNodeID rightNodeID')

    def optim_tac(self):
        # 生成四元式字符串的列表
        tac_list = get_info_list_from_file(self.tac_path)
        # 生成符号字符串列表
        sym_list = get_symbol_list_from_file(self.sym_path)
        # 生成变量集合和四元式集合(正序）
        self.var_set, self.qua_list = generate_var_set_and_qua_list(tac_list, sym_list)



        for info in self.qua_list:
            qua=info.QUA
            if qua.op in self.var_set:
                if qua.isUnary(): #四元式是一元运算符
                    idB=self.get_NODE(qua.src1)
                    self.delete_sym(qua.des)
                    self.add_to_node(idB,qua.src1)
                else:
                    #TODO: if constant
                    idB=self.get_NODE(qua.src1)
                    idC=self.get_NODE(qua.src2)
                    idop=self.get_NODE(qua.op,idB,idC)
                    self.delete_sym(qua.des)
                    self.add_to_node(idop,qua.des)

        self.generate_new_qua(self.nodes_list)



    def get_NODE(self,sym,leftNodeID=None,rightNodeID=None):
        #"如果存在一个结点含有sym则返回结点id；如果不存在，创一个新结点，对其编号并且返回它的id(sym 可能是操作数或操作符)"
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

        else: #sym是操作数
            for node in reversed(self.nodes_list):
                if sym in node.signs:
                    return node.ID
            else:
                signs= [sym]
                self.nodes_list.append(self.NODE(sym,len(self.nodes_list),signs,None,None))
                return len(self.nodes_list)-1

    def generate_new_qua(self,NODES):
        print(NODES)
        for node in NODES:
            print(node)

    def delete_sym(self,A):
        #DAG中有A，但A不是主标记时，删除A
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




a=OptimDAG("../tac.txt","../symbol.txt")
a.optim_tac()