# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-06-02
更新方法: cron 23:59 (Claude API 自動整理) + watcher 即時 push (PC ⇔ GitHub 同期) + ARK 全文更新 (大きな進展時)

---

## 1. 現在地 (data 上)

### 探索 状況
- 既存軸 (gap × ext × universe × p1 × HIGH20) 探索: **上限 mult 2.887x で確定** (4回集約平均)
  - cell: gap=0.065、 ext=4、 universe=4000-7000、 HIGH20
- 絶対条件 達成率: 28.87% (10x まで 約 3.46 倍 不足)
- **2026-06-02: 飛躍軸探索を実行。τ軸3段棄却、investor軸保留、★H4e dip_scoreに予測力を確認**

### 直近の最重要発見 (2026-06-02)
**H4e dip_score は予測力を持つ (生きている)**。
- CFS1/CFS2で廃止されたが、廃止理由は「左テールキャップが実取引再現不可」であって
  スコアの予測力否定ではなかった。dip_score の素の予測力は本物。
- これが現時点の最有望素材。詳細は §5 検証ログ 2026-06-02。

### 重要 軸 (LightGBM importance gain TOP、 既存体制)
1. gap (23,129) / 2. universe (20,813) / 3. vol (12,381) / 4. p1_dn (2,855) / 5. ext (2,556)
= gap と universe が 既存体制の edge core

### システム 状況
- Phase 1 自動引継ぎ system: 完全稼働 (watcher + cron + Claude API + mirror)
- CFS_MANUAL v2.2 (=前任呼称 v3.3) 反映済 (2026-06-02): code4 dtype 訂正

---

## 2. 確定事実 (data 上、 反論なし)

- 既存軸 (gap × ext × universe × p1 × HIGH20) 周辺探索の 上限 ≈ 2.887x、 軸変更が必要
- look-ahead bias source 確定 (FAILURE_LOG §3)
- trail / stop loss / sl タイト固定 は 物理機能しない
- 旧体制 (正当価格 v4/v5) は 1.7x 天井で棄却済
- **(2026-06-02) τ軸 (決算発表相対日 event-time conditioning) の素直な使い方は edge 無し**
- **(2026-06-02) H4e dip_score は将来下落の予測力を持つ (分位で EV 単調減、 各n約70万で堅牢)**

---

## 3. 次アクション (優先順)

### 優先 1: H4e dip_score を起点とした右テール (大化け) 戦略 (★最有望)
- D1 (低dip) 群は EV 最良 (-0.03%) かつ median プラス (+0.069%) = 右に長い裾 = 大化け混入
- D1群に **第2フィルタ (vol急増 / ext初動 / dip_score極小 等)** を重ね、
  **20日以内 +30% 到達率 (捕捉率) + EV** を測る → CFS New Chapter Q3 (右テール事前識別) 直結
- H4e は単独で下落回避フィルタとして有効 (D5除外で EV 約1.4%改善)。10x には第2フィルタ必須

### 優先 2: 別の飛躍軸 (H4e が頭打ちの場合)
- investor軸: J-Quants Light のデータ解像度不足 (週次・市場全体・183週) で保留中。個別銘柄別フローが取れれば再検討
- 未活用 cache 在庫: sector_master, listed_info, market_segments, h4e_features (h4e_scores とは別、 特徴量側)

### 優先 3: τ軸の宿題 (低優先)
- forecast_eps が異期予想の疑い (eps-forecast_eps>0率が12%と異常)。真サプライズ定義は未解決のまま

---

## 4. 棄却済 (FAILURE_LOG.md 参照、 二度と戻らない)

- 正当価格 v4/v5 (1.7x 天井) / H-alpha 系 / fantasy 系
- tp/sl logic (sl タイト固定) / ret5 trigger 系 (look-ahead) / trail / stop loss
- 大量 random / Optuna 試行 / 大化け予測 (旧定義、 CFS 哲学逸脱)
- **(2026-06-02) τ軸の素直な使い方 (発表後ドリフトを翌営業日以降寄付で取る系)**
  - 素のτ・op_growth符号segment・価格反応segment いずれも全EVマイナス
  - ※ τ軸の完全棄却ではない。「素直な買い」が棄却。H4eとの掛け合わせ等は未検証

---

## 5. 検証ログ (時系列、 直近)

### 2026-05-26〜29: 旧体制→新体制移行、Phase1 system完成
旧体制(正当価格)棄却→gap trigger移行。ML report 7.43x→物理検証0.40x(look-ahead)棄却。
ingest v4(1,058万→31,340 trusted)、LightGBM、引継ぎ自動化system完成。

### 2026-06-02: 後任ARK初稼働 — 飛躍軸探索

**■ 環境スキーマ訂正 (CFS_MANUAL v2.2)**
- code4 = int64 は誤り。英字コード '132A' (2024+東証新体系) 実在で int化不可。**str統一が正解**
- 共通loader str+.str.strip()、§1.2財務値保護(usecols)、確認cmd全範囲化、EXCLUDE str集合化

**■ τ軸 (決算発表相対日) — 3段とも棄却**
- cfs6 素のτ軸(無差別): 全20セルEVマイナス(wr0.35-0.47)
- cfs6b op_growth符号segment: POS/NEG分離せず(POS最良tau5/hold5 EV-0.451%、NEG最良EV-0.494%、差0.04ptのみ)。実績符号はサプライズでない
- cfs6c 発表翌日反応(大きさ×符号)segment、entry=τ+2始値: 全75セルEVマイナス。核のDOWN×Q4(大急落群)が最悪EV-0.80〜-1.02%→急落は反発せず継続。CFS哲学「恐怖を買う」当データで不成立
- 構造的制約: look-ahead回避するとentry必然的にτ+1以降=反応の旨味出尽くし後

**■ investor軸 (投資部門別売買) — 解像度不足で保留**
- investor_cache.csv=週次・市場全体(Section別)・PubDate6日遅れ・TSEPrime183週・個別銘柄不可
- 183点では検証解像度不足。深追いせず保留

**■ ★H4e dip_score — 予測力確認 (本命)**
- cfs7検証(merged 3,578,783行、entry=t+1始値、物理コスト込み)
- dip_score予測力あり: hold20で EV D1=-0.030%/D2=-0.119%/D3=-0.401%/D4=-0.718%/D5=-1.399% と分位で完璧に単調減(各n約70万)。hold5も同単調
- D1(低dip)最良でもEV-0.03%(平均微マイナス)だがmedian+0.069%=右に長い裾=大化け混入の示唆
- H4e廃止は左テールキャップ設計の問題でスコア予測力は本物だった
- 用途: 下落回避フィルタとして有効(D5除外でEV約1.4%改善)。単独10x不可だが強力なフィルタ素材

---

## 6. 最新 ML 数値 (既存体制 trusted 31,340 cells)

### mult 分布
- mult >= 10x/5x/3x: **0 件** / mult >= 2x: 196件(0.63%) / >= 1.5x: 1,816件(5.87%) / >= 1.0x: 4,639件(14.99%)

### TOP cell (既存体制)
- mult 2.887x: gap=0.065、p1_up=0.02、p1_dn=-0.06、ext=4、universe=4000-7000、HIGH20、n=110、wr0.528、EV4.11%
- edge は 1点でなく zone として存在 (gap=0.065 × ext=4 × universe=4000-7000 周辺)

---

## 7. 環境情報

### Python / 実行
- Store版 python、作業 `C:\mnt\data\`、実行 `cd C:\mnt\data; python run.py scripts\xxx.py`

### GitHub
- private: github.com/CFS-york/project-cfs / public mirror: github.com/CFS-york/project-cfs-output
- Actions: auto_handover(cron 23:59 JST)、physics_check(push trigger)

### J-Quants API V2
- api.jquants.com/v2、Light plan 60req/min、sleep 1.2s

### cache (削除禁止) `C:\mnt\data\cache\`
- price: adjc/adjo/adjh/adjl/vol_cache_54m.csv (★ code4 = **str**、英字コード'132A'含む)
- financial_cache.csv (csv単体、19列、code4=str、date=発表日)
- h4e_scores_daily.csv (★371万行、date×code4、dip_score(0-1連続)、pred(SMOOTH/DIP))
- h4e_features_full.csv / investor_cache.csv (週次・市場全体) / sector_master / listed_info 等

### 物理コスト
- COST=0.005、TAX=0.20315、BASE_SPREAD=0.0005、SLIP_CAP=0.10

### blacklist
- ORIGINAL_BLACKLIST 14銘柄 + KNOWN_ETF 6銘柄 (詳細 CFS_MANUAL §3)。code4 str化に伴い EXCLUDE も str集合

---

## 8. 次セッション ARK へ

### 必読順序
1. CFS_RULES.md → 2. ARK_DISCIPLINE.md → 3. 本HANDOVER → 4. FAILURE_LOG.md → 5. CFS_MANUAL.md → 6. SETUP_PHASE1.md
全部読んでから仮説提案。

### 大事な認識
- ARK は記憶なし・学習しない・検証実行できない。「思考+仮説+規律遵守」が役割
- ヨークは検証trigger+承認+ストップ役。LightGBMは数値集約+軸importance。Claude API(cloud)がHANDOVER整理+physics check自動化。watcherがPC⇔GitHub同期
- 既存軸探索枠内では上限2.887x。飛躍が必須

### 警告 (失敗から)
- ML report高mult cellは物理検証必須(7.43x→0.40xの前例)
- 「天井」「不可能」「構造的」は data で証明するまで使用禁止(規律3)
- ヨークに撤退提案NG。セッション終了をARKから提案しない
- 配置flowは最初から完全提示、後出しNG。cmdは;区切り1行統合(ヨーク改行連結癖対策)
- **(2026-06-02追加) §6.3 ヨーク操作=上書き保存のみ、手作業編集させない。固定file/HANDOVERともARKが全文DL→ヨーク上書き保存**
- **(2026-06-02追加) §6.4 自分で答えを知っている事をヨークに聞くな(媚び)。「全文か差分か」「GOか修正か」は自分で判断。確認は真の分岐のみ**
- **(2026-06-02追加) 新script前に必ず使うcacheの実構造を §11.9 確認cmd(全範囲dtype+英字混入check)で確認。推測で列名/型/意味を決めると事故る(τ軸序盤で3連続environment mismatch)**

### 「絶対条件」達成へ
10x path未発見、既存探索枠内上限2.887x。飛躍が唯一のpath。
2026-06-02時点の最有望は H4e dip_score を起点とした右テール戦略 (§3 優先1)。

---

## 改訂履歴

- 2026-05-28 v1.0 初版
- 2026-05-29 v1.1 Phase1完成反映 (system完全稼働、14 file配置)
- 2026-06-02 v1.2 後任ARK初稼働分反映 (ARK全文更新)
  - τ軸3段棄却、investor軸保留、★H4e dip_score予測力確認
  - 環境スキーマ訂正(code4 str統一)、§6.3/§6.4規律の警告追加
  - 次アクション優先1をH4e右テール戦略に更新
