# Contributing / 参与复核

[English README](README.md) · [中文入口](README.zh-CN.md)

Report a concrete discrepancy rather than a general impression. Include the upstream commit, target theorem, tool versions, exact command, full exit status and smallest relevant evidence. Classify the issue as **mathematical argument**, **statement mismatch**, **axiom/checker rejection**, **build/environment failure**, or **archive inconsistency**.

Do not overwrite historical logs to make a new run appear successful. Put new runs in a separate dated directory with their own environment, changes, exit codes and checksums. Never add an axiom, weaken a theorem or change an allowed-axiom list and describe the result as verification of the unchanged target.

A new run may use another kernel or rebuild trusted libraries from source. Report those as additional evidence with their own trust assumptions. A favorable LLM review alone is not a formal replay.

Local archive-checker tests:

```bash
python -m unittest discover -s tests -v
python scripts/check_bundle.py
```

The tests and archive checker do **not** execute Lean. They check this package's handling of evidence.

## 中文

请报告具体差异，并附上游提交、定理名、工具版本、原始命令、完整退出状态与最小相关证据。请区分**数学论证问题、声明不对应、公理或检查器拒绝、构建／环境失败、归档不一致**。

不要覆盖历史日志来营造新一次成功。新增重放应保存在另一个带日期的目录，单独记录环境、修改、退出码与散列。不得增加公理、弱化命题或扩大允许公理后，仍称为原命题的验证。

第二内核或从源码重建可信依赖，都应作为附加证据单独报告，并披露其可信前提。模型赞同不能代替形式化重放。

上面的测试命令只检查本归档对证据的处理，不会运行 Lean。公开日志前，请检查其中的令牌、密码、凭据 URL、私人路径与第三方信息。
