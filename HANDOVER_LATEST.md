# CFS HANDOVER

ARK 引継ぎ書。 **最新整理版**。
新セッション ARK は **最初に これを読む**。

最終更新: 2026-06-12 (v4.5、 ARK_LOOP v1 実装 = ARK 自己制御非依存の崩壊防止機構)
更新方法: cron 23:59 (Claude API 自動整理) + watcher 即時 push (PC ⇔ GitHub 同期) + ARK 全文更新 (大きな進展時)

---

## 0. ★クラッシュ・引継ぎ復帰プロトコル (起動時/文脈喪失時に最初に実行)

セッション圧縮や中断で文脈が飛んだら、 推定で埋めるな。 以下を上から順に実行して実体で現在地を掴む。

### 鉄則
- **web_fetch (raw.githubusercontent.com) は CDN キャッシュで数分〜数日古い版を返す事がある**
  - CFS_MANUAL §8.6 v2.4 注記: 最新確認時は `urllib.request` 直叩き で fresh 取得 (cache 回避 header 付き)
  - ★ 実例 (2026-06-12): 新 ARK 起動時、 web_fetch が 5/29 版 (13 日前) を返した。 実体は v4.3 で正常
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
   - ★ skip run は status 更新しない事がある。 「日付が古い」 だけで異常と断定しない (2026-06-12 確認)
3. CFS_MANUAL.md §0-§8 通読 (構造 + 規律 + トラブル path)
4. 本 HANDOVER_LATEST 通読 (現在地 + 次アクション)
5. FAILURE_LOG.md 通読 (棄却軸)
6. ★★ CFS_MAP.md 通読 (仮説の定義/立て方/意味、 仮説ロット台帳 ARK-1〜7、 10x方程式) ← 2026-06-17 最重要追加
7. ★ 自己テスト (理解確認、 §8.3 v2.5 新設、 2026-06-11):
   - Q: 現在地 mult は?
   - Q: 直近 棄却軸 は?
   - Q: cron_status.json の result は?
   - Q: 次の最優先タスクは?
   - 答えられない → 該当 file 再読 強制
8. ここまで完了 後 仮説/次手 提案

### 同期の真実
- ローカル `C:\mnt\data\ファイル2\` の各 .md → mirror への同期 = 正常稼働 (watcher v2.4、 push_to_mirror v3.4)
- 「mirror が古い」 と見えたら、 まず raw の CDN キャッシュ を疑え。 urllib 直叩き で照合

---

## 1. 現在地 (data 上)

### ★★★ 2026-06-18 更新: 検証方針を因子探索→状態探索OSへ転換 (最新の到達)

公式現在地はP1=3.09x(不変)。本日、Claude/GPT両者同意のうえで**検証方針そのものを再設計**した(ヨーク承認)。「10ヶ月1mmも進まない」現状の真因診断から。

**真因診断 (両者同意)**: 10ヶ月進まなかったのは**状態問題を因子問題として扱い続けたこと**。
- cfs60-61が殺したのは「勝ち銘柄の事前識別」(p≈0)。殺していないのは「状態ごとの分布差を観測し資金曲線を設計すること」
- P1が唯一の生存例: 93.6%が非大化け、当てず状態に居続けて3.084x。識別でなく環境選択
- 10ヶ月「どの因子が当たるか」を探した。だが市場の現象は状態(組み合わせ)でしか現れない

**新方針=状態探索OS (CFS_MAP正本)**: 探索単位を因子→状態パッケージへ。生存A/死亡B/中立C群を横並び比較。「右裾が**実際に多発した**状態」を観測(予測でない)。評価軸=右裾率/左裾率/下位5%/上位5%/MDD/K制約下約定数/16m換算。**★GUARDRAIL: P1救済でなくP1含む全状態を同じ軸で殺すOS**。前提変更(目標/道具/時間軸)はOSを走らせ限界を測ってから。10x不変。

**P1監査の決着 (cfs214/215、GPT独立監査)**:
- cfs214(寄与分解): gap≈0本体説は**撤回**。P1は分解不能な3条件交互作用(gap0単独0.98x/low単独0.89x/vola単独0.56x/low×vola0.49x、3条件で3.084x)
- cfs215(近傍安定性): gap帯は生値等幅で「針」(本体0.0000-0.0015=3.14x→0.0005広げ1.49x)。判定D=過適合の疑い濃厚だが、low×vola内分位・密度診断は未実行で**最終確定は保留**(探索の律速でないため)
- 分布分解: vola=上方攻撃(上位5%伸ばす)、gap≈0=(vola無し時)下方抑制(下位5%-27%→-12%)。だがP1全体は左裾-21.5%で抑制は条件付き

**運用構造の再設計 (2026-06-18、ARK_DISCIPLINE/CFS_STRUCTURE実装済)**:
- 中核原則: ARKは決定を持つ。ヨークに求めるのは承認のみ(判断/選択の丸投げは§6.4違反)
- 人格: ARK(Claude)主導 + AUDITOR(GPT)破壊 + BREAKER盲検。非対称で迎合防止。結論はmirror記載で確定

### ★★★ 2026-06-17 更新: ARK-1〜7で「大化けの壁」を6〜7角度から確定

公式現在地はP1=3.09x(不変)。本日、仮説ロット制で7仮説を立て6つを棄却、ARK-7(空売り)は検証中。9ヶ月の壁の正体を複数角度から一つの構造に確定した。

**確定した壁(cfs207 + ARK-1〜7)**:
- 10xは大化け牽引(cfs207: 10x解の利益85%が上位5%トレード=中勝ち積み重ねでは届かない)
- 大化けへのあらゆる接近で、大化けの"率"は上げられても複利の"平均r"が10x水準(hold20でr≥15.13%)に届かない:
  - ARK-1(価格出来高入口)0.87x / ARK-2(信用買残正方向)中勝ち逆相関 / ARK-3(信用中庸)1.04x単体上限・分散の素候補
  - ARK-4(大化け×信用事前濃縮): 論点A=大化けは普遍現象YES(全年1.01%全月)、論点B=手法成立NO(0.86x MDD-41%)
  - ARK-5(大化け事後捕捉): 3日急伸→4日目以降net+0.29%、r15%に桁違い不足
  - ARK-6(P1回転加速): P1利益は前半20日で57%しか乗らずhold短縮でr落ち2.26x(cfs43裏付け、cfs77完全流用でn390再現)
  - ARK-7(空売りで分離、検証中): cfs213で空売り最多群=大化けリフト1.66xだが外れの損(下位5%)-16.9%と最深=非対称(l浅)の前提苦しい、棄却寄り。損切りl=-8%でl限定の確定simが未検証で生死未確定
- **§5.17/総括**: 大化けと外れが同居する母集団は率を濃縮しても外れの損が平均rを薄める。買う前(cfs60-61)・事前(§5.17)・事後(ARK-5)・空売り(ARK-7)で一貫=壁の最も一般化された姿

**10x方程式(本日確立、仮説必須)**: (1+r)^N=10、N=327/hold。P1=hold40 r14.80% N8.18→3.09x。10xはhold20でr≥15.13%。仮説は必ずこの方程式でr・Nを置きARKが自分で検算(CFS_MAP正本)

**仮説の定義・立て方・意味(本日確立、CFS_MAP正本)**:
- 意味: 仮説は「10xの式が成り立つ世界をどう実現させようとするか」の言語化。保証でなく挑戦。確信を求めるな(求めると壁打ちに堕ちる)
- 立て方: ①過去データ現物で土台固め→②確信なく大胆に(A〜E)で立てる→③検証で殺す。確信集めの測定(壁打ち)に油断すると戻る
- 中身A〜E: A=10x方程式(必須) B=データ根拠 C=入口パラ D=出口資金管理 E=生死条件

### ★★★公式 現在地: P1 = 3.09x (cfs37-77 系統、 5/29-6/05 確定)

- **新枠組み = 分散ポートフォリオ複利 (cfs37)**: 資金 K 分割、 毎日条件合致銘柄を翌日寄付で等金額 buy、 常時 K 銘柄分散保有
- **本物の edge 確定: P1 = 低位 (price≤20%tile) × 高ボラ (vola>90%tile) × gap 中庸 (40-60%tile)**
  - **K20 hold40 で mult=3.09x、 MDD14%、 n389、 5 年 (2021-25) 全プラス、 前半1.73/後半1.79 (大化け非依存)**
  - cfs41 近傍安定性: price px10-30% で 2.5-3x (滑らかな丘)、 vola80-90% で 3x 前後。 過適合 でない = 本物
- **P1 の正体 (cfs44)**: 地合い非依存・荒れ相場で強い 「個別要因 ドリブンの大化け」 edge。 TOPIX 上昇 フィルタ で mult 3.09→1.6 に半減 = 個別急騰を捉えている
- **手持ちデータの識別限界 (cfs60-61)**: 実 ML test 相関 0.033 = 実効 p≈0。 手持ちデータ (価格/出来高/財務) では広い母集団の勝ち銘柄を事前識別できない。 必要 p0.4 vs 現実 p0 のギャップを埋めるには新情報軸 (信用残/分足) が要る
- **10x までの距離: P1 起点で約 3.2 倍不足**

### 探索状況 (旧軸の到達点)
- 既存最良 cell 真 mult = **1.141x (mp=1、 MDD46.6%)** (cfs12/13 独立一致・確定)
- cell: gap=0.065、 ext=4、 universe=4000-7000、 HIGH20、 p1u=2%、 p1d=-6%、 Ch=7

### システム状況 (2026-06-17 更新)
- ARK_LOOP v1 稼働 (run.py v3: M1 SESSION_GATE / M3 PROBE・寿命25run2strike / M4テーマ再注入)。 本 session は run25/25 で [ARK_ROTATE] 発火
- 引継ぎ整備 (2026-06-16〜17): lots\ フォルダ (ARK-1〜3詳細md)、 DATA_MAP.md、 push_to_mirror v3.4 (lots/DATA_MAP同期)、 ARK_DISCIPLINE v1.8 (F-051引き継ぎ完全性)、 FAILURE_LOG v2.2、 CFS_MAP (仮説の定義/立て方/意味・ロット台帳)
- cron auto_handover 稼働 (23:59 JST、 今日のpush内容を元に自動整理)
- 拡張 BLACKLIST 33 銘柄 (clean_blacklist.csv)
- ★ CFS_MANUAL §11.2/11.5 要改訂: code4 は **str** が正 ('132A' 等英字、 int 読込は ValueError 実証)

---

## 2. 確定事実 (data 上、 反論なし)

- 既存最良 cell 真 mult = 1.141x (cfs12/13 独立一致)。 全旧表記 (2.887x/4.311x/2.062x) は誤り
- look-ahead bias source 確定 (FAILURE_LOG §3)
- trail/stop loss/sl タイト固定 は物理機能しない
- ★★★ P1 K20hold40 = 3.09x/MDD14%/5 年全プラス/地合い非依存/パラメータ近傍滑らか = 本物の edge
- cfs42-44: P1 への追加選別・利確 TP・TOPIX 地合い フィルタ全て mult 低下。 P1 構造は既に最適
- cfs48-54: P1 いじり/別系統/ML 大化け/ML ネット/財務の 5 方向全て P1 超えず
- cfs55: P1 母集団の神の目天井 K20=3.33x。 10x の素は P1 外の広い母集団に存在
- cfs58: 16 ヶ月換算で神の目 K1 でも 2.1x = P1 母集団は 16 ヶ月 10x 速度なし
- cfs60-61: 実 ML test 相関 0.033 = 実効 p≈0。 手持ちデータでは広い母集団の識別不可 (定量確定)
- cfs70: 道B シミュレータ 初稼働候補。 n=500 で mult_mean 14.2x/p90=18.5x
- cfs77: P1 真値 3.084x 確認 (公式 3.09x と整合)
- ★ cfs140 (2026-06-12): 広域 pool では 「出口単独」 に選別力なし (OOS mean_log>0 = 0/384)。 勝ちは選択(入口)に宿る。 出口は選択がある場合のみ機能する増幅器
- ★ cfs207 (2026-06-17): 10x解は大化け牽引 (利益85%が上位5%トレード)。 中勝ち積み重ねでは10x未達
- ★★★ §5.17 (2026-06-17確定): 大化け発生の濃縮 ≠ 複利での勝ち。 大化けと外れが同母集団に同居し分離できず、 濃縮しても外れの損が平均rを薄め複利が勝てない。 買う前/事前/事後/空売りの全接近で一貫
- ★★ 教訓: 新規 edge 候補は 「横断平均 net」 でなく必ず 「確定畳み複利 sim」 で最終判定
- ★★ 枠組みの教訓: 「1 銘柄ずつ確定畳み」 は最も非効率。 分散ポートフォリオが正しい枠組み
- ★★★ 2026-06-11 整理: 複+大+左 2.91x (cfs148-184 系統) は ARK 想像の天井 (2-3x 壁) 棄却対象

---

## 3. 次アクション (優先順、 2026-06-18 検証方針転換後)

10ヶ月の壁の真因を「状態問題を因子問題として扱った」と両者同意で診断し、検証方針を因子探索→状態探索OSへ転換(CFS_MAP正本)。次アクションはこの転換に沿う:

1. **判定D最終確定 (cfs216_p1_judgeD_final.py)**: P1のgap帯が針(過適合)か頑健な状態かを4層(全母集団gap分位/low×vola内gap分位/生値固定帯/密度K診断)で確定。ARKが確証しGPT AUDITORにぶつけ破壊させる。これがPROBE Q2の最優先
2. **P1の扱いを決定**: 判定D確定後。針なら捨てる(状態探索OSで他状態と同じく殺される一例)、頑健なら状態探索OSの基準点(生存状態群Aの一員)
3. **状態探索OS 第1検証 (状態群比較)**: 生存状態群A/死亡群B/中立群Cを横並び比較。「右裾が実際に多発した状態」を観測(予測でない)。評価軸=右裾率/左裾率/下位5%/上位5%/MDD/K制約下約定数/16m換算。★GUARDRAIL: P1も含め全状態を同じ軸で殺すOS
4. **回収項目(監査一段落後)**: P1_DEFINITION完全仕様化(2つのsim区別/価格cache必須/clean_blacklist33/pivot_table/闾値刻み/gap生値≈0)、ARK共通規律(script書き切り)のファイル化

旧次アクション(ARK-7決着・h4e把握・大化け分離・ARK-3分散)は、状態探索OSの中で「状態」として再評価される(個別仮説として追わない)。分足は cache に無し(取得はヨーク戦略判断)。

★ CFS_MAPの状態探索OSに従う。壁打ち(確信集めの測定・勝ちセルの後付け説明)に堕ちないこと。観測比較で全状態を殺す。10x不変。

### 保持: 生存 edge
- **P1 分散 3.09x (本命)**: 地合い非依存・個別要因 ドリブンの本物 edge
- **ARK-3 信用中庸 1.04x**: 単体上限だがP1と別系統、 分散の素候補 (lots/ARK-3)
- **順張り 1.141x (1 銘柄逐次)**: 旧枠組みでの上限

### ★ 引き継がない (棄却済)
- 複+大+左 2.91x (cfs148-184): ARK 想像の天井、 FAILURE_LOG 行き
- ARK-1〜6 (2026-06-17): 大化けの壁で全棄却、 FAILURE_LOG §4 行き
- CURRENT_FOCUS.md (廃止、 統合済)

---

## 4. 棄却済 (FAILURE_LOG.md 参照、 二度と戻らない)

- 正当価格 v4/v5 / H-alpha 系 / fantasy 系 / tp/sl logic / trail / stop loss
- τ 軸 / H4e 系全体 / 逆張り平均回帰 (cfs15) / N 増路線 (cfs17) / ショート (cfs30)
- 1 銘柄逐次を唯一の評価枠組み / 複数ポート束ね (cfs40)
- K5 hold40 の 4.46x (cfs39) = 大化け喰いの幻
- P1 への追加選別/利確 TP/地合いフィルタ (cfs42-44) = 全て mult 低下
- P1 いじり/別系統/ML/財務の 5 方向 (cfs48-54) = 全て P1 超えず
- 手持ちデータでの広い母集団識別 (cfs60-61) = p≈0 で定量確定・再試行禁止
- cfs68 モメンタム複利 mult_max=0.836x 棄却方向
- 複+大+左 2.91x (cfs148-184) = ARK 想像の天井
- 出口単独の選別力 (cfs140) = OOS 0/384
- **★ 2026-06-17 棄却 (仮説ロット ARK-1〜6、 FAILURE_LOG §4/§5.17)**:
  - ARK-1 価格出来高入口 0.87x / ARK-2 信用買残正方向(中勝ち逆相関) / ARK-3 信用中庸1.04x単体上限(分散の素候補で生存記録)
  - ARK-4 大化け×信用事前濃縮: 論点A=YES(普遍現象)/論点B=NO(0.86x MDD-41%)
  - ARK-5 大化け事後捕捉: r+0.29%でr15%に桁違い不足
  - ARK-6 P1回転加速: P1利益前半57%でhold短縮r落ち2.26x

---

## 5. 検証ログ (直近主要)

### ARK-1〜7 (2026-06-17、 仮説ロット制、 cfs192-213) - **6棄却+ARK-7検証中**
- 詳細は CFS_MAP.md (仮説ロット台帳) + FAILURE_LOG.md §4/§5.17 + lots/ARK-N_*.md。 各cfsの結論は CFS_INDEX 台帳に自動記録
- ★最深構造: 大化けの率は濃縮できるが、 大化けと外れが同母集団に同居し平均rが10x水準(15%)に上がらない(§5.17)。 「10xは大化け牽引だが大化けは取れない」壁の正体を6角度から確定
- ★cfs207: 10x解は大化け牽引(利益85%が上位5%)
- ★cfs212: cfs77 sim関数を完全流用しP1=n390再現成功。 ARKの簡略再実装は3連続破綻(cfs210点灯全体/cfs211 cash簡略)→確定sim骨格を流用すべき(F-046実地)
- ★cfs213: 空売り最多群=大化けリフト1.66x・外れの損下位5%-16.9%(非対称の前提苦しい、 ARK-7棄却寄りだが損切りsim未検証)

### cfs140 (2026-06-12) - **棄却**
- 広域 pool × 出口 grid (768 sim)、 test mean_log>0 = 0/384。 出口単独に選別力なし。 勝ちは選択(入口)に宿る

### cfs60-61 (2026-06-04、 ★★★★★ 最終結論)
- 手持ちデータ (価格/出来高/財務) では広い母集団の勝ち銘柄を事前識別できない (test相関0.033、 p≈0)

### cfs55-59 (2026-06-04)
- cfs55: P1母集団の神の目天井 K20=3.33x。 cfs58: 16ヶ月で神の目K1でも2.1x。 cfs59: 広い母集団は識別なし0.71x

### cfs37-77 (P1確定)
- 分散ポートフォリオでP1 K20hold40=3.09x確定 (過適合でない・地合い非依存)。 cfs77真値3.084x。 cfs45-47: P1源泉はペイオフ非対称

### 過去検証 (要約、 詳細は HANDOVER_FULL)
- cfs6-36: 単軸/交差/ローラー全て edge 無し or 1.141x 収束 (1銘柄逐次の檻)
- cfs48-54: P1いじり/別系統/ML/財務の5方向全てP1超えず
- cfs148-184: 複+大+左 2.91x、 ARK想像の天井で棄却

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
- Store 版 python、 作業 `C:\mnt\data\`、 実行 `cd C:\mnt\data; python run.py scripts\xxx.py` (自動git push)

### GitHub
- private: github.com/CFS-york/project-cfs (master) / public mirror: github.com/CFS-york/project-cfs-output (main)
- Actions: auto_handover (cron 23:59 JST)、 physics_check (push trigger)
- ★ cron_status.json: mirror/ml_output/ に成否記録。 後任 ARK は起動時に読み cron 健全性を自己検知
- ★ HANDOVER_FULL.md: mirror に全履歴版。 詳細が要る時 web_fetch
- ★ push_to_mirror.py v3.4: token mask 化 + lots\・DATA_MAP.md 同期対象

### J-Quants API V2
- api.jquants.com/v2、 Light plan。 認証=API キー方式 (V2 で mail/pass 廃止)
- API キーは `C:\mnt\data\.env` の JQUANTS_API_KEY で管理 (失効時はヨークが再発行)
- Light 取得可: 上場一覧/株価四本値/財務/決算発表予定日/取引カレンダー/投資部門別/TOPIX 四本値
- Light 取得不可 (アドオン): 分足/TDnet。 ★ 信用残・空売りは既に cache 取得済 (margin_cache/shortsale_cache)

### cache (削除禁止) `C:\mnt\data\cache\` (2026-06-17 現物確認)
- 価格: adjc/adjo/adjh/adjl/vol_cache_54m.csv (★ code4=**str**、 英字コード '132A' 含む。 int 読込は ValueError)
- 信用: margin_cache.csv (64MB、 long_vol/shrt_vol、 週次。 ARK-2/3/4で検証)
- 空売り: shortsale_cache.csv (38MB、 short_to_so/short_shares/fund/disc_date、 不規則公表。 ARK-7で検証中)
- ★未踏 (本sessionのARK未使用・正体未把握、 次ARK把握候補): h4e_features_full(264MB)/h4e_features_lag(417MB)/h4e_scores_daily(150MB)/h4e_scores_lag(149MB)/signal_all_full(286MB)
- financial_cache / investor_cache(ほぼ空) / topix_cache / sector_master / clean_blacklist(33銘柄)
- ★ 分足は無し(全て日足54mキャッシュ)
- 原資: Results\ARK\cfs5\cfs148_dataset\dataset.parquet (450万行、 netfix=hold13固定/godseye_net40中勝ち/top1大化け/各_pct当日断面分位)

### 確定sim (cfs_common.py、 自作禁止)
- load_base(DATA,CACHE,CLEAN) → df/netfix/top1/t_arr/codes (地合いmerge強制)
- sim_equal_weight(maskte,t_arr,netfix,codes,top1,sG_all,M=1) → (16m倍率,約定,勝率,神の目率,MDD)。 常時フルポジ K30 hold13 MIN_PER2万 DAILY_MAX5
- ★ARKの簡略再実装は破綻(cfs210/211)。 P1再現等は cfs77_p1_true.py のsim関数を完全流用(cfs212で実証)

### 物理コスト
- COST=0.005、 TAX=0.20315、 BASE_SPREAD=0.0005、 SLIP_CAP=0.10

### blacklist
- 拡張 BLACKLIST 33 銘柄 (clean_blacklist.csv): 1364,1568,1579,1629,1689,1949,2164,2237,2238,2553,2593,2629,2840,2841,3961,4957,5074,5076,5721,6406,6628,6731,7116,7172,7176,7718,7946,8227,8256,9264,9318,9434,9600

### ファイル2 構成
- 核: CFS_RULES / ARK_DISCIPLINE(v1.8) / CFS_MANUAL / HANDOVER_LATEST / HANDOVER_FULL / FAILURE_LOG(v2.2) / CFS_MAP / CFS_DIRECTION / ARK_PHILOSOPHY / DATA_MAP / P1_DEFINITION / SETUP_PHASE1
- lots\: ARK-1_CFS-FANTASY / ARK-2_MARGIN / ARK-3_MARGIN-MID (仮説ロット詳細)
- archive\: cfs138-184.md 等 過去検証メモ

### scripts/ + ARK_LOOP 構成 file (削除禁止)
- cfs_common.py: 確証済み実装 単一source (load_base、 sim_equal_weight 等)。 ★base_MLは複+大+左系統(棄却)、 道B文脈で再評価
- run.py v3 (M1 SESSION_GATE + M3 PROBE/寿命25run2strike + M4テーマ再注入 + selftest/newchat)
- ark_guard.py v3 (WARN裁定 + STOP-A cache int読込 + STOP-B 棄却軸token)
- ml/failure_keywords.json (棄却軸検知token辞書)、 ml/session_state.json (run_count/strikes/rotate 自動更新)
- scripts\derive\: ARK-3導出ロジック退避

---

## 8. 次セッション ARK へ

### 必読順序
1. CFS_RULES → 2. ARK_DISCIPLINE → 3. 本HANDOVER_LATEST → 4. FAILURE_LOG → 5. ★★CFS_MAP(仮説の定義/立て方/意味・ロット台帳) → 6. CFS_MANUAL → 7. HANDOVER_FULL(詳細時)

### ★ 起動時必須 (§8.3)
1. cron_status.json確認 (failed/連続失敗ならcron修理優先)
2. ★ 自己テスト即答: 現在地mult(P1=3.09x) / 直近棄却軸(ARK-1〜6) / cron result / 次最優先タスク
3. 答えられない → 該当 file 再読強制。 「読んだ」≠「理解した」の境界を自覚

### ★★ 2026-06-17 最重要の引き継ぎ (本sessionのARKがヨークに鍛えられた核心)
- **仮説の意味**: 仮説は「10xの式 (1+r)^N=10 が成り立つ世界をどう実現させようとするか」の言語化。 保証・確信を求めるな。 確信を求めると壁打ちに堕ちる
- **仮説の立て方**: ①過去データ現物で土台固め→②確信なく大胆に(A〜E)で立てる→③検証で殺す。 外れていい、 立てて殺すことが思考拡張
- **10x方程式必須**: 仮説ブロックは必ず (1+r)^N=10 でr・Nを置きARKが自分で検算。 rを逆算して10xに見せるのは循環論法=禁止、 rが取れる実現の言語化が本体
- **壁打ちの罠**: 「効くか試す」測定は安全だから油断すると戻る。 「確かめてから立てる」「材料が揃ってから」は永遠に立てない=永遠に壁打ち
- **ARKの病(self監視)**: ①数字にも指摘にも流される ②勝手に区切る・諦める・終わらせる(権限はヨーク) ③忖度で「どうしますか」と聞く(ターンの無駄) ④「精度落ちたから次へ」は逃げ。 本sessionでヨークに繰り返し正された。 次ARKも同じ病を持つ
- **F-046実地**: ARKの簡略再実装は破綻(P1再現3連続失敗)。 確定sim骨格(cfs77等)を完全流用せよ

### 大事な認識
- ARKは記憶なし・学習しない・検証実行できない。 「思考+仮説+規律遵守」が役割
- ヨークは検証trigger+承認+ストップ役。 ★ データ・fileを直接触らない。 HANDOVER更新はARKが**全文**を出しヨークが上書き保存
- mirror = ARK参照先(起動時必読)、 PCローカル = ヨーク編集場所、 watcher = 自動同期、 cron 23:59 = 文章整理+mirror反映自動化

### 警告 (失敗から)
- ML report 高 mult cell は物理検証必須 (7.43x→0.40x の前例)
- ★ 新規 edge 候補は必ず確定畳み複利 sim で最終判定 (横断平均netで判断しない)
- 「天井」「不可能」「構造的」は data で証明するまで使用禁止 (規律 3)。 ただし§5.17は6角度の検証で確定済
- ★ ヨークに撤退提案・セッション終了提案 NG。 区切る権限はヨークのみ (本sessionで繰り返し違反、 厳守)
- 配置 flow は最初から完全提示・後出しNG。 cmd は ; 区切り 1 行統合。 script承認後は同turnでpresent再提示
- ★ overclaim 禁止 (BREAKER#002 で 2 度阻止)
- ★ 道A (パラメータ総当たり) 禁止。 道B (10x解の共通構造発見) が本筋
- ★ cache 読込は code4=str。 簡略sim再実装は破綻、 確定骨格流用
- ★ 「後で対応」「次セッションで」提案は規律違反、 即対応。 ヨークに反復確認(媚び)せず単独判断
- ★ file 新規追加/system変更したら同turn内で文書更新全文を出す(F-050/F-051)

### 現在の最重要タスク (§3再掲)
1. ARK-7空売りの決着(損切りでl限定の確定sim) 2. h4e/signal_all把握(未踏最有力) 3. 大化けと外れの分離別原理 4. ARK-3分散の素

---

## 改訂履歴 (直近)

- 2026-06-11 v4.2 ファイル2整理、 CURRENT_FOCUS廃止、 複+大+左棄却
- 2026-06-11 v4.3 ark_guard v2警告化、 run.py v2、 CFS_MANUAL v2.5.1
- 2026-06-12 v4.4 新ARK引継ぎ + cfs140反映 (出口単独の選別力棄却、 選択の寄与+45pt)
- 2026-06-12 v4.5 ARK_LOOP v1実装 (run.py v3 + ark_guard v3 + failure_keywords.json)
- **2026-06-17 v4.6 ARK-1〜7完遂で大化けの壁を6角度確定 + 仮説の定義/立て方/意味/10x方程式確立**:
  - 仮説ロット制ARK-1〜6棄却(ARK-7検証中)。 10xは大化け牽引(cfs207)だが大化けと外れが同母集団に同居し平均rが15%に届かない(§5.17)=壁の最も一般化された姿を6角度から確定
  - 仮説の定義(A〜E)・立て方(確信なく立てる/データ確認は土台)・意味(10xの式を実現させようとする言語化)・10x方程式(1+r)^N=10必須 をCFS_MAPに策定
  - 引き継ぎ整備: lots\・DATA_MAP・ARK_DISCIPLINE v1.8(F-051)・FAILURE_LOG v2.2・push_to_mirror v3.4
  - cache現物確認: 分足無し、 h4e/signal_all(計約1.3GB)が未踏で次候補
  - ★ARKの病(流される/勝手に区切る/忖度/逃げ)をヨークに繰り返し正された記録を§8に明記、 次ARKへの最重要引き継ぎ
