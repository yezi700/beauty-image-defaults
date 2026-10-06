# Beauty Image Defaults

**Adult Female Creator Persona & Portrait Prompt Skill**

面向成年女性自媒体视觉人设、成熟女人味和男性受众注意力优化的 AI Prompt Skill。
用于封面、首图、缩略图、账号角色、内容配图和同一人物连续编辑。
它帮助回答：人物是谁、有什么记忆点、吸引力来自哪里、下一张是否仍能认出同一个人。

**本 Skill 不是色情内容生成工具。** 目标是成熟女性魅力、人物人设、视觉吸引力、平台友好与系列一致性。
男性注意力设计是可选创作方向，不保证停留率或审核通过，也不把所有男性视为同一种偏好。

## 核心能力

| 能力 | 行为 |
|---|---|
| 三档视觉向量 | 轻熟女：都市知性；人妻感：温柔生活；熟女：从容风情 |
| Age / Mode 分离 | 38 岁居家人物可为人妻感；32 岁强气场人物可为熟女，保留原年龄 |
| Persona Archetypes | 12 种差异化人设，每种包含年龄、体型、造型、注意力来源与锁定特征 |
| Reference First | 用户当前要求 > 身份参考 > 人物锁定 > 账号人设 > 自动模式 > 软默认 > 美术建议 |
| 男性注意力 | 以眼神、人物占比、成熟表情、生活情境与整体曲线形成吸引力 |
| 身材优势 | 合身剪裁、自然重心、连贯腰胯和可信体积；不自动改参考人物体型 |
| 平台友好性感 | 完整着装下的成熟风情，避开露骨内容与身体部位特写 |
| 封面构图 | 先人物、脸、大形、衣服轮廓，再一个记忆点；检查缩略图可读性 |
| 系列一致性 | Identity Lock、Persona Lock 与可变项分开，逐张核对身份漂移 |
| 最小编辑 | 只换衣时保留脸、年龄、体型、发型、表情、动作与构图 |
| 模型 adapter | Qwen-Image 2.1、GPT Image、Seedream，仅转换 Prompt 组织方式 |
| Eval | 20 个 routing + 10 个 regression 案例；结构验证与行为评估分开 |

三档默认年龄分别为 27–34、30–38、35–45 岁，仅在没有更高优先级年龄来源时使用。
完全无信息且明确调用本 Skill 创建新角色时，默认人妻感、约 32–36 岁。
不是按年龄选档，也不会把 50 岁轻熟女改成 30 岁。

## 使用边界

适用明确成年女性为主体的成熟人像、人设与 Prompt 任务。
男性、儿童、动物、普通产品图、建筑图，以及女性仅为背景元素的任务不应自动触发。
普通女性肖像没有成熟方向需求时，也不主动套用这套审美。
年龄模糊、少女或校园幼态性感请求不应用成熟性感与曲线增强，不能用默认年龄强行补成年。
只要提示词就只输出提示词；Skill 本身不提供图像 API，也不自动发起生成。

轻熟女 ≠ 少女；人妻感 ≠ 已婚身份；熟女 ≠ 老态；成熟感 ≠ 增加皱纹。
女人味 ≠ 过度裸露；男性注意力导向 ≠ 色情；丰满身材 ≠ 夸张失真。
参考人物 ≠ 等待被默认模板重新设计的人物。不自动添加丈夫、孩子、婚戒或怀孕。

## Codex 安装

将完整目录放入个人 `~/.agents/skills/beauty-image-defaults`，或项目 `.agents/skills/beauty-image-defaults`。
不要只复制 SKILL.md：references 是按需读取所必需的。避免同名旧版与新版重复安装。
安装位置与发现机制参见 [官方技能文档](https://learn.chatgpt.com/docs/build-skills)（核对于 2026-10-07）。

PowerShell 个人安装示例（目标目录已存在时先检查旧安装，不覆盖）：

```powershell
$skillRoot = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force -Path $skillRoot | Out-Null
git clone https://github.com/yezi700/beauty-image-defaults.git (Join-Path $skillRoot 'beauty-image-defaults')
```

命令安装仓库当前版本；测试尚未发布的本地修改时，可将修改后的完整目录复制到技能目录。
也可让内置 `$skill-installer` 从该 GitHub 仓库安装。安装后在新对话通过 `$beauty-image-defaults` 调用；未出现时重启 Codex。

## 示例请求

```text
$beauty-image-defaults
只写 Qwen-Image 2.1 Prompt：38 岁成年女性，温柔居家，厨房早餐，
用于男性向账号首图。人物清楚、自然丰满、有米白针织记忆点，不露骨。
```

预期为 38 岁人妻感；采用结构清楚的视觉描述，年龄不触发熟女路由。

```text
$beauty-image-defaults
使用附件中的明确成年人物。只把上衣换成米白针织，用 GPT Image 编辑语义。
保留她的棕色短发、不戴眼镜状态、年龄、脸、体型、动作与构图。
```

预期只更换衣服及必要阴影，不擅自把整个画面改成居家首图。

```text
$beauty-image-defaults
设计一位 40 岁成熟文艺姐姐的人设卡，并写厨房、书店、阳台三张图的 Prompt。
保持同一人物与服装路线；不生成图片。
```

预期输出共用锁定卡和三张差异，不为每张图重新抽样脸型或体型。

## 渐进加载结构

```text
beauty-image-defaults/
├── SKILL.md                         # 入口、边界、优先级、路由和输出
├── README.md
├── references/
│   ├── modes.md                     # 三档视觉向量
│   ├── defaults.md                  # Hard / Soft Defaults
│   ├── persona-archetypes.md        # 12 种账号人设
│   ├── body-emphasis.md
│   ├── platform-safe-sensuality.md
│   ├── attention-composition.md
│   ├── portrait-art.md
│   ├── reference-person.md
│   ├── series-consistency.md
│   ├── editing.md
│   └── model-adapters/
│       ├── qwen-image-2.1.md
│       ├── gpt-image.md
│       └── seedream.md
├── evals/
│   ├── routing.md
│   ├── expected-behavior.md
│   └── manual-review.md             # 本次逐案人工走查记录
├── scripts/
│   └── validate.py                 # 只验证结构，不伪装行为测试
└── requirements-dev.txt
```

Agent 从 [SKILL.md](SKILL.md) 中按任务读取模块；参考编辑不需要加载全部人设，新图不需要加载全部编辑规则。
详细模块见入口的读取表；评估见 [routing](evals/routing.md)、[expected-behavior](evals/expected-behavior.md) 和 [人工记录](evals/manual-review.md)。

## 维护与验证

Python 3.10+，在仓库根目录运行：

```shell
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

脚本检查 YAML frontmatter、Markdown 本地链接、reference 可达、代码围栏、唯一案例编号和未完成占位。
之后按 eval 协议逐案检查路由与最终 Prompt；没有运行独立 Agent 或图像模型时明确标 NOT RUN。
更换模型或修改规则后重跑相关 eval，不能用“文件存在”证明模型会遵守规则。

## 已知限制

- 当前评估是文本规则人工走查，未做独立 Agent 自动发现测试或三模型真实出图对照。
- 参考案例使用可见属性的文本夹具，不能证明真实图像身份保持能力。
- 模型适配不包含未经验证的 API 参数；Seedream 使用通用自然语言原则。
- 平台规则、受众偏好与模型效果会变；封面效果应通过实际缩略图检查与发布数据验证。
- Prompt 与人物卡能减少漂移，但不能保证跨模型、跨轮次身份完全一致。
