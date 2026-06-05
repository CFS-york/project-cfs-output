# P1_DEFINITION — 確定edge P1 の完全定義（再現用・圧縮対象外）

> **このファイルはHANDOVER圧縮の対象外。確定edgeの定義は結果値だけでなく生成定義式・sim骨格・元スクリプトをセットで永続記録する。**
> 作成: 2026-06-05 / 再現確認: cfs77_p1_true.py で 3.084x・n388（確定値3.09x・389と誤差0%）

---

## 1. P1とは
Project CFS唯一のBREAKER確定edge（#001-2確定）。低位×高ボラ×gap中庸の分散ポートフォリオ。
- **確定値: 全期間 3.09x（16ヶ月換算 1.35x）、MDD約14%、エントリ n=389**
- 過適合でない（cfs41で近傍スイープ＝price/vola/gapずらしで頑健性確認、地合い非依存）

## 2. 母集団定義（t時点特徴、look-ahead禁止）
universe = listed>=60 & 100<=price<=50000 & blacklist除外 & KNOWN_ETF除外
の上で、各営業日tにおいて以下を全て満たす銘柄がP1候補:

```
C[t]      <= px20      # price が 20%ile 以下（低位）
vola20[t]  > vo90       # 20日ボラ（日次リターンの20日std）が 90%ile 超（高ボラ）
gap[t]     > g40        # gap = (O[t]-C[t-1])/C[t-1] が 40%ile 超
gap[t]    <= g60        # かつ 60%ile 以下（gap中庸）
```
分位は valid全体から算出:
- px20 = nanquantile(C[valid], 0.20)
- vo90 = nanquantile(vola20[valid], 0.90)
- g40  = nanquantile(gap[valid], 0.40),  g60 = nanquantile(gap[valid], 0.60)

（参考実測値 2021-04〜2026-04: px20≈572, vo90≈0.0358, g40≈0.0000, g60≈0.0015）

## 3. エントリ・エグジット
- エントリ: t判断 → **e=t+1 の Open（AdjO）で買い**
- エグジット: **end = min(e+HOLD, T-1) の Close（AdjC）で売り**
- HOLD = 40, K = 20

## 4. ★sim骨格（複利定義）── ここが最重要・誤再現の温床
**配分は per = cash / free（free = K - 現在保有数 = その日の空き枠全部で割る）。**
**候補数では割らない。** これにより常にK=20分散で薄く張る。候補が少ない日は資金を使い切らず現金で待機。

```python
def sim(mask, K=20, HOLD=40):
    sig_by_day = {}                       # 各日のP1候補（発生順=元データ順、神の目でない）
    ti, ci = np.where(mask)
    for t, c in zip(ti, ci): sig_by_day.setdefault(t, []).append(c)
    cash = INIT; holding = []; n = 0
    for t in range(T):
        # 決済: exit_day == t のものを net_mult で精算
        still = []
        for (xt, inv, gr) in holding:
            if xt == t: cash += inv * net_mult(gr)
            else: still.append((xt, inv, gr))
        holding = still
        free = K - len(holding)
        if free > 0 and t in sig_by_day and cash > 0:
            take = sig_by_day[t][:free]    # 発生順に空き枠まで
            per  = cash / free             # ★空き枠free（=K-保有）で割る。候補数でなく！
            for c in take:
                gr = gcl[t, c]
                if np.isnan(gr): continue
                cash -= per
                holding.append((t+1+HOLD, per, gr)); n += 1
    for (xt, inv, gr) in holding: cash += inv * net_mult(gr)
    return cash/INIT

def net_mult(g):                            # コスト・税引き後（損益クリップなし）
    nt = g - COST - BASE_SPREAD             # COST=0.005, BASE_SPREAD=0.0005
    return 1.0 + (nt*(1-TAX) if nt>0 else nt)   # TAX=0.20315（利益にのみ課税）
```

## 5. 選択ロジック
**発生順（sig_by_day[t] を元データ順にそのまま）。forward net上位で選ぶ「神の目」ではない。**
P1母集団は1日数銘柄しか出ないため、free枠(20)に対し候補がほぼ常に少なく、実質「その日のP1候補を全部買う」動作になる。

## 6. 誤再現の記録（2026-06-05、cfs73-77）
- 誤: `n=min(signal_count, open_slots, capital/MIN_PER); alloc=capital/n`（候補数で割る＝候補少の日に集中投資）→ P1で9.86x/n32（確定値の3倍）
- 正: `per=cash/free`（空き枠Kで割る＝常にK分散）→ P1で3.084x/n388 ✓
- この誤再現が cfs64-76 のシミュレータ全体のバグだった。

## 7. 元スクリプト
- 定義・命名: scripts/cfs38_p1_deepdive.py（P1=2.19xで発見）
- 確定: scripts/cfs41_p1_stability.py（近傍頑健性確認、sim骨格の正本）、scripts/cfs48_p1_tail_cut.py
- 再現確認: scripts/cfs77_p1_true.py（2026-06-05、3.084x/n388）
