#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ===== AUDITOR実行ガイド(今日の失敗を繰り返さないため) =====
# 実行エントリは sim()。run/verify/simulate/main は無い。
# 使い方: base,m,s=load() -> sim(base,m,s, YOUR_signal_fn, exit_fn, start_idx, K)
#   signal_fn(t,O,C,V,MR,SS,N)->買いindexのlist  (O..SSは2D日×銘柄, V=売買代金)
#   exit_fn = lambda t: t+1+HOLD   (hold20なら t+1+20)
#   返り値7つ: mult,Nt,p,w,l,mv,Nm (倍率,N,勝率,平均勝,平均負,m,Nxm)
# signal_fnを差し替えた実行版を cfs2/scripts/(使い捨て)に置いて実行。
# ==========================================================
"""
cfs2 検証sim (AUDITOR提出版) — (N,p,w,l)内訳を出す。
CFS2_GOALの式で判定: N×m≥2.303 (m=p·ln(1+w)+(1-p)·ln(1+l))。
LOGIC_01の3世界(D-01/02/03 二重需給)を実データで測る。
出力: 最終倍率 + 内訳(N,勝率p,平均勝ちw,平均負けl,実測m,N×m)。
→ロジックの予測(p,w,l)と実測を照合できる。
"""
import numpy as np, pandas as pd
U=r"C:\mnt\data\cache"
COST,TAX=0.005,0.20315; INIT=300000; MIN_VA=5e7; MONTHS16=344

def load():
    o=pd.read_csv(f"{U}/adjo_cache_54m.csv",low_memory=False)
    c=pd.read_csv(f"{U}/adjc_cache_54m.csv",low_memory=False)
    v=pd.read_csv(f"{U}/vol_cache_54m.csv",low_memory=False)
    m=pd.read_csv(f"{U}/margin_cache.csv",low_memory=False)
    s=pd.read_csv(f"{U}/shortsale_cache.csv",low_memory=False)
    for df in (o,c,v,m,s): df.columns=[x.strip().lstrip("\ufeff") for x in df.columns]
    o=o.rename(columns={"AdjO":"o"});c=c.rename(columns={"AdjC":"c"});v=v.rename(columns={"Va":"va"})
    base=o.merge(c,on=["date","code4"]).merge(v,on=["date","code4"])
    base["date"]=pd.to_datetime(base["date"]); m["date"]=pd.to_datetime(m["date"]); s["date"]=pd.to_datetime(s["date"])
    m["ratio"]=m["long_vol"]/m["shrt_vol"].replace(0,np.nan)
    base=base.sort_values(["date","code4"]).reset_index(drop=True)
    return base,m,s

def piv(df,dates,codes,col):
    return df.pivot_table(index="date",columns="code4",values=col).reindex(index=dates,columns=codes).values

def sim(base,m,s,signal_fn,exit_fn,start_idx,K):
    """(N,p,w,l)内訳も返す。exit_fn(entry_px,path)->売却pxとtrade純リターン"""
    dates=np.sort(base["date"].unique())[start_idx:start_idx+MONTHS16]
    codes=np.sort(base["code4"].unique())
    O=piv(base,dates,codes,"o");C=piv(base,dates,codes,"c");V=piv(base,dates,codes,"va")
    MR=pd.DataFrame(piv(m,dates,codes,"ratio")).ffill().values
    SS=pd.DataFrame(piv(s,dates,codes,"short_to_so")).ffill().values
    T,N=O.shape; cash=INIT; holds=[]; t=0; trades=[]
    while t<T-2:
        keep=[]
        for h in holds:
            entry_i,sh,ci,inv,epx,sell_t=h
            do_sell=False; px=None
            if t>=sell_t: do_sell=True; px=C[t,ci] if not np.isnan(C[t,ci]) else epx
            if do_sell:
                proceeds=sh*px;gross=proceeds-inv;ca=(inv+proceeds)*COST;net=gross-ca
                if net>0:net*=(1-TAX)
                cash+=inv+net
                trades.append(net/inv)  # 純リターン率
            else: keep.append(h)
        holds=keep; slots=K-len(holds)
        if slots>0 and cash>20000:
            picks=signal_fn(t,O,C,V,MR,SS,N)
            picks=[p for p in picks if V[t+1,p]>=MIN_VA and not np.isnan(O[t+1,p]) and O[t+1,p]>0][:slots]
            if picks:
                alloc=cash/K
                for p in picks:
                    inv=min(alloc,V[t+1,p]*0.05)
                    if inv<20000:continue
                    sh=inv/O[t+1,p];cash-=inv
                    sell_t=exit_fn(t)
                    holds.append((t+1,sh,p,inv,O[t+1,p],sell_t))
        t+=1
    final=cash+sum(h[1]*C[-1,h[2]] for h in holds if not np.isnan(C[-1,h[2]]))
    tr=np.array(trades)
    if len(tr)>0:
        wins=tr[tr>0]; losses=tr[tr<=0]
        p=len(wins)/len(tr); w=wins.mean() if len(wins)>0 else 0; l=losses.mean() if len(losses)>0 else 0
        mval=p*np.log(1+w)+(1-p)*np.log(1+l) if (1+w>0 and 1+l>0) else np.nan
        Nm=len(tr)*mval
    else: p=w=l=mval=Nm=0
    return final/INIT,len(tr),p,w,l,mval,Nm

def worlds():
    W={}
    # D-01 二重需給: 倍率≤0.5 かつ 空売り比上位20% 、20日固定
    def sig_dual(t,O,C,V,MR,SS,N):
        if np.all(np.isnan(SS[t])): 
            cond=(MR[t]<=0.5)&(~np.isnan(MR[t]))
        else:
            thr=np.nanpercentile(SS[t][~np.isnan(SS[t])],80) if np.any(~np.isnan(SS[t])) else 1e9
            cond=(MR[t]<=0.5)&(~np.isnan(MR[t]))&(SS[t]>=thr)
        return list(np.where(cond)[0])
    W["D01_二重需給20d"]=(sig_dual, lambda t:t+1+20, 5)
    # D-02 二重需給×トレイル近似(40日まで持つ=右裾を伸ばす代理)
    W["D02_二重需給40d"]=(sig_dual, lambda t:t+1+40, 5)
    # D-03 集中(K=1)×二重需給
    W["D03_集中二重K1_20d"]=(sig_dual, lambda t:t+1+20, 1)
    return W

if __name__=="__main__":
    print("[load]...");base,m,s=load()
    dates=np.sort(base["date"].unique()); starts=[0,len(dates)//3,2*len(dates)//3]
    W=worlds()
    print(f"\n{'='*78}")
    print("cfs2 検証sim — (N,p,w,l)内訳 [10x=N×m≥2.303]")
    print('='*78)
    for name,(sig,exit_fn,K) in W.items():
        print(f"\n【{name}】K={K}")
        print(f"  {'窓':<4}{'倍率':>7}{'N':>5}{'勝率p':>7}{'平均勝w':>9}{'平均負l':>9}{'m':>8}{'N×m':>7}")
        for wi,si in enumerate(starts,1):
            try:
                mult,Nt,p,w,l,mv,Nm=sim(base,m,s,sig,exit_fn,si,K)
                jd="★" if Nm>=2.303 else ""
                print(f"  {wi:<4}{mult:>6.2f}x{Nt:>5}{p:>7.2f}{w*100:>8.1f}%{l*100:>8.1f}%{mv:>8.3f}{Nm:>7.2f}{jd}")
            except Exception as e:
                print(f"  {wi:<4} err {str(e)[:40]}")
    print(f"\n{'='*78}")
    print("★N×m≥2.303で10x。p,w,lの実測がロジック予測(D-01:p0.4,w+60%,l-10%)と合うか。")
