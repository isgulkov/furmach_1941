## Задание 4, вариант {{var_number}}

### Часть I

Оценим линейную зависимость выборки $Y$ от $X_2$, $X_3$ и $X_4$, то есть найдем оценки $\hat{\beta_1}$, ..., $\hat{\beta_4}$ коэффициентов $\beta_1$, ..., $\beta_4$ регрессии $Y = \beta_1 + \beta_2 X_2 + \beta_3 X_3 + \beta_4 X_4 + \epsilon$ методом наименьших квадратов. Для этого найдем для реализаций выборок приближенное решение уравнения

$$
 \begin{pmatrix}
	y_1 \\
	\vdots \\
	y_{40}
\end{pmatrix} = \begin{pmatrix}
	1 & X_2^{(1)} & X_3^{(1)} & X_4^{(1)} \\
	\vdots & \vdots & \vdots & \vdots \\
	1 & X_2^{(40)} & X_3^{(40)} & X_4^{(40)} 
\end{pmatrix} \begin{pmatrix}
	\beta_1 \\
	\beta_2 \\
	\beta_3 \\
	\beta_4 \\
\end{pmatrix}.
$$
  
Решив, получили оценки:

$$
{% for i in range(4) %}\hat{\beta_{{ i + 1 }}} = {{ '%.3f' % beta_hats[i] }} \\
{% endfor %}$$

*Проверим значимость регрессии в целом* при $\alpha = 0.05$.

$H_0: \beta_1 = \beta_2 = \beta_3 = \beta_4 = 0;$
$H_1: \exists i \in \overline{1, 4} : \beta_i \neq 0.$

$F = \frac{\frac{ESS}{k-1}}{\frac{RSS}{n-k}} \sim F(k - 1, n - k)$, тогда

$F > F_{крит.} = F_\alpha (k - 1, n - k) \Rightarrow H_0$ отвергается в пользу $H_1$.

Посчитаем и получим:

$RSS = \sum_{i=1}^n (Y_i - \hat{Y}_i)^2 = {{ '%.1f' % overall_rss }};$

$ESS = \sum_{i=1}^n (\hat{Y}_i - \overline{Y})^2 = {{ '%.1f' % overall_ess }};$

$F_{крит.} = {{ '%.3f' % overall_f_crit }};$
{% if overall_f > overall_f_crit %}
$F = {{ '%.3f' % overall_f }} > {{ '%.3f' % overall_f_crit }} \Rightarrow H_0$ отвергается в пользу $H_1$, регрессия значима при $\alpha = 0.05$.{% else %}
$F = {{ '%.3f' % overall_f }} \leq {{ '%.3f' % overall_f_crit }} \Rightarrow H_0$ принимается, регрессия не значима при $\alpha = 0.05$.{% endif %}

*Проверим значимость коэффициентов по отдельности* при $\alpha = 0.05$.
 
$H_{0i}: \beta_i = 0;$
$H_{1i}: \beta_i \neq 0.$

По теореме **сочной залупы**:

$t_i = \frac{\hat{\beta_i}}{\sqrt{\hat{\sigma^2}(\beta_i)}} \sim t(n - k)$, тогда

$t_i > t_{крит.} = t_\alpha (n - k) \Rightarrow H_0$ отвергается в пользу $H_1$.

$t_{крит.} = {{ '%.3f' % coef_t_crit }};$
{% for i in range(4) %}{% if coef_t_vals[i] > coef_t_crit %}
$t_{{ i + 1 }} = {{ '%.3f' % coef_t_vals[i] }} > {{ '%.3f' % coef_t_crit }} \Rightarrow$ коэффициент *значим* при $\alpha = 0.05$;{% else %}
$t_{{ i + 1 }} = {{ '%.3f' % coef_t_vals[i] }} \leq {{ '%.3f' % coef_t_crit }} \Rightarrow$ коэффициент *незначим* при $\alpha = 0.05$;{% endif %}{% endfor %}

*Проверим совместную значимость коэффициентов $\beta_3$ и $\beta_4$* при $\alpha = 0.05$.
 
$H_{0}: \beta_3 = \beta_4 = 0;$
$H_{1}: \beta_3 \neq 0 \vee \beta_4 \neq 0.$

$F=\frac{\frac{RSS_r-RSS_{ur}}{q}}{\frac{RSS_{ur}}{n - k}}$ ~ $F_{q, n - k}$, где

$RSS_{ur}$ – RSS полученной регрессионной модели, $RSS_{r}$ – RSS модели при выполнении условия $H_0$ ($\widehat{Y_{34}} = \hat{\beta_1} + \hat{\beta_2} X_2$).

$RSS_{ur} = \sum_{i=1}^n (Y_i - \hat{Y}_i)^2 = {{ '%.3f' % overall_rss }};$

$RSS_{r} = \sum_{i=1}^n (Y_i - \widehat{Y_{34}}_i)^2 = {{ '%.3f' % restricted34_rss }};$

$F_{крит.} = {{ '%.3f' % restricted34_f_crit }};$
{% if restricted34_f > restricted34_f_crit %}
$F = {{ '%.3f' % restricted34_f }} > {{ '%.3f' % restricted34_f_crit }} \Rightarrow H_0$ отвергается в пользу $H_1$, коэффициенты совместно значимы при $\alpha = 0.05$.{% else %}
$F = {{ '%.3f' % restricted34_f }} \leq {{ '%.3f' % restricted34_f_crit }} \Rightarrow H_0$ принимается, коэффициенты совместно незначимы при $\alpha = 0.05$.{% endif %}

*Построим таблицу корреляции объясняющих переменных.*
  
|&nbsp; | $X_2$ | $X_3$ | $X_4$ |
|-------|-------|-------|-------|
| $X_2$ | 1 | {{ '%.2f' % xs_corr['23'] }} | {{ '%.2f' % xs_corr['24'] }} |
| $X_3$ | {{ '%.2f' % xs_corr['23'] }} | 1 | {{ '%.2f' % xs_corr['34'] }} |
| $X_4$ | {{ '%.2f' % xs_corr['24'] }} | {{ '%.2f' % xs_corr['34'] }} | 1 |

### Часть II

Используем вместо обычной оценки

$\hat{\beta} = (X^T X)^{-1} X^T Y$

оценку ридж-регрессии

$\hat{\beta}_{ridge} = (X^T X + D)^{-1} X^T Y$,

где $D$ — некая матрица (обычно диагональная с неотрицательными элементами на главной диагонали).

Рассмотрим частный случай ридж-регрессии:  

$\hat{\beta}_{ridge} = (X^T X + \lambda I)^{-1} X^T Y$.

Попробуем оценить зависимость $Y$ от $X_2$, $X_3$ и $X_4$ с помощью этой оценки, варьируя значения $\lambda$ в промежутке $[0;2]$ с шагом $0.1$ и построим график зависимости полученных оценок от $\lambda$:

![]({{ figure_path }})

Если прочертить графики дальше, то можно заметить, что при $\lambda \rightarrow +\infty$ коэффициенты $\widehat{\beta_i}_{ridge}$ стремятся к нулю.

