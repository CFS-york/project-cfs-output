# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-06-03 (v2.5)
更新方法: cron 23:59 (Claude API 自動整理) + watcher 即時 push (PC ⇔ GitHub 同期) + ARK 全文更新 (大きな進展時)

---

## 1. 現在地 (data 上)

### 探索 状況
- ★★**現在地 最終確定: 既存最良cellの真mult = 1.141x (mp=1, MDD46.6%)**
  - cell: gap=0.065、ext=4、universe=4000-7000、HIGH20、p1u=2%、p1d=-6%、Ch=7
  - **真の達成率 11.4%、10xまで約8.76倍不足**
  - 数字変遷(全て誤り→真値): 2.887x→4.311x→2.062x(simバグ)→**1.141x(確定)**
  - 確定根拠: 確定畳みsim(cfs12)とcfs13が独立に1.141x一致
- exit軸(SL下/trailing上)・mp並列・entry側全軸・betting・N増、全て尽きた。1.141xは証明された天井
- ★1.141xは"小さく薄く勝つ"の的。10xは"+30%級を11回当てる"全く別の的

### ★★最重要発見: 10xの的確定 + 逆張りに微かな芽

**10xの的(cfs20)**: +30%を11回で10x。+30%大化けは1日117件実在(全銘柄日3.17%)。的は十分大きい。
- +20%なら16回(258件/日)、+15%なら21回(431件/日)。必要N≪実在件数
- 問題は「edgeが無い」でなく「大化け候補の事前識別力(precision)」だけ
- 探索目標確定: New Chapter Q3=「20日以内+30%動く銘柄の事前識別」

**逆張りgapdown反発(cfs26)**: 今日20本で唯一のnetプラス
- gap<=-7% × 寄り買い→3日後寄り = net+0.098% wr53.98%(n12,277)
- 当日引けexitは全マイナス→反発は数日かけて起こる
- オーバーナイトプレミアム(引け→翌寄り)はnet-0.53% wr24%で否定
- ★net+0.098%は弱い(コスト割れすれすれ)。だがwr53%超は順張りに無い性質+方向性は明確
- 次: gap深さ(-10/-15/-20%)×保有日数(1-10日)×銘柄質でnet+0.5%以上に引き上げ(cfs27)
- 育てば1.141xと別系統の2つ目edge → cfs19のbettingで束ねて複利向上。§5.2 飛びつかない

**順張り×翌日寄付の完全枯渇(cfs25)**:
- 当日引けexit(寄り→引け)も全層net-0.6〜-1.0%、wr26-38%。翌日寄付=寄り天井確定
- precision路線(cfs24)も否定: past_big到達率lift6.08でもnetマイナス(-2.1%)。到達率≠収益性

### 重要 軸 (LightGBM importance gain TOP)
gap(23,129) / universe(20,813) / vol(12,381) / p1_dn(2,855) / ext(2,556)

### システム 状況
- Phase 1 自動引継ぎ system: 完全稼働
- CFS_MANUAL v2.2 反映済 (code4 dtype 訂正)
- 拡張BLACKLIST33銘柄確定(clean_blacklist.csv)

---

## 2. 確定事実 (data 上、 反論なし)

- 既存軸(gap×ext×universe×p1×HIGH20)周辺探索の上限≈2.887x(外挿)、真mult=1.141x
- look-ahead bias source 確定 (FAILURE_LOG §3)
- trail/stop loss/slタイト固定は物理機能しない
- 旧体制(正当価格 v4/v5)は1.7x天井で棄却済
- τ軸の素直な使い方はedge無し(発表後ドリフトを翌日寄付で取る系)
- H4e dip_scoreは予測力あり(分位でEV単調減、各n約70万)。ただしH4e系全体は打ち止め
- ★★真mult=1.141x(mp=1,MDD46.6%)。確定畳みsim cfs12/cfs13独立一致。10xまで8.76倍不足
- 全mult表記(2.887x/4.311x/2.062x)は誤り。真値は1.141x
- exit軸決着: SL(下方向)もtrailing(上方向)も全て真mult低下。固定短期exitが最適
- 逆張り平均回帰(cfs15)は全層EVマイナス。日本株個別は続落支配
- 価格時系列次元ではnetプラスedgeは順張りモメンタムのみ
- ファンダ変化率(op_accel/fcst_rev, cfs16)も素のnet edge無し
- 構造的洞察: 「シグナル後に翌日寄付で素直に入る」は全次元でedge無し。例外はgap急騰モメンタム短期のみ
- N増路線(cfs17)否定: N111にマイナス23個混入でmult1.141x→0.27x崩壊
- betting軸決着(cfs18/19): netプラスedge1つでは全額逐次が複利最大。分散は2つ目edgeが要る
- 核心: netプラスedgeは4000-7000 gap急騰top1の1つだけ。betting/N増/exit/mpは2つ目edge無しで無力
- ★拡張BLACKLIST33銘柄確定(既存14+cfs21新規19)。clean_blacklist.csvに保存
- past_big +30%到達率lift6.08だがnetマイナス(-1.7〜-2.1%)。到達率=両方向ボラ、上方向edgeでない(cfs24)
- precision/到達率路線は否定。大化け+30%は観測時すでに高値圏→翌日寄付entryは下げる
- ★★cfs25: 当日引けexit(寄り→引け)も全層netマイナス・wr26-38%。順張り×翌日寄付は完全枯渇
- ★cfs26: gapdown反発(gap<=-7%→寄り→3日後寄り)がnet+0.098% wr53.98%=今日唯一のnetプラス
- オーバーナイトプレミアム(引け→翌寄り)否定。反発は数日かけて起こる

---

## 3. 次アクション (優先順)

### ★★最重要: gapdown反発の深掘り(cfs27) → 2つ目edge候補へ
- 現状: gap<=-7%×3日後寄り = net+0.098% wr53.98%。弱すぎる(コスト割れすれすれ)
- 目標: net+0.5%以上に引き上げ → 1.141xと別系統の2つ目edge
- 深掘り方向:
  - (A)ギャップ深さ拡張(-10/-15/-20%)で過剰反応をより厳選
  - (B)保有日数最適化(1-10日)。反発は数日かけて起こる
  - (C)銘柄質フィルタ(出来高/価格帯/ボラ)
  - (D)寄り→引けは負けるので「寄り買い→数日後寄りexit」固定
- ★§5.2 飛びつかない。past_big(到達率lift6でもnet否定)の轍を踏まない。netで判定
- 育たなければ: 業種内相対強弱ロード等さらに別軸へ

### 優先 2: 20日以内+30%事前識別(New Chapter Q3)— 骨格問題が先決
- cfs20で的確定。+30%を11回で10x、+30%は1日117件実在
- ★精度より先に骨格問題: cfs24/25確定「翌日寄付entry×順張り」骨格ではどんな識別子もnetマイナス
- 骨格として有効な候補: gapdown反発(cfs27で検証中)が育てば、大化け候補識別×逆張り骨格の組合せも検討
- 起点: cfs8で非D1×vol急増が+30%捕捉率8.78%(基準2.4倍)。だし骨格問題解決が先

### 優先 3: investor軸 / τ軸(低優先)
- investor軸: 週次・市場全体・183週で解像度不足。個別銘柄別フローが取れれば再検討
- τ軸: forecast_eps異期予想の疑い(真サプライズ定義未解決)。低優先

---

## 4. 棄却済 (FAILURE_LOG.md 参照、 二度と戻らない)

- 正当価格 v4/v5 (1.7x天井) / H-alpha系 / fantasy系
- tp/sl logic(slタイト固定) / ret5 trigger系(look-ahead) / trail / stop loss
- τ軸の素直な使い方(発表後ドリフト翌日寄付系)
- H4e D1(低dip)群を大化け母集団とする仮説(cfs8)
- H4e系全体(cfs7-10)打ち止め。既存gap戦略と水と油
- mp(slot並列)でN増→mult増の発想
- (1+R)^N外挿mult式(netを過大評価)
- cfs11 event駆動複利sim(idxバグ、2.062x誤出力)
- 既存最良cellへのSL(-8〜-20%)・trailing exit。全て真mult低下
- 逆張り平均回帰(cfs15)。全層EVマイナス
- 価格時系列次元の探索全般(順張り以外netプラス無し)
- ファンダ変化率(op_accel/fcst_rev, cfs16)のnet edge
- 別universe N増(cfs17)。全netマイナス
- fractional betting単独(cfs19)。2つ目edge無しで1.141x超えず
- precision/到達率路線(cfs23/24)。to達率lift6.08でもnetマイナス
- 当日引けexit骨格(順張り×翌寄付、cfs25)。全層netマイナス・wr26-38%
- オーバーナイトプレミアム(引け→翌寄り、cfs26)。net-0.53% wr24%

---

## 5. 検証ログ (直近5件)

### cfs26 逆張り: gapdown反発 + オーバーナイトプレミアム (2026-06-03) ★今日唯一netプラス
- gapdown反発: gap<=-7%×寄り→3日後寄り = net+0.098% wr53.98%(n12,277)。当日引けは全マイナス
- オーバーナイト(引け→翌寄り)はnet-0.53% wr24%で否定。反発は数日かけて起こる
- ★弱いが方向性明確。gap深さ×保有日数×銘柄質でnet+0.5%以上を目指す(cfs27)

### cfs25 当日引けexit骨格検証 (2026-06-03) ★順張り×翌寄りの完全枯渇確定
- 翌日寄付→当日引けも全層net-0.6〜-1.0%、wr26-38%。日中こそ下落の主戦場
- gap_t1 Q5(大窓開け翌日)net-0.863% wr28%。寄り=直近天井で数日も日中も必ず下げる
- ★残る方向=逆: 売られた寄り(gap_t1 Q1)が最もマシ → cfs26逆張りへ

### cfs24 past_big群のnet期待値 (2026-06-03) ★precision路線の否定
- past_big Q5群を翌日寄付entry→固定hold+TP: 全exit netマイナス(Q5 hold20=-2.13%)
- 到達率lift6.08の正体は両方向ボラ。高到達率=高ボラ、上方向edgeでない

### cfs23 +30%大化けの単一特徴リフト探索 (2026-06-03)
- 基準到達率2.96%。past_big Q5=17.99% lift6.08、vola20 lift2.57、range20 lift2.47、price低位 lift1.88
- 到達率高いが収益性は別(cfs24で否定)。教訓: 到達率≠収益性

### cfs21/22 拡張BLACKLIST確定 (2026-06-03)
- 始値→高値異常(H/O>3x)=17,282件。anom_any>=3で新規19銘柄検出
- 既存14+新規19=33銘柄をclean_blacklist.csvに保存。既存script自動適用

### 過去検証(要約)

- **cfs6/6b/6c (2026-06-02)**: τ軸3段とも棄却。全セルEVマイナス。発表翌日entry=旨味出尽くし後
- **cfs7/8 (2026-06-02)**: H4e dip_score予測力確認(D1-D5単調減)。大化け母集団は非D1×vol急増(捕捉8.78%)
- **cfs9/10 (2026-06-02)**: 非D1×vol TP執行もEVマイナス。H4e×既存戦略は水と油。H4e系打ち止め
- **cfs11/12/13 (2026-06-02)**: 真mult=1.141x確定。cfs11 simバグ(idx管理)判明。SLは全て逆効果
- **cfs14/15 (2026-06-02)**: trailing exit全悪化。逆張り平均回帰は全層EVマイナス
- **cfs16/17 (2026-06-02)**: ファンダ変化率もnet edge無し。N増は質低下でmult崩壊(1.141x→0.27x)
- **cfs18/19 (2026-06-02)**: fractional bettingも1.141x超えず。netプラスedge1つでは全額逐次最適
- **cfs20 (2026-06-02)**: 10xの的確定。+30%×11回で10x、1日117件実在。1.141x執着の沼を脱出

---

## 6. 最新 ML 数値 (既存体制 trusted 31,340 cells)

### mult 分布
- mult >= 10x/5x/3x: **0件** / >= 2x: 196件(0.63%) / >= 1.5x: 1,816件(5.87%) / >= 1.0x: 4,639件(14.99%)
- ★これら外挿値。正式複利simでは更に低い見込み(TOP cellの真mult=1.141x)

### TOP cell (既存体制、全て外挿値)
- cell: gap=0.065、p1_up=0.02、p1_dn=-0.06、ext=4、universe=4000-7000、HIGH20、n=111、wr0.523
- edge は 1点でなく zone として存在 (gap=0.065×ext=4×universe=4000-7000 周辺)

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
- h4e_scores_daily.csv (371万行、date×code4、dip_score(0-1連続)、pred(SMOOTH/DIP))
- h4e_features_full.csv / investor_cache.csv (週次・市場全体) / sector_master / listed_info 等
- **clean_blacklist.csv** (★2026-06-03新規: 33銘柄、既存scriptが自動読込)

### 物理コスト
- COST=0.005、TAX=0.20315、BASE_SPREAD=0.0005、SLIP_CAP=0.10

### blacklist
- ORIGINAL_BLACKLIST 14銘柄 + cfs21新規19銘柄 = **拡張BLACKLIST 33銘柄**
- 33銘柄: 1364,1568,1579,1629,1689,1949,2164,2237,2238,2553,2593,2629,2840,2841,3961,4957,5074,5076,5721,6406,6628,6731,7116,7172,7176,7718,7946,8227,8256,9264,9318,9434,9600

---

## 8. 次セッション ARK へ

### 必読順序
1. CFS_RULES.md → 2. ARK_DISCIPLINE.md → 3. 本HANDOVER → 4. FAILURE_LOG.md → 5. CFS_MANUAL.md → 6. SETUP_PHASE1.md

### 大事な認識
- ARK は記憶なし・学習しない・検証実行できない。「思考+仮説+規律遵守」が役割
- ヨークは検証trigger+承認+ストップ役。LightGBMは数値集約+軸importance。Claude API(cloud)がHANDOVER整理+physics check自動化

### 警告 (失敗から)
- ML report高mult cellは物理検証必須(7.43x→0.40xの前例)
- 「天井」「不可能」「構造的」はdataで証明するまで使用禁止(規律3)
- ヨークに撤退提案NG。セッション終了をARKから提案しない
- 配置flowは最初から完全提示、後出しNG。cmdは;区切り1行統合
- §6.3 ヨーク操作=上書き保存のみ、手作業編集させない
- §6.4 自分で答えを知っている事をヨークに聞くな。確認は真の分岐のみ
- 新script前に必ず使うcacheの実構造を確認cmd(全範囲dtype+英字混入check)で確認

### 現在の最重要タスク
1. **cfs27**: gapdown反発の深掘り(gap深さ×保有日数×銘柄質)。net+0.5%以上に育てば2つ目edge
2. net+0.5%達成後: cfs19 bettingで1.141x×逆張りedgeを束ねる複利計算
3. 育たなければ業種内相対強弱等さらに別骨格へ

---

## 改訂履歴 (直近10版)

- 2026-05-28 v1.0 初版
- 2026-05-29 v1.1 Phase1完成反映
- 2026-06-02 v1.2 τ軸3段棄却・investor軸保留・H4e予測力確認・環境スキーマ訂正
- 2026-06-02 v1.3 cfs8反映: 大化け母集団はD1でなく非D1×vol急増と仮説反転
- 2026-06-02 v1.4 cfs9-11反映: H4e系打ち止め・正式複利sim導入(※cfs11バグは後判明)
- 2026-06-02 v1.5 cfs12-13反映: ★★真mult=1.141x最終確定・SL逆効果確定
- 2026-06-02 v1.6 cfs14反映: trailing exit全悪化・exit軸決着
- 2026-06-02 v1.7 cfs15反映: 逆張り平均回帰全層EVマイナス・価格時系列次元一巡
- 2026-06-02 v1.8 cfs16反映: ファンダ変化率不成立・「翌日寄付で素直に入る」全次元でedge無し確定
- 2026-06-02 v1.9 cfs17反映: N増路線否定・別universe全netマイナス
- 2026-06-02 v2.0 cfs18/19反映: betting軸決着・netプラスedge1つでは全額逐次最適
- 2026-06-02 v2.1 cfs20反映: ★★発想転換・10xの的確定(+30%×11回、1日117件実在)
- 2026-06-03 v2.2 cfs21-23反映: 拡張BLACKLIST33確定・past_big到達率lift6.08(net否定予告)
- 2026-06-03 v2.3 cfs24反映: precision路線否定・到達率lift6でもnetマイナス
- 2026-06-03 v2.4 cfs25反映: 順張り×翌寄りの完全枯渇確定
- 2026-06-03 v2.5 cfs26反映: ★逆張りgapdown反発に微かな芽(net+0.098% wr54%)・次はcfs27深掘り