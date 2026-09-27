"""Task 2 competition extension. Source files are read only; no model tuning to a target score."""
from pathlib import Path
import json, hashlib, platform
import numpy as np
import pandas as pd

P=Path(__file__).resolve().parent; SRC=P.parent.parent/'BI10_ROUND01_DATASET'
D=pd.read_csv(SRC/'consumer_financial_health_engagement_2025.csv')
H='financial_health_score'; F=['spend_to_income_ratio','credit_utilization_ratio','spending_volatility','essential_spend_ratio']
D['month']=pd.to_datetime(D.analysis_month).dt.month
D['health_band']=pd.cut(D[H],[-1,40,60,80,101],right=False,labels=['Stressed','Monitoring','Stable','Healthy'])
D['age_group']=pd.cut(D.age,[0,25,35,45,55,np.inf],right=False,labels=['<25','25–34','35–44','45–54','55+'])
D['low60']=D[H]<60; D['stress40']=D[H]<40; D['high_eng80']=D.engagement_score>=80
Q=[]
def ck(name,ok,details=''): Q.append(dict(check=name,passed=bool(ok),details=str(details)))
def save(n,x): x.to_csv(P/(n+'.csv'),encoding='utf-8-sig',float_format='%.12g')
def serial(x):
    if isinstance(x,(np.integer,np.floating)):return x.item()
    if isinstance(x,np.ndarray):return x.tolist()
    raise TypeError(type(x))
rng=np.random.default_rng(20260928)
def ci_mean(v,b=3000):
    v=np.asarray(v,dtype=float)
    z=np.array([rng.choice(v,len(v),replace=True).mean() for _ in range(b)])
    return np.quantile(z,[.025,.975]).tolist()
ck('Unique customer-month',not D.duplicated(['consumer_id','month']).any())
ck('Required analysis variables complete',D[[H,'engagement_score','consumer_id','month','age','occupation','province_city']+F].notna().all().all())
ck('Source fingerprint unchanged',hashlib.sha256((SRC/'consumer_financial_health_engagement_2025.csv').read_bytes()).hexdigest()=='f7b52bc5f80b879a0a5d1ce63bc3e73c8bb3563c0f754217fcce25b4bd1aec49')
coverage=D.groupby('consumer_id').size();full=coverage.index[coverage==12];B=D[D.consumer_id.isin(full)].copy()
nov=D[D.month==11].set_index('consumer_id'); dec=D[D.month==12].set_index('consumer_id')
ids=nov.index.intersection(dec.index).sort_values();A=nov.loc[ids].copy();Z=dec.loc[ids].copy();n=len(ids)
delta=Z[H]-A[H]
pair=pd.DataFrame({'health_nov':A[H],'health_dec':Z[H],'health_change':delta,'spend_ratio_dec_nov':Z.total_spend_vnd/A.total_spend_vnd,'income_ratio_dec_nov':Z.monthly_income_vnd/A.monthly_income_vnd,'count_ratio_dec_nov':Z.transaction_count/A.transaction_count,'ticket_ratio_dec_nov':(Z.total_spend_vnd/Z.transaction_count)/(A.total_spend_vnd/A.transaction_count)})
pair['income_pressure_ratio_dec_nov']=(Z.total_spend_vnd/Z.monthly_income_vnd)/(A.total_spend_vnd/A.monthly_income_vnd)
pair['log_pressure_change']=np.log(pair.income_pressure_ratio_dec_nov)
pair['log_frequency_contribution']=np.log(pair.count_ratio_dec_nov)
pair['log_ticket_contribution']=np.log(pair.ticket_ratio_dec_nov)
pair['log_income_contribution']=-np.log(pair.income_ratio_dec_nov)
ck('Log decomposition exact per customer',np.allclose(pair.log_pressure_change,pair.log_frequency_contribution+pair.log_ticket_contribution+pair.log_income_contribution,atol=1e-12))
save('paired_nov_dec',pair)
components=pair[['log_frequency_contribution','log_ticket_contribution','log_income_contribution']].mean()
decomp=pd.DataFrame({'mean_log_contribution':components,'percent_of_net_log_pressure_change':components/pair.log_pressure_change.mean()*100})
decomp['geometric_multiplier']=np.exp(decomp.mean_log_contribution)
save('pressure_decomposition',decomp)
trans=pd.crosstab(A.health_band,Z.health_band,dropna=False)
save('nov_dec_transitions_counts',trans);save('nov_dec_transitions_row_percent',trans.div(trans.sum(axis=1),axis=0)*100)
ck('Paired transition count reconciles',trans.to_numpy().sum()==n)
summary={'rows':len(D),'customers':D.consumer_id.nunique(),'complete_customers':len(full),'paired_customers':n,'mean_score':D[H].mean(),'median_score':D[H].median(),'sample_sd':D[H].std(),'paired_nov_mean':A[H].mean(),'paired_dec_mean':Z[H].mean(),'paired_mean_change':delta.mean(),'paired_median_change':delta.median(),'paired_change_ci95':ci_mean(delta),'paired_declined_n':int((delta<0).sum()),'paired_low60_nov_n':int(A.low60.sum()),'paired_low60_dec_n':int(Z.low60.sum()),'paired_low60_increase_pp':(Z.low60.mean()-A.low60.mean())*100,'paired_low60_increase_ci95_pp':np.array(ci_mean((Z.low60.astype(int)-A.low60.astype(int))*100)),'new_low60_n':int((~A.low60 & Z.low60).sum()),'eligible_new_low60_n':int((~A.low60).sum()),'paired_spend_gmean_ratio':np.exp(np.log(pair.spend_ratio_dec_nov).mean()),'paired_income_gmean_ratio':np.exp(np.log(pair.income_ratio_dec_nov).mean()),'paired_pressure_gmean_ratio':np.exp(pair.log_pressure_change.mean()),'paired_count_gmean_ratio':np.exp(np.log(pair.count_ratio_dec_nov).mean()),'paired_ticket_gmean_ratio':np.exp(np.log(pair.ticket_ratio_dec_nov).mean()),'spend_increased_n':int((pair.spend_ratio_dec_nov>1).sum()),'complete_panel_change':(B[B.month==12].set_index('consumer_id')[H]-B[B.month==11].set_index('consumer_id')[H]).mean()}
month=D.groupby('month').agg(customers=('consumer_id','nunique'),mean_score=(H,'mean'),median_score=(H,'median'),low60_n=('low60','sum'),stress40_n=('stress40','sum'),spend_income_mean=('spend_to_income_ratio','mean'),engagement_mean=('engagement_score','mean'))
month['low60_pct']=month.low60_n/month.customers*100;month['stress40_pct']=month.stress40_n/month.customers*100
save('monthly_health',month)
complete_month=B.groupby('month').agg(mean_score=(H,'mean'),low60_pct=('low60',lambda s:s.mean()*100),stress40_pct=('stress40',lambda s:s.mean()*100))
save('complete_panel_monthly_health',complete_month)
hist=D.groupby('consumer_id').agg(observed_months=('month','size'),low60_months=('low60','sum'),stress40_months=('stress40','sum'),mean_score=(H,'mean'))
hist['share_low60_observed_months']=hist.low60_months/hist.observed_months
save('customer_health_history',hist)
# Consecutive observed calendar months only, avoiding fabricated transitions over gaps.
prev=D.copy();prev['month']=prev.month+1
edges=prev[['consumer_id','month','health_band','low60','stress40']].merge(D[['consumer_id','month','health_band','low60','stress40']],on=['consumer_id','month'],suffixes=('_previous','_current'),validate='one_to_one')
save('all_adjacent_transitions',pd.crosstab(edges.health_band_previous,edges.health_band_current,dropna=False))
ck('Adjacent transitions have no missing status',edges.notna().all().all())
# Time and customer confounding checks use balanced panel double demeaning.
demean=B[F+[H]]-B.groupby('consumer_id')[F+[H]].transform('mean')-B.groupby('month')[F+[H]].transform('mean')+B[F+[H]].mean()
C=D.groupby('consumer_id')[F+[H]].mean()
robust=pd.DataFrame({'pooled_Pearson':D[F+[H]].corr()[H].loc[F],'pooled_Spearman':D[F+[H]].corr(method='spearman')[H].loc[F],'customer_means_Pearson':C.corr()[H].loc[F],'balanced_two_way_demeaned_Pearson':demean.corr()[H].loc[F],'excluding_December_Pearson':D[D.month!=12][F+[H]].corr()[H].loc[F]})
for f in F:
    lo,hi=D[f].quantile([.01,.99]); trimmed=D[D[f].between(lo,hi)]
    robust.loc[f,'own_predictor_trim_1_99_Pearson']=trimmed[[f,H]].corr().iloc[0,1]
save('association_robustness',robust)
# Broad exploratory screen beyond the original team's four suggested indicators.
screen=D.copy()
screen['ending_balance_to_income']=screen.ending_balance_vnd/screen.monthly_income_vnd
screen['opening_balance_to_income']=screen.opening_balance_vnd/screen.monthly_income_vnd
candidates=F+['engagement_score','online_spend_ratio','transaction_count','active_transaction_days','category_diversity','transaction_recency_days','ending_balance_to_income','opening_balance_to_income','age']
screening=pd.DataFrame({'Pearson':screen[candidates+[H]].corr()[H].loc[candidates],'Spearman':screen[candidates+[H]].corr(method='spearman')[H].loc[candidates]})
screening=screening.loc[screening.Pearson.abs().sort_values(ascending=False).index]
save('expanded_indicator_screen',screening)
# Standardized OLS after two-way demeaning: conditional association, no causal interpretation.
X=demean[F].to_numpy();y=demean[H].to_numpy();X=X/X.std(axis=0,ddof=0);y=y/y.std(ddof=0)
beta=np.linalg.lstsq(X,y,rcond=None)[0]
ols=pd.DataFrame({'standardized_conditional_coefficient':beta},index=F)
for j,f in enumerate(F):
    other=np.delete(X,j,axis=1); pred=other@np.linalg.lstsq(other,X[:,j],rcond=None)[0]
    r2=1-np.square(X[:,j]-pred).sum()/np.square(X[:,j]).sum();ols.loc[f,'VIF']=1/(1-r2)
save('two_way_conditional_associations',ols)
summary['within_model_R2']=1-np.square(y-X@beta).sum()/np.square(y).sum()
# Unadjusted customer-level demographic ranking with bootstrap; no demographic targeting rule.
demog={}
customer=D.groupby('consumer_id').agg(mean_score=(H,'mean'),age_group=('age_group','first'),occupation=('occupation','first'),province_city=('province_city','first'))
for dim in ['age_group','occupation','province_city']:
    g=D.groupby(dim,observed=True).agg(customer_months=(H,'size'),customers=('consumer_id','nunique'),pooled_mean=(H,'mean'),low60_pct=('low60',lambda s:s.mean()*100),stress40_pct=('stress40',lambda s:s.mean()*100))
    g['equal_customer_mean']=customer.groupby(dim,observed=True).mean_score.mean()
    # Common time exposure: only customers with all 12 months.
    g['complete_panel_mean']=B.groupby(dim,observed=True)[H].mean()
    g['complete_panel_customers']=B.groupby(dim,observed=True).consumer_id.nunique()
    for key,v in customer.groupby(dim,observed=True).mean_score:
        low,high=ci_mean(v,1000) if len(v)>=2 else (np.nan,np.nan)
        g.loc[key,'customer_bootstrap_ci95_low']=low;g.loc[key,'customer_bootstrap_ci95_high']=high
    g['small_n']=g.customers<10
    g=g.sort_values('pooled_mean');save('demographics_'+dim,g);demog[dim]=g
# Canonical stricter primary definition: health <40 and engagement >=80.
rules=[]
for health in [35,40,45]:
    for eng in [60,70,80]:
        m=D[H].lt(health)&D.engagement_score.ge(eng);current=dec[H].lt(health)&dec.engagement_score.ge(eng)
        rules.append(dict(health_below=health,engagement_at_least=eng,customer_months=int(m.sum()),customer_month_pct=m.mean()*100,ever_customers=D.loc[m,'consumer_id'].nunique(),ever_customer_pct=D.loc[m,'consumer_id'].nunique()/999*100,dec_customers=int(current.sum()),dec_customer_pct=current.mean()*100))
save('threshold_sensitivity',pd.DataFrame(rules))
cross=D.stress40&D.high_eng80
save('crossover_strict_observations',D[cross].set_index(['consumer_id','analysis_month']))
cross_history=D[cross].groupby('consumer_id').agg(qualifying_months=('month','size'),first_month=('month','min'),last_month=('month','max'))
save('crossover_strict_customers',cross_history)
crossprofile=D[cross][F+[H,'engagement_score','online_spend_ratio']].agg(['mean','median']).T
save('crossover_strict_profile',crossprofile)
summary.update(strict_observations=int(cross.sum()),strict_customers=D.loc[cross,'consumer_id'].nunique(),strict_dec=int((dec.stress40&dec.high_eng80).sum()),strict_recurrent_customers=int((cross_history.qualifying_months>=2).sum()),all_high_eng80_pct=D.high_eng80.mean()*100,stress_high_eng80_pct=D.loc[D.stress40].high_eng80.mean()*100,strict_over_income=int(D.loc[cross].spend_to_income_ratio.gt(1).sum()))
# Disjoint support tiers at a common snapshot, independent of engagement eligibility.
dec=dec.copy();dec['support_tier']=np.select([dec[H]<40,(dec[H]<60)&(dec.spend_to_income_ratio>1),dec[H]<60],['1. Stressed','2. Monitoring + spend above income','3. Monitoring without overspend'],default='4. Stable / healthy')
tiers=dec.groupby('support_tier').agg(customers=(H,'size'),mean_score=(H,'mean'),mean_spend_income=('spend_to_income_ratio','mean'),very_high_engagement=('high_eng80','sum'))
tiers['percent_of_dec_customers']=tiers.customers/len(dec)*100
save('december_support_tiers',tiers);save('december_customer_support_list',dec)
ck('Support tiers cover December exactly once',tiers.customers.sum()==len(dec) and dec.index.is_unique)
# Raw transaction analysis: equal-customer normalized category contributions, not raw VND rankings.
parts=[];channelparts=[];raw_rows=0;raw_missing=0;raw_negative=0
for chunk in pd.read_csv(SRC/'consumer_transactions_2025.csv',usecols=['consumer_id','transaction_month','spending_category','transaction_channel','spend_amount_vnd','essential_spending_flag'],chunksize=250000):
    raw_rows+=len(chunk);raw_missing+=int(chunk.isna().any(axis=1).sum());raw_negative+=int(chunk.spend_amount_vnd.lt(0).sum())
    v=chunk[chunk.consumer_id.isin(ids)&chunk.transaction_month.isin([11,12])]
    parts.append(v.groupby(['consumer_id','transaction_month','spending_category']).agg(spend=('spend_amount_vnd','sum'),count=('spend_amount_vnd','size'),essential_min=('essential_spending_flag','min'),essential_max=('essential_spending_flag','max')))
    z=chunk[(chunk.transaction_month==12)&chunk.consumer_id.isin(dec.index)]
    channelparts.append(z.groupby(['consumer_id','transaction_channel']).spend_amount_vnd.agg(['sum','size']))
raw=pd.concat(parts).groupby(level=[0,1,2]).agg(spend=('spend','sum'),count=('count','sum'),essential_min=('essential_min','min'),essential_max=('essential_max','max'))
ck('Raw required fields complete',raw_missing==0);ck('Raw spend nonnegative',raw_negative==0)
category_flags=raw.groupby(level=2).agg(min_flag=('essential_min','min'),max_flag=('essential_max','max'))
ck('Category essential flags consistent',category_flags.min_flag.eq(category_flags.max_flag).all())
categories=raw.index.get_level_values(2).unique().sort_values()
novcat=raw.xs(11,level=1).spend.unstack(fill_value=0).reindex(index=ids,columns=categories,fill_value=0)
deccat=raw.xs(12,level=1).spend.unstack(fill_value=0).reindex(index=ids,columns=categories,fill_value=0)
ck('November category spend reconciles exactly',np.array_equal(novcat.sum(axis=1),A.total_spend_vnd))
ck('December category spend reconciles exactly',np.array_equal(deccat.sum(axis=1),Z.total_spend_vnd))
contributions=(deccat-novcat).div(A.total_spend_vnd,axis=0)*100
cat=pd.DataFrame({'mean_contribution_pp_of_Nov_spend':contributions.mean(),'median_contribution_pp_of_Nov_spend':contributions.median(),'Nov_mean_customer_share_pct':novcat.div(A.total_spend_vnd,axis=0).mean()*100,'Dec_mean_customer_share_pct':deccat.div(Z.total_spend_vnd,axis=0).mean()*100,'essential_flag':category_flags.min_flag})
cat['share_change_pp']=cat.Dec_mean_customer_share_pct-cat.Nov_mean_customer_share_pct
cat['share_of_mean_spend_growth_pct']=cat.mean_contribution_pp_of_Nov_spend/contributions.mean().sum()*100
for key in cat.index:cat.loc[key,'contribution_ci95_low'],cat.loc[key,'contribution_ci95_high']=ci_mean(contributions[key],1000)
cat=cat.sort_values('mean_contribution_pp_of_Nov_spend',ascending=False);save('category_growth_attribution',cat)
ck('Category attribution sums to arithmetic mean customer spend growth',np.isclose(cat.mean_contribution_pp_of_Nov_spend.sum(),(pair.spend_ratio_dec_nov-1).mean()*100,atol=1e-10))
channel=pd.concat(channelparts).groupby(level=[0,1]).sum();shares=channel['sum'].unstack(fill_value=0).div(dec.total_spend_vnd,axis=0)
ck('December channel shares sum to 1 for each customer',np.allclose(shares.sum(axis=1),1))
save('december_channel_profiles',shares.join(dec.support_tier).groupby('support_tier').mean()*100)
summary.update(raw_transactions=raw_rows,mean_customer_spend_growth_pct=(pair.spend_ratio_dec_nov-1).mean()*100,top_category=str(cat.index[0]),top_category_contribution_pp=cat.iloc[0].mean_contribution_pp_of_Nov_spend,top_category_share_of_growth_pct=cat.iloc[0].share_of_mean_spend_growth_pct)
save('quality_checks',pd.DataFrame(Q).set_index('check'))
ck('All core source checks remain passed',all(c['pass'] for c in json.loads((P.parent/'task2/audit.json').read_text())['checks']))
save('quality_checks',pd.DataFrame(Q).set_index('check'))
summary['checks_passed']=sum(q['passed'] for q in Q);summary['checks_total']=len(Q);summary['bootstrap_seed']=20260928
summary['source_sha256']=hashlib.sha256((SRC/'consumer_financial_health_engagement_2025.csv').read_bytes()).hexdigest()
summary['python']=platform.python_version();summary['pandas']=pd.__version__;summary['numpy']=np.__version__
(P/'findings.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=serial))
print(json.dumps(summary,ensure_ascii=False,indent=2,default=serial));print('\nDECOMPOSITION\n',decomp.to_string());print('\nROBUSTNESS\n',robust.to_string());print('\nCATEGORIES\n',cat.head(6).to_string());print('\nTIERS\n',tiers.to_string());print('\nCHANNELS\n',shares.join(dec.support_tier).groupby('support_tier').mean().to_string())
assert all(q['passed'] for q in Q),Q
