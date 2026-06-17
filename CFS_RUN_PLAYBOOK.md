# CFS 検証実行プレイブック (新ARKが検証を実行する前に必読 / 散在情報の集約)

最終更新: 2026-06-17
目的: 「新しい検証をどう書き・どう実行し・何をもって成功とするか」を一箇所に集約。これが無いと各ARKが毎回探す/質問する(2026-06-17 GPT引き継ぎ練習で欠落が露呈)。

---

## 1. 検証フローの登場人物 (CFS_MANUAL §8.2b)

- **ARK** (Claude/GPTの1チャット): 仮説立案 + 検証scriptを書く。**自分では実行しない**
- **ヨーク**: ARKが渡したscriptをPCで実行し、結果(標準出力+CSV)をARKに貼る。データ・ファイルは直接編集しない
- **BREAKER**: 別チャットの独立盲検。確定候補(主張+根拠+想定弱点)をストレスし、突破して初めて「確定」昇格
- ★ CLUTCH / LONG は廃止(過去概念、現役でない)

## 2. 検証の実行フロー (ARK→ヨーク→フィードバック)

```
1. ARK: 仮説を(A)〜(E)で立てる(CFS_MAPの仮説の定義に従う)
2. ARK: 検証scriptを書く(下記§3の骨格を流用)→ ヨークにpresent
3. ヨーク: cd C:\mnt\data; python run.py scripts\cfsXXX.py で実行(自動git push)
4. ヨーク: 標準出力 + Results CSV をARKに貼る
5. ARK: 結果を読み、仮説の生死を(E)生死条件で判定 → CFS_MAP/FAILURE_LOG更新(全文)
```

- 実行コマンドは必ず `cd C:\mnt\data;` 始まりの1行(F-051)
- 新chat開始時のみ `cd C:\mnt\data; python run.py newchat`(state reset)
- [ARK_ROTATE]が出たら HANDOVER全文更新→新chat→newchat

## 3. ★検証scriptの骨格 (自作sim禁止・確定土台流用)

**絶対ルール: 自作・簡略simは破綻する。** 確定sim骨格を流用せよ:
- 一般検証: `scripts/cfs_common.py` の `load_base(DATA,CACHE,CLEAN)` + `sim_equal_weight(...)` を import
- P1再現/P1系: `scripts/cfs77_p1_true.py` の sim関数を**完全流用**(gcl事前計算 + net_mult決済返却 + take=sig_by_day[t][:free])
- 過適合監査(近傍スイープ): `scripts/cfs41_p1_stability.py`

**自作simの破綻実例(二度とやるな)**:
- cfs210: 点灯全体を見てP1非再現(中央マイナス)
- cfs211: cash返却を簡略化しcash枯れ、約定20で停止
- cfs73-76: alloc=cash/n(候補数で割る)で9.86x(確定3.09xの3倍)= per=cash/free が正
- cfs11/18/28: idxバグ/accept緩め/entry基準ズレ
- → 新規simは確定骨格流用 + assert強制で整合確認必須

**必須ヘッダ(run.pyのM1/M3が機械照合)**:
```python
# ARK_BLOCK: CFS188
# ARK_SESSION_CHECK: 公式現在地 P1=3.09x ... (newchat直後の初scriptのみ)
# ARK_FAILURELOG_DIFF: (棄却軸に触れる場合、過去との差分宣言)
# ARK_REPLAY_DIFF: (過去cfsとの差分宣言、再発明防止)
ARK_PREFLIGHT = {"mode":..., "purpose":..., "drift_check":...}
ARK_PROBE_ANS = {"Q1":"P1 3.09x ...", "Q2":"道B=CFS188 ..."}
```

## 4. データ・成果物の配置 (DATA_MAP)

- 原資: `C:\mnt\data\Results\ARK\cfs5\cfs148_dataset\dataset.parquet`(450万行、netfix/godseye_net40/top1/各_pct)
- 価格cache: `C:\mnt\data\cache\adjc/adjo/adjh/adjl/vol_cache_54m.csv`(★code4=str、'132A'等英字。int読込はエラー)
- 信用: margin_cache.csv / 空売り: shortsale_cache.csv(short_to_so)
- 確定sim: `scripts/cfs_common.py`
- 検証結果出力先: `C:\mnt\data\Results\ARK\cfs5\<検証名>\*.csv`
- ★成果物(CSV)はローカル/private。public mirrorには非同期(.md要約のみ)。ARKは直接読めず、ヨークが貼る

## 5. 物理定数 (全検証共通)

```
COST=0.005  TAX=0.20315  BASE_SPREAD=0.0005  INIT=1,000,000
P1: HOLD=40, K=20  /  確定sim標準: K30 hold13 MIN_PER=20000 DAILY_MAX=5
days_16m=327(16ヶ月の営業日)
```

## 6. P1再現の合格判定基準 (検証結果監査の例)

| 項目 | 期待値 | 許容誤差 |
|---|---|---|
| 全期間mult | 3.09x | ±5%(cfs77実測3.084x) |
| trade数 n | 389 | ±10%(cfs77=388, cfs212=390) |
| MDD | 約14% | ±5pt |
| 16ヶ月換算 | 1.35x | (3.09xは5年値。混同禁止) |

判定: mult/n/MDDが許容内 → P1再現成功。逸脱 → sim骨格の誤再現を疑う(§3)

## 7. 10x方程式 (仮説の(A)で必須)

```
(1+r)^N = 10、 N = 327/hold
P1実績: hold40 r=14.80% N=8.18 → 3.09x
10x必要r: hold20でr≥15.13% / hold13でr≥9.65% / hold10でr≥7.27%
```
仮説は必ずこの式でr・Nを置き、ARKが自分で検算。rを逆算して10xに見せるのは循環論法=禁止。

## 8. out-of-sample / 頑健性の確認 (過適合監査)

- 期間分割: train(2021-2023) / test(2024-2026)で両期間成立するか
- 近傍スイープ: パラメータをずらして「滑らかな丘」か(cfs41方式)。特定セルだけ突出→過適合
- 縮約環境の偽濃縮(§5.16): 流動性上位N銘柄で導いた法則は本番全体で消える/逆転。必ず本番datasetで確認
