# 复跑核验

[English](REPRODUCE.en.md) | [中文](REPRODUCE.zh-CN.md) · [首页](../README.zh-CN.md)

检查这个归档与重新检查数学证明，是两种操作。不要把前者描述为后者。

## A. 查看公开归档

在仓库根目录执行：

```bash
python scripts/check_bundle.py
python -m unittest discover -s tests -v
```

只使用 Python 标准库，读取散列、固定声明、日志、退出状态与公理记录，不调用 Lean 或模型。所需文件缺失／改变、记录的运行失败、存在未允许的公理或配置不一致，都会让归档检查以非零状态结束。

清单检查的是本次公开的字节，不是原始运行环境的数字签名。若数据与散列同时被篡改，也能伪造归档；要获得新一次证明验证证据，需要实际独立运行检查器。

## B. 准备新的形式化核验

使用一次性 Linux 环境和非 root 账户，不挂载私人令牌、SSH 密钥、生产目录或其他项目。执行任何 Solution 代码前，阅读固定版本的 [Comparator README](https://github.com/leanprover/comparator/blob/d03acab154d269c06e60e4de7e4cc85deebff94b/README.md)。项目 `lakefile.lean` 与可信 Challenge 依赖也需要检查，因为 Lake 配置本身可以执行代码。

`evidence/machine/` 中的旧脚本是历史记录，含原机绝对路径，**不是可直接执行的通用安装器**。本包不会替你安装环境或启动新的大型证明构建。

### 记录中的版本

| 组件 | 版本／提交 |
|---|---|
| openai/math | `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| Lean | `leanprover/lean4:v4.34.1` |
| Lean 构建提交 | `5045d0056413266e57c625dcd7c365b10e377c52` |
| Comparator | `d03acab154d269c06e60e4de7e4cc85deebff94b` |
| lean4export | `076e8e57707e813375e8f9da8bf989799ace9680` |
| landrun | `811cfff51ceaf3d9843708aa6d22e9b84ccac8b4` |
| Mathlib | `d13f23b723b8a846827a245b89c10fc7d3f11612` |

Comparator 仅把工具链从 4.34.0 对齐到 4.34.1，[原始差异](../evidence/machine/tool-patch-comparator-toolchain.diff)已保存。Comparator 与 lean4export 要用匹配的 Lean 编译，不要默默升级到最新版。安装差异应作为新的环境变体记录，完整历史版本见 [VERSIONS.txt](../evidence/machine/VERSIONS.txt)。

### 获取数学源文件

```bash
git clone https://github.com/openai/math.git math
cd math
git checkout --detach adc7f1241b42e322a6451854ab7e4b4c146bf78a
git rev-parse HEAD
git status --porcelain
```

第一次运行 Lake 前，检查 Challenge 文件、两个 JSON 配置、`lean/lean-toolchain`、`lean/lakefile.lean` 和 `lean/lake-manifest.json`。被审计配置没有 definition holes，只允许 `propext`、`Quot.sound`、`Classical.choice`。

在隔离账户内准备依赖。历史运行从 `math/lean/` 执行 `lake exe cache get`，使用官方 Mathlib 缓存，保留固定 manifest，**没有运行 `lake update`**，也没有复用预先编译的 OAI 证明对象。详见[机器报告](../evidence/machine/REPORT.md)和[预审记录](../evidence/machine/PREAUDIT.md)。

完全从源码重建是另一种有价值的变体，但应单独报告，不与使用缓存的时间直接比较。不要在受保护的 Comparator 调用之前，直接构建或执行待检查的 Solution。

### 执行 Comparator

前提：匹配版本的 `lean`、`lake`、`comparator`、`lean4export` 和真实 `landrun` 已在 PATH；可信依赖已准备完成；systemd 用户管理器能够工作。用官方隔离启动方式，只替换两个固定配置名。

在 `math/lean/` 下，下面示例会立即保留各进程的真实退出码：

```bash
# 输出目录与上游源文件分开；环境与隔离前提需由操作者落实。
mkdir -p "$HOME/mahler-replay-results"
OUT="$HOME/mahler-replay-results"
set +e
for name in MahlerConjecture SymmetricPolar; do
    cfg="ComparatorChallenges/$name.json"
    date -Is > "$OUT/$name.started.txt"
    systemd-run --property=RestrictAddressFamilies=~AF_UNIX \
      --user --pty -E PATH="$PATH" --working-directory "$(pwd)" -- \
      bash -c "lake env comparator $cfg" \
      > "$OUT/$name.stdout.log" 2> "$OUT/$name.stderr.log"
    rc=$?
    printf '%s\n' "$rc" > "$OUT/$name.exitcode"
    date -Is > "$OUT/$name.finished.txt"
    printf '%s: process exit %s (inspect full logs)\n' "$name" "$rc"
done
```

这是已准备环境中的操作说明，不是无人值守安装脚本。若 systemd、Landlock、工具链或资源不满足要求，应报告 `ENVIRONMENT_BLOCKED` 或 `BUILD_FAILED`，不要使用 fake-landrun 或关闭隔离来获取通过。

历史机器因为没有 systemd 使用了自定义 AF_UNIX seccomp 包装器。其源码与自测保留在证据中，并披露了审读限制。复用需自行审查；本包不认证它是完整沙箱。

### 判断和保存结果

运行必须以真实退出码 0 到达默认内核接受与 Comparator 最终成功。随后核对未经修改的目标配置与数学含义，保存 stdout／stderr、工具版本、源代码 diff、依赖变化、允许／实际公理、用时、资源信息和散列。不要用手工补写的成功句替换日志。

后续 `#print axioms` 或语义脚本若会加载已构建的 `.olean`，也应按上游要求在受保护环境中运行，不要在隔离构建之后又不受保护地加载它们。

下载失败、OOM 或工具链不兼容不是数学反例。导出或公理检查被拒绝，说明这次形式化验证未成立，也不自动说明数学命题为假。

两个原配置均关闭 nanoda。附加独立内核需要另外记录兼容检查器与配置，不能把新做的第二内核检查追记为原始单内核运行的一部分。
