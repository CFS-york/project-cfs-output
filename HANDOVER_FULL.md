# CFS HANDOVER FULL (全履歴版)

圧縮しない時系列蓄積。詳細はここを遡る。LATESTは圧縮active版。

---

## 2026-06-04T17:42:21.701902+00:00

### summary
1. HANDOVER_LATEST.md: cfs55-61の検証ログを直近5件形式に整理・圧縮。cfs53-54以前は要約行に統合。「次フェーズ方針」セクションを明確化し道Bシミュレータ・新情報軸・P1境界の3アクションを前面に。改訂履歴を直近10版に圧縮(v2.8以前を削除)。全体を約9KBに収めた。
2. FAILURE_LOG.md: §4に本日の棄却確定項目(cfs29-33の残余分/cfs37/cfs39-40/cfs42-44/cfs48-54/cfs55-56のoverclaim/cfs58-61の識別精度限界)を追記。§5.9「識別精度と母集団速度のトレードオフ」を新設。改訂履歴にv1.6を追加。既存項目は一切変更せず。
3. 矛盾解消: 「棄却確定」と「本物のedge」の整合を確認。P1 3.09xは確定edgeとして保持、P1いじり系は全棄却として明示。
4. 次セッションARKが「道Bシミュレータ設計」を最優先タスクとして即座に把握できる構造に整理。

### 当日検証結果 (today_results)
# 当日 検証結果 集約

対象期間: 過去 24 時間
検出 file: 18 件
検出 script: 15 件

## mult 統計 TOP (script 単位、 mult_max 降順)

| script | n | mult_max | mult_mean | mult_p90 |
|---|---|---|---|---|
| cfs55_ideal_ceiling | 12 | 42796353126.345 | 3655063213.604 | 930273994.001 |
| cfs56_breaker002_remand | 15 | 346.050 | 44.786 | 107.443 |
| cfs60_wide_kelly_map | 40 | 267.540 | 55.499 | 243.171 |
| cfs49_mdd_budget | 36 | 5.103 | 3.131 | 4.546 |
| cfs48_p1_tail_cut | 5 | 3.090 | 2.433 | - |
| cfs51_orthogonal_edge | 6 | 3.090 | 1.321 | - |
| cfs54_financial_axis | 9 | 3.090 | 1.970 | - |
| cfs55_composite_axis | 13 | 3.090 | 1.110 | 1.969 |
| cfs57_capture_check | 1 | 3.090 | 3.090 | - |
| cfs58_kelly_precision_map | 30 | 2.130 | 1.602 | 2.067 |
| cfs59_practical_identification | 13 | 1.401 | 0.650 | 1.223 |
| cfs53_lgbm_netreg | 4 | 1.285 | 1.208 | - |
| cfs46_loss_avoid_pastbig | 12 | 1.167 | 0.705 | 0.984 |
| cfs61_wide_ml_real | 5 | 1.160 | 0.762 | - |
| cfs52_lgbm_winset | 4 | 1.152 | 0.886 | - |


---
