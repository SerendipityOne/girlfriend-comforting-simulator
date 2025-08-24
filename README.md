# 女友安慰模拟器 🎮💕

一个基于AI的互动游戏，模拟哄女朋友开心的场景，帮助用户提升情感沟通技巧。

## 📖 项目简介

女友安慰模拟器是一个有趣的AI互动游戏，玩家需要通过恰当的话语来安慰生气的AI女朋友，让她的原谅值从初始的20分提升到60分才能通关。游戏旨在帮助用户：

- 🗣️ 提升情感沟通技巧
- 💬 学习如何表达关心和歉意
- 🎯 练习情感智能和同理心
- 🎮 在轻松的游戏环境中学习人际交往

## 🚀 快速开始

### 环境要求

- Python 3.7+
- 智谱AI API密钥 或 千问AI API密钥

### 安装依赖

```bash
pip install openai zhipuai
```

### 配置API密钥

在运行游戏前，您需要设置AI模型的API密钥。项目支持智谱AI和千问AI两种模型。

**方式一：环境变量（推荐）**

```bash
# Windows
set ZHIPUAI_API_KEY=your_zhipu_api_key_here
set DASHSCOPE_API_KEY=your_qwen_api_key_here

# Linux/macOS
export ZHIPUAI_API_KEY="your_zhipu_api_key_here"
export DASHSCOPE_API_KEY="your_qwen_api_key_here"
```

**方式二：使用.env文件**

1. 安装python-dotenv：`pip install python-dotenv`
2. 在项目根目录创建`.env`文件：

```env
ZHIPUAI_API_KEY=your_zhipu_api_key_here
DASHSCOPE_API_KEY=your_qwen_api_key_here
```

### 运行游戏

```bash
python main.py
```

## 🎮 游戏规则

### 基本玩法

1. **初始状态**：女朋友因为随机生成的理由生气，原谅值为20
2. **目标**：通过合适的话语让原谅值达到60分通关
3. **失败条件**：原谅值降到0或以下时游戏结束

### 评分机制

游戏会根据您的回复内容给出不同的分数变化：

- **+10分**：非常开心的回复，会有很多可爱表情
- **+5分**：开心的回复
- **0分**：正常回复
- **-10分**：生气的回复
- **-20分**：非常生气的回复，简短且多感叹号
- **-30分**：敷衍回复（如"哦"、"嗯"等）会直接扣30分

### 游戏提示

- 💡 真诚地道歉和表达关心
- 💝 承诺具体的改正行动
- 🎁 提出实际的补偿方案
- ❌ 避免敷衍和无意义的回复
- 🚫 不要试图争辩或推卸责任

## 🔧 技术特性

### 核心功能

- **多模型支持**：支持智谱AI（GLM系列）和千问AI（Qwen系列）
- **智能对话**：基于大语言模型的自然语言理解和生成
- **情感分析**：AI能够理解和回应不同的情感表达
- **动态评分**：实时评估用户回复的质量和情感温度
- **内容审核**：自动过滤不当内容，确保健康的对话环境

### 支持的AI模型

**智谱AI系列：**
- `glm-4.5` (默认)
- `glm-4.5-flash` (快速响应)
- `glm-4.5-plus` (增强版)
- `glm-4.5-air` (轻量版)
- `glm-4.5-airx` (超轻量版)

**千问AI系列：**
- `qwen-plus` (默认)
- `qwen-max` (最强性能)
- `qwen-turbo` (快速便宜)

### 项目架构

```
girlfriendo-comforting-simulator/
├── main.py           # 游戏主程序
├── ai_models.py      # AI模型管理器
└── README.md         # 项目说明
```

## 🛠️ 开发说明

### 核心组件

#### AIModelManager 类

`ai_models.py` 中的核心类，提供统一的AI模型调用接口：

- `chat()`: 多轮对话接口
- `simple_chat()`: 单轮对话接口
- `get_chat_with_tokens()`: 带token统计的对话
- `content_moderation()`: 内容审核功能
- `get_embedding()`: 文本嵌入向量生成

#### 游戏逻辑

`main.py` 实现了完整的游戏流程：

- 原谅值提取和跟踪
- 游戏状态判断
- 用户输入处理
- AI对话管理

### 自定义开发

您可以基于现有框架进行扩展：

```python
from ai_models import chat_with_zhipu, ai_manager

# 简单对话
response = chat_with_zhipu("你好")

# 多轮对话
messages = [
    {"role": "user", "content": "你好"}
]
response = ai_manager.chat(messages, model="glm-4.5")

# 内容审核
moderation = ai_manager.content_moderation("待审核的文本")
```

## 🔒 安全特性

- **API密钥保护**：通过环境变量管理敏感信息
- **内容审核**：自动检测和过滤不当内容
- **错误处理**：完善的异常处理机制
- **输入验证**：防止恶意输入和注入攻击

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 开发建议

- 遵循Python PEP8代码规范
- 添加适当的注释和文档
- 确保代码具备良好的可读性
- 提交前进行充分测试

## 🙋‍♂️ 常见问题

**Q: 如何获取API密钥？**
A: 
- 智谱AI：访问 [智谱AI开放平台](https://open.bigmodel.cn/) 注册获取
- 千问AI：访问 [阿里云DashScope](https://dashscope.aliyuncs.com/) 注册获取

**Q: 游戏太难/太简单怎么办？**
A: 您可以修改`main.py`中的prompt来调整游戏难度和AI女朋友的性格。

**Q: 可以添加更多AI模型吗？**
A: 可以！在`ai_models.py`中的`supported_models`字典中添加新模型，并实现对应的调用方法。

**Q: 如何修改评分规则？**
A: 修改`main.py`中的prompt部分，调整不同回复类型对应的分数变化。

---

💝 **愿这个小游戏能帮助你成为更好的沟通者！** 💝
