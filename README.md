# game24_python

实现的 24 点游戏求解器，使用 ToT（Train of Thought）来寻找解法。

程序参考[https://github.com/AI-FE/game24-solver](https://github.com/AI-FE/game24-solver)实现，基本就是将javascript代码用python实现，去除了原来的cache实现，主要是为了体验一下推理过程，顺便学一下python，底层AI模型基座用的是Deepseek V3模型

以下的开发思路是抄的，不是我写的，寻求javascript版本的请移步[AI-FE/game24-solver](https://github.com/AI-FE/game24-solver)

## 项目说明

24 点游戏是一个数学游戏，玩家需要使用四个数字，通过基本算术运算（加、减、乘、除）得到 24。每个数字必须且只能使用一次。

工作流程如下：

1. 输入 4 个数字
2. AI 提出可能的下一步操作（加减乘除）
3. 对每个操作后的结果进行评估：
   * 如果确定可以达到 24（bingo），返回解法
   * 如果确定无法达到 24（impossible），放弃该分支
   * 如果可能达到 24（likely），继续探索
4. 使用缓存系统避免重复评估相同的数字组合

本项目使用 AI 模型来:

1. 提出可能的运算步骤
2. 评估中间结果是否可能达到 24
3. 使用广度优先搜索找到解法

## 配置文件说明(config.yaml)
```yaml
ai:
  endpoint: [aip base url]
  api_key: [api key]
  model: [model name]
```
