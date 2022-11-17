# User Manual 目标代码生成

 Tongji Univ. SSE Compilers Principle coursework demo: generating object code

启动说明：切换到本项目根目录src文件夹下，python启动即可:

```shell
cd ./Object-Code-Generator
python main.py
```

输入说明：

1. `tac.txt` 原始三地址代码的文件形式输入，格式和课件中一致，如果格式有误将进行错误提醒

2. `symbol.txt` 符号表输入，表示三地址代码可以支持处理的运算符
3. `dag_tac.txt` 在选择了DAG代码优化模式的情况下使用，代替tac.txt作为输入文件
4. 命令行输入：选择是否进行DAG代码优化(0为否，1为是)，输入活跃变量，设定寄存器个数，。如果格式有误将进行错误提醒并要求使用者重新输入



要点：

1. 选择DAG代码生成模式时将自动根据 `tac.txt` 中的三地址代码进行重排（必要时生成tmp节点），并将结果存储在 `dag_tac.txt` 中，经过DAG代码优化后生成的汇编代码性能将优于未优化的情况
2. 输入活跃变量列表后，会自动生成“待用-活跃信息表”，这将作为GETREG算法和目标代码生成算法的输入
3. 为了方便使用，这里将自动扫描出“本身已经在内存”中的变量（即第一次出现时不作为四元式的左值）
