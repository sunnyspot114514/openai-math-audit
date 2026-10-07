# Publish this package / 上传这个包

[English README](../README.md) · [中文入口](../README.zh-CN.md)

## 中文

建议仓库名：`openai-math-audit`。这是建议名称，打包时没有替你创建仓库，也没有推送任何内容。

解压 ZIP，进入 `openai-math-audit` 文件夹。将**里面的文件与目录**上传到 GitHub 新仓库的根目录，让 `README.md` 直接出现在首页，不要再套一层同名文件夹。英文 README 是默认首页，中文入口在顶部；中英文文章放在 `articles/`。

建议仓库简介：

> Independent Comparator/Lean audit of two OpenAI mathematical results, with bilingual evidence, scope notes and an essay on verification and explanation.

建议 Topics：`lean4`、`formal-verification`、`mathematics`、`mahler-conjecture`、`symplectic-geometry`、`ai-for-science`、`reproducibility`。

本包不包含已配置的 CI、发布令牌或任何指向尚未创建仓库的状态徽章。顶部徽章是静态说明，不会声称 GitHub Actions 已经运行。引用信息已放在 `CITATION.cff`，未虚构 DOI。

用 Git 上传时，在解压目录中执行下面的前几行；把最后的 HTTPS 地址换成你实际创建的仓库。需要你自行完成认证，不要把访问令牌写进 URL 或文件。

```bash
git init
git add .
git commit -m "Publish bilingual Mahler and polar-product audit"
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git push -u origin main
```

`.gitattributes` 会让证据文件保留原始字节。若以后修改 README 或其他被校验文件，应重新生成公开版本清单并增加版本说明；不要直接改历史证据后沿用旧结论。

## English

Suggested repository name: `openai-math-audit`. No repository was created and no content was pushed during packaging.

Unzip the archive and upload the **contents** of its `openai-math-audit` folder to the root of your new repository. `README.md` should be at the root, not inside another nested folder. English is the default entry point; the Chinese README is linked at the top. Both article versions live in `articles/`.

Use the suggested description and topics above as editable metadata. Replace the example remote in the Git commands with your actual repository URL. Keep authentication outside the repository; do not embed a token in a URL.

No CI result, repository URL or DOI has been invented. The badges are static descriptions of the recorded audit, not a claim that a newly created GitHub workflow has passed. The `.gitattributes` file preserves evidence bytes. New publications need a new checksum manifest and version note; historical evidence should not be overwritten.
