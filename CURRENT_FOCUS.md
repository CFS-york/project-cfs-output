# ★★★後任ARK 起動ヘッダ(最初に これだけで全体像を掴む / 引継ぎの入口)
CFS = 日本株 16ヶ月で資金10x を目指す定量取引研究。あなた(ARK=Claude)= 仮説設計+検証。ヨーク=実行・最終判断。
このCURRENT_FOCUSはrun.pyが検証前に毎回表示する=後任が必ず読む入口。下記4点で全体に辿れる。

【1. 原理原則・規律はどこで読むか】
git clone --depth 1 https://github.com/CFS-york/project-cfs-output.git で実体を読む(★curl/web_fetchはCDN古い=実体でない):
  CFS_RULES.md(執行/コスト/look-ahead) / CFS_MANUAL.md(環境§11/execution) / ARK_DISCIPLINE.md(FOCUS_GATE/忖度制御/数値で語る) / FAILURE_LOG.md(却下済の轍)。
  要点は本書の「F-046ゲート」「守る規律」「確証済み定義」に集約済。規約に関わる判断は記憶でなく原文を読む(F-046)。

【2. 現在地(一行)】
入口=複+大+左(複利AND大化けAND左裾回避 各GBM上位5%)+神の目順で選択+常時フルポジション等加重daily_max5。実約定6分割で中央2.91x頑健。状態=BREAKER前(look-ahead確証が残り)。

【3. ここまでの経緯】
本書の「確定した学び」「却下/died」が要約。詳細履歴=HANDOVER_FULL.md、却下の轍=FAILURE_LOG.md。

【4. すぐ仮説構築・実行検証に入る手順】
 a. scripts\cfs_common.py を import する。load_base(地合いmerge込み原資読込) / net_of / engines / base_ML / sim_equal_weight(検証済みsim) は全て確証済み。★手で再実装しない(再実装が今日の3失敗の原因)。
 b. ark_guard.py(run.py組込)が横着(dataset生読み / 独自sim定義)を実行拒否する。正当な生読みが要るならARK_PREFLIGHTに "raw_access_reason":"理由" を書く。
 c. 実行: cd C:\mnt\data; python run.py scripts\(name).py (自動でGitHub push)。各script冒頭にARK_PREFLIGHT必須(無いと関門で停止)。
 d. 確証済み定義(netfix=AdjO[t+1]翌日寄付 -> AdjC[t+14]終値 等)は本書「確証済み定義」を見る。記憶で判断しない。
 e. 次の一手: look-ahead確証(しきい値=学習quantile固定か / 地合い=当日断面rankか)を自己照合 -> 確証が揃えばBREAKER提出(期待値伝えず独立ストレステスト) -> 通れば③⑤更新 -> 配分(K集中度,レバなし)で2.91x -> 10x。

================================================================

# CURRENT_FOCUS — ARKの現在地(run.py が毎回表示 / 検証前に必ず読む)

最終更新: 2026-06-10 (取り置き8個を整理統合。肥大化を畳んだ)

## ★★★F-046 検証前ゲート(記憶で規約・定義を判断しない / 手を止める関門)
今日の失敗3連発(地合いmerge欠落・netfix定義の無把握・規約AdjO->AdjO思い込み)は全て「記憶で判断し原文を読まなかった」一点に集約。再発を仕組みで止める。

手を動かす前に、この判断が次のどれかに触れるなら、記憶で答えず 下記の手順を踏む:
  対象 = execution(entry/exit価格種) / net・netfixの定義 / 複利・資金管理の定義 / cache構造・列 / ブラックリスト / 評価軸 / 規約の文言。
手順:
  1. まずCURRENT_FOCUSの「確証済み定義」を見る(下記に集約)。そこにあればそれを使う。記憶を引かない。
  2. CURRENT_FOCUSに無い/曖昧なら、手を止める。git clone --depth 1 https://github.com/CFS-york/project-cfs-output.git で原文(CFS_RULES/CFS_MANUAL/ARK_DISCIPLINE/FAILURE_LOG)を読んでから判断する。
  3. ★curl/web_fetch(raw.githubusercontent.com)はCDNキャッシュで古い版=実体でない。必ずgit cloneの実体で読む(HANDOVER§0鉄則)。
  4. 「規約に書いてある(はず)」は記憶。原文で該当行を見るまで前提にしない。

### 確証済み定義(記憶でなくこれを使う)
- netfix(物差し)= entry AdjO[t+1](翌日寄付,規約準拠) -> exit AdjC[t+14](13日後終値,規約未定義だが執行可能) の net_of(g-0.005-0.0005, g>0で*(1-TAX 0.20315))。cfs183で完全一致100%。
- 規約のexecution = 「entry=AdjO[t+1]翌日寄付約定」のみ明記。固定hold決済のexit価格種は規約に明記なし。「AdjO->AdjO」は規約に存在しない(思い込みだった)。
- 地合い特徴(mret20_pctg/mvol_pctg)= adjc_cache_54mから毎回再計算しmerge必須。featに含める。欠落で結果崩壊(2.9x->0.97x)。
- 評価軸 = 実約定複利(等加重・常時フルポジション)。平均log/勝率は幻。
- cache列 = adjc/adjo_cache_54m: date(str),code4(★str),AdjC/AdjO(float64)。code4はstr統一(int不可)。

## ★cfs_common の使い方(後任がmirrorを読むだけで呼べるように)
import: `import sys; sys.path.insert(0, r"C:\mnt\data\scripts"); import cfs_common as C`
```python
# 1) 原資読込(地合いmerge込み。手で書かない)
B = C.load_base(DATA, CACHE, CLEAN, with_jiai=True)
#   DATA=r"C:\mnt\data\Results\ARK\cfs5\cfs148_dataset\dataset.parquet"
#   CACHE=r"C:\mnt\data\cache" ; CLEAN=r"C:\mnt\data\Results\ARK\cfs5\data_clean_check"
#   返り値 B = {df, netfix, top1, t_arr, codes, X, feat}  (feat=price系_pct+地合い)
t_arr=B['t_arr']; netfix=B['netfix']; codes=B['codes']; top1=B['top1']; X=B['X']

# 2) 4エンジン学習(複利/大化け/左裾回避/神の目)
eng = C.engines(X, trm, netfix, top1)          # trm=学習mask(bool配列, 例 t_arr<=sp)
scd = {k:g.predict(X) for k,g in eng.items()}
th  = {k:__import__('numpy').quantile(scd[k][trm],0.95) for k in eng}  # しきい値=学習quantile固定(look-ahead防止)

# 3) 入口=複+大+左 のAND
base = C.base_ML(scd, th)                        # bool配列(複利&大化け&左裾回避 各上位5%)

# 4) 実約定複利sim(常時フルポジ等加重daily_max5。検証済み)
m327,ntr,wr,gr,dd = C.sim_equal_weight(base & tem, t_arr, netfix, codes, top1, scd['神の目'], M=1)
#   tem=検証mask(t_arr>sp)。M=同銘柄最大玉数(1=乗り続けなし)。
#   返り値 = (16m倍率, 約定数, 勝率, 神の目率, 最大DD)
```
定数(C.COST/TAX/BASE_SPREAD/INIT/K=30/HOLD=13/MIN_PER/DAILY_MAX=5)もcfs_commonにある。
★cfs_common/ark_guard/各cfsXXX.pyのソースはmirror(.mdのみ)に無い。中身を読みたい時はヨークにアップロードを依頼するか private repo(github.com/CFS-york/project-cfs)を参照。



## 絶対原則
神の目を物差しに。神の目=未来netの上位を選別。その買い目と決済を解剖し手法化するのが本筋。

## ★★★失念防止チェックリスト(検証前に毎回 必ず読む)
1. レバレッジ禁止(大原則)。10xはレバなし全額複利。
2. 評価軸は実約定複利(等加重・常時フルポジション)。全候補の平均log/勝率は幻(cfs162で確定)。平均logで入口を語らない。
3. 入口の本数も構成も選択基準も資金管理も、実約定複利で選ぶ。古い軸(平均log)で選んだ結論を引きずらない。
4. 順序: 実約定複利でプラス安定 -> BREAKER -> 通過で初めて確定 -> ③⑤更新。確定前に倍率/出口で遊ばない。
5. courtで停止しない。コード作成->検証->present_files->説明を一つの応答で完遂。
6. 取り置きを増やすだけにしない。確定したら統合し、否定されたら却下に畳む。
7. 対照が崩れたらsimだけでなくデータ準備(特徴量merge=地合いmret20_pctg/mvol_pctg等)も疑う。cfs177-179で地合い欠落を3回simのせいと誤認した。新scriptは原資読込の地合いmergeを必ず確認。
8. BREAKERはARKが確証を得たもののストレステスト(検証の代行でない)。確証を得てから出す。詳細は下記★BREAKERの役割。

## ★BREAKERの役割(何度も失念。検証前に必ず確認)
- BREAKER = ARKが確証を得た入口を「確定に昇華できるか」独立にストレステストする役。★ARKの検証の代行ではない。
- 正しい順序:
  1. ARK自身が look-ahead / execution(netfixのentry/exit定義=AdjO[t+1]翌日寄付->AdjC[t+14]終値で確証済、同日約定でないか) / 頑健性 を照合し尽くし「確証」を得る。
  2. その確証を、期待値を伝えずBREAKER(別Incognitoスレ、コードのみ)が独立に殴る。
  3. 崩壊確定/判断保留/判定B を受け、通れば確定 -> ③⑤更新。
- ★BREAKERに検証を丸投げしない。確証を得てから出す。確証なきもの(ARKが生きてると判断しただけ)を出すと即崩れる=無駄。
- 「2.91x頑健を見た」は確証でない。execution照合・look-ahead照合・最小手動ケースまでやって初めて確証。

## ★現在地(確定候補形。次はBREAKER。BREAKER未通過=未確証)
- 入口: 3本AND = 複利(logret) + 大化け(net>=0.5) + 左裾回避(net>=-0.05) 各GBM上位5%(学習60%quantile固定)。
- 選択: 同日複数から神の目エンジンスコア順。
- 資金管理: 常時フルポジション等加重(各銘柄=総資産/K)。daily_max=5。K30 hold13 MIN_PER2万。
- 入力特徴: price系_pct + 地合い(mret20_pctg/mvol_pctg)。★地合い必須(欠落で2.9x->0.97xに崩れる)。
- 実約定頑健性(地合いあり 6分割): 全6分割>1.0x 中央2.91x 約定69 神の目率2.2% DD低。頑健。
- ★次: この複+大+左をBREAKERに出して入口確定 -> ③⑤更新 -> 配分(K集中度。レバなし)で10xへ。
- 候補比較(cfs172, 地合いあり): 複+左+神3.64xは約定15薄くブレ(cfs173で厚くすると崩れ却下)。複+大+左が約定厚く信頼。

## ★netfixの定義(cfs183で確証。完全一致100%)= execution確証完了
- netfix(私の物差し)= entry AdjO[t+1](翌日寄付) -> exit AdjC[t+14](13営業日後の終値) の net_of(g-COST-BASE_SPREAD, g>0で*(1-TAX))。完全一致100% 相関1.0。
- ★規約照合(CFS_RULES §2 + CFS_MANUAL execution、原文確認済): 規約は「entry=AdjO[t+1]翌日寄付約定」のみ明記。固定hold決済のexit価格種は規約に明記なし。「AdjO->AdjO」という規定は規約に存在しない(私のメモリの思い込みだった)。
- 結論: netfixのentry=翌日寄付は規約準拠。exit=13日後終値は規約未定義領域だが引け成行で執行可能・look-aheadなし=違反でない。execution確証完了。
- 教訓: (1)自分の物差し(net)の定義を確証作業まで把握してなかった。(2)規約をメモリで思い込み原文を読まず、ありもしない違反を直そうとした。規約に関わる判断は必ず原文(CFS_RULES/CFS_MANUAL)を読む。

## ★確定した学び(今日cfs157-170で掴んだ。生きてる)
1. 入口は1本でも2本でもない。目的関数違いのエンジンをN本ANDで重ねる。本数は3本がベスト(実約定: 1本1.64->2本1.89->3本2.56->4本2.40x)。
2. 平均log(全候補)は幻。実約定複利(資金制約下で実際に約定する複利)が真の評価軸。
3. ★最大の発見: 複利の壁の真因は資金管理。alloc=cash/nの現金全額投下+13日ロックで勝率68%母集団を取り逃していた。中立な分散運用(等加重+時間分散)に変えただけで1.28x->2.56x、DD-13%->-4%。入口でも予測精度でもなかった。
4. 等加重(各銘柄=総資産/K)が最大の効き。時間分散(daily_max5)で上乗せ。
5. 選択基準は複利/勝率/神の目系ならどれでも2.2-2.5xで頭打ち(団子)。神の目順が物差し原則に素直。
6. 左裾回避エンジンが頑健性の鍵(cfs160もcfs171も)。神の目/勝率エンジンに置換すると神の目率は上がるが時期依存で脆くなる。頑健性>神の目率。
7. ★波の回収決着(cfs175-180): 神の目の98%は波(同銘柄の急騰連続)由来、波が大化けの源泉(波の大化け率21%vs単発1.5%)。だが波は近似入口では捉えられない=波の起点予測(cfs176)は希少0.08%で不能、波への乗り続け(cfs180 同銘柄買い増し)は分散損ない倍率下げる(M1 2.91x>M2 2.50x>M3 2.46x)。波は神の目の特権(完全選別)。入口は1トレード単位の複+大+左が最良。
8. 入口構成いじり(cfs172-174)も選択基準(cfs169)も実約定2.2-3.6xで頭打ち。10xには入口でなく配分(レバなし)の次元が要る可能性。

## 却下/died(戻らない。否定された仮説も含む)
- 逆張り/cfs127選別/cfs130-131勝率/cfs124総当たり: 負けルート。
- 入口の1点選別で神の目率を上げる(cfs125-139b): 密度3-7%頭打ち。
- pos250高x価格低x静か(cfs147): 平均log-0.00156でプラス未達。平均log時代の手がかり=評価軸が幻と判明し優先度低下。
- 出口tp/sl(cfs165): 全24通りhold13持ち切りに及ばず。神の目近似は持ち切り前提。途中決済は回復取り逃す。
- 「予測精度の壁」仮説(cfs165取り置き4): 誤り。真因は資金管理(cfs166-168で否定)。
- 新構成(大化け+勝率+神の目)cfs170で実約定2.56x: 頑健でない(cfs171で時期依存)。却下。左裾回避が頑健性の鍵。
- 複+左+神 中央3.64x(cfs172): 約定15薄く、しきい値緩めると崩れる(cfs173)。約定15のブレ。却下、複+大+左を採る。
- 波の起点予測入口(cfs176): 起点0.08%希少で予測不能(0.80x 神の目率0.4%)。却下。
- 波への乗り続け=同銘柄買い増し(cfs180): 分散損ない倍率下げる(M2 2.50x M3 2.46x < M1 2.91x)。却下。

## 守る規律 (BREAKER確定)
1. look-ahead排除(当日断面/財務asof/特徴も買う前日まで)
2. 神の目を物差しに
3. walk-forward(前半設計/後半検証)
4. 複利は実約定複利。勝率/medianで複利を語らない。損益クリップなし
5. ARKが判断しただけのものを生きた入口と書かない(BREAKER通過まで未確証)

## 大目的: 16ヶ月10x(レバなし全額複利)。神の目あり=唯一ルート。

## FOCUS_GATE (各script前に自問)
1. 実約定複利で評価しているか。平均logの幻に乗っていないか。
2. 神の目を物差しに、買い目と決済をセットで見ているか。
3. look-ahead排除/レバ禁止/順序(実約定->BREAKER->確定)を守るか。
3b. この判断は規約・定義(execution/net/複利/cache/評価軸)に触れるか。触れるなら記憶でなくF-046ゲート(確証済み定義 or git clone原文)を参照したか。
4. 悪い結果を限界と畳まず、次の組み替えを考えているか。

## 禁止語(run.pyドリフト警告): [Standard][完成形][限界][天井][手持ち尽き]
## courtは改行を入れて読みやすく書く。
