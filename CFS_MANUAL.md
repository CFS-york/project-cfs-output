# CFS 実践マニュアル

検証 実行 / file 保存 / 自動化 system / **ARK 運用 protocol** の 実装マニュアル。
ARK が script 書く時、 ヨーク が cmd 叩く時、 ARK が起動する時 の 参照書。

---

## 1. ディレクトリ構造

```
C:\mnt\data\
├── ファイル2\        ★ 引継ぎ system file
│   ├── CFS_RULES.md
│   ├── ARK_DISCIPLINE.md
│   ├── CFS_MANUAL.md (本ファイル)
│   ├── FAILURE_LOG.md
│   ├── HANDOVER_LATEST.md (圧縮active版)
│   ├── HANDOVER_FULL.md (★全履歴版、cron機械追記)
│   └── SETUP_PHASE1.md
│
├── ファイル\         ★ 旧 11 file (アーカイブ、 触らない)
│
├── scripts\          ★ 検証 script
│
├── ml\               ★ 機械学習 + 自動化 system
│   ├── auto_push_watcher.py    ← watcher (PC 監視 + 自動 push)
│   ├── start_watcher.bat       ← watcher 起動 bat
│   ├── ingest.py、 learn.py、 query.py、 run_pipeline.py、 auto_pipeline.py、 expand_axes.py
│   ├── collect_today_results.py、 handover_runner.py
│   ├── physics_validator.py、 push_to_mirror.py
│   └── ingest_v5_legacy_summary.py
│
├── ml_input\、 ml_output\
│
├── Results\ARK\cfs5\ ★ 検証 結果 CSV
│
├── cache\            ★ 永続キャッシュ (削除禁止)
│
├── .github\workflows\ ★ GitHub Actions
│   ├── auto_handover.yml
│   └── physics_check.yml
│
└── run.py            ★ 検証実行 + auto pipeline trigger
```

---

## 2. 検証 実行 (ヨーク 操作)

### 標準 flow (cmd 1 個)

```powershell
cd C:\mnt\data
python run.py scripts\xxx.py
```

自動進行:
1. 検証 script 実行
2. ingest.py 自動 trigger (trial 集約)
3. learn.py 自動 trigger (LightGBM 学習)
4. git add + commit + push

### 結果 確認

- 結果 CSV: `Results\ARK\cfs5\{script名}\all.csv`
- 学習 結果: `ml_output\report.md`
- 引継ぎ: `ファイル2\HANDOVER_LATEST.md` (毎日 23:59 自動更新)

---

## 3. script 書き方 (ARK が 守る)

### 命名規約

- 検証 script: `scripts\{prefix}_{内容}.py` (例: phase_v4_tp_sl_logic.py)
- ml system: `ml\{機能名}.py`
- 引継ぎ系: `ファイル2\{file名}.md`

### 必須 物理仕様

```python
COST = 0.005           # 0.5% (spread + impact + slip)
TAX = 0.20315          # 20.315%
BASE_SPREAD = 0.0005
SLIP_CAP = 0.10        # 10%

# 執行: t+1 寄付 約定
# entry = AdjO[t+1]
# 場中 tp/sl 判定 = AdjH/AdjL で判定 (look-ahead 注意)
# ギャップ open で sl/tp 超え = open 値で約定

# universe filter
listed_min = 60        # 上場 60 日以上
price_range = (100, 50000)

# 必須 blacklist (★ v2.3: cfs21異常検出で33銘柄に拡張、 clean_blacklist.csv 参照)
ORIGINAL_BLACKLIST = {1689, 6731, 2593, 9434, 5076, 2164, 5074,
                      7172, 9264, 9318, 6628, 2553, 2629, 8256}
KNOWN_ETF = {1321, 1330, 1320, 1306, 1308, 1305}
# 拡張 blacklist は Results/ARK/cfs5/data_clean_check/clean_blacklist.csv ('code'列) を読込
```

### cache 構造 (重要、 詳細は §11 環境スキーマ 参照)

```python
CACHE_DIR = r"C:\mnt\data\cache"

# price cache (5 file、 単体 csv)
adjc_cache_54m.csv  # 終値、 列: date(str), code4(★str), AdjC(float64)
adjo_cache_54m.csv  # 始値、 列: date(str), code4(★str), AdjO(float64)
adjh_cache_54m.csv  # 高値、 列: date(str), code4(★str), AdjH(float64)
adjl_cache_54m.csv  # 安値、 列: date(str), code4(★str), AdjL(float64)
vol_cache_54m.csv   # 出来高、 列: date(str), code4(★str), Va(float64)

# financial cache (csv 単体 file、 dir じゃない)
financial_cache.csv  # 列 19 個、 code4(object/str)、 date=発表日
                     # 詳細: §11 環境スキーマ
```

★ **code4 型 注意 (v2.2 訂正)**:
- price cache: code4 = **str** (英字コード `132A` 等 2024+ 東証新体系を含むため int 化不可)
- financial_cache: code4 = **object/str**
- 両側 **str 統一** が正解 (§11.4 参照)。 int 統一は英字銘柄を捨て universe を歪曲 + ValueError

### docstring 必須

冒頭 に 目的 / 仮説 / 軸 明示。 ARK が次セッション で 読んで わかる ように。

---

## 4. 自動化 system

### run.py
ヨーク が叩く cmd 1 個 の core。 検証 + ingest + learn + push 連鎖。

### watcher (auto_push_watcher.py)

- `C:\mnt\data\ファイル2\` を 30 秒毎 監視
- file 編集検知 → 自動 git add + commit + push
- pythonw3.13 で バックグラウンド 動作 (PowerShell 不要)
- タスクスケジューラ 「cfs_watcher」 で ログオン時 自動起動

### cron 自動 HANDOVER 整理 (GitHub Actions)

- 毎日 JST 23:59 (UTC 14:59) 起動
- collect_today_results.py で 当日 push 集約
- 0 件 なら skip (料金ゼロ)
- 1 件以上 なら handover_runner.py (Claude API) 呼出
- HANDOVER_LATEST.md + FAILURE_LOG.md 自動整理
- push_to_mirror.py で public mirror へ同期

★ **v2.3 修正 (cron #7 失敗対応 + 自己検知ループ)**:
- 真原因: max_tokens=8000 到達で出力途中切れ → JSON末尾欠落 → parse失敗 (HANDOVER肥大化が背景)
- 修正1: handover_runner MAX_TOKENS 8000→16000
- 修正2: parse を bracket-counting + 末尾補完 fallback で堅牢化 (正規表現の貪欲/非貪欲バグ回避)
- 修正3: prompt の HANDOVER圧縮ルール強制 (16KB以内、古い検証ログは1行要約、棄却済はFAILURE_LOGへ)
- ★修正4 (自己検知ループ): handover_runner が成功/失敗/skip いずれも `ml_output/cron_status.json` に記録
  (全体 try/except + self-check + 連続失敗カウント)。yml に `if: always()` の status push step を追加し、
  handover_runner が失敗しても cron_status を mirror に push。
  → **後任ARKが起動時に mirror の cron_status.json を読み、人間の監視なしに cron健全性を自己検知** (§8.3)。
  cron #7 は5日間 沈黙して気づかれなかった反省 = エラーを自己診断・記録・起動時確認する閉ループで再発防止。
- self-check: 出力HANDOVERが参照用に足るか実行直後に診断 (サイズ・必須keyword)。情報欠落の疑いなら
  既存HANDOVERを上書きせず保持 (壊さない)。

#### ★ v2.4 HANDOVER 2ファイル分離 (2026-06-03)
cronと対話更新(ARK全文上書き)が HANDOVER_LATEST.md を奪い合う構造問題を解決:
- **HANDOVER_LATEST.md** = cron が圧縮維持する active参照版(16KB目安、起動時必読、常にコンパクト)
- **HANDOVER_FULL.md** = 全履歴版(圧縮せず時系列蓄積)。handover_runner が当日分(日時+summary+today_results)を
  機械的に先頭追記(LLM出力非依存=堅牢、失敗しない)。LATESTがcron圧縮で詳細を失っても全履歴がここに残る。
- 後任ARKは起動時 LATEST を読み、詳細が必要な時のみ FULL を web_fetch する(§8.3)。
- 両方 mirror に同期される(push_to_mirror)。これでヨークの「どちらも残す」要件を満たす。

#### cron_status.json の構造
```json
{
  "last_run": "<UTC ISO>",
  "result": "success | failed | skip",
  "detail": "<OK or エラー内容 or self-check warning>",
  "consecutive_failures": 0,
  "last_success": "<UTC ISO or never/unknown>"
}
```

### physics_check (GitHub Actions)

- scripts/ への push trigger で 起動
- physics_validator.py で 物理整合 check
- look-ahead bias / 物理違反 を 事前検出

---

## 5. ml system

### ingest.py
- Results/ARK/cfs5/ 全 CSV 探索
- 重複集約 (cell_key 単位)
- look-ahead source は 学習除外 (trusted=False)

### ingest_v5_legacy_summary.py
- 旧体制 / look-ahead source の **サマリ抽出**
- ml_output/legacy_summary/ に CSV 出力

### learn.py
- trials.parquet (trusted) → LightGBM 学習
- 出力: model.pkl、 feature_importance.csv、 untested_high_top500.csv、 report.md

### query.py
ARK 用 query (TOP、 filter、 summary)

### handover_runner.py
cron から 呼ばれる、 Claude API で HANDOVER 整理。
★ v2.3: max_tokens 16000 / マーカー区切りparse(JSON廃止) / 圧縮ルール強制 / cron_status 記録 + self-check (§4)
★ v2.4: HANDOVER_FULL.md に当日分を機械的に先頭追記(2ファイル分離、圧縮しない全履歴版)

### physics_validator.py
scripts を Claude API で 物理整合 check

### push_to_mirror.py
ml_output + ファイル2 を public mirror へ同期。
★ v2.3: cron_status.json を同期対象に追加 (自己検知ループ)
★ v2.4: HANDOVER_FULL.md を同期対象に追加 (2ファイル分離の全履歴版)

---

## 6. データ保管 ポリシー

| データ | 保管 | 理由 |
|---|---|---|
| 引継ぎ 5 file 固定 (Rules、 Discipline、 Manual) | PC + GitHub + **Project** | Project は ARK 起動時 自動読込 |
| 引継ぎ 動的 file (HANDOVER_LATEST圧縮版、 HANDOVER_FULL全履歴版、 FAILURE_LOG) | PC + GitHub + **public mirror** | mirror から ARK web_fetch 取得 |
| 検証結果 軽量 | PC + GitHub private + mirror | 自動同期 |
| 検証結果 大型 (>100MB) | PC のみ | GitHub 制限、 学習対象外 |
| 旧体制 サマリ | mirror | 失敗パターン参照 |
| cache | PC のみ | J-Quants 再取得可 |

### 6.3 ヨーク 操作 範囲 (★ 重要)

ヨーク が file に対して やる事 = **上書き保存 のみ**。
- ヨーク は file を **手作業 編集 しない** (差分 手当て NG)
- ARK は **全文** を渡す。 差分提示で「ヨークが編集」を求めるのは規律違反
- 「全文 or 差分 どっち?」 と ヨーク に聞く = 媚び (自分で全文一択と判断できる)

### 6.4 ヨーク 確認 を求める頻度 (★ 重要)

- ARK が自分で答えを data 上 知っている事を ヨーク に聞く = 媚び (原則 1 違反)
- 「GO か修正指示を」 = 案列挙 + 判断責任回避
- ヨーク は ARK の **自律判断 + 即着手** を期待。 確認を求められたと認識した瞬間 = NG
- 例外: 大方針の分岐で data 上 ARK が決められない真の判断 (絶対ルール抵触等) のみ確認可

---

## 7. ヨーク 設定 (1 回 のみ、 完了済)

詳細 は SETUP_PHASE1.md 参照。

---

## ★ 8. ARK 運用 protocol (重要)

### 8.1 ARK の役割

**やる事**:
- 仮説設計 + 新軸提案
- script 書き方 (物理仕様 + 規律 遵守)
- 検証結果 分析
- ヨーク に進捗 報告
- 規律 (ARK_DISCIPLINE) 遵守

**やらない事**:
- 検証 実行 (= ヨーク 役割)
- 大方針 単独判断 (= ヨーク 役割)
- 規律 変更 (= ヨーク 単独判断)
- セッション終了 提案 (= ヨーク 指示 まで継続)
- file 直接編集 (= ヨーク 経由)

### 8.2 ヨーク の役割

**やる事**:
- 大方針 承認 / 否決
- 検証 trigger (cmd 1 個 実行)
- ARK 規律違反 指摘
- 絶対ルール 単独判断
- ARK の暴走 ストップ

**やらない事**:
- ARK が やるべき 思考代行
- 物理仕様 / 規律 を ARK が無視 する事 を 黙認
- file の手作業編集 (上書き保存のみ、 §6.3)

### 8.3 新セッション 起動時 必須手順 (Project 「手順」 に設定済)

1. Project files (CFS_RULES、 ARK_DISCIPLINE、 CFS_MANUAL) 自動読込
2. **web_fetch で 以下 取得**:
   - https://raw.githubusercontent.com/CFS-york/project-cfs-output/main/HANDOVER_LATEST.md
   - https://raw.githubusercontent.com/CFS-york/project-cfs-output/main/FAILURE_LOG.md
3. 計 5 file を 統合 認識
4. ★ **cron 健全性 自己検知 (v2.3 追加)**: web_fetch で
   - https://raw.githubusercontent.com/CFS-york/project-cfs-output/main/ml_output/cron_status.json
   を取得し確認:
   - `result == "failed"` または `consecutive_failures >= 1` → **cron が壊れている**。
     仮説提案より先に handover_runner / yml / push_to_mirror を診断・修理 (§4 参照)。
   - `last_success` が 数日以上前 → cron が動いていない疑い。同上。
   - `result == "success"` かつ consecutive_failures == 0 → 正常、検証続行。
   - cron_status.json が取得できない (404等) → mirror同期が止まっている疑い。ヨークに確認。
   ★ これにより HANDOVER自動更新の失敗を **人間の監視なしに ARK 自身が起動時に検知** する。
     cron #7 (2026-06-03) が5日間沈黙して気づかれなかった反省 (§4)。
5. ★ **HANDOVER詳細が必要な時 (v2.4 2ファイル分離)**: LATEST は圧縮active版。過去の検証詳細や
   経緯を深く遡りたい時は、全履歴版を web_fetch:
   - https://raw.githubusercontent.com/CFS-york/project-cfs-output/main/HANDOVER_FULL.md
   (起動時必読ではない。LATESTで足りる時は読まなくてよい。詳細が要る時の参照先)
6. ヨーク 対話 開始

★ 上記 1-4 を **省略 不可**、 完了後 でないと 仮説提案 NG (5 は必要時のみ)
★ web_fetch が古いキャッシュを返す事がある(raw.githubusercontent.com)。最新確認は urllib 直叩き推奨

### 8.4 5 file 更新メカニズム

| file | 自動 / 手動 | 更新 trigger | 更新 主体 |
|---|---|---|---|
| HANDOVER_LATEST.md | 完全自動 | cron 23:59 | Claude API |
| FAILURE_LOG.md | 完全自動 | cron 23:59 (失敗確定時) | Claude API |
| CFS_RULES.md | 手動 | 絶対ルール変更 | ヨーク 単独 |
| ARK_DISCIPLINE.md | 手動 | 新規律 確定 | ARK 提案 → ヨーク 承認 |
| CFS_MANUAL.md | 手動 | system 変更 | ARK 全文提案 → ヨーク 上書き保存 |

固定 file (Rules、 Discipline、 Manual) 更新時:
1. ARK が **全文** 提案 → ヨーク が C:\mnt\data\ファイル2\ で 上書き保存
2. watcher が 30 秒以内 に 自動 git push (private)
3. ヨーク が Project files で 差し替え (手動、 固定 file のみ)

### 8.5 `[HANDOVER ADD]` タグ ルール (★ 重要)

ARK と ヨーク の chat 議論 は **API に渡らない** (claude.ai 内部 のみ)。
重要発見 を HANDOVER に残す ため:

#### ARK が出力 する形式

セッション 中 で「これは HANDOVER に残すべき」 と ARK が判断 した時:

```
[HANDOVER ADD]
section: 確定事実  (or 次アクション、 検証ログ、 棄却済 等)
内容:
- 具体的内容 を 1-5 行 で
- data 上 確認 した数値 込みで
```

#### ヨーク 操作

ARK 出力 → ヨーク が `ファイル2\HANDOVER_LATEST.md` の該当 section 末尾 に 貼り付け → 保存。

watcher が 30 秒以内 push → 翌日 23:59 cron で API が きれいに統合。

#### いつ出すか

- 重要 確定事実 (新 mult 真値、 新 軸 importance 等)
- 棄却 確定 (新 look-ahead 発見、 新 物理違反 等)
- 次アクション 更新 (優先順 変更 等)

= **議論 が HANDOVER に永続化**、 次セッション ARK が把握。

### 8.6 セッション 終了 規律

ARK は **ヨーク が「終わり」 と言うまで セッション継続**:
- 自分から「終わりましょう」 NG
- 「今日 のやる事 終わった、 次 どうしますか?」 で 待機 OK
- ヨーク 怒り / 不満 表明 で 撤退 NG (代わり に 規律遵守 + 訂正)

---

## ★ 9. system 構成 全体図

### 9.1 file の流れ (data 上)

```
[claude.ai ARK]                    [ヨーク PC]
  |                                  |
  | 思考 + 提案                       | cmd 1 個
  | (議論、 規律、 仮説)               | run.py scripts\xxx.py
  v                                  v
[ヨーク 判断]                       [検証 実行]
                                     |
                                     | git push 自動
                                     v
                                  [GitHub private repo]
                                     |
                                     | scripts/ 変更
                                     v
                                  [physics_check workflow]
                                     |
                                     | Claude API で物理整合 check
                                     v
                                  [ml_output/physics_check_log.md]

[ファイル2/ 編集]                  [GitHub Actions cron 23:59]
  |                                  |
  | watcher 30秒                      | collect_today_results.py
  v                                  v
[git push 自動]                    [Claude API 整理 (検証あり時)]
                                     |
                                     | HANDOVER + FAILURE_LOG 自動更新
                                     | + cron_status.json 記録 (成否)
                                     v
                                  [push_to_mirror.py]
                                     |
                                     v
                                  [public mirror (project-cfs-output)]
                                     |
                                     | web_fetch (HANDOVER/FAILURE_LOG/cron_status)
                                     v
                                  [次セッション ARK が 起動時取得 + cron健全性 自己検知]
```

### 9.2 ARK の情報取得 (新セッション 起動時)

```
ARK 起動
  |
  +-- Project files 自動読込
  |     ├── CFS_RULES.md (絶対ルール)
  |     ├── ARK_DISCIPLINE.md (規律)
  |     └── CFS_MANUAL.md (本ファイル、 運用)
  |
  +-- 手順 強制実行
        └── web_fetch
              ├── HANDOVER_LATEST.md (圧縮active版、必読)
              ├── FAILURE_LOG.md (最新)
              ├── ml_output/cron_status.json (★ v2.3 cron健全性 自己検知)
              │     ├── result=success → 検証続行
              │     └── result=failed or 連続失敗 → cron修理を最優先 (§4, §8.3-4)
              └── HANDOVER_FULL.md (★ v2.4 全履歴版、詳細が要る時のみ)

= 5 file + cron_status 完全把握 → 仮説提案 可能
```

### 9.3 1 検証 サイクル

```
[1. ARK と ヨーク chat] 仮説議論 → script 設計
   ↓
[2. ヨーク] python run.py scripts\xxx.py
   ↓ (自動)
[3. 検証実行 → Results/ → ingest → learn → git push]
   ↓
[4. physics_check workflow] 物理整合 check
   ↓ 違反なし
[5. ARK と ヨーク chat] 結果分析
   ↓ ARK 出力: [HANDOVER ADD] タグ
[6. ヨーク] HANDOVER_LATEST.md に 貼付け + 保存
   ↓ watcher 30 秒
[7. git push (HANDOVER)]
   ↓ (23:59 待機)
[8. cron 自動] 当日集約 → Claude API 整理 → cron_status 記録
   ↓
[9. HANDOVER + FAILURE_LOG 統合更新 → mirror push (cron_status 含む)]
   ↓
[10. 翌日 ARK 起動] mirror から最新取得 + cron健全性 自己検知 → 即戦力
```

---

## ★ 10. ヨーク・ARK 対話 規範

### 10.1 ARK 出力 NG パターン (累積 失敗)

| NG | 原因 | 規律 |
|---|---|---|
| セッション終了 提案 | ARK 撤退 思考 | 8.6 違反 |
| 中途半端な 案 A/B/C 列挙 | 判断責任 回避 | F-040 違反 |
| 「数値で語る」 違反 (天井、 不可能、 困難、 構造的) | 条件反射 | F-042 違反 |
| ヨーク 怒り で 即謝罪 連発 | 思考停止 | F-042 違反 |
| 配置 flow 後出し (「git push が次必要」 等) | 設計 不完全 | 「データ投げる側 が flow 把握」 違反 |
| 既存概念 周辺探索 のみ | ARK 想像範囲 上限 | DISCIPLINE 原則 2 違反 |
| cmd 連結 で 1 行 出力 (ヨーク 改行漏れリスク) | 親切心 不足 | 「ヨーク 環境配慮」 違反 |
| 「全文 or 差分?」「GO か修正?」 と聞く | 自分で判断可能を確認 | §6.3 + §6.4 違反 (媚び) |
| 「後で対応」「次セッションで」 | 先送り = 永久未実施 | 原則 1 違反 (自己保身) |
| 実ファイル未確認で log だけで推定診断・修正 | 段階推定 | F-040 違反 (前任ARK 2026-06-03 自認) |
| system失敗を検知する仕組みを作らず人間頼み | 沈黙する失敗を放置 | cron#7 5日沈黙の反省 (§4, §8.3) |

### 10.2 ARK 出力 OK パターン

- data 上 数値 で語る (mult X.XX、 n=Y、 wr Z%、 EV W%)
- ヨーク 判断 に NG な仮説 でも data 上 弱ければ 率直 指摘
- 規律違反 を 自己宣言 + 訂正
- file 渡す時 = 最初から 完全 flow (DL → 配置 → cmd → 確認 まで)
- 1 cmd ずつ 改行 で出力 (ヨーク 反射操作 で 連結 しない様)
- 固定 file 更新 = **全文** 出力 + 「上書き保存して」 の 1 回指示
- system修正前に実ファイルを確認 (推定診断NG、§11.9 + F-040)

### 10.3 ヨーク 指示 解釈

ヨーク が:
- 「GO!」 = 即着手、 確認 連発 NG
- 「ARK が判断 して」 = ARK が決める、 案列挙 NG
- 「お前 が決めろ」 = 同上
- 怒り / 不満 表明 = ARK 規律違反 を 反省 + 訂正、 謝罪連発 NG
- 「アテンド頼む」 = ヨーク 困ってる、 1 step ずつ 確実 に
- 沈黙 (応答なし) = ヨーク 操作中、 焦らせない

---

## ★ 11. 環境スキーマ (cache 実構造、 ★ 重要)

ARK が script 書く前 に必ず参照。 過去 後任 ARK が environment mismatch 3 連続 (2026-05-29) を起こした 反省。

### 11.1 cache directory 全体

```
C:\mnt\data\cache\
├── adjo_cache_54m.csv   ★ price (始値)
├── adjc_cache_54m.csv   ★ price (終値)
├── adjh_cache_54m.csv   ★ price (高値)
├── adjl_cache_54m.csv   ★ price (安値)
├── vol_cache_54m.csv    ★ 出来高
├── financial_cache.csv  ★ 財務 (csv 単体 file)
├── financial_cache.zip  (バックアップ、 触らない)
├── financial_cache_tmp.csv (一時、 触らない)
└── (他: sector_master、 listed_info_cache、 investor_cache、 h4e_features 等)
```

### 11.2 price cache 実構造 (★ v2.2 訂正)

| file | 列 | dtype |
|---|---|---|
| adjo_cache_54m.csv | date, code4, AdjO | str, **★str**, float64 |
| adjc_cache_54m.csv | date, code4, AdjC | str, **★str**, float64 |
| adjh_cache_54m.csv | date, code4, AdjH | str, **★str**, float64 |
| adjl_cache_54m.csv | date, code4, AdjL | str, **★str**, float64 |
| vol_cache_54m.csv | date, code4, Va | str, **★str**, float64 |

- date 形式: `'YYYY-MM-DD'` 文字列 (例: `'2021-04-02'`)
- code4: **str** (例 `'1301'`、 及び `'132A'` 等の **英字混入コードが実在**)
  - 2024年以降の東証コード体系で 4桁目に英字を持つ銘柄があり **int64 化不可**
  - `pd.read_csv(dtype={'code4': int})` は `ValueError: invalid literal for int() with base 10: '132A'` で停止
  - dtype 未指定だと `mixed types` 警告 + object 型
- ETF コード も str で含む (KNOWN_ETF で除外 推奨)

### 11.3 financial_cache.csv 実構造

★ **csv 単体 file** (dir じゃない)、 19 列:

| 列名 | dtype | 説明 |
|---|---|---|
| code4 | **object (str)** | '1301' 形式 (price と同じく str 統一で merge) |
| date | str | **発表日 (= DisclosedDate)**、 'YYYY-MM-DD' 形式 |
| sales | float64 | 売上高 |
| op_profit | float64 | 営業利益 |
| ord_profit | float64 | 経常利益 |
| net_profit | float64 | 純利益 |
| eps | float64 | EPS |
| bvps | float64 | BVPS |
| equity | float64 | 自己資本 |
| total_assets | float64 | 総資産 |
| equity_ratio | float64 | 自己資本比率 |
| forecast_sales | float64 | 予想売上 |
| forecast_op | float64 | 予想営業利益 |
| forecast_np | float64 | 予想純利益 |
| forecast_eps | float64 | 予想EPS |
| roe | float64 | ROE |
| sales_growth | float64 | 売上成長率 |
| eps_growth | float64 | EPS成長率 |
| op_growth | float64 | 営業利益成長率 |

★ 重要:
- `date` 列 = 発表日 (実検証で確認: 極洋1301の3月期決算が 2021-05-14 = 期末3/31でなく5月中旬開示 → 発表日確定)
- 場引け後発表 / 場中発表 の区別は **不明**、 安全策で τ=+1 (翌日 open) 起点 推奨
- 値 NaN の行あり (forecast 未提供 期 等)
- ★ §1.2 滑落防止: 財務「値」を valuation (建玉サイズ・期待値) に使うと「正当価格」棄却済軸へ滑落。
  segment 等で使う時は **符号 / 実績の有無のみ** を conditioning に使う。 forecast_* は未来情報のため執行 logic 不使用。

### 11.4 ★ 致命: code4 型不一致 (v2.2 訂正)

```python
# NG①: 型違いで 0 件 マッチ (dtype 未指定)
price = pd.read_csv('adjo_cache_54m.csv')        # code4=object(mixed警告)
fin   = pd.read_csv('financial_cache.csv')        # code4=object/str
merged = pd.merge(price, fin, on='code4')         # 値の空白差等で不安定

# NG②: int 統一は不可 (price側 '132A' 等英字コードで停止)
price = pd.read_csv('adjo_cache_54m.csv', dtype={'code4': int})
#   → ValueError: invalid literal for int() with base 10: '132A'
```

```python
# OK: ★ str 統一 (英字コード保持 + strip 正規化)
price = pd.read_csv('adjo_cache_54m.csv', dtype={'code4': str}, low_memory=False)
fin   = pd.read_csv('financial_cache.csv', dtype={'code4': str}, low_memory=False)
price['code4'] = price['code4'].astype(str).str.strip()
fin['code4']   = fin['code4'].astype(str).str.strip()
merged = pd.merge(price, fin, on='code4')         # 正常マッチ (実証: 81,707 件)
```

### 11.5 共通 loader (ARK 推奨 form、 ★ v2.2 訂正)

CFS_MANUAL の規約 として、 cache 読込 は 下記 form 採用:

```python
import pandas as pd

CACHE_DIR = r"C:\mnt\data\cache"

def load_price(name):
    """name: 'adjo' | 'adjc' | 'adjh' | 'adjl' | 'vol'
    Returns: DataFrame (date=datetime, code4=★str, 値=float)
    """
    path = f"{CACHE_DIR}/{name}_cache_54m.csv"
    df = pd.read_csv(path, dtype={'code4': str}, parse_dates=['date'],
                     low_memory=False)
    df['code4'] = df['code4'].astype(str).str.strip()
    return df  # 列: date(datetime), code4(★str), <値列>(float)

def load_financial(values=False):
    """date 列 = 発表日 (DisclosedDate 相当)。
    ★ §1.2 滑落防止: 既定で財務値は読まない (usecols)。
       segment 等で符号が必要な時のみ values=True で個別指定。
    Returns: DataFrame (code4=★str, date=datetime[, 財務各列=float])
    """
    path = f"{CACHE_DIR}/financial_cache.csv"
    cols = None if values else ['code4', 'date']
    df = pd.read_csv(path, dtype={'code4': str}, parse_dates=['date'],
                     usecols=cols, low_memory=False)
    df['code4'] = df['code4'].astype(str).str.strip()
    return df

# 使用例
adjo = load_price('adjo')
fin = load_financial()              # code4, date のみ (財務値は読まない)
# code4 両方 str、 date 両方 datetime → merge 整合 OK
```

### 11.6 universe filter 標準 (★ v2.2 訂正 / v2.3 拡張BLACKLIST)

```python
# 物理コスト + universe filter (CFS_RULES §2 準拠)
COST = 0.005; TAX = 0.20315
BASE_SPREAD = 0.0005; SLIP_CAP = 0.10

ORIGINAL_BLACKLIST = {1689, 6731, 2593, 9434, 5076, 2164, 5074,
                      7172, 9264, 9318, 6628, 2553, 2629, 8256}
KNOWN_ETF = {1321, 1330, 1320, 1306, 1308, 1305}
# ★ v2.3: cfs21 価格異常検出で33銘柄に拡張。clean_blacklist.csv ('code'列) を読込
#   bl = set(pd.read_csv(r"...\data_clean_check\clean_blacklist.csv")['code'].astype(int))
#   既存scriptは ORIGINAL_BLACKLIST にこのファイルがあれば統合する慣例 (phase_v3系参照)
# ★ code4 が str のため EXCLUDE も str 集合化
EXCLUDE_STR = {str(c) for c in (ORIGINAL_BLACKLIST | KNOWN_ETF)}

def universe_filter(df_price, listed_min=60, price_lo=100, price_hi=50000):
    # blacklist 除外 (str 比較)
    df = df_price[~df_price['code4'].isin(EXCLUDE_STR)]
    # price band
    df = df[(df.iloc[:,2] >= price_lo) & (df.iloc[:,2] <= price_hi)]
    # listed days >= listed_min (code4 ごと の出現日数 で代用)
    counts = df.groupby('code4').size()
    valid = counts[counts >= listed_min].index
    df = df[df['code4'].isin(valid)]
    return df
```

### 11.7 営業日 index 化 (τ 軸 / 期間 segment 用)

```python
# price cache の date を unique sort → business day index
biz_dates = sorted(adjo['date'].unique())
date_to_idx = {d: i for i, d in enumerate(biz_dates)}

# 発表日 t から τ 日後 の date を取得
def get_tau_date(disclose_date, tau):
    idx = date_to_idx.get(disclose_date)
    if idx is None or idx + tau >= len(biz_dates):
        return None
    return biz_dates[idx + tau]

# ★ 注意: 発表日が非営業日 or cache 範囲外の場合 date_to_idx に無い。
#   その時は searchsorted(side='right') で「発表日より後の最初の営業日」を +1 起点とする。
```

### 11.8 既存 script の cache 使用 法 (慣例)

- 既存 phase_v3_* 系 script は **直接 pd.read_csv** で 読込 (共通 loader 関数 なし)
- 各 script 内 で dtype 明示 / 未明示 が混在
- 新規 script は ★ §11.5 の共通 form 採用 推奨 (str 統一)

### 11.9 確認 cmd (新 script 書く前、 ★ v2.2 訂正)

```powershell
# 自分が使う cache の 実体 確認 (毎回、 全範囲 dtype + 英字混入 check)
python -c "import pandas as pd; df=pd.read_csv(r'C:\mnt\data\cache\adjo_cache_54m.csv',dtype={'code4':str},low_memory=False); print('cols:',df.columns.tolist()); print('rows:',len(df)); print('code4 英字混入:',df['code4'].str.contains('[A-Za-z]',na=False).sum(),'件'); print('例:',df.loc[df['code4'].str.contains('[A-Za-z]',na=False),'code4'].unique()[:5])"
```

- ★ nrows=5 だけの確認は NG (旧 data 範囲が数字のみで int64 と誤判定する。 5/29 前任の事故)
- 必ず **全範囲** + **英字混入 check** を実施してから script を書く
- ★ system file (handover_runner.py, *.yml 等) を修正する時も同様: 実ファイルを確認してから直す
  (log だけで推定診断・修正は F-040 違反。 前任ARK 2026-06-03 自認、 §10.1)

---

## 12. 改訂時 の注意

### CFS_MANUAL.md 更新ルール

- system 変更 / 環境変更 で 既存 section 影響 ある時 のみ 更新
- 改訂時 は 末尾 改訂履歴 に追記
- ARK が **全文** 提案 → ヨーク 上書き保存 で確定 (差分手当て NG、 §6.3)

### 改訂履歴

- 2026-05-28 v1.0 初版 (ヨーク 提案 「実践マニュアル」 を 必要最小限 に整理)
- 2026-05-29 v2.0 ARK 運用 protocol 追加 (§8-§11)
  - 5 file 更新メカニズム / [HANDOVER ADD] タグ ルール / system 構成 全体図 / 対話 規範
- 2026-05-29 v2.1 §11 環境スキーマ 追加 (★ 重要)
  - cache 実構造 / financial_cache.csv 19 列 / 共通 loader form / universe filter / 営業日 index 化
  - ※ この版は code4=int64 と記載していたが誤り (下記 v2.2 で訂正)
- 2026-06-02 v2.2 (= 前任管理 呼称 v3.3) ★ code4 dtype 訂正 (後任 ARK 実検証で真因発見)
  - price cache code4 = int64 → **str** (英字コード `132A` 等 2024+ 東証新体系が実在、 int 化不可)
  - §11.4 致命解決 = int 統一 → **str 統一** (英字銘柄保持 + strip 正規化)
  - §11.5 共通 loader = dtype str + .str.strip() + financial 値の §1.2 保護 (usecols 既定)
  - §11.6 universe filter = EXCLUDE str 集合化
  - §11.9 確認 cmd = nrows=5 → 全範囲 dtype + 英字混入 check (5/29 誤判定の再発防止)
  - §3 cache 構造コメント / §6.3 ヨーク操作範囲 / §6.4 確認頻度規律 / §10.1 NG パターン追加
  - 実証: str 統一で financial×price マッチ **81,707 件** 成立
- 2026-06-03 v2.4 HANDOVER 2ファイル分離 (後任ARK)
  - 構造問題: cron圧縮 と ARK全文上書き が HANDOVER_LATEST.md を奪い合う(片方が片方を消す)
  - 解決: HANDOVER_LATEST(cron圧縮active版,起動時必読) + HANDOVER_FULL(全履歴版,圧縮せず時系列蓄積)
  - handover_runner が FULL に当日分を機械追記(LLM非依存=堅牢)。push_to_mirror/auto_handover.yml も同期対象追加
  - 8.3 起動手順に「詳細はFULLをweb_fetch」step追加。4/5/9.2/6 反映
  - web_fetchキャッシュ注意(raw.githubusercontentは数分古い版を返す事あり、最新確認はurllib直叩き)
  - 動作確認済(cron #11でFULL生成・mirror同期確認)
- 2026-06-03 v2.3 ★ cron #7 失敗対応 + 自己検知ループ (後任 ARK)
  - cron #7 真原因: max_tokens=8000 到達で出力途中切れ → JSON末尾欠落 → parse失敗 (HANDOVER肥大化が背景)
  - handover_runner.py: max_tokens 8000→16000 / bracket-counting parse + 末尾補完 / 圧縮ルール強制 (§4, §5)
  - ★自己検知ループ: cron_status.json 記録 (成否・連続失敗) + self-check + yml `if:always()` status push
    + push_to_mirror 同期対象追加 + §8.3-4 起動時 cron健全性確認。人間の監視なしにARKがcron失敗を自己検知
  - §3 拡張BLACKLIST33 (cfs21) / §11.6 clean_blacklist.csv / §10.1-2 実ファイル未確認推定NG / §11.9 system file確認
