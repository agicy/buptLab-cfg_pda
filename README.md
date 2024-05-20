# buptLab-cfg_pda

这个仓库包含了北京邮电大学 2023-2024 春季学期《形式语言与自动机》课程实验——上下文无关文法与下推自动机的相关代码和报告（见 Release）。

## 文件结构

```
.
├── LICENSE                            # 许可证文件
├── README.md                          # 项目简介文件
├── requirements.txt                   # 项目依赖文件
├── src                                # 源代码目录
│   ├── algorithm                            # 算法模块
│   │   ├── eliminate_epsilon_production.py        # 消除 epsilon 产生式算法
│   │   ├── eliminate_unit_production.py           # 消除单产生式算法
│   │   ├── eliminate_useless_symbol.py            # 消除无用符号算法
│   │   ├── transfer_epda_to_cfg.py                # 空栈接受 PDA 转 CFG 算法
│   │   └── transfer_fpda_to_epda.py               # 终态接受 PDA 转空栈接受 PDA 算法
│   ├── datastructure                        # 数据结构模块
│   │   ├── cfg.py                                 # 上下文无关文法（CFG）实现
│   │   └── pda.py                                 # 下推自动机（PDA）实现
│   ├── exceptions.py                        # 自定义异常类
│   └── main.py                              # 主程序入口
└── test                               # 测试代码目录
    ├── test_cfg.py                           # 测试 CFG 模块
    ├── test_eliminate_epsilon_production.py  # 测试消除 epsilon 产生式算法
    ├── test_eliminate_unit_production.py     # 测试消除单产生式算法
    ├── test_eliminate_useless_symbol.py      # 测试消除无用符号算法
    └── test_pda_to_cfg.py                    # 测试空栈接受 PDA 转 CFG 算法
```
