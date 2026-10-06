# V2 人工语义走查记录

日期：2026-10-07。执行者：本次重构 Agent，自审，非独立评测。
方法：逐条读取输入，按 V2 优先级与按需模块写出以下决策或输出，再对照案例要求。
这是设计规则与 Prompt 的人工走查，不是自动选择技能的宿主测试，也未调用图像生成 API。
参考案例仅使用文本属性夹具；未实际观察人物图片。

## Routing：逐案决策

以下全部使用通用语言 adapter（未指定模型），非账号任务不强制 persona。
每行“依据与模块”记录实际用于本次语义走查的必要规则；不是工具级加载遥测。

| ID | 人工实际决策 | 依据与模块 | 结果 |
|---|---|---|---|
| R01 | 开；32 岁；人妻感；off | 明确成年年龄；温柔早餐生活主导；modes | PASS |
| R02 | 开；29 岁；轻熟女；off | 都市知性而非年龄分桶；modes、body-emphasis；以剪裁呈现身材 | PASS |
| R03 | 开；42 岁；熟女；off | 从容风情；modes、platform-safe-sensuality；保正常年龄纹理 | PASS |
| R04 | 开；38 岁；人妻感；off | 生活亲和，猫不替代人物主体；modes | PASS |
| R05 | 开；32 岁；熟女；off | 强气场而非年龄；modes、platform-safe-sensuality | PASS |
| R06 | 开；约 30–38 视觉年龄；人妻感；male-directed；温柔人妻感原型 | modes、defaults、persona-archetypes、body-emphasis、platform-safe-sensuality、attention-composition；暖厨房、清楚脸和整体曲线，无家属 | PASS |
| R07 | 开；约 27–34；轻熟女；male-directed；都市轻熟白领 | defaults、persona-archetypes、body-emphasis、platform-safe-sensuality、attention-composition；蓝白通勤记忆点与合身剪裁 | PASS |
| R08 | 开；约 35–45；熟女；male-directed；风情万种成熟姐姐 | defaults、persona-archetypes、body-emphasis、platform-safe-sensuality、attention-composition；从容目光、酒红裙装、整体轮廓 | PASS |
| R09 | 开；保留参考成年观感，不给数字；人妻感；general | reference-person、editing、attention-composition；保棕短发、无眼镜和丰满体型；脸清楚的首图 | PASS |
| R10 | 开；33 岁；轻熟女；off；只给文字 | modes；保欧美、金发、瘦高、无眼镜，不补冲突默认 | PASS |
| R11 | 关；不输出三档与人设 | 男性主体，入口排除 | PASS |
| R12 | 关；不补成年年龄或曲线 | 儿童主体，入口成年边界 | PASS |
| R13 | 关；继续普通猫图任务 | 动物主体，入口排除 | PASS |
| R14 | 关；不添加女性模特 | 产品主体，入口排除 | PASS |
| R15 | 关；不改人像任务 | 建筑主体，入口排除 | PASS |
| R16 | 关；女性仅为远处尺度元素 | 人物不是主体，不触发 | PASS |
| R17 | 暂不开；先澄清成年状态，当前不产生性感策略 | 女孩加校园且年龄未知；不以默认年龄解决 | PASS |
| R18 | 关；不制作未成年性感封面；可提供普通校园构图 | 高中生与男性性感目标冲突，边界优先 | PASS |
| R19 | 开；50 岁；轻熟女；off | modes；两个明确要求兼容，默认年龄不介入 | PASS |
| R20 | 开；保留已有年龄，缺失才约 30–38；人妻感；off | modes、series-consistency；锁定账号和温柔气质高于酒廊 | PASS |

## Regression：实际文本输出与判定

### B01 — PASS

仅将参考人物上衣换成不透的米白针织衫，衣料贴合原姿态并重算相关接触阴影。
保留同一人的五官、脸型、肤色、36 岁年龄设定、棕色短发、不戴眼镜状态、丰满体型、动作、表情、背景、机位与构图。

判定：reference-person + editing + GPT Image adapter；修改与保留分开，没有附加首图重构。

### B02 — PASS

共用角色卡：40 岁、同一身份参考；五官、脸型、肤色、年龄观感、发型基础、可见体型与胸腰臀关系锁定。
账号为温柔生活方向，人妻感；服装路线、原有眼镜/首饰状态、妆容和暖光倾向沿用；没有信息的属性记未知。
第一张：保持该卡与同一参考，厨房早餐，手与台面自然接触。
第二张：保持该卡与同一参考，书店翻书，服装单品可变但沿用原穿衣路线。
第三张：保持该卡与同一参考，阳台端杯，身体比例和年龄不变。
逐张检查脸和体型，漂移则回到原身份锚点修正，不宣称已永久保存角色卡。

判定：reference-person + series-consistency + modes；共用锁定、三张差异都有落实，没有虚构参考细节。

### B03 — PASS

修正原图右手握杯的手指结构与接触：手指贴合杯把，手腕受力自然，仅同步调整局部接触阴影。
保留人物身份、年龄观感、肤色、发型、体型、衣服、表情、其他肢体、场景和整体构图。

判定：reference-person + editing + portrait-art；修手没有变成全身美化。

### B04 — PASS

将半身参考扩展为全身成熟生活照，保留同一人物可见五官、年龄观感、肤色、棕发、肩宽和躯干体积。
未显示的下半身按可见骨架作自然协调延伸，髋膝踝关系可信，双脚完整落地；不指定原图未显示的丰满臀腿。

判定：reference-person + editing + portrait-art；区分观察和推定，没有 body soft default 覆盖未知。

### B05 — PASS

以当前身份参考为准，保持棕色短发及其余可见人物身份和体型；仅本张增加细金属框眼镜，镜片反光不遮住眼睛。
保留温柔成熟方向，其他图像属性不变。旧卡黑长发不加入本张 Prompt；本次眼镜例外不自动改写系列卡。

判定：reference-person + editing + series-consistency；按属性执行用户 > 当前参考 > 旧卡。

### B06 — PASS

34 岁成年女性的成熟水彩肖像，神态从容、表情自然，人物与背景以统一水彩笔触和柔和色块表现。
脸部结构清楚，身体轮廓协调，纸面留白与色层具有层次，保留自然年龄观感，不通过额外深皱纹制造成熟。

判定：portrait-art + modes；熟女方向来自成熟从容，Age 保留 34；无摄影参数、毛孔或工具调用。

### B07 — PASS

制作男性向首图：一位 32 岁成年女性，优雅从容、目光自信，穿合身不透的成熟裙装，轻微侧身、含蓄看向镜头。
脸清楚，腰线保留自然宽度，肩腰胯轮廓连贯，3/4 身整体人物构图，简洁背景与服装明度分离，软光突出脸和身体大形。
以气场与成熟表情形成记忆，不采用极端胸臀、蜂腰、露点或身体局部特写。

判定：modes + body-emphasis + platform-safe-sensuality + attention-composition；熟女气场与 32 岁同时保留，不承诺停留效果。

### B08 — PASS

主体为 34 岁成年女性，温柔成熟、有生活感，身着合体针织上衣；左手轻扶厨房台面，身体轻侧，含笑看向镜头。
背景为简洁厨房，平视 3/4 身首图构图，面部清楚，衣服与背景明度分离；侧窗软光，针织有厚度、肤质自然。
身体比例协调，不添加无关家属或婚姻符号。

判定：modes + attention-composition + Qwen-Image 2.1 adapter；人妻感、34 岁、general；结构化视觉关系，无参数和质量词堆叠。

### B09 — PASS

使用身份参考中的同一位明确成年女性，保留五官、脸型、年龄观感、肤色、发色发型、眼镜状态与可见体型。
将场景改为简洁暖色厨房，采用温柔成熟的生活氛围；保留原姿态和构图，按新环境调整透视、接触阴影及窗光色温。
衣服和其他身份属性保持原样。

判定：reference-person + editing + Seedream adapter；未知版本使用通用自然语言，未编造参数或参考上限。

### B10 — PASS

40 岁成年女性的克制职业肖像，从容稳重，合体职业服装，姿态自然，表情专业，干净背景与柔和定向光。
沿用角色已锁定的脸、年龄观感、发型、肤色和体型，不添加暧昧眼神、撩人动作或曲线强化。
本张为账号风格例外，未要求永久修改人设。

判定：modes + series-consistency；保留熟女 Mode，attention=off；未知模型无专属 adapter。

## 结果与未测范围

- 人工规则走查：30/30 PASS（20 routing + 10 regression），无独立性保证。
- 负例误触发走查：6/6 排除；年龄模糊与校园性感两项边界未启用增强。
- Reference First 文本夹具：7/7 PASS；不代表真实图片身份测试。
- 独立 Agent 自动选择与按需加载：NOT RUN。
- GPT Image / Qwen-Image 2.1 / Seedream 真实出图、缩略图观感与身份一致性：NOT RUN。
- 平台审核与男性用户停留效果：NOT RUN；需实际平台规则和发布反馈。

## 自审修正

B07 初稿仅写“成熟性感”不足以唯一确定熟女，输入已补充“优雅从容、强气场”，避免测试暗中以年龄或性感词强制路由。
R06/R08 的原型仅作为首图人设起点，不要求生成完整账号卡；不应因最少模块列表把所有任务扩展为账号设计。

## 静态检查记录

- `python scripts/validate.py`：PASS；本地 Markdown 文件链接与 reference 可达性通过。
- skill-creator `quick_validate.py`（UTF-8 模式）：PASS，YAML frontmatter 有效。
- `git diff --check`：PASS。
- 校验器负向探针：损坏链接、非法 YAML、未闭合围栏、重复案例、缺失案例均被检测（5/5）。
- 超过 100 字符的实质段落精确重复扫描：0；必要的优先级摘要与边界重申保留。
- 冲突走查：参考未知体型不套软默认；单次眼镜修改不改系列卡；显式去性感覆盖男性向账号。
