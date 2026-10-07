# OpenAI Math Audit

[![Recorded audit: 2 targets](https://img.shields.io/badge/recorded_audit-2_targets-2c7a7b)](docs/AUDIT.zh-CN.md)
[![Lean 4.34.1](https://img.shields.io/badge/Lean-4.34.1-blue)](evidence/machine/VERSIONS.txt)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[🇺🇸 English](README.md) | [🇨🇳 中文](README.zh-CN.md)

**对 OpenAI 2026 年 10 月数学发布中两个明确命题的独立核验与证据归档。**

本仓库保存 **对称 Mahler 主不等式**与**对称极体乘积 Gromov 宽度定理**的 Comparator 重放记录，附原始执行证据、公理输出、语义检查、复核说明及中英文文章。

> **当生成成本下降，验证与解释应该得到更多重视。**

## 60 秒查看证据

下载或克隆仓库后，在根目录运行：

```bash
python scripts/check_bundle.py
```

只需 Python 3.10+ 与标准库。

输出形式如下：

```text
PASS  public file checksums
PASS  publication provenance
PASS  mahler: recorded exit 0, kernel acceptance, permitted axioms
PASS  polar: recorded exit 0, kernel acceptance, permitted axioms
BUNDLE_OK — evidence consistency only; no Lean verification was run.
```

这条命令检查公开归档。要重新执行形式化核验，见[复跑说明](docs/REPRODUCE.zh-CN.md)。

## 具体核验了什么？

本次固定上游版本：

```text
openai/math
adc7f1241b42e322a6451854ab7e4b4c146bf78a
```

| 目标 | 记录结果 | 墙钟时间 | 直接证据 |
|---|---|---|---|
| 任意 n ≥ 1 的对称 Mahler 主不等式 | Comparator 退出码 **0**；Lean 默认内核接受 | **11:21.19** | [stdout](evidence/machine/mahler.stdout.log)、[计时](evidence/machine/mahler.time.txt)、[公理](evidence/machine/axcheck-AxMahler.out) |
| 任意 n ≥ 2 的对称极体乘积宽度定理 | Comparator 退出码 **0**；Lean 默认内核接受 | **47:52.38** | [stdout](evidence/machine/polar.stdout.log)、[计时](evidence/machine/polar.time.txt)、[公理](evidence/machine/axcheck-AxPolar.out) |

这些是依赖准备之后、使用官方 Mathlib 缓存的验证时间。详见[机器审计报告](evidence/machine/REPORT.md)。

对任意原点对称凸体 $K\subset\mathbb R^n$，第一个目标为：

$$
|K|\,|K^\circ|\geq\frac{4^n}{n!},\qquad n\geq1.
$$

第二个目标为：

$$
c_G\!\left(\operatorname{int}K\times\operatorname{int}K^\circ\right)=4,\qquad n\geq2,
$$

并包含每个容量 $0<c<4$ 的球到该乘积中的光滑辛嵌入。

两个最终定理的公理输出都只有：

```text
propext, Classical.choice, Quot.sound
```

精确假设、归一化与范围检查见 [SEMANTICS.md](evidence/machine/SEMANTICS.md) 和[中文核验说明](docs/AUDIT.zh-CN.md)。

## 它解决什么问题？

生成了一份手稿、模型评价“没有问题”、Lean 文件编译成功，以及一个确定命题通过完整检查，是不同的证据。

| 需要回答的问题 | 本仓库提供的材料 |
|---|---|
| 到底检查了哪个命题？ | 固定版本的 Challenge 文件与原始 JSON 配置 |
| 检查器真的执行完了吗？ | stdout、stderr、进程退出码和计时记录 |
| 有没有增加假设来换取通过？ | Comparator 公理检查及另行输出的 `#print axioms` |
| 数学含义有没有被弱化？ | 定义、量词、假设和归一化的对应检查 |
| 还需要信任什么？ | 工具版本、缓存、补丁与隔离限制 |
| 其他人可以理解或继续使用什么？ | 证明路线解读、审读笔记和复跑说明 |

## 基本流程

```text
候选数学结果
     |
     v
精确且版本固定的定理声明
     |
     v
形式化重放与执行证据保存
     |
     v
数学语义与适用范围核对
     |
     v
可理解、可复用的数学知识
```

AI 可以参与每一个环节。

## 从哪里开始读？

| 用途 | English | 中文 |
|---|---|---|
| 核验结果 | [Audit overview](docs/AUDIT.en.md) | [核验说明](docs/AUDIT.zh-CN.md) |
| 重新执行形式化核验 | [Reproduction guide](docs/REPRODUCE.en.md) | [复跑说明](docs/REPRODUCE.zh-CN.md) |
| 理解数学路线 | [Proof map](docs/EXPLANATION.en.md) | [证明路线解读](docs/EXPLANATION.zh-CN.md) |
| 阅读作者观点 | [Essay](articles/essay.en.md) | [知乎回答稿](articles/zhihu.zh-CN.md) |
| 公开包如何整理 | [Provenance](docs/PROVENANCE.en.md) | [来源与公开处理](docs/PROVENANCE.zh-CN.md) |

## 谁做了什么？

**SUNNY99** 组织问题探索和核验。GPT 辅助完成正文审读、局部诊断、审计包复核与文字整理。**Grok bot** 执行记录里的机器重放。**Comparator 与 Lean 默认内核**完成记录中的形式化检查。

## 研究背景

作者在 7 月讨论过 AI 攻克数学开放问题；8 月有个回答提出用 Viterbo／Mahler 作为挑战，于是开始了约两个月的 AI 辅助尝试，得到部分特殊情形下的候选结果。这次发布的一般结果覆盖了那个阶段的目标。

作者的态度是**总体正面，带一点小失望**。验证与可解释性是此次发布前就反复关注的方向。[文章](articles/zhihu.zh-CN.md)写了这段经历。

## 仓库结构

```text
README.md / README.zh-CN.md  中英文入口
articles/                   英文文章与知乎回答稿
docs/                       核验、复跑、解读与来源说明
evidence/machine/           机器执行记录及固定版本源文件快照
evidence/manual/            早期审读与有限诊断材料
evidence/secondary/         对交付审计包的二次复核
evidence/provenance/        来源散列与公开处理映射
scripts/check_bundle.py     离线归档检查器
tests/                      归档检查器的测试
SHA256SUMS                  这个公开版本的完整性清单
CITATION.cff                本审计记录的引用信息
```

## 贡献与引用

提交具体问题时，请附版本、目标、命令、日志与最小差异。区分数学问题、形式化语义不对应和环境故障，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

本审计与原始数学论文应分别引用；引用信息见 [CITATION.cff](CITATION.cff)，上游来源见 [SOURCES.md](docs/SOURCES.md)。

## 许可

新增文字与归档检查脚本采用 **Apache-2.0**。上游快照保留原始署名与许可。见 [LICENSE](LICENSE)、[NOTICE](NOTICE) 和 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
