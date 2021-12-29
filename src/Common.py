# -*- coding: UTF-8 -*-
"""
 # @Project     : myCompilerStudy
 # @File        : Common.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/5 8:40 下午
 # @Description :
"""


class QuaternaryCode:
    """
        四元式代码，形如"W:=V+U"的四元式字符串的分解形式
        对应： 目标数(des)
              操作数1(src1)
              操作符(op，可能没有，比如A:=B）
              操作数2(src2，可能没有，比如A:=op B
    """

    def __init__(self, des: str, src1: str, op: str = "", src2: str = ""):
        """
            使用时，用.des获取目标数，用.src1获取操作数1，用.op获取操作符，用.src2获取操作数2
        """
        self.des = des
        self.src1 = src1
        self.op = op
        self.src2 = src2

    def __str__(self):
        if self.op == "":
            return self.des + ":=" + self.src1
        elif self.src2 == "":
            return self.des + ":=" + self.op + self.src1
        else:
            return self.des + ":=" + self.src1 + self.op + self.src2

    def isUnary(self) -> bool:
        """
        一元运算时，形如A:=B的
        """
        return self.src2 == ""


class VarInfo:
    """
    表示变量在信息表中的符号对，包括(待用信息，活跃信息)
    待用信息：表示该变量在什么四元式中即将被用到，如：2表示将在第2条四元式中被用到，^表示非待用
    活跃信息：表示该变量是否还需要用到，用到即活跃，y表示活跃，^表示非活跃
    """

    # 这里默认(待用信息，活跃信息)是(^,^)好一点，方便后续一元运算和赋值运算的信息表填写（HJK）
    def __init__(self, next_state: str = "^", active: str = "^"):
        self.next = next_state
        self.active = active

    def __str__(self):
        """
        形如(^,^)的字符串
        """
        return "(" + str(self.next) + "," + str(self.active) + ")"


class ActiveInfoItem:
    """
    四元式活跃信息表的表项，其成员为：
    .QUA: 四元式,QuaternaryCode类型（即包含des,src1,op,src2)
    .LV:  左值, VarInfo类型 （即四元式的des对应的符号对）
    .LN:  左操作数，VarInfo类型 （即四元式的src1对应的符号对）
    .RN   右操作数，VarInfo类型 （即四元式的src2对应的符号对）
    """

    def __init__(self):
        self.QUA = None
        self.LV = None
        self.LN = None
        self.RN = None
