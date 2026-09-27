"""Independent headline verification using only Python's standard library."""
from pathlib import Path
import csv, json, math, statistics
P=Path(__file__).resolve().parent
rows=list(csv.DictReader(open(P.parent.parent/'BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv')))
s=json.loads((P/'findings.json').read_text());results={}
def verify(name,ok):results[name]=bool(ok)
def close(a,b):return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-10)
nov={r['consumer_id']:r for r in rows if r['analysis_month']=='2025-11-01'}
dec={r['consumer_id']:r for r in rows if r['analysis_month']=='2025-12-01'}
ids=sorted(nov.keys()&dec.keys());deltas=[];fc=[];ticket=[];income=[];pressure=[]
for k in ids:
 a,z=nov[k],dec[k]
 deltas.append(float(z['financial_health_score'])-float(a['financial_health_score']))
 f=float(z['transaction_count'])/float(a['transaction_count']);t=(float(z['total_spend_vnd'])/float(z['transaction_count']))/(float(a['total_spend_vnd'])/float(a['transaction_count']));i=float(z['monthly_income_vnd'])/float(a['monthly_income_vnd'])
 fc.append(math.log(f));ticket.append(math.log(t));income.append(math.log(i));pressure.append(math.log((float(z['total_spend_vnd'])/float(z['monthly_income_vnd']))/(float(a['total_spend_vnd'])/float(a['monthly_income_vnd']))))
verify('909 matched customer IDs',len(ids)==s['paired_customers']==909)
verify('Paired mean and median change',close(statistics.mean(deltas),s['paired_mean_change']) and close(statistics.median(deltas),s['paired_median_change']))
verify('Geometric frequency multiplier',close(math.exp(statistics.mean(fc)),s['paired_count_gmean_ratio']))
verify('Geometric ticket multiplier',close(math.exp(statistics.mean(ticket)),s['paired_ticket_gmean_ratio']))
verify('Geometric income multiplier',close(math.exp(statistics.mean(income)),s['paired_income_gmean_ratio']))
verify('Exact multiplicative decomposition',close(statistics.mean(pressure),statistics.mean(fc)+statistics.mean(ticket)-statistics.mean(income)))
strict=[r for r in rows if float(r['financial_health_score'])<40 and float(r['engagement_score'])>=80]
verify('Strict annual 52 observations /45 customers',len(strict)==52 and len({r['consumer_id'] for r in strict})==45)
verify('Strict December 8 customers',sum(float(r['financial_health_score'])<40 and float(r['engagement_score'])>=80 for r in dec.values())==8)
verify('Strict observations all spend above income',all(float(r['spend_to_income_ratio'])>1 for r in strict))
newlow=sum(float(nov[k]['financial_health_score'])>=60 and float(dec[k]['financial_health_score'])<60 for k in ids)
verify('642 newly below 60',newlow==642)
counts=[0,0,0,0]
for r in dec.values():
 h=float(r['financial_health_score']);i=float(r['spend_to_income_ratio'])
 tier=0 if h<40 else (1 if h<60 and i>1 else (2 if h<60 else 3));counts[tier]+=1
verify('December tiers 25/656/91/146',counts==[25,656,91,146] and sum(counts)==918)
verify('No core source quality failures',all(c['pass'] for c in json.loads((P.parent/'task2/audit.json').read_text())['checks']))
verify('No extended quality failures',s['checks_passed']==s['checks_total']==15)
out={'implementation':'Python csv, math, statistics; does not import pandas or numpy','checks':results,'passed':sum(results.values()),'total':len(results)}
(P/'independent_verification.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2));assert all(results.values()),results
