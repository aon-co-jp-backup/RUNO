# PORTING.md(RUNO、旧称: open-aruaru-runo-iLumi → aon)

このリポジトリは`aon-co-jp`エコシステム全体の**メタ索引**であり、
移植対象となる実装コード・お引越し可能な機能を一切持たない
(ローカル作業ドライブは`F:\runo`)。

他プロジェクトの`PORTING.md`(お引越し可能ファイル一覧)への入口は、
[`README.md`](README.md)の一覧表から各プロジェクトへ辿ることができる。

移植可能な資産が生じた場合(索引生成補助スクリプト等)、この節を更新する。

---

## 2026-09-03(続き29) チェックポイント(open-cuda / open-directx / aruaru-llm: 32GB VRAM級3ベンダー前提 + F16/F32/F64/F128 精度対応)

ユーザー指示「open-directx open-cuda aruaru-llmにて、RTXかAMDやINTELで
32GB VRAMグラフィックボード想定でF16/F32/F64などを想定して開発を進めて」
「F128まで対応しておいて」への対応。3リポジトリへ並行してバックグラウンド
エージェントを投入(この開発機の実機はGT 730〈Kepler、2GB〉のみのため、
32GB級マルチベンダー実機検証はいずれのリポジトリでも不可能)。

- **open-cuda**(コミット`f4652ce`・`8ed166c`): `opencuda-core::KernelArg`/
  `ResolvedArg`へF16(`half::f16`)・F64・F128(自前実装のdouble-double型
  `DoubleDouble`)を追加、対応する`hgemm`/`dgemm`/`qgemm`(CPUリファレンス
  実装)を新設。**F128はGPU上のネイティブハードウェア対応が存在しない
  ためソフトウェアエミュレーション**であることを明記。`OmniGPU-Design.md`
  §13に32GB級VRAMベンダー方針を文書化。clippy/テストすべてgreen。
- **open-directx**(コミット`1849fea`・`610a8ea`): 実装調査の結果、
  DXIL(LLVMビットコード型システム)デコーダが`half`/`min16float`
  (HLSL SM6.2+のネイティブ16bit型)に対応する`TYPE_CODE_HALF`を未知の
  型として取りこぼしていた実バグを発見・修正。**F128はHLSL/DXILに
  対応する構文自体が存在しないため対象外**と正直に判断・記録
  (誤って「対応しているふり」をするコードは追加しなかった)。
- **aruaru-llm**(コミット`700f78d`・`735b072`・`c32d80d`):
  `src/hardware.rs`のVRAM推奨ヒューリスティックへ`InferencePrecision`
  (F16/F32/F64/F128、バイト/パラメータ)を導入し、同じVRAM容量でも
  fp16推論なら約2倍のパラメータ数のモデルを推奨できるようにした
  (既存関数はF32既定で委譲、後方互換)。9/9テストgreen。
- クロスリポジトリのビルド確認(aruaru-llm→open-cudaのpath依存)も
  成功を確認済み。3リポジトリともpush済み。

**English**: In parallel across `open-cuda`, `open-directx`, and
`aruaru-llm`, per user instruction to target 32GB-VRAM-class NVIDIA/AMD/
Intel GPUs and support F16/F32/F64/F128 going forward (this dev machine
only has a GT 730, so no real multi-vendor 32GB hardware verification
was possible anywhere). **open-cuda**: added `F16`/`F64`/`F128` to
`KernelArg`/`ResolvedArg` plus `hgemm`/`dgemm`/`qgemm` CPU-reference
GEMMs; F128 is an honest from-scratch software double-double type (no
GPU has native FP128 hardware). **open-directx**: found and fixed a real
bug where the DXIL type decoder didn't recognize `TYPE_CODE_HALF`
(HLSL's `half`/`min16float`); F128 was correctly declared out of scope
since HLSL/DXIL have no such construct at all — no fake support was
added. **aruaru-llm**: made the VRAM-recommendation heuristic
precision-aware (`InferencePrecision`, bytes/param), so the same VRAM
budget now recommends a bigger model at fp16 than at fp32; 9/9 tests
pass. Cross-repo build (aruaru-llm's path dependency on open-cuda) was
also verified working. All three repos pushed.

## 2026-09-03(続き28) チェックポイント(aruaru-db: .NET 実バグ修正 + Python asyncpg ハング調査 + Mojo コネクタ新設)

続き27に続き、同日中に実施。aruaru-dbコミット`4083022`・`7568a42`
(いずれもpush済み)。

- **.NET コネクタ実サーバ往復で実バグ発見・修正**: `NpgsqlDataSource`
  既定のブートストラップ(接続確立時に`pg_type`等へ型情報を問い合わせる)
  が、aruaru-dbが`pg_catalog`を完全実装していないため`"SELECT: missing
  FROM"`で失敗していた。`ServerCompatibilityMode.NoTypeLoading`で
  ブートストラップ自体を無効化して解消、`dotnet test`
  `ARUARU_DB_TEST_CONNSTRING`付きで10/10 green(実サーバ往復)。
- **Python `asyncpg` の接続がハングする問題を発見(未解決)**:
  `asyncpg.connect()`/`create_pool()`いずれも、ローカルaruaru-server
  相手にタイムアウトするまで応答が返らない(単一接続`pool=False`でも
  同様)。.NETと同種の型システム自動探索の非互換が疑われるが未確証。
  `clients/python-aruaru-db/live-check.py`を新設し、README に正直に
  記録(次回調査対象)。
- **Mojo対応を新設**: Mojoには成熟したネイティブPostgreSQLドライバが
  無いため、Python interop(`from python import Python`)経由で既存の
  `python-aruaru-db`コネクタを薄くラップする設計(`clients/
  mojo-aruaru-db/`)。commit_id検証(`is_safe_commit_id`)のみ純Mojoで
  実装(ネットワーク前の防御)。この開発機に`mojo`/`magic`/`modular`
  いずれのツールチェーンも無く、`.mojo`ファイルは未コンパイル・
  未実行(README に正直に明記、Go/Java/Rubyと同じ扱い)。
- これで公式薄いコネクタは Rust/Python/Node/PHP/COBOL/Go/Java/.NET/
  Ruby/Mojo の10言語。`docs/CLIENTS.md`・`clients/README.md`・
  aruaru-db `CLAUDE.md`(続き33)も同コミットで更新済み。

**English**: Same-day continuation of 続き27 (aruaru-db commits
`4083022`/`7568a42`, both pushed). **(1)** Found and fixed a real bug in
the .NET connector's live round-trip: `NpgsqlDataSource`'s default
bootstrap (querying `pg_type` etc. at connection time) fails against
aruaru-db with `"SELECT: missing FROM"` since aruaru-db doesn't fully
implement `pg_catalog`; fixed via `ServerCompatibilityMode.
NoTypeLoading`, `dotnet test` now 10/10 green against a real server.
**(2)** Discovered (unresolved) that Python `asyncpg.connect()`/
`create_pool()` hang indefinitely against a local aruaru-server (even
with a single connection, `pool=False`) — a similar type-introspection
incompatibility to the .NET case is suspected but unconfirmed; recorded
honestly in `clients/python-aruaru-db/README.md` with a new
`live-check.py` for future investigation. **(3)** Added a Mojo connector
(`clients/mojo-aruaru-db/`) — since no mature native Mojo PostgreSQL
driver exists, it thinly wraps the existing Python connector via
`from python import Python` interop; `is_safe_commit_id` is implemented
natively in Mojo (pre-network defense). No `mojo`/`magic`/`modular`
toolchain is installed on this machine, so the `.mojo` files are
uncompiled/unrun — stated plainly in the README, same honesty standard as
the Go/Java/Ruby connectors. The official thin-connector count is now 10
languages (Rust/Python/Node/PHP/COBOL/Go/Java/.NET/Ruby/Mojo).

## 2026-09-03(続き27) チェックポイント(aruaru-db 公式薄いコネクタ: 拡張プロトコルのライブ往復検証 + Go/Java/.NET/Ruby 新設)

ユーザー指示「拡張プロトコルのライブ往復検証(Rust/Node)を実施 + 未着手
コネクタ(Go/Java/.NET/Ruby)の追加、この２つをお願い」への対応。

### 拡張プロトコルのライブ往復検証(aruaru-db コミット `e4aef79`)
projection-fix 入り release バイナリ完成後、ローカル`aruaru-server`
(`:5433`、`ARUARU_USERS=app:secret`)相手に実施。
- **Rust `aruaru-db-connector`**: `cargo test -- --ignored` = passed
  (`connect` SCRAM/NoTls → `commit()` → `query_as_of()` 過去値`1`/最新`5`)。
- **Node `@aruaru/db`**: `npm i pg && node live-check.js` = OK(同上)。
  実装中に**実バグ1件発見・修正**: `commit()`が`SELECT aruaru_commit($1)
  AS commit_id`の別名に依存していたが、aruaru-dbは`AS alias`を無視し
  結果列名は関数名`aruaru_commit`のまま → 列名非依存(先頭列位置読み)へ
  修正。`node test.js` 4件green。
- Python(asyncpg未導入で実サーバ往復は未実施、単体4件はgreen)、PHP/COBOL
  はツールチェーン無しのため引き続き未実施。

### Go/Java/.NET/Ruby コネクタ新設(aruaru-db コミット `f418fa3`)
Rust/Nodeと同一方式(薄いラッパー、`commit()`は結果列を位置で読む、
`query_as_of()`はcommit_idを整数/安全な文字集合として検証してから
`AS OF COMMIT`へ埋め込み)。
- `clients/go-aruaru-db/`(`pgx/v5`ラッパー)、
  `clients/java-aruaru-db/`(Maven、`org.postgresql:postgresql`、
  既存`clients/java-jdbc/`を統合・削除)、
  `clients/dotnet-aruaru-db/`(`.csproj`、`Npgsql`)、
  `clients/ruby-aruaru-db/`(`pg` gem)を新設。
- **検証状況(正直な開示)**: このWindows環境に`.NET SDK`のみ導入済み
  だったため**.NETのみ実ビルド・実テスト**(`dotnet build`成功、
  `dotnet test` 10/10 green、ライブサーバ往復は未実施)。
  **Go/Java/Rubyはツールチェーン未導入のため未コンパイル・未テスト**
  (各READMEの「検証状況」節に正直に明記、PHP/COBOLと同じ扱い)。
- `docs/CLIENTS.md`・`clients/README.md`(日英両方)・`CLAUDE.md`
  (続き32、再開用メッセージ更新)も同コミットに含む。

### 作業上の注意点(次回の教訓)
サブエージェントへ委譲した際、最初の2回は「バックグラウンドエージェント
を起動した」という**計画の報告のみ**で実作業(ファイル作成・コミット)
をしていなかった(応答時間が20〜30秒と極端に短く、`git log`で検証して
発覚)。「あなた自身が直接ツールを使って実行しろ、他のエージェントを
起動するな」と明示的に再指示して初めて実作業(68ツール呼び出し・約
475秒)が行われた。委譲後は必ず`git log`/`git status`で実際の変更が
生じたか検証すること。また、この再指示と並行して別経路からも同種の
再開が走り、一時的に同一ファイルへの重複エージェント実行が発生した
(最終的には片方が正常にコミットし、もう片方は`TaskStop`で停止して
実害なし)。

**残作業**: Python asyncpgのライブサーバ往復検証(このセッションでは
未実施)。

## 2026-09-03(続き26) チェックポイント(aruaru-db HLC P-HLC-3 案A 全面移行 + open-cuda AWQ 量子化器 + クロスベンダー/OS 設計)

ユーザー指示「世界中の言語で Google/GitHub を調査して最新理論・設計思想を
新規設計書に活かしてから実装、実用的になるまで数回反復」。

### aruaru-db: HLC P-HLC-3(案A 全面移行、`docs/HLC_TIMESTAMP_REDESIGN.md` §6)
- 追加の一次資料調査(CockroachDB `util/hlc` は WallTime int64・Logical
  int32・Synthetic bool をパックせず別フィールド + `sync.Mutex`、uhlc-rs も
  `Mutex` + incoming が壁時計+delta 超で `Err`)。
- 内部を **`HlcTimestamp { wall_nanos: u64(切り捨て無し), logical: u32,
  synthetic: bool }`** へ刷新。順序 = `(wall_nanos, logical)` 辞書式。
  シフト・パックが無いので u64 オーバーフロー構造的に不可能。
  `Hlc` は `parking_lot::Mutex` 保護。
- **外向き u64 互換維持**: `as_ordinal()` は案B の 65µs 射影、`Hlc` が
  `last_ordinal` でクランプして `now_ordinal()` を厳密単調に。
  `now_ordinal`/`observe_ordinal`/`try_observe_ordinal`/`from_ordinal` は
  互換シグネチャ維持 → `closed_ts`/`wal_service`/GraphQL `closedTsAdvance`
  は無変更。
- 新 API: `now_hlc`/`observe_hlc`(フル精度)、
  `HlcTimestamp::uncertainty_upper(max_offset)`(CockroachDB の uncertainty
  interval 上端)。GraphQL `Query.hlcNow` 追加(観測専用)。
- 検証: `cargo test` aruaru-dist hlc 21 / graphql 21 / server 13、
  `cargo build --workspace` 成功、clippy 警告0。実 HTTP E2E(release):
  `hlcNow` が 17 桁のフル精度 Unix ナノ秒を返し(truncated ordinal では
  ない)、2 連続で ordinal 厳密増加、`uncertaintyUpperNanos = wallNanos +
  500ms`、`closedTsAdvance`(nowNanos 省略)は従来どおり有効。
  **案A 全面移行はこれで完了扱い。**

### aruaru-db: HLC P-HLC-3c/3d(続き27、`b96b7d5`)
- **P-HLC-3c**: `closed_ts` の follower read staleness を CockroachDB の
  uncertainty interval へ。`can_serve_uncertainty_safe_read_at(read_ts,
  max_offset)` = `[read_ts, read_ts + max_offset]` の全域が閉じ済み。
  `plan_uncertainty_safe_read`(`max_offset==0` は `plan_exact_staleness_read`
  へ委譲)。GraphQL `planFollowerRead(mode: "uncertainty-safe")`。
- **P-HLC-3d(ユーザー指摘「シフト・パックが無い?」への対応)**: 外向き
  u64 射影から**シフト・パック・切り捨てを完全撤去**。
  `as_ordinal() = wall_nanos + logical`(`<<16` も `& !0xFFFF` も、
  `advance_locked` のバケット分岐も削除、CockroachDB `hlc.go` `Now()` と
  ビット一致)。`from_ordinal = {wall_nanos: o, logical: 0, synthetic: true}`。
  `ORDINAL_*` 定数・`ordinal_bucket()` 削除。→ `closed_ts` 等が受け取る
  u64 は**フル精度 Unix ナノ秒スケール**、案B の 65µs 粒度の代償が消滅。
  `now_ordinal`/`observe_ordinal`/`closed_ts`/`wal_service`/`closedTsAdvance`
  は無変更。
- 検証: hlc 21 / closed_ts 9、フルスイープ dist 108 / graphql 22 /
  server 13、`cargo build --workspace` OK、clippy 新規指摘なし。
  実 HTTP E2E(release, `follower_read.max_offset_ms: 500`):
  `hlcNow` で `wallNanos == ordinal` 完全一致(17桁 `1788412243861359300`)、
  `uncertaintyUpperNanos == wallNanos + 500ms`。`closedTsAdvance(now=20s)`
  → closed=17s、`planFollowerRead(uncertainty-safe, staleness=1s)`
  → `route_to_leaseholder`、`staleness=4s` → `follower_read`
  `readTimestamp=16000000000`。**案A 全面移行は P-HLC-3a/b/c/d 完了。**

### open-cuda: AWQ 量子化器 + クロスベンダー×クロスOS 設計
- `pub fn quantize_conv1d_awq`(`load_conv1d_awq` の厳密な逆)+
  実重み相当ラウンドトリップテスト(逆量子化誤差 ≤ scale の 0.6 倍)。
  「合成テンソル厳密一致が検証上限」→「実重み相当の誤差評価」へ引き上げ。
  実 AutoAWQ ワイヤ形式互換は GPT-2 アーキの AWQ 公開モデルが無く未検証。
- `OmniGPU-Design.md` §11 新設: rust-gpu「running on every GPU」/ CubeCL /
  MoltenVK / `VK_EXT_shader_float8` + `VK_KHR_cooperative_matrix` の一次
  資料調査に基づくクロスベンダー×クロスOS 設計。Vulkan+SPIR-V を移植性の
  背骨と正式化、macOS は MoltenVK 経由 Vulkan を検証(新バックエンド不要)、
  FP8 移植性実装先を SPIR-V + Vulkan FP8/coop-matrix 拡張へ訂正
  (対応 HW = NVIDIA Hopper/Ada/Blackwell〈RTX 5080/5090〉∪ AMD RDNA4
  〈Radeon AI PRO R9700 等〉∪ Intel Arc B/Xe2)。実装変更は文言のみ。
- `cargo test -p open-cuda-llm --release` 47 passed / 7 ignored、clippy 警告0。

### English summary
aruaru-db: HLC "case-A" full migration — internal representation is now
`HlcTimestamp { wall_nanos: u64 (full precision), logical: u32, synthetic:
bool }` ordered by `(wall_nanos, logical)` (no shift/pack → the original
u64 overflow is structurally impossible), `Hlc` `Mutex`-guarded like
CockroachDB/uhlc-rs. The external u64 ordinal wire format is unchanged
(`as_ordinal()` = case-B 65µs projection, `last_ordinal` clamp keeps
`now_ordinal()` strictly monotonic), so `closed_ts`/`wal_service`/GraphQL
`closedTsAdvance` need no changes. New API: `now_hlc`/`observe_hlc` (full
precision), `uncertainty_upper`. GraphQL `Query.hlcNow` added. Verified
end-to-end over real HTTP. open-cuda: added `quantize_conv1d_awq` +
real-weight-like round-trip test (raises the verification ceiling beyond
synthetic exact-match), and `OmniGPU-Design.md` §11 — a researched
cross-vendor × cross-OS portability design (Vulkan+SPIR-V as the
backbone; macOS via MoltenVK, not a new backend; portable FP8 via
`VK_EXT_shader_float8` + `VK_KHR_cooperative_matrix`). Doc-only change;
still only verified on one NVIDIA GT 730.

### エコシステム横断の GPU 移植性設計見直し(5 リポジトリ)
ユーザー指示「dream-os / open-directx / open-cuda / aruaru-llm / aruaru-db の
新規設計・新規実装の見直しに活かす」。**正本は
`open-cuda/OmniGPU-Design.md` §11(クロスベンダー×クロスOS)・§12(横断
見直し)**。追加調査: vkd3d-proton/DXVK 3.0(`dxil-spirv`)・llama.cpp
バックエンド行列・「Llamas on the Web」(WebGPU)・MLC-LLM。方針:
- **SPIR-V を唯一の実行時 GPU IR**に(CUDA/HIP/Metal は任意の高速化経路)。
- **open-directx**: 並行バックエンド → DXBC/DXIL→SPIR-V フロントエンドへ
  役割再定義(vkd3d-proton が実証)。
- **dream-os**: GPU 実行系は open-cuda へ委譲、OS レベル割り当てのみ。
- **aruaru-llm**: バックエンド行列明示 + 起動時の能力交渉による自動選択、
  int8 活性化量子化(`dot_i8`/VNNI)配線、WebGPU/wasm は将来オプション。
- **aruaru-db**: 「外向き互換を保ちつつ内部を刷新」(HLC P-HLC-3 が実証例)。
各リポジトリの CLAUDE.md にこの正本へのポインタ HANDOFF を追記済み
(aruaru-llm `f2c9f62` / dream-os `27f8258` / open-directx `10e82bc`)。

### 2026-09-03(続き27)世界中の言語で Google/GitHub 再調査 → 設計書更新

ユーザー指示「OmniGPU-Design.md 等は世界中の言語で Google/GitHub 再調査
してから再編集して」。EN/JA/ZH + GitHub 中心で再検索。**§11.4 / §12.2-12.3
の設計方針は 1 行も撤回せず**、一次資料の更新のみ反映(`open-cuda`
`04f3bbb` = `OmniGPU-Design.md` §11.6 追加、consuming repos の CLAUDE.md
に「2026-09-03(続き)」節: open-directx `31e948d` / dream-os `f128639` /
aruaru-llm `99ea2f4`):
- **`EmbarkStudios/rust-gpu` は 2025-10-31 アーカイブ** → 「単一 Rust
  ソース → 全 GPU」のメンテ実装は **CubeCL(`tracel-ai/cubecl`)** と
  **wgpu+`naga`**(WGSL/SPIR-V → SPIR-V/MSL/GLSL/HLSL/DXIL、golden
  parity SPIR-V 87/87・MSL 91/91・HLSL 72/72)。
- **`VK_EXT_shader_float8`(E4M3/E5M2)は出荷ドライバ入り**: NVIDIA
  2025-06 / **AMD Adrenalin 25.10.2(2025-10)**。Intel 未確認。→ FP8
  移植性実装先(SPIR-V + Vulkan 拡張)は理論値 → 実前提へ格上げ。
- **Vulkan 1.4.342 `VK_QCOM_cooperative_matrix_conversion`**、llama.cpp
  Vulkan の拡張スタック(`VK_KHR_cooperative_matrix` +
  `VK_NV_cooperative_matrix2` + `VK_KHR_shader_integer_dot_product` +
  `VK_KHR_shader_bfloat16`、FOSDEM 2026)。
- **llama.cpp 2026-04 バックエンド非依存テンソル並列**(ベンダー混在可)。
- **`dxil-spirv` 2026-02 production SM 6.9**(DXBC は `dxbc-spirv`)→
  open-directx「DXBC/DXIL→SPIR-V フロントエンド」役割再定義の実現性確定。
- **WebGPU W3C Candidate Recommendation Draft(2026-05-21)**、WebLLM は
  ネイティブ比 ~80%、埋め込みは WebGPU が WASM 比 40〜75×。
- **Intel** Arc/Xe は Vulkan・SYCL 両対応、`intel/compute-runtime`
  (Level Zero)成熟 → Vulkan/SPIR-V の同一経路で扱う。

### 2026-09-03(続き28)クライアント接続・GPU 3ベンダー・インストーラ名

- **aruaru-llm `e74560a`**: `hardware.rs` に高VRAM帯 GPU 3ベンダーの実在
  確認(RTX 5090 32GB / RTX PRO 6000 Blackwell 96GB / **AMD R9700 32GB
  FP8 383 TFLOPS** / **Intel Arc Pro B60 24GB**、「RTX 5900」は非実在)。
  3ベンダーとも open-cuda の同一 Vulkan/SPIR-V 経路。ヒューリスティックは
  不変(gpt2-xl 上限)、テスト 6 件 green。
- **aruaru-llm `34cd004`**(続き27): `GET /v1/runtime` に llama.cpp 風
  `backend_matrix`(8 行、report only)、4 テスト、実 HTTP E2E、README 日英。
- **aruaru-db `90223a7`**: **`docs/CLIENTS.md`(日英)+ `clients/` コネクタ
  キット**新設。結論 = aruaru-db は **pgwire(:5433)+ GraphQL/HTTP
  (:4001)** の 2 標準契約だけを公開し、どの言語も**標準 PostgreSQL
  ドライバ**でそのまま繋がる → **独自ドライバ・`device-driver-installer.exe`
  は作らない**(「闇雲な代替を避ける」原則、独自変換層は速度をむしろ
  落とす)。同期/非同期はワイヤ同一、ハイブリッドは両対応ドライバ選択、
  OS 差は TCP+TLS に閉じる。Java/Rust(Axum・Poem・RPoem)/Python
  (FastAPI)/PHP(Laravel)/Go/Node/.NET/Ruby のレシピ + OS 別ドライバ
  入手表(Win/Mac/Linux/UNIX/z/OS メインフレーム/Android/iOS/iPadOS)。
  `clients/` に python-fastapi・rust-axum・php-laravel・java-jdbc の
  実行可能サンプル。配布物名が要る場合は `aruaru-db-<言語>-connector`。
  管理GUIインストーラ名を `aruaru-db-admin-win-installer.exe` へ統一
  (主 `aruaru-db-installer.exe` は既に規則どおり)。
- **aruaru-db `64f4366`(続き29)**: 公式 Rust コネクタ
  **`clients/rust-aruaru-db/`(`aruaru-db-connector` v0.1.0)** を新設。
  独自ドライバではなく `tokio-postgres` の薄いラッパー: `commit(msg)` /
  `query_as_of(base_select, commit_id, params)`(commit_id を
  `is_safe_commit_id` で検証、SQLi 防止)。`cargo test` 2 passed / 1
  ignored + doctest(ネットワーク不要ぶん green)。`docs/CLIENTS.md §3.8b`
  に **RPoem/Poem での使い方**: 「Poem 用ドライバ」は無いし要らない
  ——RPoem は Web FW で DB クライアントを指定しない。Rust 非同期 PG
  クライアント(`aruaru-db-connector` / `tokio-postgres` 生 / `sqlx`
  `PgPool` / RPoem 同梱 `open-runo-db::AruaruDbBackend`〈KV のみ、
  Git-on-SQL 非対応〉)をそのまま使う。pgwire は拡張プロトコル込みで
  PG 互換なので新規開発不要。
- **aruaru-db `b082b4c`(続き30)**: 公式薄いコネクタを **Python / Node /
  PHP / COBOL** へ拡張(いずれも標準ドライバ + `commit()`/`query_as_of()`、
  commit_id 検証で SQLi 防止):
  - `clients/python-aruaru-db/`(PyPI `aruaru-db`): `AruaruDb`(asyncpg、
    FastAPI)+ `AruaruDbSync`(psycopg v3、Django/Flask)。`unittest` 4
    passed(Python 3.14)。
  - `clients/node-aruaru-db/`(npm `@aruaru/db`): `pg` の薄いラッパー +
    `.d.ts`。`node test.js` 4 passed。
  - `clients/php-aruaru-db/`(Composer `aruaru/db`): `PDO` の薄いラッパー。
    `AruaruDb::fromPdo(DB::connection()->getPdo())` で Laravel の PDO 再利用。
    未検証(PHP なし)。
  - `clients/cobol/ARUARU.cob`: 埋め込み SQL 参照実装。pgwire なので
    ODBC(psqlODBC、**z/OS USS** 含む)/ libpq `CALL` / OCESQL で接続。
    未検証(COBOL 環境なし)。
  `docs/CLIENTS.md` §0.2 コネクタ表 + COBOL 行(言語マトリクス・OS 表)。
  次: Go / Java / .NET / Ruby の同種薄ラッパー、稼働 server でのライブ往復。
- **aruaru-db `1566c0b` + `177afb3`(続き31)**: 公式コネクタの**実サーバ
  往復検証中に実バグを発見・修正**。(1) `SELECT col ... AS OF COMMIT` が
  列射影を無視して常にフル行を返す既知制限(2026-07-13)が、型なし
  クライアントで「頼んだ列と違う値が返る」実害だった → `parser.rs` /
  `engine.rs::select_as_of`(`SELECT *`=フル行、列指定=その順・その列、
  不明列=Err)/ `aruaru-wire::describe_columns` を修正(RowDescription と
  DataRow の列数不一致による拡張プロトコル `error parsing response` も解消)。
  (2) 結果列は現状すべて `VARCHAR`(text)で返る → 型付きゲッターは使えず
  文字列で受けて parse(`docs/CLIENTS.md §5.1` に明記)。
  検証: `cargo test` aruaru-query 60 / aruaru-wire 10 / aruaru-graphql 22
  green。simple プロトコル実往復で `AS OF qty=1` 確認。**VPS 反映済み**
  (`1566c0b` active / healthz 200)。拡張プロトコルのコネクタ・ライブ
  往復(Rust `cargo test -- --ignored` / Node `node live-check.js`)は
  projection-fix 入り release バイナリのビルド完了待ち(このセッション中に
  ビルドが複数回タイムアウト/ロック競合で再実行)。CLAUDE.md 続き31 の
  「🛑 再開用メッセージ」に手順記載。

### 次回再開ポイント
1. aruaru-db: P-HLC-3c/3d は続き27(`b96b7d5`)で完了・VPS 反映済み。
   残りは復活用メッセージ項目5(Tauri 設定タブの `aruaru.yaml` 編集 UI 化)・
   項目6・項目7(P4〜P6)。
2. **aruaru-llm(次の実装スライス、最も着手しやすい)**: (A) `GET /v1/runtime`
   をバックエンド行列 + 能力交渉結果を返す形へ、(B) README 日英に llama.cpp
   風バックエンド表(CPU-SIMD=済/Vulkan=済/DXIL=済/Metal via MoltenVK=将来/
   HIP・SYCL=optional/WebGPU=将来)、(C) `ARUARU_LLM_ENABLE_*` を「未指定なら
   能力交渉で自動、指定なら override」へ(env 意味を変えない後方互換)。
3. open-cuda: macOS 実機での MoltenVK 経由 Vulkan 検証。FP8 対応 GPU が
   入手できた場合の SPIR-V + `VK_EXT_shader_float8` + `VK_KHR_cooperative_
   matrix` 経路実装。
4. open-directx: `dxil-spirv` vs `naga` の DXBC/DXIL→SPIR-V 変換比較 PR →
   `directx-shader-translate` をフロントエンドの薄いラッパーへ縮退。

---

## 2026-09-02(続き25) チェックポイント(aruaru-db: 真の別プロセス learner E2E + `disaster_backup.email` reconcile 配線)

残タスク3件のうち、この環境で完結できる2件を消化。

### (1) `--columnar-learner` 真の別プロセス learner の実 HTTP E2E(検証・バグ無し)
- leader(単一 voter)+ columnar learner を release バイナリで 2 プロセス起動。
- leader へ `POST /admin/cluster/propose` で CREATE + 5 INSERT → RaftWriter
  経由 commit → バイナリトランスポートで learner へ複製。
- learner の `columnar_pod`:
  `GET /columnar/gear` → `appliedIndex=6`(**同居モードの 0 と違い、`apply_at`
  が実 Raft ログインデックスを記録**)、`GET .../prune?...gt&25` →
  `skippedBlocks=2`、`GET .../gear?required_index=99999` → **409**
  (`stale:true`)、`required_index=6` → 200、DELETE 後
  `deletionVectorPositions=1`。バグは見つからず。

### (2a) `disaster_backup.email` の reconcile 配線(feature = "disaster_email_backup")
- `config::reconcile` に feature ゲート付きブロックを追加。`aruaru.yaml:
  disaster_backup.enabled: true` + 必須7フィールドで `DisasterEmailBackupConfig`
  を構築 → `AdminState::set_disaster_email_backup`(新設・REST と共通)で
  保管 + 稼働中 `RaftWriter` へ注入。`PartialEq` で冪等、欠落は warn のみ。
- `aruaru-dist::DisasterEmailBackupConfig::from_parts(...)` 追加。
- **pre-existing バグ修正**: feature 配下の REST ハンドラ 2 本の
  `check_admin_auth(req)`(1 引数)が `KeyGuardian` 追加以降コンパイル不能
  だった → `check_admin_auth(req, &state.keyring)`。
- テスト: `disaster_backup_email_reconcile_wires_config_and_is_idempotent`。

### 検証
- 既定: `cargo test -p aruaru-server` 13、`cargo build --workspace` 成功。
- feature: `cargo test -p aruaru-server -p aruaru-dist --features
  disaster_email_backup` → aruaru-server 14 / aruaru-dist 108 passed。

### 未着手(制約により不可、正直な開示)
- **HLC 案A 全面移行(P-HLC-3)**: P3 で GraphQL 化したばかりの API の再全面
  変更。過大なため保留。
- **open-cuda Hopper/Ada `sgemm_fp8_weight_vendor`**: H100/RTX40 + cuBLASLt
  FP8 が必要。開発機は GT 730 のため実装・検証とも不可能。
- **AWQ 実配布モデル E2E**: GPT-2 アーキテクチャの AWQ 公開モデルが事実上
  存在しない。合成テンソルの厳密一致テストが loader の検証上限。

### English summary
Two of three remaining next-phase items done in this environment. **(1)** The
true separate-process `--columnar-learner` path was verified end-to-end over
real HTTP: leader replicates via the binary transport to a learner process
whose `columnar_pod` now reports a real Raft log index (`appliedIndex=6`, vs
0 in co-located mode); `?required_index=99999` → 409, `?required_index=6` →
200; pruning and the deletion vector work. No bugs. **(2a)**
`disaster_backup.email` is wired into `config::reconcile` (feature
`disaster_email_backup`): declarative `aruaru.yaml` block → builds
`DisasterEmailBackupConfig` and injects into the live `RaftWriter` via a new
shared `AdminState::set_disaster_email_backup`; idempotent via `PartialEq`.
Fixed a pre-existing compile break in the two feature-gated REST handlers
(stale 1-arg `check_admin_auth`). Tests: default `cargo test -p
aruaru-server` 13 + `cargo build --workspace` OK; feature build 14 / 108
passed. **Still blocked (honestly)**: HLC case-A full migration (over-churn);
open-cuda Hopper/Ada FP8 vendor GEMM (needs H100/RTX40, this box is a GT
730); AWQ real-model E2E (no public GPT-2-architecture AWQ models).

### 次回再開ポイント
1. 復活用メッセージ項目5 後半 / 項目6(Tauri)・項目7(P4〜P6)。
2. HLC 案A 全面移行(P-HLC-3)。
3. Hopper/Ada 実機が入手できた場合の open-cuda FP8 ベンダー GEMM。

---

## 2026-09-02(続き24) チェックポイント(aruaru-db: `Query.htapReplicasAll` 全テーブル一覧)

続き23 の残りの1つ——`htapReplicas` の複数テーブル一括版——を実装。
TiFlash の `INFORMATION_SCHEMA.TIFLASH_REPLICA` が全 (db, table) 行を返す
のと同じく、テーブル名を知らなくても全列レプリカの同期状態を一覧できる
(監視サーフェスとしての実用性向上)。

- `ColumnarApplier::replicated_tables() -> Vec<String>`(`replica_state`
  のキー、ソート済み)。
- `htapReplicas` / `htapReplicasAll` 共通の `htap_status_for` ヘルパーへ
  切り出し。`Query.htapReplicasAll -> [HtapReplicaStatusGql]`
  (prune プレビューなし、列レプリカ無効なら空配列)。
- テスト: 2 テーブル目を足すと `htapReplicasAll` がソート順で両方返す。
  `cargo test -p aruaru-graphql` 20 / `-p aruaru-dist` 101、
  `cargo build --workspace` 成功。

### English summary
Added `Query.htapReplicasAll`, the multi-table version of `htapReplicas`
(like TiFlash's `INFORMATION_SCHEMA.TIFLASH_REPLICA` returning one row per
(db, table)): list the sync state of every columnar replica without
knowing table names. `ColumnarApplier::replicated_tables()` returns sorted
`replica_state` keys; a shared `htap_status_for` helper removes
duplication; `htapReplicasAll` returns `[HtapReplicaStatusGql]` (no prune
preview, empty when disabled). Test extended (second table → both returned
sorted). `cargo test -p aruaru-graphql` 20 / `-p aruaru-dist` 101,
`cargo build --workspace` OK.

### 次回再開ポイント
1. `--columnar-learner` 真の別プロセス learner での `?required_index=` 409 実 HTTP。
2. aruaru-db 復活用メッセージ項目5(`disaster_backup.email` reconcile)以降 /
   HLC 案A 全面移行(P-HLC-3)。
3. open-cuda: Hopper/Ada 実機での `sgemm_fp8_weight_vendor` 実装、AWQ 実配布
   モデルでの E2E。

---

## 2026-09-02(続き23) チェックポイント(aruaru-db: `Query.htapReplicas` を GraphQL 正式公開 + 続き22 (a)〜(d) 実 HTTP E2E)

続き22 の残り2件を実施。ユーザー指示「世界中の言語で Google/GitHub 調査を
実装に活かし、実用的になるまで数回繰り返す」に沿い、TiFlash /
CockroachDB のレプリカ観測手法を WebSearch 調査してから設計した。

### 調査
- TiFlash: `INFORMATION_SCHEMA.TIFLASH_REPLICA` の `PROGRESS`(0.0〜1.0)+
  `AVAILABLE`(0/1)。PROGRESS<1 は pushdown クエリのタイムアウト要因。
- CockroachDB: per-range closed timestamp がフォロワーリードの根拠。
  Raft パイプラインの end-to-end 観測は現状限定的(issue #72393)。
  → applied-index / progress / availability を一括で出す価値あり。

### 実装(aruaru-db)
- `QueryEngine::set_columnar_observer`(`olap_notify` と独立チャネル)。
- `ColumnarApplier::observing(shared_engine)` = 本番 `QueryEngine` を共有した
  同居(co-located)オブザーバモード + `observe_table` + `replication_progress`
  (TiFlash PROGRESS 相当)+ `replica_available`(AVAILABLE 相当)。
- `main.rs`: `aruaru.yaml: htap.columnar_replicas: true` で同居
  `ColumnarApplier` を立て `set_columnar_observer` 通知で追従、
  `AdminCtx.columnar` へ共有。
- `Query.htapReplicas(table, pruneColumn, pruneOp, pruneValue)` を新設。
  TiFlash `TIFLASH_REPLICA` 相当の同期状態 + 枝刈り込みプレビュー。

### 検証
- `cargo test -p aruaru-graphql` 20 / `-p aruaru-dist` 101 /
  `-p aruaru-query` 60 / `-p aruaru-server` 13、`cargo build --workspace` 成功。
- **実 HTTP E2E(release、`htap.columnar_replicas: true` +
  `max_offset_ms: 60000`)**: `/graphql` の `execSql` で CREATE+5 INSERT →
  同居オブザーバが自動追従(`replicationCount=6`)、`htapReplicas` が
  `available=true`/`progress=1.0`/`blockCount=6`/`liveRowCount=5`、
  prune `amount>250` で `skippedBlocks=2`/`keptLiveRows=3`、DELETE で
  `deletionVectorPositions=1`、未知テーブルは `available=false`。
  `/admin/closed-timestamp/receive` に far-future 値 → WARN で HLC 汚染前に
  拒否(`max_offset` 有効)。

### English summary
`Query.htapReplicas` is now a first-class GraphQL query on the production
`aruaru-server`. With `aruaru.yaml: htap.columnar_replicas: true` the
server runs a co-located `ColumnarApplier` sharing the production
`QueryEngine`, following writes via a new
`QueryEngine::set_columnar_observer` channel. The query returns TiFlash
`INFORMATION_SCHEMA.TIFLASH_REPLICA`-style `PROGRESS`/`AVAILABLE` plus a
pruning preview; design informed by a WebSearch pass over TiFlash's
columns and CockroachDB issue #72393. Verified end-to-end over real HTTP
`/graphql` (release build): auto-follow of `execSql` writes, prune / DELETE
deletion-vector / unknown-table / far-future `max_offset` rejection all
confirmed. Remaining: the true separate-process `--columnar-learner`
`?required_index=` 409 path; multi-table `htapReplicas`; HLC case-A full
migration (P-HLC-3).

### 次回再開ポイント
1. `--columnar-learner` 真の別プロセス learner での `?required_index=` 409 実 HTTP。
2. `htapReplicas` の複数テーブル一括版(TiFlash `TIFLASH_REPLICA` は全行返す)。
3. aruaru-db 復活用メッセージ項目5(`disaster_backup.email` reconcile)以降 /
   HLC 案A 全面移行(P-HLC-3)。
4. open-cuda: Hopper/Ada 実機での `sgemm_fp8_weight_vendor` 実装、AWQ 実配布
   モデルでの E2E。

---

## 2026-09-02(続き22) チェックポイント(aruaru-db 次フェーズ一括 + open-cuda AWQ/FP8ベンダー分岐、ビルドまで)

ユーザー指示「次フェーズ … 進めて」→「ビルドまでで記録」。実プロセス
HTTP E2E は未実施、`cargo test` / `cargo build --workspace` の成功までが
検証範囲。全スライスをリポジトリ別にコミット済み・未push分あり。

### aruaru-db(復活用メッセージ項目4 の (a)〜(d) を一括実装)
- **(a) `aruaru.yaml: htap` セクション**: `config::HtapConfig`
  (`columnar_replicas` / `read_consistency` / `delta.compaction_threshold`、
  static 扱い = reconcile で restart_required)。`ColumnarApplier::
  with_compaction_threshold`。`--columnar-learner` を `--config` 経由の
  `htap.delta.compaction_threshold` へ統合。`aruaru.example.yaml` 更新。
- **(b) `Query.htapReplicas` 相当の枝刈り込み観測 API**:
  `ColumnarApplier::prune_range_preview` / `prune_equality_preview`
  (MoR ビュー〈base+delta+deletion vector〉を `disproves`/bloom へ流し
  `HtapPrunePreview` を返す)。`GET /columnar/:table/prune?column&op&value`。
- **(c) A.6-3 Raft index + MVCC SI 検証**: `Applier::apply_at(index, cmd)`
  (既定は `apply` 委譲、既存実装無変更)。`ColumnarApplier` が
  `applied_index` / `applied_commit_seq` を記録。`read_at_index` が未達で
  `Err(StaleRead)`、達していれば `HtapReplicaView`。`GET /columnar/:table`
  に `appliedIndex`/`appliedCommitSeq`、`?required_index=&
  required_commit_seq=` 指定で未達なら 409 CONFLICT。
- **(d) HLC `max_offset`**: `Hlc::max_offset_nanos`(0=無効)+
  `try_update` / `try_observe_ordinal`(壁時計+max_offset 超のリモートは
  `Err(ClockSkew)`、permissive `update` はリモート無視でローカル進行のみ)。
  `config::follower_read.max_offset_ms`(動的、reconcile で HLC へ反映)、
  `closed_ts_receive` が `try_observe_ordinal` で遠すぎるリモート拒否。
  **案A 全面移行は `docs/HLC_TIMESTAMP_REDESIGN.md` P-HLC-3 として将来**。
- 検証: `cargo test -p aruaru-dist -p aruaru-server -p aruaru-graphql`
  失敗0、`cargo build --workspace` 成功(既存警告2件のみ)。

### open-cuda(直前エントリ「残課題」2件)
- **AWQ(interleave INT4)逆量子化ロード**: `open-cuda-llm::load_conv1d_awq`。
  `qweight [in, out/pack]` / `qzeros [in/group, out/pack]` /
  `scales [in/group, out]`、ニブル並び `AWQ_ORDER=[0,2,4,6,1,3,5,7]`、
  zero は実値、`w=(q-z)*scale`。`load_conv1d_maybe_quant` が
  `quant_method="awq"` で分岐(GPTQ 経路は従来どおり awq を拒否)。
- **Hopper/Ada ベンダー FP8 GEMM 分岐(コンパイルのみ)**:
  `GpuDevice::supports_fp8_tensor_core()`(既定 false)+
  `GemmPath::Fp8Tensor` + `select_fp8_gemm_path`。`sgemm_fp8_weight_vendor`
  はスタブ(明示エラー)、`sgemm_fp8_weight` は warn を出して既存の
  ソフトウェア dequant 経路へフォールバック(AVX-512 と同じ方針)。
- 検証: `cargo test -p open-cuda-llm --release` 46 / `opencuda-blas` 43、
  clippy 警告0、`cargo build --workspace --release` 成功。

### 次回再開ポイント
1. aruaru-db: `--columnar-learner` 2プロセス構成での実 HTTP E2E
   (`/columnar/:table/prune`、`?required_index=` の 409、
   `follower_read.max_offset_ms` を設定した `closed_ts_receive` 拒否)。
2. aruaru-db: `Query.htapReplicas` を GraphQL(`AdminCtx`)へ正式公開。
3. open-cuda: Hopper/Ada 実機での `sgemm_fp8_weight_vendor` 実装、
   AWQ 実配布モデルでの E2E。
4. aruaru-db 復活用メッセージ項目5(disaster_backup.email reconcile)以降。

---

## 2026-09-02 チェックポイント(open-cuda / aruaru-llm / aruaru-db 横断: F16/BF16/FP8ローダー + DialoGPT-small カタログ + aruaru-db A.6-4 段階2 Merge-on-Read)

ユーザー指示「123の順番で」の3項目を順に実施した。

**項目1 — open-cuda-llm ローダー拡張 + FP8/F8 演算カーネル(完了・push済み)**:
- 第一段(open-cuda `9c4ff39` / aruaru-llm `ef4004f`): `tensor_f32` を
  F32 のみから **F16・BF16(`half`)・FP8 E4M3・FP8 E5M2(OCP仕様準拠の
  自前デコーダ)→f32 変換**へ拡張。対話FT済み GPT-2 互換モデル
  (DialoGPT-small、F16 配布)を実際にロード可能に。`model_catalog` へ
  `dialogpt-small` + `tokenizer_hf_repo`(gpt2 の tokenizer 流用)追加。
- **第二段(ユーザー追加要望「FP8とF8演算カーネルを実装」「対応外dtype
  のエラーを修正」、open-cuda `b9fae40` / aruaru-llm `b9eb255`)**:
  `opencuda-blas` に FP8(E4M3/E5M2)量子化 API + **`sgemm_fp8_weight`
  (dequant-on-the-fly GEMM = FP8 演算カーネルの実体)**。`tensor_f32` が
  F64 + 全整数/真偽 dtype(BOOL/U8..U64/I8..I64)も**直接キャストで**
  読めるようになり「対応外エラー」は真に未知の dtype のみへ。
  `GptModel::enable_fp8_weights`(opt-in)+ aruaru-llm 側
  `ARUARU_LLM_ENABLE_FP8_WEIGHTS=e4m3|e5m2` 配線。**正直な開示**:
  GT730 に FP8 Tensor Core が無く softwareパスで、利益は重みメモリ 1/4
  であり速度ではない。実 HTTP E2E(distilgpt2 で配線ログ発火 →
  `/v1/generate` がコヒーレントな英文、f32 版と僅かに異なる継続)確認済み。
- **第三段(ユーザー追加要望「対応外dtype(INT8/INT4)は正直なエラー。
  対応して」、open-cuda `4f27a41`)**: **GPTQ(AutoGPTQ 形式)の
  INT4/INT8 量子化モデルの逆量子化ロード**。GPTQ は単一 dtype ではなく
  「I32 ビットパックの `qweight` + `scales` + `qzeros` + `config.json` の
  `quantization_config`」で表現されるため、`GptModel::load` がそれを
  自動検出して `w = (q - (zero+1)) * scale` で復元。AWQ(interleave
  パック)は正直なエラーで拒否。合成 4bit テンソルの厳密一致テスト。
  aruaru-llm 側はコード変更不要(`GptModel::load` を呼ぶだけ)。
  open-cuda-llm 45 / aruaru-llm 101 passed、clippy 0件。

**項目2 — Model Folding 残課題(前回=続き2 で Attentionスキップ軽量パス
完了済み)**: 高性能統合GPUでの再実測はこの機に該当GPUが無く未達、
日本語較正データの品質定量評価は未着手(いずれも前回チェックポイントの
記録から変更なし)。

**項目3 — aruaru-db A.6-4 段階2「base+delta の Merge-on-Read」(完了・push済み)**:
`ColumnarApplier` を都度フル再構築から base+delta 方式へ格上げし、
続き18 が「まだ残る配線」と明記していた**実 DELETE/UPDATE 発生時に
deletion vector を立てる書き込み側の経路**を実装(aruaru-db `0d51944`、
`crates/aruaru-dist/src/columnar_applier.rs`)。DELETE/PK変更UPDATE は
該当 block の `deletion_vector` へ位置を insert(block 実体は書き直さない
= 即時 rewrite 無しの MoR)、INSERT/内容変更UPDATE は小さな delta block を
追加、閾値8で base へ compaction。`columnar_pod` の `GET /columnar/:table`
に `columnarBlockCount`/`columnarLiveRowCount`/`columnarDeletionVector
Positions` を追加。8ユニットテスト green、aruaru-dist 91 / aruaru-backup 45
失敗0、`cargo build --workspace` 成功、**2プロセス実HTTP E2E**
(leader + `--columnar-learner`)で in-place UPDATE → deletionVectorPositions 1、
DELETE → 2、blockCount は書き直されず維持、liveRowCount が行ストアミラーに
追従することを実証。詳細は `aruaru-db/CLAUDE.md` の続き20 エントリ。
**項目3 追加 — HLC タイムスタンプの設計ミス修正(ユーザー指摘
「オーバーフローする設計を一から設計し直して新規設計書をまず完成させて」、
aruaru-db `0ead341`)**:
`hlc.rs` の `as_nanos()` が実 Unix ナノ秒 `pt` を `<<16` して u64
オーバーフローしていた。一次資料調査(CockroachDB は物理/論理を別
フィールドでパックしない、compact 版は物理を ms/µs 粒度へ落とす)に
基づき **`docs/HLC_TIMESTAMP_REDESIGN.md` を新設**、案B(物理を
65.536µs 粒度へ切り捨てて下位 16bit に論理を収める=左シフトなし=
オーバーフローなし=厳密単調)を採用。`hlc.rs` 全面書き換え(13テスト)、
`closed_ts` 系の「now 既定値」を HLC ordinal へ配線(`AdminState`/
`AdminCtx` 共有、`closed_ts_receive` で `observe_ordinal`)。
aruaru-dist 95 / aruaru-graphql 19 / aruaru-server 13 passed、
実 HTTP E2E で `closedTsAdvance`(now 省略)が実 Unix ナノ秒スケールの
単調 ordinal `1788327316574937600` を返し、旧 REST は 404 を確認。

**残り(要求③実装トラック)**: `aruaru.yaml: htap` セクション(§5・A.7、
`columnar_replicas`/`read_consistency`/`delta`)+ `--columnar-learner` の
宣言的設定経由起動への統合、`Query.htapReplicas` 相当の枝刈り込み
観測 API、A.6-3(Raft index + MVCC SI 検証)、HLC の案A全面移行・
`max_offset` スキュー上限(`docs/HLC_TIMESTAMP_REDESIGN.md` P-HLC-3、将来)。

**VPS(ユーザー指示「aruaru-llm/open-cuda も VPS 対象にして」)**:
- open-english(項目2、続き2)は既にデプロイ済み。
- **aruaru-llm を新規に VPS デプロイ**(`/root/aruaru-llm`、open-cuda を
  隣に clone してビルド、systemd `aruaru-llm.service`)——従来「利用者PC
  上で動作、VPS 非対象」としていた方針をユーザー指示で変更。open-cuda は
  aruaru-llm へ path 依存でビルド時に取り込まれる(単体サービスは無い)。
- aruaru-db は `/root/aruaru-db` へ `git pull` + `cargo build --release
  -p aruaru-server` + `systemctl restart aruaru-server`(続き19 の
  `ln -sf /root/open-raid-z /root/repository/open-raid-z` パス不整合対応が
  必要な場合あり)。

---

## 2026-09-01(続き2) チェックポイント(open-cuda + aruaru-llm + open-english: Attentionスキップ軽量パス実装 + 「open-cudaは必須の相方」明文化)

**背景**: 直前チェックポイント(d631cf1)の「未着手・次回検討候補」に
明記されていた **open-cuda + aruaru-llm + open-english の3リポジトリに
またがる開発** ——「線形アダプタ折りたたみで潰した層のAttentionを、
出力をゼロで捨てるだけでなく推論時に丸ごとスキップする軽量パス」——を
実装した。あわせてユーザー指示「aruaru-llmを使うリポジトリは全て
open-cudaも一緒にSETUPすべきことを日英で明記、またはインストーラー
同梱」へ対応した。

### 実施内容

1. **Attentionスキップ軽量パス(3リポジトリスライス)**:
   - **open-cuda**(`crates/open-cuda-llm/src/lib.rs`、正本): `DecoderLayer`
     へ`skip_attention: bool`(既定`false`、`linear_adapter`のみ`true`)。
     `forward_step`/`forward_prefill`が`skip_attention`時にln_1・QKV射影・
     softmax・P·V・attn_out・KVキャッシュpushを一切実行せず残差だけを
     FFNへ渡す。`linear_adapter`の`qkv`/`attn_out`はゼロ出力なので
     **ビット単位で数値等価**(生成トークン列が1トークンも変わらない)。
     `AdapterFoldReport`へ`attention_compute_skipped: bool`追加。
   - **aruaru-llm**: `FoldResult`/`FoldLayersResponse`へ
     `attention_compute_skipped: Option<bool>`(線形アダプタ版のみ
     `Some(true)`)、`POST /v1/models/fold-layers`レスポンスへ反映、
     disclosure文(日英)更新。
   - **open-english**: `index.html`のfold-layers開示文へ日英併記で追記、
     `app.js`がレスポンスの新フィールドをステータス欄へ表示。
   - **検証**: open-cuda `cargo test -p open-cuda-llm --release --
     --test-threads=1` **35件全green**(新規bitwise等価テスト
     `linear_adapter_attention_skip_is_bitwise_identical_to_computing_zeroed_attention`
     ——skip有無で`generate()`出力がバイト完全一致することを確認)、
     `cargo clippy ... -- -D warnings` **警告0件**(既存の
     `explicit_counter_loop` 1件も併せて修正)。
     aruaru-llm `cargo test --release -- --test-threads=1` **101件全green**。
     open-english `node --check` OK + 実ブラウザで白画面なし・新開示文が
     DOMに存在を確認。
   - **CPU実測(開発機、`--ignored`ベンチ2件)**: 合成モデル(12層中8層
     折りたたみ)で**約19%高速化**(731ms→899ms/gen)、実GPT-2 124M
     (12層中6層折りたたみ)で**生成トークン列がskip有無でバイト完全
     一致**を確認した上で**約9%高速化**(1.175s→1.289s/gen)。
   - **実HTTP E2E検証(distilgpt2、実aruaru-llmサーバー)**: `POST
     /v1/models/fold-layers`(`use_linear_adapter:true`)のレスポンスが
     `attention_compute_skipped:true`・`ridge_lambda_used:0.5`を返し、
     `completion_after_fold`が劣化ループではない実在英文を生成、
     折りたたみ後も`/v1/generate`が正常動作、閾値方式では`null`に
     なることを確認。

2. **「open-cudaは必須の相方」明文化**: 調査の結論——**open-cudaは
   `aruaru-llm`バイナリへ静的リンクされるため別途同梱・別プロセス
   起動は不要**。`fetch-aruaru-llm.ps1`/`.sh`が取得するリリース済み
   `aruaru-llm`実行ファイルに`opencuda-*`(GEMM・Attention・GPT-2
   デコーダ・埋め込み・音声認識)が既に含まれる。ソースからビルドする
   場合のみ隣に`open-cuda`のcloneが必要(CIは`release.yml`が自動clone)。
   Vulkan/DirectX GPUバックエンドだけは`aruaru-llm`側のGPUビルド
   (`installgpu`タスク、既定オフ)使用時のみ有効。
   `aruaru-llm/README.md`・`README-English.md`に「open-cudaは必須の
   相方(SET)」節を新設(正本)、`open-english/installer/{windows,unix}/
   fetch-aruaru-llm.{ps1,sh}`のコメントにも日英併記で追記。

### 次にすべきこと

1. open-englishのUIボタン(fold-layers実行フォーム)から実際にボタン
   操作でこの経路を通す実ブラウザ検証(今回は`curl`での実HTTP検証まで)。
2. 実GPU経路(Vulkan/DirectX)でのskip有無の速度比較(今回はCPU実測のみ)。
3. 前回チェックポイントの残課題(2)(高性能統合GPUでの再実測)、(3)
   (日本語較正データの品質定量評価)は引き続き未着手。

### コミット・デプロイ

- open-cuda / aruaru-llm / open-english / RUNO をコミット・push。
- open-englishのVPS(`easy-web.tokyo`)へ`index.html`/`app.js`の
  fold-layers開示更新を反映(静的HTMLのためサーバー再起動不要)。

---

## 2026-09-01 チェックポイント(open-cuda + aruaru-llm + open-english: Model Folding残タスク4項目完了、セッション末尾のため記録)

**背景**: 直前セッションで実装した「Model Folding」(層冗長性検出+
実際の層折り畳み、3手法: 独立閾値/連続ブロック探索/線形アダプタ)に
ついて、ユーザーから明示された4つの未着手タスクへ対応した。

**実施内容(全4項目、実機検証済み)**:

1. **`ridge_lambda`外部化**: `open-cuda`側`fold_block_with_linear_
   adapter`に`ridge_lambda: Option<f32>`引数を追加、`aruaru-llm`側
   `POST /v1/models/fold-layers`のリクエストパラメータ経由で調整
   可能に。非有限・非正値は`ensure!`で拒否。テスト実行・pass確認済み。
2. **open-english UIボタン**: `index.html`/`app.js`に`fold-layers`を
   実際に呼ぶフォーム+ボタンを実装。稼働中aruaru-llmサーバー
   (`127.0.0.1:4601`)へ実HTTPリクエストを送り、`ridge_lambda_used`が
   正しく反映され折りたたみ前後とも自然な英文が生成されることを確認。
3. **GPU実測**: 実機(NVIDIA GT 730)でVulkan/DirectX経由のベンチマーク
   を実際に実行(`--ignored`テスト)。結果: CPU 1.96〜2.07秒に対し
   DirectXは4.0〜4.6秒(約2倍遅い)、Vulkanは32〜44秒(約17〜22倍遅い)
   ——GPUの方が明確に遅いという結果を誇張せずそのまま記録した。
4. **多言語較正**: 英日中仏独西6言語の較正プロンプトを新設し、fold系
   3関数の既定較正データへ配線。日本語プロンプトを含む較正データで
   実GPT-2重みの折りたたみを実行し、クラッシュしないことを確認
   (品質が英語と同等とまでは主張していない——語彙が英語中心のBPE
   トークナイザのため)。

**注意点**: このセッションでは並行して複数のバックグラウンドエージェント
を起動しており、うち何回かは「エージェントを起動しました」という空虚な
報告のみでツール呼び出し1回・実質作業ゼロのまま終了する不具合が発生した
(委任を繰り返す再帰的な問題)。「委任するな、自分で直接ツールを使え」と
明記した指示でようやく実質的な作業に至った。今後同様の作業を依頼する際は、
この失敗パターンを踏まえて指示すること。

**コミット**: open-cuda `b6e8c3b`、aruaru-llm `071a50a`、open-english
`1bfbed2`(いずれもpush済み、日英併記でCLAUDE.mdに記録)。

**残課題**: (1) Attentionサブ層を完全スキップする軽量パスは未実装、
(2) より高性能な統合GPU(過去実測のAdreno 619等)での再実測は該当
ハードウェアが無く未検証、(3) 日本語較正データでの生成品質の定量評価
(現状は「クラッシュしないこと」の確認止まり)。

---

## 2026-08-29 チェックポイント(open-english + aruaru-llm: AI音声認識(ASR)精度の抜本改善、セッション末尾のため記録)

**対象リポジトリ**: `open-english`(branch `master`、集中)、`aruaru-llm`
(branch `main`、`POST /v1/transcribe` 新設)。関連参照のみ:
`open-directx` / `open-cuda` / `open-cpu`(既存の推論基盤、今回コード変更なし)。

**正本**: `open-english/docs/SPEECH_RECOGNITION_REDESIGN.md`(英日・多言語で
Google/GitHub 調査した結果 + 3 フェーズ設計 + 試作駆動の進め方 + 受け入れ
基準)。各リポジトリの詳細は `open-english/CLAUDE.md` / `aruaru-llm/CLAUDE.md`
の 2026-08-29 HANDOFF。

### 到達点

- **P1(クライアントのみ・新規依存ゼロ、`open-english/app.js`)= 実装済み**:
  P1-α `speechLangTag()`(BCP-47 言語タグ、ja/en 固定を廃止)、
  P1-β `refineTranscript(alts, langTag)`(n-best → 1 回の LLM 訂正、
  空/過長は却下して 1-best へ)、P1-β2 `lastTrainerUtterance()`(直前
  トレーナー発話で contextual biasing)、P1-γ `speechTranslationHelper()`
  (話した内容を母国語へ翻訳して補助表示)。
- **P2-α(ブラウザ内 Whisper、transformers.js)= 実装済み**: 実行段
  カスケード WebGPU → WebNN(npu/gpu/cpu)→ WASM(スレッド数は
  `/v1/cpu-runtime` = open-cpu ヒント)。マイク押下で Web Speech API と
  `MediaRecorder` を並行起動、認識終了時に Whisper 候補 + Web Speech
  n-best を融合。モデル/ランタイムは `fetch-whisper-model.ps1` +
  `whisper-model-installer.exe` + `server` の `maybe_fetch_whisper_model()`
  で同一オリジン配信。未配置なら静かに無効化 → Web Speech API 単独
  (回帰ゼロ)。
- **2026-08-29 多言語再調査を反映**: transformers.js の dtype 落とし穴
  (WebGPU + q8 デコーダは出力が壊れる)→ **fp32 encoder + q4 decoder の
  ハイブリッド**へ修正。tfjs は 3.8.1 固定(v4-next はタイムスタンプ
  回帰)。幻覚対策の `condition_on_previous_text:false` 等を追加。
- **P2-β(`aruaru-llm` の `POST /v1/transcribe`)= ✅ 完了(方針変更込み)**:
  `whisper-rs` 直リンクは Windows/MSVC ビルド不能(`0.16.0` でも
  `WHISPER_DONT_GENERATE_BINDINGS=1` でも解消せず、issue 2026-04-21)→
  **whisper.cpp のプレビルド CLI(`whisper-cli`)を子プロセス起動**する
  方式へ全面書き換え(`pg_dump` / `adb` と同じ)。Cargo feature 撤去。
  `is_available()` = `cli_present && model_present` の実行時判定。
  `cargo test --release` **100 passed / 1 ignored**。実 CLI + 実 GGML
  での E2E のみ未達。
- **P2-α を VPS 本番(`easy-web.tokyo/open-english/`)へ実配信・実ブラウザ
  検証済み**: Linux 用 `installer/unix/fetch-whisper-model.sh` 新設、
  ORT は jsep 統合ビルドのみ、`app.js` の vendor/model パスをアプリの
  ベース(`/` or `/open-english/`)からの相対に。`open-english-server`
  再ビルド・再起動、モデル配信ルート全 200、`loadWhisperModule()` 成功。
- **P2-γ(`open-english`)= ✅ 3 経路融合を配線済み**: `serverTranscribeBlob()`
  新設。可否は `lastRuntimeInfo.whisper`(`GET /v1/runtime`)で判定、
  到達不可なら静かにスキップ。`finalizeVoiceInput()` が
  `Promise.all([whisperTranscribeBlob, serverTranscribeBlob])` で並行実行し
  `serverAlts.concat(whisperAlts).concat(speechAlts)` を `refineTranscript()`
  へ。VPS 配信済み、実ブラウザで関数定義・f32→base64 往復を確認。
- **付随のサービス向上(ユーザー確認の上)**: (a) HTTPS 配信時に
  aruaru-llm の平文 HTTP プローブをやめ Mixed Content エラーを解消
  (実ブラウザで消失を確認)、(b) VPS の `open-english.service` の平文
  SMTP パスワードを `/etc/open-english.env`(mode 600)+ `EnvironmentFile=`
  へ移設(`systemctl cat` に出なくなった、`request-otp` が `{"sent":true}`
  で SMTP 継続動作を確認)。

### 到達点(続き、2026-08-29 セッション後半)

- **P2-γ VAD = ✅ 2 段実装済み**(`open-english/app.js`):
  - 第一段 `trimSilenceVad()`(依存ゼロ・DLゼロの RMS ベース、30ms/10ms
    フレーム、適応しきい値でトリム)。VPS 実ブラウザで 3s 合成音→1.44s 確認。
  - 第二段 `sileroVadTrim()` = **Silero VAD(ONNX v5、`onnx-community/
    silero-vad` ~2.2MB)**。transformers.js は `InferenceSession` を公開
    しないので standalone `onnxruntime-web@1.22.0`(非 jsep wasm 一式)を
    `/vendor/ort-vad/` へ**完全隔離**して vendor。512 サンプルごとに発話
    確率 → ヒステリシス + 最小発話長 + ギャップ連結で発話区間へまとめ
    **内部の無音も落とす**。`vadTrim()` = Silero → RMS フォールバック
    (必ず有効 PCM、回帰ゼロ)。**VPS 実ブラウザ検証**: セッションロード
    849ms、I/O 名自動検出(`input`/`state`/`sr`→`output`/`stateN`)、
    推論 89ms/3s、合成音は非発話と正しく判定(誤検出なし)。
- **P2-β contextual biasing = ✅**: `/v1/transcribe` に `prompt` フィールド
  (`aruaru-llm`、末尾1000字に切詰 → `whisper-cli --prompt`)。`open-english`
  の `serverTranscribePcm()` が `lastTrainerUtterance()` を送る。
- **評価ハーネス(§5)= ✅ 実装済み**: `open-english/tools/asr-bench/wer.mjs`
  (依存ゼロ Node、`--ref`/`--hyp`/`--keywords`/`--md`。NFKC 正規化 →
  語 or 文字 Levenshtein、`lang`+空白率で CJK 自動判定、kw-recall =
  R-WER 近似、`missing` = 取りこぼし数、言語別内訳。自己テスト済み)+
  `split-bench.mjs`(`window.__asrBench` → `hyp-*.jsonl`)+ `app.js` の
  `localStorage["openEnglish.asrBench"]="1"` ダンプ + `docs/asr-eval/`
  (README・`refs.example.jsonl`・`keywords.example.jsonl`・`.gitignore`)。

### 次にすべきこと(他アカウントでの再開ポイント)

1. **実機 E2E(最優先、実マイクが要る)**: `open-english` をブラウザで開き
   `localStorage.setItem("openEnglish.asrBench","1")` → 各発話を話す →
   `copy(JSON.stringify(window.__asrBench))` → `split-bench.mjs` →
   `wer.mjs --md` で WER/CER を出し `docs/asr-eval/README.md` の結果ログへ。
   同時に、利用者 PC へ プレビルド `whisper-cli` + `ggml-base.bin` を置いて
   `POST /v1/transcribe` の実書き起こしと Silero の実発話セグメント抽出を確認。
2. **Moonshine を低遅延エンジン候補に**(`open-english`): 27M・量子化 ONNX
   ~50MB、日本語版 `moonshine-tiny-ja-ONNX` あり。Whisper より軽速。
   `getWhisperPipeline()` 相当を Moonshine 用に足し、融合リストへ 4 本目として。
3. **P3(`aruaru-llm`)**: Parakeet-TDT-0.6B-v3 / Canary-1B-v2 / Omnilingual
   ASR を `/v1/transcribe` の選択可能エンジンに(`whisper-cli` と同じ
   「プレビルドバイナリを子プロセス」パターンで)。評価は Open ASR
   Leaderboard(多言語 + long-form)を `docs/asr-eval/` 基準に。

### コミット(すべて push 済み)

- `open-english@master`: `c26d7ca`(P2-α)→ … → `6671dde`(P2-γ 3 経路融合)
  → `571c8de`(評価ハーネス)→ `1eeef9f`(RMS VAD + PCM 一回デコード)→
  `da8d960`(Silero VAD)→ `2f85996`(standalone ORT loader)→ `3310bd4`
  (ORT を非 jsep で完全隔離)→ `6914a0a`(Silero VPS 検証記録)→ `ec28ffa`
  (serverTranscribePcm が prompt を送る)。
- `aruaru-llm@main`: `78a85e3`(P2-β API)→ … → `24bcfd1`(**方針変更実装** =
  whisper-cli 子プロセス、feature 撤去、100 テスト)→ `4e9ddb4`(README/
  CLAUDE/PORTING を CLI 方式へ)→ `b98b928`(`/v1/transcribe` に `prompt`)。
- `RUNO@main`(旧 runo): 本チェックポイント。
- **VPS(easy-web.tokyo)反映済み**: `/root/easy-web.tokyo/open-english` を
  最新へ、`open-english-server` 再ビルド・再起動、Whisper モデル + ORT +
  Silero VAD + vendor 一式を配信(全ルート 200)。`aruaru-llm` は利用者 PC
  側で動く設計のため VPS には配置しない(コードは GitHub 上)。

---

## 2026-08-29 チェックポイント(aruaru-db: REST 完全撤廃 P3 本体 + 付録A「2026最新設計」再構成、並列セッションで実施)

**対象リポジトリ**: `aruaru-db`(branch `main`)。**この ASR セッションと
並列**でバックグラウンドエージェントが実施。再開起点は
`aruaru-db/CLAUDE.md` 冒頭「🛑 復活用メッセージ」+ HANDOFF「続き10」、
正本は `aruaru-db/docs/CONTROL_PLANE_REDESIGN.md`。

### ユーザーの不変要求(逸脱禁止)
①SET 全体から REST を例外なく完全撤廃・中途半端禁止 ②RPoem は
WunderGraph Cosmo 互換・API キー完全自動ライフサイクル ③CockroachDB×
Snowflake ハイブリッド変種(TiDB 等、**関連全て**)の実装理論・技術を
取り込む ④世界中の言語で再調査し実用的になるまで再設計・再実装・
再テストを反復。**実装 P3 より ③ の調査・再設計を優先**。

### 到達点(push 済み `origin/main` `23ff114..250956d`)

- **③④ = ✅ 完了**: 英日独露中で 15 検索(一次論文・公式 doc・GitHub)。
  `docs/CONTROL_PLANE_REDESIGN.md` 付録 A を **59 → 約480行**へ全面再構成。
  TiDB/TiKV+TiFlash(DeltaTree=B+木×LSM、FFI push、**read-index SI 検証
  アルゴリズム**)・CockroachDB(Range/HLC/Pebble/closed ts/protected ts、
  MVCC range key)・YugabyteDB(DocDB/IntentsDB)・Snowflake(不変16MB
  マイクロパーティション/pruning/time travel)・**Neon vs Aurora**
  (safekeeper Paxos `flushLsn[n-quorum]` / pageserver materialize)・
  SingleStore(Universal Storage 5機能)・ClickHouse(MergeTree granule /
  **SharedMergeTree + Keeper**)・Iceberg/Delta/Hudi/**Paimon・Fluss**
  (deletion vector の RoaringBitmap レイアウト、MoR、record-level index、
  merge engine)・Photon/DuckDB(FSST/ALP、adaptive kernel 選択)を
  **実装方法(アーキ/データ構造/アルゴリズム)まで**、出典 URL 併記。
  取り込み判断を明記: **取り込む** = HLC(アルゴリズム明記)/
  **Raft-Learner 上の行→列非同期変換レプリカ(本命、`ColumnarApplier` 案)** /
  read-index+MVCC SI 検証 / deletion vector+MoR(段階的)。**条件付き保留**
  = 型認識軽量圧縮。**取り込まない(理由明記)** = Aurora 型モノリシック
  ストレージ。A.7 に `aruaru.yaml: htap` セクション案 + execution-config
  配布案、A.8 に「2026 業界の現実(単一エンジン HTAP は専用OLTP+専用
  OLAP+CDC に対しシェアを取れていない)」。
- **① P3 本体 = 3/5 群完了**: `closed-timestamp` / `wal-service` /
  `sharded-store` を GraphQL 化し REST 撤廃(`admin.rs` からルート・
  ハンドラ・構造体7個・`now_nanos()` 削除、`AdminCtx` へ `Arc` 注入 =
  `object_table`/`keyring` と同一パターン、safekeeper 列挙 off-by-one
  是正)。**着手前に grep で Tauri/Android/web クライアントの当該 REST
  参照が皆無なことを確認**。タイムスタンプ・LSN は GraphQL では String。
  `/closed-timestamp/{receive,publish}` は B4(ノード間 side transport、
  既にバイナリ)として残置。
- **次スライスへ(技術的理由を doc §8 P3・CLAUDE.md 続き10 に明記)**:
  `ephemeral-query`(`current_exe()`+`Command` で自プロセス再起動する
  `aruaru-server` バイナリ固有 → `Arc<dyn EphemeralRunner>` trait 注入が
  必要)、`multi-raft`(`MultiRaftCluster<crate::cluster::EngineApplier>`
  が server-local ジェネリック → trait object 化 or applier のクレート
  移設が必要)。状態注入だけで済んだ 3 群とは規模が別、というのが
  「回した」理由。
- **検証**: `cargo build --release -p aruaru-graphql -p aruaru-server`
  成功(11分17秒、既存 `build_cluster`/`propose_commit` の 2 警告のみ)。
  `cargo test -p aruaru-dist -p aruaru-graphql -p aruaru-server` 失敗 0
  (72 + 16 + 13、**新規 3 テスト**が closed_timestamp / wal_service /
  sharded_store を GraphQL だけで完結させ共有状態への実読み書きを検証)。
- **README.md / README-Japan.md / README-English.md / PORTING.md §7 /
  CLAUDE.md** を日英で整合。

### 続き(2026-08-31、別アカウント/別セッションで再開・完了分)

1. ✅ **実プロセス HTTP E2E**: 実 `aruaru-server` を起動し
   `closedTimestamp`/`walService`/`shardedStore*`/`selfIssueKey` を
   `/graphql` へ実 HTTP で確認、旧 REST パスが正しいトークン付きで
   実際に `404`(トークン無しの `401` に惑わされないことも確認)。
2. ✅ **`ephemeral-query` の GraphQL 化**: `EphemeralRunner` trait +
   型を `aruaru-dist::ephemeral` へ移設(`admin_shared.rs`/
   `keyring.rs`と同パターン)、`ProcessEphemeralRunner`
   (`aruaru-server`)が実装、`Mutation.ephemeralQuery`新設。実プロセス
   E2E(federatedQueryでテーブル作成→ephemeralQueryが実際に子プロセス
   を起動しSELECT結果を返す)まで確認済み。commit `c30a6b5`→`8bfec95`。
3. ✅ **`multi-raft` の GraphQL 化(P3 本体、最終スライス)**:
   `EngineApplier`を`aruaru-server::cluster`から`aruaru-dist::
   engine_applier`へ移設し、`aruaru-graphql`が`MultiRaftCluster
   <EngineApplier>`を具体型のまま共有(trait object化は不要と判明)。
   `Query.multiRaftScatterQuery`・`Mutation.multiRaftSplit`/
   `multiRaftMerge`新設。実プロセスE2E(split→scatter→merge の
   range数遷移1→2→1を実HTTPで確認、旧REST`/admin/multi-raft/*`は
   トークン付きで404)まで確認済み。commit `afb4826`。
   **これでP3本体(closed-timestamp・wal-service・sharded-store・
   ephemeral-query・multi-raft)が全て完了**。

### 続き2(2026-08-31、要求③実装トラック着手・完了分)

4. ✅ **A.6-1 HLC**: `aruaru-dist::hlc`(CockroachDB/Spanner方式、物理+
   論理成分をAtomicU64へパックしCASループでロックフリー実装)。9テスト
   全green(並行呼び出しでの重複無し検証込み)。`closed_ts`等への実配線は
   未実施。commit `c806846`。
5. ✅ **A.6-2 ColumnarApplier(本命)+ 実プロセス配線**: TiFlash型HTAPの
   核心=Raft-Learner上の行→列非同期変換レプリカ。`Applier` trait実装
   (行ストアミラー適用+テーブル全体を`table_format`〈Databend方式〉の
   blockへ列変換してcommit、min/max統計+主キーbloom filter)。
   `--columnar-learner`起動フラグを新設し、**実際にleader/columnar-
   learnerの2プロセスを起動し、CREATE TABLE→INSERT→UPDATEの各commitが
   binary Raft経由で別プロセスの列レプリカへ反映されることを実HTTPで
   確認**(replicationCount/snapshotIdの遷移、誤トークンでの401)。
   commit `56ef06c`→`27be65c`。
6. ✅ **A.6-4段階1 deletion vector + 枝刈り配線**: `BlockMeta.
   deletion_vector`(Delta Lake方式の論理削除、`BTreeSet<u64>`)。
   `with_deleted`/`is_deleted`/`live_row_count`。**`prune_range`/
   `prune_equality`が全行削除済みblockを実際に読み飛ばすよう配線**
   (「宣言しただけ」で終わらせず読み取り側を完成)。旧block JSONとの
   `serde(default)`後方互換込み、計8テスト。commit `b6aaaac`→`84b321e`。
   **残る配線**: `ColumnarApplier`の書き込み側からdeletion vectorを
   呼ぶ経路(A.6-4段階2 Merge-on-Reseへ格上げ時)。

### 次にすべきこと(aruaru-db、他アカウントでの再開ポイント)

1. A.6-4段階2(base+deltaのMerge-on-Read、`ColumnarApplier`をdelta蓄積
   方式へ格上げ)、HLCを`closed_ts`/`wal_service`/`multi_raft`へ配線、
   `aruaru.yaml: htap`セクションの実装(§5・A.7、この際`--columnar-
   learner`を宣言的設定経由の起動へ統合することも検討)。
2. `disaster_backup.email` reconcile(feature ゲート)、Tauri/Android/web
   の残りクライアント移行、P4(`admin_routes` 撤去 + `/raft/*` バイナリ化)。

### コミット(push 済み `origin/main`)

`6e5b3e0`(付録A 2026最新設計へ全面拡充)→ `efeebab`(**P3 本体** 3 群
GraphQL 化・REST 撤廃 + 日英ドキュメント整合)→ `33ae605`(付録A: 中国語
一次資料 / Paimon・Fluss)→ `250956d`(付録A: HLC アルゴリズム・Photon
adaptive execution)→ `c30a6b5`(続き11: 実プロセスHTTP E2E完了)→
`8bfec95`(続き12: ephemeral-query GraphQL化・REST撤廃)→
`afb4826`(続き13: multi-raft GraphQL化・REST撤廃、P3本体完了)→
`c806846`(続き14: A.6-1 HLC実装)→`56ef06c`(続き15: A.6-2 ColumnarApplier
本体)→`27be65c`(続き16: ColumnarApplier実プロセス配線・実HTTP検証)→
`b6aaaac`(続き17: A.6-4段階1 deletion vector)→`84b321e`(続き18: prune
系APIへのdeletion vector配線)。**VPS未反映**
(次回`git pull`で`8bfec95`まで追従させること)。

---

## 2026-08-29 チェックポイント(aruaru-db 管理面の抜本再設計、セッション末尾のため記録)

**対象リポジトリ**: `aruaru-db`(集中)、`RPoem`(SET の相方、次フェーズ P5 で本格関与)。

**到達点**: aruaru-db の `/admin/*` REST を**完全撤廃**する抜本再設計に着手。
「REST を 1 本ずつ GraphQL mutation へ」は *稼働中プロセスの生状態をフィールド
単位でライブ書き換えするアンチパターン* の移送にすぎない、というユーザー指摘を
受けた方針転換。正本の設計文書
[`repository/aruaru-db/docs/CONTROL_PLANE_REDESIGN.md`](repository/aruaru-db/docs/CONTROL_PLANE_REDESIGN.md)
を新設(設計哲学12か条・4バケツ仕分け・目標 HTTP 面・aruaru.yaml スキーマ・
フェーズ P0〜P6・付録 A=TiDB/TiFlash 調査・付録 B=REST 撤廃を可能にする
Cosmo の技術)。

進捗: P0(設計)/P1(宣言的設定基盤 `aruaru-server::config` + `--config` +
ホットリロード)/P2(`query.parallel` 4フィールド化、`follower_read.target_lag_ms`
完全ホットリロード)/P3 一部(`/admin/parallel*`・`/v1/keys/self-issue` 撤廃 →
GraphQL `explainDistributed`・`parallelJobs`・`selfIssueKey`)まで完了・push 済み。
各スライスで `cargo test` 失敗0。

**次回再開の起点**: **[repository/aruaru-db/CLAUDE.md](repository/aruaru-db/CLAUDE.md)
冒頭「🛑 復活用メッセージ」** をまず読む。P3 本体は `closed-timestamp` の
GraphQL 化から(`AdminCtx.closed_ts` 注入、`object_table`/`keyring` と同じ
パターン)。`wal-service`・`sharded-store` も同様。`ephemeral-query`・
`multi-raft` は trait 注入のリファクタが要る。

**ユーザーの不変の要求**: (1) SET(RPoem + aruaru-db)全体から REST API を
例外なく完全撤廃・中途半端禁止、(2) RPoem は Cosmo 互換で REST 不要・APIキー
完全自動ライフサイクル、(3) aruaru-db は CockroachDB×Snowflake ハイブリッド
変種の実在DB(TiDB 等)の技術を取り込む、(4) 必要なら多言語で再調査し
再設計・再実装・再テストを実用的になるまで数回繰り返す。

---

## 2026-08-20 チェックポイント(利用制限接近のため記録、大規模マルチリポジトリセッション)

ユーザー指示「リミットなので、README/CLAUDE/PORTINGを日本語で編集して
push・コミットして停止して」により、本セッションの到達点をここに記録する。

**このセッションで作業したリポジトリ(概要)**:
- **open-english**: モデル重み配置・同期バックアップUI、Facebook経由
  入口ページ、クロスプラットフォーム自動アップデート(Windows/Linux/
  macOS)+自動ロールバック、無料枠情報バナー(Google/DeepSeek/ChatGPT/
  Gemini/Claude)、1日利用回数制限メッセージ、スマホ計算ワーカー
  (PhoneAccelWorker、NNAPI検出+PC URL自動検出)、PS/Switch/Wii/WiiU
  ロードマップ(許可待ちとして明文化)。**重大なデータ損失バグを発見・
  修正**(Windows自動更新で会話履歴DBが消失する実害バグ、実インストーラー
  経由のE2E検証まで完了)。
- **aruaru-llm**: アイドル検知バックグラウンド基盤、NPU/USB検出、
  タスク配布API、自己更新機構、open-cuda連携の運用ルール整理。
- **open-cuda・open-directx**: 常駐サービス化の是非を事実ベースで
  調査(本家DirectX/CUDAもランタイムライブラリ方式と確認、実装見送り)、
  open-directxにLLM推論用の固定2x2 GEMMコンピュートシェーダーを実装・
  実機検証、FlexQ風INT6量子化を実装。
- **aruaru-db**: 自動アップデート機能(GitHub Releases検知+ヘルスチェック
  +ロールバック)を実装・実E2E検証(モックAPI経由)。Raft(openraft)・
  Multi-Raft・HTAP(OLAPキャッシュ)が既に実装済みと判明、TiFlash/
  CockroachDB Serverless/Neon型の3パターンを統合した「トライブリッド」
  実装に着手中(セッション中断、要再開)。
- **world-lab**: ワークユニット永続化(aruaru-db実DB、プロセス再起動を
  跨いだ復元を実機検証済み)、コーディネータをRPoem(Tomcat相当)+
  open-web-server(Apache相当)ベースへ再構築(既存の暗号化・リプレイ
  対策資産を保持したまま、SupervisedTenantRegistry経由でプロセス管理)。
  「4層4重通信」は過大と判断し見送り(正直な理由付き)。
- **dream-os**: `aruaru_persistence.rs`のドキュメント不整合(認証要否の
  誤記)を発見・修正。
- **open-easy-web・open-web-server・RPoem・rs-sync・open-raid-z**:
  自動更新機能の実装・完成、インストーラー整理(open-easy-webはサービス
  登録方式に統合)。
- **多言語翻訳**: 上記の変更を、各リポジトリの既存多言語ドキュメント
  (英語・中国語・独伊仏露烏ヘブライペルシャ語等、リポジトリごとに
  対応言語は異なる)へ反映。

**進行中・要再開のタスク**:
1. `aruaru-db`のトライブリッド実装(TiFlash非同期HTAP+CockroachDB
   Serverless層分離+Neonブランチング機能の統合)——特にNeon型
   ブランチング(Git-on-SQLとの親和性が高い)を優先。
2. 一部リポジトリでpush待ちのコミットが残っている可能性がある
   (各リポジトリの`git log --oneline origin/<branch>..HEAD`で確認)。

**正直な開示**: このセッションは非常に長時間・多数のバックグラウンド
エージェントを並行実行しており、一部エージェントが「委任した」等の
空応答で実作業をしていないケースが複数回発生し、都度直接指示して
やり直させる対応を行った。次回セッション再開時は、まず各リポジトリの
`git status`/`git log`で実際の到達点を裏取りしてから続行すること
(このエコシステム共通の運用ルール通り)。

---

## 2026-08-04(さらに続き) チェックポイント(多言語ページ展開＋open-directx/open-cuda/aruaru-llm連携強化、セッション末尾のため記録)

ユーザー指示「今日はここまでにします」により本セッションを終了。次回
再開の起点は以下の通り。

**今回完了した作業(コミット・push済み)**:
1. **多言語ページ展開**(`audiocafe-tokyo-php`・`audiocafe-tokyo-rust`・
   `open-web-server`): `aruaru`/`aruaru-lady`を11言語→18言語へ拡張、
   `rakuten-mobile`にヘブライ語を追加、3サイトとも18言語で統一。日本語
   ページ(Rust版)に多言語ナビを新設。本番デプロイ中に2つの実バグ
   (`open-web-server`のルーティングが多言語ページへの到達を阻んでいた、
   過去HANDOFFの「rakuten-mobile本番反映済み」という記述が実は誤りで
   VPS上に実ファイルが存在しなかった)を発見・修正し、実インターネット
   経由で全言語ページの200応答を確認済み。
2. **open-directx**: D3D11グラフィックスパイプラインのピクセル位置↔NDC
   座標変換式を実機(NVIDIA GT 730)で検証するテストを追加、実測誤差1
   (UNORM丸め範囲内)で一致確認。push済み(`3424340`)。
3. **open-cuda**: `open-cuda-llm`にQKV融合GEMM＋プリフィル/デコード
   分離を実装。実GPT-2 124M重みで変更前後の生成トークン列が完全一致
   することを実証(挙動を変えない最適化であることの証明)。push済み
   (`d8a49c7`)。
4. **aruaru-llm**: `real-vulkan` featureを新設し実推論をVulkanへ
   ディスパッチする配線を追加。実機検証の結果、**`open-cuda`側
   `Linear::forward`が`matmul.spv`を`sgemm`へ渡していないため
   `GemmPath::VulkanGeneric`が機能しない(即座にエラー)という未解決の
   実バグを発見**——性能比較のベンチマークはまだ実施できていない。
   push済み(`0327661`)。`open-cuda/CLAUDE.md`にも次回最優先課題として
   記録済み。

**次回再開の起点(優先順位順)**:
1. **`open-cuda`の`Linear::forward`にSPIR-V(`matmul.spv`)配線を追加**
   (`crates/open-cuda-llm/src/lib.rs`、`open-cuda/CLAUDE.md`2026-08-04
   〈続き〉エントリ参照)——これが解消して初めて`aruaru-llm`側の
   実Vulkan/CPU速度比較ベンチマークが実施できる。
2. 上記完了後、`aruaru-llm`(`--features real-vulkan`)で実機再検証:
   CPU版とVulkan版の生成トークン列一致・実速度差の計測。
3. `open-directx`側の残課題(DXILチェーンクラスのDXBC側への追従、
   テクスチャサンプリング・スワップチェーン拡張、AMD/Intel実機検証)。

---

## 複数リポジトリ横断セッションチェックポイント(2026-08-04追加)

> 以下は`F:\runo`ローカル作業ドライブでのセッション(どのリポジトリ・
> どのセッションから再開しても迷わないための直近の到達点)の記録。
> このメタ索引リポジトリ自体の実装対象ではないが、複数プロジェクトに
> またがる作業の「今どこまで進んでいるか」を一箇所で追える場所として、
> このリポジトリでホストする(ユーザー指示、2026-08-04)。

どのリポジトリ・どのセッションから再開しても迷わないための、直近の
到達点と次回再開ポイントの一覧。各詳細は各リポジトリの`CLAUDE.md`の
HANDOFFセクション参照。

## 🧳 2026-09-09 アカウント引っ越し用メッセージ(Claude TEAMアカウント解約・乗り換え)

> **背景**: ユーザーがClaudeのTEAMアカウント(料金が高い)を解約し、
> 普通の安いアカウント1つに一本化する予定。旧TEAMアカウント2つ
> (このアカウント+もう1つのTEAMSアカウント)は完全に削除される見込み。
> 新しいアカウント(セッション)に引き継ぐため、直近の到達点をここに
> まとめる。**アカウントの解約・削除自体はAnthropicの課金/アカウント
> 管理画面(claude.ai / console.anthropic.com の設定)からユーザー自身が
> 行う必要があり、Claude Codeセッションからは操作不可**(ツールの
> アクセス範囲外)。

**Background (English)**: The user is canceling their Claude Team
account (too expensive) and consolidating to a single regular
account. Both old Team accounts (this one + another Teams account)
are expected to be fully deleted. This entry summarizes recent
progress so a new account/session can pick up without confusion.
**Account cancellation/deletion itself must be done by the user via
Anthropic's own billing/account settings (claude.ai /
console.anthropic.com) — a Claude Code session has no access to
perform that.**

### 直近の到達点(2026-09-08〜09時点)

1. **VPS(conoha)復旧完了**: メモリ不足(OOM)によりSSH/HTTPSとも応答
   不能になっていたVPSを、ユーザーによるコントロールパネルからの
   再起動+`cargo build --release -j 1`での再ビルドで復旧。
   `aruaru-server.service`・`aruaru-db-web.service`とも`active`、
   ディスクは100%→79%(空き20G)まで回復。**恒久ルール**として
   `open-raid-z/CLAUDE.md`「運用ルール」節に「VPS上のcargo buildは
   必ず`-j 1`で行うこと」を追記済み(全リポジトリ共通の正本)。
2. **aruaru-llmのWindows配布バグ修正完了**: `open-cpu`のsibling
   checkout漏れ→CIビルド全滅、GPUビルド(DirectXシェーダー未整備)が
   installer全体を巻き込んで失敗、の2点を修正。`v0.2.4`で
   `aruaru-llm-windows-x86_64.zip`・`aruaru-llm-windows-x86_64-installer.exe`
   (改名済み)・`aruaru-llm-linux-x86_64.tar.gz`が正しく公開されることを
   確認済み。open-english側の`fetch-aruaru-llm.ps1`のダウンロードリンクも
   追従修正済み。GPUビルド自体(DirectXシェーダー .dxil未整備)は別課題
   (task_e9df0ef8として切り出し済み、未着手)。
3. **open-englishのプラットフォーム別バッジ統一**: Windows/macOS/Linuxを
   個別ブランドにせず「PC版起動中！」に統一、新たに「モバイル版起動中！」
   (スマホ・ガラケー・折りたたみ複数画面スマホ)・「タブレット版起動中！」
   をUser-Agent判定で追加。実ブラウザ検証済み、push済み。
4. **aruaru.tokyo/aon.tokyo(=aon.co.jp)/runo.tokyo/ion.tokyo(LOLIPOP)の
   コンテンツ更新**: KIKOU動画・金融シリーズ①動画(NIHON-KOKUSAI.mp4)の
   レイアウト統一、新規事業提案文(不動産電子契約・AUDIOルーム・酪農家
   人工授精士・植林・商工会議所SET創業支援等)の日英併記掲載を
   aruaru.tokyo/aon.tokyo/runo.tokyoへ追加・pushずみ。ion.tokyo
   (LOLIPOP、WebDAV: `hiho-aon.webdav-lolipop.jp`)も同内容へ更新済み。
5. **未着手・次回への持ち越し**: (a) aruaru-llm以外の各リポジトリの
   `target/`ビルドキャッシュ削除(ディスク再利用、aruaru-db分のみ完了)、
   (b) `open-english-pc`(OTP/TOTP認証付き新規URL)・`open-english-f`
   (Facebookモバイルアプリ)のeasy-web.tokyoへの実装、(c) LOLIPOPの
   ion.tokyo SSL証明書は2026-09-08にユーザー自身が対応済み(現在
   `https://ion.tokyo/`は正常稼働、証明書有効期限2026-12-07)。
6. **ドキュメント言語ポリシー(2026-09-08指示、memory
   `feedback_doc_language_policy`参照)**: README/CLAUDE/PORTINGは
   PCローカルドライブ・VPS上=日本語のみ、GitHub公開分のみ最大10ヶ国語
   程度(英・露・独・伊・仏・波斯・アラビア語等)に絞る方針。既存の
   11ヶ国語超のREADME群(open-english等)の削減作業は未着手。

## 2026-08-28 VPS(ConoHa、`ssh conoha`)ディレクトリ構成整理

**背景**: ユーザー指示「`/root`の下にrepositoryフォルダを作りリポジトリ
はそこに移動、`/root`の下にURLフォルダを作りWEBサイトはそこに移動、
シンボリックリンクを貼って全てのVPSとGithubのプログラムに対して編集
して」への対応。ハードリンクはLinuxの仕様上ディレクトリには作成
できない(ファイル単位のみ)ことをユーザーへ説明し、シンボリックリンク
のみで進める・ドメイン兼リポジトリのフォルダは両方(`/root/repository`
に実体+`/root/url`にもシンボリックリンク)に置く・1サービスずつ停止→
移動→シンボリックリンク作成→起動→実HTTP確認、という方針で合意の上
実施した。

### 実施内容

1. **`/root/repository/`(27件、gitリポジトリ)・`/root/url/`(10件、
   ドメイン兼リポジトリ8件+非リポジトリのWEB/デモ用ディレクトリ2件
   `easy-web.tokyo`・`open-raid-z-demo-disks`)を新設**。旧`/root/<名前>`
   には全てシンボリックリンクを残し、systemdユニット・nginx alias等の
   既存の絶対パス参照はすべて透過的に機能する(実際に編集が必要だった
   設定ファイルは無かった——`open-web-server`の`domains.toml`はポート・
   パスプレフィックスのみでファイルパス不使用、nginx側の唯一の
   `/root/`参照〈aruaru.tokyoの動画ファイルalias〉もシンボリックリンク
   越しにそのまま機能、cron〈`sync-repos.sh`〉・certbot設定にも該当
   パス参照は無かったことを確認済み)。
2. **移動対象外(意図的に現状維持)**: `aon.co.jp`・`audiocafe.tokyo`
   (実サイトは`/var/www/audiocafe.tokyo`、この`/root/audiocafe.tokyo`は
   未使用の古いclone)・`aruaru-db-data`(データディレクトリ、コードでは
   ない)・`disabled-vhosts-backup`・`dream-os`・`easy-web`(`.tokyo`
   無し)・`gitbucket-test`・`gitea-test`・`mirror-cache`・`open-aruaru`・
   `open-aruaru-core`・トップレベルの`open-cg-cad-demo`/`open-english-demo`
   (実体はいずれも`easy-web.tokyo`配下にあり、こちらは無関係な残骸)・
   `open-mqa`・`RFrontEnd`(`.git`が無く正規のcloneではない)・
   `rs-gitbucket`・トップレベルの`rs-sync-demo`(実サービスは
   `/root/rs-sync`を指すため無関係)・`world-lab`。いずれも稼働中の
   systemdサービスから参照されておらず、リポジトリともWEBサイトの実体
   とも言い切れないため今回は触れていない。
3. **予期しない発見・修復(今回の移動作業とは別の既存問題)**: サービス
   停止のたびに`target/release/<binary>`の実在を確認したところ、
   **このVPS全体で12個のサービスが、実体は既にディスクから削除済み
   (過去のディスク容量整理等の影響と推測)なのにプロセスだけ稼働を
   続けている「ゴースト状態」だったことが判明**——今回サービスを
   一度停止したことで初めて表面化した(今回の移動作業が原因ではなく、
   移動のために止めたことで顕在化した)。対象:
   `open-gitea`・`fbi.tokyo`・`e-gov.info`・`karu.tokyo`・`icpo.tokyo`・
   `runo.tokyo`・`open-redmine`・`RS-Blog`・`RS-EC`・`open-cg-cad`/
   `open-cg-cad-demo`・`open-kagaku`(いずれも現在チェックアウト済みの
   ソースのまま`cargo build --release`で再ビルド、`git pull`はしていない
   ——今回の目的はインフラ修復であり、無関係な機能更新を混在させない
   ため)。**`RS-Ops`はソースディレクトリ自体
   (`/root/runo.tokyo/RS-Ops`)が消失していたため、GitHubから再clone→
   ビルド→起動**して復旧した。全12件、再ビルド後に`systemctl is-active`
   +実際にTCPポートでlistenしていることを確認済み。
4. **`open-web-server`(全ドメインのリバースプロキシ)は当初Phase 6
   〈最後〉に予定していたが、RPoem等の相対パスsibling依存
   (`../../open-web-server/crates/...`)を解決するため、実際には
   `open-gitea`再ビルドの前段で先行して移動した**。
5. **実HTTP検証**: 移動・再ビルド後、`aon.tokyo`・`aruaru.tokyo`・
   `e-gov.info`・`fbi.tokyo`・`icpo.tokyo`・`karu.tokyo`・`nasa.tokyo`・
   `runo.tokyo`・`easy-web.tokyo`(および`/rsync`・`/open-redmine`・
   `/rs-sync`・`/rs-link-fusion`配下)・`runo.tokyo/RS-Ops`が実際に
   `https://`経由で200を返すことを確認。`easy-web.tokyo/open-gitea/`の
   404は移動前から存在した仕様(バックエンド自体がルートパスで404を
   返す)であり回帰ではないことを確認済み。
6. **GitHub側の「VPS上の作業パス」記載更新(5リポジトリ、CLAUDE.mdの
   現状記述のみ——HANDOFFの日付付き履歴エントリは当時の事実の記録
   として書き換えていない)**: `RS-Blog`・`RS-EC`・`open-redmine`・
   `rs-link-fusion`・`e-gov.info`(ドメイン兼リポジトリのため
   `/root/url/e-gov.info`併設にも言及)。各リポジトリで無関係な既存の
   未コミット差分(`open-redmine`のREADME/installスクリプト、
   `rs-link-fusion`の`Cargo.lock`)には触れず、`CLAUDE.md`のみを個別に
   commit・push済み。
7. **未実施(次回以降の課題)**: 他の全リポジトリ(`RS-Guard`・
   `RS-JSON`・`RS-SmartTCP`・`aruaru-db`・`audiocafe-tokyo-rust`・
   `open-gitea`・`open-web-server`・`rs-sync`・`open-raid-z`等)の
   CLAUDE.md内にも`/root/`への言及はあるが、いずれも日付付きの過去の
   作業記録(HANDOFFエントリ)であり「現状」を宣言する文ではないと
   判断し今回は変更していない——今後これらのファイルへ「現状」節を
   新設する場合は新パス(`/root/repository/<名前>`)を使うこと。

### 2026-08-28(続き) WEBサイト系8ドメインの実体を`/root/url/`側へ再配置

ユーザー指示「WEBサイトはリポジトリとは別です。ホームページやWEBサイトは
全てこの様に変更して」への対応。上記7分類のうち「ドメイン兼リポジトリ
(実体は`/root/repository/`、`/root/url/`は単なるsymlink)」としていた
8ドメインについて、**「WEBサイトとしての性質を優先し、実体を
`/root/url/`側に置く」**という設計へ変更した(gitリポジトリである
ことは副次的な属性、という位置づけ)。

- **変更内容**: `aon.tokyo`・`aruaru.tokyo`・`e-gov.info`・`fbi.tokyo`・
  `icpo.tokyo`・`karu.tokyo`・`nasa.tokyo`・`runo.tokyo`(+入れ子の
  `RS-Ops`)の8件について、実体を`/root/repository/<名前>`から
  `/root/url/<名前>`へ`mv`し、`/root/repository/<名前>`を
  `/root/url/<名前>`へのsymlinkへ変更した。旧`/root/<名前>`パスは
  変更していない(`/root/<名前>` → `/root/repository/<名前>` →
  `/root/url/<名前>`という2段のsymlinkチェーンとして、そのまま透過的に
  解決される——Linuxのパス解決はシンボリックリンクの多段チェーンを
  問題なく辿るため、既存のsystemdユニット等への影響は無い)。
- **手順**: 前回と同じ「1つずつサービス停止→`mv`→symlink再作成→
  起動→実際にTCPポートでlistenしているか確認」を徹底、全8件成功。
- **実HTTP検証**: 8ドメイン全て+`https://runo.tokyo/RS-Ops/`が
  実際に`200`を返すことを確認済み。
- **最終的な構成**: `/root/repository/<名前>`(gitリポジトリとしての
  参照、symlink)・`/root/url/<名前>`(WEBサイトとしての実体)・
  `/root/<名前>`(後方互換のためのsymlink、既存参照はそのまま機能)。
  この3者の役割分担が今回のセッションでの最終的な結論。

## 2026-08-28 ログイン方式4択(パスワード無し/email OTP/QR撮影のみ/email OTP+QR撮影)の横展開チェックポイント

**背景**: ユーザー指示「ログインは、1.パスワード無し 2.email OTP
3.QR撮影のみ(自動送受信・自動承認) 4.email OTP+QR撮影、と選べるように。
open-englishに限らず全リポジトリへ展開して」への対応。QR確認は公開鍵・
秘密鍵などの非対称暗号は使わず、短命(3分・1回限り)なランダムトークンを
含むURLをQR化するだけの設計(open-english側でユーザーと確認済み)。
確認端末でこのURLを開くと、ボタン操作無しに自動的にログインが承認される
(「撮影すると自動送受信・自動承認」という要件への対応)。

### 完了・push済み

- **open-english**: 4方式すべて実装完了。`server/src/auth.rs`の
  `login_mode`設定(`none`/`otp`/`qr`/`otp_qr`)、`qr-confirm.html`新設。
  実HTTP検証・実ブラウザでの別タブ確認(自動承認→プライマリタブの
  ポーリング検出→ゲート自動クローズ)まで完了。VPS本番
  (`easy-web.tokyo/open-english/`)へもデプロイ・反映済み。詳細は
  [open-english/CLAUDE.md](open-english/CLAUDE.md)の2026-08-28
  HANDOFF参照。
- **open-easy-web**: `qr`/`otp_qr`の2方式を追加(**「パスワード無し」は
  意図的に非実装**——VPS/サイト管理という重要操作を扱うアプリのため、
  認証省略は不適切と判断した正直な設計判断、詳細は同リポジトリの
  CLAUDE.md参照)。既存のリアルTOTP基盤(`totp::qr_svg`)を再利用。
  実HTTP統合テスト4件を新規追加、`cargo test` 96件全green(3回連続
  実行でフレーク無し確認)。GitHubへcommit・push済み(`66bf1ea`)。
  **VPS本番デプロイは未実施**。詳細は
  [open-easy-web/CLAUDE.md](open-easy-web/CLAUDE.md)の2026-08-28
  HANDOFF参照。

- **RS-Blog**: `qr`/`otp_qr`の2方式を追加(**「パスワード無し」は
  意図的に非実装**——公開ブログの管理者アカウントであり、投稿の
  改ざん・削除が可能なためコンテンツ完全性を優先し、open-easy-webと
  同じ判断基準を適用)。RS-Blogは登録アカウント制を持たず単一の
  管理者(`RSBLOG_ADMIN_EMAIL`)のみのため、open-easy-webの
  「TOTP登録済みアカウントのみqr可」という前提条件は不要とし、QR単体
  ログインは事前準備なしに常時利用可能な設計にした。`src/auth.rs`に
  `login_mode`(otp/qr/otp_qr)・QRログインセッション一式、
  `src/main.rs`に管理API+`qr-confirm.html`を追加。`cargo build`成功
  (警告0件)、`cargo test`**26件全green**(新規11件、実HTTP経由の
  統合テスト3件を含む)。実バイナリを起動してのcurl検証も実施
  (`GET /`・`GET /api/auth/login-mode`・`POST /api/auth/qr-login/start`
  のモード別403・`GET /qr-confirm.html`・未ログインでの
  `POST /api/auth/login-mode`401・SMTP未設定時の`request-otp`503、
  いずれも期待通り)。GitHubへcommit・push済み(`15fe134`)。
  **VPS本番デプロイは未実施**(v0.1.0時点でRS-Blog自体がまだVPS本番
  稼働していないため対象外)。詳細は
  [RS-Blog/CLAUDE.md](RS-Blog/CLAUDE.md)の2026-08-28 HANDOFF参照。

- **RS-EC**: `otp`(既定)/`otp_qr`(QR確認2FA)の2方式のみ実装
  (**「パスワード無し」に加え、QR単体〈no-OTP〉ログインも意図的に
  非実装**——`RS-Blog`〈単一固定管理者〉やopen-easy-web〈TOTP登録済み
  アカウントのみqr可〉とは異なり、RS-ECは`accounts.rs`による複数の
  登録メールアドレス〈会員+管理者〉を持ち、TOTP等の事前登録済み第二
  要素も無いため、「メールアドレスさえ知っていればQRセッションを
  開始できてしまう」設計は注文・決済に関わるアカウントの完全性を
  損なうと判断した)。`src/auth.rs`に`login_mode`(otp/otp_qr)・
  QRログインセッション一式(常に`verify_otp`経由でのみ開始、単体
  start APIは無い)、`src/main.rs`に管理API+`qr-confirm.html`を追加。
  `cargo build`成功(警告0件)、`cargo test`**47件全green**(新規
  10件、実HTTP経由の統合テスト含む)。実バイナリを起動してのcurl
  検証も実施。GitHubへcommit・push済み(`394d74b`)。VPS本番デプロイは
  対象外(RS-EC自体がまだVPS本番稼働していない)。詳細は
  [RS-EC/CLAUDE.md](RS-EC/CLAUDE.md)の2026-08-28 HANDOFF参照。

### 未着手(次回再開ポイント、優先度は次回ユーザーに確認)

認証機能(`auth.rs`/`totp.rs`)を持つことを確認済みの残り4リポジトリ:

- **RS-Ops**
- **open-gitea**
- **open-redmine**
- **rs-sync**

いずれも`server/src/auth.rs`または`totp.rs`を保有していることは
確認済みだが、各リポジトリの認証設計(セッション方式・OTP実装・
TOTP有無・単一/複数アカウント制)は個別に異なる可能性が高く、着手前に
各リポジトリの既存`auth.rs`実装を読んでから、open-english/
open-easy-web/RS-Blog/RS-ECと同じパターン(`start_qr_login`/
`confirm_qr_login`/`qr_login_status`/`finish_qr_login`+
`qr-confirm.html`+`login_mode`管理API)を、そのリポジトリの既存設計に
合わせて移植する、という進め方を踏襲すること。「パスワード無し」
モードを実装してよいかどうかは、そのアプリが扱う操作の重要度に応じて
都度判断すること(open-easy-web=VPS管理アプリでは非実装、RS-Blog=
公開ブログ管理者アカウントでも非実装、という前例を判断基準として
参考にする)。加えて、**QR単体(no-OTP)ログインを実装してよいかは
「事前に本人確認できる仕組み(単一固定管理者、またはTOTP等の既存の
第二要素)を持つか」で判断すること**(RS-EC=複数アカウント制+
事前確認手段が無いため非実装、という前例を参考にする——単一
アカウントのRS-Blog/固定管理者のopen-easy-webでは実装済み)。

### 次回セッション開始時にそのまま使える再開メッセージ

```
ログイン4択方式(パスワード無し/email OTP/QR撮影のみ/email OTP+QR撮影)の
横展開を再開してください。open-english・open-easy-web・RS-Blog・RS-ECは
完了済み(`F:\runo\PORTING.md`の「2026-08-28 ログイン方式4択…横展開
チェックポイント」節参照)。残りはRS-Ops/open-gitea/open-redmine/rs-sync
の4リポジトリです。まず着手するリポジトリを1つ選んで(優先度を指定
するか、私に選ばせてください)、そのリポジトリのsrc/auth.rs(または
server/src/auth.rs)を読んでから、open-easy-web/RS-Blog/RS-ECと同じ
パターン(QR確認ログイン+login_mode管理API+qr-confirm.html)を移植して
ください。「パスワード無し」モードを実装するかどうかはそのアプリが扱う
操作の重要度に応じて、「QR単体(no-OTP)」モードを実装するかどうかは
事前に本人確認できる仕組み(単一固定管理者、またはTOTP等の既存の第二
要素)を持つかどうかで判断してください(RS-ECは複数アカウント制+
事前確認手段が無いため後者を非実装とした前例あり)。
```

## 2026-08-04(続き) チェックポイント(複数GitHubアカウント・Gitea/GitBucket連携・マルチデバイス同期の強化着手)

ユーザー指示「複数GitHubアカウントとGitea同期とVPSやレンタルサーバーや、
スマホやタブレットやPCなどと同期可能なWEBアプリの完成度、実用性、
使いやすさなどを向上させて」を受けて着手。

### 完了・push済み

- **open-redmine**: 本家Gitea(OSS)・GitBucket(OSS)のSCM連携を新規実装
  (`ScmProvider::Gitea`/`GitBucket`、`Project.scm_base_url`新設、
  `fetch_recent_commits_gitea`/`fetch_recent_commits_gitbucket`)。
  `rs-sync`の`GiteaProvider`/`GitbucketProvider`と同じ「公式API仕様に
  基づき実装するが実サーバー未検証」という開示方針を踏襲。
  `cargo test` 93→94件全green、`web/`側wasmビルドも成功(回帰なし)、
  commit・push済み(`bf4e924`)。詳細は
  [open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)「2026-08-04」参照。

### 重大なブロッカーを発見(要ユーザー対応)

- **VPS(conoha、160.251.237.162)のディスクが満杯**(99GB中98GB
  使用、空き0バイト)。主因は`/root/aon.tokyo/`配下の個人/事業データ
  72GB(Content 31GB=動画等・Books 22GB=PDF書籍コレクション・backup
  3.4GB等)。これにより、本家Gitea/GitBucketの実サーバー検証用に
  計画していたDocker新規起動(`/root/gitea-test`・`/root/gitbucket-test`
  ディレクトリとdocker-compose.ymlは作成済みだが未起動)が実行不能。
  **ディスクプラン拡張はConoHaコントロールパネルでの契約変更が必要
  なため、ユーザー側の対応待ち**。拡張完了後、`docker compose up -d`を
  両ディレクトリで実行すれば起動できる状態まで準備済み。
- （余談・対応不要）ユーザーからConoHa VPS一覧に別途「mail-2026-07-18」
  (IP 133.117.75.153)というインスタンスがあるがメールはLOLIPOP運用の
  ため不要では、との確認があったが、時期が来ると自動解約される契約との
  ことで対応不要と判明。

### 次回再開の起点

**最優先(ブロッカー解消後すぐ着手できる状態に準備済み)**:
1. VPSディスク拡張(ユーザー対応待ち)後、`/root/gitea-test`・
   `/root/gitbucket-test`で`docker compose up -d`→本家Gitea/GitBucket
   実サーバーを起動→`rs-sync`の`GiteaProvider`/`GitbucketProvider`
   (`rs-sync/src/provider.rs`)と`open-redmine`の
   `fetch_recent_commits_gitea`/`_gitbucket`(今回実装分)を実HTTPで
   検証。

**ディスク拡張を待たずに継続可能**:
2. マルチデバイス同期の実インストール(`rs-sync`+`open-easy-web`+
   `open-web-server`連携)——調査エージェントを1件バックグラウンドで
   起動済み(rs-sync/open-easy-web/open-web-serverの現状連携ポイント・
   実際の「連携インストール」の具体的手順を調査中、結果は次回セッション
   冒頭で確認すること)。
3. 複数GitHubアカウント対応の強化(open-redmine/rs-syncでの複数
   アカウント切り替え・並行運用のUX改善、今回はGitea/GitBucket対応を
   優先したため未着手)。

## 2026-08-04 チェックポイント(リミット接近のため記録)

### 直近でpush済みの変更

- **open-redmine**: カスタムフィールド・保存済みクエリ・ロールプリセット・
  ガントチャート・優先度・カテゴリ・GitHub連携(GitHub/GitLab/Bitbucket
  対応、他セッションで拡張済み)
- **open-raid-z**: インストーラー電源プロファイル方針・Android優先方針・
  「省機能+省メモリボタン」標準方針を正本として記録(全リポジトリ横断)
- **rs-link-fusion**(旧RS-LinkFusion): リネーム・電源プロファイル実装・
  landingサーバー・VPSデプロイ完了
- **open-easy-web**: 電源プロファイル・メモリ円グラフ(実メモリ+仮想
  メモリ)・省機能ボタン・Androidアンインストール機能。実バグ発見・修正
  (`/admin/power-profile`が`open-web-server`自身の同名APIに横取りされ
  本番到達不能だった→`/admin/easyweb-power-profile`へリネームで解消)。
  VPS本番デプロイ・実HTTPS検証済み
- **aruaru-llm**: `POST /v1/translate`の実HTTP検証(GPT-2流用実装は
  実用に耐えないと判明)→翻訳プラグイン(M2M100/`rust-bert`、
  `nllb-translate` Cargo feature着脱式)を新設。**正直な開示**:
  feature有効時の実M2M100翻訳品質検証はlibtorch未整備のため未実施
- **rs-sync**: 36/36テスト全green、既に高い完成度(実機検証項目のみ残る)

### 次回再開の起点

**次にすべきこと(優先順)**:
1. `aruaru-llm`: `--features nllb-translate`での実ビルド・実M2M100翻訳の
   実HTTP検証(libtorchダウンロードを要するため時間のかかる作業)
2. `open-directx`/`open-cuda`/`aruaru-llm`のSET連携: 既にかなり作り
   込まれているため、各CLAUDE.mdのHANDOFF末尾「次にすべきこと」を確認
3. 「省機能+省メモリボタン」パターンの他GUI保有リポジトリ
   (`open-redmine`・`rs-link-fusion`)への展開
4. `open-raid-z`に記録したAndroid対応の段階的展開(NDKクロスビルド
   実証済みのリポジトリから優先)

### 参照

- プロジェクト自動認識: [runo-scan.txt](runo-scan.txt) / [runo-scanner](runo-scanner)
- 開発方針の正本: [open-raid-z/CLAUDE.md](open-raid-z/CLAUDE.md)

## 2026-08-03 チェックポイント(ユーザー指定4項目、「その順番で続けて」の進捗)

ユーザーが順番指定した4項目のうち、4番目まで一通り着手完了:

1. **rs-link-fusion・open-easy-webへのAndroid対応展開**: `open-easy-web`
   は既存の埋め込みバイナリ方式`.so`を再ビルドして最新化(1週間以上
   stale状態を解消)。`rs-link-fusion`は`tun-rs`crateにAndroid向け
   `DeviceBuilder`実装が存在しない(低レベルFDコードのみandroid-gated)
   ため、`VpnService`+JNI再設計が必要と判明——単純な`cargo ndk`では
   不可能なアーキテクチャ上の制約として記録([rs-link-fusion/CLAUDE.md](rs-link-fusion/CLAUDE.md)参照)。
2. **複数ドメインでのバイナリ共有(RPoemのSharedDispatcher統合)**:
   `open-web-server`の`TenantRegistry`が既に本番稼働中の同種機構である
   ため、RPoem側の`appserver_tenants.rs`(実装済みだが未デプロイ)を
   重複導入しない判断([open-raid-z/CLAUDE.md](open-raid-z/CLAUDE.md)参照)。
3. **RS-Sync動作確認・open-easy-web+open-web-server連携インストール**
   (2026-08-03に大きく進捗):
   - SFTPフォルダ同期を実conoha VPSで初めて実機検証、Windows開発機特有の
     バックスラッシュ混入パスバグを発見・修正(`join_unix_path`)。
   - WiFiルーターUSB共有・市販NAS向けにSMBバックエンド
     (`FolderEndpointKind::Smb`、`smb2`crate)を新規追加(実ルーター/NAS
     実機は無く未検証、正直な開示)。
   - デスクトップインストーラーをLinux(systemd、既存)に加え
     macOS(launchd)・Windows(Task Scheduler)へ拡張(この開発環境は
     ドメイン参加Windowsかつ非管理者アカウントのためTask Scheduler登録
     自体がAccess Deniedで実地確認未了、launchd plistのXML整形式のみ
     別途確認)。
   - Android版アプリシェルを新規実装(open-redmine版と同じ「リモート
     クライアント」設計)、`gradle assembleDebug`で実際にAPK生成まで確認
     (実機/エミュレータでの起動は未確認)。
   - iOS/iPadOS対応はユーザー指示により後回し、実現可能性調査のみ
     [open-easy-web/IOS_FEASIBILITY_MEMO.md](open-easy-web/IOS_FEASIBILITY_MEMO.md)
     に記録。
   詳細は[RS-Sync/CLAUDE.md](https://github.com/aon-co-jp/RS-Sync/blob/main/CLAUDE.md)
   「2026-08-03」系エントリ参照。
   **引き続き未着手**: Gitea(OSS)/GitBucket/GitLab/Bitbucket各プロバイダの
   実サーバー検証、open-easy-web+open-web-server連携によるマルチデバイス
   ドライブ同期+自動バックアップの実インストール作業。
4. **open-redmineのGitHub/GitBucket/Bitbucket/GitLab/Gitea連携対応**:
   GitHub(既存)に加えGitLab・Bitbucketを新規実装、実ネットワークAPI
   検証+ブラウザ実クリックE2E(GitLab側)完了、VPSへデプロイ・200確認
   済み。GitBucket・実Gitea(OSS)は実行中の検証用サーバーが無く
   未実装のまま(open-gitea自身にはコミット一覧APIが無いため代替不可)。
   詳細は[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)「2026-08-03」参照。

### 次回再開の起点

- 項目3の未着手部分(RS-Syncの実サーバー連携検証、open-easy-web+
  open-web-serverによるマルチデバイスドライブ同期+自動バックアップの
  インストール)が最大の残課題。
- 項目1の`rs-link-fusion`Android対応はVpnService+JNI再設計が必要な
  大きめの作業として別途スコープを切ること。
- 項目4のGitBucket/Gitea連携は実サーバーが用意できてから。
- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)は引き続き
  ブロック中。

## 2026-08-01(続き5) チェックポイント(open-raid-z本体「A」完了、次は横断バックログ「B」)

ユーザー指示「Aを進めて完成したらBを進めて」(A=open-raid-z単体リポジトリ、
B=open-raid-z/CLAUDE.mdに記録された複数リポジトリ横断のバックログ)を
受け、Aから着手。

**Aで完了した内容**(詳細は[open-raid-z/CLAUDE.md](open-raid-z/CLAUDE.md)
「2026-08-01」エントリ参照):
1. GPU parity実装(P/Q both実機検証済み)が`orzctl`から一度も呼ばれて
   いなかった(死んだコード)実バグを発見・修正、全4サブコマンドで
   実際に接続。
2. 接続直後に実測ベンチマーク(`examples/raidz2_parity_benchmark.rs`
   新設)を行ったところ、この環境ではGPU版がCPU版よりおよそ9〜14倍
   遅いと判明——「実装した・検出できた」だけでGPUを既定にせず、
   `--accel gpu`明示指定時のみの実験的オプションへ設計修正(実測に
   基づく誠実な判断)。
3. 副次的に発見: Linux(`fuse_backend`)ビルドが`BridgeError`の
   非網羅マッチで壊れていた実バグを修正(Windows専業開発で長らく
   未検出だった回帰)。
4. Web管理UI(`web/`crate、以前ローカル検証止まりだった)を実際に
   VPSへデプロイ、`https://easy-web.tokyo/open-raid-z/`で実際に
   稼働中のプール状態を確認済み。

**B(横断バックログ)は未着手**——open-raid-z/CLAUDE.mdの「関連
プロジェクト」節・エコシステム共通方針セクションに記録されている
複数リポジトリ横断の項目(Android優先対応、GPU/NPU検出ロジックの
他リポジトリへの展開、`aruaru-db`側の同種Web管理UI等)から着手する。

### 次回再開の起点

- Bの横断バックログへ着手(具体的にどの項目から着手するかは次回
  `open-raid-z/CLAUDE.md`「関連プロジェクト」節・各リポジトリの
  「次にすべきこと」を巡回して優先度を判断する)
- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)

## 2026-08-01(続き4) チェックポイント(残課題2件を消化)

前回チェックポイントの2項目に対応:

1. **GitHub側Webhook登録**(open-redmine): 引き続きユーザー操作待ち
   ——VPS保存済みのfine-grained PATに`Webhooks`権限が無く、エージェント
   側からは登録できない(手順は[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)
   「2026-08-01(続き2)」参照)。今回はこれ以上進められる状態ではない
   ため見送り。
2. **Android版UIへの電源プロファイル反映**(open-easy-web): 調査の結果、
   Android版ネイティブの電源プロファイル選択画面(`PowerProfile.kt`)は
   起動時の排他的3択(WakeLock取得有無というOSレベルのプロセス起動
   モード)であり、Web GUI側の独立チェックボックス(実行時に組み合わせ
   可能なランタイムフラグ)とは性質が異なる別概念と判明したため、
   変換は意図的に見送った。Androidアプリの「ブラウザで開く」ボタンは
   外部ブラウザでWeb GUIを開くだけの導線のため、Androidユーザーは
   既にこのボタン経由で新チェックボックスUIへ到達できる(Android側の
   コード変更は不要)。詳細は[open-easy-web/CLAUDE.md](open-easy-web/CLAUDE.md)
   「2026-08-01(続き2)」参照。

### 次回再開の起点

- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)
- 現時点で他に明確な次のタスクは記録されていない。新しい指示を待つか、
  各リポジトリのCLAUDE.md「次にすべきこと」欄を巡回して優先度の高い
  ものから着手する。

## 2026-08-01(続き3) チェックポイント(open-easy-webも追従、全3リポジトリ完了)

前回チェックポイントの残課題「`open-easy-web`のチェックボックス方式への
追従」を実施。旧3ボタン方式(排他的選択、「省機能」ボタンが
`memory_saver`を自動設定)を、`open-redmine`/`open-gitea`と揃えた
チェックボックス方式へ変更。既存バックエンド(`power_profile.rs`の
`PowerProfileFlags`)は元々独立フラグの組み合わせを表現できる設計
だったため、フロントエンドのみの変更で対応できた。加えて新設
`GET /admin/easyweb-power-profile`でページ読み込み時にサーバー実態へ
同期する導線も追加。

実サーバーを起動しての実ブラウザ検証(チェックボックス変更→`curl`で
サーバー側の実際の状態変化を確認→組み合わせ→ボタンでの省機能表示/
全機能復元)・本番デプロイ・本番wasmバイナリへの新コード混入確認まで
完了。詳細は[open-easy-web/CLAUDE.md](open-easy-web/CLAUDE.md)の
2026-08-01付HANDOFF参照。

これで「省機能+省メモリ版に切替」ボタン導入対象の3リポジトリ
(`open-easy-web`・`open-redmine`・`open-gitea`)全てがチェックボックス
方式で揃った。

### 次回再開の起点

- GitHub側Webhook登録(ユーザー操作待ち、open-redmine、
  `open-redmine/CLAUDE.md`「2026-08-01(続き2)」参照)
- Android版UI(`open-easy-web/android/`)への電源プロファイル
  チェックボックス反映(優先度低、現状Android UIが同機能を持つか要確認)
- 他にGUIパネルを持つリポジトリが増えた場合、同パターンで展開

## 2026-08-01(続き8) チェックポイント(open-redmineのAndroid版アプリシェルを新規実装)

GitHub Webhook登録は引き続きブロック中(fine-grained PATに`Webhooks`
権限が無く、再試行しても`403`)——手動登録手順は
[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)参照。

ユーザー指示により、横断バックログのうちAndroid対応へ着手。
`open-raid-z/CLAUDE.md`の段階的着手方針(NDKクロスビルド実証済みの
リポジトリを優先)に該当する`open-redmine`に`android/`ディレクトリを
新規実装(`aruaru-db/android`・`open-web-server/android`と同じKotlin
パターン: 3電源プロファイル・電源抜き差しダイアログ・プロファイル別
ホーム画面アイコン)。open-redmine本体は既に完成度の高いWASMブラウザ
GUIを持つため、ネイティブUIを再実装せず「疎通確認+ブラウザで開く」
クライアントとして設計。`gradle :app:assembleDebug`成功・APK生成まで
確認済み(実機/エミュレータでの実疎通確認は未実施)。

### 次回再開の起点

- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)
- Android対応の続き: `rs-link-fusion`・`open-easy-web`はまだ`android/`
  未着手
- 複数ドメインでのバイナリ共有(RPoemの`SharedDispatcher`/
  `appserver_tenants`経由の統合、`open-raid-z/CLAUDE.md`に複数箇所で
  「次回の課題」として記録されたまま)

## 2026-08-01(続き7) チェックポイント(横展開点検でopen-raid-zにも同じ実バグ発見・修正)

前回チェックポイントの提案「他にもGUI/管理APIを持つリポジトリがあれば
同様の観点で点検する価値がある」を実施。リポジトリ横断で`fetch('/api`
パターンを検索した結果、**`open-raid-z`のWeb管理UIにも`aruaru-db`と
全く同じ絶対パスfetch罠が実際に存在した**(直前のHANDOFFエントリ自体が
「絶対パスだから問題ない」と誤って記載していた箇所)。実ブラウザで
`https://easy-web.tokyo/open-raid-z/`が`{"error":"not found"}`を
表示することを確認した上で、`aruaru-db`と同じ`BASE_PATH`パターンで
修正・本番デプロイ・実ブラウザでの正常動作確認まで完了。
`aruaru.tokyo/src/main.rs`にも同じコードパターンが見つかったが、
こちらは`path_prefix`無しでドメインルートに直接マウントされているため
該当しないことを`domains.toml`で確認済み(誤検知)。

これで、`path_prefix`付きでデプロイされている全Web UI
(open-redmine・open-gitea・RS-Sync・aruaru-db・open-raid-z)の絶対パス
fetch罠点検が完了した。

### 次回再開の起点

- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)
- Android優先対応・複数ドメインでのバイナリ共有等、`open-raid-z/
  CLAUDE.md`に記録された残りの横断バックログ項目
- 新規にpath_prefix付きWeb UIを追加する際は、最初からBASE_PATHパターンを
  組み込むこと(今回の教訓)

## 2026-08-01(続き6) チェックポイント(「B」横断バックログ、aruaru-db優先着手)

ユーザー指示「CLAUDEの判断で優先順位を付けて、すいすいどんどん開発を
進めて」を受け、`open-raid-z/CLAUDE.md`の「関連プロジェクト」から
`aruaru-db`(open-raid-zと対のWeb管理UIパターンを持つ、既に「次に
すべきこと」に「VPS実デプロイ」と明記されていた)を優先着手先として
選び、以下を実施:

1. **Web管理UIをVPS本番へデプロイ**(`aruaru-server`を単一ノード
   スタンドアロン構成でport 4001/5433に起動、Web UIをport 8111に起動、
   `https://easy-web.tokyo/aruaru-db/`で公開)。デプロイ直後、実ブラウザで
   開いたところ**実バグを発見**: `fetch('/api/status')`という絶対パス
   fetchが`/aruaru-db`マウント配下で壊れていた——open-redmine/
   open-gitea/RS-Syncが過去に繰り返し踏んだのと全く同じ「絶対パス
   fetch罠」がこのリポジトリでも初めて実際に踏まれた形。
   `ARUARU_WEB_BASE_PATH`を追加して修正、実ブラウザで正しく動作する
   ことを確認済み。
2. **GraphQL経由の管理操作に認証を適用**(実バグ修正): REST
   `/admin/*`は2026-07-30に認証済みだったが、**同じ管理操作を
   `/graphql`経由で呼べば無認証のまま実行できる抜け穴**が残っていた。
   `x-admin-token`検証を全Admin resolverへ適用(非管理系VCSクエリは
   対象外)、本番で実際にHTTPリクエストにより無トークン/誤トークン
   拒否・正トークン成功・非管理クエリは無認証で成功、の4パターンを
   確認済み。**なお、調査の過程で`cluster_propose`のRaftWriter経由化
   自体は2026-07-26に既に実装・テスト済みだったと判明**——CLAUDE.mdの
   「次にすべきこと」記載が更新されないまま古い情報として残っていた
   だけだった(このエコシステムで繰り返し見られる「ドキュメントの
   追従漏れ」パターン、実装自体は問題無し)。

詳細は[aruaru-db/CLAUDE.md](aruaru-db/CLAUDE.md)の2026-08-01付
HANDOFF各エントリ参照。

### 次回再開の起点

- 他にもGUI/管理APIを持つリポジトリがあれば同様の観点(絶対パスfetch・
  認証欠如)で点検する価値がある
- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)
- Android優先対応・複数ドメインでのバイナリ共有等、`open-raid-z/
  CLAUDE.md`に記録された残りの横断バックログ項目

## 2026-08-01(続き2) チェックポイント(電源プロファイルUIをチェックボックス方式へ)

前回チェックポイントの「他のGUIを持つリポジトリへの省機能+省メモリ版
展開」を`open-gitea`で実施中、ユーザーから「省メモリ、常時電源接続などは
チェックボックスとボタンにして」という形式指定を受け、以下を実施:

1. **`open-gitea`**: 省電力/省メモリ/常時電源接続を独立チェックボックス
   として実装(`open-easy-web`の`PowerProfileFlags`と同じ組み合わせ
   可能な設計)+「省機能表示に切替」「全機能を復元」ボタン。実装中に
   **本番の実バグを発見**: `static/rgit_web.*`(2026-07-27のリネーム前・
   Wiki機能実装前の半年近く古いビルド)がコミットされたままで、
   `index.html`が実際にimportする`open_gitea_web.js`は一度も
   コミットされていなかった——本番は2026-07-28以降ずっと壊れたUI
   (JSファイル404)を配信していた。修正・デプロイ済み、実際に
   `404`→`200`になったことを確認。
2. **`open-redmine`**: 前回チェックポイントで実装した3ボタン方式
   (排他的選択)を、上記と同じチェックボックス方式へ作り直し。
3. **`open-raid-z/CLAUDE.md`**: エコシステム標準方針をチェックボックス
   方式へ改定。**`open-easy-web`(先行実装)は旧3ボタン方式のまま
   ——チェックボックス方式への追従は未着手として記録**。

いずれも本番(`easy-web.tokyo`)へデプロイ済み・実際にHTML/JSに新UIの
文字列が含まれることを確認済み。

### 次回再開の起点

- GitHub側Webhook登録(ユーザー操作待ち、open-redmine)
- `open-easy-web`の電源プロファイルUIをチェックボックス方式へ追従
- 他のGUIを持つリポジトリ(`rs-link-fusion`は静的ランディングページのみで
  対象外と判断——GUIパネルを持つ他リポジトリがあれば順次展開)

## 2026-08-01(続き) チェックポイント(open-redmine、上から順に4項目対応)

前回チェックポイントで挙げた4項目に上から順に対応した:
1. **本番デプロイ+実クリックE2E**: デプロイ済み。実クリックE2E自体は
   本番のOTPメール受信箱にアクセスできないため、ローカルで
   `RSCHIKETTO_DEV_LOG_OTP`+`BASE_PATH`一時変更により実施・確認済み。
2. **GitHub Webhook受信によるリアルタイム更新**: 実装・デプロイ・
   ローカルE2E(署名検証・キャッシュ優先・実クリックでバッジ→チケット
   詳細)確認済み。**GitHub側のWebhook登録は権限不足(fine-grained PATに
   Webhooks権限無し)でブロック中**——ユーザーによる手動登録または
   PATスコープ拡張が必要(手順は`open-redmine/CLAUDE.md`参照)。
3. **install.sh/install.ps1**: 前回「未着手」と記録していたが、実際には
   既に存在していた(2026-07-22時点で追加済み)。誤った記録だった。
4. **省機能+省メモリ版に切替ボタン**: 実装・デプロイ・実クリックE2E
   確認済み。

詳細は[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)の2026-08-01付
HANDOFF各エントリ参照。

### 次回再開の起点

- GitHub側Webhook登録(ユーザー操作待ち、上記2.)
- 他のGUIを持つリポジトリ(`rs-link-fusion`等)への「省機能+省メモリ版」
  展開(`open-raid-z/CLAUDE.md`の段階的着手方針)

## 2026-08-01 チェックポイント(open-redmine続き)

前回チェックポイント以降、`open-redmine`は単独でさらに進んでいた
(GitHubリポジトリ連携機能を追加、commit `4fdd9c6`)。今回のセッションは
その「次にすべきこと(2)」——GitHubコミットの参照チケットバッジを
クリック可能にする対応を実施・commit・push済み(`f5d656d`)。
詳細は[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)の
「2026-08-01」HANDOFFエントリ参照。

### 次回再開の起点

**[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)の「2026-08-01」
エントリ**から再開すること。次にすべきこと:
1. 本番(`easy-web.tokyo/open-redmine`)へのデプロイ+バッジクリックの
   実ブラウザE2E(このセッションでは未実施)
2. GitHub連携のWebhook受信によるリアルタイム更新(将来検討)
3. インストーラー(`install.sh`/`install.ps1`)自体がopen-redmineに
   まだ存在しない——電源プロファイル選択機能(省電力/省メモリ/常時電源
   接続、エコシステム全体の標準方針、詳細は
   [open-raid-z/CLAUDE.md](open-raid-z/CLAUDE.md)参照)の前提として
   先にインストーラー本体を新設する必要がある
4. 「省機能+省メモリ版に切替」ボタン(`open-easy-web`で先行実装済みの
   パターン)のopen-redmineへの展開はまだ未着手

## 2026-07-31 チェックポイント(open-redmine集中セッション)

### 直近でpush済みの変更(すべて`open-redmine`)

このセッションはユーザー指示「Redmine本家と違って対応していない機能を
open-redmineにも対応させて」「見た目の細部も本物に近づけて」「どんどん
一般的なチケット一覧の構成に近づけて」に沿って、`open-redmine`1リポジトリ
に集中して以下を実装・commit・push済み:

1. カスタムフィールド(`Project.custom_field_defs`+`Ticket.custom_fields`)
2. 保存済みクエリ(`src/saved_queries.rs`、個人用のみ)
3. 名前付きロールプリセット(`access::RolePreset`: Manager/Developer/Reporter)
4. ガントチャート・カレンダーGUI(`web/`、進捗%オーバーレイ付き)
5. スケジュール(開始日・期限日)・進捗率の入力/編集UI新設
6. チケットステータス`resolved`追加(担当者割り振り→resolved→closedの
   遷移を実HTTPで確認)
7. `web/`側の英語(日本語)併記を徹底(placeholder・動的エラーメッセージ約20箇所)
8. チケット一覧をRedmine本家に近いテーブル形式へ刷新(色分けバッジ・
   進捗バー・期限超過赤字表示)
9. 優先度(Priority、Low/Normal/High/Urgent/Immediateの5段階)フィールド追加
10. `created_at`/`updated_at`追加、一覧に更新日列+更新日降順の既定ソート
11. カテゴリ(Category)フィールド追加(`Project.category_defs`+
    `Ticket.category`、値の検証あり)

メインクレート`cargo test`: 81→85件、全green(回帰なし)。`web/`側
`cargo test`: 4件全green。各段階でwasm32リリースビルド+実バイナリでの
`curl`/DOM確認を実施(詳細・commit hashは`open-redmine/CLAUDE.md`の
2026-07-31付けHANDOFF各エントリ参照)。

**正直な開示**: このセッション環境のブラウザ拡張によるfetch計装が
原因で、実クリック操作でのフルE2E(ログイン→操作→表示確認)は行えず、
DOM直接注入によるレンダリング確認+curlによるAPI往復確認に留まった。

### 次回再開の起点

**[open-redmine/CLAUDE.md](open-redmine/CLAUDE.md)の「2026-07-31(続き4)」
カテゴリ追加のエントリ**から再開すること。次にすべきこと:
1. プロジェクトの`category_defs`/`custom_field_defs`管理画面
   (現状いずれもAPIのみ、web側UI未実装)
2. 一覧テーブルの列クリックによるソート機能
3. 本番(`easy-web.tokyo/open-redmine`)へのデプロイ+実クリックE2E
   (このセッションで未検証だった範囲)
4. 保存済みクエリ・ロールプリセットのweb側UI(現状APIのみ)

## 2026-07-29 チェックポイント

### 直近でpush済みの変更

- **aruaru-llm**: モデルカタログ・ホットスワップ機能
- **open-redmine**: 担当者フィールド・プロジェクトマネージャーロール・
  storageバックエンド修正
- **open-easy-web**: 分散同期・ディザスタリカバリ機能
- **open-raid-z**: SFTPホスト鍵TOFU検証
- **open-directx**: グラデーション補間・GPUベンダー診断・チェーン
  sub/div対応
- **aruaru-db**: Tauri Admin GUIのビルド不能状態解消

### 次回再開の起点

**[rs-sync/CLAUDE.md](rs-sync/CLAUDE.md)の「HANDOFF追記(2026-07-29続き5)」
フォルダ同期(SFTP)+通知機能+ハートビート横展開**から再開すること。
次にすべきこと:
1. 実SFTPサーバーでのフォルダ同期の実機検証
2. 実トークン期限切れシナリオでの通知メール実地確認
3. open-easy-webの`uninstall.ps1`(Windows版)が未作成
   (`install.ps1`のみ既存、`uninstall.sh`はLinux版のみ新設済み)

### 未コミット作業の確認・commit済み(2026-07-29)

前回チェックポイント時点で残っていた2件のローカル変更は、内容確認
(既存コードの削除ゼロ・純粋な追加のみと確認)・ビルド/テスト確認の上、
commit・pushした:
- `open-redmine`: チケット添付ファイルのアップロード/ダウンロード/削除API
  (`src/attachments.rs`新規+`src/main.rs`にハンドラ・ルート追加)。
  `cargo build`成功を確認。(`e9c55c0`)
- `open-raid-z`: ストライプ整列済み書き込みでRMWの読み出しを省略する
  高速パス(`pool.rs`)+検証テスト(`tests/unaligned_io.rs`)。該当テスト
  8件全green。(`1586497`)

### 参照

- プロジェクト自動認識: [runo-scan.txt](runo-scan.txt) / [runo-scanner](runo-scanner)
- 開発方針の正本: [open-raid-z/CLAUDE.md](open-raid-z/CLAUDE.md)

## 2026-09-27 チェックポイント(限界前の緊急停止)

ユーザーから「もうリミットなので」との指示で、ドキュメント更新・pushのみ行い緊急停止。

### 今回作った・触ったリポジトリ

- **open-bar**: 共有モード出力のtry_lock無音混入バグ修正・open-audioコンテナ(.mka)再生対応・
  高音補正(MP3向け、biquad EQ)・テスト用PD音源10曲整備・追加バグ3件修正。全てpush済み。
- **open-av**: 音声専用プロファイル(旧称open-audio)を`open-mqa-dsd`へ完全移設し、
  映像プロファイル専用の薄いクレートへ縮小。push済み。
- **open-mqa-dsd**: 上記コンテナ実装(`container`モジュール)を吸収、
  `"format": "open-mqa-dsd"`へ改称。push済み。
- **open-audio-sr(新設)**: AudioSR(実在の拡散モデル)による音声帯域拡張。
  実機で「単純補間-59.3dB vs AI超解像-24.8dB」を定量確認、HTTP API(RPoem経由)も
  エンドツーエンドで実機検証済み。push済み。
- **open-audio-sr内、Python環境構築時のハマりどころ**: 32bit Pythonは不可(torch非対応)、
  audiosrパッケージ自身のrequirements(numpy 1.23.5等)がPython 3.13と非互換のため
  `--no-deps`+個別解決、`torchaudio.load`はtorchcodec(FFmpeg共有ライブラリ要)を
  soundfile版へmonkeypatchして回避。詳細は`open-audio-sr/CLAUDE.md`。
- **open-music-llm(新設、未完了)**: MusicGen(実在のオーディオLLM)でテキストから音楽生成。
  Python venv構築・依存インストールまで完了したが、**実際の生成(推論)は未検証のまま中断**
  (`transformers`のimportがこの開発機で90秒待っても終わらない現象に遭遇、詳細は
  `open-music-llm/CLAUDE.md`の「環境の既知の問題」参照)。次回はここから再開すること。

### 訂正した誤った説明(記録のため)

セッション中に「LLM(言語モデル)は音声を生成できない」と説明したが不正確だった。
正しくは「テキストの次単語予測を行う通常のLLMは音声を直接生成できないが、EnCodec等の
ニューラル音声コーデックで音声を離散トークン化し、そのトークン列に通常のLLMと同じ
Transformerデコーダ+次トークン予測を適用する『オーディオLLM』という設計は実在し、
MusicGen/AudioGenが採用している既に主流の一つ」。ただし帯域拡張(超解像)用途に限っては
2026年の研究でオーディオLLMは拡散モデルに性能面で劣ると報告されており、
open-audio-sr(拡散モデル)の選択自体は妥当だった。

### 次回再開の起点

1. **open-music-llm: 完了(2026-09-27)**。`USE_TF=0 USE_FLAX=0 TRANSFORMERS_NO_ADVISORY_WARNINGS=1`
   を付けて実行することで実際に音楽生成(facebook/musicgen-small、5.06秒・32kHz、
   `ffmpeg volumedetect`でmean -23.1dB/max -6.1dBの実音声を確認)に成功した。
   前回「transformersのimportが90秒で終わらない」ように見えた真因は、バックグラウンド
   実行コマンド文字列側に重ねて`&`を付けたことでラッパーシェルが即終了し完了と
   誤通知されていたことだった(importの遅さ自体は残るが、ツール側の`run_in_background`
   機能だけに任せれば正しく完了まで待てる)。詳細は`open-music-llm/CLAUDE.md`。
2. **open-mqa-dsd/open-avの統合は完了済み**(前回HANDOFFで「次回」としていたが今回完了)。
3. **`aruaru-search`+archive.org連携: 実装・実機確認済み(2026-09-27)**。新エンドポイント
   `GET /v1/media-search?q=&n=`で、曲名/演奏者/作曲者/レーベル名によりarchive.orgを横断検索し、
   パブリックドメイン・CC0・CC-BY・CC-BY-SAの音源だけ(CC-BY-NC/ND系・ライセンス不明は除外)を
   即時ストリーミング可能なURL付きで返す。既存のHTML解析前提のengine.rsとは別に、archive.org
   自身の構造化JSON APIを使う専用モジュール`src/archive_org.rs`として実装(aruaru-searchの
   「機能ごとにモジュールを分ける」既存方針に沿う)。実機で`curl .../v1/media-search?q=Caruso&n=5`
   を確認し、Enrico Carusoのパブリックドメイン録音がストリーミングURL付きで返ることを確認済み。
   未実施: VPSへの本番デプロイ、open-bar等の再生側からこのAPIを呼ぶ導線。詳細は
   `aruaru-search/CLAUDE.md`の「archive.org横断検索」節参照。
4. **make-disk-installer.exeのGUI実クリック検証: 完了(2026-09-27)**。専用のGUI自動操作
   ツールは無いため、Windows UI Automation(`System.Windows.Automation`)+
   `SetCursorPos`/`mouse_event`によるPowerShellスクリプトを自作し、実際のマウス座標で
   「参照...」「インストール」ボタン・チェックボックス・完了モーダルのOKを実クリックした。
   実クリックで実際に`perform_install`が走り、既定のインストール先へファイルが展開され、
   レジストリ(`HKCU\...\Uninstall\make-disk-installer`)が正しく登録され、登録された
   `UninstallString`をそのまま実行してアンインストール(フォルダ・レジストリ削除)まで
   実機で確認できた。詰まった点(DPI-awareness不整合でクリックが無反応になる、完了
   モーダルがUIAのルート列挙に出てこないためEnumWindowsが必要、UTF-8 BOM無しの
   PowerShellスクリプトが文字化けで構文エラーになる)は`make-disk/installer-exe/README.md`
   に記録。**open-bar同時インストールの経路も、ユーザーの明示的な指示により実機へ本当に
   インストールする副作用を承知の上で追加検証済み**: `--test-install --with-open-bar`で
   GitHub Releasesから最新のopen-barインストーラーを実際に取得し`/S`サイレントインストールが
   最後まで成功することを確認(既存インストール環境での再インストール確認であり、まっさらな
   環境での初回インストールは未検証)。
5. **open-bar高音補正のAI本格化: 実装・テスト・push完了(2026-09-27)**。`src/ai_treble.rs`が
   open-audio-sr(実在の拡散モデルAudioSR)を呼び、MP3の高域を実際に復元する。推論が重いため
   再生をブロックせず、初回はリアルタイムEQ(既存)にフォールバックしつつバックグラウンドで
   AI強化版を生成、次回同じ曲を再生するときはキャッシュ済みのAI強化版を再生してEQは重ねない。
   **副産物のバグ修正**: open-audio-srをgit依存として他プロジェクト(open-bar)から使おうとして
   初めて判明した不具合(HTTPサーバー専用のRPoem/open-cpu依存が常時必須でビルドできない)を
   open-audio-sr側で修正(`server`featureへ隔離)。両リポジトリともpush済み、`cargo test`は
   open-bar 33件・open-audio-sr(lib/server両方)ビルド成功で確認。
   **未実施**: 実機での音質検証(AI強化版の生成完了を待った聴き比べ)、GUI側の生成中/完了表示、
   GPU(open-cuda/open-directx)推論(open-audio-sr側が未実装のため)。
6. **make-disk GUI改善+新機能3件: 実装・テスト・push完了(2026-09-28)**。
   - **色分けUI**(前回続き): 8.2のトリミング編集で「使う範囲」🔵と「消す範囲」🟠を色分け。
     GUI実クリックでの動作確認は、Windowsのフォーカス乗っ取り防止(foreground lock)により
     自動化スクリプトから確実に対象ウィンドウへフォーカスできず、無関係な別アプリ(動画編集
     アプリ)へ誤って入力してしまう事故が発生したため断念(実機での手動確認が必要)。
   - **時間指定フォームの統合**(ユーザー指摘「複数箇所に散らばって混乱の原因」): 旧「7.5
     元データのカット」(全ファイル一括)を「8. 時間指定・トリミング」節へ移動し、8.1(一括)・
     8.2(個別精密編集、色分け済み)としてこの1箇所にまとめた。
   - **見積もり(所要時間・空き容量・収まるか)の音声/CD対応**(ユーザー指摘「ビデオのみでCD/
     音声に未対応」): 動画のAI超解像(4.3)専用だった機能を、7.に新設した汎用ボタンで
     CD取り込み・通常の音声変換にも使えるようにした(`estimate_bitrate_fit`/
     `free_space_bytes`新設)。
   - **チャンネル構成変換(3.7新設)**: モノラル/ステレオ→5.1ch/7.1ch(単純な複製・按分による
     疑似〈バーチャル〉サラウンドと明記、3ch以上の音源には適用しない)、サラウンド→ステレオ/
     モノラル(ffmpeg標準降ミックス)。`channel_layout_args`新設。
   - **そのまま含める(includeAsIs)**(前回続き): make-diskが変換できない任意のファイルを
     無変換でISO/ディスクへ含める機能(`copy_source_as_is`)も実装・push済み。
   - `cargo test`: 147 passed, 0 failed(新規テスト全て含む)。
   - **未実施**: 実機GUIクリックでの動作確認(上記の理由により断念、次回は手動確認が必要)。
7. **make-disk: AIアップミックス(HT-Demucs実音源分離)を新設(2026-09-28)**。
   ユーザーから「単純なpanフィルタではなく実際のAIで」との要望を受け、実在する
   Meta製音源分離モデルHT-Demucs(MIT、demucs-onnxのONNX変換版)を、make-diskの
   他のAI機能(RNNoise/LavaSR)と同じ純Rust(tract)推論で実装。
   - **技術的な壁の突破**: 配布されているhtdemucs.onnxはtractのONNX `Pad`
     (省略可能な第3入力を必須とみなす)・`Range`(697ノードでsymbolic dimension型
     推論に失敗)の実装の狭さでそのままは読み込めなかった(onnxruntimeでは正常動作、
     モデル側の欠陥ではない)。onnxライブラリでグラフを直接パッチ(Pad: 明示的定数
     入力を追加、Range: onnxruntimeで実際に推論して値を捕捉しConstant化)する手法を
     確立し、tractでの読み込み・最適化・推論実行(出力shape `[1,4,2,343980]`)まで
     実機確認済み。再現手順は`make-disk/tools/demucs-onnx-patch/README.md`。
   - 設計: ボーカル/ドラム/ベース/その他の4分離→センター=ボーカル、フロント=ドラム+
     ベース、リア=その他(残響/伴奏)、LFE=無音、へ配置(`src-tauri/src/engine/ai_upmix.rs`)。
   - **未実施**: モデル配布(パッチ後約2.2GBがGitHub Releases標準上限2GB超のため、
     LavaSR等と同じ自動ダウンロード方式は未実装。現状は環境変数
     `MAKE_DISK_DEMUCS_MODEL_DIR`での手動配置のみ、未設定時はpanフィルタへ自動
     フォールバック)、オーバーラップ加算によるチャンク境界のクロスフェード。
   - `cargo test`: 153 passed, 0 failed。

## 2026-10-14 お引越し対応(aruaru-llm/open-english) / Migration readiness

**日本語**: 女性キャラ=メイドの先生・男性キャラ=執事の先生、モデル非依存の知識ストア、WEB/GitHubからの自動復元、6時間ごとのGitHub退避を実装しVPSへ反映済み(open-english v0.8.14)。お引越し手順は各リポジトリのPORTING.md「お引越し」節(`aruaru-llm`・`open-english`)。未了: Android実機確認、VPS丸ごとの再構成の通し試験、国別ニュース見出しが応対に入らない原因調査。

**English**: Female character = maid teacher, male = butler teacher; a model-independent knowledge store with automatic restore from the web/GitHub and a 6-hourly GitHub backup are implemented and deployed (open-english v0.8.14). Migration runbooks: "Migration" in each repo's PORTING.md (`aruaru-llm`, `open-english`). Open items: real Android device check, a full from-scratch VPS rebuild rehearsal, and why today's news headline is not reaching replies.

## 2026-10-14 open-github-backup(GitHub Actionsによる自動バックアップ) / GitHub Actions backup

**日本語**: `aon-co-jp`の全リポジトリを`runo-aruaru`(非公開)へミラーする[`open-github-backup`](https://github.com/aon-co-jp/open-github-backup)(非公開、`F:\open-github-backup`)を新設し、
RS-Syncの同期ジョブとVPSのcron(`/root/sync-repos.sh`)を停止して置き換えた。2026-10-08に全件ミラー成功(宛先135件、全て非公開)。
**ただし10/8以降の定期実行はGitHubの課金/利用上限(「recent account payments have failed or your spending limit needs to be increased」)でジョブが開始されず失敗**しており、
`aon-co-jp`のBilling and plansの確認が必要(1ジョブ・差分方式へ書き換え済みだが、課金が解消するまで検証不能)。教訓: `aon-co-jp`はUser(`user/repos`)、Fine-grained tokenは個人アカウントのリポジトリを作れない(Classicの`repo`+`workflow`)、
`F:\runo-aruaru-github-token.txt`は当初`aon-co-jp`のトークンで宛先が自分自身になっていた、大量作成は二次レート制限。
VPSデータ(PostgreSQL・aruaru-db・設定)のGPG暗号化バックアップ(秘密鍵`F:\vps-data-backup-gpg-PRIVATE.asc`)はスクリプト作成済みで**VPS未配置**。
VPSの旧cronはコメントアウト、`rs-sync`のジョブは無効化(退避`/root/*.bak-20261008`)。詳細・再開手順・別PCへの移行手順は`open-github-backup/PORTING.md`と`CLAUDE.md`。

**English**: Created [`open-github-backup`](https://github.com/aon-co-jp/open-github-backup) (private, `F:\open-github-backup`), which mirrors all `aon-co-jp` repositories to `runo-aruaru` (private),
replacing the RS-Sync job and the VPS cron (`/root/sync-repos.sh`). A full mirror succeeded on 2026-10-08 (135 destination repos, all private).
**Scheduled runs since 10/8 fail because GitHub does not start the jobs (billing / spending limit: "recent account payments have failed or your spending limit needs to be increased")**;
check Billing and plans of `aon-co-jp` (the workflow was rewritten to a single-job differential design but cannot be verified until billing is resolved). Lessons: `aon-co-jp` is a User (`user/repos`), fine-grained tokens cannot create repos in a personal account (use classic `repo` + `workflow`),
`F:\runo-aruaru-github-token.txt` initially held an `aon-co-jp` token so the destination was itself, bulk creation hits the secondary rate limit.
The GPG-encrypted backup of the VPS data (PostgreSQL, aruaru-db, configuration; private key `F:\vps-data-backup-gpg-PRIVATE.asc`) has its script written but is **not yet deployed to the VPS**.
Old VPS cron commented out, `rs-sync` job disabled (backups `/root/*.bak-20261008`). Details, resume steps and PC-migration steps: `open-github-backup/PORTING.md` and `CLAUDE.md`.

**追記 2026-10-14(完了) / Update (done)**: **日本語**: `runo-aruaru`の146件でActionsを全て無効化、空の`aon-co-jp/vps-data-backup`を削除、宛先だけにある15件(`RCosmo`・`RGit`・`RS-Git`等)は旧名のバックアップなので残し、
10/8以降の新規3件(`cnf-diamond-fiber-battery`・`open-backup`・`open-media`)は課金で自動実行が止まっていたため手動ミラーした。VPSデータの暗号化バックアップ(`vps-data-backup.timer`、毎日03:30)は稼働中・復号確認済み。
**残る課題は`aon-co-jp`のBilling確認のみ**(解消後に`gh workflow run backup.yml`で差分方式を検証)。
**English**: Actions disabled on all 146 `runo-aruaru` repos, the empty `aon-co-jp/vps-data-backup` deleted, the 15 destination-only repos (`RCosmo`, `RGit`, `RS-Git`, …) kept as old-name backups,
and the 3 repos created after 10/8 (`cnf-diamond-fiber-battery`, `open-backup`, `open-media`) mirrored by hand because scheduled runs were blocked by billing. The encrypted VPS data backup (`vps-data-backup.timer`, daily 03:30) is running and restore-verified.
**The only open item is checking Billing of `aon-co-jp`** (then verify the differential design with `gh workflow run backup.yml`).

## JSON処理の使用方針: `parse_secure_sonic`(速い型+安全)と`sonic-rs`は使える所では全て使う(2026-10-14、ユーザー指示)
正本は[`RS-JSON`](https://github.com/aon-co-jp/RS-JSON)(`README.md`・`PORTING.md`)。

**方針**: JSONを読む所は、使える所では**全て** `rust-json`(RS-JSON)の `parse_secure_sonic`(`fast`機能、結果は`sonic_rs::Value`)を使う。
`sonic-rs` を直接使える所(型付き構造体への読み込みなど)も同様。使えない所は `parse_secure`(結果は`serde_json::Value`)を使う。
外部から来る信頼できない入力(HTTP本文・ネットワーク越しのファイル・アップロード)は、**必ずサイズ・深さ・重複キーの上限つき**で読む。

**実測(7 MB・4万件)**: `serde_json` 200 ms / `parse_secure` 217 ms / **`parse_secure_sonic` 83 ms(約2.4倍速い、防御込み)** / `sonic-rs`そのまま 33 ms(約6倍、防御なし)。
`serde_json::Value`に読む限りSIMDでもほぼ速くならない(188 ms)。**速さの源は、結果を連続した領域に詰め込む値の型**。

**使える所 / 使えない所**
- ✅ 読み取り中心で、JSONを大きく・頻繁に読む所(キャッシュJSON、設定、APIの応答、ログ、インデックス)。
- ✅ 外部からの入力の入口(速さより防御が目的。`parse_secure`でも可)。
- ⚠️ `serde_json::Value`を関数間で受け渡している既存コードは、型を`sonic_rs::Value`に直す書き換えが要る(`JsonValueTrait`/`JsonContainerTrait`のメソッド)。書き換えずに`serde_json::Value`へ読むと速くならない。
- ❌ WASM(`rust_json::light`、依存ゼロ)、PHP/JavaScript側のJSON処理(Rustの部品は使えない)。
- 注意: 依存先の`sonic-rs`は内部で`unsafe`を使う(自前コードに`unsafe`は無い)。小さなJSON(数KB)では体感差が出ない。速度目的の書き換えは、実測で効く所から。

**導入**: `Cargo.toml`に `rust-json = { path = "../RS-JSON", features = ["fast"] }`。使用例は`RS-JSON/README.md`。

**このリポジトリでの適用状況**: 未適用(方針のみ)。コードの切り替えは、JSONを大きく・頻繁に読む所から実測して順に行う。

## JSON handling policy: use `parse_secure_sonic` (fast type + secure) and `sonic-rs` everywhere they can be used (2026-10-14, user instruction)
The source of truth is [`RS-JSON`](https://github.com/aon-co-jp/RS-JSON) (`README.md`, `PORTING.md`).

**Policy**: wherever JSON is read, use `parse_secure_sonic` from `rust-json` (RS-JSON, the `fast` feature; the result is `sonic_rs::Value`) **everywhere it can be used**.
Use `sonic-rs` directly where possible too (e.g. reading into typed structs). Where it cannot be used, use `parse_secure` (result: `serde_json::Value`).
Untrusted input from outside (HTTP bodies, files over the network, uploads) **must always be read with size / depth / duplicate-key limits**.

**Measured (7 MB, 40,000 records)**: `serde_json` 200 ms / `parse_secure` 217 ms / **`parse_secure_sonic` 83 ms (about 2.4x faster, with the defences)** / raw `sonic-rs` 33 ms (about 6x, no defences).
Reading into `serde_json::Value` gives almost no speed-up even with SIMD (188 ms). **The speed comes from the value type that packs the result into contiguous memory.**

**Where it can / cannot be used**
- ✅ Read-heavy code that parses large or frequent JSON (cache JSON, config, API responses, logs, indexes).
- ✅ Entrances for outside input (the goal there is defence rather than speed; `parse_secure` is fine).
- ⚠️ Existing code that passes `serde_json::Value` between functions needs its type changed to `sonic_rs::Value` (methods from `JsonValueTrait` / `JsonContainerTrait`). Reading into `serde_json::Value` without that change is not faster.
- ❌ WASM (`rust_json::light`, zero dependencies) and the JSON handling on the PHP / JavaScript side (Rust components cannot be used there).
- Note: the `sonic-rs` dependency uses `unsafe` internally (our own code has none). For small JSON (a few KB) the difference is not noticeable; do speed-motivated rewrites where measurements show a benefit.

**Adoption**: in `Cargo.toml`, `rust-json = { path = "../RS-JSON", features = ["fast"] }`. Example in `RS-JSON/README.md`.

**Status in this repository**: Not yet applied (policy only). Code will be switched over place by place, starting where measurements show large or frequent JSON reads.

## アカウント引っ越しのための引き継ぎ(2026-10-14)

別のアカウントのClaudeで作業を続けるための、事実だけの引き継ぎ。**秘密(APIキー・パスワード・トークン)の値はここに書かない**(場所だけ)。
別アカウントのClaudeは、まず各リポジトリの`CLAUDE.md`冒頭と、このPORTINGの本節を読むこと。

### 環境(推測せず確認する)
- 作業ドライブは`F:\`(Windows)。本番は **ConoHa VPS**(`ssh conoha`、AlmaLinux、4コア・RAM 3.6GB・GPUなし)。リポジトリはVPSの`/root/repository/`と`/root/url/`にもある。
- 秘密は`F:\`直下のtxt(`github-token.txt`、`ARUARU_LLM_*`、`lolipop*.txt`等)とVPSの`.env.*`(`/root/aruaru-llm/`)。**値を画面・コミット・チャットに出さない**。`lolipop*.txt`にはパスワードがある(2026-10-08に誤って一部を表示したので、パスワード変更を推奨済み)。
- 別アカウントではClaudeの記憶(`~/.claude/projects/F--runo/memory/`)が引き継がれない可能性がある。この節と各リポジトリの`CLAUDE.md`が正。
- ネットワーク/SSHが間欠的に詰まる。重い操作は1つずつ、バックグラウンド+監視で。VPSの負荷自体は低い(load 0.00)。

### 2026-10-08〜14に完了したこと(いずれもpush済み・本番確認済み)
- **audiocafe.tokyoの毎朝クロール**: ロリポップのcronは削除済み、VPSのsystemdタイマー2本(`audiocafe-cron-rust`・`audiocafe-cron-php`、毎朝05:00)。止まっていた技術ランキング等を修正(`--cron-tech`)。
- **AI学習コメント**: OpenAIは使わず`aruaru-llm`経由(Gemini/Groq/Mistral等の無料枠)。AIが書いた価格欄は24件中23件が誤りだったため、実取得価格に訂正し、`aruaru-llm`の知識ストアに学習→GitHub(`open-english/data/knowledge`)へ自動バックアップ(復元テスト合格)。「無料」表記474件も検証。
- **サイトへの掲載**: `audiocafe.tokyo/aruaru`・`aruaru.tokyo`にオンライン学習サイト5件、AI駆動開発の研究記事、AI学習リンク(120技術・612件)。
- **PHPコードのGit化**: `aon-co-jp/audiocafe-tokyo`(ハイフン)へ3方向マージで保存、`deploy/vps/`にsystemd・nginx、引越し手順は同リポジトリのPORTING「VPS お引越し手順」。
- **`aruaru-llm`**: 知識検索の日本語対応、外部取り込みを`parse_secure`で。**`RS-JSON`**: `parse_secure`/`parse_secure_sonic`(実測: `serde_json`200ms・安全版217ms・**`parse_secure_sonic`83ms**)。**`open-easy-web`**: ロリポップ向け時間指定オートクロール+設定画面+後追い実行。

### 未完了・要判断(優先順)
1. **`open-web-server`がVPSに未pushの独自コミット2件(certbot webroot修正・ストリーミング対応)+未コミット16件を持つ**。GitHubに無い本物の作業。**早めにpush**(履歴を触らない、`git pull --rebase`などは慎重に)。
2. **JSON処理の実コード切り替えは未実施**(`sonic-rs`は2026-10-15に新設した`RS-JSON`の姉妹リポジトリ=評価記録と方針、コードは`RS-JSON`)(方針は16リポジトリに記載済み)。効果が見込めるのは`audiocafe-tokyo-rust`の`fetch_cache`(ページ表示のたびに約200KBのJSONを読み直す)。`serde_json::Value`を`sonic_rs::Value`に直す書き換えが必要。小さなJSONでは差が出ない。
3. **`maid-cafe-se`は上流(push先)未設定**のためpushしていない。
4. **新品VPSでの引越し通し試験は未実施**(手順書・`install-units.sh`は未検証)。
5. 本番`audiocafe.tokyo`のPHPは、`audiocafe-tokyo`リポジトリより古い部分がある(例: `rakuten-mobile`の言語切替)。リポジトリを本番に入れる前に差分を確認。

### 注意(過去の事故・落とし穴)
- GitHub上の`aruaru-llm`・`audiocafe-tokyo-rust`は**履歴が書き直されている**(内容は同じでハッシュが違う)。手元とVPSは揃え済み、旧履歴は`backup-before-rewrite-20261014`/`vps-before-rewrite-20261014`ブランチ。誰が書き直したかは不明。強制pushしない。
- `aruaru-llm`は`../RS-JSON`を相対パスで参照する。VPSでビルドする前に`RS-JSON`を最新にする。
- 知識検索(`aruaru-llm`)は日本語バイグラム対応済みだが、知識は公開リポジトリに保存されるため、公開してよい内容だけを入れる。
- 禁止事項に注意: パスワードでのログイン、秘密の値の表示、強制push、確認なしの削除。

## Hand-off for moving to another account (2026-10-14)

Facts-only hand-off so work can continue with Claude on another account. **No secret values (API keys, passwords, tokens) are written here** — only where they live.
The next Claude should first read the top of each repository's `CLAUDE.md` and this section of PORTING.

### Environment (verify, do not assume)
- Work drive is `F:\` (Windows). Production is a **ConoHa VPS** (`ssh conoha`, AlmaLinux, 4 cores, 3.6 GB RAM, no GPU). The repositories also live on the VPS under `/root/repository/` and `/root/url/`.
- Secrets live in txt files at the root of `F:\` (`github-token.txt`, `ARUARU_LLM_*`, `lolipop*.txt`, ...) and in the VPS `.env.*` files (`/root/aruaru-llm/`). **Never print values on screen, in commits or in chat.** `lolipop*.txt` contains a password (part of a file was displayed by mistake on 2026-10-08; changing the password was recommended).
- Claude's memory (`~/.claude/projects/F--runo/memory/`) may not carry over to another account. This section and each repository's `CLAUDE.md` are the source of truth.
- Network/SSH sometimes stalls intermittently. Do heavy operations one at a time, in the background with monitoring. The VPS itself is lightly loaded (load 0.00).

### Done 2026-10-08 to 14 (all pushed and verified on production)
- **Daily crawl of audiocafe.tokyo**: the Lolipop cron was removed; two systemd timers on the VPS (`audiocafe-cron-rust`, `audiocafe-cron-php`, daily 05:00). Fixed the stalled tech ranking etc. (`--cron-tech`).
- **AI learning comments**: OpenAI is not used; they go through `aruaru-llm` (Gemini/Groq/Mistral free tiers). 23 of 24 AI-written prices were wrong, so they are corrected to the crawled prices, taught to the `aruaru-llm` knowledge store and automatically backed up to GitHub (`open-english/data/knowledge`; restore test passed). 474 "free" claims were also verified.
- **On the sites**: `audiocafe.tokyo/aruaru` and `aruaru.tokyo` show five online-learning sites, the AI-driven-development research article and the AI learning links (120 technologies, 612 links).
- **PHP code under Git**: saved to `aon-co-jp/audiocafe-tokyo` (hyphen) by a three-way merge; systemd and nginx files in `deploy/vps/`; the migration procedure is in that repository's PORTING ("VPS migration guide").
- **`aruaru-llm`**: Japanese knowledge search, outside imports read with `parse_secure`. **`RS-JSON`**: `parse_secure` / `parse_secure_sonic` (measured: `serde_json` 200 ms, secure 217 ms, **`parse_secure_sonic` 83 ms**). **`open-easy-web`**: timed auto-crawl for Lolipop + settings screen + catch-up runs.

### Not done / needs a decision (in priority order)
1. **`open-web-server` has two un-pushed commits on the VPS (certbot webroot fix, streaming support) plus 16 uncommitted files.** Real work that is not on GitHub. **Push it soon** (do not touch the history; be careful with `git pull --rebase` etc.).
2. **The actual JSON code switch-over has not been done** (`sonic-rs`, created 2026-10-15, is the sister repository of `RS-JSON`: evaluation notes and policy; the code is in `RS-JSON`) (the policy is written in 16 repositories). The best candidate is `fetch_cache` in `audiocafe-tokyo-rust` (re-parses ~200 KB of JSON on every page view). It needs `serde_json::Value` rewritten to `sonic_rs::Value`. Small JSON shows no difference.
3. **`maid-cafe-se` has no upstream (push target)**, so it was not pushed.
4. **No end-to-end migration test on a fresh VPS yet** (the runbook and `install-units.sh` are untested).
5. The PHP on production `audiocafe.tokyo` is older than the `audiocafe-tokyo` repository in places (e.g. the `rakuten-mobile` language switcher). Review the diff before deploying the repo to production.

### Pitfalls (past incidents)
- On GitHub, `aruaru-llm` and `audiocafe-tokyo-rust` have **rewritten history** (same content, different hashes). Local copies and the VPS are aligned; the old history is kept in the `backup-before-rewrite-20261014` / `vps-before-rewrite-20261014` branches. Who rewrote it is unknown. Do not force-push.
- `aruaru-llm` references `../RS-JSON` by relative path. Update `RS-JSON` before building on the VPS.
- Knowledge search in `aruaru-llm` handles Japanese (bigrams), but knowledge is stored in a public repository, so only put publishable content in it.
- Mind the prohibitions: logging in with passwords, printing secret values, force-pushing, deleting without confirmation.

## 公開リポジトリの個人情報の取り除き(2026-10-16) — アカウント引っ越しの引き継ぎ(続き)

> **【決定 2026-10-16】ユーザーが「作者名は本名に統一」と決定した。以下の「未決」(匿名方針と本名コミットの食い違い)は解決済みで、匿名化の方針は取り下げ。本名のコミットは取り消さない。`scrub-history.sh`による内容の名前除去も不要。`git pull`禁止(古い履歴が戻る)の注意だけは有効。** / *Decision (2026-10-16): the user chose the real name as the author for everything; the open conflict below is resolved and the anonymous policy is withdrawn. Do not revert real-name commits; the content scrub is not needed. Only the "never git pull in a rewritten repo" warning still applies.*

**Claudeの記憶はアカウントを消すと失われる前提で、ここに全部書く。** 秘密の値・個人の名前やメールの文字列は、この公開リポジトリには書かない(場所と手順だけ)。

### ユーザーの方針(会話での指示、時系列の最終形)
1. **公開リポジトリのコミットの作者・コミッターは匿名**にする: 名前 `aon-co-jp`、メール `18116749+aon-co-jp@users.noreply.github.com`(GitHubの匿名用)。**今後のコミットも匿名**(PCのグローバル設定・`open-english-pc`のローカル設定・VPSのグローバル設定を変更済み)。
2. **第三者(他の開発者)の作者表示は残す**: 元のOSSの作者や、取り込んだ変更の作者(`pdf-r2l-win` など)は、その人自身が公開した情報で、ライセンス上の著作者表示でもある。書き換えない。
3. **ファイルの内容にある、ユーザー本人の名前・メールは削除**する。例外は、`open-english`の「作者を聞かれたときの答え」の中の**名前だけ**(表記は日本語の姓名を、1文字ずつ空白で区切った形)。住所・趣味・職業・夢の話・第三者の事情は残さない。
4. **検索や収集で集めた第三者の個人名**は削除(履歴の作者は収集ではないので該当しない)。実在の私人(名前が不確か)を、家族の事情と結びつけて載せない(`open-english`の自己紹介にあった記述は、この理由で取り除く)。
5. **強制pushはユーザーが明示して許可した範囲だけ**(この作業)。他の用途では強制pushしない。

### やったこと(完了・確認済み)
- **112個の公開リポジトリ**(`gh repo list aon-co-jp`のうちPUBLIC)の、**全ブランチ・タグのコミットの作者・コミッター**を匿名に書き換え。89個を書き換え、17個は対象のコミットが無い(空や第三者のみ)。書き換え前後で**全ブランチ・タグのファイルの内容(ツリー)が同一**であることを確かめてから、`--force-with-lease`で強制push(取得後にGitHubが変わっていたら拒否=他のセッションの新しいコミットを上書きしない)。全件で、既定ブランチの先頭が一致することを確認。
- `open-backup`は、加えて、誤って履歴に入っていたビルドの生成物(ユーザー名入りのパス)を履歴から除去し、配布物(Windows/Linux/Android)は`--remap-path-prefix`で作り直した(`open-backup/scripts/build-release.ps1`)。
- **書き換え前の完全なコピー**(ミラー、全ブランチ・タグ)を、`F:\_anon\backup\<リポジトリ>.git`(112個、約800MB)と、WSL `~/anon/backup/`に保存。**これらは旧い個人情報入りの履歴なので、公開リポジトリやクラウドに上げない**。復元は、そのミラーから`git push --force`(慎重に)。
- 作業スクリプトは`F:\_anon\`(`anonymize-repo.sh` 1リポジトリの書き換え、`scrub-history.sh` 履歴の中身からの文字列の除去、`run-wsl.sh` WSLで8並列、`get-token.sh`、`vps-sync.sh` VPSの写しの整列、`wsl-setup.sh`)。**取り除く文字列そのものを含むので、公開リポジトリにコミットしない**(非公開リポジトリか、手元だけで保管)。実行の記録は`F:\_anon\wsl-summary.log`と`F:\_anon\wsl-logs\`。
- 手元の写し(`F:\`の公開リポジトリ46個)を新しい履歴に揃えた(`git reset --mixed origin/<ブランチ>`。作業中のファイルは残る)。

### 未了・未決(優先順)
1. **【要判断】別のセッションが、同時期に「作者名を、本人の名前に統一(`Cargo.toml`の`authors`)」というコミットを複数のリポジトリへ push している**(`aruaru-IME`・`open-media`・`open-directx`・`rs-FFmpeg`・`rs-xorriso`・`runo`・`open-raid-z`…)。しかもそのセッションのコミットの作者名が本人の名前になっている。**上の方針1・3と食い違う**。どちらにするか、ユーザーに確認する(確認前に、その変更を取り消したり、書き換えたりしない)。
2. **ファイルの内容(`CLAUDE.md`・README・ソース)にある本人の名前・メールの取り除き**(現在のファイルと履歴の両方): 未実施(1の判断待ち)。`scrub-history.sh`が、履歴の全コミットの内容を文字列置換する(第三者の私人の名前、本人のメール、本人の名前)。実施前に、`open-english`だけは、作者の答えのコードを書き戻す最後のコミットが要る。
3. **`open-english`の作者の答え**(`web/app.js`と`mobile/android/app/src/main/assets/webroot/app.js`の同一コピー、`creatorIntroductionText`): 名前だけにする(未実施)。パズルの紹介文・運営者の説明の名前は削除。
4. **VPSの写しの整列**(`/root/repository/*`・`/root/easy-web.tokyo/*`): 未実施。2の後に1回でまとめて行う(`F:\_anon\vps-sync.sh report`で状況を見て、`apply`は内容が同一のものだけ)。VPSには、GitHubに無い本物の作業がある(`open-web-server`など)。**`git pull`はしない**(古い履歴が戻る)。
5. 手元に、他のセッションの未push作業があり、触っていない: `RS-JSON`(7コミット)、`open-raid-z`。
6. **GitHub上の旧コミットは、コミットIDを知っていれば閲覧できる場合がある**(キャッシュ・フォーク)。完全に消すには、GitHubサポートに、キャッシュされたビューとフォークの削除を依頼する。

### 注意(落とし穴)
- **履歴を書き換えたリポジトリで`git pull`しない**。古い履歴がマージで戻り、個人情報を再公開する。揃え方は`git fetch origin && git reset --mixed origin/<ブランチ>`(未pushのコミットが無いことを、`git cherry -v origin/<ブランチ> HEAD`などで先に確認)。
- 書き換えは、WSL(Linux)のgitで行う(Windowsのgitは1コミット約1.3秒で、WSLは数十倍速い)。`wsl`へのコマンドは、Git Bashだと`/mnt/...`が勝手にWindowsのパスに変換される(`MSYS_NO_PATHCONV=1`を付ける)。入れ子の引用符で変数が消える→スクリプトをファイルにして渡す。
- 認証は、WSLの中から`"/mnt/c/Program Files/GitHub CLI/gh.exe" auth token`で環境変数に入れる(ファイルに残さない)。

## Removing personal information from public repositories (2026-10-16) — account-move hand-off (continued)

**Written on the assumption that Claude's memory is lost when the account is deleted.** No secret values and no personal name/e-mail strings are written in this public repository (only locations and procedures).

### The user's policy (given in conversation; final form, in time order)
1. **Commit authors and committers of public repositories are anonymous**: name `aon-co-jp`, e-mail `18116749+aon-co-jp@users.noreply.github.com` (GitHub's anonymous address). **Future commits are anonymous too** (global git settings on the PC and on the VPS, and the local setting of `open-english-pc`, were changed).
2. **Third parties' (other developers') author attribution stays**: original OSS authors and authors of merged changes (e.g. in `pdf-r2l-win`) published it themselves, and it is also licence attribution. It is not rewritten.
3. **The user's own name/e-mail inside file contents is removed**. The only exception is the **name alone** in `open-english`'s answer to "who is the author?" (the Japanese full name written with a space between every character). No address, hobbies, occupation, dream story or third parties' circumstances.
4. **Third parties' personal names gathered by search/crawling are removed** (commit authors are not gathered, so they do not apply). A real private individual (with an uncertain name) must not be tied to family circumstances (the passage in `open-english`'s self-introduction is removed for this reason).
5. **Force-pushing only within what the user explicitly allowed** (this operation). No force-pushing for anything else.

### Done (complete, verified)
- Rewrote the author/committer of **all branches and tags** of the **112 public repositories** (`gh repo list aon-co-jp`, PUBLIC) to the anonymous identity: 89 rewritten, 17 had nothing to rewrite (empty or third-party only). Before pushing, verified that the **file contents (trees) of every branch/tag are identical** before and after; pushed with `--force-with-lease` (refused if GitHub changed after the clone, so another session's new commits are never overwritten). For all of them the default-branch tip was verified to match.
- For `open-backup`, additionally removed build artifacts (paths containing the user name) that had slipped into its history, and rebuilt the release assets (Windows/Linux/Android) with `--remap-path-prefix` (`open-backup/scripts/build-release.ps1`).
- **Complete pre-rewrite mirrors** (all branches and tags) are kept in `F:\_anon\backup\<repo>.git` (112 repositories, ~800 MB) and in WSL `~/anon/backup/`. **They hold the old history with personal information, so never upload them to a public repository or cloud.** Restore by `git push --force` from the mirror (carefully).
- Working scripts live in `F:\_anon\` (`anonymize-repo.sh` rewrite one repository, `scrub-history.sh` remove strings from the content of history, `run-wsl.sh` 8-way parallel in WSL, `get-token.sh`, `vps-sync.sh` align the VPS clones, `wsl-setup.sh`). **They contain the very strings to remove, so never commit them to a public repository** (keep them in a private repository or locally only). Run records: `F:\_anon\wsl-summary.log` and `F:\_anon\wsl-logs\`.
- Aligned the local clones (46 public repositories on `F:\`) with the new history (`git reset --mixed origin/<branch>`; working files are kept).

### Not done / needs a decision (priority order)
1. **[Decision needed] Another session pushed commits at about the same time that "unify the author name to the real name (`authors` in `Cargo.toml`)" to several repositories** (`aruaru-IME`, `open-media`, `open-directx`, `rs-FFmpeg`, `rs-xorriso`, `runo`, `open-raid-z`, ...), and that session's commit author name is the real name. **This conflicts with policy 1 and 3 above.** Ask the user which one applies (do not revert or rewrite those changes before asking).
2. **Removing the user's name/e-mail from file contents (`CLAUDE.md`, READMEs, sources)** (current files and history): not done (waiting for decision 1). `scrub-history.sh` string-replaces the content of every commit (private third-party names, the user's e-mail, the user's name). Before running it, `open-english` needs a final commit that restores the author-answer code.
3. **`open-english`'s author answer** (`web/app.js` and its identical copy `mobile/android/app/src/main/assets/webroot/app.js`, `creatorIntroductionText`): reduce to the name only (not done). Remove the name from puzzle intros and the operator statement.
4. **Aligning the VPS clones** (`/root/repository/*`, `/root/easy-web.tokyo/*`): not done. Do it once after step 2 (`F:\_anon\vps-sync.sh report` to look, `apply` only resets clones whose content is identical). The VPS holds real work that is not on GitHub (e.g. `open-web-server`). **Do not `git pull`** (the old history would come back).
5. Other sessions' un-pushed local work was left untouched: `RS-JSON` (7 commits), `open-raid-z`.
6. **Old commits on GitHub may still be viewable by commit ID** (caches, forks). To remove them completely, ask GitHub Support to purge cached views and forks.

### Pitfalls
- **Never `git pull` in a repository whose history was rewritten.** The old history would be merged back and re-publish the personal information. Align with `git fetch origin && git reset --mixed origin/<branch>` (first check there are no un-pushed commits, e.g. `git cherry -v origin/<branch> HEAD`).
- Rewrite with git inside WSL (Linux): Windows git takes ~1.3 s per commit, WSL is tens of times faster. Git Bash silently converts `/mnt/...` arguments to Windows paths for `wsl` (set `MSYS_NO_PATHCONV=1`). Nested quoting loses variables → pass a script file.
- Authenticate from inside WSL with `"/mnt/c/Program Files/GitHub CLI/gh.exe" auth token` into an environment variable (do not leave it in a file).

## 2026-10-16 easy-web.tokyoへの紹介ページ追加の調査結果 / Survey for adding intro pages to easy-web.tokyo

**日本語**: `easy-web.tokyo`はnginx→`open-easy-web`サーバー(ポート8080)で、**各リポジトリの`webpage/index.html`を`/<リポジトリ名>/`として配信**する(例: `/root/easy-web.tokyo/open-backup/webpage/index.html`)。
VPSの`/root/easy-web.tokyo/<名前>`に`git clone`し、`webpage/index.html`があれば紹介される。`/ime`は専用の配信で、ダウンロードはGitHubリリースのURLへ誘導する。
2026-10-16時点の紹介済み: `open-english`・`open-backup`・`rs-sync`・`open-web-server`・`/ime`(aruaru-IME)。VPSにフォルダはあるが`webpage/`が無く404: `open-cuda`・`open-directx`・`open-raid-z`・`open-kagaku`・`open-cg-cad`・`open-cpu`・`RPoem`・`RS-Guard`・`RS-JSON`・`RS-SmartTCP`・`aruaru-jobs`。
**配布物(GitHubリリース)を持つ公開リポジトリのうち未紹介**: `open-media`(v0.1.10)・`open-bar`(v0.1.0)・`make-disk`(v0.1.32)・`open-cuda`(v0.4.1)・`open-raid-z`(v0.1.0)・`open-cpu`(v0.1.0)・`RPoem`(v0.1.0)・`pdf-r2l-rs`(v1.3.0)・`maid-cafe-se`(v0.5.3)。`RS-Guard`(v0.1.0)は`runo.tokyo/RS-Guard`で別途紹介済み。
公開ページはOTP不要(ダウンロードはGitHubのリリースURL)。管理画面だけを本人限定にする場合は`open-easy-web`の既存のメールOTP(`auth.rs`/`totp.rs`)を使う。`/demo`は実際に動かせるもの(`open-english`など)だけに付ける。
`open-github-backup`(非公開、インフラ用)は紹介ページを作らない。

**English**: `easy-web.tokyo` is nginx → the `open-easy-web` server (port 8080), which **serves each repository's `webpage/index.html` at `/<repository name>/`** (e.g. `/root/easy-web.tokyo/open-backup/webpage/index.html`).
Clone the repo to `/root/easy-web.tokyo/<name>` on the VPS and it is introduced if `webpage/index.html` exists. `/ime` has its own handler and points downloads at GitHub release URLs.
Already introduced as of 2026-10-16: `open-english`, `open-backup`, `rs-sync`, `open-web-server`, `/ime` (aruaru-IME). Folders exist on the VPS but return 404 for lack of `webpage/`: `open-cuda`, `open-directx`, `open-raid-z`, `open-kagaku`, `open-cg-cad`, `open-cpu`, `RPoem`, `RS-Guard`, `RS-JSON`, `RS-SmartTCP`, `aruaru-jobs`.
**Public repos with GitHub releases that are not yet introduced**: `open-media` (v0.1.10), `open-bar` (v0.1.0), `make-disk` (v0.1.32), `open-cuda` (v0.4.1), `open-raid-z` (v0.1.0), `open-cpu` (v0.1.0), `RPoem` (v0.1.0), `pdf-r2l-rs` (v1.3.0), `maid-cafe-se` (v0.5.3). `RS-Guard` (v0.1.0) is already introduced separately at `runo.tokyo/RS-Guard`.
Public pages need no OTP (downloads go to GitHub release URLs). To restrict only an admin console to the owner, use the existing email OTP of `open-easy-web` (`auth.rs` / `totp.rs`). Add `/demo` only for things that can really run (e.g. `open-english`).
`open-github-backup` (private, infrastructure) gets no intro page.

### 追記(2026-10-16): 紹介ページを実際に公開した / Intro pages actually published

**日本語**: 上の調査の「`webpage/index.html`があれば紹介される」は**誤り**だった。実際は、リポジトリごとに静的配信のsystemdサービス(`<名前>-web.service`、`python3 -m http.server <ポート> --bind 127.0.0.1`、`WorkingDirectory=/root/easy-web.tokyo/<名前>/webpage`)を立て、VPSの`/root/open-web-server/domains.toml`(`/root/repository/open-web-server/domains.toml`は同一ファイル)に`path_prefix = "/<名前>"`の`[[domain]]`を足し、`open-web-server`を再起動して初めて公開される(`:8080`は`webpage/`を配信しない)。
今回公開: `open-media`(8117)・`pdf-r2l-rs`(8118)・`maid-cafe-se`(8119)・`open-cuda`(8120)・`open-cpu`(8121)・`RPoem`(8122)。`open-cuda`・`open-cpu`・`RPoem`は`webpage/index.html`を新規作成してpush。`open-bar`・`make-disk`・`open-raid-z`は以前から公開済みだった。
VPSの`open-cuda`・`open-cpu`・`RPoem`のcloneは履歴書き換え後の別履歴だったため(未pushなし・変更なしを確認して)`git reset --hard origin/main`で揃えた。`domains.toml`の変更前は`domains.toml.bak-20261016-intro6`。空きポートは8123以降。

**English**: The survey above was wrong that a `webpage/index.html` is enough. A page goes live only when (1) a per-repo static systemd service (`<name>-web.service`, `python3 -m http.server <port> --bind 127.0.0.1`, `WorkingDirectory=/root/easy-web.tokyo/<name>/webpage`) runs, (2) a `[[domain]]` with `path_prefix = "/<name>"` is added to `/root/open-web-server/domains.toml` (same file as `/root/repository/open-web-server/domains.toml`), and (3) `open-web-server` is restarted (`:8080` does not serve `webpage/`).
Published now: `open-media` (8117), `pdf-r2l-rs` (8118), `maid-cafe-se` (8119), `open-cuda` (8120), `open-cpu` (8121), `RPoem` (8122); pages for `open-cuda`, `open-cpu`, `RPoem` were newly written and pushed. `open-bar`, `make-disk`, `open-raid-z` were already live. The VPS clones of those three had the pre-rewrite history; after confirming nothing unpushed/dirty they were aligned with `git reset --hard origin/main`. Backup before the edit: `domains.toml.bak-20261016-intro6`. Free ports start at 8123.

## 2026-10-18 open-vsc-claude新設・easy-web.tokyo/open-vps-claudeにデモ公開 / open-vsc-claude created, demo live at easy-web.tokyo/open-vps-claude

**日本語**: VS Code拡張[`open-vsc-claude`](https://github.com/aon-co-jp/open-vsc-claude)(公開、MIT、v0.1.1)を新設。言語・フレームワーク(GraphQL+Cosmo/RPoem、TypeScript+Node+REST、自由入力)を選んでプレビュー、Claudeで改良、保存。Web拡張(vscode.dev等)・ブラウザデモ(PWA)・SHA-256検証つき更新確認・README/CLAUDE/PORTINGを12言語で用意。
RPoemには外部サブグラフへのHTTP中継を実装(`RPoem`の`babc658`)。VPS公開は`easy-web.tokyo/open-vps-claude`(所有者指定のパス。リポジトリ名は`open-vsc-claude`):`/root/easy-web.tokyo/open-vsc-claude`にclone、`open-vps-claude-web.service`(8123、`webpage/`)、`domains.toml`に`path_prefix = "/open-vps-claude"`を追加(変更前は`domains.toml.bak-20261018-vpsclaude`)。更新は`git pull --ff-only`だけ(静的配信)。
**未了**: VS Code Marketplace/Open VSX公開(所有者のアカウントとトークンが必要、手順は同リポジトリの`PUBLISHING.md`)、Cosmo Routerの実起動、実キーでのClaude生成、実機iOS/Android、翻訳のネイティブ確認、`aruaru-tokyo`側の索引への追従。

**English**: Created the public VS Code extension [`open-vsc-claude`](https://github.com/aon-co-jp/open-vsc-claude) (MIT, v0.1.1): pick a stack (GraphQL+Cosmo/RPoem, TypeScript+Node+REST, or free-form), preview, refine with Claude, save. Includes a web extension (vscode.dev etc.), a browser demo (PWA), an update check with SHA-256 verification, and README/CLAUDE/PORTING in 12 languages.
RPoem now forwards to external subgraphs over HTTP (`RPoem` `babc658`). The VPS demo is at `easy-web.tokyo/open-vps-claude` (the path the owner asked for; the repository is `open-vsc-claude`): cloned to `/root/easy-web.tokyo/open-vsc-claude`, `open-vps-claude-web.service` (port 8123, `webpage/`), and a `domains.toml` entry with `path_prefix = "/open-vps-claude"` (backup `domains.toml.bak-20261018-vpsclaude`). Updating is just `git pull --ff-only` (static).
**Open**: Marketplace/Open VSX publication (owner account + token; steps in the repo's `PUBLISHING.md`), running the Cosmo Router, Claude generation with a real key, real iOS/Android devices, native review of translations, and mirroring the index into `aruaru-tokyo`.

## 2026-10-18 Windows再起動前の引き継ぎ(dream-os用VS Code) / Hand-off before the Windows restart (VS Code for dream-os)

**日本語**: `F:\dream-os\vsc`(コミット`c130a1b`)に、dream-os用Visual Studio Code=**Code-OSS**(VS Code本体のOSS版、MIT)のビルド・パッケージ手順を追加し、`open-vsc-claude`を組み込み拡張として同梱する構成にした。WSL2のUbuntuで`build.sh`を実行し、**node・clone(1.142.0)・`npm ci`は完了、`gulp vscode-linux-x64-min`は`package-linux-x64`まで成功したが最終工程のCopilot準備で失敗(原因未調査)、同梱と`verify.sh`は未実行**。`verify.sh`(拡張ホストで`open-vsc-claude`が有効化されるか)も未実行なので「ビルドできた」とはまだ言えない。再開コマンド・落とし穴は`dream-os/vsc/BUILD-REPORT.md`。互換性の契約(最小VS Code 1.85・VSCodium 1.140・Web拡張で実機確認済み)は`open-vsc-claude/docs/COMPATIBILITY.md`。dream-os自体はまだ起動できるOSではないため、検証はWSL2のUbuntuで行う。
**English**: Added build/package scripts for **Code-OSS** (the MIT-licensed core of VS Code) as "VS Code for dream-os" in `F:\dream-os\vsc` (commit `c130a1b`), bundling `open-vsc-claude` as a built-in extension. Run with `build.sh` in WSL2 Ubuntu: **node, clone (1.142.0) and `npm ci` are done; `gulp vscode-linux-x64-min` got through `package-linux-x64` but failed at the final Copilot step (cause not investigated); bundling and `verify.sh` have not run**; `verify.sh` has not been run, so do not claim it builds yet. Resume commands and pitfalls: `dream-os/vsc/BUILD-REPORT.md`. The host contract (verified on VS Code 1.85, VSCodium 1.140 and the web extension host) is `open-vsc-claude/docs/COMPATIBILITY.md`. dream-os itself is not a bootable OS yet, so verification happens on Ubuntu in WSL2.

## API 方針: REST 全廃・gRPC / Connect へ (2026-11-04)

### 日本語
- **REST は全廃する。新しい API は REST で作らない。** ブラウザや `curl` から呼ぶ API は **Connect の単純呼び出し**(`POST /<パッケージ>.<Service>/<Method>`、`content-type: application/json`、本文は JSON)、サービス間は **gRPC / gRPC-web**(RPoem の管理API `open_runo.admin.v1.Admin` と同じ流儀)。ストリーミングは、必要になってから。
- **既存の REST は、触るときに順に移す。** 移したら旧 REST の経路は消す。移行が終わるまで残るが、**新規には追加しない**。
- **JSON は RS-JSON に統一**する(読み込みは `from_str_secure` / `parse_secure` でサイズ・深さ・重複キーの上限つき、書き出しは `rust_json::fast`)。ブラウザの WASM に `prost` は入れない(サイズが増えるため)。
- **例外(自分たちの API ではなく、相手の規格が決めているもの)**: ACME、OAuth/OIDC のコールバック、第三者(GitHub など)からの Webhook、ヘルスチェック、静的ファイル配信、OTLP など。これらは規格どおりの HTTP を受ける。
- 参考実装: `RPoem`(`open_runo.admin.v1.Admin`)、`open-easy-web`(`server/src/connect.rs`、`proto/open_easy_web/admin/v1/admin.proto`)。
- ※ このリポジトリのコードが既に方針どおりかどうかは、各リポジトリの現状による。この節は方針の記録であり、コードの変更を意味しない。

### English
- **REST is being abolished. New APIs are not built as REST.** APIs called from browsers or `curl` use **Connect unary calls** (`POST /<package>.<Service>/<Method>`, `content-type: application/json`, JSON body); service-to-service calls use **gRPC / gRPC-web** (the same style as RPoem's admin API `open_runo.admin.v1.Admin`). Streaming only when it is actually needed.
- **Existing REST endpoints are migrated one by one, when they are touched.** The old REST route is removed once migrated. Until migration is finished they remain, but **no new ones are added**.
- **JSON is unified on RS-JSON**: reading with `from_str_secure` / `parse_secure` (size, depth and duplicate-key limits), writing with `rust_json::fast`. `prost` is not put into browser WASM (it would grow the binary).
- **Exceptions (shapes dictated by someone else's standard, not our own API)**: ACME, OAuth/OIDC callbacks, webhooks from third parties (e.g. GitHub), health checks, static file serving, OTLP, and so on. These accept plain HTTP as the standard requires.
- Reference implementations: `RPoem` (`open_runo.admin.v1.Admin`) and `open-easy-web` (`server/src/connect.rs`, `proto/open_easy_web/admin/v1/admin.proto`).
- Note: whether the code in a given repository already follows this policy depends on that repository. This section records the policy; it does not mean the code has been changed.

### Deutsch (KI-Übersetzung, redaktionell überarbeitet; noch nicht von Muttersprachlern geprüft)
- **REST wird vollständig abgeschafft; neue APIs entstehen nicht mehr als REST.** APIs, die aus dem Browser oder per `curl` aufgerufen werden, verwenden **unäre Connect-Aufrufe** (`POST /<Paket>.<Service>/<Methode>`, `content-type: application/json`, JSON-Body). Zwischen Diensten kommen **gRPC bzw. gRPC-web** zum Einsatz, im selben Stil wie die Admin-API von RPoem (`open_runo.admin.v1.Admin`). Streaming wird erst ergänzt, wenn es tatsächlich gebraucht wird.
- **Bestehende REST-Endpunkte werden schrittweise umgestellt, und zwar immer dann, wenn man ohnehin an ihnen arbeitet.** Sobald ein Endpunkt umgestellt ist, wird die alte REST-Route entfernt. Bis zum Abschluss der Migration bleiben die übrigen bestehen, es werden aber **keine neuen mehr hinzugefügt**.
- **JSON wird einheitlich über RS-JSON verarbeitet**: Gelesen wird mit `from_str_secure` bzw. `parse_secure` (mit Obergrenzen für Größe, Verschachtelungstiefe und doppelte Schlüssel), geschrieben mit `rust_json::fast`. `prost` wird nicht in das Browser-WASM aufgenommen, da es die Datei vergrößern würde.
- **Ausnahmen (Schnittstellen, deren Form ein fremder Standard vorgibt und die nicht zu unserer eigenen API gehören)**: ACME, OAuth/OIDC-Callbacks, Webhooks von Drittanbietern (z. B. GitHub), Health-Checks, die Auslieferung statischer Dateien, OTLP und Ähnliches. Diese nehmen, wie vom jeweiligen Standard verlangt, gewöhnliches HTTP entgegen.
- Referenzimplementierungen: `RPoem` (`open_runo.admin.v1.Admin`) und `open-easy-web` (`server/src/connect.rs`, `proto/open_easy_web/admin/v1/admin.proto`).
- Hinweis: Ob der Code eines einzelnen Repositorys diese Richtlinie bereits erfüllt, hängt vom jeweiligen Repository ab. Dieser Abschnitt dokumentiert lediglich die Richtlinie; er besagt nicht, dass der Code schon angepasst wurde.

### Русский (перевод выполнен с помощью ИИ и отредактирован; носителями языка пока не проверен)
- **От REST мы полностью отказываемся; новые API больше не создаются в стиле REST.** API, к которым обращаются из браузера или через `curl`, используют **унарные вызовы Connect** (`POST /<пакет>.<Service>/<Method>`, `content-type: application/json`, тело запроса — JSON). Для взаимодействия между сервисами применяются **gRPC и gRPC-web** — в том же стиле, что и административный API RPoem (`open_runo.admin.v1.Admin`). Потоковая передача данных добавляется лишь тогда, когда в ней действительно возникает необходимость.
- **Существующие REST-эндпоинты переводятся поэтапно — по мере того, как с ними приходится работать.** После перевода старый REST-маршрут удаляется. Пока миграция не завершена, оставшиеся эндпоинты сохраняются, но **новые не добавляются**.
- **Работа с JSON унифицирована на основе RS-JSON**: чтение — через `from_str_secure` или `parse_secure` (с ограничениями на размер, глубину вложенности и повторяющиеся ключи), запись — через `rust_json::fast`. `prost` в браузерный WASM не включается, поскольку это увеличило бы размер файла.
- **Исключения (интерфейсы, форму которых определяет чужой стандарт, а не наш собственный API)**: ACME, обратные вызовы OAuth/OIDC, вебхуки сторонних сервисов (например, GitHub), проверки работоспособности, раздача статических файлов, OTLP и тому подобное. Такие интерфейсы принимают обычный HTTP, как того требует соответствующий стандарт.
- Эталонные реализации: `RPoem` (`open_runo.admin.v1.Admin`) и `open-easy-web` (`server/src/connect.rs`, `proto/open_easy_web/admin/v1/admin.proto`).
- Примечание: соответствует ли код конкретного репозитория этой политике, зависит от самого репозитория. Данный раздел лишь фиксирует политику и не означает, что код уже изменён.

## API 方針の補足: 用語の整理と使い分け (2026-11-04)

### 日本語
**1つに統一するものではなく、別の層の話です。** 「REST の代わり」になるのは Connect・gRPC・GraphQL だけで、WASM は画面を作る技術です。

| 用語 | 何か | REST の代わりか |
|---|---|---|
| REST | URL と HTTP メソッドで操作を表す API の作り方 | 全廃する側 |
| **Connect** | `POST /サービス名/メソッド名` に JSON を送る形式。`curl` でもブラウザの `fetch` でも呼べる | はい(**採用**) |
| **gRPC** | 同じ「サービス/メソッド」の考え方を、バイナリ(protobuf)と HTTP/2 で行う形式。速く、ストリーミングも得意 | はい(**サービス同士に採用**) |
| gRPC-web | gRPC のブラウザ向けの変形版 | はい(必要なら) |
| GraphQL | 欲しい項目を問い合わせる形式 | 一部だけ(**問い合わせ(読み取り)専用**) |
| WASM | Rust をブラウザの中で動かす仕組み | いいえ(画面を作る技術) |

- **ブラウザの画面や `curl` から呼ぶ API は Connect**(POST、JSON を RS-JSON で読み書き)。ブラウザの WASM は素の gRPC を話せず、Connect なら `fetch` のままで、`prost` を足さずに済む(画面のサイズも増えない)。
- **サービス同士の通信(サーバー間、重い処理、ストリーミング)は gRPC。** 多くは Connect で足りるので、ストリーミングが必要になった所だけ gRPC に上げる。
- **GraphQL は、まとめて問い合わせたいときの読み取り専用。** 書き込み(操作)には使わない。
- **WASM は画面を作る技術として、そのまま使う。** 画面から呼ぶ API が Connect になっただけ。
- 外部の規格が形を決めるもの(ACME、OAuth のコールバック、第三者の Webhook、ヘルスチェック、静的ファイル、OTLP)は、規格どおりの HTTP のまま。
- **迷ったら Connect。**

### English
**These are not alternatives to unify; they sit at different layers.** Only Connect, gRPC and GraphQL can replace REST; WASM is a way to build the UI.

| Term | What it is | Replaces REST? |
|---|---|---|
| REST | API style that expresses operations through URLs and HTTP methods | The thing being abolished |
| **Connect** | `POST /Service/Method` with a JSON body; callable from `curl` and from a browser `fetch` | Yes (**adopted**) |
| **gRPC** | The same service/method idea over binary (protobuf) and HTTP/2; fast, good at streaming | Yes (**for service-to-service**) |
| gRPC-web | A browser-friendly variant of gRPC | Yes (if needed) |
| GraphQL | A query language: ask for exactly the fields you want | Partly (**read-only queries**) |
| WASM | Runs Rust inside the browser | No (a UI technology) |

- **APIs called from browser screens or `curl` use Connect** (POST, JSON read and written with RS-JSON). Browser WASM cannot speak plain gRPC; with Connect it stays a `fetch`, and `prost` is not needed (the binary does not grow).
- **Service-to-service calls (server to server, heavy work, streaming) use gRPC.** Connect is enough in most places; move a call to gRPC only where streaming is actually needed.
- **GraphQL is read-only**, for queries that gather several pieces of data. It is not used for writes (operations).
- **WASM stays as the way to build the UI.** The API it calls simply became Connect.
- Interfaces whose shape an outside standard dictates (ACME, OAuth callbacks, third-party webhooks, health checks, static files, OTLP) stay plain HTTP.
- **When in doubt, use Connect.**

### Deutsch (KI-Übersetzung, sprachlich überarbeitet; noch nicht von Muttersprachlern geprüft)
**Es geht nicht darum, eine einzige Technik auszuwählen – die Begriffe liegen auf unterschiedlichen Ebenen.** Als Ersatz für REST kommen nur Connect, gRPC und GraphQL in Frage; WASM dagegen ist eine Technik, mit der die Benutzeroberfläche gebaut wird.

| Begriff | Was ist das? | Ersatz für REST? |
|---|---|---|
| REST | Ein API-Stil, bei dem Operationen über URLs und HTTP-Methoden ausgedrückt werden | wird abgeschafft |
| **Connect** | `POST /Dienst/Methode` mit JSON im Body; aufrufbar mit `curl` ebenso wie mit `fetch` im Browser | ja (**gewählt**) |
| **gRPC** | Dasselbe Prinzip aus Dienst und Methode, aber über binäres protobuf und HTTP/2; schnell und gut für Streaming geeignet | ja (**zwischen Diensten**) |
| gRPC-web | Eine für den Browser angepasste Variante von gRPC | ja (bei Bedarf) |
| GraphQL | Abfragesprache, mit der man genau die benötigten Felder anfordert | teilweise (**nur für lesende Abfragen**) |
| WASM | Führt Rust-Code direkt im Browser aus | nein (Technik für die Oberfläche) |

- **APIs, die von Browseroberflächen oder per `curl` aufgerufen werden, verwenden Connect** (POST; JSON wird mit RS-JSON gelesen und geschrieben). WASM im Browser kann kein reines gRPC sprechen. Mit Connect bleibt es bei einem gewöhnlichen `fetch`, und `prost` ist nicht nötig – die WASM-Datei wird dadurch nicht größer.
- **Für die Kommunikation zwischen Diensten (Server zu Server, rechenintensive Aufgaben, Streaming) wird gRPC eingesetzt.** In den meisten Fällen reicht Connect aus; auf gRPC wird nur dort umgestellt, wo Streaming tatsächlich gebraucht wird.
- **GraphQL dient ausschließlich lesenden Abfragen**, wenn mehrere Informationen gebündelt abgefragt werden sollen. Für Schreibzugriffe (Operationen) wird es nicht verwendet.
- **WASM bleibt die Technik für die Oberfläche.** Geändert hat sich lediglich, dass die aufgerufene API nun auf Connect beruht.
- Schnittstellen, deren Form durch einen externen Standard festgelegt ist (ACME, OAuth-Callbacks, Webhooks von Drittanbietern, Health-Checks, statische Dateien, OTLP), bleiben gewöhnliches HTTP.
- **Im Zweifel: Connect.**

### Русский (перевод выполнен с помощью ИИ и литературно отредактирован; носителями языка пока не проверен)
**Это не варианты, из которых нужно выбрать один, а технологии разных уровней.** Заменить REST могут только Connect, gRPC и GraphQL; WASM же — это способ создания пользовательского интерфейса.

| Термин | Что это | Заменяет REST? |
|---|---|---|
| REST | Стиль построения API, при котором операции выражаются через URL и HTTP-методы | отменяется |
| **Connect** | `POST /Сервис/Метод` с телом в формате JSON; вызывается как из `curl`, так и из браузерного `fetch` | да (**выбран**) |
| **gRPC** | Тот же принцип «сервис — метод», но поверх двоичного формата protobuf и HTTP/2; работает быстро и хорошо подходит для потоковой передачи | да (**для связи между сервисами**) |
| gRPC-web | Адаптированный для браузера вариант gRPC | да (при необходимости) |
| GraphQL | Язык запросов: клиент запрашивает ровно те поля, которые ему нужны | частично (**только запросы на чтение**) |
| WASM | Позволяет выполнять код на Rust прямо в браузере | нет (технология для интерфейса) |

- **API, которые вызываются из браузерных интерфейсов или через `curl`, строятся на Connect** (POST; JSON читается и записывается через RS-JSON). Браузерный WASM не умеет работать с «чистым» gRPC. С Connect достаточно обычного `fetch`, а `prost` не требуется — размер WASM-файла не увеличивается.
- **Для обмена между сервисами (сервер — сервер, ресурсоёмкие задачи, потоковая передача) применяется gRPC.** В большинстве случаев достаточно Connect; на gRPC переходят только там, где потоковая передача действительно необходима.
- **GraphQL используется только для чтения**, когда нужно получить сразу несколько связанных данных. Для записи (операций) он не применяется.
- **WASM по-прежнему остаётся технологией для интерфейса.** Изменилось лишь то, что вызываемый им API теперь построен на Connect.
- Интерфейсы, форма которых задана внешним стандартом (ACME, обратные вызовы OAuth, вебхуки сторонних сервисов, проверки работоспособности, статические файлы, OTLP), остаются обычным HTTP.
- **Если есть сомнения — выбирайте Connect.**


## REST 全廃の編集記録・実施状況 (2026-11-06)

### 日本語
- **決定(2026-11-04、ユーザー)**: aon-co-jp 全リポジトリで REST API を廃止し、Connect(ブラウザ/`curl`)と gRPC / gRPC-web(サービス間)へ移す。方針の正本は [`API-POLICY.md`](API-POLICY.md)、担当への共通指示は [`API-MIGRATION-BRIEF.md`](API-MIGRATION-BRIEF.md)、残りの一覧は [`API-REST-REMAINING-20261106.md`](API-REST-REMAINING-20261106.md)。
- **実施状況(origin 基準の静的な目安)**: REST風ルート 509(11-04)→481(11-05)→**318(11-06)**。移行済み: open-english・aruaru-search・aruaru-llm・open-web-server・RS-Sync。ほぼ移行: aruaru-db(残8)。作業中: open-cosmo(残22)、RPoem(23、第1段階)。
- **未移行**: RS-EC 28 / RS-Blog 22 / aruaru.tokyo 17 / aruaru-IME 14 / aon.tokyo 13 / backup-to-discord-by-github 11 ほか小規模。**例外か自前かの判定待ち**: open-gitea・open-redmine(Gitea/Redmine互換なら例外)、ows-base・ows-stream(管理APIは自前なら移行)。
- **進め方**: 各リポジトリで 調査 → 分類(移す/例外/ブラウザGET) → 開発 → TEST → 記録(README/CLAUDE/PORTING/POLICY) → 本番反映。同時に動かす担当は最大2つ。例外は理由と規格URLつきで `version-control` の台帳へ。
- **正直な注意**: この節は記録であり、全リポジトリの完了を意味しない。各リポジトリへの同内容の追記は、担当セッションがそのリポジトリを移行する際に行う。本番反映済みと確認できたのは open-english(直接確認)と RS-Sync(担当報告)のみ。

### English
- **Decision (2026-11-04, user)**: abolish REST across all aon-co-jp repositories; move to Connect (browser/`curl`) and gRPC / gRPC-web (service-to-service). Policy source: `API-POLICY.md`; shared instructions: `API-MIGRATION-BRIEF.md`; remaining list: `API-REST-REMAINING-20261106.md`.
- **Status (static estimate, origin-based)**: REST-like routes 509 (11-04) → 481 (11-05) → **318 (11-06)**. Migrated: open-english, aruaru-search, aruaru-llm, open-web-server, RS-Sync. Nearly: aruaru-db (8 left). In progress: open-cosmo (22), RPoem (23, stage 1).
- **Not migrated**: RS-EC 28, RS-Blog 22, aruaru.tokyo 17, aruaru-IME 14, aon.tokyo 13, backup-to-discord-by-github 11, and small ones. **Exception-or-own undecided**: open-gitea, open-redmine, ows-base, ows-stream.
- **Process**: per repository: survey → classify → build → test → record (README/CLAUDE/PORTING/POLICY) → deploy. At most two assignees at a time. Exceptions go to the `version-control` ledger with reason and standard URL.
- **Caveat**: this is a record, not a claim that every repository is done; each repository's own docs are updated by its assignee when it is migrated. Production deployment is confirmed only for open-english and RS-Sync.

## VPSクローン4件の最新化(2026-11-07、version-controlの通知対応) / Refreshed 4 VPS clones

- RUNO(42遅れ)・aon.tokyo(5)・backup-to-discord-by-github(5)・rs-sync(1)を、`git fetch`後に`--ff-only`で最新化(履歴の書き換え無し)。
- bdgの未コミット`Cargo.lock`差分は`/root/bdg-Cargo.lock.local.patch`に退避して最新を採用。bdg・rs-syncはビルド+テスト全通過、aon.tokyoはビルド成功(テスト0件)。
- 稼働中の`aon-tokyo-server`・`rs-sync`・`rs-sync-demo`・`bdg-server`(`/usr/local/bin`へ配置、旧版は`.prev`)を再起動し、active・エラーログ無しを確認。
- 確認: `/video/fukuyama/<ファイル>`は200(ディレクトリ自体はindex無しで404=従来どおり)。`/cancer`・`/links`等は末尾スラッシュ無しで200(ルートは完全一致、`/cancer/`が404なのは従来仕様)。未確認: bdgのWebhook実受信。
- Refreshed by fetch + fast-forward only; services rebuilt/restarted and verified active. Routes are exact-match (`/cancer` is 200, `/cancer/` 404 by design). Unverified: real bdg webhook delivery.

## 2026-11-07 バックアップ再開・紹介ページ追加の到達点 / Backup resumed and intro pages added

**日本語**: (1) `open-github-backup`: 課金は解消、scheduleを再開、検証run成功(ミラー16・飛ばし132・失敗0)。全件runの失敗2件(`rs-dpiAwareness`・`rs-kokoro-ja`)は宛先の作成が一時的に失敗したもので、手動で作成・ミラー済み。宛先165件でActionsが有効だった14件を無効化し、ワークフローに「作成直後に無効化」を追加。
(2) VPSデータの暗号化バックアップ(`vps-data-backup.timer`、毎日03:30)は稼働中・復号確認済み。秘密鍵は`F:\vps-data-backup-gpg-PRIVATE.asc`のみ(別媒体にも保管)。
(3) `easy-web.tokyo`の紹介・ダウンロードページ: `open-media`・`pdf-r2l-rs`・`maid-cafe-se`・`open-cuda`・`open-cpu`・`RPoem`を追加(`webpage/index.html`、配布物はGitHubリリースのURL)。VPSの各クローンは`git pull --ff-only`で更新(VPSだけのコミットは無かった。「分岐」に見えたのは`git pull`の設定のため)。
(4) **未了(判断待ち)**: `easy-web.tokyo/open-raid-z/`は管理UI(画面は誰でも開け、公開の`/api/status`はデモデータ、プール作成だけ`X-Admin-Token`)。VPSの`/root/easy-web.tokyo/open-raid-z`に未コミット変更4件(`webpage/index.html`の削除を含む)があり、触っていない。紹介ページにするか、管理UIを本人限定のメールOTPにするか、`/demo`に分けるかを決める。
**English**: (1) `open-github-backup`: billing resolved, schedule re-enabled, verification run succeeded (16 mirrored, 132 skipped, 0 failed). The 2 failures of the full run (`rs-dpiAwareness`, `rs-kokoro-ja`) were transient creation failures and were fixed by hand. Actions disabled on 14 of the 165 destination repos that had it enabled; the workflow now disables it right after creation.
(2) The encrypted VPS data backup (`vps-data-backup.timer`, daily 03:30) runs and was restore-verified. The private key exists only as `F:\vps-data-backup-gpg-PRIVATE.asc` (keep another copy elsewhere).
(3) `easy-web.tokyo` intro/download pages added for `open-media`, `pdf-r2l-rs`, `maid-cafe-se`, `open-cuda`, `open-cpu` and `RPoem` (`webpage/index.html`; downloads are GitHub release URLs). VPS clones were updated with `git pull --ff-only` (there were no VPS-only commits; the "divergence" came from the `git pull` configuration).
(4) **Open (needs a decision)**: `easy-web.tokyo/open-raid-z/` is an admin UI (anyone can open the screen, the public `/api/status` shows demo data, only pool creation needs `X-Admin-Token`). `/root/easy-web.tokyo/open-raid-z` on the VPS has 4 uncommitted changes (including a deleted `webpage/index.html`) and was left untouched. Decide: intro page, owner-only e-mail OTP for the admin UI, or a `/demo` split.

## 2026-11-08 検証の到達点 / Verification checkpoint

- 日本語: HANDOFF(CLAUDE.md先頭)の2026-11-08項に同じ内容。確認済み=aruaru-searchの自動再開(本番ログ)、version-controlの`--pr`/`--push`(ローカルbare origin・`gh`は偽物)。未確認=本物の`gh pr create`、aruaru-llm要約(VPSは3分超でタイムアウト)。version-control手元クローンは分岐中(`git pull`しない)。
- English: Same as the 2026-11-08 HANDOFF entry. Confirmed: aruaru-search auto-resume (production logs), version-control `--pr`/`--push` (local bare origin, stubbed `gh`). Unconfirmed: real `gh pr create`, aruaru-llm summaries (over 3 min on the VPS). The local version-control clone has diverged; do not `git pull`.

## 2026-11-08 RustSecの依存更新(RS-Blog・RS-EC・karu.tokyo) / RustSec dependency update

- 日本語: 3リポジトリとも Cargo.lock のみ更新してpush済み(h2 0.4.15→0.4.20。RS-Blog・RS-ECはさらに rustls 0.23.46、rustls-webpki 0.103.16、webpki-roots 1.0.11)。karu.tokyoは依存がh2のみ。cargo test成功(RS-Blog 27本・RS-EC 48本・karu 1本)。VPSは各clone(clean)を`git fetch`+`merge --ff-only`で追従し、`cargo build --release`→service再起動。localhostで RS-Blog:8101・RS-EC:8102 の `/healthz` が200、`https://karu.tokyo/` が200。旧バイナリは `*.bak-20261108`(RS-Blog/RS-EC)。注意: RS-EC のVPS cloneは本件以前の数コミット(webpage/index.html追加など)も一緒に進んだ。`karu.tokyo`にはF:のcloneが無く、検証はscratchpadのcloneで実施。**未確認**: 認証つきの画面操作・Connect経路の通し確認、`cargo audit`による警告解消の再走査(version-controlの次回走査で確認)。major更新(rand/sha2/reqwest等)は未着手。**open-gitea**はcloneとoriginが分岐(behind 37/ahead 26)のため触らず、ユーザー確認待ち。
- English: Cargo.lock-only updates pushed for all three (h2 0.4.20; RS-Blog/RS-EC also rustls 0.23.46, rustls-webpki 0.103.16, webpki-roots 1.0.11; karu.tokyo depends only on h2). Tests pass. VPS clones fast-forwarded, rebuilt in release mode and restarted; healthz 200 on RS-Blog/RS-EC and karu.tokyo returns 200. Not verified: authenticated flows and a re-scan clearing the advisories (next version-control run). Majors untouched. open-gitea (diverged 37/26) left alone pending the user's decision.

- **2026-11-08 追記(tokio)**: RS-Blog・RS-EC・karu.tokyo の tokio を 1.54.1 へ更新(RUSTSEC-2026-0386、Cargo.lockのみ)。cargo test成功、`cargo audit`は3つとも警告0、VPSで再ビルド・再起動、healthz(8101/8102)と`https://karu.tokyo/`が200。認証つき操作は引き続き未確認。 / Bumped tokio to 1.54.1 in the three repos; audit clean, redeployed, health checks 200; authenticated flows still unverified.

- **2026-11-08 追記(本番のログイン後確認)**: RS-Blog(`https://runo.tokyo/blog`)・RS-EC(`https://runo.tokyo/ec`)で、管理者のメールOTPでログイン→一覧・作成(下書き)・取得・削除→ログアウト後に401、を本番で実測(依存更新後のバイナリ)。確認用データは削除済み。 / Authenticated production flows (list/create draft/get/delete/logout, 401 afterwards) verified on both services after the dependency updates; test data deleted.

## 2026-11-15 別アカウントでの再開用メモ / Resume notes for another account (2FastAPI, 2FastAPI-VSC, RMojo, Windows ARM64)

### 日本語
**到達点**
- `2FastAPI`(`F:\2FastAPI`、v0.2.0+): Flask/Django→FastAPI(MFastAPI互換)変換。Flask: フック・render_template・request.files・Flask-RESTful/MethodView対応。Django: `View`継承クラス対応。`2fastapi scan/auto/convert`(複数プロジェクト自動検出、変換先を英日で質問、フォルダ自動作成)。差分テスト36件、CIは3OSで成功。
- `2FastAPI-VSC`(`F:\2FastAPI-VSC`、v0.1.0、新規): VS Code拡張。CLIを呼び、スキャン→選択→保存先→作成確認(英日)→変換。テスト6件+実CLI(WSL)通し確認、CI成功、.vsix同梱。VS Code画面の実操作は未確認。
- `RMojo`(`F:\RMojo`、v0.3.0): Windows x64インストーラー・Android実機・Android TVエミュレーターで確認済み。Windows ARM64(Snapdragon)のネイティブビルドとインストーラー(`RMojo-Setup-arm64.exe`)をCIで追加(実機は未確認)。
- **Windows ARM64(Snapdragon)**: 14リポジトリの`release.yml`に非ブロッキングの`build-windows-arm64`(`windows-11-arm`)を追加。CIで成功: RS-Blog/RS-EC/RS-Red/RS-Guard/RS-Ops/RS-Sync/open-cpu/open-cuda/open-cosmo/RPoem/open-gitea。
- 元からのCI不具合を修正: open-gitea・RPoemは兄弟リポジトリ(`../RS-JSON`等)がCIに無く失敗していた→cloneする手順を追加。open-easy-webはYAMLの名前のコロンで読み込めなかった→引用符で修正。

**未了**
1. ARM64ジョブが失敗: open-raid-z・open-easy-web・open-web-server(x64/Linuxも同時に失敗=元からの兄弟依存等の疑い。ログ確認から)。
2. ARM64未対応: Tauri系(open-media/make-disk/open-bar)、インストーラー系(aruaru-IME/open-english/aruaru-llm/maid-cafe-se)、pdf-r2l-rs、MFastAPIのwheel(cibuildwheelにwindows-11-arm追加)。
3. 2FastAPI: Django `TemplateView`/DRF、Flask-SQLAlchemy/marshmallow/JWT等の組み合わせ、PyPI公開。2FastAPI-VSC: Marketplace/Open VSX公開、VS Code画面の実操作確認。
4. RMojo: Snapdragon実機、BSD実機、iOS実行パッケージ、リスト多用時の速度(CPythonの約3.5倍遅い)。
5. WSL(Ubuntu)でのAndroidビルド: Linux版NDKが無くリンクで失敗(Windows側cargoでは成功)。WSLへLinux NDKを入れて検証する。
6. 後片付け: `F:\_vsc_smoke_*`、`F:\rmojo_verify_*`、`F:\ci_sim_*`、`F:\runo\.tmp-*`の削除(ユーザー確認の上)。

**落とし穴**: Git Bashは`/mnt/...`を書き換える→WSLはPowerShellから呼ぶ。bashのheredocで`\b`等のバックスラッシュが壊れる→Writeツールで書く。`wsl.exe`はバックスラッシュを潰す→`F:/`形式で渡す。`rm -rf`は安全チェックで拒否される。

**再開用メッセージ(そのまま貼り付け)**:
> `F:\runo\PORTING.md`末尾「2026-11-15 別アカウントでの再開用メモ」と、`F:\2FastAPI`・`F:\2FastAPI-VSC`・`F:\RMojo`の`PORTING.md`を読んで続きをして。まず未了1(open-raid-z / open-easy-web / open-web-server のCIログを`gh run view --log-failed`で確認して修正)、次に未了2(MFastAPIのwheelにWindows ARM64を追加)、未了3・4の順。確認なしで開発・TEST・DEBUG・commit・pushしてよい。チャットは日本語のみ。

### English
**Where things stand**
- `2FastAPI` (`F:\2FastAPI`, v0.2.0+): Flask/Django → FastAPI (MFastAPI compatible). Flask: hooks, render_template, request.files, Flask-RESTful/MethodView. Django: plain `View` subclasses. `2fastapi scan/auto/convert` detects several projects, asks (English + Japanese) where to put the result and creates folders. 36 differential tests; CI green on 3 OSes.
- `2FastAPI-VSC` (`F:\2FastAPI-VSC`, v0.1.0, new): VS Code extension driving the CLI (scan → choose → destination → create? → convert). 6 tests + a real-CLI run via WSL, CI green, .vsix attached. Real interaction inside VS Code is not verified.
- `RMojo` (`F:\RMojo`, v0.3.0): verified on the Windows x64 installer, a real Android phone and the Android TV emulator. Native Windows ARM64 (Snapdragon) build + installer (`RMojo-Setup-arm64.exe`) added in CI (no real device yet).
- **Windows ARM64 (Snapdragon)**: a non-blocking `build-windows-arm64` job (`windows-11-arm`) was added to 14 repositories' `release.yml`. Green in CI: RS-Blog, RS-EC, RS-Red, RS-Guard, RS-Ops, RS-Sync, open-cpu, open-cuda, open-cosmo, RPoem, open-gitea.
- Pre-existing CI bugs fixed: open-gitea and RPoem failed because sibling repos (`../RS-JSON` etc.) are absent in CI (now cloned); open-easy-web's workflow was unparsable (colon in a name, now quoted).

**Open**
1. ARM64 job red: open-raid-z, open-easy-web, open-web-server (x64/Linux fail too, so probably pre-existing sibling-dependency problems; read `gh run view --log-failed`).
2. No ARM64 yet: Tauri apps (open-media/make-disk/open-bar), installer-based apps (aruaru-IME/open-english/aruaru-llm/maid-cafe-se), pdf-r2l-rs, MFastAPI wheels (add `windows-11-arm` to cibuildwheel).
3. 2FastAPI: Django `TemplateView`/DRF, Flask-SQLAlchemy/marshmallow/JWT combinations, PyPI. 2FastAPI-VSC: Marketplace/Open VSX, real UI check.
4. RMojo: Snapdragon hardware, BSD hardware, iOS runnable package, list-heavy speed (~3.5x slower than CPython).
5. Android build inside WSL (Ubuntu): the Windows NDK has no Linux host tools, so linking fails there (works with Windows cargo). Install a Linux NDK in WSL and verify.
6. Clean-up with the user's OK: `F:\_vsc_smoke_*`, `F:\rmojo_verify_*`, `F:\ci_sim_*`, `F:\runo\.tmp-*`.

**Pitfalls**: Git Bash rewrites `/mnt/...` (call WSL from PowerShell); bash heredocs mangle backslashes such as `\b` (use the Write tool); `wsl.exe` eats backslashes (pass `F:/...`); `rm -rf` is blocked by the safety check.

**Resume message (paste as is)**:
> Read "2026-11-15 別アカウントでの再開用メモ" at the end of `F:\runo\PORTING.md` and the `PORTING.md` of `F:\2FastAPI`, `F:\2FastAPI-VSC` and `F:\RMojo`, then continue: first open item 1 (read the failing CI logs of open-raid-z / open-easy-web / open-web-server with `gh run view --log-failed` and fix), then item 2 (add Windows ARM64 to MFastAPI wheels), then 3 and 4. You may develop, test, debug, commit and push without asking. Chat in Japanese only.

## 2026-11-15 再開用メッセージ(検証の残り・共有基盤調査) / Resume message (verification leftovers, shared-base survey)

### 日本語
**再開するリポジトリ**: `F:\runo`(本リポジトリ、索引と記録)・`F:\version-control`・`F:\aruaru-search`・`F:\aruaru-llm`。別件の再開(2FastAPI・2FastAPI-VSC・RMojo・Windows ARM64のCI)は、直上の「2026-11-15 別アカウントでの再開用メモ」を使う。

**確認済み(2026-11-08〜15)**
- aruaru-search の自動再開(`b15f63a`)は本番ログで実働(探り成功で復帰、braveは429でバックオフ)。
- version-control の `--pr`/`--push` は、ローカルbareのoriginを使ったWSLの往復で成功(`gh`は偽物)。`F:\version-control` の手元クローンは `origin/main` と一致(分岐は解消済み)。
- VPSの稼働状況(読み取りのみ): aruaru-llm(127.0.0.1:4600)・aruaru-search(4610)は**1プロセスずつ**で、サイトごとの同梱・個別起動の形跡は無い。

**未了**
1. 本物の `gh pr create` は未実行(実PRが作られるため、本人の許可を得てから、使い捨てのリポジトリで)。
2. aruaru-llm の変更点要約: VPS(4コアCPU、GPT-2)では同じ形のGenerate(48トークン)が3分超で、`llm_timeout_secs=45` では必ず打ち切られる。高速な推論先(GPU等)を `version-control` の `llm_url` に向けて確認する。**確認用の呼び出しを続けて投げない**(1件でVPSのCPUを数分使い切る)。
3. 配備アーキテクチャ方針(共有基盤を1回だけ入れる)の調査: 同時要求の上限・テナントごとの分離・タイムアウトは未調査。調査結果は `API-REST-REMAINING-20261106.md` 末尾へ。
4. 直上の再開用メモの未了1〜6(open-raid-z/open-easy-web/open-web-server のCI赤など)。

**落とし穴**: 書き換え済みの公開リポジトリで `git pull` しない(`git fetch` + `git reset --mixed origin/<branch>`)。PowerShell 5.1で日本語を含むファイルを書かない(Pythonか Edit/Write)。Git Bashは `/mnt/...` を書き換えるのでWSLはPowerShellから呼ぶ。トークン類は `F:\` 直下のtxtに置き、値を出力・commitしない。チャットは日本語のみ。

**再開用メッセージ(そのまま貼り付け)**:
> `F:\runo\PORTING.md` 末尾の「2026-11-15 再開用メッセージ」と「2026-11-15 別アカウントでの再開用メモ」を読んで続きをして。まず未了4(CIが赤のopen-raid-z / open-easy-web / open-web-server を `gh run view --log-failed` で確認して修正)、次に未了3(共有基盤の同時要求の上限・分離・タイムアウトを `aruaru-llm`・`aruaru-search`・`open-cuda` で調査して記録)、未了2(高速な推論先で `version-control` の変更点要約を確認)の順。未了1(本物の `gh pr create`)は、私の許可があるまでやらない。確認なしで開発・TEST・DEBUG・commit・pushしてよい。チャットは日本語のみ。

### English
**Repositories to resume**: `F:\runo` (this meta repo, index and records), `F:\version-control`, `F:\aruaru-search`, `F:\aruaru-llm`. For the other thread (2FastAPI, 2FastAPI-VSC, RMojo, Windows ARM64 CI) use the section just above, "2026-11-15 別アカウントでの再開用メモ".

**Verified (2026-11-08 to 15)**
- aruaru-search auto-resume (`b15f63a`) works in production logs (probe success -> recovered; brave backs off on 429).
- version-control `--pr`/`--push` succeeded in a WSL round trip against a local bare origin (`gh` was stubbed). The local clone of `F:\version-control` now matches `origin/main` (the divergence is gone).
- VPS state (read-only): aruaru-llm (127.0.0.1:4600) and aruaru-search (4610) run as **one process each**; no sign of per-site bundling or per-site instances.

**Open**
1. A real `gh pr create` has not been run (it creates a real PR: only with the owner's permission, on a throwaway repository).
2. aruaru-llm change summaries: on the VPS (4-core CPU, GPT-2) the same-shaped Generate call (48 tokens) takes over 3 minutes, so `llm_timeout_secs=45` always cuts it off. Point `llm_url` of `version-control` at a fast backend (GPU etc.) and verify. **Do not fire repeated probe calls** (one call saturates the VPS CPU for minutes).
3. Survey for the deployment policy (install the shared base once): concurrency limits, per-tenant isolation and timeouts are not yet surveyed for `aruaru-llm`, `aruaru-search`, `open-cuda`. Record results at the end of `API-REST-REMAINING-20261106.md`.
4. Open items 1-6 of the resume notes just above (red CI of open-raid-z / open-easy-web / open-web-server, etc.).

**Pitfalls**: never `git pull` in a rewritten public repository (`git fetch` + `git reset --mixed origin/<branch>`). Do not write Japanese into files with PowerShell 5.1 (use Python or Edit/Write). Git Bash rewrites `/mnt/...`, so call WSL from PowerShell. Keep tokens in txt files at the root of `F:\`; never print or commit values. Chat in Japanese only.

**Resume message (paste as is)**:
> Read "2026-11-15 再開用メッセージ" and "2026-11-15 別アカウントでの再開用メモ" at the end of `F:\runo\PORTING.md`, then continue: first open item 4 (check the red CI of open-raid-z / open-easy-web / open-web-server with `gh run view --log-failed` and fix), then item 3 (survey concurrency limits, isolation and timeouts of the shared base in `aruaru-llm`, `aruaru-search`, `open-cuda` and record them), then item 2 (verify `version-control` change summaries against a fast inference backend). Do not do item 1 (a real `gh pr create`) until I give permission. You may develop, test, debug, commit and push without asking. Chat in Japanese only.

## 2026-11-15 追記: Android同梱バイナリのConnect化の結果(open-english v0.8.18)/ Addendum: Android bundled binaries (open-english v0.8.18)

### 日本語
**到達点**
- 原因: `open-cuda`がopen-cpuをgit依存、`aruaru-llm`がpath依存で持ち、`Cargo.lock`にopen-cpuが2つ入って同名JNIシンボルが二重リンクされていた。修正は`aruaru-llm/Cargo.toml`の`[patch."https://github.com/aon-co-jp/open-cpu"]`(別セッションが`dae7d25`で先にpush済み。私の重複コミットは破棄)。
- 確認済み: `cargo ndk -t arm64-v8a build --release`が`aruaru-llm`・`open-cpu`・`open-english/server`で成功。バイナリに新しいConnect版の文字列(`aruaru_llm.v1.Llm`・`openenglish.v1.`)を確認。
- `open-english`は版を0.8.18に上げ`v0.8.18`タグをpush。リリースCI成功(APK phone/tablet・Windows/Linux/macOSインストーラー)。
- 実機(`ZY22J7RFND`)で、手元ビルドのdebug APKと**CIが作ったリリースAPK**の両方を起動確認: `libopenenglishserver.so`・`libaruarullm.so`が稼働、`aruaru_llm.v1.Llm/Runtime`と`openenglish.v1.PlatformInfo`が応答、旧REST経路は404、クラッシュ0。

**未了 / 注意**
1. 署名が違うと上書きインストールできない(debug↔リリース)。入れ替えにはアンインストール(アプリ内データは消える)が必要。
2. `open-english`の`server/Cargo.lock`はビルドで大きく変わるため、そのままコミットしない(取り込むなら別途`cargo update`方針を決める)。
3. 実機のUI操作(チャット送信・翻訳など、画面からの通し試験)は未実施。サーバー応答までの確認。
4. 別セッションの国別ニュース話題の件は`aruaru-llm/CLAUDE.md`の「HANDOFF 2026-11-15」を参照。

**再開用メッセージ**:
> `F:\runo\PORTING.md`末尾「2026-11-15 追記: Android同梱バイナリ」を読み、`F:\open-english`(`maid-cafe-english`)のv0.8.18リリースAPKを実機にインストールして、画面からチャット・翻訳を通しで試し、不具合があれば`web/`を直して`mobile/android/app/src/main/assets/webroot`へ同期し、次のタグでリリースして。確認なしで開発・TEST・commit・pushしてよい。チャットは日本語のみ。

### English
**Where things stand**
- Cause: `open-cuda` depends on open-cpu via git while `aruaru-llm` uses a path, so `Cargo.lock` held two open-cpu copies and the same JNI symbols were linked twice. Fix: `[patch."https://github.com/aon-co-jp/open-cpu"]` in `aruaru-llm/Cargo.toml` (another session pushed it first as `dae7d25`; my duplicate commit was dropped).
- Verified: `cargo ndk -t arm64-v8a build --release` succeeds for `aruaru-llm`, `open-cpu` and `open-english/server`; the binaries contain the new Connect strings (`aruaru_llm.v1.Llm`, `openenglish.v1.`).
- `open-english` was bumped to 0.8.18 and tag `v0.8.18` pushed; the release CI succeeded (phone/tablet APKs, Windows/Linux/macOS installers).
- On the real device (`ZY22J7RFND`) both the local debug APK and the **CI-built release APK** start: `libopenenglishserver.so` and `libaruarullm.so` run, `aruaru_llm.v1.Llm/Runtime` and `openenglish.v1.PlatformInfo` answer, the old REST route returns 404, zero crashes.

**Open / cautions**
1. APKs with different signatures cannot be installed over each other (debug vs release); uninstalling is needed (app data is lost).
2. Do not commit `open-english`'s `server/Cargo.lock` as is (the build churns it a lot); decide a `cargo update` policy first.
3. No end-to-end UI test yet (sending chat, translating from the screen); only up to server responses.
4. For the separate session's country-news topic issue see "HANDOFF 2026-11-15" in `aruaru-llm/CLAUDE.md`.

**Resume message**:
> Read "2026-11-15 追記: Android同梱バイナリ" at the end of `F:\runo\PORTING.md`, install the v0.8.18 release APK of `F:\open-english` (`maid-cafe-english`) on the real device, run chat and translation end to end from the screen, fix any bug in `web/` (sync it into `mobile/android/app/src/main/assets/webroot`) and release the next tag. You may develop, test, commit and push without asking. Chat in Japanese only.

## 2026-11-15 別アカウントでの再開用メモ(version-control依存更新・open-raid-z/インストーラーのRust化)
**日本語**: 今回の到達点: (1) version-controlの通知メールの作業を順に実施。e-gov・open-redmine・open-easy-web・aruaru-search・RPoem・realdata.pro・open-barのRustCrypto/rand/reqwest等のメジャー更新をpush済み(各リポジトリのテスト成功)。make-diskは「open-mediaへ引っ越しました」の日英READMEとLICENSEだけにし(`9e516a0`)、version-controlは`make-disk-legacy`を走査対象から外して(`c5d094d`)**VPSのバイナリも差し替え済み**(旧は`version-control.bak-20261114`)。(2) open-raid-z: 依存更新(`0dd19d4`、bincodeは3.0.0がコンパイル不可のため1.3のまま)、fuserのAndroid版を新リポジトリ`fuser-android`へ、インストーラー画面を新リポジトリ`open-raid-z-installer`(Leptos)へ。**旧TypeScript版の削除は通し試験後**。
**再開用メッセージ(そのまま貼り付け)**: 「`F:\open-raid-z-installer`の`CLAUDE.md`の再開用メッセージに従い通し試験(実ウィンドウ・MSI/NSISのインストール/アンインストール)を行って。全て通ったら`F:\open-raid-z`の旧`open_runo_zfs_source/open_runo_installer`を削除してpushし、通った/通らなかった項目を正直に報告して。その後、version-controlの次回通知メールで`make-disk-legacy`が出なくなったことを確認し、残りの更新(open-mediaのlopdf 0.47/sonic-rs 0.5/thiserror 2、whisper.cppのnpm、open-gitea=分岐しているので先にユーザーへ確認、aruaru-llmの脆弱性=`nllb-translate`機能を外すか判断待ち、open-cosmoの`cargo fmt`でCIが赤)を進めて。更新済みcrate(open-redmine・open-easy-web・aruaru-search・realdata.pro)のVPS反映は未実施。」
**English**: Status: (1) The version-control notification e-mails were worked through in order: major updates (RustCrypto/rand/reqwest etc.) for e-gov, open-redmine, open-easy-web, aruaru-search, RPoem, realdata.pro and open-bar are pushed (tests pass in each). make-disk now holds only a bilingual "moved to open-media" README and the LICENSE (`9e516a0`); version-control skips `make-disk-legacy` (`c5d094d`) and **the VPS binary was swapped** (old one: `version-control.bak-20261114`). (2) open-raid-z: dependencies updated (`0dd19d4`; bincode stays at 1.3 because 3.0.0 does not compile), the Android fuser fork moved to the new repo `fuser-android`, the installer UI moved to the new repo `open-raid-z-installer` (Leptos). **Deleting the old TypeScript version waits for the end-to-end tests.**
**Resume message (paste as is)**: "Follow the resume message in `F:\open-raid-z-installer\CLAUDE.md` and run the end-to-end tests (real window, MSI/NSIS install/uninstall). If all pass, delete the old `open_runo_zfs_source/open_runo_installer` in `F:\open-raid-z`, push, and report honestly what passed and what did not. Then confirm that the next version-control e-mail no longer lists `make-disk-legacy`, and continue with the remaining updates: open-media (lopdf 0.47 / sonic-rs 0.5 / thiserror 2), whisper.cpp npm, open-gitea (diverged: ask the user first), aruaru-llm vulnerabilities (decide whether to drop the `nllb-translate` feature), and open-cosmo's red CI from `cargo fmt`. Deploying the updated crates (open-redmine, open-easy-web, aruaru-search, realdata.pro) to the VPS has not been done."

## 2026-11-15 追記: open-bar・version-control・インストーラー試験・RPoemゲートウェイの再開用メモ / Addendum: open-bar, version-control, installer test, RPoem gateway

(同じ日付の他の節〈2FastAPI・RMojo・ARM64／検証の残り・共有基盤／Android同梱バイナリ〉とは別の作業群。それぞれ未了があるので、続きは全部を見ること。/ A separate group of work from the other sections of the same date; each has open items, so read them all.)

### 日本語
**到達点(確認済みのもののみ)**
- **open-bar**: `wasapi` 0.27へ更新してpush(`4f65b95`)。実機テスト`real_files` 11件は**直列実行(`-- --test-threads=1`)で全件成功**。並列だと同じ音声デバイスを取り合って3件が失敗する(0.26でも同じ=0.27のせいではない)。`tests/fixtures`の古い録音のノイズは録音自体のもの(確認音はノイズ無し)。注意書きは`open-bar/CLAUDE.md`末尾。
- **version-control**: `make-disk`の旧`src-tauri`を削除(`make-disk` `9e516a0`)、`make-disk-legacy`を走査対象から除外(`c5d094d`)。VPSのバイナリを`c5d094d`版に差し替え済み(旧は`target/release/version-control.bak-20261114`)、`state.json`に`make-disk-legacy`の記述が0件であることを実確認。`cargo test` 42件成功。
- **RPoemゲートウェイ**: VPSで稼働(127.0.0.1:8140、専用aruaru-db。書き込みの永続化・特殊文字・誤キー401/正キー200を実測、`RPoem/PORTING.md` `e8571b2`)。
- **共有基盤**(`CLAUDE.md`「配備アーキテクチャ方針」): aruaru-llmに同時実行の上限・サイト別の公平な待ち行列・タイムアウトを実装(`6c8f552`)、open-web-serverにサイト別の接続上限・ポート自動割り当て(`c971a38`)。open-cuda・open-directxはライブラリのまま(`e429720`・`1ae10a9`)。
- **aruaru-db・open-cosmo**の自前RESTは0本。Androidは新経路のみ(`/ime/api/aruaru_ime.v1.Ime/Key`)を本番ログで確認。

**未了・注意**
1. **`open-raid-z-installer`の通し試験**: `cargo tauri build`は成功(MSI 3.08 MiB・NSIS 2.04 MiBが`F:\adb-target\oritauri\release\bundle\`)、ビルドしたexeの起動・応答・200% DPIの描画・実データ表示は確認済み。**MSIのインストール/アンインストール試験と複数解像度は未了**(担当が利用上限で停止)。済むまで**旧TypeScript版`open_runo_installer`は削除しない**。
2. **aruaru-IMEのVPS反映は2026-12-06まで保留**(旧経路`/key`・`/session`・`/convert`等の削除を含む`6344880`はmainにあるが未リリース。VPSは0.2.23で旧経路が生きている)。
3. 共有基盤の負荷試験(同時実行・公平性)の**実測値は未確認**(担当の最終報告を読んでいない)。open-barのwasapi以外では、pushしたリポジトリの`cargo test`は流していない(open-web-server・open-easy-web・aruaru-llmは`cargo check --locked`のみ)。
4. 依存更新は打ち切り(aruaru-llmのh2 0.3・protobuf 2・zip 0.6等の脆弱性は残る。mongodb 3.x待ちのidna/rustlsも)。`version-control`の通知で扱う。
5. 判断待ち: `open-cosmo`本体の本番起動(RPoemゲートウェイと役割が重なる)、`open-gitea`の紹介ページの置き場所、`F:\open-easy-web\target-ime\`(607MB)と`F:\runo\.tmp-*`の削除(秘密の混入未確認のためコミットしていない)。
6. open-web-serverの`STATIC_TOKEN_MODE=loopback`切替は、本人がメールOTP+TOTPで2FAログインを通してから。

**落とし穴**: VPSでビルドしない(WSLでビルド→glibc≤2.39確認→scp→旧バイナリ退避→差し替え→そのサービスだけ再起動)。Git Bashでcargoを使うときは`export PATH="/c/Users/noruk/.cargo/bin:$PATH"`。書き換え済みリポジトリで`git pull`しない。複数セッションが同じ`README.md`/`CLAUDE.md`/`PORTING.md`を追記するので、編集前に`git status`と`git pull --rebase`で最新を確認する。

**再開用メッセージ(そのまま貼り付け)**:
> `F:\runo\PORTING.md`末尾「2026-11-15 追記: open-bar・version-control・インストーラー試験・RPoemゲートウェイの再開用メモ」を読んで続きをして。まず未了1(`F:\open-raid-z-installer`の`src-tauri`でMSIのインストール/アンインストール試験と複数解像度の確認。全部通ったら旧TypeScript版`open_runo_installer`を削除してpush)、次に未了3(`F:\aruaru-llm`の共有基盤の負荷試験の実測と`API-REST-REMAINING-20261106.md`への記録)。未了2は2026-12-06まで触らない。確認なしで開発・TEST・DEBUG・commit・pushしてよいが、VPSの本番反映は手順(WSLビルド→カナリア→差し替え→失敗時は自動で戻す)を守る。チャットは日本語のみ。関連リポジトリ: open-bar / version-control / open-raid-z-installer / aruaru-llm / open-web-server / RPoem / aruaru-IME。

### English
**Where things stand (verified items only)**
- **open-bar**: updated to `wasapi` 0.27 and pushed (`4f65b95`). The 11 real-device tests in `real_files` **pass when run serially (`-- --test-threads=1`)**; in parallel 3 tests fight over the same audio device and fail (identical on 0.26, so not caused by 0.27). The noise in the old recordings under `tests/fixtures` is in the recordings themselves (the confirmation tone is clean). The warning is at the end of `open-bar/CLAUDE.md`.
- **version-control**: removed the legacy `src-tauri` from `make-disk` (`9e516a0`) and excluded `make-disk-legacy` from scanning (`c5d094d`). The VPS binary was swapped to `c5d094d` (old one kept as `target/release/version-control.bak-20261114`); `state.json` was checked to have 0 mentions of `make-disk-legacy`. `cargo test`: 42 pass.
- **RPoem gateway**: live on the VPS (127.0.0.1:8140, dedicated aruaru-db; persistence, special characters, wrong key 401 / right key 200 measured; `RPoem/PORTING.md` `e8571b2`).
- **Shared infrastructure** (see "Deployment architecture policy" in `CLAUDE.md`): aruaru-llm now has a concurrency cap, a per-site fair queue and timeouts (`6c8f552`); open-web-server has a per-site connection cap and port auto-assignment (`c971a38`). open-cuda and open-directx stay libraries (`e429720`, `1ae10a9`).
- **aruaru-db and open-cosmo** have 0 own REST routes; the Android app was seen in production logs using only the new route (`/ime/api/aruaru_ime.v1.Ime/Key`).

**Open / cautions**
1. **`open-raid-z-installer` end-to-end test**: `cargo tauri build` succeeded (MSI 3.08 MiB and NSIS 2.04 MiB under `F:\adb-target\oritauri\release\bundle\`); the built exe launches, responds, renders at 200% DPI and shows real data. **MSI install/uninstall and multi-resolution checks are not done** (the assignee hit its usage limit). Until they pass, **do not delete the old TypeScript `open_runo_installer`**.
2. **The aruaru-IME VPS update is held until 2026-12-06** (`6344880`, which removes the old `/key`, `/session`, `/convert` routes, is on main but unreleased; the VPS runs 0.2.23 with the old routes alive).
3. The **measured numbers of the shared-infra load test** (concurrency / fairness) have not been read (the assignee's final report is unread). Apart from open-bar, `cargo test` was not run on the pushed repositories (open-web-server, open-easy-web and aruaru-llm only got `cargo check --locked`).
4. Dependency updates were cut off (aruaru-llm's h2 0.3, protobuf 2, zip 0.6 etc. stay vulnerable, as do idna/rustls waiting on mongodb 3.x); handled through version-control notifications.
5. Waiting for a decision: running open-cosmo itself in production (its role overlaps the RPoem gateway), where to put open-gitea's intro page, and deleting `F:\open-easy-web\target-ime\` (607 MB) and `F:\runo\.tmp-*` (not committed; possible secrets unchecked).
6. Do not switch open-web-server to `STATIC_TOKEN_MODE=loopback` until the owner has completed a real 2FA login (e-mail OTP + TOTP).

**Pitfalls**: never build on the VPS (build in WSL → check glibc ≤ 2.39 → scp → back up the old binary → swap → restart only that service). In Git Bash, prefix `export PATH="/c/Users/noruk/.cargo/bin:$PATH"` before cargo. Never `git pull` in a rewritten repository. Several sessions append to the same `README.md` / `CLAUDE.md` / `PORTING.md`, so run `git status` and `git pull --rebase` before editing.

**Resume message (paste as is)**:
> Read "2026-11-15 追記: open-bar・version-control・インストーラー試験・RPoemゲートウェイの再開用メモ" at the end of `F:\runo\PORTING.md` and continue: first open item 1 (in `F:\open-raid-z-installer`'s `src-tauri`, run the MSI install/uninstall test and multi-resolution checks; once everything passes, delete the old TypeScript `open_runo_installer` and push), then item 3 (measure the shared-infra load test in `F:\aruaru-llm` and record it in `API-REST-REMAINING-20261106.md`). Do not touch item 2 before 2026-12-06. You may develop, test, debug, commit and push without asking, but follow the production procedure on the VPS (WSL build → canary → swap → automatic rollback on failure). Chat in Japanese only. Related repositories: open-bar / version-control / open-raid-z-installer / aruaru-llm / open-web-server / RPoem / aruaru-IME.

## 2026-11-15 再開用メッセージ(open-gitea / open-redmine のConnect化の本番反映) / Resume message (production deploy of open-gitea / open-redmine Connect)

### 日本語
**再開するリポジトリ**: `F:\runo`(本リポジトリ、索引と記録)・`F:\open-gitea-rest`(`aon-co-jp/open-gitea`のローカルclone、`main`=`54058bf`、`Cargo.lock`に未コミット変更あり=触らない)。`open-redmine`のローカルcloneは`F:\`に無く、`https://github.com/aon-co-jp/open-redmine.git`を別cloneする(`6612f6b`+`6c884ac`)。

**到達点(2026-11-08、VPS=`ssh conoha`)**
- **open-redmine**: `6612f6b`を反映済み。WSLでリリースビルド(必要glibc 2.34、VPSは2.39)→ scp → バックアップ(`/root/rd-bak-20261108-065255`)→ 入れ替え(`rs-chiketto`・`web/index.html`・`web/pkg`)→ `open-redmine`(8100)と`open-redmine-demo`(8113)を再起動。確認: `/`=200、旧`/api/projects`=404、Connect `open_redmine.v1.Projects/List`=200・`Create`に空本文=400、画面は白画面でなくログイン表示、コンソールエラー無し。ロールバック無し。記録は`open-redmine/PORTING.md`(`6c884ac`、push済み)。
- **open-gitea**: 別セッションが2026-11-07 20:29に反映済み(バイナリ+`static/`、旧バイナリは`/root/open-gitea-bin.bak.1794050996`)。この反映では二重に入れ替えていない。確認: 旧`/api/repos`=404、Connect `open_gitea.v1.Gitea/ListRepos`=200。
- サービス: `open-gitea.service`(ポート8090、`/root/open-gitea/target/release/open-gitea`、`/root/open-gitea`は`/root/repository/open-gitea`へのリンク、VPSのcloneに未コミットの`Cargo.lock`変更あり=触らない)、`open-redmine.service`(8100)、`open-redmine-demo.service`(8113、同じバイナリ)。前面は`open-web-server`(nginxは停止中・触らない)。

**未了 / 注意**
1. **open-giteaの`/`が404**(`/index.html`は200)。画面は`/ui`配下で配信される仕様(`src/main.rs`の`.nest("/ui", StaticFilesEndpoint…)`)で、それ以外は最後のルート`/*path`(git smart HTTP)に落ちる。公開`https://easy-web.tokyo/open-gitea/`も404。反映前から同じか未確認(旧バイナリは上記バックアップにある)。直すなら「前面から`/ui/`へ転送」か「アプリ側で`/`を`/ui/`へ」を決めてから、コード変更→再反映。`/ui/`が白画面でないかのブラウザ確認も未実施。
2. open-redmine・open-giteaとも、**ログイン後の通し操作は未実施**(認証つきの画面操作)。
3. open-giteaのWSLビルドは、兄弟リポジトリ(RS-JSON・RPoem・open-web-server・RS-SmartTCP・open-raid-z)が`../`に無いと失敗する。`F:\`から`~/dep/`へコピーして揃える。WSLの`~/dep/`にビルド作業ディレクトリが残っている(削除可)。
4. ローカルのsshトンネル(`-L 18100:localhost:8100`)が残っている可能性。VPSには影響しない。

**注意**: VPSでビルドしない(3.6GB)。`git pull`せず、秘密を出さない。Git Bashは`/mnt/...`を書き換える(`MSYS_NO_PATHCONV=1 wsl -d Ubuntu -- bash スクリプト`)。

**再開用メッセージ(そのまま貼り付け)**:
> `F:\runo\PORTING.md`末尾の「2026-11-15 再開用メッセージ(open-gitea / open-redmine のConnect化の本番反映)」を読んで続きをして。まず未了1(open-giteaの`/`が404の件)を、反映前のバイナリ(VPSの`/root/open-gitea-bin.bak.1794050996`)との比較で退行かどうか確かめ、`/ui/`が白画面でないかブラウザで確認し、入口の振り替え方(前面から転送かアプリ側か)を決めて直して再反映(WSLビルド→バックアップ→入れ替え→再起動→確認→失敗時ロールバック)。次に未了2(ログイン後の通し操作)。確認なしで開発・TEST・DEBUG・commit・pushしてよい。VPSの他サービスは再起動しない。チャットは日本語のみ。

### English
**Repositories to resume**: `F:\runo` (this meta repo, index and records) and `F:\open-gitea-rest` (local clone of `aon-co-jp/open-gitea`, `main` = `54058bf`, uncommitted `Cargo.lock` change: leave it). There is no local clone of `open-redmine` under `F:\`; clone `https://github.com/aon-co-jp/open-redmine.git` fresh (`6612f6b` + `6c884ac`).

**Where things stand (2026-11-08, VPS = `ssh conoha`)**
- **open-redmine**: `6612f6b` is deployed. WSL release build (needs glibc 2.34; the VPS has 2.39) -> scp -> backup (`/root/rd-bak-20261108-065255`) -> swap (`rs-chiketto`, `web/index.html`, `web/pkg`) -> restart `open-redmine` (8100) and `open-redmine-demo` (8113). Checks: `/` = 200, old `/api/projects` = 404, Connect `open_redmine.v1.Projects/List` = 200, `Create` with an empty body = 400, the UI shows the login screen (not a white screen), no console errors. No rollback. Recorded in `open-redmine/PORTING.md` (`6c884ac`, pushed).
- **open-gitea**: another session deployed it on 2026-11-07 20:29 (binary + `static/`; old binary at `/root/open-gitea-bin.bak.1794050996`). It was not swapped a second time. Checks: old `/api/repos` = 404, Connect `open_gitea.v1.Gitea/ListRepos` = 200.
- Services: `open-gitea.service` (port 8090, `/root/open-gitea/target/release/open-gitea`; `/root/open-gitea` links to `/root/repository/open-gitea`, whose uncommitted `Cargo.lock` change must be left alone), `open-redmine.service` (8100), `open-redmine-demo.service` (8113, same binary). The front is `open-web-server` (nginx is stopped; leave it).

**Open / cautions**
1. **open-gitea returns 404 for `/`** (`/index.html` is 200). By the current code the UI is served under `/ui` (`.nest("/ui", StaticFilesEndpoint…)` in `src/main.rs`); everything else falls to the last route `/*path` (git smart HTTP). The public `https://easy-web.tokyo/open-gitea/` is also 404. Whether it was the same before the deploy is unverified (the old binary is in the backup above). To fix: decide between forwarding to `/ui/` from the front or redirecting `/` to `/ui/` in the app, then change the code and redeploy. A browser check that `/ui/` is not a white screen has not been done.
2. For both open-redmine and open-gitea, **authenticated end-to-end flows were not exercised**.
3. The open-gitea WSL build fails unless the sibling repos (RS-JSON, RPoem, open-web-server, RS-SmartTCP, open-raid-z) exist next to it; copy them from `F:\` into `~/dep/`. A build working directory is left in WSL `~/dep/` (safe to delete).
4. A local ssh tunnel (`-L 18100:localhost:8100`) may still be running; it does not affect the VPS.

**Pitfalls**: never build on the VPS (3.6 GB), never `git pull`, never print secrets; Git Bash rewrites `/mnt/...` (use `MSYS_NO_PATHCONV=1 wsl -d Ubuntu -- bash script`).

**Resume message (paste as is)**:
> Read "2026-11-15 再開用メッセージ(open-gitea / open-redmine のConnect化の本番反映)" at the end of `F:\runo\PORTING.md` and continue. First open item 1 (open-gitea `/` returns 404): compare with the pre-deploy binary (`/root/open-gitea-bin.bak.1794050996` on the VPS) to see whether it is a regression, check in the browser that `/ui/` is not a white screen, decide how to route the entrance (forward from the front or in the app), fix it and redeploy (WSL build -> backup -> swap -> restart -> verify -> roll back on failure). Then open item 2 (authenticated end-to-end flows). You may develop, test, debug, commit and push without asking. Do not restart other VPS services. Chat in Japanese only.

## 2026-11-15 再開用メッセージ: 共有基盤の受付制御(別アカウントで再開)
**再開するリポジトリ**: `F:\aruaru-llm`(本体)、`F:\runo`(記録)。`F:\open-cuda`・`F:\open-directx`は判断の記録のみ(コード変更なし)。
**済み**: aruaru-llmに受付制御(`src/admission.rs`、`src/connect.rs`)を実装し、2026-11-09にVPSへ反映(同時2・待ち行列全体32/サイト別8・待ち30秒=503・実行120秒=504・満杯=429、Connect形式)。3サイト同時の生成は全て200。単体の公平性測定はA=1400/B=767/C=867ms。open-cuda/open-directxはライブラリのまま(理由は各`CLAUDE.md`)。コミットはorigin/mainに反映済みを確認。
**未了**: (1)前面open-web-serverが`x-tenant`ヘッダを付けているかの確認(付かないと全サイトが`anonymous`扱い=公平配分が効かない)。(2)実推論での公平性の実測(VPS/WSLのGPT-2は遅く、単発でも60秒超。高速な推論先が要る)。(3)上限値(既定2/32/8)の調整。(4)Chat/Classify等の軽い呼び出しは対象外のまま。
**落とし穴**: VPSではビルドしない(WSLでビルド→glibc<=2.39確認→scp→バックアップ→再起動→自動ロールバック)。`ARUARU_LLM_GPT2_DIR=models/gpt2`が無いとモデルを読めない。シェルスクリプトで`wait`を引数なしで使うとバックグラウンドのサーバーまで待つ。
**そのまま貼る再開用メッセージ**:
> `F:\aruaru-llm/CLAUDE.md`の「共有基盤としての受付制御」と`F:\runo/API-REST-REMAINING-20261106.md`末尾(2026-11-09)を読み、未了(1)`x-tenant`ヘッダの前面付与の実機確認から再開して。VPSではビルドせずWSLでビルドして差し替え、REST新設禁止(Connect)、秘密は出さない。

### 2026-11-15 Resume message: shared-base admission control (resuming on another account)
**Repos to resume**: `F:\aruaru-llm` (code), `F:\runo` (records). `F:\open-cuda` and `F:\open-directx` only hold a decision record (no code change).
**Done**: admission control in aruaru-llm (`src/admission.rs`, `src/connect.rs`), deployed to the VPS on 2026-11-09 (2 concurrent, queue 32 total / 8 per site, 30 s wait = 503, 120 s run = 504, full = 429, Connect-style errors). Three simultaneous sites all got 200. Unit-level fairness: A=1400 / B=767 / C=867 ms. open-cuda / open-directx stay libraries (reasons in each `CLAUDE.md`). The commits are confirmed on origin/main.
**Open**: (1) verify the front open-web-server sets `x-tenant` (otherwise every site is `anonymous` and fairness has no effect); (2) measure fairness with real inference (GPT-2 on the VPS/WSL is slow, >60 s even for one call; needs a fast backend); (3) tune the limits (defaults 2/32/8); (4) light calls (Chat/Classify) are still not governed.
**Pitfalls**: never build on the VPS (build in WSL, check glibc <= 2.39, scp, back up, restart, auto-rollback). Without `ARUARU_LLM_GPT2_DIR=models/gpt2` the model fails to load. A bare `wait` in a shell script also waits for a background server.
**Paste-ready resume message**:
> Read "Shared-base admission control" in `F:\aruaru-llm/CLAUDE.md` and the 2026-11-09 section at the end of `F:\runo/API-REST-REMAINING-20261106.md`, then resume at open item (1): verify on the real front server that `x-tenant` is set. Do not build on the VPS (WSL build then swap), no new REST (Connect only), never print secrets.

## 2026-11-15 Android実機確認(REST全廃後)と再開用メッセージ / Android device verification after REST abolition, and resume message

### 日本語
端末は moto g53y(`ZY22J7RFND`、adb は `C:\Users\noruk\AppData\Local\Android\Sdk\platform-tools`)。**端末の設定(IME・回転)は元に戻し済み**(IME は Gboard のまま)。
**確認できたこと**: (1) aruaru-IME v0.2.24(Release の `aruaru-ime-android.apk` 7,022,068 B、sha256 一致)は起動・縦横表示が正常で、端末が新経路 `POST /ime/api/aruaru_ime.v1.Ime/Key` を21回叩いた(VPSのアクセスログ `/var/log/messages`、JST 15:50)。同じ時間帯に旧 `/ime/api/key|session`・`/convert` は0件。APK内の接続先文字列は `/aruaru_ime.v1.Ime/Key|Session` のみ。「konnichiha→今イチは」はエンジンの不具合ではなく、Space が第2候補へ進んだ表示(第1候補は「今日は」)。(2) open-english v0.8.18(`open-english-android-phone.apk` 25,628,873 B)は更新・起動・メイン画面・横向きが正常(ログイン方式は既定の「パスワード無し」で適用)。(3) open-redmine は公式Releaseが無く、`android/` を新規cloneからビルド(3,244,283 B)して起動、「疎通確認」で `/healthz` 200。アプリはWebViewの殻+`/healthz`のみで、ログイン・チケット操作はブラウザ側。(4) open-media v0.1.10(728,345,245 B)は、端末の `jp.co.aon.make_disk`(署名違い)をユーザー承認のうえアンインストールして導入、起動・タブ切替・横向きが正常。
**未了**: open-english のチャット返答の表示、自動更新の新旧リポジトリ照会、open-media の再生・変換・書き込み実操作、open-redmine のブラウザ側ログイン〜チケット操作、文字サイズ変更時の表示、open-easy-web(端末は8月の0.1.0のまま=移行後ビルドではない)。旧経路(aruaru-IME の旧 `/key`・`/session`)の削除期限は2026-12-06。
**落とし穴**: Gboard はローマ字を自分で変換するため、アプリの変換エンジンに届かせるには Gboard を英字モード(「あa1」キー)にする(IME自体の切替は端末設定の変更なので、ユーザー自身が行う)。Play プロテクトの確認画面が出たら「送信しない」で進める。VPSのアクセスログは `/var/log/messages`(`journalctl` には出ない)。
**再開するリポジトリ**: `F:\aruaru-IME`(`aon-co-jp/aruaru-IME`)・`F:\open-redmine`(`aon-co-jp/open-redmine`、`android/`)・`F:\open-english`(`aon-co-jp/maid-cafe-english`)・`F:\open-media`・`F:\runo`(索引)。
**貼り付け用の再開用メッセージ**:
> `F:\runo\PORTING.md` 末尾の「2026-11-15 Android実機確認」を読み、未了(open-english のチャット返答確認、open-media の実操作、open-redmine のブラウザ側、文字サイズ)から再開する。端末は adb(`ZY22J7RFND`)。端末の設定(IME・Play プロテクト)は変更しない。新規RESTは作らない(Connect のみ)。秘密(パスワード・トークン)は画面・コミットに出さない。

### English
Device: moto g53y (`ZY22J7RFND`, adb at `C:\Users\noruk\AppData\Local\Android\Sdk\platform-tools`). **Device settings (IME, rotation) were restored** (the IME is still Gboard).
**Verified**: (1) aruaru-IME v0.2.24 (`aruaru-ime-android.apk`, 7,022,068 B, sha256 matches) starts and renders in portrait and landscape; the device called the new route `POST /ime/api/aruaru_ime.v1.Ime/Key` 21 times (VPS access log `/var/log/messages`, 15:50 JST) with zero hits on the old `/ime/api/key|session` and `/convert` in that window. The only endpoint strings in the APK are `/aruaru_ime.v1.Ime/Key|Session`. "konnichiha -> 今イチは" is not an engine bug: Space advanced to the 2nd candidate (the 1st is 今日は). (2) open-english v0.8.18 (`open-english-android-phone.apk`, 25,628,873 B) updates, starts, shows the main screen and landscape correctly (login mode applied with the default "no login"). (3) open-redmine has no published release; `android/` was built from a fresh clone (3,244,283 B), started, and "connectivity check" returned `/healthz` 200. The app is a WebView shell plus `/healthz` only; login and tickets happen in the browser. (4) open-media v0.1.10 (728,345,245 B) was installed after the user approved uninstalling the device's `jp.co.aon.make_disk` (different signature); it starts, switches tabs and rotates correctly.
**Open**: the chat reply in open-english, the old/new repo query of auto-update, real playback/convert/burn in open-media, the browser-side login and tickets of open-redmine, display at larger font sizes, open-easy-web (the device still has the August 0.1.0, not a post-migration build). The legacy aruaru-IME routes `/key` and `/session` are to be removed on 2026-12-06.
**Pitfalls**: Gboard converts romaji itself, so switch it to alphanumeric mode (the "あa1" key) for input to reach the app's engine (switching the IME itself is a device-setting change the user must do). Choose "Don't send" on the Play Protect dialog. The VPS access log is `/var/log/messages`, not `journalctl`.
**Repositories to resume**: `F:\aruaru-IME`, `F:\open-redmine` (`android/`), `F:\open-english` (`aon-co-jp/maid-cafe-english`), `F:\open-media`, `F:\runo` (index).
**Paste-ready resume message**:
> Read "2026-11-15 Android実機確認" at the end of `F:\runo\PORTING.md` and resume from the open items (open-english chat reply, open-media real operations, open-redmine browser side, font sizes). The device is on adb (`ZY22J7RFND`). Do not change device settings (IME, Play Protect). No new REST (Connect only). Never print secrets (passwords, tokens).

## 2026-11-15 別アカウントでの再開用メモ(aruaru-db / open-cosmo のREST全廃の仕上げ・ブラウザ確認)

**日本語**: aruaru-db と open-cosmo は自前RESTが0本(例外のみ残存)。aruaru-db は公開`/graphql`から管理Mutationを撤去(内部`AruaruSchema`=Connect用、公開`PublicSchema`=管理Mutationなし)し、Connect 32メソッドで同等機能を維持、旧REST残骸約540行を削除。コミット: aruaru-db `777b9d5`・`5ed818a`・`3b4a0f7`・`0faaaf2`、open-cosmo `9d4f1c2`・`31416cb`・`7fa4241`(open-cosmoの例外・理由は`POLICY.md`、`openapi.rs`は`/mcp`が使うため残す)。本番(VPS)は`aruaru-server`と`realdata-aruaru-db`を反映済み(WSLビルド・glibc 2.39以下・バックアップ・入れ替え・自動ロールバック付き)。open-cosmoはVPSで非稼働のため反映対象外。
**確認済み**: 本番の管理画面`https://easy-web.tokyo/aruaru-db/`は白画面でなく描画、`Demo`/`Status`がConnect(`/…Admin/…`)で200、旧REST呼び出し0、`Rebalance`をトークンなしで401(仕様)。Tauri管理画面(`aruaru-db/admin`)はビルド・起動し、WebViewに`localhost:1420`(vite dev)のUIが描画されることを確認(`#root`にUI、`main.tsx`読み込みエラーなし)。
**未了**: (1)`aruaru-admin`アプリ本体(Web管理画面)は`tsc`型検査まで・ブラウザでの操作確認と本番反映は未実施(本番に出ているのは`web/`のデモUI)。(2)Rebalance成功側など本番での書き込み操作は管理トークンを入れる必要があり未実施。(3)aruaru-db `admin.rs`の未使用警告(`engine/registry/backups`フィールド・`replicator`メソッド)。(4)open-cosmoの`docs/*.md`に旧`/api/...`の記述が残る(注記つき)。(5)VPSのaruaru-db cloneは`849f082`のまま(未コミット変更1件・`git pull`しない)。
**落とし穴**: 手元の`F:\runo\repository\*`は履歴が書き換わっているため`git pull`/`merge`しない(新規cloneか`F:\_work\aruaru-db`を使う)。WSLビルドは兄弟`RS-JSON`が同階層に要る(`F:\_work\RS-JSON`)。VPSでビルドしない(RAM 3.6GB)。Tauriの`cargo build`(dev)はdevUrl(1420)を見るので、事前に`npm run dev`でviteを起動する(組み込みなら`npx tauri build --debug --no-bundle`)。管理トークンを画面・ログ・コミットに出さない。
**再開するリポジトリ**: `aon-co-jp/aruaru-db`(作業用`F:\_work\aruaru-db`)、`aon-co-jp/open-cosmo`、`F:\runo`(索引)。
**貼り付け用の再開用メッセージ**:
> `F:\runo\PORTING.md` 末尾「2026-11-15 別アカウントでの再開用メモ(aruaru-db / open-cosmo …)」を読み、未了(aruaru-admin本体のブラウザ確認と反映、`admin.rs`の未使用警告、open-cosmoのdocs整理)から再開してください。リポジトリは aruaru-db(新規clone)と open-cosmo。新規RESTは作らずConnectのみ。`git pull`禁止(履歴書き換え済み)、VPSでビルドしない、秘密(管理トークン等)は出さない。チャットは日本語のみ。

**English**: aruaru-db and open-cosmo now have 0 own REST routes (exceptions only). aruaru-db removed admin mutations from the public `/graphql` (internal `AruaruSchema` serves Connect; public `PublicSchema` has no admin mutations), kept parity through 32 Connect methods, and deleted ~540 lines of dead REST code. Commits: aruaru-db `777b9d5`, `5ed818a`, `3b4a0f7`, `0faaaf2`; open-cosmo `9d4f1c2`, `31416cb`, `7fa4241` (exceptions and reasons in open-cosmo `POLICY.md`; `openapi.rs` is kept because `/mcp` uses it). Production: `aruaru-server` and `realdata-aruaru-db` deployed (WSL build, glibc <= 2.39, backup, swap, auto-rollback). open-cosmo is not running on the VPS, so nothing to deploy.
**Verified**: the production admin UI `https://easy-web.tokyo/aruaru-db/` renders (no white screen), `Demo`/`Status` return 200 over Connect (`/…Admin/…`), no old REST calls, `Rebalance` without a token returns 401 (by design). The Tauri admin (`aruaru-db/admin`) builds, starts, and its WebView renders the UI from `localhost:1420` (vite dev; UI in `#root`, no `main.tsx` load error).
**Open**: (1) the `aruaru-admin` app itself (web admin) was only type-checked with `tsc`; no browser test or deployment (production serves the `web/` demo UI). (2) Production write paths such as a successful `Rebalance` were not exercised (needs the admin token). (3) Unused-code warnings in aruaru-db `admin.rs` (`engine/registry/backups` fields, `replicator` method). (4) open-cosmo `docs/*.md` still contain old `/api/...` text (with notices). (5) The VPS aruaru-db clone is still at `849f082` (1 uncommitted change; do not `git pull`).
**Pitfalls**: local `F:\runo\repository\*` clones have rewritten history, so never `git pull`/merge there (use a fresh clone or `F:\_work\aruaru-db`). WSL builds need the sibling `RS-JSON` (`F:\_work\RS-JSON`). Never build on the VPS (3.6 GB RAM). Tauri dev `cargo build` points at devUrl (1420), so start vite with `npm run dev` first (or embed with `npx tauri build --debug --no-bundle`). Never print the admin token.
**Repositories to resume**: `aon-co-jp/aruaru-db` (working copy `F:\_work\aruaru-db`), `aon-co-jp/open-cosmo`, `F:\runo` (index).
**Paste-ready resume message**:
> Read "2026-11-15 別アカウントでの再開用メモ(aruaru-db / open-cosmo …)" at the end of `F:\runo\PORTING.md` and resume from the open items (browser test and deployment of the aruaru-admin app, the `admin.rs` unused warnings, open-cosmo docs cleanup). Repositories: aruaru-db (fresh clone) and open-cosmo. No new REST (Connect only). No `git pull` (history was rewritten), no builds on the VPS, never print secrets (admin token etc.). Chat in Japanese only.


## 2026-11-15 別アカウントでの再開用メモ(REST全廃の本番確認・反映 / aruaru-db・open-easy-web・aruaru-IME)

### 日本語
**到達点**
- 本番VPS(`ssh conoha`)で、移行済みサービス(aruaru-search/llm・open-web-server・aruaru.tokyo・RS-Sync・RS-EC・RS-Blog・aruaru-db・open-english・open-easy-web)の**新Connectが応答し、旧RESTは404**であることを実測。
- **aruaru-db**: 本番バイナリが古かったため、`849f082`をWSLでなくVPS上でビルドして差し替え(バックアップ`/root/aruaru-server.bak.20261109`)。管理トークン付きで旧`/admin/*`=404、新Connect=200を確認。
- **open-easy-web**: `/ime/api/key`・`/ime/api/session`の旧経路を削除(`6344880`)、VPS再ビルド・再起動(バックアップ`/root/open-easy-web-server.bak-20261109`)。新経路は`/ime/api/aruaru_ime.v1.Ime/Key|Session`。
- **aruaru-IME**: v0.2.25(`bdf237d`)で常駐エンジンの旧経路も削除。VPSエンジン(4660)は旧`/key`・`/session`=404、新=400(ハンドラ到達)。旧経路ヒットは全期間7件で11-09 15:58が最後。2026-12-06の削除作業は不要。
**未了・要確認**
1. (解決済み 2026-11-17) VPSの`downloads/VERSION`は0.2.25でタグと一致。
2. Android実機の通し試験(別セッション`rest-android`担当)、open-easy-webのAndroidアプリは0.1.0のまま。
3. VPS `/root/aruaru-db`の`Cargo.lock`に未コミット差分(`rust-json`2行、ビルド由来)。コミットせず整理。
4. 古いTSF DLL(v0.2.23以前)のクライアントは旧経路が404で変換不可になる。影響の兆候は未確認。
5. open-gitea/open-redmineの紹介ページ置き場所、open-giteaの`/`が404の件(前節参照)。
**落とし穴**: 認証層が先に動くため、未認証の`/admin/*`は存在しないパスでも401(404は管理トークン付きでのみ見える)。VPSの古いcloneを信用しない(originを確認)。トークンはSSH標準入力で渡し画面に出さない。VPS上の`cargo build --locked`はlock不一致で失敗しうる。
**再開用メッセージ(そのまま貼り付け)**:
> `F:\runo`の`PORTING.md`末尾「2026-11-15 別アカウントでの再開用メモ(REST全廃の本番確認・反映)」を読み、再開するリポジトリ`F:\runo`・`F:\aruaru-IME`・`F:\open-easy-web`・`aruaru-db`(新規clone)で未了2(Android実機通し試験)から進めてください(未了1のVPS版揃えは解決済み)。新規RESTは作らずConnectのみ、秘密は出力しない、VPSの古いcloneは信用せずoriginを確認、WSL/VPSの差し替えは必ずバックアップ付きで。

### English
**Reached**
- On the production VPS (`ssh conoha`), migrated services (aruaru-search/llm, open-web-server, aruaru.tokyo, RS-Sync, RS-EC, RS-Blog, aruaru-db, open-english, open-easy-web) answer on the **new Connect routes and return 404 on the old REST**.
- **aruaru-db**: the production binary was stale; `849f082` was built on the VPS and swapped in (backup `/root/aruaru-server.bak.20261109`). With the admin token: old `/admin/*` = 404, new Connect = 200.
- **open-easy-web**: legacy `/ime/api/key` and `/ime/api/session` removed (`6344880`), VPS rebuilt and restarted (backup `/root/open-easy-web-server.bak-20261109`). New path: `/ime/api/aruaru_ime.v1.Ime/Key|Session`.
- **aruaru-IME**: v0.2.25 (`bdf237d`) removed the daemon's legacy routes too. VPS engine (4660): old `/key`, `/session` = 404, new = 400 (reaches the handler). Legacy hits: 7 in total, last on 11-09 15:58. The planned 2026-12-06 removal is unnecessary.
**Open / to verify**
1. (Resolved 2026-11-17) VPS `downloads/VERSION` is 0.2.25, matching the tag.
2. End-to-end Android device test (owned by the `rest-android` session); the open-easy-web Android app is still 0.1.0.
3. Uncommitted `Cargo.lock` diff in VPS `/root/aruaru-db` (2 `rust-json` lines from the build): do not commit, clean up.
4. Old TSF DLL clients (v0.2.23 or earlier) now get 404 and cannot convert; no sign of real impact found.
5. Intro page placement for open-gitea/open-redmine, and open-gitea `/` returning 404 (see the previous section).
**Pitfalls**: the auth layer runs first, so unauthenticated `/admin/*` returns 401 even for nonexistent paths (404 is only visible with the admin token). Do not trust stale VPS clones (check origin). Pass tokens via SSH stdin, never print them. `cargo build --locked` on the VPS can fail on a lock mismatch.
**Paste-ready resume message**:
> Read "2026-11-15 別アカウントでの再開用メモ(REST全廃の本番確認・反映)" at the end of `PORTING.md` in `F:\runo`. Repos to resume: `F:\runo`, `F:\aruaru-IME`, `F:\open-easy-web`, `aruaru-db` (fresh clone). Start with open item 2 (Android E2E; item 1, the VPS version alignment, is resolved). No new REST (Connect only), never print secrets, do not trust stale VPS clones (check origin), always back up before swapping binaries.

## 2026-11-15 再開用メモ: appserver系REST・open-raid-z管理UIのConnect化(別アカウントでの再開用) / Resume note: appserver REST and open-raid-z UI on Connect

### 日本語
**到達点(すべてpush済み、各リポジトリの`origin/main`)**
- **RPoem `6ca9b74` / open-cosmo `6c67196`**: `/admin/appserver-processes*`(6本)・`/admin/appserver-tenants*`(3本)ほか計10本を削除し、`open_runo.admin.v1.Admin` の `AppServerRegisterProcess`/`ListProcesses`/`ProcessStatus`/`StopProcess`/`StopProcessGraceful`/`RestartProcess`/`StopAll`/`UpsertTenant`/`ListTenants`/`RemoveTenant` へ移行(gRPC・gRPC-web・Connect共通、要求・応答は `google.protobuf.Struct`)。実装はルーターの拡張フック `grpc_admin::AdminExt` と、ゲートウェイの `appserver_admin.rs`(`AppServerAdmin`)。試験: router 180件・gateway `appserver_admin` 3件成功(WSL)。
- **open-easy-web `33863ad`**: 呼び出し元(`server/src/appserver_registration.rs`、PoemCosmoTauri登録)を `AppServerUpsertTenant` に変更(試験4件成功)。
- **open-raid-z `bb31771`**: `web/` の `/api/status`・`/api/create` を `POST /open_raid_z.admin.v1.Admin/Status`・`/CreatePool` へ(`/healthz`は例外)。実サーバーで未認証/不正トークン401・旧パス404・`/healthz` 200を確認(Statusは`orzctl`の無い環境で500=想定どおり)。
- **aruaru-db `849f082`(記録のみ)**: `admin_routes()` はルート0本で旧REST無し(「旧REST7本」はVPSの古いクローン由来で対象外)。
**未了・注意**
- **VPS未反映**: RPoemゲートウェイはVPSで稼働中(127.0.0.1:8140)だが、今回のappserver系の変更は未反映(再ビルド・差し替えが必要)。open-raid-zはVPSクローンに未コミット変更4件があり触っていない。open-easy-webのVPS反映も未実施。反映手順=WSLでビルド→glibc確認→scp→バックアップ→入れ替え→再起動→確認(VPSでビルドしない)。
- Connect経由で実プロセスを起動する通しの試験は未実施(レジストリ自体は`open-runo-appserver`の試験で担保)。
- `version-control` の集計から、テストコード内のモックルート(`/api/db/:table/:key`、ACMEモック、`cfg(test)`・`tests/`配下)を除外する件は別セッション(`vc-exclude-tests`)が担当。
- 作業用のcloneは`F:\_work_rest`(兄弟リポジトリへのシンボリックリンクあり)。ビルドは`MSYS_NO_PATHCONV=1 wsl -d Ubuntu -- bash <script>`、`CARGO_TARGET_DIR`はWSLのホーム。`cargo fmt --all`禁止、`git pull`ではなく`git fetch`+rebase。
**再開するリポジトリ**: `RPoem`・`open-cosmo`・`open-raid-z`・`open-easy-web`(必要なら`aruaru-db`)と、索引の`runo`。
**そのまま貼り付ける再開用メッセージ**:
> `F:uno\PORTING.md` 末尾「2026-11-15 再開用メモ: appserver系REST・open-raid-z管理UIのConnect化」を読み、未了(RPoemゲートウェイ・open-easy-webのVPS反映、Connect経由の実プロセス起動試験)から再開してください。対象リポジトリは RPoem・open-cosmo・open-raid-z・open-easy-web(いずれも新規cloneで作業)。VPSでビルドせずWSLでビルドしてscp、反映前にバックアップとロールバック手順を用意。open-raid-zのVPSクローンの未コミット変更は触らない。新規RESTは作らない(Connectのみ)。秘密(トークン・パスワード)は画面・ログ・コミットに出さない。チャットは日本語のみ。

### English
**Where things stand (all pushed to each repo's `origin/main`)**
- **RPoem `6ca9b74` / open-cosmo `6c67196`**: removed the 10 REST routes (`/admin/appserver-processes*` x6, `/admin/appserver-tenants*` x3, and the register route) and moved them to `open_runo.admin.v1.Admin` RPCs `AppServerRegisterProcess`/`ListProcesses`/`ProcessStatus`/`StopProcess`/`StopProcessGraceful`/`RestartProcess`/`StopAll`/`UpsertTenant`/`ListTenants`/`RemoveTenant` (gRPC, gRPC-web and Connect share them; messages are `google.protobuf.Struct`). Implemented via the router extension hook `grpc_admin::AdminExt` and the gateway's `appserver_admin.rs` (`AppServerAdmin`). Tests (WSL): router 180 and gateway `appserver_admin` 3 pass.
- **open-easy-web `33863ad`**: the caller (`server/src/appserver_registration.rs`, PoemCosmoTauri registration) now uses `AppServerUpsertTenant` (4 tests pass).
- **open-raid-z `bb31771`**: `web/` `/api/status` and `/api/create` moved to `POST /open_raid_z.admin.v1.Admin/Status` and `/CreatePool` (`/healthz` stays as an exception). On a real server: unauthenticated/bad token 401, old paths 404, `/healthz` 200 (Status returns 500 without `orzctl`, as expected).
- **aruaru-db `849f082` (docs only)**: `admin_routes()` has zero routes; no old REST remains (the "7 old routes" came from an old VPS clone).
**Open items / cautions**
- **Not deployed to the VPS**: the RPoem gateway runs on the VPS (127.0.0.1:8140) but without this appserver change (rebuild and swap needed). open-raid-z's VPS clone has 4 uncommitted changes that were left alone. open-easy-web is not redeployed. Procedure: build in WSL -> check glibc -> scp -> backup -> swap -> restart -> verify (never build on the VPS).
- A full test that starts a real process through Connect has not been run (the registry itself is covered by `open-runo-appserver` tests).
- Excluding test-only mock routes (`/api/db/:table/:key`, ACME mocks, anything under `cfg(test)`/`tests/`) from the `version-control` count belongs to another session (`vc-exclude-tests`).
- Working clones live in `F:\_work_rest` (with symlinks to sibling repos). Build with `MSYS_NO_PATHCONV=1 wsl -d Ubuntu -- bash <script>`; `CARGO_TARGET_DIR` in the WSL home. No `cargo fmt --all`; use `git fetch` + rebase, not `git pull`.
**Repositories to resume**: `RPoem`, `open-cosmo`, `open-raid-z`, `open-easy-web` (and `aruaru-db` if needed), plus the index repo `runo`.
**Paste-ready resume message**:
> Read "2026-11-15 再開用メモ: appserver系REST・open-raid-z管理UIのConnect化" at the end of `F:uno\PORTING.md` and resume from the open items (deploy the RPoem gateway and open-easy-web to the VPS; a real process-start test over Connect). Repos: RPoem, open-cosmo, open-raid-z, open-easy-web (work in fresh clones). Never build on the VPS: build in WSL and scp, with a backup and rollback plan first. Do not touch the uncommitted changes in open-raid-z's VPS clone. No new REST (Connect only). Never print secrets (tokens, passwords). Chat in Japanese only.

## 2026-11-15 別アカウントでの再開用メモ(REST全廃の仕上げ: ストリーミング・bdg・open-cg-cad・e-gov) / Resume memo for another account (REST abolition finish: streaming, bdg, open-cg-cad, e-gov)

### 日本語
**到達点(すべてpush済み、本番(VPS)は未反映)**:
- **ストリーミング(RPoem、`1570371`・`34cb595`)**: server-streaming は `open-runo-connect-{core,server,client}`(旧称 gRPC-web-Connect。`F:\gRPC-web-Connect` は手元にもGitHubにも無い)に既にあり、不足分を追加。`Reply::TryStream`(途中の`Err`を各方式の終端フレームで返す)、`StreamLimits`(既定100万件/1時間、`handle_with`で変更)、切断で資源解放、実TCPの`connect+json` `WatchEvents`試験。実gatewayへ`curl -N`で確認(認証なし=終端エラー、鍵あり=ストリーム、ストリーム専用メソッドを単項で呼ぶと400)。`grpcurl`は未使用(素のgRPCは実HTTP/2試験で確認)。VPSはRPoem gateway稼働の有無・再ビルド要否の確認から。文書は`RPoem/docs/connect-hybrid.md`末尾。`API-POLICY.md`のストリーミング節は別セッションが日英で追記済み(独語・露語は未追記)。
- **backup-to-discord-by-github(`9066b60`)**: 旧`/api/*` 6本を `POST /bdg.admin.v1.Admin/{ListJobs,GetJob,ListTargets,ListBackups,StartBackup,StartPrune}` へ(RS-JSON上限つき、重複キー400、エラーは`{code,message}`、旧REST文書も廃止)。`/healthz`とGitHub Webhookは例外。統合テスト5件成功。その後の本番反映は別セッションの記録を確認すること。
- **open-cg-cad(`68aa70e`)**: 旧`/v1/*` 12本を `POST /open_cg_cad.v1.Cad/<Method>`(Generate・GenerateDxf・UploadDrawing・ListDrawings・GetDrawing・AnalyzeDrawing・RedesignDrawing・MergeDrawings・GithubRead・GithubCommit・VpsRead・VpsWrite)へ。GETだった図面取得・VPS読み込みは本文`{id}`・`{path}`に。画面`index.html`も更新、`api_docs.rs`(REST文書)は削除。`curl`で旧経路404・重複キー400・未存在404を確認。**未確認**: `Generate`の正常系200(建物種別は小文字`house`等)、ブラウザ操作、VPS反映、画面の共有ログイン表示が呼ぶ open-english の `GET v1/auth/session` がConnect化後も通るか。
- **e-gov(`6301a9b`)**: 掲示板の`POST /board/post`(フォーム→303)を `POST /e_gov.v1.Board/AddPost`(JSON、16KiB上限)へ。ページのフォームは`fetch`化(JS無効では投稿不可)。`curl`で正常200/不明カテゴリ・重複キー・20KB超400/旧経路404、ページ出力を確認。**未確認**: ブラウザ目視、VPS反映。`/webhook/line`・`/healthz`は例外。
- **自前APIが0本(すべて例外、記録のみ)**: aon.tokyo(`d760c3d`)・karu-tokyo(`7b2e348`)・audiocafe-tokyo-rust(`7a7f7c6`)・runo.tokyo(`8631850`)。
- **方針の遵守チェック**: 手元チェックアウトの粗い一覧(REST風ルート数と`serde_json`だけで読む箇所)を作った(作業用メモ、リポジトリ外)。正確な数は`version-control`の巡回結果を使う。RS-JSON未使用の候補: RS-Guard・open-fudousan・open-mqa-dsd・pdf-r2l系・rs-kokoro-ja・rsa-rs・runo-scanner(未対応、コード変更なし)。

**未了**: (1)上記の本番反映と通し確認(bdg・open-cg-cad・e-gov・RPoemストリーミング)。(2)GitHubに`atr-sonic`・`open-easy-web-app`が見つからない(非公開か別名か要確認)。(3)open-cg-cad の open-english 認証セッション呼び出しの修正要否。(4)`API-POLICY.md`の独語・露語(ストリーミング節)。(5)ほかの担当(open-cosmo・aruaru-db・RPoem・gitea/redmine)の状況は別の再開メモを参照。
**落とし穴**: 各リポジトリの更新は`git fetch`+`git merge --ff-only`で追従し、`git pull`しない(履歴を書き換えたリポジトリがある)。e-gov・karu-tokyo・audiocafe-tokyo-rust の作業用cloneは一時フォルダ(消えている)なので新規cloneする。Windowsでcargoは`%USERPROFILE%\.cargo\bin`をPATHへ。RS-JSONは兄弟パス`../RS-JSON`(open-cg-cad・bdgはpath依存)。PowerShell 5.1で日本語を書かない(PythonかEdit)。秘密は画面・コミットに出さない。

**そのまま貼り付ける再開用メッセージ**:
> `F:\runo\PORTING.md` 末尾の「2026-11-15 別アカウントでの再開用メモ(REST全廃の仕上げ: ストリーミング・bdg・open-cg-cad・e-gov)」を読み、未了から再開してください。リポジトリ: `RPoem`(ストリーミング、VPS反映の要否)・`backup-to-discord-by-github`・`open-cg-cad`(`Generate`正常系・ブラウザ・open-english認証呼び出し)・`e-gov`(新規clone、ブラウザ確認)・`runo`(本リポジトリ、索引のみ)。新しいRESTは作らない(Connectのみ)、`git pull`しない(`git fetch`+`--ff-only`)、VPSでビルドしない(WSLでビルド→scp→バックアップ→入れ替え→確認)、秘密を出さない、チャットは日本語のみ。

### English
**Where things stand (all pushed; production VPS not updated)**:
- **Streaming (RPoem, `1570371`, `34cb595`)**: server-streaming already existed in `open-runo-connect-{core,server,client}` (formerly "gRPC-web-Connect"; `F:\gRPC-web-Connect` exists neither locally nor on GitHub). Added `Reply::TryStream` (a mid-stream `Err` ends every protocol with its terminal frame), `StreamLimits` (default 1M messages / 1 h, change via `handle_with`), resource release on disconnect, and a real-TCP `connect+json` `WatchEvents` test. Checked against a running gateway with `curl -N` (no auth = terminal error frame, key = stream, calling a streaming method as unary = 400). `grpcurl` was not used (plain gRPC is covered by the real HTTP/2 test). For the VPS, first check whether the RPoem gateway runs there and whether a rebuild is needed. Docs: end of `RPoem/docs/connect-hybrid.md`. The streaming section of `API-POLICY.md` was added (JA/EN) by another session; German/Russian are missing.
- **backup-to-discord-by-github (`9066b60`)**: the 6 old `/api/*` routes became `POST /bdg.admin.v1.Admin/{ListJobs,GetJob,ListTargets,ListBackups,StartBackup,StartPrune}` (RS-JSON limits, duplicate keys rejected, errors as `{code,message}`, REST docs removed). `/healthz` and the GitHub webhook are exceptions. 5 integration tests pass. Check other sessions' notes for the later production deploy.
- **open-cg-cad (`68aa70e`)**: the 12 old `/v1/*` routes became `POST /open_cg_cad.v1.Cad/<Method>` (Generate, GenerateDxf, UploadDrawing, ListDrawings, GetDrawing, AnalyzeDrawing, RedesignDrawing, MergeDrawings, GithubRead, GithubCommit, VpsRead, VpsWrite). The former GETs now take `{id}` / `{path}` in the body; `index.html` updated; `api_docs.rs` (REST docs) removed. Checked with `curl`: old routes 404, duplicate key 400, missing id 404. **Not verified**: the `Generate` success path (200; building types are lowercase such as `house`), browser use, VPS deploy, and whether the page's shared-login call to open-english `GET v1/auth/session` still works after open-english moved to Connect.
- **e-gov (`6301a9b`)**: the board's `POST /board/post` (form → 303) became `POST /e_gov.v1.Board/AddPost` (JSON, 16 KiB cap); the form now uses `fetch` (posting needs JS). Checked with `curl` (success 200; unknown category, duplicate key, >20 KB = 400; old route 404; page output). **Not verified**: visual check in a browser, VPS deploy. `/webhook/line` and `/healthz` are exceptions.
- **No own API (all exceptions; docs only)**: aon.tokyo (`d760c3d`), karu-tokyo (`7b2e348`), audiocafe-tokyo-rust (`7a7f7c6`), runo.tokyo (`8631850`).
- **Compliance scan**: a rough list from local checkouts (REST-like routes, `serde_json`-only readers) was made (a working note outside the repository). Use the `version-control` scan for exact numbers. Candidates without RS-JSON: RS-Guard, open-fudousan, open-mqa-dsd, pdf-r2l family, rs-kokoro-ja, rsa-rs, runo-scanner (not changed).

**Open**: (1) deploy and end-to-end checks of the above (bdg, open-cg-cad, e-gov, RPoem streaming). (2) `atr-sonic` and `open-easy-web-app` were not found on GitHub (private or renamed?). (3) whether open-cg-cad's call to open-english's session endpoint needs fixing. (4) German/Russian text for the streaming section of `API-POLICY.md`. (5) For open-cosmo, aruaru-db, RPoem and gitea/redmine see the other resume memos.
**Pitfalls**: update repos with `git fetch` + `git merge --ff-only`, never `git pull` (some histories were rewritten). The scratch clones of e-gov, karu-tokyo and audiocafe-tokyo-rust were temporary and are gone; clone fresh. On Windows put `%USERPROFILE%\.cargo\bin` on PATH. RS-JSON is a sibling path dependency (`../RS-JSON`) for open-cg-cad and bdg. Do not write Japanese with PowerShell 5.1 (use Python or Edit). Never print secrets.

**Paste-ready resume message**:
> Read "2026-11-15 別アカウントでの再開用メモ(REST全廃の仕上げ: ストリーミング・bdg・open-cg-cad・e-gov)" at the end of `F:\runo\PORTING.md` and resume from the open items. Repositories: `RPoem` (streaming; is a VPS update needed?), `backup-to-discord-by-github`, `open-cg-cad` (`Generate` success path, browser, the open-english session call), `e-gov` (fresh clone, browser check) and `runo` (this index repo). Build no new REST (Connect only), never `git pull` (use `git fetch` + `--ff-only`), never build on the VPS (WSL build -> scp -> backup -> swap -> verify), never print secrets, chat in Japanese only.

## 2026-11-17 追記: 2FastAPI / RMojo / MFastAPI の到達点
2FastAPI v0.3.3(Flask `session`/`g`変換)、RMojo v0.4.1、MFastAPI v0.2.3(win_arm64済み)。直上「2026-11-15 別アカウントでの再開用メモ」の2FastAPI・RMojo・MFastAPI関連の記述は、この節が新しい。残り: PyPI/Marketplace(所有者の認証)、実機Snapdragon、open-raid-z等のCI。 / Latest: 2FastAPI v0.3.3, RMojo v0.4.1, MFastAPI v0.2.3 (win_arm64 done); this supersedes the older note above. Open: PyPI/Marketplace (owner credentials), real Snapdragon, CI of open-raid-z etc.

## 2026-11-17 Snapdragonの研究: 「PCにつないだスマホ」と「PC用CPUのモバイル版」/ Snapdragon research (phone attached to a PC, and the PC-class CPU)

**日本語**
- **前提**: Snapdragon搭載のWindows PCは無く、Snapdragonスマホ(QTI SM7435、Android 16、Cortex-A78×4+A55×4、armv8.2、NEON・dotprod・fp16あり、i8mm/SVE無し)だけがある。
- **観点1: PCにつないだスマホとして**(adb/USB)。Windows ARM64の代用ではなく、**同じARM64命令(aarch64)の実機試験台**として使う。`aarch64-linux-android`向けにビルドした実行ファイルを`adb push`して端末で直接走らせる。確認済み: `open-cpu`の単体試験34件がスマホ上で全件成功(NEON版の`dot`/`axpy`/`scale`/`popcount`ほか)。手順=`cargo test --release --target aarch64-linux-android --no-run`(`CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER`にNDKの`aarch64-linux-android30-clang.cmd`)→`adb push`→`adb shell`。AndroidアプリはUSBデバッグでの通し試験(従来どおり)。
- **観点2: PC用CPU(Snapdragon X、Oryon)のモバイル版として**。Qualcommは第1世代XをARMv8.7-A準拠、SIMDはNEONのみ(SVE無し)と説明、第3世代でSVE/SVE2が加わるとの報道([Chips and Cheese](https://chipsandcheese.com/p/qualcomms-oryon-core-a-long-time-in-the-making)、[Qualcomm](https://www.qualcomm.com/developer/windows-on-snapdragon))。x86/x64アプリはPrismエミュレーションで動くが、AVX多用・GPU負荷の高い処理は不利で、カーネルドライバは動かない。
- **スマホで確かめられること**: NEON実装の正しさ、Cortex系コアでの速度の傾向。**確かめられないこと**: Oryonコア固有の速度、Windows固有の挙動(インストーラー、DLL、署名、ドライバ)、Windows ARM64のPrism下のx64動作。これらはCI(`windows-11-arm`ランナー)の合否だけが根拠で、実機の通し試験は未了。
- **注意**: スマホとPCのCPUは同じARMでも命令セットの対応が違う(スマホはdotprodあり・i8mm無し。PC側の対応は`open-cpu inventory`で実機確認するまで断定しない)。USBテザリングはWindows ARM64で制限の報告があり、Snapdragonスマホ+ARM64 WindowsでPhone Link/adbが動く確証は見つからなかった(未検証)。
- **CIの追加(2026-11-17)**: `aruaru-IME`(matrixのwindows-arm64)・`pdf-r2l-rs`・`aruaru-llm`に、必須にしないWindows ARM64ジョブを追加。open-media/make-disk/open-bar/open-raid-z/open-easy-web/open-web-serverは前回までに追加済み。

**English**
- **Premise**: no Snapdragon Windows PC; only a Snapdragon phone (QTI SM7435, Android 16, 4x Cortex-A78 + 4x A55, armv8.2 with NEON/dotprod/fp16, no i8mm/SVE).
- **View 1 - the phone attached to a PC (adb/USB)**: not a Windows ARM64 substitute but a **real aarch64 test bench**. Build for `aarch64-linux-android`, `adb push`, run on the device. Verified: all 34 `open-cpu` unit tests pass on the phone (NEON dot/axpy/scale/popcount etc.). Recipe: `cargo test --release --target aarch64-linux-android --no-run` with the NDK `aarch64-linux-android30-clang.cmd` as linker, then `adb push` and `adb shell`.
- **View 2 - the PC-class CPU (Snapdragon X / Oryon) as the "big sibling"**: first-gen X is ARMv8.7-A with NEON only (no SVE); SVE/SVE2 are reported for the third generation. x86/x64 apps run under Prism emulation, with AVX-heavy/GPU-heavy work penalised and no x64 kernel drivers.
- **What the phone can show**: correctness of NEON code, rough behaviour on Cortex cores. **What it cannot**: Oryon-specific speed, Windows-specific behaviour (installers, DLLs, signing, drivers, Prism). Those rest on the `windows-11-arm` CI result only; no real-hardware run yet.
- **Caveat**: the phone and the PC share ARM but not the same optional features (phone: dotprod yes, i8mm no); the PC's set stays unconfirmed until `open-cpu inventory` runs on one. No evidence was found that Phone Link/adb/USB tethering work between a Snapdragon phone and a Windows ARM64 PC (unverified).
- **CI added (2026-11-17)**: non-blocking Windows ARM64 jobs for `aruaru-IME`, `pdf-r2l-rs`, `aruaru-llm`.

## open-cpu の同梱と、アクセラレーターの扱い(2026-11-17)
- **同梱済み(実行時に AVX-512BW > AVX2 > NEON > スカラーを自動選択、`OPEN_CPU_MAX_ISA`で上限指定可)**: MFastAPI(`--cpu`、長いクエリ文字列の探索)、RMojo(`rmojo cpu`、`str.find`/`str.count`)、open-web-server・open-easy-web(起動時の要約、`System/GetCpu`、FastCGIヘッダー走査)。実機はNEONをSnapdragon端末2台で、AVX-512BWはCIで確認(開発PCはAVX2まで)。
- **2FastAPI**: 変換ツール(Python)で、実行時の計算処理を持たないため open-cpu は使わない。
- **open-cuda / aruaru-llm / open-directx は同梱しない**: 共有基盤を1回だけVPSに入れ、各サイトはConnect/gRPCで呼ぶ方針(本ファイル冒頭の配備アーキテクチャ方針)に従う。
- **ブラウザ(Windows/Linux/Mac/Android/iPhone)**: 計算はサーバー側で行うため、どの端末のブラウザからでも利用できる。RMojoのWASM(`wasm32-unknown-unknown`の`cargo check`は通過)は将来の遊び場候補。WASMでは open-cpu のSIMD自動選択は使わない。
- **スマホのアクセラレーター化**: `open-cpu/remote`(`open-cpu-remote`)。実測では手元PCが速いため自動判断は「手元のみ」で、手元が非力な場合に効く。詳細は`open-cpu/remote/README.md`。

## 起動時の自動バージョンアップ(2026-11-17)/ Self-update at startup
**日本語**: 起動のたびに前回の確認から24時間以上たっていれば、切り離した子プロセスで GitHub の最新リリースを調べ、新しければ取得して入れ替える(起動は遅くならない。更新は次回の起動から有効で、その旨を一度だけ表示)。**リリースの `<ファイル名>.sha256` と一致したときだけ**入れ替え、`.sha256` が無いリリース・GitHub 以外の取得先・先行版(-alpha 等)へは更新しない。信頼の根拠は GitHub への TLS と SHA-256(電子署名ではない)。手動実行と停止は下表。失敗は黙って次回に回し、理由は状態ディレクトリの `last_error` に残る。
**English**: On each start, if 24 h have passed since the last check, a detached child process queries the latest GitHub release and, if newer, downloads and swaps it in (startup is not delayed; the update takes effect on the next start, announced once). It installs **only if the SHA-256 matches the release's `<file>.sha256`**; releases without `.sha256`, non-GitHub hosts and pre-releases are refused. Trust = TLS to GitHub + SHA-256 (not a signature). Failures are silent and recorded in `last_error` in the state directory.
- MFastAPI: Python パッケージは `accelerate()` 呼び出し時に起動し、`pip download --no-index`(PyPI は見ない)で環境に合うホイールを取得→SHA-256 検証→`pip install --no-deps`。`mfastapi-server` バイナリは単体で自己入れ替え(Windows は実行中 exe を `.old` へ退避)。手動: `python -m mfastapi._autoupdate --now` / `mfastapi-server update`、停止: `MFASTAPI_NO_UPDATE=1`。状態: `~/.mfastapi/`。
- RMojo: Linux/macOS/Android は `tar.gz` の `rmojo` を同じ場所へ rename で入れ替え(実行中でも安全)、Windows は公式 `RMojo-Setup-<arch>.exe` を静かに実行(利用者権限)。手動: `rmojo update`、停止: `RMOJO_NO_UPDATE=1`(`CI` 設定時も停止)。状態: `~/.rmojo/`。Windows 実機で v0.4.3 のダウンロード→SHA-256 検証→Setup 静か実行→アンインストールまで確認済み(2026-11-17)。
- 2FastAPI: pip 版は `2fastapi`/`2fastapi-gui` 起動時に、`pip download --no-index`→SHA-256 検証→`pip install --no-deps`(別の仮想環境で 0.5.0→0.5.1 を実リリースで確認済み)。インストーラー版(Windows)は新しい `2FastAPI-Setup-<arch>.exe` を取得・検証して置き、次回起動時に静かに実行。手動: `python -m tofastapi._autoupdate --now`、停止: `TOFASTAPI_NO_UPDATE=1`。状態: `~/.2fastapi/`。

## 上流の新版への追従(2026-11-17)/ Following upstream releases
- **定期試験**: CI を毎日(UTC 03:23)実行し、最新の Python・Flask・Django・FastAPI・Starlette(RMojo は最新の CPython との差分試験)で再試験。失敗したら日付つきの issue を1件起こす。
- **easy-web.tokyo**: `runo/scripts/refresh_versions.py` を VPS のタイマー(`easy-web-intros-refresh.timer`、1時間ごと)で実行し、MFastAPI・RMojo・2FastAPI・2FastAPI-VSC の最新版と上流(Python・Flask・Django・FastAPI・Starlette・Rust・Mojo)の最新版を各紹介ページと `/demo` に表示(`<製品>/versions.json`)。ページはダウンロード専用のまま。
- **未了**: 上流の新版が出たときに、利用者の環境(Flask/Django 等)まで自動で上げる機能は無い(本製品が更新するのは本製品自身)。aruaru-llm の同梱は未着手(open-cpu は同梱済み)。iPhone・iPad には対応していない。


## 2026-11-15 再開用メモ: RS-Sync依存更新・テスト/検証が上手くいかない理由の調査 / Resume notes: RS-Sync dependency update and why tests/verification go wrong

### 日本語

**完了**(RS-Sync、push済み): 依存を最新の主要版へ更新(`3b144cd`: rand 0.10 / sha2 0.11 / hmac 0.13 / sha1 0.11 / thiserror 2 / reqwest 0.13 / russh 0.65 / russh-sftp 3 / smb2 0.43)、open-giteaテストの期待値をConnectへ追従し記録を追記(`177d68c`)。全テスト通過、`cargo ndk`でarm64-v8a/x86_64のreleaseビルド成功。

**調査(日英のWeb検索+GitHub)で分かった「テスト・検証が上手くいかない理由」**:
1. プロセス共通の状態(カレントディレクトリ・環境変数)を並列テストで触ると競合する。対策=ロックで直列化、子プロセスの`current_dir`、`--test-threads=1`。reqwestも同じ理由の不安定さを環境変数テストの直列化で直している(seanmonstar/reqwest#2529)。`git`を起動するテストが削除済みカレントを引き継いで`getcwd failed`になる事例もある(theodoreOnzGit/outram-park-backend#1308)。
2. Windowsではウイルス対策/indexerが一時ファイルのハンドルを掴み、削除やgit操作が時々失敗する(microsoft/windows-drivers-rs#607、Python-Devの議論)。対策=リトライ、テストごとの専用ディレクトリ、`handle.exe`で原因プロセスの確認。
3. モックはAPI形式の変更で静かに古くなる(今回のopen-giteaのConnect化がそれ)。AIはモックを増やしがちで、コードとテストを同じAIが書くと誤解がテストに固定される。実際に実行していない/実機と違う経路の「通った」報告にも注意(arXiv 2602.00409)。対策=実サーバー呼び出しでの確認、記録と再生、独立した検証。

**未了**: RS-Syncの稀に落ちる結合テスト(`two_way_sync_propagates_dest_only_change_back_to_source`)の原因特定、Android実機の起動確認。詳細と再開用メッセージは`F:\RS-Sync`の`PORTING.md`末尾「再開用メモ(2026-11-15)」。

**再開するリポジトリ**: `F:\RS-Sync`(aon-co-jp/RS-Sync、main)、メモの置き場の`F:\runo`。

**そのまま貼り付ける再開用メッセージ**:
> `F:\runo`の`PORTING.md`末尾「2026-11-15 再開用メモ: RS-Sync依存更新・…」と、`F:\RS-Sync`の`PORTING.md`末尾「再開用メモ(2026-11-15)」を読み、RS-Syncの不安定な結合テストの原因特定と修正、Android実機の起動確認の順に進めてください。長いテストは`run_in_background`で。完了したら両リポジトリの文書を日英で更新してpushしてください。

### English

**Done** (RS-Sync, pushed): dependencies updated to the latest majors (`3b144cd`: rand 0.10 / sha2 0.11 / hmac 0.13 / sha1 0.11 / thiserror 2 / reqwest 0.13 / russh 0.65 / russh-sftp 3 / smb2 0.43); the open-gitea test expectation was aligned with Connect and the notes were added (`177d68c`). All tests pass and `cargo ndk` release builds succeed for arm64-v8a and x86_64.

**Why tests/verification go wrong (English/Japanese web search + GitHub)**:
1. Parallel tests that touch process-wide state (cwd, environment variables) race. Fixes: serialise with a lock, pass `current_dir` to child processes, or use `--test-threads=1`. reqwest fixed the same kind of flakiness by serialising env-var tests (seanmonstar/reqwest#2529); a git-spawning test inheriting a deleted cwd fails with `getcwd failed` (theodoreOnzGit/outram-park-backend#1308).
2. On Windows, antivirus/indexers hold handles on temp files so deletes and git operations fail now and then (microsoft/windows-drivers-rs#607, Python-Dev thread). Fixes: retries, per-test directories, `handle.exe` to find the culprit.
3. Mocks go stale silently when an API shape changes (exactly the open-gitea Connect case). AI tends to add mocks, and when the same AI writes code and tests a misreading gets locked in; also beware "tests pass" claims that were not run or took a different path (arXiv 2602.00409). Fixes: check against a real server call, record/replay, independent verification.

**Open**: root cause of the occasionally failing RS-Sync integration test (`two_way_sync_propagates_dest_only_change_back_to_source`) and a real-device Android launch check. Details and the resume message are in the "Resume notes (2026-11-15)" section at the end of `PORTING.md` in `F:\RS-Sync`.

**Repositories to resume**: `F:\RS-Sync` (aon-co-jp/RS-Sync, main) and `F:\runo` (where the notes live).

**Paste-ready resume message**:
> Read the section "2026-11-15 再開用メモ: RS-Sync依存更新・…" at the end of `PORTING.md` in `F:\runo`, and "Resume notes (2026-11-15)" at the end of `PORTING.md` in `F:\RS-Sync`. Then find and fix the flaky RS-Sync integration test and verify the app on a real Android device. Use `run_in_background` for long tests. When done, update the docs of both repositories in Japanese and English and push.

## 2Poem 新設・自動更新の深化・open-web-server 本番反映(2026-11-17)
- **2Poem**(`aon-co-jp/2Poem`、`F:\2Poem`、v0.1.0): Flask/Django/FastAPI(Python 2 は最低限)→ Rust + Poem / RPoem の骨組みへ自動変換(Django→RPoem、他→Poem、`--target`で指定)。**RPoem 変換は Node.js・JS・TS・React・Bootstrap・Cosmo・手書き HTML/CSS を基本的に使わず**、画面は `open-runo-view` の SSR、画面資産は `MIGRATION.md` に記録。`2poem deps` で JS/TS/React(全世代)/Bootstrap/Cosmo/DB/Python の依存を検出・版書き換え、`2poem versions` で上流の最新版。Poem 向け(Flask/FastAPI)と RPoem 向け(Django、画面ハンドラ含む)の生成物は `cargo check` 通過。起動時の自動更新あり。公開ページ: https://easy-web.tokyo/2Poem/(と /demo)。
- **自動バージョンアップ**: RMojo v0.4.3・MFastAPI v0.2.5・2FastAPI v0.5.1・2Poem v0.1.0。RMojo は Windows 実機で「ダウンロード→SHA-256 検証→Setup 静か実行→アンインストール」を通し確認、2FastAPI の pip 経路は別の仮想環境で 0.5.0→0.5.1 を実リリースで確認。
- **VPS**: `easy-web-intros-refresh.timer`(1時間ごと、`/root/refresh_versions.py`、正本 `runo/scripts/refresh_versions.py`)が紹介ページ(5製品+/demo)に最新版と上流(Python/Flask/Django/FastAPI/Starlette/Rust/Mojo/Poem/Node/TypeScript/React/Bootstrap/PostgreSQL/MySQL/SQLite)を表示。ロールバック=`/root/easy-web-intros.before-versions-20261117`。
- **open-web-server 本番反映**: open-cpu 同梱版(WSL ビルド、`admin-2fa,domain-watchdog,fastcgi-client,ddns,sftp`、glibc 2.39)へ入れ替え、`domains.toml` に `/2Poem` を追加。5ドメインの応答は反映前後で同一、`/2Poem/` 200。ロールバック=`/root/open-web-server/target/release/open-web-server.before-opencpu-20261117`・`/root/domains.toml.before-2poem-20261117`。VPS の CPU は AVX-512BW まで検出。
- **未了**: aruaru-llm の同梱(open-cpu は同梱済み)、利用者の環境の Flask/Django 等を上流の新版へ自動で上げる機能(本製品が更新するのは本製品自身)、2Poem の PyPI 公開(将来対応)、Windows ARM64 実機(将来対応)、2Poem の macOS/Linux 実機試験、iPhone/iPad。

### 追記(2026-11-17): VPSの確認結果 / Addendum: VPS check (read-only)
**日本語**: VPSでは`open-runo-gateway.service`が稼働中(127.0.0.1:8140、Admin/DbMutate)。VPSの`/root/RPoem`は`57582aa`でoriginに2コミット遅れ、**ストリーミング強化(`1570371`・`34cb595`)を含むバイナリはまだ入っていない**(反映には WSL でビルド→scp→バックアップ→入れ替え→再起動→確認。VPSではビルドしない)。反映前の検証(connect-server 9件・router grpc_admin 17件)は手元で成功済み。本番は変更していない。
**English**: On the VPS, `open-runo-gateway.service` is running (127.0.0.1:8140, Admin/DbMutate). `/root/RPoem` is at `57582aa`, 2 commits behind origin, so **the binary with the streaming hardening (`1570371`, `34cb595`) is not deployed yet** (deploy = WSL build -> scp -> backup -> swap -> restart -> verify; never build on the VPS). Pre-deploy tests (connect-server 9, router grpc_admin 17) pass locally. Production was not changed.

## 2026-11-17 到達点のまとめと再開用メッセージ / Checkpoint summary and resume message (2026-11-17)

(同じ日付前後の他の節の内容を置き換えるものではなく、2026-11-17時点で**各担当の最新の報告**をまとめた索引。個別の詳細は各節・各リポジトリを見ること。/ An index of the latest reports as of 2026-11-17; it does not replace the other sections.)

### 日本語
**確認できたこと(担当の報告に基づく。私が直接確認したものは明記)**
- **open-raid-z-installer**: `cargo tauri build`成功、NSIS版のインストール・起動・画面下端までの到達を確認。横スクロールバーの原因はヘッダーの折り返し不足(CSSを直して再ビルド中)。**直した版でのインストール・表示確認・アンインストールの試験は未了**。MSIの試験も未了。済むまで旧TypeScript版`open_runo_installer`は削除しない。
- **RPoemゲートウェイ**: appserver系Connect化込み(`3a0d9b9`基準)をVPSへ反映。新Connect応答・キー無し401・旧`/admin/appserver-*`404・`DbMutate`健在(400=入力検証)を実測、active継続。旧バイナリは`open-runo-gateway.before-appserver-20261117`。**実プロセス起動のE2EとVPSのopen-easy-web反映は未了**。
- **ストリーミング**(Connect/gRPC): 反映前の検証をやり直し成功(`open-runo-connect-server` 9件・`grpc_admin` 17件、失敗0)。RPoem `1570371`・`34cb595`。**本番(VPS)には未反映**。
- **aruaru-IME**: VPSの`downloads/VERSION`は0.2.25でタグと一致(解決済み)。VPSの旧経路`/key`・`/session`は404、新経路は応答(私の担当が読み取りで確認)。v0.2.25のWindowsインストーラーをSHA256一致で管理者インストール→新経路200・旧経路404を確認(試験用インストールは元に戻したが**TSF DLLが1件残っている**)。**メモ帳での実入力は未確認**。
- **open-gitea**: `/`が404なのは反映前のバイナリでも同じ(退行ではない)、`/ui/`は200、直近3日のログにerror/panic 0件。**`/`を`/ui/`へ振り替えるかはユーザーの判断待ち**。
- **open-bar**: wasapi 0.27へ更新・push(`4f65b95`)、実機テストは`-- --test-threads=1`で直列実行すること。
- **version-control**: `make-disk-legacy`除外をVPSへ反映・実確認済み。

**未了・注意(優先順)**
1. open-raid-z-installerの通し試験(直した版でのNSIS/MSIのインストール・表示確認・アンインストール)→全部通ったら旧TS版を削除。
2. aruaru-IMEのメモ帳での実入力、残ったTSF DLLの後始末(管理者権限・ユーザーの許可が要る)。
3. ストリーミングの本番反映(反映手順を守る)。RPoem実プロセス起動のE2E、open-easy-web反映。
4. open-giteaの`/`の扱いの判断。Android実機の通し試験。共有基盤の負荷試験の実測。
5. 依存更新は打ち切り(`version-control`の通知で扱う)。

**落とし穴**: VPSでビルドしない(WSLビルド→glibc≤2.39→scp→旧バイナリ退避→差し替え→そのサービスだけ再起動)。複数セッションが同じ3ファイルに追記するので、編集前に`git status`と`git pull --rebase`。書き換え済みリポジトリで`git pull`しない。UAC・実機操作の許可が出ない作業は、迂回せずユーザーに依頼する。

**再開用メッセージ(そのまま貼り付け)**:
> `F:\runo\PORTING.md`末尾「2026-11-17 到達点のまとめと再開用メッセージ」と、その上の各「2026-11-15」節を読んで続きをして。まず未了1(`F:\open-raid-z-installer`の`src-tauri`でCSS修正版のNSIS/MSIのインストール・複数解像度の表示確認・アンインストール。全部通ったら旧TypeScript版`open_runo_installer`を削除してpush)、次に未了3(ストリーミングのVPS反映:RPoemの`docs/connect-hybrid.md`の手順、カナリア→差し替え→失敗時は自動で戻す)。未了2・4はユーザーの許可・判断が要るので、まず状況を報告して聞く。確認なしで開発・TEST・DEBUG・commit・pushしてよいが、VPS本番はWSLビルド→glibc確認→旧バイナリ退避の手順を守る。チャットは日本語のみ。関連リポジトリ: open-raid-z-installer / RPoem / open-easy-web / aruaru-IME / open-gitea / open-bar / version-control。

### English
**Verified (per the assignees' reports; what I checked myself is stated)**
- **open-raid-z-installer**: `cargo tauri build` succeeded; the NSIS build installs, launches and reaches the bottom edge of the window. The horizontal scrollbar came from missing header wrapping (CSS fixed, rebuilding). **Install / display check / uninstall of the fixed build is not done yet**, nor is the MSI test. Do not delete the old TypeScript `open_runo_installer` until they pass.
- **RPoem gateway**: the build with the appserver Connect migration (based on `3a0d9b9`) is deployed to the VPS; new Connect answers, 401 without a key, old `/admin/appserver-*` 404, `DbMutate` alive (400 = input validation), still active. Old binary: `open-runo-gateway.before-appserver-20261117`. **A real process-start E2E and deploying open-easy-web are not done.**
- **Streaming** (Connect/gRPC): pre-deploy verification redone and green (`open-runo-connect-server` 9, `grpc_admin` 17, 0 failures); RPoem `1570371`, `34cb595`. **Not deployed to the VPS.**
- **aruaru-IME**: VPS `downloads/VERSION` is 0.2.25 and matches the tag (resolved); old `/key`, `/session` return 404 and the new route answers (read-only check by my assignee). The v0.2.25 Windows installer (SHA256 matched) was installed as admin: new route 200, old route 404; the test installation was reverted but **one TSF DLL is left behind**. **Real typing in Notepad is unverified.**
- **open-gitea**: `/` returns 404 on the pre-deploy binary too (not a regression), `/ui/` is 200, 0 errors/panics in the last 3 days of logs. **Whether to redirect `/` to `/ui/` awaits the owner's decision.**
- **open-bar**: updated to wasapi 0.27 and pushed (`4f65b95`); run the real-device tests serially (`-- --test-threads=1`).
- **version-control**: the `make-disk-legacy` exclusion is deployed to the VPS and verified.

**Open / cautions (priority order)**
1. End-to-end test of open-raid-z-installer (install / display / uninstall of the fixed NSIS and MSI builds) → delete the old TS installer once everything passes.
2. Real typing in Notepad for aruaru-IME and cleanup of the leftover TSF DLL (needs admin rights and the user's permission).
3. Deploy streaming to production (follow the procedure); real process-start E2E for RPoem; deploy open-easy-web.
4. Decide what `/` should do on open-gitea; Android device E2E; measure the shared-infra load test.
5. Dependency updates were cut off (handled through version-control notifications).

**Pitfalls**: never build on the VPS (WSL build → glibc ≤ 2.39 → scp → back up the old binary → swap → restart only that service). Several sessions append to the same 3 files, so run `git status` and `git pull --rebase` first. Never `git pull` in a rewritten repository. When UAC / real-device permission is not granted, do not work around it; ask the user.

**Resume message (paste as is)**:
> Read "2026-11-17 到達点のまとめと再開用メッセージ" at the end of `F:\runo\PORTING.md` and the "2026-11-15" sections above it, then continue: first open item 1 (in `F:\open-raid-z-installer`'s `src-tauri`, install the CSS-fixed NSIS/MSI builds, check the display at several resolutions and uninstall; once everything passes, delete the old TypeScript `open_runo_installer` and push), then item 3 (deploy streaming to the VPS using the procedure in RPoem's `docs/connect-hybrid.md`: canary → swap → automatic rollback on failure). Items 2 and 4 need the owner's permission/decision, so report the status and ask first. You may develop, test, debug, commit and push without asking, but on the VPS keep the procedure (WSL build → glibc check → back up the old binary). Chat in Japanese only. Related repositories: open-raid-z-installer / RPoem / open-easy-web / aruaru-IME / open-gitea / open-bar / version-control.

### 追記(2026-11-17): 2Poem v0.1.1・RMojo更新のLinux確認 / Addendum: 2Poem v0.1.1, RMojo updater on Linux
**日本語**: 2Poem v0.1.1 公開(CI成功)。RMojo の自動更新を WSL Ubuntu で実リリース v0.4.3 に対し確認(取得・SHA-256・置換・次回起動で反映通知)。未了: macOS/Android/iOS の更新試験、利用者スタックの自動アップグレード、業務ロジック移植、aruaru-llm 同梱(VPSで遅く見送り)。PyPI公開・Windows ARM64実機は将来対応。**再開用メッセージ**: 「`F:\runo`・`F:\2Poem`・`F:\RMojo`・`F:\MFastAPI`・`F:\2FastAPI` を開き、`2Poem/PORTING.md` 末尾の未了を続けて完成させて。完成したらコミット・push・VPS反映。」
**English**: 2Poem v0.1.1 is released (CI green). The RMojo self-update was verified on WSL Ubuntu against the real v0.4.3 release (download, SHA-256, replace, notice on next start). Open: updater tests on macOS/Android/iOS, auto-upgrade of users' stacks, business-logic porting, aruaru-llm bundling (skipped: too slow on the VPS). PyPI publication and Windows ARM64 hardware are deferred. **Resume message**: "Open `F:\runo`, `F:\2Poem`, `F:\RMojo`, `F:\MFastAPI`, `F:\2FastAPI` and continue the open items at the end of `2Poem/PORTING.md`; when done, commit, push and deploy to the VPS."

## 2026-11-17 更新: 通し試験の結果と再開用メッセージ / Update: end-to-end test results and resume message
**日本語**: 通し試験(NSISセットアップ、ユーザー単位・UAC不要): 静かなインストール→起動→アンインストールが成功(終了コード0、アンインストール後にフォルダ消滅)。実ウィンドウで「対応状況」ボタンの開閉・実データ表示・ページ最下部まで到達を確認。1600x1200/1000x1300/700x1100で表示を確認。**横スクロールバーはヘッダーの折り返し不足が原因**で、`ui/styles.css`の`.app_header`と`.header_actions`に`flex-wrap: wrap`を追加して解消(直した版をビルド→インストール→目視で消えたことを確認→アンインストール)。**未実施**: MSIのインストール/アンインストール(MSIは全ユーザー用でUAC昇格が必要、Claudeは昇格できない。ユーザーが管理者で実行する)、非管理者では物理ディスクが列挙されないため管理者実行時の実ディスク表示、文字サイズ変更、主要ボタンの「下部固定」(この画面は縦スクロール構成で固定ボタン無し、仕様として許容するか要判断)。**旧TypeScript版`open_runo_zfs_source/open_runo_installer`は未削除**(MSI未試験のため。MSIも通ったら削除してpush)。
**再開用メッセージ(そのまま貼り付け)**: 「`F:\open-raid-z-installer`で、MSI(`F:db-target\oritaurieleaseundle\msi\`、無ければ`src-tauri`で`cargo tauri build`)を管理者権限でインストール→起動→アンインストールして結果を確認し、管理者実行でのディスク一覧も確認して。全て通ったら`F:\open-raid-z`の旧`open_runo_zfs_source/open_runo_installer`を削除してpushし、`F:uno`の`PORTING.md`の該当記述を更新して。通らない項目があれば削除せず原因を報告して。」
**English**: End-to-end results (NSIS setup, per-user, no UAC): silent install, launch and uninstall succeeded (exit code 0; the folder is gone afterwards). In the real window the "Compatibility" panel opens and closes, shows real data, and the page bottom is reachable; checked at 1600x1200 / 1000x1300 / 700x1100. **The horizontal scrollbar was caused by the header not wrapping**; fixed by adding `flex-wrap: wrap` to `.app_header` and `.header_actions` in `ui/styles.css` (rebuilt, installed, visually confirmed gone, uninstalled). **Not done**: MSI install/uninstall (the MSI is per-machine and needs UAC elevation, which Claude cannot do; the user must run it as administrator), the real-disk list when run as administrator (non-elevated runs enumerate no physical disks), font-size changes, and "pinned bottom button" (this UI scrolls vertically and has no pinned button; decide whether that is acceptable). **The old TypeScript `open_runo_zfs_source/open_runo_installer` is NOT deleted** (the MSI is untested; delete and push once it passes).
**Resume message (paste as is)**: "In `F:\open-raid-z-installer`, install the MSI (`F:db-target\oritaurieleaseundle\msi\`, or run `cargo tauri build` in `src-tauri` if missing) as administrator, launch, uninstall and check the result, and also check the disk list when run as administrator. If everything passes, delete the old `open_runo_zfs_source/open_runo_installer` in `F:\open-raid-z`, push, and update the matching entry in `F:uno`'s `PORTING.md`. If anything fails, do not delete and report the cause."

### 2026-11-17 追記: 上の「未了」の仕上げ(aruaru-db / open-cosmo)
**日本語**: 11-15の未了を片付けた。(1)`aruaru-admin`本体(Web管理画面)をローカルでブラウザ確認(`aruaru-server`+vite)。**修正前は白画面**で、4件の不具合(`serverBase`未定義・Tauriダイアログのvite解決500・クラスタ画面の応答形式不一致・対応DB画面の日本語ステータス)を直し、全10画面が描画、`CreateBackup`はtokenなし401/あり200、`RebalanceCluster`200、旧REST 0を確認(aruaru-db `aca3fca`)。(2)`admin.rs`の未使用警告を全て解消(警告0、テスト成功、`9a390b8`)。(3)open-cosmoのdocs10本は先頭に「REST全廃・対応表」の注記が既にあり、追加の整理は不要と判断(本文は歴史的記録)。**残り(正直に)**: `aruaru-db-admin-web`はVPS未配備(本番にあるのは`web/`のデモUI、Dockerfile/nginx.confのみ)、`tsc --noEmit`は`@types/react`解決などの型エラーが残る(`vite build`は成功)、ダッシュボード/ブランチ/クエリは「実装中」のスタブ、VPSのaruaru-db cloneは古いまま(未コミット変更1件・`git pull`しない)、`admin.rs`の変更は挙動無変更のため本番再配備はしていない。
**English**: The open items from 11-15 are closed. (1) The `aruaru-admin` web app was browser-tested locally (`aruaru-server` + vite). It **showed a white screen before** four fixes (undefined `serverBase`, vite 500 on the Tauri dialog import, cluster response shape mismatch, Japanese registry status); now all 10 pages render, `CreateBackup` is 401 without a token / 200 with one, `RebalanceCluster` is 200, and there are 0 old-REST calls (aruaru-db `aca3fca`). (2) All unused-code warnings in `admin.rs` are gone (0 warnings, tests pass, `9a390b8`). (3) open-cosmo's 10 docs already carry the "REST abolished / mapping" notice at the top; no further cleanup needed (the bodies are historical). **Still open**: `aruaru-db-admin-web` is not deployed on the VPS (production serves the `web/` demo UI; only a Dockerfile/nginx.conf exist), `tsc --noEmit` still reports type errors (`@types/react` resolution etc.; `vite build` succeeds), Dashboard/Branch/Query pages are "implementing" stubs, the VPS aruaru-db clone is still old (1 uncommitted change; do not `git pull`), and `admin.rs` changes are behaviour-neutral so production was not redeployed.


## 2026-11-17 version-control通知14件の依存更新・VPS反映 / Dependency updates for the 14 version-control items

**日本語**: (1) 脆弱性: open-gitea `253de21`・open-redmine `13773b7`(h2・quinn-proto・rustls・libz-sys・webpki-roots等、cargo audit 0)、aruaru-llm `d76b692`(古い`Cargo.lock`に未使用の`rust-bert`/`tch`/`zip`/`protobuf`/`zstd-safe`が残っていただけ。再生成で消え、quinn-udp・tokio・rustixを更新、テスト190件成功・audit 0)。(2) メジャー更新: RS-Blog `a8497f5`・RS-EC `a17163c`(rand 0.10・sha2 0.11、`rng()`/`random_range`/`RngExt`、ハッシュは小文字16進のまま)、audiocafe-tokyo-rust `a34b859`(reqwest 0.13は機能名`rustls-tls`→`rustls`、html-escape 0.3)。**見送り**: aruaru-IMEの`windows-core` 0.100(`windows`クレートが0.62.2で追従しておらず、上げると型が二重になる)。(3) VPS: RS-Blog・RS-EC・open-redmine(demo含む)・audiocafe-tokyo-rustを再ビルド・再起動し、各`/healthz`または`/`が200。旧バイナリは`*.before-deps-20261117`(RS-Blog・RS-EC・open-redmine)。audiocafe-tokyo-rustは旧バイナリ無し(戻すなら旧コミットから再ビルド)。RUNO・aruaru-IME・open-cuda・rs-sync・open-redmineは`git pull --ff-only`で追従(再ビルドなし)。**`atr-base`・`atr-sonic`は別リポジトリではなくaudiocafe-tokyo-rustの作業用クローン**(VPSの`/root/repository/`、依存は更新済み、atr-sonicはsonic-rs書き換えの途中ブランチ)。**open-gitea**のVPS側分岐は、VPSの26コミットがすべてoriginと同内容(履歴書き換えの影響)だったため`git reset --mixed origin/main`で履歴だけ揃えた(旧状態は`backup-before-realign-20261117`ブランチ、作業ツリーはそのまま=`static/`をディスクから配信しているため上書きしない)。**未了**: aruaru-llmのVPSクローンは17遅れ・未コミットの`Cargo.lock`とデータあり(pullしていない・再配備なし)、open-giteaのVPS作業ツリーはoriginと差(再ビルド+wasm配備のときに整える)、audiocafe-tokyo-rustのVPS `Cargo.lock`は環境差(`../RS-JSON`)で毎回差が出る。version-controlの走査はロックファイルの古い記載を拾うので、再生成してから判断する。
**English**: Vulnerabilities fixed (open-gitea, open-redmine; aruaru-llm's four were stale `Cargo.lock` entries of unused `rust-bert`/`tch`, gone after regeneration). Majors done: rand 0.10 / sha2 0.11 (RS-Blog, RS-EC), reqwest 0.13 (feature `rustls`) / html-escape 0.3 (audiocafe-tokyo-rust). Skipped: `windows-core` 0.100 in aruaru-IME (the `windows` crate is still 0.62.2). VPS: RS-Blog, RS-EC, open-redmine (+demo) and audiocafe-tokyo-rust rebuilt and restarted, all healthy; old binaries kept as `*.before-deps-20261117` except audiocafe-tokyo-rust. `atr-base`/`atr-sonic` are working clones of audiocafe-tokyo-rust, not separate repos. open-gitea's VPS history was realigned (`reset --mixed`, backup branch kept, working tree untouched because `static/` is served from disk). Open: aruaru-llm VPS clone is 17 behind with local changes, open-gitea VPS working tree differs from origin until the next rebuild + wasm deploy.


## 2026-11-17 再開用メッセージ(依存更新) / Resume message (dependency updates)

**日本語**(そのまま貼り付け):
> 依存更新の続きを再開します。作業ドライブは`F:\`、VPSは`ssh conoha`(`/root/repository/`)。まず`F:uno\PORTING.md`末尾の「2026-11-17 version-control通知14件の依存更新」を読んでください。完了済み: open-gitea・open-redmine・aruaru-llmの脆弱性、RS-Blog・RS-EC・audiocafe-tokyo-rustのメジャー更新(VPS反映・再起動・healthz 200まで)。残り: (1) aruaru-IMEの`windows-core` 0.100は`windows`クレートが0.62.2のままなので保留(`cargo search windows`で新版が出たら`windows`と同時に上げる)。(2) VPSのaruaru-llmクローンは17コミット遅れ・未コミットの`Cargo.lock`とデータあり: `git pull`せず、`git stash`ではなく差分を確認してから`git fetch`のうえ整理し、再ビルド・再起動前にバイナリを`*.before-*`で退避。(3) VPSのopen-giteaは作業ツリーがoriginと差(`static/`はディスク配信なので勝手に上書きしない)、次の再ビルド+wasm配備で整える。(4) atr-base/atr-sonicはaudiocafe-tokyo-rustの作業用クローン(atr-sonicはsonic-rs書き換え途中)。注意: 書き換え済みリポジトリで`git pull`しない、日本語を含むファイルをPowerShellで書かない(Python UTF-8かEdit/Write)、cargoはPATHに`%USERPROFILE%\.cargoin`を前置き、`cargo audit`は`Cargo.lock`を再生成してから判断(古い記載を拾う)、秘密は表示・コミットしない。

**English** (paste as it is):
> Resume the dependency-update work. Drive `F:\`, VPS via `ssh conoha` (`/root/repository/`). First read "2026-11-17 version-control通知14件の依存更新" at the end of `F:uno\PORTING.md`. Done: vulnerabilities in open-gitea, open-redmine and aruaru-llm; major updates of RS-Blog, RS-EC and audiocafe-tokyo-rust (deployed to the VPS, restarted, healthz 200). Open: (1) aruaru-IME `windows-core` 0.100 is on hold because the `windows` crate is still 0.62.2 (bump both together once `cargo search windows` shows a newer one). (2) The VPS aruaru-llm clone is 17 commits behind with an uncommitted `Cargo.lock` and data: do not `git pull`; inspect the diff, `git fetch`, tidy up, and keep the old binary as `*.before-*` before any rebuild/restart. (3) The VPS open-gitea working tree differs from origin (`static/` is served from disk, so do not overwrite it blindly); align it at the next rebuild + wasm deploy. (4) atr-base/atr-sonic are working clones of audiocafe-tokyo-rust (atr-sonic is a half-done sonic-rs rewrite). Pitfalls: never `git pull` in a rewritten repository, do not write Japanese files with PowerShell (use Python UTF-8 or Edit/Write), put `%USERPROFILE%\.cargoin` on PATH for cargo, re-generate `Cargo.lock` before trusting `cargo audit` (stale entries), never print or commit secrets.

**再開するリポジトリ(aruaru-db / open-cosmo の仕上げ) / Repositories to resume**: `aon-co-jp/aruaru-db`(新規clone、または作業用`F:\_work\aruaru-db`。`9a390b8`・`aca3fca`までpush済み)、`aon-co-jp/open-cosmo`、`F:\runo`(索引)。
**落とし穴 / Pitfalls**: 兄弟`open-raid-z`が先に進んでいるとaruaru-dbの`Cargo.lock`が解決できない→手元の確認ビルドだけ`cargo generate-lockfile`(コミットしない)。WSLのコマンドは長いPATHで壊れるので`.sh`ファイルにして`MSYS_NO_PATHCONV=1 wsl -d Ubuntu-24.04 -- bash /mnt/f/...`で実行。pnpmは`npx pnpm@9`。`aruaru-server`のトークン環境変数は`ARUARU_DB_ADMIN_TOKEN`(ローカル確認用の使い捨て値だけ使う)。Local `cargo generate-lockfile` is for scratch builds only (never commit it); put WSL commands in a `.sh` file; the token env var is `ARUARU_DB_ADMIN_TOKEN` (throwaway values only).
**貼り付け用の再開用メッセージ / Paste-ready resume message**:
> `F:\runo\PORTING.md` 末尾「2026-11-17 追記: 上の『未了』の仕上げ(aruaru-db / open-cosmo)」を読み、残り(①`aruaru-db-admin-web`のVPS配備の要否の判断と配備、②`tsc --noEmit`の型エラー解消、③ダッシュボード/ブランチ/クエリのスタブ実装)から再開してください。リポジトリは aruaru-db(新規clone)と open-cosmo。新規RESTは作らずConnectのみ。`git pull`禁止(履歴書き換え済み)、VPSでビルドしない、秘密(管理トークン等)を出さない。画面を変えたらブラウザで全画面を通し、白画面・コンソールエラー0を確認すること。チャットは日本語のみ。
> Read "2026-11-17 追記: 上の『未了』の仕上げ(aruaru-db / open-cosmo)" at the end of `F:\runo\PORTING.md` and resume from the remaining items (1: decide on and deploy `aruaru-db-admin-web` to the VPS, 2: fix the `tsc --noEmit` type errors, 3: implement the Dashboard/Branch/Query stubs). Repos: aruaru-db (fresh clone) and open-cosmo. No new REST (Connect only). No `git pull` (history was rewritten), no builds on the VPS, never print secrets. After UI changes, click through every page in a browser and confirm no white screen and 0 console errors.

## 2026-11-17 追記: RPoemゲートウェイのVPS反映(appserver系Connect化) / Update: RPoem gateway deployed to the VPS

**日本語**: RPoem(`3a0d9b9`基準、appserver系は`6ca9b74`)のゲートウェイをWSLでreleaseビルド(glibc 2.39)し、`/opt/open-runo-gateway/open-runo-gateway`へ入れ替え済み(ロールバック用=同ディレクトリの`open-runo-gateway.before-appserver-20261117`、戻すときはこれを戻して`systemctl restart open-runo-gateway`)。実測: `AppServer*`のテナント登録→一覧→削除が成功、存在しないホストの停止は`not_found`、キー無しは401、旧`/admin/appserver-tenants`は404、`DbMutate`空本文は400(入力検証)、サービスactive。キーの環境変数名は`OPEN_RUNO_SERVICE_API_KEY`(`/etc/open-runo-gateway.env`、値は出さない)。
**未了**: (1) `AppServerRegisterProcess`で実プロセスを起動する通し試験(`profile`の形式=`RuntimeProfile`を確認してから)、(2) open-easy-web(`33863ad`、呼び出し元)のVPS反映の有無確認と反映、(3) 実際のLedger書き込みの通し確認。
**再開用メッセージ**:
> `F:\runo\PORTING.md`末尾「2026-11-17 追記」を読み、未了(実プロセス起動のConnect通し試験、open-easy-webのVPS反映確認、Ledger実書き込み確認)から再開してください。リポジトリは RPoem・open-easy-web・`runo`(新規clone)。VPSでビルドせずWSLでビルドしてscp、バックアップとロールバックを用意。新規RESTは作らない。秘密は出さない。チャットは日本語のみ。

**English**: The RPoem gateway (`3a0d9b9`, appserver change `6ca9b74`) was built in WSL (release, glibc 2.39) and swapped into `/opt/open-runo-gateway/open-runo-gateway`; rollback = restore `open-runo-gateway.before-appserver-20261117` and `systemctl restart open-runo-gateway`. Verified: `AppServer*` tenant upsert/list/remove OK, stopping an unknown host returns `not_found`, no key = 401, old `/admin/appserver-tenants` = 404, empty `DbMutate` = 400, service active. The key variable is `OPEN_RUNO_SERVICE_API_KEY` in `/etc/open-runo-gateway.env` (never print it).
**Open**: (1) a real process-start test via `AppServerRegisterProcess` (check the `RuntimeProfile` shape first), (2) confirm/deploy open-easy-web (`33863ad`, the caller), (3) a real Ledger write end to end.
**Resume message**:
> Read "2026-11-17 追記" at the end of `F:\runo\PORTING.md` and resume from the open items. Repos: RPoem, open-easy-web, `runo` (fresh clones). Never build on the VPS: build in WSL and scp, with backup and rollback. No new REST. Never print secrets. Chat in Japanese only.


## 2026-11-17 追記: RPoemゲートウェイのDB化・Ledger接続の到達点と再開用メッセージ(別アカウントでの再開用) / Gateway DB persistence and Ledger wiring: status and resume message

### 日本語
- **到達点**: VPSでRPoemゲートウェイ(`open-runo-gateway.service`、127.0.0.1:8140)が稼働し、`OPEN_RUNO_SERVICE_API_KEY`で実鍵認証、専用aruaru-db(`open-runo-aruaru-db.service`、pg 15434、修正版`/opt/open-runo-aruaru-db/aruaru-server`)へ永続化。有効な鍵の書き込みは200で`db_commit_id`が入り、鍵は再起動後も有効。本番`aruaru-server`(5433)は無変更。open-web-serverは`OPEN_RUNO_API_KEY`設定済みで接続(2026-11-14)。open-raid-zのConnect版もVPS反映済み。詳細は`RPoem/PORTING.md`末尾。
- **未了**: (1) aruaru-dbの`parse_insert`修正(ブランチ`fix/insert-quoted-values`、`1590750`)は**main未マージ・本番未適用**。(2) Androidの実機通し確認(`rest-android`担当)。(3) `\`F:\open-runo-gateway.new`・`\`F:\aruaru-server.new`は手動で削除。(4) open-cosmo本体の本番起動は判断待ち。(5) Ledgerの実書き込み(open-web-server経由)の通し確認。
- **再開するリポジトリ**: `RPoem`・`aruaru-db`(WSLの`~/aruaru-db-src`)・`open-web-server`・`open-raid-z`・`open-easy-web`・`runo`。
- **落とし穴**: ビルドはVPSでなくWSL `Ubuntu-24.04`(glibc 2.39)、PowerShellから`wsl`を呼ぶ。差し替えは バックアップ→入替→検証→自動ロールバック。起動制限は`systemctl reset-failed`。秘密は出さない。書き換え済みリポジトリで`git pull`しない。
- **貼り付け用の再開用メッセージ**: 「`F:\runo\PORTING.md`末尾『2026-11-17 追記: RPoemゲートウェイのDB化…』と`F:\RPoem\PORTING.md`末尾『2026-11-15 別アカウントでの再開用メモ』を読み、(1)aruaru-dbの`fix/insert-quoted-values`をレビューしてmainへマージするか判断、(2)`ssh conoha`でゲートウェイ・専用DB・open-web-serverを読み取り確認、(3)Ledger実書き込みの通し確認、の順に進めて。VPSではビルドしない。本番の変更は事前確認、結果は日英でPORTING.mdに記録してpush。チャットは日本語のみ。」

### English
- **Status**: The RPoem gateway (`open-runo-gateway.service`, 127.0.0.1:8140) is live on the VPS with real key auth (`OPEN_RUNO_SERVICE_API_KEY`) and persists to a dedicated aruaru-db (`open-runo-aruaru-db.service`, pg 15434, fixed binary `/opt/open-runo-aruaru-db/aruaru-server`). A write with a valid key returns 200 with a `db_commit_id`; keys survive restarts. Production `aruaru-server` (5433) is untouched. open-web-server has `OPEN_RUNO_API_KEY` set and is wired in (2026-11-14); the Connect build of open-raid-z is deployed. Details at the end of `RPoem/PORTING.md`.
- **Open**: (1) the aruaru-db `parse_insert` fix (branch `fix/insert-quoted-values`, `1590750`) is **not merged and not on production**. (2) Real-device Android check (owned by `rest-android`). (3) Delete `\`F:\open-runo-gateway.new` and `\`F:\aruaru-server.new` by hand. (4) Running open-cosmo itself in production awaits a decision. (5) End-to-end real Ledger write through open-web-server.
- **Repos to resume**: `RPoem`, `aruaru-db` (WSL `~/aruaru-db-src`), `open-web-server`, `open-raid-z`, `open-easy-web`, `runo`.
- **Pitfalls**: build in WSL `Ubuntu-24.04` (glibc 2.39), not on the VPS, calling `wsl` from PowerShell. Swap = backup, replace, verify, auto-rollback. Use `systemctl reset-failed` after start-limit failures. Never print secrets. Never `git pull` in rewritten repositories.
- **Paste-ready resume message**: "Read the end of `F:\runo\PORTING.md` ('2026-11-17 追記: RPoemゲートウェイのDB化…') and the end of `F:\RPoem\PORTING.md` ('2026-11-15 別アカウントでの再開用メモ'). Then: (1) review aruaru-db `fix/insert-quoted-values` and decide on merging to main; (2) check by read-only `ssh conoha` that the gateway, dedicated DB and open-web-server are healthy; (3) verify a real Ledger write end to end. Never build on the VPS; confirm before production changes; record results in Japanese and English in PORTING.md and push. Chat in Japanese only."
