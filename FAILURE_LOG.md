# CFS 失敗ログ

過去 ARK / ヨーク が **試して 失敗 した もの**。 次 ARK が 同じ轍 踏まない ため。

「これ 試したい」 と思ったら、 まず この log で 検索。 該当あれば 棄却 or 本質的に異なる軸 で 再構築。

---

## 1. 旧体制 (正当価格 v4/v5、 block220-333、 〜2026-05-26)

### 1.1 戦略空間 v4/v5 探索 (約 280 万試行)

**仮説**: signal × ranking × filter 組合せ で robust 10x

**手法**:
- v4: 25 signal × 11 ranking × 11 filter、 Optuna 3,000 試行
- v4+IPO: listed≥5 条件追加、 Optuna 3,000 試行
- v5: + 5 集合歪み signal、 Optuna 3,000 試行

**結果**:
- v4 worst: **1.623x**
- v4+IPO worst: **1.719x**
- v5 worst: **1.530x**

**棄却理由**: ARK 探索範囲 (signal/ranking/filter 組合せ) の **上限 ≈ 1.7x** を data 上 確定。 280 万試行 で 10x cell ゼロ。 **ARK 想像範囲外** への 飛躍 が必要。

**教訓**: 既存 軸 の 周辺探索 では どんなに 試行数 増やしても 突破不可。 軸そのもの を 変える必要。

### 1.2 正当価格 定義 (block254-296)

**仮説**: 「実力 × 市場心理」 の 掛け合わせ で 正当価格 算出 → 割安 銘柄 を 買えば edge

**最終 確定式 (block296)**:
```
正当価格(i,t) = sqrt(正常化eps(i,t) × bvps(i,t)) × Qe(i,t)
              × sqrt(市場PER中央(t) × 市場PBR中央(t))
```

**結果**: 定義 は 確定 した。 ただし 運用 (割安 で 買う) で 10x には 届かず (v4/v5 探索 で 1.7x 天井)。

**棄却理由**: 「正当価格 定義」 と 「運用で勝つ」 は 別段階。 定義 確定しても 運用設計 で edge 出ず。

**教訓**: 「定義 を 直す」 と 「運用 を 直す」 を 混同しない。 定義 確定後、 運用 で 勝てない 場合 → 軸変更 (本セッション の gap trigger 移行)。

### 1.3 「掛け合わせ」 を 和形式 で実装 (block254-292)

**ARK 誤実装**: `w·earn + (1-w)·asset·Q` (和形式)

**結果**: 和の片方の項 が 支配的 → 単純式 と 区別不能 (Spearman 0.9848)

**棄却理由**: 「掛け合わせ」 は **積** であるべき。 和では 順位 に効かない。

**教訓**: 「掛け合わせ」 の 文字通り の意味 = 積。 和で 近似 するな。

### 1.4 質係数 Qe を 乗数 で実装

**ARK 誤実装**: Qe を 0.8〜1.2 の乗数 として 価格 に掛ける

**結果**: 順位 選別 に効かない (F0 vs F5 Spearman 0.9989)

**棄却理由**: Qe は **加算項** (0〜1 範囲) で 相乗平均 に掛けるべき。

**教訓**: 質補正 は 順位 に効く 範囲設計 が必須。

---

## 2. 新体制 (gap trigger、 phase_v3/v4、 2026-05-27〜28)

### 2.1 H-alpha 系 (2026-05-23)

**仮説**: H-alpha (財務系 signal の派生) で edge

**結果**: 全 path 失敗、 棄却

**教訓**: 旧体制 由来 の signal 派生 は 軸変更 にならない、 周辺探索 と同じ

### 2.2 fantasy 系 (2026-05-25)

**仮説**: fantasy_winrate_grid 等 で 高 mult zone 発見

**結果**: 軒並み 棄却 (look-ahead bias 含む source あり)

**教訓**: 大量 grid で 出た 高 mult cell は look-ahead bias 疑え

### 2.3 tp/sl logic、 sl=-1% 固定 (2026-05-27、 phase_v4)

**仮説 (ML report 由来)**: ret5≥10% × tp=20% × sl=-1% × hold=1 で mult **7.43x、 n=388、 wr 38%**

**ARK 物理整合 検証 (phase_v4_tp_sl_logic.py、 1,152 grid)**:
- 自前 cache (AdjH/AdjL) で 場中 sl/tp タッチ判定
- ギャップ open で sl 超え = open 約定 (現実 logic)

**結果**: mult **0.40x**、 wr **9.8%**、 EV **-0.08%**、 sl_n **76%**

**棄却理由 (data 上 確定)**: param_grid_fine_stage1_ext の sl logic は **物理機能しない**。 sl=-1% は 場中 タッチで 即約定、 76% が sl 損失確定。 期待 mult 7.43x は **look-ahead bias** または 非現実 sl 計算 由来。

**教訓**:
- 過去 trial の「高 mult cell」 を 鵜呑み に しない、 物理検証 必須
- sl タイト (-1% 等) は 統計的 に sl 連発 で 損失累積
- tp 大 (+20%、 +100%) は 達成率 低い

### 2.4 ret5 trigger 系 (2026-05-27)

**仮説**: ret5≥10% momentum で edge

**結果**: 物理整合検証 で TOP mult 1.07x、 期待 7.43x の 1/7 以下

**棄却理由**: 物理 logic で 機能しない zone

### 2.5 trail / stop loss 構造問題

**仮説**: trail stop で 急落 防止

**結果**: optuna_dynamic_hold で worst 22.035x → look-ahead bug 修正後 **0.099x** (220 分の 1)

**棄却理由**:
- trail 判定 当日 close、 売却 翌日 open = look-ahead
- 翌日 open gap down 直撃 で 実損 -8〜-9%
- CFS 哲学 (集合的恐怖を買う) と矛盾

**教訓**: stop loss / trail は 現実 では ギャップ で 想定以上 損失。 CFS 哲学 と 矛盾。

### 2.6 ARK base cell 4.31x → 真値 2.887x

**ARK 認識**: base cell `gap=0.065 × ext=4 × universe=4000-7000 × HIGH20` で mult 4.31x、 「探索枠 上限」 と確定

**ML system 解析 (本セッション)**:
- 同 cell を 4 回 検証で 集約 → 平均 **mult 2.887x、 std 1.65、 min 1.40、 max 4.31**
- = 4.31x は **1 検証 の 上振れ**、 真の robust 値 は 2.887x

**教訓**: 単一検証 の mult は ばらつく。 同 cell 複数回 検証 で **真値** を出す。 LightGBM 集約 が この役割。

---

## 3. look-ahead bias 確定 source (本セッション 確定)

学習対象外 として ingest で trusted=False マーク:

| source | 棄却理由 |
|---|---|
| block_lookahead_clean | mult 9000x 等 の異常値、 look-ahead 検出用 file |
| block_lookahead_analysis | 同上 |
| param_grid_fine_stage1 | sl logic 物理整合せず |
| param_grid_fine_stage1_ext | mult 7.43x cell が物理検証 で 0.40x |
| param_grid_fine_stage2 | 同上 |
| candidate_A_extend_tp | tp=1.0、 sl=-0.01 cell の look-ahead 疑い |
| fantasy_target_ev_picker | n=1976 で wr=0% の 集計バグ |

---

## 4. ARK 棄却済 軸 (二度と 戻らない)

これら を ARK が 「新仮説」 として 出したら ヨーク は 即 ストップ:

- 正当価格 (財務 ベース) を 軸 に した 戦略
- H-alpha 系
- fantasy 系
- tp/sl logic (sl タイト 固定)
- ret5 trigger + tp/sl
- trail stop (look-ahead リスク)
- 大化け予測 (CFS 哲学 逸脱)
- monte carlo / random / Optuna 大量試行 (F-036 違反、 構造的歪み 捕捉と矛盾)

---

## 5. 構造的 学び (普遍)

### 5.1 ARK 想像範囲 の限界
過去 5 セッション + 旧体制、 ARK 想像 で 出した 軸 の上限 = **1.7x (旧)、 4.31x (新)**。 突破 には ARK 想像範囲外 への 飛躍 が必須。

### 5.2 大量試行 の罠
random / Optuna / ML 大量探索 で 出た 「高 mult cell」 = 高確率 で look-ahead bias or curve fit。 物理整合 検証 必須。

### 5.3 単一検証 の ばらつき
同 cell でも 検証回 で mult 大きく振れる (4.31x ⇔ 2.887x、 std 1.65)。 単一値で 判断しない、 複数回 検証 + 集約 で 真値。

### 5.4 物理 logic 違反 の見落とし
backtest 上 で 機能する logic が 実取引 で 機能しない パターン 多数 (trail、 sl タイト、 場中タッチ判定 等)。 物理整合 check が必須。

### 5.5 「定義」 と 「運用」 の混同
旧体制 で ARK が 何度も 繰り返した 失敗。 運用結果 悪い時 に 定義 を 直すのは F-023 反復確定。

---

## 改訂履歴

- 2026-05-28 v1.0 初版 (旧体制 1.7x 天井 + 新体制 4.31x 上限 + look-ahead 7 source を 失敗サマリ に圧縮)
