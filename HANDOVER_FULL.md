# CFS HANDOVER FULL (全履歴版)

圧縮しない時系列蓄積。詳細はここを遡る。LATESTは圧縮active版。

---

## 2026-06-03T05:01:36.152095+00:00

### summary
1. **HANDOVER v2.7へ更新**: 当日検証結果(ML統計再確認)を統合。mult統計はscriptレベルで外挿値のみ確認され、真値=1.141xに変更なし。新規棄却軸なし。
2. **改訂履歴を圧縮**: 10版上限ルールに従い最古(v1.7)を削除し、v1.8〜v2.7の10版に整理。
3. **FAILURE_LOG v1.5へ更新**: 当日検証で新規棄却確定項目はゼロ。追記専用ルール遵守のため既存項目は一切変更せず、改訂履歴のみ追記。
4. **次アクション確認**: cfs29(業種内相対強弱)が最重要タスクとして変わらず確定。cfs28教訓(複利simで最終判定)を即適用する旨を維持。
5. **構造維持**: セクション構成・heading・検証ログ直近5件・過去要約・ML数値・環境情報・警告、全て前版と同一構造を保持。

### 当日検証結果 (today_results)
# 当日 検証結果 集約

対象期間: 過去 24 時間
検出 file: 17 件
検出 script: 9 件

## mult 統計 TOP (script 単位、 mult_max 降順)

| script | n | mult_max | mult_mean | mult_p90 |
|---|---|---|---|---|
| cfs10_high20_h4e_filter | 180 | 4.311 | 1.341 | 2.171 |
| cfs11_true_compound_sim | 4 | 2.062 | 0.524 | - |
| cfs14_trailing_exit | 13 | 1.141 | 0.357 | 0.446 |
| cfs17_sequential_n_increase | 6 | 1.141 | 0.253 | - |
| cfs19_fractional_betting_fixed | 24 | 1.141 | 0.834 | 1.141 |
| cfs28_two_edge_combine | 6 | 1.141 | 0.286 | - |
| cfs12_compound_sl_optimize | 5 | 1.141 | 0.644 | - |
| cfs13_sim_reconcile | 5 | 1.141 | 0.644 | - |
| cfs18_fractional_betting | 24 | 0.962 | 0.614 | 0.855 |


---
