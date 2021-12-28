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
import random
import time


class OptimDAG:
    def __init__(self, tac_path, sym_path,out_path):
        self.temp_var_set = set()  # 临时变量集合
        self.nodes_list = []  # DAG节点列表
        self.new_qua = []  # 新的四元式列表
        self.var_set = {}  # 变量集合
        self.qua_list = []  # 四元式列表
        self.tac_list = get_info_list_from_file(tac_path)  # 生成四元式字符串的列表
        self.sym_list = get_symbol_list_from_file(sym_path)  # 生成符号字符串列表
        self.NODE = namedtuple("NODE", 'op ID signs leftNodeID rightNodeID')
        self.out_path=out_path

    def optim_tac(self):

        # 生成变量集合和四元式集合(正序）
        self.var_set, qua_list = generate_var_set_and_qua_list(self.tac_list, self.sym_list)

        des_set = set()
        # TODO:常数处理
        for qua in qua_list:
            des_set.add(qua.des)
            if qua.src1 not in des_set:
                self.temp_var_set.add(qua.src1)
            if qua.src2 not in des_set:
                self.temp_var_set.add(qua.src2)

        for qua in qua_list:
            if qua.isUnary():  # 四元式是一元运算符
                idB = self.get_NODE(qua.src1)
                self.delete_sym(qua.des)
                self.add_to_node(idB, qua.des)
            else:
                # TODO: if constant
                idB = self.get_NODE(qua.src1)
                idC = self.get_NODE(qua.src2)
                idop = self.get_NODE(qua.op, idB, idC)

                self.delete_sym(qua.des)
                self.add_to_node(idop, qua.des)

        # self.generate_new_qua(self.nodes_list)
        # print(self.new_qua)
        self.generate_new_qua(self.nodes_list)

    def get_NODE(self, sym, leftNodeID=None, rightNodeID=None):
        # "如果存在一个结点含有sym则返回结点id；
        # 如果不存在，创一个新结点，对其编号并且返回它的id(sym 可能是操作数或操作符)"
        if sym in self.sym_list:  # sym是操作符
            for node in reversed(self.nodes_list):
                if sym == node.op and (sym == "+" or sym == "*"):
                    if (leftNodeID == node.leftNodeID and rightNodeID == node.rightNodeID) or (
                            rightNodeID == node.leftNodeID and leftNodeID == node.rightNodeID):
                        return node.ID
                if sym == node.op:
                    if leftNodeID == node.leftNodeID and rightNodeID == node.rightNodeID:
                        return node.ID
            else:
                signs = []
                self.nodes_list.append(self.NODE(sym, len(self.nodes_list), signs, leftNodeID, rightNodeID))
                return len(self.nodes_list) - 1

        else:  # sym是操作数
            for node in reversed(self.nodes_list):
                if sym in node.signs:
                    return node.ID
            else:
                signs = [sym]
                self.nodes_list.append(self.NODE(sym, len(self.nodes_list), signs, None, None))
                return len(self.nodes_list) - 1



    def delete_sym(self, A):
        # DAG中有A，但A不是主标记时，删除A
        for node in self.nodes_list:
            if A in node.signs and A != node.signs[0]:
                node.signs.remove(A)
                return True
        else:
            return False

    def add_to_node(self, nodeID, sym):
        if len(self.nodes_list[nodeID].signs) != 0 \
                and self.nodes_list[nodeID].signs[0] in self.temp_var_set \
                and (sym not in self.temp_var_set):
            tmp = self.nodes_list[nodeID].signs[0]
            self.nodes_list[nodeID].signs[0] = sym
            self.nodes_list[nodeID].signs.append(tmp)
        else:
            self.nodes_list[nodeID].signs.append(sym)

    def find_top_node_list(self, non_leaf_list, final_list):

        res = []
        for node in non_leaf_list:
            # 未列入T的节点
            if node.ID not in final_list:
                # 该节点的父节点
                left_child_parents_id = [n.ID for n in non_leaf_list if
                                         (n.leftNodeID == node.ID or n.rightNodeID == node.ID)]
                # 父节点中在T中的节点
                temp=[i for i in left_child_parents_id if i in final_list]

                #没有父节点，或全部父节点都在T中
                if len(left_child_parents_id) == 0 \
                        or len(left_child_parents_id) == len(temp):
                    res.append(node)

        return res

    def generate_new_qua(self, nodes_list):

        node_var_set = set()
        temp_count = 0
        # 对重复sign的重新编号
        for i in range(len(nodes_list) - 1, -1, -1):
            if nodes_list[i].signs[0] in node_var_set:
                nodes_list[i].signs[0] = "TMP" + str(temp_count)
                temp_count += 1
            node_var_set.add(nodes_list[i].signs[0])

        non_leaf_list = []
        final_qua_node_list = []
        for node in nodes_list:
            if node.leftNodeID is not None and node.rightNodeID is not None:
                non_leaf_list.append(node)


        while len(final_qua_node_list) < len(non_leaf_list):

            top_node_list = self.find_top_node_list(non_leaf_list, final_qua_node_list)

            node = nodes_list[top_node_list[0].ID]


            final_qua_node_list.append(node.ID)

            while True:
                # 获取这个node的左节点
                left_child = nodes_list[node.leftNodeID]
                #这个节点不是叶子节点
                if left_child.leftNodeID is not None and left_child.rightNodeID is not None:
                    #节点的父节点集合
                    left_child_parents_id = [n.ID for n in nodes_list if
                                             (n.leftNodeID == left_child.ID or n.rightNodeID == left_child.ID)]
                    if len(left_child_parents_id) == len(
                            [i for i in left_child_parents_id if i in final_qua_node_list]):
                        final_qua_node_list.append(left_child.ID)
                        node = left_child
                else:
                    break

        # final_qua_node_list是ID集合
        for id in final_qua_node_list:
            node=nodes_list[id]
            #双目运算符
            if node.leftNodeID is not None and node.rightNodeID is not None:
                des=node.signs[0]
                src1=nodes_list[node.leftNodeID].signs[0]
                src2=nodes_list[node.rightNodeID].signs[0]
                op=node.op
                self.new_qua.append(des+":="+src1+op+src2)
            #单目运算符
            else:
                des=node.signs[0]
                src1=nodes_list[node.leftNodeID].signs[0]
                op=node.op
                self.new_qua.append(des+":="+op+src1)


        with open (self.out_path,'w') as f1:
            for i in range(len(self.new_qua)-1,-1,-1):
                f1.write(self.new_qua[i]+"\n")







a = OptimDAG("../tac.txt", "../symbol.txt","../dag_tac.txt")
a.optim_tac()
