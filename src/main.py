# -*- coding: UTF-8 -*-
"""
 # @Project     : myCompilerStudy
 # @File        : main.py
 # #@Author     : mount_potato
 # @Date        : 2021/12/5 4:12 下午
 # @Description :
"""

from ActiveInfoList import generate_active_info_list

tac_path = "../tac.txt"
sym_path = "../symbol.txt"

# 算法6.1：三地址代码的待用、活跃信息表生成算法
active_info_list, act_set = generate_active_info_list(tac_path, sym_path)
# 在算法6.2输入时需要算法6.1的输出也就是active_info_list，这里可以直接引入这个list，
# list中的每一项的使用方法详见Commom.py
