# 对称极体乘积证明：阅读路线图

[English](EXPLANATION.en.md) | [中文](EXPLANATION.zh-CN.md) · [首页](../README.zh-CN.md)

这是对早期核验所读论证的导读，不是新证明，也不是另一次逐行认证。来源为[固定版本的极体乘积论文](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Symplectic-Balls-in-Symmetric-Polar-Products-September-22-2026/build/sections)。更详细的原始记录见 [audit_zh.md](../evidence/manual/audit_zh.md)。

## 目标，以及它为什么推出 Mahler 下界

把对称凸体 $K$ 放在位置坐标，把极体 $K^\circ$ 放在动量坐标。定理在这个开乘积中给出每个容量 $c<4$ 的光滑辛球嵌入。辛映射保持体积，容量为 $c$ 的球体积为 $c^n/n!$，因此

$$
|K||K^\circ|\geq c^n/n!\qquad(0<c<4).
$$

在这个数值不等式中令 $c\uparrow4$，就得到对称 Mahler 下界。这一步不需要容量恰为 4 的球能嵌入，也不需要一列嵌入映射有良好的极限。

## 构造的五个步骤

**1. 从高阶全纯零点构造一个球。** 只有一个共同零点的全纯函数组 $f$ 给出势函数 $|z|^2+|f(z)|^2$。局部径向替换产生球，再用紧支撑的 Moser 变形送回原来的形式。审读重点是：修改是否具有共同紧支撑；是否先固定内部半径，再减小平滑参数。仅有大体积不能推出辛球；这里需要实际构造嵌入。

**2. 对所有平面切片取得一致估计。** 共形透镜提供逆映射 $g$ 与水平原函数 $J_k$，需要证明

$$
|J_k(v,t)|/k\leq (\pi/4)|g(v+it)|^{2k}+\epsilon_k,\qquad\epsilon_k\to0,
$$

而且对所有点一致成立。切片可以随 $k$ 逼近尖点。最需要小心的误差通过

$$
I(k,a)=k\int_a^1r^{2k-1}\sqrt{\frac{1-r}{r-a}}\,dr\leq1+\pi/e
$$

控制。换元 $H=k(1-a)$、$y=k(1-r)$ 明确处理移动端点，并在增大 $k$ 前先选固定截断。这一环不能用逐点收敛替代。

**3. 在缩放后的极体乘积中实现辛形式。** 对固定的有限条带体，写 $z=u+ix$，令

$$
q=x,\qquad p=-u-\sum_jJ_k(b_j\cdot u,b_j\cdot x)b_j.
$$

拉回计算得到所需辛形式。在同一个 $x$ 上，单调性给出

$$
(p_2-p_1)\cdot(u_2-u_1)\leq-\|u_2-u_1\|^2,
$$

于是得到全局单射，而不只是局部非退化。支持函数估计把像控制在 $\operatorname{int}K\times S\operatorname{int}K^\circ$ 中。

**4. 平衡两个尺度。** 全纯构造给出容量小于 $\pi k$ 的球，而动量尺度可以取为 $S=(1+\eta)\pi k/4$。只把动量除以 $S$ 不是辛变换；证明同时把源球放大 $\sqrt S$，拉回中的因子恰好相消。对固定 $c<4$，先取 $(1+\eta)c<4$，再取充分大的 $k$。

**5. 推广到一般凸体，并取得上界。** 在极体中作有限逼近，得到 $K\subset K'\subset(1+\alpha)K$ 和 $(K')^\circ\subset K^\circ$。对每个目标容量先固定近似体及其约束数，再选 $k$，无需一列嵌入的极限。支撑柱体构造结合 nonsqueezing 给出匹配的上界 4。

## 这说明了旧路线的什么问题？

作者之前的工作处理特殊多面体族和显式体积公式，但从一般对象到已处理类别的归约仍是另一项障碍。这里的路线处理任意有限条带列表，然后再作逼近，不要求预先给顶点数或面数设定统一上限。

因此，一般结果能够覆盖逐族推进的目标。旧公式或构造是否仍有独立的新颖性和用途，需要另外判断，不能仅由一般下界成立与否决定。

## 继续阅读的入口

固定目录中的 `ball.tex`、`planar.tex`、`realization.tex` 和 `approximation.tex` 对应上面的主线。可与 [SEMANTICS.md](../evidence/machine/SEMANTICS.md) 对照，避免混淆论文中的目标与形式化目标。

`evidence/manual/diagnostics.json` 里的有限数值检查是诊断样本，不是严格区间证书，也不覆盖无限参数域。它们是解析审读与后续形式化重放的辅助材料。
