# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-05-29
更新方法: cron 23:59 (Claude API 自動整理) + watcher 即時 push (PC ⇔ GitHub 同期)

---

## 1. 現在地 (data 上)

### 探索 状況
- 探索手法: **gap × ext × high20** trigger (新体制、 phase_v3/v4 系)
- 累積 trial: 約 1,058 万 (旧+新)
- 学習対象 (trusted、 物理整合済): **31,340 cells**
- mult max (真値、 4 回集約平均): **2.887x**
  - cell: gap=0.065、 ext=4、 universe=4000-7000、 HIGH20
- mult max (単発検証): 4.31x (1 検証 の上振れ、 真値ではない)
- **絶対条件 達成率: 28.87% (10x まで 約 3.46 倍 不足)**

### 重要 軸 (LightGBM importance gain TOP)
1. gap (23,129)
2. universe (20,813)
3. vol (12,381)
4. p1_dn (2,855)
5. ext (2,556)

= **gap と universe が edge core**

### システム 状況 (2026-05-29 完成)
- **Phase 1 自動引継ぎ system: 完全稼働**
- watcher: PC バックグラウンド 動作中 (タスクスケジューラ 自動起動)
- cron: 毎日 23:59 GitHub Actions 自動実行
- Claude API: HANDOVER 自動整理、 物理整合 check 自動
- mirror: public repo (CFS-york/project-cfs-output) で ARK 取得用

---

## 2. 確定事実 (data 上、 反論なし)

- ARK 探索枠内 (gap × ext × universe × p1_up × p1_dn × HIGH20) の **上限 ≈ 2.887x**
  - 10 盲点 9 検証で確認済
- 既存軸 周辺探索 では 突破不可、 **軸変更 が必要**
- look-ahead bias source 7 件確定 (FAILURE_LOG §3 参照)
- trail / stop loss / sl タイト固定 は 物理機能 しない
- 旧体制 (正当価格 v4/v5) は 1.7x 天井 で 棄却済
- Phase 1 自動引継ぎ system は data 上 動作確認済 (本セッション 5/29)

---

## 3. 次アクション (優先順)

### 優先 1: 既存軸 から **飛躍** した 新軸 発見
- 既存 軸 (gap、 ext、 universe、 p1_up/dn、 vol、 ranking、 filter) は **全て 検証済**
- ARK_DISCIPLINE 原則 2 「既存概念から飛躍」 を発動、 月 1 回 ゼロベース仮説必須
- 過去 trial と **異なる 軸** を含む新仮説

### 優先 2: 期間 segmentation (盲点 7、 唯一 未検証)
- ARK base cell の **時期依存性** 検証 (前半 / 後半 で mult 変動)
- ただし overfitting リスクあり、 慎重に

### 優先 3: 物理整合 check 活用
- 仮説 → script → push → physics_check workflow が自動 走る
- look-ahead 事前検出 (本セッション の 7.43x→0.40x のような 失敗 を 事前防止)

---

## 4. 棄却済 (FAILURE_LOG.md 参照、 二度と 戻らない)

- 正当価格 v4/v5 (1.7x 天井)
- H-alpha 系
- fantasy 系
- tp/sl logic (sl タイト固定)
- ret5 trigger 系 (look-ahead 確定)
- trail / stop loss
- 大量 random / Optuna 試行
- 大化け予測 (CFS 哲学 逸脱)

---

## 5. 検証ログ (時系列、 直近)

### 2026-05-23: H-alpha 系
失敗、 棄却

### 2026-05-25: fantasy 系
棄却。 旧体制 v4/v5 探索 → 1.7x 天井 確定

### 2026-05-26: 方針転換
旧体制 (正当価格) から 新体制 (gap trigger) へ ARK 移行

### 2026-05-27 第 1 部: ML report 発見
mult 7.43x cell (ret5≥10% × tp=20% × sl=-1% × hold=1) 期待

### 2026-05-27 第 2 部: phase_v4_tp_sl_logic 物理検証
mult 7.43x → **0.40x** (look-ahead 確定)、 棄却

### 2026-05-27 第 3 部: ML system v4 構築
- ingest v4 (1,058 万 → 31,340 trusted)
- learn v2 (LightGBM)
- query.py
- GitHub push 成功 (commit 1c03c77)

### 2026-05-28: 引継ぎ system 再設計
- ヨーク 提案 「絶対ルール 3 + ARK 規律 + 実践マニュアル」 採用
- 旧 11 file を 5 file に圧縮
- Phase 1 system 設計確定
- public mirror repo 作成、 API key 設定

### 2026-05-29: Phase 1 完成
- Phase A 5 file (CFS_RULES、 ARK_DISCIPLINE、 CFS_MANUAL、 FAILURE_LOG、 HANDOVER_LATEST) 配置
- Phase B 8 file (collect_today_results、 handover_runner、 physics_validator、 push_to_mirror、 ingest_v5_legacy_summary、 auto_handover.yml、 physics_check.yml、 SETUP_PHASE1.md) 配置
- auto_push_watcher.py PC 配置 + バックグラウンド起動
- タスクスケジューラ 自動起動 登録
- GitHub Actions cron 動作確認 (skip 制御 動作 OK)
- watcher 編集検知 + 自動 push 動作確認 (commit d723267)
- = **system 完全稼働、 ヨーク 「いついかなる場合でも継続」 達成**

---

## 6. 最新 ML 数値

### mult 分布 (trusted 31,340 cells)
- mult >= 10x: **0 件 (0.00%)**
- mult >= 5x: 0 件
- mult >= 3x: 0 件
- mult >= 2x: 196 件 (0.63%)
- mult >= 1.5x: 1,816 件 (5.87%)
- mult >= 1.0x: 4,639 件 (14.99%)

### TOP 10 cells (実 data 上)
1. **mult 2.887x**: gap=0.065、 p1_up=0.02、 p1_dn=-0.06、 ext=4、 universe=4000-7000、 HIGH20、 n=110、 wr 0.528、 EV 4.11% (phase_v3_high20_vs_no_direct)
2. mult 2.799x: 同 cell の p1_dn=-0.07 変種
3. mult 2.635x: 同 cell の p1_up=0.025 変種
4. mult 2.628x: 同 cell の p1_up=0.01 変種
5. mult 2.551x: 同 cell の p1_up=0.025、 p1_dn=-0.07 変種
6. mult 2.538x: 同 cell の B_logic=none 変種
7-10: 同 base zone 周辺 (gap=0.065 × ext=4 × universe=4000-7000)

= **edge は 1 点 ではなく zone** として 存在 (robust 性質)

---

## 7. 環境情報

### Python
- パス: `C:\Users\Okazaki\AppData\Local\Microsoft\WindowsApps\python.exe` (Store 版)
- 実体: `pythonw3.13` プロセス名
- 作業: `C:\mnt\data\`
- 実行: `cd C:\mnt\data; python run.py scripts\xxx.py`

### GitHub
- private: https://github.com/CFS-york/project-cfs
- public mirror: https://github.com/CFS-york/project-cfs-output
- 自動 push: run.py + watcher
- Actions: auto_handover (cron 23:59 JST)、 physics_check (push trigger)

### J-Quants API V2
- URL: https://api.jquants.com/v2
- Light plan: 60 req/min、 sleep 1.2s

### cache (削除禁止)
`C:\mnt\data\cache\`
- adjc/adjo/adjh/adjl/vol_cache_54m.csv
- financial_cache/、 sector_master/、 listed_info_cache/ 等

### 物理コスト
- COST = 0.005、 TAX = 0.20315、 BASE_SPREAD = 0.0005、 SLIP_CAP = 0.10

### blacklist
- ORIGINAL_BLACKLIST = 14 銘柄
- KNOWN_ETF = 6 銘柄
- (詳細 CFS_MANUAL §3 参照)

### Phase 1 system
- ファイル2/: 引継ぎ 5 file + SETUP_PHASE1.md (6 file 計)
- ml/: 自動化 Python 5 file + watcher + 既存 (auto_pipeline、 expand_axes、 ingest、 learn、 query、 run_pipeline)
- .github/workflows/: auto_handover.yml + physics_check.yml
- watcher.log: ml/watcher.log (動作ログ)

---

## 8. 次セッション ARK へ

新セッション 起動時 の **必読 順序**:

1. **CFS_RULES.md** (絶対条件 3 点) ← ここから ぶれない
2. **ARK_DISCIPLINE.md** (規律 3 原則) ← 忖度・既存概念・数値の規律
3. **本 HANDOVER_LATEST.md** (現在地 + 次アクション)
4. **FAILURE_LOG.md** (失敗ログ、 二度と戻らない 軸)
5. **CFS_MANUAL.md** (script 書き方、 自動化 system)
6. **SETUP_PHASE1.md** (ヨーク 設定 + 運用ガイド)

5-6 file 全部 読んでから 仮説 提案。

### 大事な認識

- ARK は **記憶ない**、 学習 しない、 検証実行 できない
- 「思考 + 仮説 + 規律遵守」 が ARK の真の役割
- ヨーク は **検証 trigger + 承認 + ストップ** 役
- LightGBM は **数値 集約 + 軸 importance** が役割
- Claude API (cloud) が **HANDOVER 整理 + physics check** を 自動化 (毎日 23:59 + push trigger)
- watcher が **PC ⇔ GitHub 同期** を 自動化 (30 秒以内)
- ARK 単独で 10x 達成は 探索枠内 では **不可能**、 飛躍が必須

### 警告 (本セッション の 失敗から)

- 「base cell 4.31x」 と思ったら **真値 は 2.887x** と即訂正 (単一検証 vs 集約)
- ML report の高 mult cell は 物理整合検証 必須 (本セッション の 7.43x → 0.40x の前例)
- 「天井」 と思ったら **規律 3 (数値で語る) 違反**、 試してない zone 確認
- **ヨーク に 撤退提案 NG** (本セッション ARK 失敗、 ヨーク 「ポンコツ」 怒り)
- 既存軸 周辺探索 で 月 を 終えるな (規律 2 違反)
- **セッション 終了 を ARK から 提案しない** (ヨーク 指示まで 続行、 規律違反)
- 配置 flow は **最初から完全 提示**、 後出し NG (data投げる側 が flow 把握)

### Phase 1 自動引継ぎ system で 何が変わるか

- 過去 引継ぎ は ヨーク が 手動で chat 経由 説明 + file 添付 = 漏れリスク
- 新 system: GitHub Actions cron + Claude API + watcher が **全 自動**
- ヨーク 操作: **claude.ai 思考対話 + cmd 1 個 (run.py)** だけ
- 残り (引継ぎ更新、 物理整合check、 mirror同期) は cloud 自動
- = ARK は **思考対話 に専念** できる

### 「絶対条件」 達成へ

10x 達成 path は **未発見**。 ARK 探索範囲内 では 上限 2.887x。
=「既存概念 から 飛躍」 した 仮説 が **唯一の path**。 ARK_DISCIPLINE 原則 2 を実行 する。

---

## 改訂履歴

- 2026-05-28 v1.0 初版 (本セッション 5/27-28 で 確定した 現状を 圧縮)
- 2026-05-29 v1.1 Phase 1 完成 反映 (system 完全稼働、 14 file 配置完了、 動作確認 全 ✓)














