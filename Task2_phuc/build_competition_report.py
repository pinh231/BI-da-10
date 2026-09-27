from pathlib import Path
import json, html, shutil
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

P=Path(__file__).resolve().parent;OLD=P.parent/'task2'
S=json.loads((P/'findings.json').read_text()); E=html.escape
def read(name):return pd.read_csv(P/(name+'.csv'),index_col=0)
M=read('monthly_health');PAIR=read('paired_nov_dec');CAT=read('category_growth_attribution');RULE=read('threshold_sensitivity');T=read('december_support_tiers');R=read('association_robustness')
def table(df):return '<div class="scroll">'+df.to_html(float_format=lambda x:f'{x:,.3f}',border=0,na_rep='Not estimable')+'</div>'
def chart(name,title,body,height=430,source='Source: consumer-month file, 2025. Ratios and scores are synthetic.'):
    x=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 {height}" role="img" aria-label="{E(title)}"><style>text{{font-family:Arial,sans-serif;fill:#152f3e;font-size:14px}}.title{{font-size:23px;font-weight:700}}.note{{font-size:12px;fill:#526b77}}</style><rect width="1100" height="{height}" fill="white"/><text x="28" y="34" class="title">{E(title)}</text>{body}<text x="28" y="{height-14}" class="note">{E(source)}</text></svg>'
    (P/(name+'.svg')).write_text(x);return x
body=''
for i,(mo,r) in enumerate(M.iterrows()):
    x=65+i*83;h=r.low60_pct/100*260;col='#b85530' if mo==12 else '#197c89'
    body+=f'<rect x="{x}" y="{335-h}" width="52" height="{h}" fill="{col}"/><text x="{x+26}" y="{325-h}" text-anchor="middle">{r.low60_pct:.1f}%</text><text x="{x+26}" y="360" text-anchor="middle">{mo:02d}</text>'
for k in [0,20,40,60,80,100]:body+=f'<text x="12" y="{340-k*2.6}">{k}</text>'
body+='<text x="40" y="61">Customers with health score &lt;60 (%)</text><text x="465" y="391">Month of 2025</text>'
trend=chart('01_monthly_monitoring','December exposes pressure hidden by the annual average',body,source='Source: consumer-month file. Monthly denominator: 911–920 observed customers; December n=918.')
TR=read('nov_dec_transitions_counts');body='<text x="350" y="66">December health band (destination)</text>'
for j,c in enumerate(TR.columns):body+=f'<text x="{375+j*170}" y="95" text-anchor="middle">{E(c)}</text>'
for i,(k,row) in enumerate(TR.iterrows()):
    y=116+i*67;body+=f'<text x="30" y="{y+32}">{E(k)} in November (n={int(row.sum())})</text>'
    for j,v in enumerate(row):
        op=.05+.85*v/max(1,row.sum());x=290+j*170
        body+=f'<rect x="{x}" y="{y}" width="166" height="62" fill="#197c89" opacity="{op}"/><text x="{x+83}" y="{y+27}" text-anchor="middle">{int(v)} customers</text><text x="{x+83}" y="{y+48}" text-anchor="middle">{100*v/row.sum():.1f}% of row</text>'
transition=chart('02_paired_transitions','642 of 770 previously stable / healthy customers fall below 60',body,440,source='Source: 909 matched customers observed in November and December. Each row sums to 100%.')
body=''
labels=[('Transaction count',S['paired_count_gmean_ratio']),('Spend per transaction',S['paired_ticket_gmean_ratio']),('Monthly income',S['paired_income_gmean_ratio']),('Spend / income',S['paired_pressure_gmean_ratio'])]
for i,(label,v) in enumerate(labels):
    y=90+i*67;body+=f'<text x="28" y="{y+23}">{label}</text><rect x="285" y="{y}" width="{v*280}" height="32" fill="{"#b85530" if i==3 else "#197c89"}"/><text x="{300+v*280}" y="{y+23}">{v:.4f}× ({(v-1)*100:+.2f}%)</text>'
body+='<line x1="565" x2="565" y1="72" y2="340" stroke="#183446" stroke-dasharray="4 4"/><text x="530" y="370">1× = no change</text><text x="285" y="395">December / November multiplier (geometric mean across customers)</text>'
decomp=chart('03_frequency_decomposition','The increase is driven by frequency; ticket size is almost unchanged',body,435,source='Source: 909 matched customers. Exact spend/count ticket; ratios calculated from unrounded inputs.')
body=''
for i,(k,row) in enumerate(CAT.iterrows()):
    y=80+i*32;w=row.mean_contribution_pp_of_Nov_spend*28
    body+=f'<text x="25" y="{y+15}">{E(k)}</text><rect x="375" y="{y}" width="{w}" height="20" fill="#197c89"/><text x="{386+w}" y="{y+15}">+{row.mean_contribution_pp_of_Nov_spend:.2f} pp</text><text x="930" y="{y+15}">{row.share_change_pp:+.2f} pp</text>'
body+='<text x="375" y="58">Contribution to spend growth</text><text x="895" y="58">Category share change</text><text x="375" y="560">Percentage points of each customer’s November total spend</text>'
category=chart('04_category_attribution','Growth is broad-based across all 14 categories',body,605,source='Source: raw transactions; 909 matched customers. Equal-customer means. Total growth = +105.56%.')
def groupchart(dim,title,labels):
    g=read('demographics_'+dim);v=g if dim=='age_group' else pd.concat([g.head(4),g.tail(4)])
    b='<text x="380" y="65">Mean score (0–100), pooled customer-month observations</text>'
    for i,(k,r) in enumerate(v.iterrows()):
        y=86+i*39;w=r.pooled_mean*5
        b+=f'<text x="22" y="{y+18}">{E(str(k))} (n={int(r.customers)})</text><rect x="380" y="{y}" width="{w}" height="24" fill="#197c89"/><text x="{390+w}" y="{y+18}">{r.pooled_mean:.2f}</text>'
    return chart('05_'+dim,title,b,132+39*len(v),source='Source: consumer-month file, 2025. n = unique customers, not number of months. Rankings are descriptive.')
agechart=groupchart('age_group','Age gaps are modest: only 1.13 points from lowest to highest',None)
occchart=groupchart('occupation','Occupation extremes are not reliable population-level findings',None)
provchart=groupchart('province_city','Geographic gaps merit exploration, not demographic targeting',None)
dist=(OLD/'chart_01_distribution.svg').read_text();(P/'00_distribution.svg').write_text(dist)
def clarify_density_axes(svg_text):
    """Align endpoint labels and disclose the per-panel logarithmic color scale."""
    namespace='http://www.w3.org/2000/svg'
    ET.register_namespace('',namespace)
    root=ET.fromstring(svg_text)
    for label in root.findall('{'+namespace+'}text'):
        x=float(label.get('x',0)); y=float(label.get('y',0))
        # Each density grid is 35 cells * 11 units = 385 units wide.
        if x in (420,900) and y in (304,599):
            label.set('x',str(int(x+30)))
            label.set('text-anchor','end')
        if x in (35,515) and y in (95,390) and label.text=='100':
            label.set('y',str(int(y-5)))
    legend=ET.SubElement(root,'{'+namespace+'}text',{'x':'24','y':'646','class':'note'})
    legend.text='Cell opacity uses log(count + 1), normalized separately per panel. Compare density within each panel only.'
    return ET.tostring(root,encoding='unicode')

assoc=clarify_density_axes((OLD/'chart_02_associations.svg').read_text());(P/'06_associations.svg').write_text(assoc)
sections=[]; english=[]
def sec(id,title,paragraphs,extra='',vn=''):
    english.append('## '+title+'\n\n'+'\n\n'.join(paragraphs))
    texts=''.join('<p>'+E(t)+'</p>' for t in paragraphs)
    if vn:texts+='<aside><strong>Giải thích cho Phúc:</strong> '+E(vn)+'</aside>'
    sections.append(f'<section id="{id}"><div class="eyebrow">{id.upper()}</div><h2>{E(title)}</h2>{texts}{extra}</section>')
sec('thesis','Detect pressure when it happens, then offer support that matches its scale.',[
 'The annual mean health score is 66.37, but December’s mean is 54.25 and 772 of 918 observed customers (84.10%) score below 60. A small stressed segment alone does not describe the full support opportunity.',
 'Among 909 customers observed in both November and December, average health falls by 13.35 points. Transaction frequency increases 95.82% on a geometric-mean basis, while average ticket size increases only 0.11% and income increases 0.44%. Category mix remains broadly stable.',
 'Use a broad, low-cost budgeting response for customers with observed spending pressure, with more focused support for the stressed group. Engagement determines a potential route for delivery; it must not determine who deserves support.'
],vn='Câu chuyện chính là phát hiện áp lực đúng thời điểm. Nhóm căng thẳng rất nhỏ không phản ánh hết nhu cầu hỗ trợ; tháng 12 có cả làn sóng khách chuyển xuống nhóm cần theo dõi. Những phát hiện này chỉ mô tả năm giả lập được cung cấp, không chứng minh hiệu ứng mùa vụ nhiều năm.')
sec('scope','One source of truth; three explicitly different denominators.',[
 'Primary population: 10,992 customer-month observations, 999 distinct customers and 12 calendar months in 2025. Transaction checks cover all 1,852,394 source transactions. The original data are retained without deletion, imputation or outlier winsorization.',
 'Annual prevalence uses customer-months. Annual reach uses unique customers who ever qualify. Current support reach uses only the 918 customers observed in December. Time comparisons use 909 matched November–December customers; a separate 908-customer panel observed in all 12 months confirms the direction.',
 '908 customers have 12 months, 86 have one month and five have two months. Missing months are not zero-spend months. The optional next-month label has 999 missing values at each customer’s last observation; these rows remain in the descriptive analysis.',
 'Official scope retained: score distribution; factors associated with low health; occupation, age and province differences; a reproducible stressed/high-engagement rule. The team’s earlier workload allocation does not limit the analysis. This remains the financial-health task, with evidence handed to segmentation and recommendations.'
],extra='<details><summary>Requirement-to-evidence map</summary>'+table(pd.DataFrame({'Requirement':['Distribution','Associated factors','Demographic differences','Stressed & highly engaged','Business interpretation','Reproducibility'],'Evidence':['Distribution statistics and four segment shares','Correlation robustness, paired panel and transaction decomposition','Full occupation, age and province outputs; sample sizes and weighting checks','Explicit <40 / ≥80 rule, denominator checks and 9 threshold combinations','December support tiers, reach and proposed evaluation plan','Source fingerprint, scripts, CSVs, quality checks and independent verification']}))+'</details>')
seg=pd.read_csv(OLD/'01_segments.csv',index_col=0)
sec('distribution','Stable annual averages conceal periods of low health.',[
 'Mean 66.3660; median 67.7000; sample standard deviation 9.4760 (ddof=1). Quartiles: 60.7 and 73.2. Range: 0.8–90.2. Giving each customer equal weight instead produces a mean of 66.3028.',
 'Stable [60,80): 7,965 / 10,992 (72.46%). Monitoring [40,60): 2,457 (22.35%). Healthy [80,100]: 475 (4.32%). Stressed [0,40): 95 (0.86%). The combined share below 60 is 23.22%.',
 '70 of 999 customers (7.01%) experience at least one stressed month. No customer has a full-observed-period average below 40; using that average to identify stressed customers would miss all 70. “Ever stressed” is not “currently stressed” or “persistently stressed”.'
],dist+table(seg),vn='Không dùng điểm trung bình năm làm cờ cảnh báo tháng. Cùng một người có thể ổn định phần lớn thời gian nhưng có một tháng cần hỗ trợ.')
sec('time','The December deterioration survives a like-for-like customer comparison.',[
 f'In the 909-customer matched sample, mean health changes from {S["paired_nov_mean"]:.2f} to {S["paired_dec_mean"]:.2f}: {S["paired_mean_change"]:.2f} points (customer bootstrap 95% interval {S["paired_change_ci95"][0]:.2f} to {S["paired_change_ci95"][1]:.2f}; 3,000 resamples). Median change is −13.70; 840 / 909 customers (92.41%) decline.',
 'Below-60 prevalence rises from 139 / 909 (15.29%) to 769 / 909 (84.60%), an increase of 69.31 percentage points. Of 770 previously stable or healthy customers, 642 (83.38%) fall below 60. These are the matched-sample results, distinct from the full December snapshot.',
 f'The complete 908-customer panel shows a {S["complete_panel_change"]:.2f}-point mean change. The result is not explained solely by new or disappearing customers. One synthetic year cannot establish recurring seasonality or identify why the data generator produced this pattern.'
],trend+transition,vn='So sánh cùng 909 người giúp loại khả năng điểm giảm chỉ vì tháng 12 có nhóm khách khác xuất hiện. Kết luận vững là có thay đổi trong cùng khách hàng; chưa được gọi đây là tác động nhân quả của tháng 12.')
sec('mechanism','More transactions, rather than larger tickets, account for the pressure increase.',[
 f'For each matched customer, spend / income = transaction count × exact average ticket / income. The December / November geometric-mean multipliers are {S["paired_count_gmean_ratio"]:.4f}× for count, {S["paired_ticket_gmean_ratio"]:.4f}× for ticket, {S["paired_income_gmean_ratio"]:.4f}× for income and {S["paired_pressure_gmean_ratio"]:.4f}× for spend/income. Multiplicative changes are decomposed with logarithms, without a residual.',
 'Mean log contributions are +0.67204 from frequency, +0.00114 from ticket size and −0.00444 from income. Frequency contributes 100.49% of the net log increase; the value exceeds 100% because the small income increase offsets part of the pressure. This is an accounting identity, not a causal attribution to customer intent.',
 f'In the transaction-level attribution, the mean of individual spending increases is +{S["mean_customer_spend_growth_pct"]:.2f}%. This arithmetic average differs from the +96.05% geometric average by design. For each category we divide its spending change by that customer’s November total; the category contributions sum exactly to +105.56 percentage points.',
 'All 14 categories contribute positively. In-store groceries contributes the most (+15.83 points), but represents only 15.00% of total mean growth. The largest absolute category-share movement is just 0.53 percentage points. This supports a broad frequency increase, not a demonstrated shift toward one discretionary category.'
],decomp+category+'<details><summary>Full arithmetic attribution and bootstrap intervals</summary>'+table(CAT)+'</details>',vn='Người đọc dễ đổ lỗi cho mua sắm tùy ý, nhưng dữ liệu không ủng hộ kết luận đó. Siêu thị đóng góp lớn nhất vì vốn chiếm tỷ trọng lớn; tỷ trọng của nó còn giảm nhẹ. Cần hỗ trợ kiểm soát nhịp chi tiêu toàn ngân sách, thay vì khẳng định một danh mục là thủ phạm.')
sec('associations','Spending relative to income remains the strongest pooled association.',[
 'An exploratory screen covers 13 contemporaneous numeric indicators: the four main ratios, engagement, online share, transaction count, active days, category diversity, recency, age and opening/ending balance normalized by income. Spend/income and utilization remain the strongest pooled Pearson associations. Future labels, health-band labels, identifiers and raw financial VND magnitudes are excluded; discretionary share is omitted because it equals one minus essential share.',
 'Pooled Pearson correlations with health: spend/income −0.898; utilization −0.862; volatility −0.496; essential share +0.481. Spearman gives the same direction. Spend/income remains −0.902 when December is excluded and −0.850 after removing both customer and month averages in the balanced panel.',
 'Essential share is positively associated with health at the monthly grain, but its correlation across customer averages is only +0.079. A monthly composition signal is not a stable customer trait. Volatility shows the same distinction: pooled −0.496 versus customer-average −0.125.',
 'A sensitivity analysis removes the outer 1% of each predictor separately; no sign changes occur. The primary analysis retains all observations. Two-way demeaning controls additive customer and month differences; it does not eliminate every confounder.',
 'Spend/income and utilization share spending in their numerators. Their conditional-model VIFs are about 10.8 and 10.7, so coefficients cannot reliably separate independent effects. The in-sample explanatory R² of 0.849 is not a predictive accuracy claim. The score-generation formula is not supplied; some association may be built into the derived score.'
],assoc+table(R)+'<details><summary>Expanded 13-indicator screen</summary>'+table(read('expanded_indicator_screen'))+'</details><details><summary>Conditional association diagnostics (appendix, not headline drivers)</summary>'+table(read('two_way_conditional_associations'))+'</details>',vn='Giữ tương quan như bằng chứng mô tả, không chuyển thành câu “tăng X sẽ làm điểm giảm Y”. R² ở đây là mức khớp trong mẫu, không phải chất lượng dự báo hay điểm đánh giá bài thi.')
sec('demographics','Demographics explain where to investigate, not whom to penalize.',[
 'Age: pooled means range from 65.79 (25–34, 177 customers) to 66.92 (55+, 390 customers), a 1.13-point gap. The lowest group changes to under-25s when each customer receives equal weight. The effect is small relative to the temporal deterioration.',
 'Province: Ha Tinh averages 60.43 (12 customers), versus Hanoi 68.04 (80), a 7.61-point gap. The same extremes persist with equal-customer weighting. Rankings remain unadjusted for customer composition, and small provincial samples limit generalization.',
 'Occupation: 396 labels for 999 customers; 128 occupations have only one customer and none exceeds ten. The extremes are film-set designer, 49.80 (one customer), and marketing director, 77.72 (three). Report these because the task requests them; do not treat them as occupational population estimates.',
 'The complete tables include pooled means, equal-customer means, full-panel means, customer counts and bootstrap intervals. The demographic bootstrap intervals estimate the equal-customer mean, not the pooled customer-month mean. A one-customer group has no reported bootstrap interval. Demographics are excluded from the proposed support-eligibility rules.'
],agechart+provchart+occchart+''.join('<details><summary>All '+dim+' results</summary>'+table(read('demographics_'+dim))+'</details>' for dim in ['age_group','province_city','occupation']))
explorer='<div class="explorer"><h3>Threshold sensitivity explorer</h3><label>Health score below <select id="health"><option>35</option><option selected>40</option><option>45</option></select></label><label>Engagement at least <select id="engagement"><option>60</option><option>70</option><option selected>80</option></select></label><div id="rule-result" aria-live="polite"></div><p class="small">Same-month intersection. December denominator: 918; annual distinct customers: 999; annual observations: 10,992.</p></div>'
sec('crossover','Use an interpretable strict rule, and show the sensitivity rather than hide it.',[
 'Primary crossover definition: financial_health_score <40 AND engagement_score ≥80 in the same customer-month. The health threshold matches the stressed band; the engagement threshold matches the supplied “very high engagement” band. This stricter definition replaces the previous team-example threshold of 70, not the underlying data.',
 'The rule identifies 52 / 10,992 observations (0.4731%), 45 / 999 ever-qualifying customers (4.5045%), and eight / 918 December customers (0.8715%). Six of the 45 qualify in two or more months. All 52 observations have spending above income.',
 'At health <40, engagement ≥60 identifies 93 observations / 69 customers; ≥70 identifies 81 / 64; ≥80 identifies 52 / 45. December counts are 25, 25 and eight respectively. A stricter reach estimate is not inherently better: ≥80 gives a clear segment definition, while support is still available to every stressed customer.',
 'Very high engagement occurs in 54.74% of stressed observations versus 34.79% of all observations. At the ≥70 threshold, the comparison reverses (85.26% versus 91.44%). Therefore “stressed customers are more engaged” is not threshold-independent. Engagement describes recorded transactions, not marketing consent or verified contactability.'
],explorer+table(read('crossover_strict_profile'))+'<details><summary>All nine health/engagement combinations</summary>'+table(RULE)+'</details>',vn='Ngưỡng 80 không được chọn để làm đẹp kết quả. Nó khớp nhãn “tương tác rất cao”, dễ giải thích hơn. 25 khách căng thẳng tháng 12 vẫn đều có nhu cầu hỗ trợ dù chỉ 8 người thuộc nhóm tương tác rất cao.')
sec('actions','Match the support model to a 681-customer December pressure cohort.',[
 'Tier 1 — 25 stressed customers (2.72% of December): offer a voluntary budget review and tailored reminders; eight have very high engagement. This group may warrant more intensive support because its observed health is below 40, not because of demographic membership.',
 'Tier 2 — 656 monitoring customers whose spending exceeds income (71.46%): provide scalable, opt-in budgeting and cumulative-spend alerts. 298 have very high engagement. At this scale, a mass service workflow is more plausible than an individually staffed intervention for every customer.',
 'Tier 3 — 91 monitoring customers without spend above income (9.91%): provide light-touch education or planning support, avoiding inaccurate “you overspent your income” messages. Tier 4 — 146 stable/healthy customers (15.90%): retain general self-service tools. The four groups are disjoint and cover all 918 observed customers.',
 'Tier 1 + Tier 2 reaches 681 distinct customers (74.18% of the December snapshot), including 306 with very high engagement. This is observed eligibility, not predicted conversion, validated intervention effectiveness, or confirmed delivery capacity.',
 'Channel evidence: POS averages 62.96% of spend for Tier 1 and 59.24% for Tier 2 (equal-customer average). High engagement does not establish an app-first customer journey. App-only outreach should not be assumed; contact permissions and usable delivery channels are absent from the dataset.'
],table(T)+table(read('december_channel_profiles')),vn='Bài thi nên có hành động tương xứng quy mô: hỗ trợ chuyên sâu cho nhóm nhỏ, công cụ tự phục vụ cho nhóm rộng. Không gộp 45 khách từng thỏa cả năm với 8 khách tháng 12, và không cộng hai tập khách chồng lấn.')
sec('evaluation','Propose measurable validation, without inventing a business lift.',[
 'Proposed pilot, not a result: at the next observable cycle, identify customers using only information available by that date, record consent/contactability, and randomize eligible customers between a support invitation and existing service. Randomize by customer, stratifying by support tier; keep access to standard support unchanged.',
 'Primary outcome proposal: the next-month share spending above income, evaluated by original randomized assignment. Secondary outcomes: spend/income, health-score change, tool activation and opt-out/complaint rate. Report follow-up coverage and missing outcomes by arm; do not silently drop customers who disappear.',
 'Reach is measured here; effect size, ROI, saved VND and channel response are not. A power calculation requires a justified minimum worthwhile effect, usable cohort size and follow-up assumptions; those are not supplied. January 2026 outcomes are absent, so the December intervention cannot be backtested as effective.',
 'If monthly aggregate files are the only available feed, run support after the month closes. In-month early warnings require live transaction totals and an income estimate available at that time, followed by separate validation. Do not claim a real-time capability from a year-end CSV.',
 'The score is a wellbeing indicator. Never use it to approve or deny credit, cut credit limits or block accounts. No proposed support rule uses occupation, age or province to exclude customers.'
])
sec('methods','What is verified, and what remains uncertain.',[
 'Verified: 16 core checks and 15 extension checks pass, including source fingerprint consistency, exact per-customer log decomposition, paired transition totals, complete December tier coverage and reconciliation of transaction categories to monthly spend. Key headline calculations are independently recomputed with Python’s standard library.',
 'The paired comparison resamples customers, not individual months, 3,000 times with seed 20260928. Category and demographic intervals use 1,000 customer resamples. These quantify resampling stability in the synthetic sample; they do not certify population estimates or correct for exploratory multiple comparisons.',
 'The case notes that source simulation dates were folded into a single 2025 year. Transaction-density and calendar artifacts may explain the observed pattern. Treat the December result as a diagnostic and an intervention hypothesis, not a forecast of every future December.',
 'Main data limitation: synthetic income/credit magnitudes, unknown score-generation formula, one year, incomplete customer coverage and tiny occupation samples. Credit utilization here is spend/credit limit capped at 1.5. Spending volatility is supplied as a coefficient of variation without a fully documented aggregation window.',
 'Source documents: BI10_ROUND01.pdf (Task 2, PDF page 9), supplied case-study file and data_dictionary.xlsx. Official presentation language is English. All required Task 2 elements are covered; extra temporal and transaction analysis strengthens the evidence rather than replaces them.'
],'<details><summary>Extension verification checks</summary>'+table(read('quality_checks'))+'</details><p class="small">Consumer-month source SHA-256: '+S['source_sha256']+'</p>')
sec('presentation','Recommended presentation narrative: six evidence-led pages.',[
 '1. The annual average hides a December deterioration. Show distribution plus the monthly below-60 chart. State the customer-month denominator.',
 '2. The deterioration occurs within the same customers. Show the paired transition matrix and −13.35-point change with the bootstrap interval.',
 '3. The pressure is frequency-led and broad-based. Show geometric multipliers and category attribution. State arithmetic versus geometric definitions.',
 '4. Behavioral associations are robust; demographic stories are weaker. Show the correlation robustness and compact age/province/occupation panels with n.',
 '5. Define stressed and very highly engaged transparently. Show 52 observations, 45 ever-customers, eight December customers and sensitivity to 60/70/80.',
 '6. Turn the finding into a support design. Show the 25/656/91/146 tiers, measured reach and proposed experiment. Do not claim proven lift. Six pages are a recommendation for this section; the team should allocate them within the full-deck limit.'
])
css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#f1f4f5;color:#152f3e;font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1200px;margin:auto;background:white;padding:52px}header{padding:20px 0 32px}h1{font-size:42px;line-height:1.13;max-width:850px;margin:15px 0}h2{font-size:27px;line-height:1.25;max-width:940px}h3{font-size:19px}.eyebrow{font-size:12px;font-weight:700;letter-spacing:2px;color:#197c89}section{padding:38px 0;border-top:1px solid #cfdbdf}p{max-width:1000px}nav{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;padding:20px 0}a{color:#146c78}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding:24px 0}.metric{border-top:3px solid #197c89;padding-top:13px}.number{font-size:31px;font-weight:700}.small{font-size:12px;color:#526b77}.scroll{overflow:auto;margin:20px 0}table{border-collapse:collapse;font-size:12px;width:100%}th,td{padding:9px;border-bottom:1px solid #dbe4e7;text-align:right;white-space:nowrap}th{background:#eef4f5}th:first-child{text-align:left}svg{display:block;width:100%;height:auto;margin:25px 0}aside{padding:16px 20px;background:#f2f7f7;border-left:3px solid #197c89;font-size:14px}details{padding:14px 0}summary{cursor:pointer;color:#146c78;font-weight:600}.explorer{padding:24px;background:#f2f7f7}select{padding:8px;margin:5px 20px 5px 8px;font:inherit}#rule-result{font-size:20px;padding:16px 0}footer{padding:25px 0;font-size:12px;color:#526b77}@media(max-width:700px){main{padding:22px}h1{font-size:33px}.metrics{grid-template-columns:1fr}h2{font-size:24px}}@media print{body{background:white}main{padding:0;max-width:none}nav,.explorer{display:none}section{break-before:page}details:not([open]){display:none}aside{background:white}.metrics{grid-template-columns:repeat(3,1fr)}}'''
ruledata=RULE.reset_index(drop=True).to_dict('records')
js='const rules='+json.dumps(ruledata)+';function update(){const h=+document.getElementById("health").value,e=+document.getElementById("engagement").value;const r=rules.find(x=>x.health_below===h&&x.engagement_at_least===e);document.getElementById("rule-result").textContent=`${r.customer_months} customer-months (${r.customer_month_pct.toFixed(3)}%) · ${r.ever_customers} ever-customers (${r.ever_customer_pct.toFixed(2)}%) · ${r.dec_customers} December customers (${r.dec_customer_pct.toFixed(2)}%)`;}document.getElementById("health").addEventListener("change",update);document.getElementById("engagement").addEventListener("change",update);update();'
nav=''.join(f'<a href="#{k}">{v}</a>' for k,v in [('thesis','Executive finding'),('time','Matched comparison'),('mechanism','Transaction evidence'),('demographics','Demographics'),('crossover','Crossover rule'),('actions','Support design'),('methods','Audit')])
doc='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BI10 Task 2 · Competition Report · Trọng Phúc</title><style>'+css+'</style><main><header><div class="eyebrow">BI10 / ROUND 01 / TRỌNG PHÚC / TASK 2</div><h1>Financial pressure is a moment to detect, not a permanent customer label.</h1><p>Financial Health Analysis · Competition edition · English findings with Vietnamese explanations</p><div class="metrics"><div class="metric"><div class="number">−13.35 points</div><div>November → December health change</div><div class="small">909 matched customers</div></div><div class="metric"><div class="number">+95.82%</div><div>Transaction frequency change</div><div class="small">Geometric mean of paired ratios</div></div><div class="metric"><div class="number">681 customers</div><div>Stressed or monitoring + overspending</div><div class="small">74.18% of 918 December customers</div></div></div><nav>'+nav+'</nav></header>'+''.join(sections)+'<footer>Prepared from the supplied BI10 data. Reproducible calculations and full CSV evidence accompany this report. Findings are descriptive; proposed interventions are not validated outcomes.</footer></main><script>'+js+'</script></html>'
(P/'report.html').write_text(doc,encoding='utf8');(P/'report_en.md').write_text('# BI10 Task 2 — Competition report\n\n'+'\n\n'.join(english),encoding='utf8')
print('Generated English competition report, Vietnamese explanations, interactive sensitivity and 9 charts.')
