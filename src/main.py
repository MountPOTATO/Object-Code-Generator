# -*- coding: UTF-8 -*-
"""
 # @Project     : myCompilerStudy
 # @File        : main.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/5 4:12 下午
 # @Description :
"""

from ActiveInfoList import generate_active_info_list
from ObjectCode import *
from DAG import *

tac_path = "../tac.txt"
sym_path = "../symbol.txt"
dag_tac_path="../dag_tac.txt"


while True:
    try:
        confirmed = int(input("请选择是否进行DAG中间代码优化:[1/0]: "))

        if confirmed==1:
            optim_dag=OptimDAG(tac_path,sym_path,dag_tac_path)
            optim_dag.optim_tac()
            obj_code_test(dag_tac_path, sym_path)
            break
        elif confirmed==0:
            obj_code_test(tac_path, sym_path)
            break
    except ValueError:
        print("输入格式有误，请重试")
    except UserWarning:
        print("出现了其他奇怪的问题")

