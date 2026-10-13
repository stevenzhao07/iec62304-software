# iec62304-software

> **Contributed by [@stevenzhao07](https://github.com/stevenzhao07) · Affiliation: MedXpert (medical-device RA & regulatory consultancy) · Pure technical input, no commercial promotion.**

IEC 62304:2006+A1:2015 医疗器械软件生命周期工具：软件安全等级 A/B/C 判定器（基于伤害可能性×严重度）、软件开发生命周期过程清单（策划/需求/架构/单元/集成/系统测试/发布/维护）、与 Agile/CI 实践的映射建议、SOUP 第三方组件管理检查点。

这是 MedXpert 把"医疗 AI 信任"方法论工程化落地的可插拔模块之一——把抽象的合规要求变成一条可重复运行的命令或参考实现。方法论四要素（白话版）：**治理守护者 XCGS** ＝ 为 AI 留下可核验的治理证据；**立法者 A³ Laws** ＝ 给自主系统划权限 / 监督 / 追责三条硬边界；**护照官 AI 护照** ＝ 为模型签发可追溯的身份凭证；**人机共存** ＝ 明确人类与 AI 的分工与兜底。

---

## 可插拔模块契约（lgd-skeleton/1.0）

本仓库是一个 **`lgd-skeleton/1.0` 可插拔模块**：

- **一切即插件**：仅依赖声明式 `module.json`，零配置；
- **按需装（lazy）**：仅 triggers 命中时加载；
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由发现；
- **扩展点**：`plugins/`(新增过程项：在 SW_PROCESSES 加一项。)。

机器可发现入口：`AGENTS.md` · `CLAUDE.md` · `llms.txt`。

## 特性

- 安全分级判定：伤害严重度 × 可能性 → Class A/B/C（62304 §4.3 精神）
- 过程清单：§5–§8 策划/需求/架构/详细设计/单元/集成/系统测试/发布/维护
- Agile 映射：sprint/DoD 与 V&V 证据的对应建议
- SOUP 登记：第三方组件（版本/已知异常/风险评估）检查点

## 内容说明

分级判定为工程辅助：最终等级须结合风险管理文件（ISO 14971）输出判定。标准原文以 IEC 官方版本为准。

## 免责声明

本工具仅提供结构化模板与计算能力，**不构成法规建议、临床建议或产品合规结论**。具体产品的注册、临床评价、灭菌验证、风险分析、软件分级等决策，须由合资格人员依据目标辖区（NMPA / FDA / EU MDR / PMDA）最新法规文本作出；条款与限值以官方发布文本为准。使用本工具产生的一切后果由使用者自行承担。

## 使用

```bash
python scripts/sw_lifecycle.py --demo
python scripts/sw_lifecycle.py --classify --severity 4 --probability 3
```

## 快速开始（30 秒）

```bash
git clone https://github.com/stevenzhao07/iec62304-software.git && cd iec62304-software
python scripts/sw_lifecycle.py --demo
```

> 想参与或遇到问题？[提 Issue](https://github.com/stevenzhao07/iec62304-software/issues) · 完整《AI 参与指南》见 [medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)。

## 路由（总入口）

本模块由 **[medical-ai-toolkit](https://github.com/stevenzhao07/medical-ai-toolkit)** 作为 `lgd-skeleton/1.0` 总入口自动路由发现。

## 关联模块

- [samd-ra-toolkit](https://github.com/stevenzhao07/samd-ra-toolkit)
- [design-controls-toolkit](https://github.com/stevenzhao07/design-controls-toolkit)
- [cybersecurity-medical](https://github.com/stevenzhao07/cybersecurity-medical)

## 许可

CC-BY-4.0 — 见 [LICENSE](./LICENSE)。

## 关联（方法论来源）

- 理念溯源：个人专家关于医疗 AI 信任与治理的公开方法论（个人观点，不构成标准）
- 同账号系列：见 `medical-ai-toolkit` 导航
