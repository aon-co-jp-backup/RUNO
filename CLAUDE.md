# 開発方針＆開発環境ルール(RUNO)

作業ドライブは`F:\runo`。本リポジトリ自身のローカルcloneは`F:\runo`直下
(サブディレクトリ無し)。この節は
[`open-raid-z`](https://github.com/aon-co-jp/open-raid-z)の
`CLAUDE.md`を**正本**とし、各プロジェクトへコピーして同期する既存の
運用ルール継承方針に準じる(比較的新しいフレームワークの参照資料一覧・
AI駆動開発ツールに関する所感・確認不要の自動継続/リミット解除後の
自動再開・白画面バグ等を見逃さない検証徹底、等の全リポジトリ共通ルールは、
詳細をここに複製せず`open-raid-z/CLAUDE.md`を参照すること)。

## このリポジトリの役割

**このリポジトリは`aon-co-jp`エコシステム全体のメタ索引であり、
個別のコード実装は持たない。** `aon-co-jp` organization配下に分散する
各プロジェクト(RCosmo/RFrontEnd/RPoem/aruaru-db/aruaru-llm/aruaru-tokyo/
aruaru-vpn/audiocafe-tokyo-rust/audiocafe.tokyo/e-gov.info/karu.tokyo/open-cuda/
open-directx/open-easy-web/open-english(ジャンル: 学習/Study)/
open-raid-z/open-tv-chat/open-LiveKit/open-web-server/rs-dpiAwareness/rs-to-readme等)への
入口(README・PORTING.md・CLAUDE.md・役割の要約)を、`README.md`に一箇所へ
まとめて掲載することだけを目的とする。

- コードを書く場合でも、それはこのリポジトリ自身のビルド設定
  (CI等)や索引生成補助スクリプトの範囲にとどめ、各プロジェクトの
  実装そのものをこのリポジトリへ移植・複製しないこと。
- 索引内容(プロジェクト一覧・リンク・役割説明)は、各プロジェクトの
  実際のREADME.md/CLAUDE.mdの記載に基づいて記述し、推測で埋めないこと。
  プロジェクトが増減した場合はこの`README.md`を更新する。
- 同じ内容を表示するWebページ実装が
  [`aruaru-tokyo`](https://github.com/aon-co-jp/aruaru-tokyo)側
  (`/open-aruaru-runo-iLumi`、エイリアス`/open-aruaru-runo`)に存在する。
  索引の内容(プロジェクト一覧)を変更する際は、両リポジトリ間で
  記載内容が乖離しないよう注意する(自動同期の仕組みは無いため、
  手動で追従させる)。


## UI・インストーラーの品質ルール(全リポジトリ共通)

GUI・Android アプリ・インストーラーを作る/変更するときの試験ルール(複数の解像度・縦横・文字サイズでの確認、主要ボタンの画面下固定、
実データでの通し試験、インストール/アンインストール試験)は、正本の[`open-raid-z/CLAUDE.md`](https://github.com/aon-co-jp/open-raid-z)
「運用ルール」節に追記した。試験スクリプトとチェックリストは[`pdf-r2l-rs`](https://github.com/aon-co-jp/pdf-r2l-rs)の
`scripts/ui-test/`・`docs/UI-TEST-CHECKLIST.md`(2026-10-10)。
## GitHub organization

https://github.com/aon-co-jp

## 複数リポジトリ横断セッションチェックポイント

`F:\runo`ローカル作業ドライブでの複数リポジトリ横断セッション
(open-redmine・rs-sync・open-easy-web等をまたぐ作業)の直近の到達点・
次回再開ポイントは、このリポジトリの[`PORTING.md`](PORTING.md)内
「複数リポジトリ横断セッションチェックポイント」節でホストする
(このリポジトリ本来の役割=エコシステム全体のメタ索引とは別目的の
追加コンテンツであり、索引一覧表〈README.md〉自体の構成・内容には
影響しない)。

## HANDOFF
- **2026-11-01 RPoemのREST全廃→管理操作はgRPC化、gRPC-web-Connect新設 / REST removed, admin = gRPC, new gRPC-web-Connect**: RPoemの`/api/`のRESTは全削除、管理操作は`open_runo.admin.v1.Admin`(gRPC。同じ定義をgRPC-web・Connectでも受け、1ポートでHTTP/1.1とh2cを判別)。管理画面・CLIをgRPC化(管理画面はConnect+gRPC-webのハイブリッド、RPC Inspector追加)、GraphQLは問い合わせ専用で本番防御4項目、gRPCはTLS1.3/mTLS。ハイブリッドは新リポジトリ[`gRPC-web-Connect`](https://github.com/aon-co-jp/gRPC-web-Connect)。open-web-serverの呼び出しはブランチ`rest-to-graphql`でConnect化(未push、前面は**HTTP/1.1のみ**で素のgRPCは通らない=実機確認)。VPSは`/root/RPoem`のgit pullと`/root/gRPC-web-Connect`のcloneのみ(ゲートウェイは未稼働、再起動なし)。詳細は`RPoem/CLAUDE.md`冒頭の「方針転換(gRPC)」。**未了**: セキュリティ更新の`version-control`連携(RustSec走査)、RPoem→gRPC-web-Connect置換、open-web-serverのHTTP/2対応。*Done: REST removed, admin over gRPC/gRPC-web/Connect, hybrid library published; open: version-control advisory scan, RPoem migration to the library, h2 in open-web-server.*
- **2026-10-28 version-control新設(全リポジトリの依存鮮度の監視→Claude向けメッセージをメール/LINEで通知) / New**: [`version-control`](https://github.com/aon-co-jp/version-control)(公開、`F:\version-control`、VPSは`/root/easy-web.tokyo/version-control`、公開`easy-web.tokyo/version-control`・デモ`/demo/`)。crates.io/npm/packagistとクローンの遅れを走査し、メジャー更新・クローンの遅れ/分岐は常にClaude行き、マイナー/パッチは自動保守(aruaru-llm/open-cuda/open-cpu/open-directx)が稼働中なら任せる。**メール通知は実働(VPSタイマー00/06/12/18時の:20)、LINEは未設定**(トークンとユーザーIDのtxtを`F:\`に置き、VPSへscp)。依存の書き換え・`git pull`はしない。お引越し手順と再開用メッセージは`version-control/PORTING.md`末尾。**落とし穴**: VPSのdomains.tomlは2つのパスが同一ファイル(追記は1回)、ポート8125はopen-mirror使用中(本機能は8126)。*Done: scanner + dashboard + e-mail notifications live; open: LINE, working through the first 326 major gaps.*
- **2026-10-26 open-mirror新設・厳選バックアップ・非公開リポジトリ公開 / open-mirror, curated backup, repositories published**: **日本語**: (1) `gitlab-mirror`→`open-mirror`に改名(公開。GitHub→GitLabの毎日ミラーは公開リポジトリのみ・PAT不要・Actions無料)。GitLab無料期間の問題ではなく、10/13以降の失敗はGitHub Actionsの課金(非公開で月の無料枠超過または支払い失敗)が原因だった。紹介・デモは`easy-web.tokyo/open-mirror`(`/demo`)、トップページにも紹介。(2) VPSの厳選バックアップ: 秘密・個人情報を除いたものを公開`aon-co-jp/vps-backup`へ、秘密・DBの中身は暗号化して手元`F:\vps-secrets`へ(VPSの`vps-curated-backup.timer`毎日03:45、手元のタスク`vps-secrets-pull`毎日10:00+ログオン時)。旧い非公開バックアップ(`runo-aruaru/vps-data-backup`、毎日03:30)はそのまま残す。(3) 公開+Release: open-fudousan・runo.tokyo・RS-Guard・runo-scanner・RS-BootStrap・sample-mario/harrier/maid・open-cg-cad・RS-Sync(履歴からGitHubトークンを除去して強制push)。**未了**: 非公開のまま=fbi/icpo/nasa.tokyo(実在機関名)・tessdata-jpn・open-github-backup等、`open-mirror`の「予定」機能(PC/スマホ等からの自動バックアップ、保存先の選択、厳選リストの実装)、手元の`zstd`は`%USERPROFILE%\bin`に導入済み。**落とし穴**: PowerShell 5.1で日本語を含むファイルを書かない(`feedback_powershell_utf8_edits`)。**English**: `gitlab-mirror` was renamed `open-mirror` (public; public repos only, no PAT, free Actions); the failures since 10/13 were GitHub Actions billing, not GitLab. A curated VPS backup now publishes only secret-free/PII-free data to the public `aon-co-jp/vps-backup` and keeps GPG-encrypted secrets on the PC (`F:\vps-secrets`). Eleven repositories were published with releases; RS-Sync had its history scrubbed of a GitHub token first. Still private: fbi/icpo/nasa.tokyo (real agency names), tessdata-jpn, etc.; the planned open-mirror features are not built yet.
- **2026-10-26 サイト更新・open-backup 暗号化/復元・PC の起動時 HDD 調査 / Site updates, open-backup encryption & restore, boot-time HDD diagnosis**:
  **日本語**: (1) **aruaru.tokyo / audiocafe.tokyo / aon.tokyo(=aon.co.jp)**に、ブログ・動画(クリックで再生)・福山雅治ビデオ集などを追加(各リポジトリにコミット・push・VPS反映済み)。
  反映の手順: `aruaru-tokyo` = GitHub へ push → VPS の `/root/aruaru.tokyo` で `git pull`・`cargo build --release`(終了コードを確認)・`systemctl restart aruaru.tokyo.service`。`audiocafe.tokyo` のトップは **Rust 版**で、VPS の `/root/repository/audiocafe-tokyo-rust/src/main.rs` を直接編集 → build → `audiocafe-tokyo-rust.service` を再起動 → push(`format!` 内に `{` `}` を書かない)。
  **前面で受けているのは nginx ではなく `open-web-server`**(nginx.service は停止中・触らない)。**`aon.tokyo` の TOP は 2026-10-20 から全パス404(`AON_TOP_HIDDEN=1`)**だが、`/video/fukuyama/` だけは公開(`StaticFilesEndpoint`)。
  (2) **`open-backup`**: 端末側の暗号化(XChaCha20-Poly1305+Argon2id)・zstd 圧縮・スレッド並列・画面/CLI からの復元を実装し、`67ac247`・`01c0041` で push。詳細は `open-backup/CLAUDE.md` の HANDOFF(2026-10-26)。GitHub への実 push を通した確認(git 方式・API 方式とも)と、Android(API 方式)の暗号化対応も完了(2026-10-26。API 方式の既存の不具合も1件修正)。GPU(open-cuda)は使わない(律速はディスクと回線)。
  (3) **PC の「OS 起動前に HDD が長時間動く」調査**(読み取りのみ): `Disk 1`(WD 3TB・`F:`)の「IO 再試行」(イベント153)が直近30日で39件(うち22件が 10/26 の起動時)、**予期しない電源断が90日で26回**(起動時の autochk の原因になりうる)。正常再起動後(11:24)は再試行0件。SyncFolder(Store アプリ)が **`F:\` 全体を `H:\` へミラー**(1.84百万ファイル・約35分)。二重バックアップする別アプリは見つからず。
  (4) **`F:`/`H:` の整理**: 再生成できる `target`/`node_modules`/`.gradle`/`__pycache__`(目印を確認したもののみ。`.venv`・起動項目が参照するものは除外)を削除中だったが、**セッションの切れ目で途中停止**。ログは scratchpad の `regen-delete.log`(`F:` 93件削除済み)・`regen-h.log`(`H:` 128件削除済み)。**続きは、同じ手順(`regen-candidates.txt` から安全確認 → 削除)で再実行可**。`H:\StreamGaGa`(約12.7GB、同じインストーラーが複数)と `H:\_sf`(SyncFolder のごみ箱 1.2GB)は**ユーザーの判断待ち**。`vps-backup-curation-list.md`(未コミットの下書き)は別作業のもの・VPS の場所を含むためコミットしない。
  **注意**: PowerShell 5.1 は BOM 無し UTF-8 の日本語 `.ps1` を読み違える(英数字だけで書く)。ブラウザ操作が安全確認で止まったら迂回せず `curl` 等で確認する。
  **English**: (1) Added blog links, click-to-play videos and a Fukuyama video set to aruaru.tokyo / audiocafe.tokyo / aon.tokyo; all committed, pushed and deployed. The edge server is **open-web-server, not nginx**; aon.tokyo's TOP stays 404 (hidden since 2026-10-20) except `/video/fukuyama/`. (2) `open-backup`: client-side encryption (XChaCha20-Poly1305 + Argon2id), zstd compression, multi-threading and UI/CLI restore (`67ac247`, `01c0041`); open: a real push to GitHub, Android (API backend). No GPU used. (3) Boot-time HDD activity diagnosis (read-only): `Disk 1` (WD 3TB, `F:`) I/O retries and 26 unexpected power losses in 90 days; zero retries after a clean reboot; SyncFolder mirrors all of `F:\` to `H:\` (no second app found). (4) Cleanup of regenerable build folders on `F:`/`H:` was interrupted; resume with the same verified procedure; `StreamGaGa` and `_sf` await the user's decision.
- **2026-10-26 backup-to-discord-by-github 新設(GitHub→暗号化→非公開Discord) / New**: [`backup-to-discord-by-github`](https://github.com/aon-co-jp/backup-to-discord-by-github)(公開、`F:\backup-to-discord-by-github`、VPSは`/root/repository/backup-to-discord-by-github`)。`bdg-core`(XChaCha20-Poly1305+Argon2id、分割、Discord REST、復元、世代整理)、`bdg`(CLI)、`bdg-server`(RPoemの管理API+GitHub Webhook)。RPoemに`webhook`/`body_limit`/`multipart_stream`を追加(`d41a70c`)。**本物のDiscordで`doctor`全OK・公開repoの往復一致を確認**。未了: 非公開repo(`F:github-token.txt`が401で拒否=失効、fine-grainedで取り直し要)、大容量(複数パート)の実機、スケジューラ登録、`easy-web.tokyo`配置、Webhook登録、`open-gitea`未調査。Botトークン/パスフレーズ/管理トークンは`F:`直下のtxt(パスフレーズ喪失=復元不能)。*Done: CLI + server + core verified against a mock and a real Discord channel (public repo round trip). Open: private repos (token rejected with 401), big multi-part repos, scheduler, deployment.*
- **2026-10-21 open-english を maid-cafe-english へ改名・お引越し(旧名も永久に残す) / Renamed open-english → maid-cafe-english (the old repo is kept forever)**: 新リポジトリ [`maid-cafe-english`](https://github.com/aon-co-jp/maid-cafe-english)(同一の履歴・タグ・最新リリース v0.8.14 をコピー)。旧 `open-english` はREADMEの改名バナーと`RENAMED.md`(約37言語)つきで永久に残す。**自動更新(サーバー・Android)は新旧の両方を問い合わせ、新しい版を採用**(どちらも削除しない)。範囲はGitHubの名前・README・文書のリンクまで(パッケージ名・公開URL・リリースのファイル名は不変)。**リリースは元の `open-english` にタグを push**し、`release.yml` のミラージョブが新リポジトリへ複製する(シークレット `MAID_CAFE_ENGLISH_TOKEN` は2026-10-21に設定済み〈`F:git.txt`由来、組織全体に書き込める広いトークンなので、可能なら`maid-cafe-english`だけの細粒度トークンへ差し替える〉)。詳細は `open-english/CLAUDE.md` 末尾の「HANDOFF 2026-10-21」。*Done: new repo with identical history/tags and a copy of the latest release; old repo kept with banners and a 37-language notice; self-update queries both repos and takes the newer release. The mirror secret `MAID_CAFE_ENGLISH_TOKEN` is set (broad token from `F:git.txt`; replace with a single-repo fine-grained token when possible).*
- **2026-10-18 Windows再起動前のお引越し・再開メッセージ / Resume message before the Windows restart**: 
  **日本語**: (1) `open-vsc-claude`(VS Code拡張、`F:\open-vsc-claude`、v0.1.2公開済み、デモ`https://easy-web.tokyo/open-vps-claude/`)の再開は同リポジトリの`PORTING.md`末尾「お引越し・再開用メッセージ」から。未了はMarketplace/Open VSX公開(所有者のアカウントとトークンが必要)・Cosmo Router実起動・実機iOS/Android。
  (2) `dream-os/vsc`(DreamOS Code=Code-OSS 1.142.0のビルド手順)は**WSLで`npm ci`と`gulp vscode-linux-x64-min`の`package-linux-x64`まで成功、最終工程(Copilot準備`prepareBuiltInCopilotRipgrepShim`)で失敗・原因未調査、`open-vsc-claude`の同梱と`verify.sh`は未実行**。再開は`F:\dream-os\vsc\BUILD-REPORT.md`の再開コマンド(PowerShellで`wsl -d Ubuntu -- bash /mnt/f/dream-os/vsc/build.sh`)。Git Bashは`/mnt/...`を書き換えるのでPowerShellを使う。
  (3) RPoemの外部サブグラフ中継(`babc658`)は反映済み。トークン類はリポジトリに入れず`F:\`直下のtxtに置く。
  **English**: (1) Resume `open-vsc-claude` (VS Code extension, v0.1.2 released, demo `https://easy-web.tokyo/open-vps-claude/`) from the "Resume message" at the end of its `PORTING.md`; open: Marketplace/Open VSX publication (owner account + token), running the Cosmo Router, real iOS/Android devices.
  (2) `dream-os/vsc` (build recipe for DreamOS Code = Code-OSS 1.142.0): in WSL **`npm ci` and the gulp `package-linux-x64` step succeeded; the final Copilot step `prepareBuiltInCopilotRipgrepShim` failed (cause not investigated); bundling `open-vsc-claude` and `verify.sh` have not run**. Resume with the commands in `F:\dream-os\vsc\BUILD-REPORT.md` (from PowerShell: `wsl -d Ubuntu -- bash /mnt/f/dream-os/vsc/build.sh`); Git Bash rewrites `/mnt/...` paths.
  (3) RPoem's external-subgraph forwarding (`babc658`) is in. Keep tokens out of repositories (txt files at the root of `F:\`).
- **2026-10-16 【決定】作者名は本名に統一(ユーザー指示) / DECISION: use the real name as the author (user decision)**: 直下の「公開リポジトリの個人情報の取り除き」の**未決だった食い違いは、ユーザーが「本名に統一」と決定して解決した**。以後、コミットの作者はgitのグローバル名**石 塚 正 浩（MASAHIRO ISHIZUKA）**(メールはGitHubの匿名メール`18116749+aon-co-jp@users.noreply.github.com`のまま)でよい。PC・VPSのgit名を本名に揃えた。別セッションが本名で出した「READMEに作者を追記」「Cargo.tomlのauthors」等のコミットは**そのまま正**(取り消さない)。「匿名にする」方針は取り下げ。既に匿名化した112リポジトリの過去コミットはそのまま(混在してよい)、`scrub-history.sh`による内容の名前除去と「open-englishの作者の答えを名前だけに」は、本名に統一するため**不要**。*The earlier open conflict was resolved by the user: the real name is canonical from now on; the anonymous-author policy is withdrawn (past anonymised commits stay as they are; the content scrub is no longer needed).* **注意は変わらず**: 書き換えたリポジトリで`git pull`しない(古い履歴が戻る)→`git fetch`+`git reset --mixed origin/<branch>`。
- **2026-10-16 公開リポジトリの個人情報の取り除き(アカウント引っ越しの引き継ぎの続き) / Removing personal information from public repositories**: 詳細は[`PORTING.md`](PORTING.md)「公開リポジトリの個人情報の取り除き」(日英)。**Claudeの記憶は失われる前提**で、全部そこに書いた。
  要点: 112個の公開リポジトリの、**全ブランチ・タグのコミットの作者・コミッターを匿名**(`aon-co-jp` / GitHubの匿名メール)に書き換え済み(内容は同一であることを確認、`--force-with-lease`で強制push)。今後のコミットも匿名(PC・VPSのgit設定済み)。第三者の作者表示は残す。書き換え前の完全なコピーは`F:\_anon\backup\`(約800MB。個人情報入りなので公開しない)。
  **未決(最優先)**: 別のセッションが「作者名を本人の名前に統一(`Cargo.toml`の`authors`)」というコミットを複数リポジトリへ push しており、匿名の方針と食い違う→ユーザーに確認。確認前に取り消さない。その後、ファイルの内容の名前・メールの取り除き(`F:\_anon\scrub-history.sh`)、`open-english`の作者の答えを名前だけに、VPSの写しの整列、の順。**書き換えたリポジトリで`git pull`しない**(古い履歴が戻る)。
  *Done: author/committer of all branches and tags of the 112 public repositories rewritten to an anonymous identity (contents verified identical; pushed with `--force-with-lease`); future commits are anonymous (PC and VPS git config set); third parties' attribution stays; complete pre-rewrite mirrors in `F:\_anon\backup\` (~800 MB, contain personal info, never publish). **Open (top priority)**: another session pushed "unify the author name to the real name (`authors` in `Cargo.toml`)" commits to several repositories, which conflicts with the anonymous policy → ask the user; do not revert before asking. Then: remove the name/e-mail from file contents (`F:\_anon\scrub-history.sh`), reduce `open-english`'s author answer to the name only, align the VPS clones. **Never `git pull` in a rewritten repository** (the old history would come back).*
- **2026-10-14 アカウント引っ越しの引き継ぎ**: 完了/未完了/注意点を[`PORTING.md`](PORTING.md)「アカウント引っ越しのための引き継ぎ」(日英)にまとめた。最優先の未完了は
  **`open-web-server`のVPS上の未push作業(certbot webroot修正ほか)をGitHubへpushすること**。次いでJSONの実コード切り替え(`audiocafe-tokyo-rust`の`fetch_cache`)、`maid-cafe-se`の上流設定。
  `aruaru-llm`・`audiocafe-tokyo-rust`のGitHub履歴は書き直されている(強制pushしない)。
- **2026-10-14 Hand-off for the account move**: done / not done / pitfalls are summarised in "Hand-off for moving to another account" in [`PORTING.md`](PORTING.md) (Japanese and English). The top unfinished item is
  **pushing the un-pushed work on the VPS in `open-web-server` (certbot webroot fix etc.) to GitHub**, then the real JSON code switch-over (`fetch_cache` in `audiocafe-tokyo-rust`) and setting an upstream for `maid-cafe-se`.
  The GitHub history of `aruaru-llm` and `audiocafe-tokyo-rust` was rewritten (do not force-push).
- **2026-10-14 audiocafe.tokyoのVPSお引越し準備(日英)**: 2026-10-08にVPS上だけで直したPHP(毎朝クロールの`--cron-tech`、AIの価格訂正、`aruaru-llm`連携、中間証明書)を、
  [`audiocafe-tokyo`](https://github.com/aon-co-jp/audiocafe-tokyo)の最新版へ3方向マージして保存(衝突0)。systemd・nginxの設定を`deploy/vps/`へ、手順を同リポジトリの`PORTING.md`
  「VPS お引越し手順」(日英)へ。`aruaru-llm`の知識はGitHubへ自動バックアップ・起動時に自動復元(実測済み)。**新品VPSでの通し試験は未実施**。
  同日、`aruaru-llm`(日本語検索)・`RS-JSON`(`parse_secure`、実測+14%・SIMD版は約5.8倍速い)・`open-easy-web`(ロリポップ向けオートクロール)・`aruaru-tokyo`・`audiocafe-tokyo-rust`の
  README/CLAUDE/PORTINGを日英で更新。**未了**: AI学習リンクのRust版表示、「無料」表記の検証、`RS-JSON`の入口への適用。
  **注意**: `audiocafe-tokyo`のPHPは本番より新しい部分がある(`rakuten-mobile`の言語切替ほか)。本番のファイルをそのままコピーしない。
- **2026-10-14 open-github-backup新設(GitHub Actionsで`aon-co-jp`→`runo-aruaru`自動バックアップ) / new**: 詳細は本リポジトリ`PORTING.md`末尾と`open-github-backup/CLAUDE.md`。10/8に全件成功したが、以降はGitHubの課金/利用上限でジョブ未開始(要Billing確認)。宛先のActions無効化・突き合わせ・新規3件の手動ミラー・VPSデータの暗号化バックアップ(毎日03:30)は完了、残りはBilling確認のみ。/ Full mirror OK on 10/8; jobs not starting since (billing). Actions disabled on the destination, reconciliation, manual mirror of 3 new repos and the encrypted VPS data backup (daily 03:30) are done; only Billing remains.
- **2026-10-14 お引越し対応 / Migration readiness**: aruaru-llm・open-englishのREADME/CLAUDE/PORTINGに日英の「お引越し」節を追記し、知識のGitHub退避(6時間ごと)とWEB/GitHubからの自動復元をVPSへ反映。詳細は`PORTING.md`末尾。 / Added bilingual Migration sections to aruaru-llm and open-english docs; knowledge is backed up to GitHub every 6 h and restores itself from the web/GitHub (deployed to the VPS). Details at the end of `PORTING.md`.
- **2026-10-14 open-mediaの文書を整備・VPSへ配置(引っ越し可能に)**: `open-media`の`README`/`CLAUDE`/`PORTING`を日英で整備(`CLAUDE.md`/`CLAUDE.en.md`/`PORTING.md`/`PORTING.en.md`)。**引っ越し手順は`open-media/PORTING.md`**(道具・鍵の運び方・確認・OS別状況)、環境診断は`scripts/doctor.ps1`、Androidローカルビルドは`scripts/android-local-build.ps1`。make-disk時代の記録は`docs/make-disk-legacy/`。VPSは`/root/repository/open-media`(`git pull`で追従)。公開は`v0.1.10`(自動更新・1つだけ起動・日本語フォント同梱で解決したUbuntuの文字化け・関連付け・自動再生)。**更新の署名鍵は`F:\open-media-updater.key`(別の場所にも保管。無くすと更新を配れない)**。未了: PowerDVDが先に開く件の入れ直し結果、DVD/Blu-ray実ディスク、macOS・Android TV実機。
- **2026-10-12 open-media新設(make-disk + open-bar)・v0.1.4リリース完了(2026-10-13追記)**: [`open-media`](https://github.com/aon-co-jp/open-media)(公開、MIT)。make-disk最終版(v0.1.32)は無変更で残し(`ai_upmix.rs`の以前からの未コミット変更のみ残存)、以降の開発はopen-mediaで継続。open-barに`loopback.rs`(OS出力音を受け取り→sinc→32bit/384kHzで別DACへ排他出力)・32bit出力・高音補正のCD/ハイレゾ適用スイッチを追加(`f6163cb`)。
  機能: ディスクプレーヤー(音声=open-barエンジン、映像=WebView、映像+別音声combo、DVD/BDタイトル列挙、映像はFull HD/4Kへlanczos引き上げ)、システム音声の橋渡し(Windows)、LinuxのPipeWire設定(`linux/pipewire/`、未検証)。
  **確認済み**: Windowsインストーラー(v0.1.2)のインストール/起動/アンインストール、実機の音楽CD(D:)を排他+アップサンプル352.8kHz+32bitで再生(音切れ0)、橋渡し(PHL→Loxjie DAC 48→384kHz/32bit)、Linux .debの起動(WSL)、Android実機(moto g53y, Android 14)でMP4/FLAC再生。
  **2026-10-13追記**: v0.1.4のCIは全OS成功(macOS Intel版はcrates.io一時障害で再実行)、CI版APKを実機に入れて起動・表示名open-mediaを確認、Android TV向けに十字キー操作の見やすさ対応(`2c03640`、TV実機は無し)。**未了**: (1)(完了)、(2)DVD/Blu-rayの実ディスク再生、(3)macOS実機、(4)自動アップデート(署名鍵未設定)、(5)YouTube/Netflix等への割り込みはループバック方式の音楽向けのみ・DRM音声は対象外、(6)TV(Android TV)対応は未着手。作業用の`F:\open-media-test`は不要になり次第削除可。
- **2026-10-11 aruaru-IME新設・v0.1.0アルファ公開(2026-10-12 v0.2.0公開: 中国語・季節用語・優先順位・全言語一覧・オンライン画面 easy-web.tokyo/ime、VPSにサーバー運転エンジン)**: [`aruaru-IME`](https://github.com/aon-co-jp/aruaru-IME)(Windows)。`pdf-r2l-rs`のOCR(`aruaru-llm`の`/v1/ocr`)とUIの試験ルールを応用した、画面の文脈から入力モードを予測してライブ変換するIME。
  Mozc OSS辞書+Viterbi、JMdictによる日英の相互翻訳、利用者辞書/ファイル取り込み/用語辞書、Googleドライブへの自動バックアップ、常駐エンジン+薄いTSF DLL(更新でアプリの再起動不要)、Inno Setupのインストーラー。
  **未了**: インストーラーの実機の通し試験、右クリックメニュー/2列候補窓の目視確認、多言語の切替入力・中国語・世界130言語、GitHubバックアップ、macOS/Linux/Android。再開は`aruaru-IME/CLAUDE.md`のHANDOFFから。VPSへのアップロードは不要(クライアントのアプリ)。
- **2026-10-10 pdf-r2l-rs(v1.0.2〜v1.2.0公開、以降は`main`に未リリースの開発中)**: `pdf-r2l-win`/`pdf-r2l-script-win`等8リポジトリを統合した、PDF仕様書だけを根拠にした独自実装の
  [`pdf-r2l-rs`](https://github.com/aon-co-jp/pdf-r2l-rs)(MIT OR Apache-2.0、Windows/macOS/Linux/Android)。旧8リポジトリは後継案内済み、`pdf-r2l-win`/`script-win`は完成版(v1.2.0)に置換済み。
  v1.2.0までの機能: 綴じ方向(右/左/元と同じ)、OCRの書体文字化(`aruaru-llm`の`/v1/ocr`、非公開`tessdata-jpn`)、画像の高解像度化(FHD〜16K、Real-ESRGAN CPU、ArmはNEON、実機で確認)、AI文脈補完の初版。
  **開発停止時点(未リリース)**: コントラスト自動補正(薄い文書が「白紙」判定されていたのを修正)、かすれ補正(超解像+再OCR、設定`reocr`)、AI文脈補完の拡張(Qwenが走査して不自然な1〜4文字を検出→候補採点→置換、検索`aruaru-search`で実文の裏付け、
  字形の照合=新設の共有クレート`RPoem/open-runo-glyph`をサーバーの`open-cuda` sgemmで実行、1升約14ms)。**測定の正直な結果**: 合成のかすれ文書で、補正のみ48%→+かすれ補正89%→補完は初版86〜90%、連続文字+検索を加えた版は87%(880秒)で**逆効果**。
  精度優先に作り直したが**作り直し後の通し測定は未了**。AI文脈補完は**実験的・既定オフ**。詳細・試験手順・次の手は`pdf-r2l-rs/PORTING.md`(日英)。
  **VPS本番の`aruaru-llm`**: `/v1/ocr`・`/v1/ocr/fill`は反映済み。停止時点の追加分(`/scan`・`/propose`・`/glyph-rank`・`/charset`)は2026-10-10にビルド・反映(VPSにQwen未導入のため補完系は503が正常。VPSは4コア・RAM3.6GBなので補完は手元PCのaruaru-llmを使う運用)。

- **2026-10-08 公開ミラー自動バックアップ `aon-co-jp-backup/backup-system` 新設(シャットダウン時点の引き継ぎ)**: `aon-co-jp`の**公開**リポジトリのみを、
  GitHub Actions(3時間おき+手動)で検査・匿名化して`aon-co-jp-backup`へ同名ミラーする。検査=gitleaks全履歴・危険ファイル名・個人情報ルール
  (`scripts/pii_scan.py`)。コミットのメールはミラー側のみ匿名化。20MB超・モデル・`install/*/*.exe`はミラーに含めない。止めたものは`STATUS.md`に記録。
  個人情報の疑いは`aruaru-db-archive/quarantine/`(非公開)へ退避(`ARCHIVE_PAT`登録済み)。トークンは`F:\backup-token.txt`/`F:\archive-token.txt`(値は出さない)。
  **二次判定は見送り(ユーザー判断A)**: aruaru-llmの`POST /v1/classify-pii`は実装・push済み(5d65774)だがVPS未反映・非公開のまま、ルール検出のみで運用。
  **未了/再開ポイント**: (1)最後の変更(OnlineTimeRecorder系`db.sqlite3`の例外=架空データ、ユーザー確認済み)がGitHubへ未pushの可能性。ネットワーク不調(TLS timeout)で確認できず。
  `F:\backup-system-unpushed.bundle`に全コミットを退避済み(`git clone`して`aon-co-jp-backup/backup-system`へpush、`gh workflow run mirror.yml`)。
  (2)新規リポジトリ作成は二次レート制限のため1回5件・3時間おきで追いつく運用、全99件の完了確認。(3)止まったもの: old.aon.tokyo/open-bar/pinax(gitleaks検出、誤検知か要確認)。
  (4)open-english.sqlite3は空DBで例外登録済み。(5)既存RS-Sync(非公開、フィルター無し)との役割整理。

- **2026-09-30 音声・音質の研究を横断反映**: maid-cafe-seでの研究(音程と声の太さの独立制御、AI帯域拡張+声向けのロールオフ検出、
  日本語ニューラルTTSのライセンス調査、Rust化と音質の実測)を、ユーザー指示でaruaru-llm/open-english/maidcafe-programming-school/
  make-disk/maid-cafe-seへ反映した。コード変更が入ったのはmake-disk(声向けの帯域拡張モード`AudioBwe.speech`)とmaid-cafe-se(Rust
  `maid-cafe-core`/`maid-cafe-enhance`)。aruaru-llm・maidcafe-programming-schoolは音声実装が無くドキュメントのみ、open-englishは
  WEB版/ローカル版/ミックス版ごとの効き方を記録(コード変更なし、音声合成エンドポイントと共有ライブラリの置き場所は要決定)。
  各リポジトリの`CLAUDE.md`「音声・音質の研究の成果」節、正本は`maid-cafe-se/PORTING.md`「音質向上の研究」。
  **同日、音声処理をRPoemの共有クレート`open-runo-voice`(`RPoem/crates/open-runo-voice`、`docs/voice.md`)へ切り出した**(ユーザー指示、
  「汎用化できるロジックはRPoemへ」の方針どおり)。maid-cafe-coreはそれを再公開している。

- **2026-09-27 aruaru-vpn新設**: `open-tv-chat`/`open-LiveKit`開発中に
  「TV CHAT利用者向け汎用VPNアプリも同時開発してはどうか」との提案があり、
  (1)独立VPN事業として運営する案は各国VPN法規制・運営者責任を理由に見送り、
  (2)本来の目的を隠して別サイトとして配布する案は不誠実・検知回避リスクを
  理由に見送り、(3)最終的に[Outline VPN](https://getoutline.org/)/
  [Algo VPN](https://github.com/trailofbits/algo)と同じ「利用者自身が
  自分のVPS上に自分専用の中継を立てる、用途を隠さないOSSテンプレート」
  方式を採用し`aon-co-jp/aruaru-vpn`を新規作成。**aon-co-jpは中継サーバー
  を運営しない**のが最重要方針。透明性告知文(`TRANSPARENCY_NOTICE.md`、
  日英正本+`open-tv-chat`と同じ主要30ヶ国語、AI翻訳につきネイティブ検証前)
  も作成済み。実装は未着手。本`README.md`に`aruaru-vpn`行を追加。
- **2026-09-27 音声系5リポジトリ新設・統合、限界前の緊急チェックポイント**:
  open-bar(バグ修正・open-audioコンテナ再生・高音補正・PD音源テストフィクスチャ)、
  open-av(音声専用プロファイルをopen-mqa-dsdへ統合、映像専用の薄いクレートへ)、
  open-mqa-dsd(上記コンテナ実装を吸収、旧称「open-audio」は廃止し
  `"format": "open-mqa-dsd"`へ改称)、**新規`open-audio-sr`**(AudioSR実在の拡散モデルで
  音声帯域拡張、実機で定量検証済み)、**新規`open-music-llm`**(MusicGen実在のオーディオLLMで
  音楽生成、環境構築のみで生成自体は未検証のまま中断)。各リポジトリのCLAUDE.md/PORTING.mdに
  詳細な引き継ぎ・環境固有の既知の問題(このPCでのPython import異常な遅さ等)を記録済み。
  本`README.md`にopen-bar/open-av/open-mqa-dsd/open-audio-sr/open-music-llmの行を追加。
  ユーザーから「もうリミットなので」との指示によりドキュメント更新・pushのみで緊急停止。

- **2026-08-28 ドキュメント整理**: 作業ドライブ移行(`F:\open-runo`→
  `F:\runo`)は完了し`F:\open-runo`自体が削除されたため、移行途上を
  前提とした記述・重複clone(`F:\open-runo\aon`)に関する記述を全文
  削除し、現在の構成(`F:\runo`のみ)を前提とした簡潔な記述へ整理した。
- **2026-09-03 aruaru-dbセッション記録の同期**: `aruaru-db`の公式薄い
  コネクタ拡張(続き27〜33、Go/Java/.NET/Ruby/Mojo新設・.NET実バグ修正・
  Python asyncpgハング調査)の詳細は、このリポジトリ本来の役割(索引)を
  汚さないよう、詳細記録は[`PORTING.md`](PORTING.md)の
  「複数リポジトリ横断セッションチェックポイント」節(続き27・続き28)へ
  日英併記で集約した。`README.md`の`aruaru-db`行の役割要約は今回の
  コネクタ追加では実質的な変更が無いため無編集(索引は実装詳細ではなく
  役割サマリのみを持つ既存方針どおり)。

  **🔁 再開用メッセージ(次回このセッションを続ける人へ)**: aruaru-db
  リポジトリ側の正本は`aruaru-db/CLAUDE.md`の「🛑 再開用メッセージ」節
  (続き32時点)。未解決の残作業は (1) Go/Java/Rubyコネクタの実ビルド・
  実テスト(この開発機にツールチェーン無し)、(2) 4コネクタとも実サーバ
  往復(ライブE2E)が未実施(.NETのみ2026-09-03に完了、`NoTypeLoading`
  修正込み)、(3) Python `asyncpg`の接続ハング問題の原因調査
  (`clients/python-aruaru-db/README.md`に記録、`live-check.py`で再現可)、
  (4) Mojoコネクタの実コンパイル・実テスト(`mojo`ツールチェーン無し)。
  VPS(`ssh conoha`、`/root/repository/aruaru-db`)は`git pull`で追従済み
  (サーバ本体は無変更のためサービス再起動は都度不要、クライアント
  コネクタのみの変更)。
- **2026-09-15 open-english-pc再統合によるリポジトリ削除**: 2026-09-10に
  `open-english`から submodule 切り出ししていた`aon-co-jp/open-english-pc`
  (クライアント実装 `web/` `pc/` `tablet/` `mobile/`)を、ユーザー指摘
  (「わざわざopen-englishから独立させた意味が無い」——インストーラー
  組み立て・リリースCI・配信サーバーが分離後も本体側に残ったままで、
  分離の目的が実現されていなかったため)により履歴を保持して本体へ
  再統合し、`open-english-pc`リポジトリ自体を削除した。本`README.md`から
  `open-english-pc`の行を削除。
- **2026-09-26 open-tv-chat新設**: Skype風「世界約130ヶ国語リアルタイム
  音声翻訳」対応のTV会議/ビデオチャットアプリ構想を`aon-co-jp/open-tv-chat`
  として新規作成。`easy-web.tokyo`でWindows/macOS/Linux/Android/iPhone向け
  クライアントを配布し、利用者PCに`open-web-server`を立てRust+`RPoem`
  (Cosmo互換)で動かす構成。音声翻訳は2ヶ国語〜最大10ヶ国語同時対応、対応言語は
  「英語名(現地呼称) = ネイティブ表記」併記(例: Iran (Persia) = فارسی (Farsi))。
  現時点は設計ドキュメント(README/CLAUDE.md/PORTING.md)のみで実装は未着手、
  音声翻訳エンジン(ASR/MT/TTS)の選定が次回最優先課題。詳細は
  `open-tv-chat/PORTING.md`の「次回再開ポイント」を参照。本`README.md`には
  `open-tv-chat`行を追加(役割要約のみ、実装詳細は転記しない既存方針どおり)。
- **2026-09-26 open-LiveKit新設**: `open-tv-chat`の通話リレーサーバー
  (既定モードで相手にIP非開示、翻訳もサーバー側処理)に使うSFU技術として、
  LiveKit(Go+Pion製、Apache-2.0)/mediasoup/Janus/Jitsi Videobridge/自前実装
  のトレードオフを比較した結果、ユーザーの意向により「LiveKitのアーキテクチャ
  を参考に、コードは流用せず一からRust+RPoemで再実装する」方針となり、
  `aon-co-jp/open-LiveKit`を新規作成。じっくり時間をかけてGoogle検索・GitHub
  調査を行った上で設計・実装を進める方針(ユーザー指示)。現時点はLiveKitの
  アーキテクチャ調査(SFUモデル・ルーム管理・Redisによる水平スケーリング・
  gRPC+Protocol Buffersシグナリング等)のみ、実装は未着手。詳細は
  `open-LiveKit/PORTING.md`の「次回再開ポイント」(WebRTCスタックのwebrtc-rs
  vs str0m比較から着手)を参照。本`README.md`には`open-LiveKit`行を追加。
- **2026-09-26 open-LiveKit技術選定1〜5決定+aruaru-db-archive新設**:
  GitHub調査(スター数・実運用実績・ライセンス)に基づき(1)WebRTCスタック=
  webrtc-rs、(3)シグナリング=RPoem GraphQL Subscriptions、(4)Simulcastは
  フェーズ2見送り、(5)翻訳エンジンはAgentフック方式、を決定。(2)水平
  スケーリングはユーザー指示により「`aruaru-db`+PostgreSQLのDUAL DB
  (VPS高速キャッシュ)+非公開の`aon-co-jp/aruaru-db-archive`(Git-on-SQL
  経由の自動バックアップ)」の2層構成に確定(世界中からの大量アクセス時に
  VPSストレージが溢れるのを防ぐため、データが古くなると自動でGitHub側
  リポジトリへ同期・VPS側は破棄する設計、利用者端末側にも任意でログ保存
  できる選択肢を用意)。`aruaru-db-archive`を新規作成(非公開)、雛形README
  のみでVPS側の自動同期実装は未着手。詳細は`open-LiveKit/README.md`
  「技術選定の決定事項」を参照。本`README.md`には`aruaru-db-archive`行を追加。

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

### Deutsch (KI-Übersetzung, redaktionell überarbeitet; noch nicht von Muttersprachlern geprüft)
**Das sind keine Alternativen, die man vereinheitlichen müsste, sondern verschiedene Schichten.** REST ersetzen können nur Connect, gRPC und GraphQL; WASM ist eine Technik zum Bauen der Oberfläche.

| Begriff | Was es ist | Ersetzt REST? |
|---|---|---|
| REST | API-Stil, der Operationen über URLs und HTTP-Methoden ausdrückt | wird abgeschafft |
| **Connect** | `POST /Service/Methode` mit JSON-Body; per `curl` und per `fetch` im Browser aufrufbar | ja (**gewählt**) |
| **gRPC** | Dasselbe Service/Methode-Prinzip über binäres protobuf und HTTP/2; schnell, gut für Streaming | ja (**zwischen Diensten**) |
| gRPC-web | Browsertaugliche Variante von gRPC | ja (bei Bedarf) |
| GraphQL | Abfragesprache: man fragt genau die gewünschten Felder ab | teilweise (**nur lesende Abfragen**) |
| WASM | Führt Rust im Browser aus | nein (Technik für die Oberfläche) |

- **Vom Browser oder per `curl` aufgerufene APIs nutzen Connect** (POST, JSON mit RS-JSON gelesen und geschrieben). Browser-WASM spricht kein reines gRPC; mit Connect bleibt es bei `fetch`, und `prost` wird nicht gebraucht (die Datei wächst nicht).
- **Zwischen Diensten (Server zu Server, schwere Arbeit, Streaming) gilt gRPC.** Meist genügt Connect; auf gRPC wird nur dort umgestellt, wo Streaming wirklich nötig ist.
- **GraphQL nur lesend**, für Abfragen, die mehrere Daten bündeln. Nicht für Schreibvorgänge.
- **WASM bleibt die Technik für die Oberfläche.** Die aufgerufene API ist nur zu Connect geworden.
- Schnittstellen, deren Form ein fremder Standard vorgibt (ACME, OAuth-Callbacks, Webhooks Dritter, Health-Checks, statische Dateien, OTLP), bleiben gewöhnliches HTTP.
- **Im Zweifel Connect.**

### Русский (перевод выполнен с помощью ИИ и отредактирован; носителями языка пока не проверен)
**Это не альтернативы, которые нужно свести к одной, а разные уровни.** Заменить REST могут только Connect, gRPC и GraphQL; WASM — это способ построить интерфейс.

| Термин | Что это | Заменяет REST? |
|---|---|---|
| REST | Стиль API: операции выражаются через URL и HTTP-методы | отменяется |
| **Connect** | `POST /Service/Method` с телом JSON; вызывается и из `curl`, и из браузерного `fetch` | да (**выбран**) |
| **gRPC** | Та же идея «сервис/метод» поверх двоичного protobuf и HTTP/2; быстро, удобен для потоков | да (**между сервисами**) |
| gRPC-web | Вариант gRPC для браузера | да (при необходимости) |
| GraphQL | Язык запросов: запрашиваются именно нужные поля | частично (**только запросы на чтение**) |
| WASM | Запускает Rust внутри браузера | нет (технология интерфейса) |

- **API, которые вызываются из браузера или через `curl`, используют Connect** (POST, JSON читается и пишется через RS-JSON). Браузерный WASM не умеет обычный gRPC; с Connect остаётся прежний `fetch`, а `prost` не нужен (размер файла не растёт).
- **Между сервисами (сервер — сервер, тяжёлые задачи, потоки) используется gRPC.** В большинстве случаев хватает Connect; на gRPC переходят только там, где потоки действительно нужны.
- **GraphQL — только для чтения**, для запросов, собирающих несколько данных. Для записи (операций) не применяется.
- **WASM остаётся технологией для интерфейса.** Изменилось лишь то, что вызываемый им API стал Connect.
- Интерфейсы, форму которых определяет чужой стандарт (ACME, обратные вызовы OAuth, вебхуки третьих сторон, проверки работоспособности, статические файлы, OTLP), остаются обычным HTTP.
- **Если сомневаетесь — Connect.**
