# OpenAI Mahler／极体乘积审计包二次复核

日期：2026-10-07  
审计提交：`adc7f1241b42e322a6451854ab7e4b4c146bf78a`

## 结论

所交付文件记录了两次成功的 Comparator 重放：对称 Mahler 主不等式和对称极体乘积的 Gromov 宽度定理。两次运行均记录退出码 0、Lean 默认内核接受、Comparator 最终成功。对报告、原始日志、执行脚本、公理输出、数学声明和工作区记录的交叉检查，没有发现足以推翻该通过结论的矛盾。

证据已强于“模型阅读论文后暂未发现错误”。在记录的工具链、公理与可信运行环境前提下，这是一份支持两个指定形式化命题通过独立验证的完整日志材料。本轮进行的是审计包二次复核；没有在本环境再运行 Lean，也没有把日志文件本身当作可由第二内核重新检查的证明对象。

## 原始证据

| 对象 | Mahler 主不等式 | 极体乘积宽度 |
|---|---|---|
| 配置 | `MahlerConjecture.json` | `SymmetricPolar.json` |
| `.exitcode` | 0 | 0 |
| GNU time 的 Exit status | 0 | 0 |
| 墙钟时间 | 11:21.19 | 47:52.38 |
| 日志内核接受 | 有 | 有 |
| 最终 Comparator 成功 | 有 | 有 |
| 公理 | propext, Classical.choice, Quot.sound | 同左 |
| 日志中的本地 OAI 构建数 | 229 | 46 |

两份 stdout 末尾都有：

```text
Running Lean default kernel on solution.
Lean default kernel accepts the solution
Your solution is okay!
```

证据位置：`out/mahler.stdout.log` 第 236–240 行；`out/polar.stdout.log` 第 53–57 行；两个 `.exitcode`；两个 `.time.txt` 第 23 行；`out/axcheck-AxMahler.out` 和 `out/axcheck-AxPolar.out`。

`run_comparator.sh` 第 22–26 行在 GNU time 运行后立即保存 `$?`，没有用 tee 的退出码代替验证进程状态。脚本自身最后的 echo 不是通过证据；已保存的子进程状态和 GNU time 记录才是。

## 本轮实际重新计算的完整性检查

- 外层 `SHA256SUMS`：58/58 匹配。
- `preaudit-copies/SHA256SUMS`：12/12 匹配。其记录的是原机绝对路径；按归档内唯一文件名映射后验证，没有改动文件字节。
- 两份 Challenge 源文件、两份 JSON 配置及固定版本 Comparator README：5/5 Git blob SHA-1 与本轮 GitHub 连接器返回值一致。
- 压缩包 SHA-256：`4f792ce069732d04029f6da79bb425662ebd113600dca1f367e62ad9f593d582`。

具体计算输出见 `hash_verification.json`、`upstream_blob_checks.json`、`review_checks.json`。

这些散列核对证明交付文件与其清单及所查上游文件一致；不单凭散列证明运行历史、二进制来源或整台机器从未受干扰。

## 检查器的成功标志含义

本轮读取了 Comparator 固定提交 `d03acab154d269c06e60e4de7e4cc85deebff94b` 的 `Main.lean`。

`verifyMatch` 先执行 `Comparator.compareAt`（目标及相关声明对应），再执行 `Comparator.checkAxioms`，之后运行内核重放。`runBuiltinKernel` 从空环境开始重放导出常量，并进行 quotient 后检查。`compareIt` 只有完成上述流程后才打印最终成功标志。因此在该原版工具正常运行的前提下，所记录的完整成功不是普通编译成功。

## 数学范围核对

### 对称 Mahler

对每个 n≥1 和每个紧、凸、原点对称、内部非空的 K⊂Rⁿ：

`|K| |K°| ≥ 4ⁿ/n!`。

Challenge 使用标准坐标内积定义极体；体积为有限积空间上的通常 Lebesgue 体积。条件没有增加顶点数、面数、光滑性或特殊对称性限制。`ENNReal.toReal` 在这些体积有限的对象上表达通常实数体积；不能靠无穷值转成零来使正下界成立。等号分类不包含在这个目标内。

### 对称极体乘积

对每个 n≥2 和每个原点对称凸体 K：

`c_G(int K × int K°) = 4`，且每个 0<c<4 都有光滑辛球嵌入。

球明确以 π(||q||²+||p||²)<c 定义，不把积空间的 sup 范数球混入；辛形式为标准 dq∧dp；嵌入条件包含拓扑嵌入、光滑性、像包含关系和导数保辛。源球是开集，所以不存在利用集合外任意延拓或 fderiv 的默认值弱化保辛条件的问题。没有声称容量恰等于 4 的球一定能嵌入。

## 警告、补丁与需要保留的环境限定

1. stdout 的 `sorry` 警告来自 Challenge 的题目占位，符合 Comparator 的设计。两个最终解答的公理输出没有 `sorryAx`。
2. stderr 中的 `has local changes` 对应 11 个仓库自动打兼容补丁的第三方包。附带清单说明它们不在两个目标的 import closure 中；工作区记录中原仓库 tracked diff 为空，Mathlib 及其可信依赖 tracked changes 为零。本轮没有逐一重新拉取这 11 个包来验证全部差异。
3. 工具补丁只有 Comparator 的 Lean 工具链从 v4.34.0 对齐到 v4.34.1；交付 diff 未显示修改检查逻辑、原命题或允许公理。
4. 没有 systemd，因此使用自写 seccomp 包装器限制 AF_UNIX socket。已静态阅读该 C 代码，并阅读成功应用 Landlock、写入限制和网络限制的自测日志；没有独立认证它等价于完整 systemd 启动环境，也没有重新执行这些自测。
5. 这不是完全不接触其他目录的新虚拟机：报告披露了同宿主上部分世界可读目录仍可读。敏感目录以独立 UID/ACL 隔离。这是安全部署说明上的限定，不是数学命题被改写的证据。
6. 一次辅助 DefsMahler 语义检查因检查脚本使用了错误的 Mathlib 引理名称而失败；修正该辅助脚本后退出码 0。两个 Comparator 原目标均是原版本成功运行，不是改原证明后成功。
7. 仅有 Lean 4.34.1 默认内核，未跑 nanoda／其他独立内核。Mathlib 使用官方缓存而非全量源码重建。

## 适当的结论与停止条件

可以表述为：

> 对 openai/math 提交 adc7f124… 的对称 Mahler 主不等式和对称极体乘积宽度定理，组织了独立环境中的 Comparator 重放。两项均记录退出码 0，默认 Lean 内核接受，最终公理仅为 propext、Quot.sound、Classical.choice；相关数学声明也经过对应检查。二次复核未发现推翻此次通过结论的矛盾。

不要扩展为：整个仓库已认证、所有 Viterbo 变体已解决、一般非对称 Mahler 已由本次验证、Hanner 等号分类已核验、或者已经完成双内核认证。

对当前两个指定目标，足以结束本轮常规核验并把成功记录归档。若日后出现具体缺陷报告，再围绕缺陷复查；第二内核或完全源码重建属于进一步降低可信计算基础的增强步骤，不是因为本包显示了数学漏洞。

## 上游来源

- Comparator README 与 Main.lean，固定提交 d03acab154d269c06e60e4de7e4cc85deebff94b。
- OpenAI math 两份 Challenge 源文件及 JSON 配置，固定提交 adc7f1241b42e322a6451854ab7e4b4c146bf78a。
- 原交付包中的 REPORT.md、SEMANTICS.md、日志、版本清单、补丁与工作区记录。
