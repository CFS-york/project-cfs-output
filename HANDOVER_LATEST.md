# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-06-03 (v2.6)
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
- ★★cfs28で確定: 確定畳み複利simで生き残るnetプラスedgeは依然 edge1(順張り1.141x)のみ

### ★★最重要発見: 10xの的確定 + 逆張りは複利で壊滅(束ね不可)

**10xの的(cfs20)**: +30%を11回で10x。+30%大化けは1日117件実在(全銘柄日3.17%)。的は十分大きい。
- +20%なら16回(258件/日)、+15%なら21回(431件/日)。必要N≪実在件数
- 問題は「edgeが無い」でなく「大化け候補の事前識別力」だけ。ただし骨格問題(下記)が先決
- 探索目標: New Chapter Q3=「20日以内+30%動く銘柄の事前識別」

**逆張りgapdown反発の決着(cfs26→27→28)**:
- cfs26: gap<=-7%×寄り→3日後寄り = net+0.098% wr54%(横断平均)。今日唯一のnetプラスに見えた
- cfs27深掘り: 最良 gap<=-7%×hold10×高出来高 net+0.267% wr54.6% n7524。+0.5%超セルなし
- ★★cfs28 複利sim判定: 逆張りedge2を確定畳み複利に乗せると mult0.035x/net-3.27%/MDD96.5%で壊滅
  - cfs27の横断平均+0.267%と符号真逆。hold長い少回数edgeは逐次で拾うN(7522候補→95)が偏り序盤大負けで複利死
  - ★教訓: 「横断平均netプラス」≠「複利実行でプラス」。新規edgeは必ず確定畳み複利simで最終判定(cfs17に続き再確認)
- ★2edge束ね(順張り+逆張り)は無効と数字で確定。月次相関0.112と低いが、edge2が複利で壊滅する以上束ねる意味なし

**順張り×翌日寄付の完全枯渇(cfs25)**:
- 当日引けexit(寄り→引け)も全層net-0.6〜-1.0%、wr26-38%。翌日寄付=寄り天井確定
- precision路線(cfs24)も否定: past_big到達率lift6.08でもnetマイナス(-2.1%)。到達率≠収益性

### 重要 軸 (LightGBM importance gain TOP)
gap(23,129) / universe(20,813) / vol(12,381) / p1_dn(2,855) / ext(2,556)

### システム 状況
- Phase 1 自動引継ぎ system: 完全稼働
- ★cron auto_handover 復旧+自己検知ループ稼働(2026-06-03): handover_runnerをJSON→マーカー方式に、
  max_tokens16000、cron_status.json記録、起動時にARKがcron健全性を自己検知(CFS_MANUAL v2.3 §4/§8.3)
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
- cfs25: 当日引けexit(寄り→引け)も全層netマイナス・wr26-38%。順張り×翌日寄付は完全枯渇
- cfs26/27: gapdown反発は横断平均で弱プラス(最良net+0.267%)だが+0.5%未達
- ★★cfs28: 逆張りgapdown反発を確定畳み複利simに乗せるとmult0.035x/MDD96.5%で壊滅。横断平均netと複利実行は別物
- ★★2edge束ね(順張り+逆張り)無効。月次相関0.112と低いがedge2が複利で壊滅し束ね意味なし
- ★★教訓: 新規edge候補は「横断平均net」でなく必ず「確定畳み複利sim」で最終判定する(cfs17/28)

---

## 3. 次アクション (優先順)

### ★★最重要: 業種内相対強弱(cfs29) — 第3の軸
- 順張り(絶対モメンタム)でも逆張り(gapdown)でもない第3軸: 市場地合いを除いた銘柄固有の相対的強さ
- sector_master(cache)で業種分類 → 同業種内での相対リターンでシグナル生成。未検証
- ★cfs28の教訓を即適用: 芽が出ても横断平均でなく確定畳み複利sim(N111/1.141x assert)で最終判定
- 10xの的(+30%大化け)の事前識別に効くかも併せて見る

### 優先 2: 20日以内+30%事前識別(New Chapter Q3)— 骨格問題が先決
- cfs20で的確定。+30%を11回で10x、+30%は1日117件実在
- ★精度より先に骨格問題: cfs24/25確定「翌日寄付entry×順張り」骨格ではどんな識別子もnetマイナス
- 逆張り骨格(gapdown反発)も複利で壊滅(cfs28)。大化け識別を活かす執行骨格自体が未発見
- 起点: cfs8で非D1×vol急増が+30%捕捉率8.78%(基準2.4倍)。ただし骨格問題解決が先

### 優先 3: investor軸 / τ軸(低優先)
- investor軸: 週次・市場全体・183週で解像度不足。個別銘柄別フローが取れれば再検討
- τ軸: forecast_eps異期予想の疑い(真サプライズ定義未解決)。低優先

### system: HANDOVER 2ファイル分離(設計予定)
- 現状 HANDOVER_LATEST.md を ARK(詳細全文) と cron(圧縮) が奪い合う構造問題
- 案: HANDOVER_LATEST=cron圧縮active版(16KB,起動時必読) + HANDOVER_FULL=全履歴版(圧縮せず蓄積)
- handover_runner/push_to_mirror/CFS_MANUAL §8.3 の3点変更。cron安定確認後に設計

---

## 4. 棄却済 (FAILURE_LOG.md 参照、 二度と戻らない)

- 正当価格 v4/v5 (1.7x天井) / H-alpha系 / fantasy系
- tp/sl logic(slタイト固定) / ret5 trigger系(look-ahead) / trail / stop loss
- τ軸の素直な使い方(発表後ドリフト翌日寄付系)
- H4e D1(低dip)群を大化け母集団とする仮説(cfs8) / H4e系全体(cfs7-10)打ち止め
- mp(slot並列)でN増→mult増の発想 / (1+R)^N外挿mult式(netを過大評価)
- cfs11 event駆動複利sim(idxバグ、2.062x誤出力)
- 既存最良cellへのSL(-8〜-20%)・trailing exit。全て真mult低下
- 逆張り平均回帰(cfs15, 終値基準)。全層EVマイナス
- 価格時系列次元の探索全般(順張り以外netプラス無し)
- ファンダ変化率(op_accel/fcst_rev, cfs16)のnet edge
- 別universe N増(cfs17)。全netマイナス
- fractional betting単独(cfs19)。2つ目edge無しで1.141x超えず
- precision/到達率路線(cfs23/24)。到達率lift6.08でもnetマイナス
- 当日引けexit骨格(順張り×翌寄付、cfs25)。全層netマイナス・wr26-38%
- オーバーナイトプレミアム(引け→翌寄り、cfs26)。net-0.53% wr24%
- ★逆張りgapdown反発の複利実行(cfs28)。横断平均+0.267%でも確定畳み複利でmult0.035x壊滅。2edge束ねも無効

---

## 5. 検証ログ (直近5件)

### cfs28 2edge束ね検証 (2026-06-03) ★★横断平均net≠複利実行の決定的実例
- edge1(順張り1.141x/N111 assert通過) + edge2(逆張りgapdown反発) を確定畳み複利simで合算
- ★edge2単独: mult0.035x net-3.27% MDD96.5%で壊滅。cfs27の横断平均+0.267%と符号真逆
- ★合算も全パターン0.07〜0.18xで崩壊。月次相関0.112と低いがedge2が複利で死ぬので束ね無意味
- ★教訓: hold長い少回数edgeは逐次で拾うN(7522→95)が偏り序盤大負けで複利死。複利simで判定必須
- sim実装3度目の同型ミス(entry_t基準でN129)をassertが検出→sig_t基準(cfs19規則)に修正し再現

### cfs27 gapdown反発の深掘り (2026-06-03)
- gap深さ×保有日数×銘柄質の3軸グリッド。最良 gap<=-7%×hold10×高出来高 net+0.267% wr54.6% n7524
- +0.5%超セルなし。gap深いほどnet悪化(崩落)、反発は3-10日、出来高大ほど反発。横断平均では弱edge止まり

### cfs26 逆張り: gapdown反発 + オーバーナイトプレミアム (2026-06-03)
- gapdown反発: gap<=-7%×寄り→3日後寄り = net+0.098% wr53.98%(横断平均)。当日引けは全マイナス
- オーバーナイト(引け→翌寄り)はnet-0.53% wr24%で否定。反発は数日かけて起こる

### cfs25 当日引けexit骨格検証 (2026-06-03) ★順張り×翌寄りの完全枯渇確定
- 翌日寄付→当日引けも全層net-0.6〜-1.0%、wr26-38%。日中こそ下落の主戦場
- gap_t1 Q5(大窓開け翌日)net-0.863% wr28%。寄り=直近天井 → 逆方向(cfs26)へ

### cfs24 past_big群のnet期待値 (2026-06-03) ★precision路線の否定
- past_big Q5群を翌日寄付entry→固定hold+TP: 全exit netマイナス(Q5 hold20=-2.13%)
- 到達率lift6.08の正体は両方向ボラ。高到達率=高ボラ、上方向edgeでない

### 過去検証(要約)

- **cfs6-10 (2026-06-02)**: τ軸3段棄却。H4e dip予測力確認も大化けTP執行EVマイナス。H4e系打ち止め
- **cfs11/12/13 (2026-06-02)**: 真mult=1.141x確定。cfs11 simバグ判明。SLは全て逆効果
- **cfs14-17 (2026-06-02)**: trailing/逆張り平均回帰/ファンダ変化率 全edge無し。N増は質低下でmult崩壊
- **cfs18/19 (2026-06-02)**: fractional bettingも1.141x超えず。netプラスedge1つでは全額逐次最適
- **cfs20 (2026-06-02)**: 10xの的確定。+30%×11回で10x、1日117件実在。1.141x執着の沼を脱出
- **cfs21/22/23 (2026-06-03)**: 拡張BLACKLIST33確定。past_big +30%到達率lift6.08(cfs24でnet否定)

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
- Actions: auto_handover(cron 23:59 JST、★2026-06-03復旧+自己検知ループ)、physics_check(push trigger)
- ★cron_status.json: mirror/ml_output/ に成否記録。後任ARKは起動時に読みcron健全性を自己検知(CFS_MANUAL §8.3)

### J-Quants API V2
- api.jquants.com/v2、Light plan 60req/min、sleep 1.2s

### cache (削除禁止) `C:\mnt\data\cache\`
- price: adjc/adjo/adjh/adjl/vol_cache_54m.csv (★ code4 = **str**、英字コード'132A'含む)
- financial_cache.csv (csv単体、19列、code4=str、date=発表日)
- h4e_scores_daily.csv (371万行、date×code4、dip_score(0-1連続)、pred(SMOOTH/DIP))
- h4e_features_full.csv / investor_cache.csv (週次・市場全体) / sector_master / listed_info 等
- **clean_blacklist.csv** (33銘柄、既存scriptが自動読込)

### 物理コスト
- COST=0.005、TAX=0.20315、BASE_SPREAD=0.0005、SLIP_CAP=0.10

### blacklist
- ORIGINAL_BLACKLIST 14銘柄 + cfs21新規19銘柄 = **拡張BLACKLIST 33銘柄**
- 33銘柄: 1364,1568,1579,1629,1689,1949,2164,2237,2238,2553,2593,2629,2840,2841,3961,4957,5074,5076,5721,6406,6628,6731,7116,7172,7176,7718,7946,8227,8256,9264,9318,9434,9600

---

## 8. 次セッション ARK へ

### 必読順序
1. CFS_RULES.md → 2. ARK_DISCIPLINE.md → 3. 本HANDOVER → 4. FAILURE_LOG.md → 5. CFS_MANUAL.md → 6. SETUP_PHASE1.md
- ★起動時: mirror の ml_output/cron_status.json を確認。result=failed や連続失敗ならcron修理を最優先(§8.3)

### 大事な認識
- ARK は記憶なし・学習しない・検証実行できない。「思考+仮説+規律遵守」が役割
- ヨークは検証trigger+承認+ストップ役。LightGBMは数値集約+軸importance。Claude API(cloud)がHANDOVER整理+physics check自動化

### 警告 (失敗から)
- ML report高mult cellは物理検証必須(7.43x→0.40xの前例)
- ★新規edge候補は「横断平均net」で判断せず必ず確定畳み複利sim(N111/1.141x assert)で最終判定(cfs28)
- sim実装は検証済骨格(sig_t基準accept)を流用。新規実装はassert強制+最小ケース検証(cfs11/18/28で3度同型ミス)
- 「天井」「不可能」「構造的」はdataで証明するまで使用禁止(規律3)
- ヨークに撤退提案NG。セッション終了をARKから提案しない
- 配置flowは最初から完全提示、後出しNG。cmdは;区切り1行統合
- §6.3 ヨーク操作=上書き保存のみ、手作業編集させない([HANDOVER ADD]差分貼付け方式は使わない)
- §6.4 自分で答えを知っている事をヨークに聞くな。確認は真の分岐のみ
- system修正は実ファイル確認後(log推定診断NG、F-040)。新script前にcache実構造を確認cmdで確認

### 現在の最重要タスク
1. **cfs29**: 業種内相対強弱(sector_master)。第3の軸。横断平均でなく複利simで判定
2. 育たなければ別骨格へ。大化け識別を活かす執行骨格自体が未発見(順張り枯渇・逆張り複利壊滅)
3. system: HANDOVER 2ファイル分離の設計(cron安定確認後)

---

## 改訂履歴 (直近10版)

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
- 2026-06-03 v2.5 cfs26反映: 逆張りgapdown反発に微かな芽(net+0.098% wr54%)
- 2026-06-03 v2.6 cfs27/28反映: ★★逆張りは複利で壊滅(横断平均+0.267%→複利0.035x)・2edge束ね無効・
  「横断平均net≠複利実行」教訓確定・cron復旧+自己検知ループ・次はcfs29業種内相対強弱
