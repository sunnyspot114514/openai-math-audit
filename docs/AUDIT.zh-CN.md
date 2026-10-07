# 核验结果与限制

[English](AUDIT.en.md) | [中文](AUDIT.zh-CN.md) · [首页](../README.zh-CN.md)

**快照日期：2026-10-07。** 本文区分机器执行、二次复核和公开打包三个环节，不增加一次新的证明验证事件。

## 结果

在 `openai/math` 的固定提交 `adc7f1241b42e322a6451854ab7e4b4c146bf78a` 上，交付记录显示两个未经修改的目标配置都通过了 Comparator。两份退出码均为 0，stdout 均到达 Lean 默认内核接受与 Comparator 最终成功标志。

| 目标 | 配置 | 形式化定理名 | 记录用时 |
|---|---|---|---|
| 对称 Mahler | `MahlerConjecture.json` | `OAI.SymmetricMahler.symmetric_mahler` | 11:21.19 |
| 对称极体乘积 | `SymmetricPolar.json` | `OAI.SymmetricPolar.symmetric_polar_main` | 47:52.38 |

直接证据：[Mahler stdout](../evidence/machine/mahler.stdout.log)、[极体乘积 stdout](../evidence/machine/polar.stdout.log)、[机器报告](../evidence/machine/REPORT.md)、[结构化摘要](../audit-summary.json)。

## 数学范围

第一个命题覆盖每个正维数，以及每个紧、凸、原点对称且内部非空的集合。极体使用标准坐标配对，`volume` 是通常的有限维 Lebesgue 体积。`toReal` 不是额外假设，也不是另一种体积定义。本目标不含等号分类。

第二个命题针对位置／动量共轭坐标下的开集 `int K × int K°`。球明确写作 `π(‖q‖² + ‖p‖²) < c`，没有把积空间的最大值范数球混入。定义要求光滑性、拓扑嵌入、像包含关系，以及导数保持标准辛形式。源球是开集，因此这里是实际局部导数。结论含每个严格小于 4 的容量，不要求上确界处存在嵌入。

完整语义记录见 [SEMANTICS.md](../evidence/machine/SEMANTICS.md)，固定目标见 [MahlerConjecture.lean](../evidence/machine/preaudit-copies/MahlerConjecture.lean) 和 [SymmetricPolar.lean](../evidence/machine/preaudit-copies/SymmetricPolar.lean)。

## 这次通过比普通编译多了什么？

记录中的 Comparator 会比较目标涉及的声明环境、检查最终证明的传递公理依赖，并把导出的解答交给 Lean 默认内核重放。这些保证依赖[上游说明](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/README.md)列出的可信输入与运行环境。

两份额外公理输出都恰为允许集合：`propext`、`Classical.choice`、`Quot.sound`。Challenge 文件里的 `sorry` 是题目占位，不是已接受 Solution 定理中的缺口。见 [Mahler 公理](../evidence/machine/axcheck-AxMahler.out)和[极体乘积公理](../evidence/machine/axcheck-AxPolar.out)。

## 每一层由谁完成？

记录里的机器工作由 Grok bot 在独立的非特权审计账户中执行。GPT 辅助审读数学路线，并在交付后交叉核对材料。[二次复核中文原件](../evidence/secondary/second_review_zh.md)另行保留，不与本文编辑说明混在一起。

公开打包阶段重新检查来源散列，保留核心执行记录，对少量无关宿主标识作去标识化，并测试归档检查脚本。这个阶段**没有重新安装 Lean、重建证明库或运行第二次内核检查**。

## 环境与必须保留的差异

机器报告记载 Debian 13、x86-64 Linux 6.12.94+、8 vCPU、16 GB 内存、无 swap。这只是一次实测环境，不是最低配置承诺。GNU time 的内存峰值是所等待进程中最大的单进程峰值，不代表整个进程树或整机的总内存需求。

使用 Lean 4.34.1；Comparator 源码固定于 `d03acab154d269c06e60e4de7e4cc85deebff94b`，仅把其工具链版本从 4.34.0 对齐到 4.34.1。交付 diff 没有修改检查逻辑。`lean4export` 使用匹配工具链编译。两个目标配置没有改动。

报告记录了官方 Mathlib 缓存的使用，没有复用已有 OAI 证明编译产物。仓库自身的依赖兼容补丁产生了本地修改警告；报告中的导入依赖范围排除了这些第三方包，可信 Mathlib 依赖与上游 tracked 工作区没有变化。本次打包没有重新拉取每一个依赖再审计一遍。

由于 systemd 不可用，运行使用归档中的 `restrict_af_unix.c` 包装器与真实的 landrun／Landlock。报告附隔离自测；二次复核阅读了代码和记录，但没有认证它等价于完整的 systemd 环境。审计账户与其他工作共享宿主机，部分无关世界可读目录仍可读。不能把这项限制删去，再描述为全新独占虚拟机。

证据：[版本](../evidence/machine/VERSIONS.txt)、[补丁](../evidence/machine/PATCHES.txt)、[工作区差异](../evidence/machine/workspace-diff.txt)、[自测](../evidence/machine/landrun-selftest.log)、[机器报告](../evidence/machine/REPORT.md)。

## 本包没有建立的结论

散列日志不能自行认证执行历史。本包不认证宿主、编译器、缓存提供方或检查器实现，也没有提供第二个独立内核。它没有把所有论文论证或所有上游定理一起认证。

一般非对称 Mahler、Hanner 等号分类、“准黎曼”结果、其他结果族与模型发现过程都在范围外。未来若修改原证明才能通过，必须把修改版作为新变体报告，不能仍称为原版验证。

## 合适的结论

> 记录中的独立重放成功完成：这两个固定形式化命题的导出解答被 Lean 默认内核接受，最终证明不依赖允许集合以外的公理。语义检查没有发现与目标数学命题的不对应。二次复核没有发现推翻这些记录的矛盾。结论限于这两个目标与已披露的可信前提。

在这个证据等级上，可以接受这两个结果。继续投入应针对具体新问题：第二内核、源码重建、明确的缺陷报告，或更好的数学解释；没有必要无限重复模型意见。
