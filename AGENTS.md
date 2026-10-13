# AGENTS.md · iec62304-software

> 机器可发现入口（AI 编码代理 / Codex / Claude / Cursor）。单一事实源：本文件。

## 这是什么
IEC 62304:2006+A1:2015 医疗器械软件生命周期工具：软件安全等级 A/B/C 判定器（基于伤害可能性×严重度）、软件开发生命周期过程清单（策划/需求/架构/单元/集成/系统测试/发布/维护）、与 Agile/CI 实践的映射建议、SOUP 第三方组件管理检查点。

## 运行
```bash
python scripts/sw_lifecycle.py --demo
python scripts/sw_lifecycle.py --help
```

## 扩展契约（lgd-skeleton/1.0）
- **一切即插件**：仅依赖声明式 `module.json`，零配置。
- **按需装（lazy）**：仅 triggers 命中时加载。
- **可嵌套（nested）**：可被 `medical-ai-toolkit` 总入口路由。
- **扩展点**：`plugins/`(新增过程项：在 SW_PROCESSES 加一项。)

## 红线
纯技术贡献，不含商业营销；MedXpert 仅作为贡献者署名（@stevenzhao07）。
