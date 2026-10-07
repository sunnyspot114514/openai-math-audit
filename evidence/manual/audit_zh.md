# OpenAI Family 087：对称极体乘积与 Mahler 主不等式核验记录

日期：2026-10-07。

## 结论与证据等级

本次固定检查 `openai/math` 的提交：

`adc7f1241b42e322a6451854ab7e4b4c146bf78a`

**人工审读结论：在本次检查的主证明链中，未发现足以使论证失效的缺口，当前判断倾向其成立。** 本次新增重点是《Symplectic Balls in Symmetric Polar Products》的球嵌入、平面一致估计、相空间实现、一般凸体逼近与宽度上界。该证明声称：对每个原点对称凸体 K⊂Rⁿ（n≥2），

\[
c_G(\operatorname{int}K\times\operatorname{int}K^\circ)=4,
\]

并对每个 0<c<4 构造辛球嵌入。体积保持给出对称 Mahler 下界。

**这不是完整 Lean/Comparator 重放认证。** 本次没有完成整个传递依赖图的公理扫描，没有复核一般非对称 Mahler 的证明，也没有完整复核对称 Mahler 的 Hanner 等号分类。局部数值检查不作为普遍命题的证明。

## 1. 精确范围

目标集合是 `int K × int K°`，不是任意中心对称的 2n 维辛域。标准球按 π(|q|²+|p|²)<c 定义，辛形式是 Σdqᵢ∧dpᵢ。结论提供每个严格小于 4 的容量，并不要求容量恰好为 4 的球能够嵌入。

Lean 的挑战声明 `ComparatorChallenges/SymmetricPolar.lean` 中，极体、容量球、辛形式、光滑嵌入和 Gromov width 的定义，与上述通常表述相符。审读未发现把目标换成仅体积保持、特殊多面体或有额外对称性的对象。

## 2. 从全纯零点获得辛球

论文令 τ=|f|²，并考虑 ω=ddᶜ(|z|²+τ)。假设 f 只有原点一个共同零点，消失阶至少 k，且 τ<1 之下的闭次水平集在原域中紧。

关键检查如下。

- log τ 在非零点处是多重次调和的：其 Levi 型分子由 Cauchy–Schwarz 非负。这不使用 Mahler 下界。
- 对固定 a<k，取 a/k<b<1，再取 a<μ<bk。用凸递增 χ 把 τ 换成在零点附近有 bk log|z|² 上界、而在边界附近与 τ 相等的势函数 H。
- 令 Pδ=μ log(|z|²+δ)−M。由于 μ<bk，Pδ−H 在趋于零点时趋于正无穷；这一估计对 δ∈(0,1] 一致。因此可先选固定内半径 r₁，再选很小的 δ。这避免了“内球半径与 δ 同时缩小，容量不够”的漏洞。
- 正则化最大值只在紧集内修改势函数，欧氏项 |z|² 保证整条 Moser 同伦非退化。相关向量场有共同的紧支撑，故流不会从开域的边界逃逸。
- 径向模型 Ψ(t)=t+μ log(t+δ) 中，映射 R(z)=sqrt(Ψ′(|z|²))z 满足正确的辛形式拉回公式。

独立复算的关键等式是

\[
\frac{d}{dt}\bigl(t\Psi'(t)\bigr)
=1+\frac{\mu\delta}{(t+\delta)^2}>0.
\]

像球的半径平方为 r₁²+μr₁²/(r₁²+δ)，可取为大于 a。因此获得容量 πa 的球；a 可任取小于 k 的数，故达到所有容量小于 πk 的球。

**审读结果：这一步提供的是实际辛嵌入，不是仅由大体积推断存在球。**

## 3. 平面共形映射与一致端点估计

论文使用

\[
F(w)=\frac8{\pi^2}\sum_{\ell\ge0}\frac{(-1)^\ell w^{2\ell+1}}{(2\ell+1)^2}.
\]

其水平截面是区间，边界虚部范围为 [-1,1]。令 g=F⁻¹、

\[
J_k(v,t)=k^2\int_0^v |g(h+it)|^{2k-2}|g'(h+it)|^2\,dh.
\]

所需命题是整个平面域上的一致估计

\[
\frac{|J_k(v,t)|}{k}
\le \frac\pi4|g(v+it)|^{2k}+\epsilon_k,
\qquad \epsilon_k\to0.
\]

这比对每个固定截面的点态收敛更强，因为截面高度可以随 k 逼近尖点。

### 3.1 尖点小分母

写 w=re^{iθ}，A=Re(wF′(w))，则

\[
A(r,\theta)=\frac4{\pi^2}\arctan\frac{2r\cos\theta}{1-r^2}.
\]

令 s=π/2−|θ|，用 1/arctan X−2/π≤2/X 以及 sin s≥2s/π，得到

\[
\frac1A\le\frac\pi2+\frac{3\pi^3}{8}\frac{1-r}{s}.
\]

再用垂直间隙 Δ≤(2/π²)s²/(1-r)，得到

\[
\frac1A\le\frac\pi2+C_0\sqrt{\frac{1-r}{\Delta}},
\qquad C_0=\frac{3\sqrt2\pi^2}{8}.
\]

这些不等号方向和常数经过重新代入检查。

### 3.2 移动端点

固定 r*∈(1/2,1)，外部积分最终归结为

\[
I(k,a)=k\int_a^1 r^{2k-1}\sqrt{\frac{1-r}{r-a}}\,dr.
\]

端点 a 可以依赖 k。令 H=k(1-a)、y=k(1-r)，则

\[
I(k,a)
\le\int_0^H e^{-y}\sqrt{\frac{y}{H-y}}\,dy.
\]

将积分分为 [0,H/2] 和 [H/2,H]。第一段不超过 1；第二段不超过

\[
e^{-H/2}\int_0^H\sqrt{\frac{y}{H-y}}\,dy
=\frac{\pi H}{2}e^{-H/2}\le\frac\pi e.
\]

因而

\[
I(k,a)\le1+\pi/e
\]

独立于 k 和移动端点。这是纸面推导，而非从测试点外推。

总误差被上界为

\[
C_*kr_*^{2k-2}+\frac{C_0(1+\pi/e)}{\sqrt{L_*}},
\quad L_*=\inf_{r\ge r_*}T'(r)\longrightarrow\infty\ (r_*\uparrow1).
\]

先选择 r* 使第二项足够小，再令 k 足够大使第一项小。由此确实得到一致收敛，未交换未经证明的极限。

## 4. 相空间实现、单射性与容量缩放

对有限条带体

\[
K=\{x:|b_j\cdot x|\le1,\ j=1,\dots,m\},
\]

取 fⱼ(z)=g(bⱼ·z)^k。向量 bⱼ 张成空间，使共同零点仅为零，并保证需要的次水平集紧性。

写 z=u+ix，论文的映射是

\[
q=x,\qquad p=-u-\sum_jJ_k(b_j\cdot u,b_j\cdot x)b_j.
\]

直接展开得 Φ*ω₀=ddᶜ(|z|²+τ)。特别是关于截面高度的导数项落在 dtⱼ∧dtⱼ=0 中，不产生漏掉的交叉项。

固定 x，由 ∂ᵥJₖ≥0，

\[
(p_2-p_1)\cdot(u_2-u_1)\le-\|u_2-u_1\|^2.
\]

因此相同像点只能来自相同原点，解决了从局部辛映射到全局单射的问题。即使 τ<1 的某个纤维不连通，这个比较仍在整个水平截面区间上有效。

支持函数估计为

\[
\frac{h_K(p)}k
\le\frac{C_K}k+\frac\pi4\tau+m\epsilon_k.
\]

K 及其 m 条约束先固定，再令 k→∞，所以 mεₖ→0。在充分大的 k 下，像位于

\[
\operatorname{int}K\times S\operatorname{int}K^\circ,
\qquad S=(1+\eta)\pi k/4.
\]

对任意 c<4，取 (1+η)c<4，则 Sc<πk。源球作 √S 倍缩放会把辛形式乘 S；目标只把动量除以 S 会把辛形式乘 1/S。两者在复合映射中相消。**动量单独缩放不是辛映射，但整个复合是。**

## 5. 一般凸体与上界

通过在极体中选有限网，得到 K⊂K′⊂(1+α)K、(K′)°⊂K°。对每个固定 c<4 先选 α，再固定 K′ 及其约束数，最后选 k。这给出一个有限构造，不需要证明一串嵌入的极限仍是嵌入。

上界使用支撑向量 q₀、p₀（内积等于 1）选共轭坐标，使目标落入 (-1,1)²×R^{2n−2}。第一个平方可面积保持地映入面积 4 的圆盘；再用 Gromov nonsqueezing，得到 c_G≤4。这里接受经典 nonsqueezing 定理作为既有定理，本次未重新证明它。

球体积为 cⁿ/n!，辛映射保持体积，因此对所有 c<4 有 |K||K°|≥cⁿ/n!，令 c↑4 得到对称 Mahler 主不等式。四维常数为 4⁴/4!=32/3。n=1 由区间及其极体直接得到。

## 6. 实际执行的局部诊断

随附 `diagnostics.py` 是独立编写并实际执行的检查脚本，输出为 `diagnostics.json`。

- 四项符号检查：径向单调性等式；一般 3×2 行矩阵下的相空间拉回等式；两类容量缩放的相消；透镜宽度的二阶导数。
- 13 个共形边界取值，采用 60 位十进制精度，包括距尖点 10⁻¹⁰ 的高度。边界虚部/反射恒等式的最大数值残差约 2.34×10⁻⁶¹。
- 42 个尖点角度/半径组合的倒数 A 上界检查。
- 109 个 k、移动端点组合的积分检查，k 从 2 到 4096，包括端点随 k 逼近 1 的样本。样本中最大 I 约 0.4439638508；通用上界为 1+π/e≈2.1557273498。

所有这些局部检查完成，未触发断言失败。**小数残差与 quadrature error estimate 不是严格区间证书；有限样本也不是无穷参数证明。** 普遍端点估计的依据是第 3 节的手工不等式推导。

## 7. Lean 与可重放状态

已读取的目标与入口包括：

- `lean/ComparatorChallenges/MahlerConjecture.json`
- `lean/OAI/Analysis/Mahler/MainTheorem.lean`
- `lean/ComparatorChallenges/SymmetricPolar.lean`
- `lean/ComparatorChallenges/SymmetricPolar.json`
- `lean/OAI/Geometry/PolarProducts/Main.lean`
- `lean/OAI/Geometry/PolarProducts/UpperBound.lean` 的开头部分（不是整文件）。

两个 Comparator 配置允许的公理仅为 propext、Quot.sound、Classical.choice。挑战文件中的 sorry 是待证题目占位；解答模块的主定理另有证明体。但这不构成实际运行检查器的替代。

当前工作容器没有 lean/lake；尝试访问原始仓库文件以配置本地重放时 DNS 失败。仓库正文通过 GitHub 连接器成功读取。未在用户电脑上安装工具或启动大型构建。没有完成完整编译、传递依赖公理核查、Comparator 或可选独立内核重放。

本次可见 Actions 返回两条依赖图更新工作流；这些记录不能充当 Lean 主证明重放日志。不能据此断言发布方从未进行验证。

## 8. 本轮没有证明什么

1. 没有完整认证整个 Family 087，更没有认证全部仓库。
2. 没有完整核验 Hanner 等号分类或一般非对称 Mahler。
3. 没有证明当前公开订阅模型能以同样预算复现内部模型的结果。
4. 没有把用户先前的局部证明候选追认为完整证明，也没有判断它们的原创优先权或发表价值。
5. 没有把“针对对称极体乘积”的结果扩写为任意中心对称辛域的 Viterbo 猜想。

## 来源与复查入口

以下路径均固定在上述 commit。各节的数学表述应以仓库原文为准；本记录是审读与独立复算摘要。

- https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections
- https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections/ball.tex
- https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections/planar.tex
- https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections/realization.tex
- https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections/approximation.tex
- https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/SymmetricPolar.lean
- https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/Geometry/PolarProducts/Main.lean
- https://openai.com/index/sharing-ai-progress-in-mathematics/

## 重放本地诊断

```sh
python diagnostics.py --output diagnostics.json
```

仅重放上列有限诊断，不重放 Lean 证明。执行结果依赖安装的数值库，浮点数末位和积分误差估计可能随平台略有差异。
