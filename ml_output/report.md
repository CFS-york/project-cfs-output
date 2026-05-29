# CFS ML Report (v2 trusted only)

*生成: 2026-05-27 16:09:45.873859*

## 学習概要
- trusted trial数: 31,340 (unique cell)
- 学習 sample: 30,946
- 特徴量数: 37

## mult 分布
- mult max: 2.887x
- mult mean: 0.560x
- mult median: 0.496x
- mult >= 10x: 0 (0.00%)
- mult >= 7x: 0 (0.00%)
- mult >= 5x: 0 (0.00%)
- mult >= 4.31x: 0 (0.00%)
- mult >= 3x: 0 (0.00%)
- mult >= 2x: 196 (0.63%)
- mult >= 1.5x: 1,816 (5.87%)
- mult >= 1.0x: 4,639 (14.99%)

## 特徴量重要度 (gain) TOP 20
| feature | importance |
|---|---|
| gap | 23129 |
| universe | 20813 |
| vol | 12381 |
| p1_dn | 2855 |
| ext | 2556 |
| mp | 1268 |
| p1_up | 1220 |
| sel | 1184 |
| trig | 868 |
| price_pos | 522 |
| og_min | 303 |
| entry_off | 250 |
| phase_struct | 145 |
| tp | 68 |
| sl | 64 |
| hold | 62 |
| vol_thr | 41 |
| max_hold | 22 |
| ret5_thr | 12 |

## TOP 10 cells (実 data 上)
| mult | n | wr | ev | sources |
|---|---|---|---|---|
| 2.887x | 110 | 0.528 | 4.11% | phase_v3_high20_vs_no_direct |
| 2.799x | 110 | 0.532 | 3.94% | phase_v3_high20_vs_no_direct |
| 2.635x | 109 | 0.514 | 3.93% | phase_v3_high20_vs_no_direct |
| 2.628x | 110 | 0.558 | 4.08% | phase_v3_high20_vs_no_direct |
| 2.551x | 109 | 0.518 | 3.76% | phase_v3_high20_vs_no_direct |
| 2.538x | 113 | 0.522 | 3.52% | phase_v3_open_gap_lower_filter |
| 2.527x | 108 | 0.524 | 3.88% | phase_v3_high20_vs_no_direct |
| 2.525x | 109 | 0.559 | 3.91% | phase_v3_high20_vs_no_direct |
| 2.519x | 102 | 0.518 | 3.81% | phase_v3_open_gap_lower_filter |
| 2.506x | 101 | 0.521 | 3.79% | phase_v3_open_gap_lower_filter |

## Sweet Spot (mult >= 3x) 軸別分布

## 未試行 高期待 TOP 10 (予測)
| 予測 mult | キー params |
|---|---|
| 2.051x | gap=0.07 universe=8.00 vol=-1.00 p1_dn=-0.04 ext=4.00 |
| 2.011x | gap=0.06 universe=14.00 vol=-1.00 p1_dn=-0.03 ext=4.00 |
| 1.800x | gap=0.07 universe=8.00 vol=-1.00 p1_dn=-0.02 ext=4.00 |
| 1.771x | gap=0.06 universe=8.00 vol=-1.00 p1_dn=-0.07 ext=4.00 |
| 1.764x | gap=0.06 universe=21.00 vol=-1.00 p1_dn=-0.05 ext=3.00 |
| 1.751x | gap=0.06 universe=8.00 vol=-1.00 p1_dn=-0.08 ext=4.00 |
| 1.741x | gap=0.05 universe=22.00 vol=-1.00 p1_dn=-0.03 ext=4.00 |
| 1.736x | gap=0.07 universe=21.00 vol=-1.00 p1_dn=-0.04 ext=4.00 |
| 1.725x | gap=0.05 universe=22.00 vol=-1.00 p1_dn=-0.04 ext=4.00 |
| 1.710x | gap=0.08 universe=21.00 vol=-1.00 p1_dn=-0.05 ext=3.00 |

## look-ahead bias 除外 source
- block_lookahead_analysis
- block_lookahead_clean
- candidate_A_extend_tp
- fantasy_target_ev_picker
- param_grid_fine_stage1
- param_grid_fine_stage1_ext
- param_grid_fine_stage2

*理由: 物理整合 検証で 再現せず、 もしくは 集計バグ含み*

## ARK セッション 引継ぎ用 サマリ

本 report は ARK が **次セッション 起動時に最初に読む** ことを 想定。
- 過去 trial の **真の edge cell** が data 上 何か
- 未試行 zone で **検証 価値の高い** 候補
- 重要 軸 (importance gain TOP) の どこに edge が 集中するか