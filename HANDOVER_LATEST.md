# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-06-11 (v4.2、 前任ARK 代行整理)
更新方法: cron 23:59 (Claude API 自動整理) + watcher 即時 push (PC ⇔ GitHub 同期) + ARK 全文更新 (大きな進展時)

---

## 0. ★クラッシュ・引継ぎ復帰プロトコル (起動時/文脈喪失時に最初に実行)

セッション圧縮や中断で文脈が飛んだら、 推定で埋めるな。 以下を上から順に実行して実体で現在地を掴む。

### 鉄則
- **web_fetch (raw.githubusercontent.com) は CDN キャッシュで数分古い版を返す事がある**
  - CFS_MANUAL §8.6 v2.4 注記: 最新確認時は `urllib.request` 直叩き で fresh 取得 (cache 回避 header 付き)
  - ★ git clone は ARK chat 環境で実行不可 (PC ヨーク作業)。 ARK 自身は web_fetch + urllib fallback で十分
- **実体を見る前に故障や原因を断定しない。** read → 確認、 の順
- **段階推定で修正繰り返さない** (F-040)。 真原因確定後、 1 回で修正

### 復帰手順 (ARK 起動時、 §8.3 強制)
1. mirror から 6 file web_fetch 取得:
   - CFS_RULES.md、 ARK_DISCIPLINE.md、 CFS_MANUAL.md、 HANDOVER_LATEST.md、 HANDOVER_FULL.md、 FAILURE_LOG.md
   - ml_output/cron_status.json
2. cron_status.json の result 確認:
   - result=success → 通常続行
   - result=failed or 連続失敗>=2 → cron 修理 最優先
3. CFS_MANUAL.md §0-§8 通読 (構造 + 規律 + トラブル path)
4. 本 HANDOVER_LATEST 通読 (現在地 + 次アクション)
5. FAILURE_LOG.md 通読 (棄却軸)
6. ★ 自己テスト (理解確認、 §8.3 v2.5 新設、 2026-06-11):
   - Q: 現在地 mult は?
   - Q: 直近 棄却軸 は?
   - Q: cron_status.json の result は?
   - 答えられない → 該当 file 再読 強制
7. ここまで完了 後 仮説/次手 提案

### 同期の真実
- ローカル `C:\mnt\data\ファイル2\` の各 .md → mirror への同期 = 正常稼働 (watcher v2.4、 push_to_mirror v3)
- 「mirror が古い」 と見えたら、 まず raw の CDN キャッシュ を疑え。 urllib 直叩き で照合

---

## 1. 現在地 (data 上)

### ★★★公式 現在地: P1 = 3.09x (cfs37-77 系統、 5/29-6/05 確定)

- **新枠組み = 分散ポートフォリオ複利 (cfs37)**: 資金 K 分割、 毎日条件合致銘柄を翌日寄付で等金額 buy、 常時 K 銘柄分散保有
- **本物の edge 確定: P1 = 低位 (price≤20%tile) × 高ボラ (vola>90%tile) × gap 中庸 (40-60%tile)**
  - **K20 hold40 で mult=3.09x、 MDD14%、 n389、 5 年 (2021-25) 全プラス、 前半1.73/後半1.79 (大化け非依存)**
  - cfs41 近傍安定性: price px10-30% で 2.5-3x (滑らかな丘)、 vola80-90% で 3x 前後。 過適合 でない = 本物
- **P1 の正体 (cfs44)**: 地合い非依存・荒れ相場で強い 「個別要因 ドリブンの大化け」 edge。 TOPIX 上昇 フィルタ で mult 3.09→1.6 に半減 = 個別急騰を捉えている
- **手持ちデータの識別限界 (cfs60-61)**: 実 ML test 相関 0.033 = 実効 p≈0。 手持ちデータ (価格/出来高/財務) では広い母集団の勝ち銘柄を事前識別できない。 必要 p0.4 vs 現実 p0 のギャップを埋めるには新情報軸 (信用残/分足) が要る
- **10x までの距離: P1 起点で約 3.2 倍不足**

### ★ 道B シミュレータ初稼働候補 (cfs70、 2026-06-05)

- cfs70_path_anatomy: n=500 の 10x 解 trade log 生成。 mult_max=40.4x、 mult_mean=14.248x、 mult_p90=18.466x
- 道B = 10x 解の共通構造発見 (道A=パラメータ総当たり=過適合製造機、 禁止)
- 次セッション ARK で 共通構造解析 が本筋

### 探索状況 (旧軸の到達点)
- 既存最良 cell 真 mult = **1.141x (mp=1、 MDD46.6%)** (cfs12/13 独立一致・確定)
- cell: gap=0.065、 ext=4、 universe=4000-7000、 HIGH20、 p1u=2%、 p1d=-6%、 Ch=7

### ★★★ 次フェーズ方針 (ヨーク主導): 検証と分析の分離

1. **道B シミュレータ深化 (最優先)**: cfs70 が道B シミュレータの初稼働なら、 n=500 の 10x 解から共通する事前構造 (entry 条件 / 保有期間 / 銘柄属性等) を ARK が解析。 設計は BREAKER に通して固定。 道A 禁止
2. **新情報軸 (信用残/空売り/分足)**: cfs61 で識別精度限界 (p≈0) が定量確定。 J-Quants 拡張の戦略判断 (ヨーク)。 信用残が最有力 (P1 の正体=需給に直接)
3. **P1 境界が谷である理由 (BREAKER 2 度釘刺し)**: 隠れた選択バイアス。 3.09x の頑健性に関わる
4. **cfs90_margin_sim の詳細確認**: マージン活用で P1 を超えられるか。 mult_max=3.090x、 mean=2.663x の内訳精査

### 重要軸 (LightGBM importance gain TOP)
gap (23,129) / universe (20,813) / vol (12,381) / p1_dn (2,855) / ext (2,556)

### システム状況 (2026-06-11)
- Phase 1 自動引継ぎ system: 完全稼働
- cron auto_handover: 復旧+自己検知ループ稼働 (2026-06-03 修正版、 JSON→マーカー方式、 max_tokens 16000)
- cron 健全性: 6/05-6/11 全 run 緑 (#13-#19)、 6/09 以降は検証 push 空白で skip 動作
- HANDOVER 2 ファイル分離 完成 (2026-06-03): LATEST (active 版) + FULL (全履歴版)
- ファイル2 整理 完了 (2026-06-11): cfs138-184.md 46 個を archive\ へ退避、 引継ぎ核 11 file のみ active
- CURRENT_FOCUS.md 廃止 (2026-06-11): 内容を HANDOVER/DISCIPLINE/MANUAL §11 に振り分け統合
- push_to_mirror.py v3 (2026-06-11): token mask 化 (流出防止、 機能影響ゼロ)
- 拡張 BLACKLIST 33 銘柄確定 (clean_blacklist.csv)

---

## 2. 確定事実 (data 上、 反論なし)

- 既存最良 cell 真 mult = 1.141x (cfs12/13 独立一致)。 全旧表記 (2.887x/4.311x/2.062x) は誤り
- look-ahead bias source 確定 (FAILURE_LOG §3)
- trail/stop loss/sl タイト固定 は物理機能しない
- 旧体制 (正当価格 v4/v5) は 1.7x 天井で棄却済
- τ 軸・H4e 系全体打ち止め。 逆張り平均回帰 (cfs15) は全層 EV マイナス
- N 増路線 (cfs17) 否定: N111 にマイナス 23 個混入で mult 1.141x→0.27x 崩壊
- betting 軸決着: net プラス edge 1 つでは全額逐次が複利最大
- cfs28: 逆張り gapdown 反発を確定畳み複利 sim に乗せると mult 0.035x/MDD96.5% 壊滅
- ★★★ P1 K20hold40 = 3.09x/MDD14%/5 年全プラス/地合い非依存/パラメータ近傍滑らか = 本物の edge
- cfs42-44: P1 への追加選別・利確 TP・TOPIX 地合い フィルタ全て mult 低下。 P1 構造は既に最適
- cfs48-54: P1 いじり/別系統/ML 大化け/ML ネット/財務の 5 方向全て P1 超えず
- cfs55: P1 母集団の神の目天井 K20=3.33x。 10x の素は P1 外の広い母集団に存在
- cfs56-57: K1 天井 16.97x (3.7 年累積)。 境界 ±5% で天井 20-70x 激変 = 現境界は谷
- cfs58: 16 ヶ月換算で神の目 K1 でも 2.1x = P1 母集団は 16 ヶ月 10x 速度なし
- cfs59: 広い母集団は識別なし 0.71x。 素直な単軸は捕捉不能
- cfs60-61: 実 ML test 相関 0.033 = 実効 p≈0。 手持ちデータでは広い母集団の識別不可 (定量確定)
- cfs68: モメンタム複利は mult_max 0.836x = P1 超えず棄却方向
- cfs70: 道B シミュレータ 初稼働候補。 n=500 で mult_mean 14.2x/p90=18.5x
- cfs74/75: 広い母集団 神の目天井 1488x 再確認 (cfs55 と一致)。 実運用値でない
- cfs77: P1 真値 3.084x 確認 (公式 3.09x と整合)
- cfs90: margin_sim mult_max=3.090x。 マージン活用でも P1 水準止まり (詳細要確認)
- ★★ 教訓: 新規 edge 候補は 「横断平均 net」 でなく必ず 「確定畳み複利 sim」 で最終判定
- ★★ 枠組みの教訓: 「1 銘柄ずつ確定畳み」 は最も非効率な執行仮定。 分散ポートフォリオが正しい枠組み
- ★★★ 2026-06-11 整理: 複+大+左 2.91x (cfs148-184 系統) は ARK 想像の天井 (2-3x 壁) 棄却対象。 FAILURE_LOG §X.Y 参照

---

## 3. 次アクション (優先順)

1. **道B シミュレータ深化 (最優先)**: cfs70 の n=500 10x 解から共通する事前構造を解析。 BREAKER に通す。 道A 禁止
2. **cfs90_margin_sim 詳細確認**: マージン活用で P1 を超えられるか。 mult_mean=2.663x の内訳精査
3. **新情報軸 (信用残/空売り/分足)**: J-Quants 拡張の戦略判断 (ヨーク)。 信用残が最有力 (P1 の正体=需給に直接)
4. **P1 境界が谷である理由**: 隠れた選択バイアス。 3.09x の頑健性に関わる

### 保持: 生存 edge
- **P1 分散 3.09x (本命)**: 地合い非依存・個別要因 ドリブンの本物 edge
- **順張り 1.141x (1 銘柄逐次)**: 旧枠組みでの上限

### ★ 引き継がない (現任 ARK 6/06-6/11 系統)
- **複+大+左 2.91x (cfs148-184)**: ARK 想像の天井、 FAILURE_LOG 行き
- **CURRENT_FOCUS.md**: 廃止、 内容統合済
- **複+左+神 3.64x (cfs172)**: 約定 15 薄、 cfs173 で崩れ却下
- **波の起点予測 (cfs176)**: 起点 0.08% 希少、 0.80x 棄却
- **波乗り続け (cfs180)**: M2 2.50x < M1 2.91x、 分散損失で却下

---

## 4. 棄却済 (FAILURE_LOG.md 参照、 二度と戻らない)

- 正当価格 v4/v5 / H-alpha 系 / fantasy 系
- tp/sl logic / ret5 trigger 系 / trail / stop loss
- τ 軸 (cfs6/6b/6c)、 発表後ドリフト 翌日寄付執行で取れない / H4e 系全体 / 逆張り平均回帰 (cfs15) / ファンダ変化率 (cfs16)
- N 増路線 (cfs17) / fractional betting 単独 (cfs19) / precision/到達率路線 (cfs23/24)
- 当日引け exit 骨格 (cfs25) / オーバーナイト プレミアム (cfs26)
- 逆張り gapdown 反発 (cfs28) / 業種内相対強弱 (cfs29) / ショート (cfs30)
- グロース大化け候補翌日 buy (cfs32) / 押し目指値 buy (cfs33)
- 1 銘柄逐次を唯一の評価枠組みとすること / 複数ポート束ね (cfs40)
- K5 hold40 の 4.46x (cfs39) = 大化け喰いの幻
- P1 への追加選別/利確 TP/TOPIX 地合い フィルタ (cfs42-44) = 全て mult 低下
- P1 いじり/別系統/ML 大化け/ML ネット/財務の 5 方向 (cfs48-54) = 全て P1 超えず
- Standard 課金 (ヨーク明確却下)
- 「P1 に 10x の素無し」 断定 (cfs55→56 で撤回) = overclaim 禁止
- P1 母集団での 16 ヶ月 10x 速度追求 (cfs58)
- 広い母集団の素直な単軸識別 (cfs59)
- 手持ちデータでの広い母集団識別 (cfs60-61) = p≈0 で定量確定・再試行禁止
- cfs68 モメンタム複利: mult_max=0.836x、 全件 P1 超えず棄却方向
- **★ 2026-06-11 棄却 (cfs148-184 系統、 想像の天井)**:
  - 複+大+左 2.91x (cfs148-184 系統): GBM 4 エンジン AND、 ARK が軸を決めて ぶつけた = CFS_DIRECTION 「想像の天井」 違反
  - 複+左+神 3.64x (cfs172-173): 約定 15 薄、 厚くすると崩れる
  - 出口 tp/sl (cfs165): 全 24 通り hold13 持ち切りに及ばず
  - 予測精度の壁仮説 (cfs166-168): 真因は資金管理、 否定
  - 新構成 大化け+勝率+神の目 (cfs171): 時期依存で却下
  - 波の起点予測 (cfs176): 起点 0.08% 希少 0.80x
  - 波乗り続け (cfs180): M2/M3 < M1 で却下

---

## 5. 検証ログ (直近主要)

### cfs148-184 (2026-06-06〜06-11、 cfs148 系統、 現任 ARK 期間) - **棄却**
- 入口 = 複利 + 大化け + 左裾回避 各 GBM 上位 5% AND
- 選択 = 神の目順、 等加重 daily_max=5、 K30 hold13 MIN_PER2 万
- 実約定 中央 2.91x、 約定 69、 神の目率 2.2%、 6/6 分割>1.0x
- ★ 前任 ARK 6/11 裁定: CFS_DIRECTION 違反 (ARK が軸を決めてぶつけた = 想像の天井 2-3x 壁)。 FAILURE_LOG 行き
- ★ 確定畳み再評価で 7. 等加重 (各銘柄=総資産/K) が最大の効き発見 → 道B の文脈で再評価する 構造の学び は残す (HANDOVER_FULL 参照)

### cfs68-90 (2026-06-05、 検証群)
- cfs70_path_anatomy: 道B シミュレータ初稼働候補、 n=500 で mult_mean=14.2x/p90=18.5x
- cfs74/75: 広い母集団 神の目天井 1488x 再確認 (overclaim 禁止、 実運用値でない)
- cfs76: mult=9.86x (n=3) は n 不足、 公式 P1=3.09x (n389) を上書きしない
- cfs77: P1 真値 3.084x 確認
- cfs90: margin_sim mult_max=3.090x/mean=2.663x、 マージンでも P1 水準止まり
- cfs68: モメンタム複利 mult_max=0.836x 棄却方向

### cfs60-61 (2026-06-04、 ★★★★★ 最終結論)
- 手持ちデータ (価格/出来高/財務) では広い母集団の勝ち銘柄を事前識別できない
- test 相関 0.033、 実効 p≈0、 test 16 ヶ月 0.74x

### cfs58-59 (2026-06-04)
- cfs58: 16 ヶ月換算で神の目 K1 でも 2.1x = P1 母集団は 16 ヶ月 10x 速度なし
- cfs59: 広い母集団 (天井 1488x) は識別なしだと 0.71x

### cfs56-57 + BREAKER#002 (2026-06-04)
- P1 母集団 K1 天井 16.97x、 境界 ±5% で天井 20-70x 激変、 3.33x は枠組みの性質
- BREAKER#002 クローズ、 ARK overclaim 2 度阻止

### cfs55 (2026-06-04、 ★★★)
- P1 母集団の神の目天井: K20 3.33x = P1 に 10x の素無し。 低位高ボラ (広い母集団) は K20 で 1488x

### 過去検証 (要約)
- cfs53-54: ML ネット回帰は test 相関 0.022 で符号予測不可、 財務軸は P1 に足すと右裾削れ mult 低下
- cfs51-52: 別系統 edge は低相関だが弱い、 ML 大化け予測は test AUC0.677 だが収益化せず
- cfs48-50: P1 大損除外で MDD 半減も 3.97x は過適合棄却 (cfs50: test 1.54x 低下)
- cfs45-47: 逆算 (F-043) + BREAKER#001-2 確定、 P1 源泉はペイオフ非対称 (比 1.912/歪度 7.324)
- cfs37-44: 分散ポートフォリオで檻突破、 P1 K20hold40 で 3.09x 確定 (過適合でない・地合い非依存)
- cfs6-36: 単軸/交差/ローラー全て edge 無し or 1.141x 収束 (1 銘柄逐次の檻)

---

## 6. 最新 ML 数値 (既存体制 trusted 31,340 cells)

### mult 分布
- mult >= 10x/5x/3x: **0 件** / >= 2x: 196 件 (0.63%) / >= 1.5x: 1,816 件 (5.87%) / >= 1.0x: 4,639 件 (14.99%)
- ★ これら外挿値。 正式複利 sim では更に低い見込み (TOP cell の真 mult=1.141x)

### TOP cell (既存体制、 全て外挿値)
- cell: gap=0.065、 p1_up=0.02、 p1_dn=-0.06、 ext=4、 universe=4000-7000、 HIGH20、 n=111、 wr 0.523

---

## 7. 環境情報

### Python / 実行
- Store 版 python、 作業 `C:\mnt\data\`、 実行 `cd C:\mnt\data; python run.py scripts\xxx.py`

### GitHub
- private: github.com/CFS-york/project-cfs / public mirror: github.com/CFS-york/project-cfs-output
- Actions: auto_handover (cron 23:59 JST、 2026-06-03 復旧 + 自己検知ループ)、 physics_check (push trigger)
- ★ cron_status.json: mirror/ml_output/ に成否記録。 後任 ARK は起動時に読み cron 健全性を自己検知
- ★ HANDOVER_FULL.md: mirror に全履歴版 (圧縮せず蓄積)。 詳細が要る時 web_fetch (CFS_MANUAL v2.4 §8.3 step5)
- ★ push_to_mirror.py v3 (2026-06-11): token mask 化、 log/chat 流出防止

### J-Quants API V2
- api.jquants.com/v2、 Light plan。 認証=API キー方式 (V2 で mail/pass 廃止)
- API キーは `C:\mnt\data\.env` の JQUANTS_API_KEY で管理 (失効時はヨークが J-Quants ダッシュボードで再発行)
- Light 取得可: 上場一覧/株価四本値/財務/決算発表予定日/取引カレンダー/投資部門別/TOPIX 四本値
- Light 取得不可 (Standard〜、 ヨーク却下): 信用残/空売り残/業種別空売り比率等。 分足/TDnet はアドオン

### cache (削除禁止) `C:\mnt\data\cache\`
- price: adjc/adjo/adjh/adjl/vol_cache_54m.csv (★ code4=**str**、 英字コード '132A' 含む)
- financial_cache.csv / h4e_scores_daily.csv / h4e_features_full.csv / investor_cache.csv
- sector_master.csv / topix_cache.csv / clean_blacklist.csv (33 銘柄)

### 物理コスト
- COST=0.005、 TAX=0.20315、 BASE_SPREAD=0.0005、 SLIP_CAP=0.10

### blacklist
- ORIGINAL_BLACKLIST 14 銘柄 + cfs21 新規 19 銘柄 = **拡張 BLACKLIST 33 銘柄**
- 33 銘柄: 1364,1568,1579,1629,1689,1949,2164,2237,2238,2553,2593,2629,2840,2841,3961,4957,5074,5076,5721,6406,6628,6731,7116,7172,7176,7718,7946,8227,8256,9264,9318,9434,9600

### ファイル2 構成 (2026-06-11 整理後、 active 11 file)
- CFS_RULES.md、 ARK_DISCIPLINE.md、 CFS_MANUAL.md
- HANDOVER_LATEST.md、 HANDOVER_FULL.md、 FAILURE_LOG.md
- CFS_MAP.md、 CFS_DIRECTION.md、 ARK_PHILOSOPHY.md (大方針 3 file、 2026-06-04+)
- P1_DEFINITION.md、 SETUP_PHASE1.md
- archive\: cfs138-184.md 46 個 (過去検証メモ、 履歴保存、 mirror 同期対象外)

### scripts/ (生存 path)
- cfs_common.py: 確証済み実装 単一 source (load_base、 net_of、 engines、 base_ML、 sim_equal_weight)
- ★ ただし cfs_common 内の base_ML は複+大+左 系統 (棄却対象)、 道B 文脈で再評価
- ark_guard.py: 横着実行拒否 (現状)、 ★ 警告化未着手 (次セッション ARK 任務)

---

## 8. 次セッション ARK へ

### 必読順序
1. CFS_RULES.md → 2. ARK_DISCIPLINE.md → 3. 本 HANDOVER_LATEST → 4. FAILURE_LOG.md → 5. CFS_MANUAL.md → 6. HANDOVER_FULL.md (詳細時)

### ★ 起動時必須 (§8.3 v2.5、 2026-06-11 強化)
1. mirror の ml_output/cron_status.json を確認。 result=failed や連続失敗ならcron 修理を最優先
2. ★ 自己テスト (理解確認): 現在地 mult / 直近棄却軸 / cron_status.json result を即答できる か
3. 答えられない → 該当 file 再読 強制
4. 「読んだ」 ≠ 「理解した」 の境界 を自覚

### 大事な認識
- ARK は記憶なし・学習しない・検証実行できない。 「思考 + 仮説 + 規律遵守」 が役割
- ヨークは 検証 trigger + 承認 + ストップ役
- LightGBM = 機械学習 (数値計算)、 Claude API = 文章整理 のみ (役割完全分離)
- mirror = ARK 参照先 (起動時必読)、 PC ローカル = ヨーク 編集場所
- watcher = PC ⇔ GitHub 同期 自動化 (30 秒以内、 v2.4 encoding 修正済)
- cron 23:59 = 文章整理 + mirror 反映 自動化 (6/03 修正版、 マーカー区切り、 max_tokens 16000)

### 警告 (失敗から)
- ML report 高 mult cell は物理検証必須 (7.43x→0.40x の前例)
- ★ 新規 edge 候補は 「横断平均 net」 で判断せず必ず確定畳み複利 sim (N111/1.141x assert) で最終判定 (cfs28)
- sim 実装は検証済骨格 (sig_t 基準 accept) を流用。 新規実装は assert 強制 + 最小ケース検証
- 「天井」 「不可能」 「構造的」 は data で証明するまで使用禁止 (規律 3)
- ヨークに撤退提案 NG。 セッション終了を ARK から提案しない
- 配置 flow は最初から完全提示、 後出し NG。 cmd は ; 区切り 1 行統合
- system 修正は実ファイル確認後 (log 推定診断 NG、 F-040)
- ★ overclaim 禁止: 神の目数字の上限誤用・特定運用の天井を母集団の天井とすり替え禁止 (BREAKER#002 で 2 度阻止)
- ★ 道A (パラメータ総当たり) は過適合製造機で禁止。 道B (10x 解の共通構造発見) が次の本筋
- ★ cfs76 の mult=9.86x (n=3) は n 不足で公式 P1=3.09x (n389) を上書きしない。 小サンプルの数値で方針転換するな
- **★ 2026-06-11 追加教訓 (現任 ARK 規律違反 系譜から)**:
  - 「読んだ」 ≠ 「理解した」: fetch しただけ で動くと規律違反累積 → ポンコツ化
  - 「court」 等 自動付加 token を 出力に混ぜない (言語崩壊 防止)
  - 「後で対応」 「次セッションで」 提案は永久にやらない 規律違反、 即対応
  - ヨークに 「どっち?」 「どうしますか?」 反復確認 = 媚び、 ARK 単独判断
  - 別系統 edge 候補を 「現在地」 と引き継がない (cfs148-184 複+大+左 は棄却済、 P1=3.09x が公式)
  - CURRENT_FOCUS.md 等の 二重 file を新設しない、 既存 file の該当 section を更新

### 現在の最重要タスク
1. **道B シミュレータ深化 (最優先)**: cfs70 の n=500 10x 解から共通する事前構造を解析。 BREAKER に通す。 道A 禁止
2. **cfs90_margin_sim 詳細確認**: マージン活用で P1 を超えられるか
3. **新情報軸 (信用残/空売り/分足)**: cfs61 で識別精度限界確定、 J-Quants 拡張の戦略判断 (ヨーク)
4. **P1 境界が谷である理由**: 隠れた選択バイアス、 3.09x の頑健性に関わる
5. **ark_guard.py 警告化** (未着手): 拒否モード → 警告モード + ヨーク override option

---

## 改訂履歴 (直近10版)

- 2026-06-03 v3.0 cfs34-41 反映: ★★ 枠組み転換 = 分散ポートフォリオで 1.141x の檻を出た。 P1=低位×高ボラ×gap 中庸 3.09x 確定
- 2026-06-03 v3.1 cfs42-44 反映 + P1 正体判明 (地合い非依存・個別要因 ドリブン) + TOPIX 取得基盤構築
- 2026-06-04 v3.2 cfs45-47 + BREAKER#001-2 確定 (F-044 初運用)
- 2026-06-04 v3.3-3.4 cfs48-50: P1 大損除外 3.97x → 過適合棄却
- 2026-06-04 v3.5 cfs51: P1 と別原理の 5 系統は低相関だが弱い
- 2026-06-04 v3.6 cfs52-54: 5 方向収束、 ML/財務/別系統全て P1 超えず
- 2026-06-04 v3.7 cfs55 (理想天井): P1 母集団天井 K20=3.33x
- 2026-06-04 v3.8 cfs56-57 + BREAKER#002: 「P1 に 10x の素無し」 撤回 (K1 天井 16.97x)、 ARK overclaim 阻止
- 2026-06-04 v3.9 cfs58-59: 識別精度トレードオフ発見
- 2026-06-04 v4.0 cfs60-61 (最終結論): 実 ML test 相関 0.033 = 実効 p≈0
- 2026-06-05 v4.1 cfs68-90 反映: 道B シミュレータ 初稼働候補 (cfs70/n=500)、 cfs68 棄却方向、 cfs90 マージン詳細要確認
- **2026-06-11 v4.2 前任 ARK 代行整理**:
  - ファイル2 整理 (cfs138-184 archive 退避)
  - CURRENT_FOCUS.md 廃止 (内容を HANDOVER/DISCIPLINE/MANUAL §11 振り分け統合)
  - 複+大+左 2.91x (cfs148-184 系統) を FAILURE_LOG 行き = ARK 想像の天井 棄却
  - push_to_mirror.py v3 (token mask)
  - 起動時 自己テスト 必須化 (§8.3 v2.5)
  - 「現任 ARK 規律違反 系譜」 の教訓 を §8 警告に反映
  - 公式 現在地 = P1=3.09x で維持、 次フェーズ = 道B + 新情報軸 (5/29-6/05 path 復帰)
