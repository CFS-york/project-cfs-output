# CFS データ配置マップ (どこに何があるか / 引継ぎ必須)

**目的**: CFSは引継ぎ前提。次ARKが「何がどこにあるか」を即座に把握するための配置記録。
**原則**: 成果物は既定の場所(本番 `C:\mnt\data` 配下)に残す。ARK環境(/home/claude等)のみのデータは揮発前提=リセットで消える=引継げない。
最終更新 2026-06-16 (ARK-1〜3、信用検証期)

## 本番リポジトリ構成 (project-cfs/master、watcherでGitHub同期)
- `C:\mnt\data\scripts\cfsXXX.py` — 検証script本体。run.pyで実行(自動push)。cfs190-199が信用/仮説ロット検証
- `C:\mnt\data\scripts\cfs_common.py` — ★確定sim(sim_equal_weight)・load_base。検証の確定土台。自作sim禁止
- `C:\mnt\data\scripts\derive\` — ★2026-06-16新設。法則導出ロジックscript(縮約環境産、考え方の記録。数値結果は§5.16より偽の可能性、ロジック参照用)
  - ark2_derive.py(信用法則をデータから導く起点)、make10x_data3.py(神の目10xデータ生成)、derive_law.py(10xデータから法則抽出)
- `C:\mnt\data\cache\` — 生データcache(adjo/adjc/adjl/vol/margin/shortsale等)。★永久保存、削除厳禁
- `C:\mnt\data\Results\ARK\cfs5\cfs148_dataset\dataset.parquet` — 確定sim原資(450万行、godseye_net40等)
- `C:\mnt\data\ファイル2\` — 引継ぎ核md(下記)

## ファイル2 (引継ぎ核、mirror同期対象)
- `HANDOVER_LATEST.md` / `HANDOVER_FULL.md` — 現在地・全履歴
- `CFS_MAP.md` — 検証地図 + ★仮説ロット台帳(第1層、ARK-N生死一覧) + 立ち戻り点
- `CFS_STRUCTURE.md` — ★運用構造の一枚図(全体フロー・更新主体・ソース優先順位・人格ARK+BREAKER・現在地の単一性・起動チェック)。2026-06-17新設
- `CFS_RUN_PLAYBOOK.md` — ★検証実行プレイブック(検証フロー・script骨格と自作sim禁止・データ配置・物理定数・P1合格判定・10x方程式・OOS監査)。2026-06-17新設。検証実行前に必読
- `FAILURE_LOG.md` — 棄却軸(第3層) + 構造的学び(§5.16縮約偽濃縮等)
- `CFS_MANUAL.md` / `CFS_RULES.md` / `ARK_DISCIPLINE.md` / `ARK_PHILOSOPHY.md` / `CFS_DIRECTION.md`
- `ファイル2\lots\ARK-N_*.md` — ★仮説ロット詳細(第2層)。ARK-1_CFS-FANTASY / ARK-2_MARGIN / ARK-3_MARGIN-MID。mirror同期(push_to_mirror v3.3〜)
- `ファイル2\archive\` — 過去検証メモ(cfs138-184.md等)

## public mirror (project-cfs-output/main、新ARKがfetch_freshで読む)
- push_to_mirror.py v3.3 が同期: ファイル2核md + archive/ + ★lots/ + ml_output/
- ★lots/ がmirrorに乗る=次ARKが仮説ロット詳細を読める(2026-06-16 v3.3で穴を塞いだ)

## ★ARK環境のみ=揮発(引継げない、本番に無い)
ARK(/home/claude等)で作ったが本番未保存=リセットで消えるもの。残す価値あるものは上記derive/へ既に退避済。
- nightbatch_dataset.parquet等の縮約中間parquet=揮発でよい(縮約産、§5.16で偽濃縮源と判明)
- god10x_trades.parquet=揮発でよい(縮約産の神の目列、ロジックはmake10x_data3.pyに残存)
- 自作sim(test_sim/leftcut_run等)=破棄(0.6x/13x/10⁹x爆発、無効。確定simに統一)

## 引継ぎ動線 (次ARK)
1. fetch_freshでmirror取得 → HANDOVER_LATEST通読
2. CFS_MAPロット台帳でARK-N生死確認 → 気になるロットはlots\詳細md
3. FAILURE_LOG §4棄却・§5学び(特に§5.16縮約偽濃縮)
4. ★CFS_STRUCTURE(運用構造)+ CFS_RUN_PLAYBOOK(検証実行)通読 → 検証する前に必読
5. 本DATA_MAPで配置把握
