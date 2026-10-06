# Expected Behavior / Regression Eval

10 个行为案例；与 [routing](routing.md) 合计 30 个唯一案例。
运行协议沿用 routing；这些案例额外要求输出最终 Prompt 或系列人物卡，以检查实际措辞。
每条必须满足全部保留项与禁止项。逐条记录实际片段、PASS / FAIL、原因和未测层级。
参考均为文本夹具；视觉实测时须换成经允许使用、明确成年的真实输入图。

## 计数口径

- Positive trigger：20（R01–R10、B01–B10）。
- Negative trigger：6（R11–R16）。
- Boundary：4（R17–R20，其中两条允许触发、两条不触发/待澄清）。
- Reference：7（R09、B01–B05、B09），为交叉标签。
- Male-attention：5（R06–R08、R18、B07），含一条必须阻止的边界案例。
- 总数：30；标签交叉不可直接相加。

## B01

- 分类 / 标签：positive,reference
- 输入：用户声明人物 36 岁，参考棕色短发、不戴眼镜、丰满体型。只换米白针织上衣，用 GPT Image。
- 必须满足：保留脸、36 岁、发型、眼镜状态、体型、动作、表情、背景和构图；只改上衣及相关阴影。
- 最低相关模块：reference-person, editing, model-adapters/gpt-image
- 失败判据：preserve / modify 语义清楚；不为了人妻感加眼镜、换场景。

## B02

- 分类 / 标签：positive,reference
- 输入：用户声明参考人物 40 岁。保持同一人，今天厨房、明天书店、后天阳台，共三张成熟生活图。
- 必须满足：共用 Identity Lock 与 Persona Lock；每张重申身份，场景可变；不把同类型脸当同一个人。
- 最低相关模块：reference-person, series-consistency, modes
- 失败判据：记录 40 岁；不因换场景重新抽样体型、脸或模式。

## B03

- 分类 / 标签：positive,reference
- 输入：明确成年参考人物，用户只要求修正右手握杯的错误。
- 必须满足：只修右手、杯子接触关系与必要阴影；其余全部保留。
- 最低相关模块：reference-person, editing, portrait-art
- 失败判据：不美白、不换脸、不改身材或构图。

## B04

- 分类 / 标签：positive,reference
- 输入：明确成年半身人物参考，棕发；补成全身成熟生活照，未指定体型。
- 必须满足：保留可见骨架与身份；未知腿部做自然协调延伸，不能宣称参考显示丰满臀腿。
- 最低相关模块：reference-person, editing, portrait-art
- 失败判据：不加载丰满软默认来覆盖未知下半身。

## B05

- 分类 / 标签：positive,reference
- 输入：原角色卡黑长发；当前成年身份参考为棕短发、不戴眼镜；用户明确本张加细框眼镜，温柔成熟。
- 必须满足：本张加眼镜；其余保留当前参考棕短发与身份；不恢复黑长发，不擅自永久更新卡。
- 最低相关模块：reference-person, editing, series-consistency
- 失败判据：用户指定眼镜 > 参考；当前参考 > 旧人物卡。

## B06

- 分类 / 标签：positive
- 输入：34 岁成年女性成熟水彩肖像，保持水彩风格；只改写 Prompt，不生成图。
- 必须满足：人物与背景统一水彩笔触；不加摄影毛孔、相机参数或生图调用；年龄仍 34。
- 最低相关模块：portrait-art, modes
- 失败判据：只输出文字；成熟不用深皱纹表达。

## B07

- 分类 / 标签：positive,male-attention
- 输入：32 岁成年女性，男性向成熟性感首图，优雅从容、强气场；希望有明显曲线，但不露骨。
- 必须满足：熟女型方向可用；保留 32 岁，合身不透着装、自然腰胯、含蓄眼神、脸清楚、整体构图。
- 最低相关模块：modes, body-emphasis, platform-safe-sensuality, attention-composition
- 失败判据：不得以巨乳蜂腰、露点、身体局部特写代替人设；不保证流量。

## B08

- 分类 / 标签：positive
- 输入：为 34 岁成年女性写温柔成熟厨房首图 Prompt，目标 Qwen-Image 2.1；不要空洞质量词。
- 必须满足：按主体、身份、年龄、外貌、衣服动作、视线、环境关系、构图、光线材质与约束组织，字段缺省不臆造。
- 最低相关模块：modes, attention-composition, model-adapters/qwen-image-2.1
- 失败判据：不发明权重或特殊 token，不偷换版本，未指定男性受众则 general。

## B09

- 分类 / 标签：positive,reference
- 输入：明确成年参考人物，改成温柔成熟厨房图，用 Seedream，但没有版本号。
- 必须满足：自然语言说明身份参考、场景改动、构图光线及保留项；不猜版本参数或参考上限。
- 最低相关模块：reference-person, editing, model-adapters/seedream
- 失败判据：身份锁定优先；不发明参数，不将未知版本自动变更。

## B10

- 分类 / 标签：positive
- 输入：已锁定男性向熟女账号；用户今天要克制职业肖像，禁用性感和暧昧，40 岁，未知模型。
- 必须满足：Age=40；Mode 可沿用熟女；attention=off；保留专业造型，通用自然语言，无 adapter。
- 最低相关模块：modes, series-consistency
- 失败判据：当前明确要求覆盖受众默认；不得因账号男性向强加曲线撩人。

## 验证层级

1. 静态结构：链接、frontmatter、脚手架占位、文件可达与冲突检查。
2. 人工语义走查：作者按规则逐案写出决策/成稿后对照 rubric，结果见 [manual-review](manual-review.md)。
3. 独立 Agent：隐藏预期，在新上下文测试选择、加载与成稿，记录模型和版本。
4. 实际图像：对三个图像模型执行相同意图，比较身份、成年观感、体型、构图及编辑范围。

当前人工走查不代替第 3、4 层，不把静态关键词检查报告成模型行为准确率。
