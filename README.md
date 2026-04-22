# 📚 1000 High-Frequency Words · 高频词汇学习系统

> 基于 **龙飞虎《6个月学会任何一种外语》** 方法论构建的英语高频词汇学习系统

![License](https://img.shields.io/badge/license-MIT-blue)
![Words](https://img.shields.io/badge/words-1000-green)
![Days](https://img.shields.io/badge/days-100-orange)
![TTS](https://img.shields.io/badge/TTS-Edge_TTS-red)

## 🎯 为什么是1000个高频词？

根据语言学研究：
- **1000个高频词** → 覆盖 **85%** 的日常口语/书面语
- **3000个高频词** → 覆盖 **98%**
- 这就是龙飞虎说的"精选高频词"策略——用最少的投入获得最大的沟通能力

## 📖 学习方法论（来自书籍 & 视频）

### 5大核心原则
| 原则 | 核心要义 |
|------|----------|
| **相关性** | 学与你生活/工作相关的内容，大脑自动筛选无关信息 |
| **工具化** | 外语是沟通工具，能传达意志比语法正确更重要 |
| **理解即获取 (Acquire)** | 听懂含义时大脑自动吸收，而非死记硬背 |
| **生理训练** | 语言涉及面部肌肉训练，需要像健身一样练嘴舌 |
| **心理状态** | 学习效率取决于状态，焦虑紧张会关闭学习通道 |

### 7把关键武器
1. **泡脑子** — 大量听，熟悉节奏和旋律
2. **含义先于单词** — 通过情境理解，不查字典
3. **大胆组合** — 像搭积木一样拼凑表达
4. **精选高频词** ← **本项目核心** — 1000词覆盖85%日常
5. **寻找"语言家长"** — AI时代我们用AI替代！
6. **面部肌肉模拟** — 观察母语者嘴型
7. **直连模式** — 建立"物体→外语单词"直接联系，跳过中文翻译

### 6个月路线图
- **第1-2周**: 泡脑子 + 救命短语 + 基本发音
- **第3周-2月**: 疯狂开口 + 逻辑连接词 + AI对话
- **第3-6个月**: 实战应用 + 阅读 + 50%日常切换为外语

---

## 🚀 项目结构

```
high-freq-words/
├── data/
│   └── frequency_1000.json    # 1000高频词库（JSON）
├── templates/
│   └── daily_template.html    # 每日HTML模板
├── scripts/
│   ├── generate.py            # 核心生成脚本
│   ├── embed_audio.py         # 音频嵌入脚本
│   └── push_notify.py         # 推送通知脚本
├── output/                     # 生成的每日HTML文件
├── audio/                      # TTS生成的音频文件
├── friends_clips/             # 老友记对话片段
├── .github/workflows/
│   └── daily.yml              # GitHub Actions 定时任务
└── README.md                   # 本文件
```

## 📝 每日内容格式

每天学习 **10个高频词**，共 **100天** 完成全部1000词。

每个单词包含：
1. **单词卡片** — 单词、音标、中文释义、难度等级
2. **标准发音** 🔊 — Edge TTS慢速发音（美式JennyNeural音色）
3. **例句朗读** 🗣️ — 用该词造的实用例句（初一水平可懂）
4. **老友记场景** 📺 — Friends原声风格对话片段（含生词标注）

## 🛠️ 本地运行

```bash
# 安装依赖
pip install edge-tts

# 测试生成第1天
python scripts/generate.py test 1

# 生成指定天数
python scripts/generate.py generate 5

# 批量生成所有天（1-100天）
python scripts/generate.py range

# 列出所有单词
python scripts/generate.py list

# 项目信息
python scripts/generate.py info
```

## ⏰ 自动化推送（GitHub Actions）

每天 **北京时间 10:00** 自动：
1. 从词库中选取当天10个高频词
2. 生成HTML页面（含TTS音频）
3. 嵌入老友记对话片段
4. 推送到 **飞书群** 和 **微信**

## 🎬 老友记对话植入

每个高频词都配一段 **Friends（老友记）** 场景对话：
- 使用角色经典口头禅和说话风格
- 标注生词和中文释义
- 适配初一英语水平

角色对照：
| 角色 | 特点 |
|------|------|
| Monica | 控制狂，爱干净，厨师 |
| Chandler | 讽刺幽默，办公室男 |
| Ross | 书呆子，古生物学家 |
| Rachel | 时尚女孩，从小富养 |
| Joey | 纯真，吃货，演员 |
| Phoebe | 古灵精怪，自由灵魂 |

## 📊 词库分级

| Level | 词数 | 说明 | 目标用户 |
|-------|------|------|----------|
| 1 | 100 | 最基础功能词（代词/be动词/介词等） | 零基础入门 |
| 2 | 300 | 核心高频动词/名词/形容词 | 初一~初三水平 |
| 3 | 400 | 中级扩展词汇 | 高中~四级水平 |
| 4 | 200 | 进阶高频词 | 六级~雅思基础 |

## 🙏 致谢

- 📖 [龙飞虎《6个月学会任何一种外语》](https://www.youtube.com/watch?v=x35aglmhBIM)
- 🎤 [Chris Lonsdale - TEDx: How to learn any language in six months](https://www.youtube.com/watch?v=dxAl0TTTiic)
- 📺 Friends / 老友记 (Warner Bros.)
- 🔊 [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - 免费神经语音合成

## 📄 License

MIT License © 2026 goodguy2
