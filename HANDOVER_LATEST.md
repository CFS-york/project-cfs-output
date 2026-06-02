# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-06-02 (v1.7)
更新方法: cron 23:59 (Claude API 自動整理) + watcher 即時 push (PC ⇔ GitHub 同期) + ARK 全文更新 (大きな進展時)

---

## 1. 現在地 (data 上)

### 探索 状況
- ★★**2026-06-02 現在地 最終確定: 既存最良cellの真mult = 1.141x (mp=1, MDD46.6%)**
  - cell: gap=0.065、ext=4、universe=4000-7000、HIGH20、p1u=2%、p1d=-6%、Ch=7
  - **真の達成率 11.4%、10xまで約8.76倍不足**。現実は想像よりはるかに遠い
  - 数字の変遷(全て誤り→真値): 2.887x(引継ぎ)→4.311x(外挿)→2.062x(cfs11 simバグ)→**1.141x(確定)**
  - 確定根拠: 確定畳みsim(cfs12)とcfs13が独立に1.141x一致。外挿式は過大、cfs11 event駆動simはバグ
  - ※真値1.141xは暫定。正式確定値化(③⑤更新)時にBREAKER検証を通すこと
- SL(cfs12,下方向exit)もtrailing(cfs14,上方向exit)も真mult全て低下=exit軸は固定短期が最適でいじると悪化
- mp並列は複利破壊。entry側(gap/ext/universe/HIGH20/τ/investor/H4e)もexit側もmp側も全て尽きた
- ★1.141xは このgap急騰モメンタムシグナルの「証明された天井」(exit最適化込み)。箱の中の最適化は完了
- 飛躍軸探索: τ軸3段棄却、investor軸保留、H4e系打ち止め(崩壊理論)

### 直近の最重要発見 (2026-06-02)
**価格時系列次元を一巡。net edgeを持つのは順張りモメンタムのみ、それも1.141x天井。別次元が必要**。
- 真mult 1.141x(mp=1, net0.285%×N111)。確定畳みsim cfs12/13/14一致。10xまで8.76倍不足
- ★今日 価格時系列ベースの軸を網羅探索し、netプラスedgeは「gap急騰モメンタム(順張り)」のみと判明:
  - 逆張り平均回帰/押し目買い(cfs15): 全層EVマイナス。売られすぎ→反発は日本株個別で不成立(続落が支配的)
  - 決算イベントτ軸(cfs6系)/H4e(cfs7-10)/exit最適化(cfs12,14)/investor: 全て不成立or天井
- 順張り1.141xが価格時系列次元の唯一かつ上限のnet edge
- ★次の本質課題: 価格時系列でない別の情報次元(ファンダ変化率、業種間資金循環、信用残の歪み等)
  - 10x逆算: net 0.23〜0.68%/trade × N 340〜1020(N500超コスト割れ)。順張り以外の収益構造が要る

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
- **(2026-06-02) ★★既存最良cellの真mult=1.141x(mp=1,MDD46.6%)。確定畳みsim cfs12/cfs13が独立一致。10xまで8.76倍不足**
- **(2026-06-02) 既存の全mult表記(2.887x/4.311x/2.062x)は誤り(外挿過大+cfs11 simバグ)。真値は1.141x**
- **(2026-06-02) exit軸決着: SL(下方向)もtrailing(上方向)も全て真mult低下。固定短期exitがこのシグナルの最適**
- **(2026-06-02) ★1.141xはgap急騰モメンタムシグナルの証明された天井(entry/exit/mp全軸最適化済)**
- **(2026-06-02) 逆張り平均回帰(売られすぎ反発・押し目買い)は日本株個別で全層EVマイナス。続落が支配的(cfs15)**
- **(2026-06-02) ★価格時系列次元ではnetプラスedgeは順張りモメンタムのみ。逆張り・イベント・exit改良は全滅。別情報次元が必要**
- **(2026-06-02) H4eは崩壊理論で10x不可。τ/investor軸も尽きた。既存手段の小改良では10x届かない**

---

## 3. 次アクション (優先順)

### 優先 1: 価格時系列でない別の情報次元の探索
- 価格時系列次元は一巡完了。netプラスedgeは順張りモメンタム(1.141x天井)のみと確定
- 逆張り/平均回帰/イベント(決算)/exit改良は全滅 → 価格時系列の中にもう新しいedgeは無い見込み
- ★必要なのは別次元の情報: ファンダ変化率(売上/利益の改善加速)、業種間資金循環/相対強弱、
  信用残の歪み(取組)、需給(出来高×値動きの非対称) 等。J-Quants Light範囲+人間執行可能 で絞る
- 注意: H4e/investorは検証済(崩壊/解像度不足)。financial_cacheの財務"変化率"は§1.2滑落に注意
  (valuationの"値"でなく、変化の方向・加速度を使う設計なら別物として検討可)
- 10x逆算: net 0.23〜0.68%/trade × N 340〜1020(N500超コスト割れ)。評価は確定畳み複利sim(mp=1)
- 着手法: 別次元シグナルを1つ選び素のnet予測力を確認(cfs7/15と同手順)→edgeあれば戦略化・複利sim

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
- **(2026-06-02) H4e D1(低dip)群を大化け母集団とする仮説 (cfs8で棄却)**
  - D1×vol急増の+30%到達率0.68%=基準の1/5。低dipは大化けも同時に避ける。大化け母集団は逆(非D1)
- **(2026-06-02) H4e系全体 (cfs7-10) 打ち止め。元々崩壊理論。既存gap戦略と水と油、新規大化けTP執行もEVマイナス**
- **(2026-06-02) ★mp(slot並列)でN増→mult増 の発想 (旧portfolio)。正式複利simで逆=複利破壊と確定**
- **(2026-06-02) ★ (1+R)^N16 外挿mult式。netを過大評価+誤差増幅。今後は確定畳み複利simのみで評価**
- **(2026-06-02) ★ cfs11 event駆動複利sim。idx管理バグで2.062x誤出力(真値1.141x)。確定畳み(全額逐次)が正**
- **(2026-06-02) 既存最良cellへの緩いSL(-8〜-20%)。真mult全て低下で逆効果(cfs12/cfs13)**
- **(2026-06-02) 既存最良cellへのtrailing exit(trail5〜15%×maxhold10〜40)。全て真mult低下(cfs14)。固定短期が最適**
- **(2026-06-02) gap急騰モメンタムシグナルの改良全般。entry/exit/mp全軸で1.141x天井と証明**
- **(2026-06-02) 逆張り平均回帰(売られすぎ反発/押し目買い, cfs15)。全層EVマイナス。日本株個別は続落支配で逆張り不成立**
- **(2026-06-02) ★価格時系列次元の探索全般。順張り以外netプラスedge無しと網羅確認。次は別情報次元**

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

**■ cfs8 H4e D1×vol急増 → +30%到達 (仮説反転)**
- 大化けは非D1(高dip=高変動)×vol急増に集中(vol≥5で到達率8.78%, 基準3.64%)。D1は到達率0.68%で大化け母集団でない

**■ cfs9 非D1×vol急増 + TP/SL執行**
- 母集団=非D1×vol急増、+30%タッチ利確+緩いSL。全9セルEVマイナス(最良vr2/SL20%でEV-0.687%)
- tp_rate 5-8%のみ、hold_rate81-88%→大化け1割未満が保有負け9割に食われる。TP執行でも成立せず

**■ cfs10 既存2.887x戦略にH4e下落回避フィルタ**
- フィルタなし(外挿mult4.311x,n111) vs D5除外(mult0.97x,n37) vs D4以上除外(mult0.91x,n33)
- H4e除外でn111→37激減・mult崩壊。既存gap戦略の勝ちトレードの2/3が高dip銘柄=H4eと水と油
- ★ここで「4.311x」がnone modeで再現→前任の2.887x集約平均との食い違い発覚→cfs11で真値確定へ

**■ cfs11 正式複利sim (※2.062xは後にバグ判明)**
- 既存全multは(1+R)^N16外挿と判明。event駆動simで真mult mp=1 2.062x と出力 → だが後述cfs13でこのsimのバグ判明
- mp2以上は複利破壊(mp2=0.031x,mp3+全損)は正しい(資金集中投下で負け直撃)

**■ cfs12 緩いSL最適化 (SL逆効果)**
- 既存最良cellに緩いSL。確定畳みsimでSL=none 1.141x / -20% 0.74x / -15% 0.76x / -10% 0.37x / -8% 0.20x
- SL全て真mult低下=逆効果。SLは勝ちトレードの一時下落も切り回復を取り逃す。SL発動率↑でmult悪化
- ★SL=noneが1.141xでcfs11の2.062xと不一致 → sim実装の食い違い発覚 → cfs13で決着

**■ ★cfs13 sim決着 (現在地 1.141x 最終確定)**
- cfs11(2.062x)とcfs12(1.141x)を同一トレード列・同一scriptで突合
- 真因: cfs11のevent駆動simがidx管理バグ(cfs13再現でmult=1.000と破綻)。確定畳み(全額逐次)=1.141xが正
- 数字変遷 2.887→4.311→2.062→1.141 に終止符。真の現在地1.141x、10xまで8.76倍不足

**■ cfs14 trailing exit (exit軸も尽きた)**
- 既存cellシグナル+trailing(trail5/8/10/15%×maxhold10/20/40)。fixed対照=1.141x再現(整合OK)
- trailing全12セル0.46x以下、net全マイナス。gap急騰銘柄はentry直後ピーク→固定短期exitが最適
- exit軸(SL下/trailing上)両方向で1.141x超えられず

**■ cfs15 平均回帰(売られすぎ反発)素性確認 — 不成立**
- ret5(直近5日リターン)分位 × trend(20日MA上下) × hold で素のnet予測力を層別(全銘柄, merged数百万)
- ★全層EVマイナス。売られすぎ(ret5 Q1)に反発edge無し。UP×Q1(上昇中の押し目買い)が最悪(-0.67〜-0.95%)
- ret5分位単調性も逆/無し: 売られすぎほどEV高くない。日本株個別は「下げたものは続落」が支配的
- cfs6c(決算急落も反発せず)と整合。逆張り平均回帰は日本株個別短期で不成立と確定
- ★今日の総括: 価格時系列次元でnetプラスedgeは順張りモメンタム(1.141x)のみ。別情報次元が次の課題

---

## 6. 最新 ML 数値 (既存体制 trusted 31,340 cells)

### mult 分布
- mult >= 10x/5x/3x: **0 件** / mult >= 2x: 196件(0.63%) / >= 1.5x: 1,816件(5.87%) / >= 1.0x: 4,639件(14.99%)

### TOP cell (既存体制)
- ★mult記述は全て外挿値で過大。同cellの正式複利sim真mult=2.062x(mp=1, cfs11)が真値
- cell: gap=0.065、p1_up=0.02、p1_dn=-0.06、ext=4、universe=4000-7000、HIGH20、n=111、wr0.523
- edge は 1点でなく zone として存在 (gap=0.065 × ext=4 × universe=4000-7000 周辺)
- 31,340 trusted cellのmult分布(>=10x/5x/3x:0件 等)も全て外挿値→正式simでは更に低い見込み

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
- 2026-06-02 v1.3 cfs8反映 (ARK全文更新)
  - ★仮説反転: 大化け母集団はD1(低dip)でなく非D1(高dip)×vol急増。D1大化け仮説は棄却
  - 次アクション優先1を「非D1×vol急増のTP執行戦略」に更新
- 2026-06-02 v1.4 cfs9-11反映 (ARK全文更新) ★現在地の根幹修正
  - cfs9 非D1×vol TP執行もEVマイナス、cfs10 H4e×既存戦略は水と油でH4e系打ち止め
  - cfs11: 正式複利sim真mult=2.062x(mp=1) ※後にこのsimのバグ判明(v1.5で訂正)
  - mp並列は複利破壊と確定。評価軸を外挿→正式複利simに切替
- 2026-06-02 v1.5 cfs12-13反映 (ARK全文更新) ★★現在地 最終確定
  - cfs12 緩いSLは全て逆効果、cfs13でcfs11 simバグ判明し真mult=1.141x確定
  - 数字変遷 2.887→4.311→2.062→1.141 に終止符
- 2026-06-02 v1.6 cfs14反映 (ARK全文更新) ★exit軸決着
  - cfs14 trailing exitも悪化。exit軸は固定短期が最適。1.141xはモメンタムの証明された天井
- 2026-06-02 v1.7 cfs15反映 (ARK全文更新) ★価格時系列次元 一巡
  - cfs15 逆張り平均回帰は全層EVマイナス(日本株個別は続落支配)
  - ★価格時系列次元を網羅探索完了: netプラスedgeは順張りモメンタム(1.141x天井)のみ
  - 優先1を「価格時系列でない別の情報次元(ファンダ変化率・業種資金循環・信用残歪み等)」に更新
