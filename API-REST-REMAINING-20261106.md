# REST全廃 残りの洗い出し (2026-11-06 10:45 JST 時点)

出典: version-control の巡回 `api-exceptions.json`(2026-11-06 10:44 生成、https://easy-web.tokyo/version-control/)。**今回から REST風ルートは、VPS の古いクローンではなく origin の最新(`git archive @{u}` の `.rs`)から数えています**(読み取りのみ。origin を読めなかった9件はクローンのまま)。
方針の正本: [API-POLICY.md](API-POLICY.md)、担当への共通指示: [API-MIGRATION-BRIEF.md](API-MIGRATION-BRIEF.md)。

## 読む前の注意
- 数え方は静的な目安です(axum `.route` / poem `.at` / hyper `(Method,"/path")`。Connect形式・`:param` 付きConnect形・例外パスは除外)。実行時に組み立てるルートは見えません。
- `api_admin` は `/api/`・`/admin/` 配下の数(`rest_like` の内数)。**Gitea / Redmine / S3 など他製品互換の API は、共通指示書では「例外(台帳に載せる)」です**。下の「例外の可能性」は未判定です。
- 内部ルーターが REST風のパスのままでも数に入ります(RS-Sync は内部ディスパッチ用の `.at("/accounts" …)` が32本として数えられていました。担当が Connect 形に書き換えて push・VPS 反映済み、次回の巡回で0になる見込み)。

## 全体の推移
| 日付 | REST風ルート(合計) | 全ルート | 備考 |
|---|---|---|---|
| 2026-11-04 | 509 | 596 | クローン基準 |
| 2026-11-05 | 481 | 573 | クローン基準 |
| 2026-11-06 | **318** | 456 | **origin 基準**(同日朝のクローン基準は 411) |

## (1) 区分 / (2) 本番(VPS)反映 — origin 基準の数
| 区分 | リポジトリ | REST風 | 担当セッション | 本番(VPS)反映 |
|---|---|---|---|---|
| 移行済み | open-english | 2(例外のみ。全93ルート中) | 完了 | **反映済み**(画面・旧パス404を確認。サーバー本体は最新コード) |
| 移行済み | aruaru-search | 0 | 完了 | 未確認 |
| 移行済み | aruaru-llm | 1 | 完了 | 稼働中 |
| 移行済み | open-web-server | 2(11-06朝は27) | 管理RESTをConnect化 | 未確認 |
| 移行済み | RS-Sync | 0(担当の push 後。11-06朝のクローン基準は32) | 担当が確認・書き換え済み | **反映済み**(担当の報告) |
| ほぼ移行 | aruaru-db | 8(朝は34) | 担当終了 | 未確認 |
| 作業中 | open-cosmo | 22(朝は44) | [担当あり](#local_53479462-a0cc-475f-ab6a-1ce83b8e4d1d) | 未確認 |
| 第1段階 | RPoem | 23 | GraphQL Mutation基盤 | 未反映 |
| 例外の可能性(未判定) | open-gitea 30 / open-redmine 29 | 59(admin 55) | なし | Gitea・Redmine 互換 API なら例外 |
| 例外の可能性(未判定) | ows-base 26 / ows-stream 26 | 52(admin 48) | なし | 管理 API。自前なら移行対象 |
| **未移行・要判定** | **RS-EC 28(admin 28)** | 28 | なし | **移行済み**(下の2026-11-07検証参照) |
| **未移行・要判定** | **RS-Blog 22(admin 22)** | 22 | なし | **移行済み**(下の2026-11-07検証参照) |
| 移行済み(2026-11-07、本番で新200/旧404を実測) | aruaru.tokyo | 0(自前API2本のみ、残りは静的・healthz) | なし | — |
| 一部移行(常駐エンジン+TSF/macOS/fcitx5/ibusはConnect済み、旧経路は期限つき互換〜2026-12-06) | aruaru-IME | 旧経路11が互換で残存 | オンライン画面(RPoem crossui→open-easy-web /ime/api→VPS常駐エンジン)とAndroid upstreamが旧経路のまま | — |
| 未移行 | aon.tokyo 13 / backup-to-discord-by-github 11 | 24 | なし | — |
| 未移行(小) | audiocafe-tokyo-rust 8 / atr-sonic 8 / open-easy-web-app 7 / e-gov.info 7 / runo.tokyo 4 / karu.tokyo 4 | 38 | なし | — |
| 例外のみ(推定) | open-raid-z 2 / RS-Guard 2 / nasa.tokyo・icpo.tokyo・fbi.tokyo 各1 | 7 | 不要 | ヘルスチェック等と推定(未確認) |

## (3) 未確認項目
1. RS-EC・RS-Blog が朝より増えた理由(古いクローンとの差か、origin に REST が追加されたか)。`git log` で確認が必要。
2. open-gitea・open-redmine・ows-base・ows-stream の `/api/`・`/admin/` が、他製品互換(例外)か自前(移行対象)か。
3. origin を読めなかった9件(非公開など、クローンのまま数えたもの)の実数。
4. 「本番反映済み」は open-english(私が直接確認)と RS-Sync(担当の報告)のみ。他は未確認。
5. aruaru-db の残り8本、open-cosmo の残り22本が移行対象か例外か。
6. REST風ルートの増加・変化を知らせる通知メールは、実運用で一度も送られていない(dry-run のみ)。

## 次の担当(影響の大きい順、同時に動かすのは最大2つ)
1. **RS-EC + RS-Blog**(合計50、増加の原因確認から。自前の管理 API なら移行)。
2. **aruaru.tokyo(17)+ aruaru-IME(14)**
   (open-gitea・open-redmine・ows-* は、先に例外かどうかの判定だけ行い、移行は判定後。)

## 追記 (2026-11-07) 担当の完了報告による更新
- **RS-EC・RS-Blog: 移行済み・本番反映済み**(Connect 68操作、旧 `/api/` 削除、例外なし)。
- **aruaru.tokyo: 本番反映済み。aruaru-IME: push 済み、旧経路は 2026-12-06 まで残す**(期限つき互換)。
- **ストリーミング: server-streaming 対応済み(RPoem)、VPS未反映**。`F:\gRPC-web-Connect` は手元・GitHub とも取得できず、実装は RPoem に統合済み。
- 未着手: open-cosmo、aon.tokyo、backup-to-discord-by-github、小規模6件。判定待ち: open-gitea・open-redmine・ows-base・ows-stream。

## 判定結果 (2026-11-07、読み取りのみ)
- **open-gitea**: `/api/repos`・`/api/accounts`・`/api/auth/request-otp` などは**独自設計で Gitea 互換ではない**(本物は `/api/v1/...`)→ **移行対象**(約30本)。例外は git smart HTTP(`info/refs`・`git-upload-pack`・`git-receive-pack`)のみ。`/api/v1/repos/..` は外部(GitHub等)を呼ぶクライアント側の文字列で、提供ルートではない。
- **open-redmine**: `/api/tickets`・`/api/projects`・`/api/saved_queries` などは**独自設計で Redmine 互換ではない**(本物は `/issues.json`)→ **移行対象**(約29本)。例外なし(GitHub連携の `/github/commits` も自前ルート)。
- **ows-base / ows-stream**: GitHub に同名リポジトリは無く、VPS(`/root/repository/ows-base`・`ows-stream`)にある **open-web-server の古い複製**(READMEが open-web-server、`/admin/tenants` 等の管理ルートが同一)。管理RESTは origin の open-web-server で Connect 化済み → **別途の移行は不要**。複製の整理(削除か git pull 相当の更新)は version-control 側の扱いを決めてから。数字(52本)は二重計上。
- 次の担当候補: open-gitea と open-redmine(自前のため移行対象)、open-cosmo、aon.tokyo。

## 2026-11-07 進捗(version-control の通知より)
- 残り REST 風ルート(目安)**266本**(前日318本から -52、11-04の509本から -243)。
- **ows-base / ows-stream の52本は open-web-server の古い複製による二重計上**のため、実質の残りは**約214本**(判定結果は上記)。
- 内訳(多い順): open-gitea 30、open-redmine 29(いずれも自前=移行対象)、RPoem 23、open-cosmo 22、aruaru.tokyo 15、aruaru-IME 14、aon.tokyo 13、backup-to-discord-by-github 11、aruaru-db 8、atr-sonic 8、audiocafe-tokyo-rust 8、e-gov.info 7、open-easy-web-app 7。
- 数字は例外(ACME・Webhook・ヘルスチェック等)を含む静的な目安。完了判断は `exceptions.toml` との突き合わせが必要。
- 次の担当: open-gitea → open-redmine(同時に動かすのは最大2つ)。

## 2026-11-07 追記: RS-Sync の確認結果(version-control の巡回・VPS 実測)
- RS-Sync は `routes=50`・`rest-like=0`・`api/admin=0`(origin 基準)。手元の `--api-only` 巡回とVPSの自動巡回(06:20 JST)の両方で確認。
- 手元・GitHub `origin/main`・VPS `/root/rs-sync` は `3b144cd` で一致、`rs-sync`・`rs-sync-demo` は稼働中。公開 Connect(`rs_sync.v1.Sync/ListAccounts`)は認証なしで 401。
- 全体の REST 風ルートは 250 本(手元の全走査)/ 259 本(VPS 06:20)。差は走査時点とclone参照の違い。
- 通知: メールはVPSから送信成功。手元は `notify.email_to` 空・環境変数 `OPEN_EASYWEB_DIST_SYNC_ADMIN_TOKEN` 未設定のため手元からは送れない(運用上はVPSが送る)。
- **未確認のまま**: 本番のログイン後の画面操作(認証情報が必要。利用者本人の確認待ち)。


## 2026-11-07 追記(aruaru.tokyo / aruaru-IME 担当)
- **aruaru.tokyo**: 別担当の移行(`tokyo_aruaru.v1.Site/ListRepos|TokoroUnlock`)が origin・VPS(8afaf4b、active)に反映済み。本担当が実測: 新経路 200/401、旧`/api/repos`・`/api/tokoro-unlock`は404。重複作業をしかけたが、重複コミットは破棄(push していない)。
- **aruaru-IME(未完)**: 旧経路の削除は未実施。理由: インストール済みTSF DLL・easy-web.tokyo/imeのオンライン画面が旧経路を使うため、配布済みクライアントを壊さない期限つき互換(2026-12-06)を維持。残作業は (1) RPoem `open-runo-crossui` の橋渡しJSを Connect パス(`/aruaru_ime.v1.Ime/Key|Session`)へ、(2) open-easy-web `ime_api` の中継を Connect パスへ(VPS反映)、(3) Android upstream、(4) IME新版exeをReleaseとVPSで同版に、(5) 期限後に daemon の旧 match 腕を削除。いずれも未着手(3リポジトリ+本番をまたぐため)。

## 2026-11-07 RS-EC・RS-Blog の独立検証(別セッションによる再確認)
- 増加の原因: 朝のクローンが古く、origin にはルートが多かった(以前の表の28/22は移行前の origin 基準)。移行は commit 0e8c223(RS-EC)・88a4a85(RS-Blog)で済み、旧 `/api/` は削除、例外なし。
- 新規 clone(`F:\RS-EC`・`F:\RS-Blog`)で `cargo test`: RS-EC 48件・RS-Blog 27件すべて成功(旧ルート404のテスト含む)。
- 本番(VPS、localhost経由で実測): RS-EC(8102)・RS-Blog(8101)とも healthz 200、旧 `/api/products`・`/api/posts` 404、Connect `POST /rs_ec.v1.Products/List`・`/rs_blog.v1.Posts/List` は認証なしで 401(JSONエラー)。ログイン後の通し呼び出しは**未確認**(認証情報を使っていない)。
- 注意: VPS上のgit cloneは古いコミットのまま(バイナリのみ差し替え)。

## 2026-11-08 追記: aon.tokyo / backup-to-discord-by-github の判定(調査のみ・コード変更なし)
- **aon.tokyo(13本)**: `src/main.rs` の全ルートがGETの表示ページ・静的ファイル(/ /links /municipal /cancer /p /k /style.css /video/*.mp4 /r.pdf 等)と `/healthz`。自前のデータAPIは0 → **すべて例外(ブラウザGET・静的配信・ヘルスチェック)、移行対象なし**。`AON_TOP_HIDDEN=1` の挙動は無変更。本番実測: `/`=404(隠し設定どおり)、`/healthz`=200。`/video/fukuyama/`(末尾スラッシュ)と `/video/fukuyama/index.html` は本番で404だった。公開状態の確認は**未了**(今回は変更していないが、期待と違う可能性があるので別途要確認)。
- **backup-to-discord-by-github(11本)**: 管理APIは既にコミット `9066b60`(2026-11-07)で Connect 化済み・push済み(`POST /bdg.admin.v1.Admin/<Method>`、本文はRS-JSON上限つき、エラー`{code,message}`)。残るのは `GET /healthz`(ヘルスチェック)と `POST /webhook/github`(GitHub Webhook、規格 https://docs.github.com/en/webhooks 、HMAC署名検証)= **例外**。テスト用の `bdg-testkit` の `/api/channels/...` は Discord/GitHub の模擬サーバーで、相手の規格どおり=例外。本番(VPS 127.0.0.1:8127、起動 2026-11-07 09:47 JST、コミット9066b60)で実測: `POST …/Admin/ListJobs`=401(トークン無し)、旧 `GET /api/jobs`=404、`/healthz`=200、`/webhook/github`=401(署名無し)。トークン付きの正常系呼び出しは今回**未実施**(テストは担当コミット時に成功と記録)。

## 追記 (2026-11-08)
- **移行・反映済み(新)**: open-gitea(31本、本番反映済み)、open-redmine(42本、本番反映済み `6612f6b`、バックアップ `/root/rd-bak-20261108-065255`)、RS-EC・RS-Blog、aruaru.tokyo、aon.tokyo(自前API 0本、全13は例外)、backup-to-discord-by-github、open-cg-cad(12本)、e-gov(`/board/post`)、RPoem の appserver 10本・open-cosmo(push済み)。
- **訂正**: aruaru-db の旧REST 7本(`/backup` 等)は VPS の古いクローン(origin より10コミット遅れ・未コミット変更あり)を読んだもので、origin/main には無い。対応不要。VPSのクローンは触らない。
- **ows-base / ows-stream**: GitHubに無く open-web-server の複製。集計の二重計上。
- **未了**: open-raid-z(`/api/status`・`/api/create`)と open-easy-web のビルド確認中、easy-web.tokyo のオンライン画面の中継の新経路化、aruaru-IME の旧経路(2026-12-06まで期限つき)と Android upstream、version-control 集計からテスト用ルートの除外。

## 2026-11-08 追記: open-gitea・open-redmine の確認(別セッションが移行・反映済みのものを検証)
- **open-gitea**: origin `f752ba5`(Connect `POST /open_gitea.v1.Gitea/<Method>` 移行は `feae9b5`、VPS反映済みと記録)。手元で `cargo test` 36件成功(初回に1件だけ失敗〈404≠400〉したが原因未特定、その後3回連続成功)。
- **open-redmine**: origin `6612f6b` で Connect 化済み(旧 `/api` 削除)。新規 clone で `cargo test` 96件成功(2件ignored)。本番反映は未確認。
- どちらも認証付きの正常系の実機呼び出しは未確認。「移行対象」としていた上の記述は、この追記で「移行済み」に置き換わる。

## 2026-11-08 追記(aruaru-IME 続報)
- **完了**: オンライン画面(RPoem crossui `f88f4d7` → open-easy-web `/ime/api` `bf2677b`)とAndroid上流呼び出しをConnect(`aruaru_ime.v1.Ime/Key|Session`)へ。easy-web.tokyo へ反映し、公開URLで新200・旧`/ime/api/key`200(互換)、実ブラウザで`/ime`の入力が`…Ime/Key`のみ200で変換されることを確認。
- **v0.2.24**: タグ・Release(Windows setup.exe+sha256、Linux/macOS/Android資産)を公開し、VPS `/var/lib/aruaru-ime/downloads/` を同版に揃え(sha256照合OK、旧版は`/root/dl-bak-20261108`)。VPS常駐エンジンは0.2.23のまま(Connect対応済み、再起動せず)。
- **注意**: CIのreleaseジョブは先にReleaseが存在しないと失敗する(手動で`gh release create`後に再実行で解消)。Windows exeはCIでは付かず、クリーンworktreeで`tools/build-installer.ps1`。
- **未了/未確認**: 期限 2026-12-06 に旧経路(daemonの旧match腕・easyの旧`/ime/api/key|session`・Android旧経路)を削除。Android・Windowsインストーラーの実機動作は未確認(Androidはcargo test 5件のみ)。


## 2026-11-08 追記: open-redmine の本番反映を確認・VPSのソースを整列
- **本番は反映済み**: VPS の `rs-chiketto`(本番8100・デモ8113)は 06:52 JST のバイナリ。VPS・公開URL(easy-web.tokyo/open-redmine)とも、旧 `/api/projects`=404、`POST /open_redmine.v1.Projects/List`=200、認証なしの `Projects/Create`=401、`/healthz`=200。
- **ソースの古さを解消**: VPS の git clone(`/root/open-redmine`・`/root/repository/open-redmine`)が `bc2ddc1` のまま「ahead 61 / behind 65」で分岐していた。`git cherry` で ahead の61コミットはすべて origin に同等のパッチがある(固有の変更0)、作業ツリーの未コミット変更(`web/pkg`)も origin と内容が同一(sha1一致)と確認したうえで、事前に `git bundle`(`/root/open-redmine-pre-align-{root,repository}.bundle`)を取り、`git fetch` + `git reset --hard origin/main` で `6c884ac` に整列。サービスは再起動せず `/healthz` 200 のまま。
- **未確認**: 稼働中バイナリが `6c884ac` のソースから作られたものか(ビルドの再現は未実施)、ログイン後の正常系呼び出し。
- **教訓**: 履歴が書き換えられたリポジトリでは `git pull` ではなく、固有コミットの有無を `git cherry` で確かめてから `reset` する。

## 2026-11-08 追記: open-cosmo・RPoem・aruaru-db の最終確認(別セッションの結果を origin で検証)
- **open-cosmo**: origin/main `6c67196`(appserver系REST10本をAdminのConnect/gRPC `AppServer*` へ、旧経路削除)で自前RESTは0本。残りは例外(`/health`・ACME・`/mcp`・SCIM・`/graphql`系・`/demo`)。VPSでは稼働していないため本番反映は対象外。今回 cargo test は再実行していない(未確認)。
- **RPoem**: origin/main `6ca9b74` で appserver 10本をConnect化。残る REST は (1) SCIM `/scim/v2/*`(RFC 7644、IdP向け標準=例外)、(2) `POST /internal/db/mutate`(内部経路。呼び出し側は open-web-server の `Ledger::forward_once` で認証ヘッダ無し)。(2)は呼び出し側を同時に直さないと壊れるため**未移行**(open-web-server側の変更が必要。今回の対象外)。`open-runo-poem-compat` の `/api/openapi.json` 等はライブラリのデモ/テストで、ゲートウェイには載らない。VPSでRPoemゲートウェイは稼働していない。
- **aruaru-db**: origin/main `849f082`「REST全廃」済み。サーバー側のRESTルートはコード上に無く(`clients/rust-axum` のサンプルのみ)。以前の「残8本」はVPSの古いクローンを読んだ誤りで対応不要。手元cloneは無く、VPSは触っていない。
- **未確認**: 上記3リポジトリの本番での新200/旧404(open-cosmo・RPoemは本番非稼働、aruaru-dbは稼働状態を今回見ていない)。

## 2026-11-08 追記2(aruaru-IME 未確認分の検証)
- **実測(v0.2.24 のWindows版エンジンを別ポート・別データ領域で起動)**: `/health`=0.2.24、Connect `Key`(konnichiwa→「今日わ」等の候補)200、`Version` 200、不正JSON 400、GETでConnect 404、`/ui`のページJSが`/aruaru_ime.v1.Ime/Key`と`/Session`を使うことを確認。
- **CI(v0.2.24)**: android-test(pixel_6 phone / pixel_c tablet)・android-apk・install-test(macOS arm64 / Ubuntu)成功。これでAndroid上流のConnect呼び出しがエミュレーター上で通ることまで確認(実機は未確認)。
- **解決**: 配布`VERSION`は公開URLでは配られない設計(easy-webが`/var/lib/aruaru-ime/downloads/VERSION`を内部で読む)=404は異常ではない。
- **未確認のまま**: Windowsインストーラーの実機インストール/アンインストール試験(`tools/installer-e2e.ps1`、管理者権限と再起動が要る。人が操作していない時に実施)、旧経路削除(2026-12-06)。
- **事故の記録**: 試験後の後始末で`taskkill`が手元PCの本物のエンジン(4660)も止めた。インストール先から起動し直し`/health`=OK(0.2.23)。インストール済みの手元エンジンはv0.2.23のまま(v0.2.24はインストーラー適用で更新)。

- **2026-11-08 未確認2点を確認**: (1) aon.tokyoの `/video/fukuyama/` はディレクトリ一覧を返さない仕様(StaticFilesEndpoint)で404が正常。動画ファイル `https://aon.tokyo/video/fukuyama/fukuyama-hotaru.mp4` は 206(video/mp4)で公開されている。(2) bdgはVPS上でトークン付き `POST /bdg.admin.v1.Admin/ListTargets` が 200 で対象一覧を返すことを確認(読み取りのみ)。
- **2026-11-08 実機インストール試験(ユーザーが管理者で実行)**: v0.2.24 のインストーラー `install exit=0`、直後の`/health`は`v=0.2.24 proto=1`で稼働(スクリプトの2秒後確認は起動が間に合わず「unreachable」と記録されたが、その後の実測で正常)。**未了**: アンインストール→再起動→再インストールの一周、実際のアプリでの日本語入力の目視確認。


## 2026-11-08 追記2: 未確認だった点の確認結果
- **RPoem**(`6ca9b74`に更新して実行): `cargo test -p open-runo-gateway -p open-runo-router` は 37 / 180 / 1 件すべて成功(失敗0、無視2)。open-cosmo は別の clone だが同じコミット内容(`6c67196`)で、そちらの cargo test は未実行。
- **aruaru-db 本番(VPS)**: 旧 `/admin/backup`・`/nodes`・`/keys`・`/status` は管理トークン付きで404。新 `POST /open_runo.aruaru.admin.v1.AdminNode/ClosedTsPublish` はトークンなし401、トークン付きでハンドラ到達(空の`{}`で400)。注意: 認証なしだと存在しない旧経路も401になるため、旧経路の削除は認証付き404で判断した。
- **未移行のまま**: RPoem `POST /internal/db/mutate`(呼び出し側 open-web-server `Ledger` の同時改修が要るため、対象外のリポジトリには触れていない)。
- **2026-11-08 追記**: インストール後、ユーザーがアプリでテキスト入力して問題なしと確認(目視確認は完了)。未了は、アンインストール→再起動→再インストールの一周のみ(任意、時間のある時)。
- **2026-11-08 インストーラー実機試験(一周完了)**: install exit=0 → アンインストール(DLL・エンジン・CLSID・Runキーがすべて外れたことをstatusで確認) → 再起動 → 再インストール `install exit=0`(`dll/clsid/daemon_exe/uninstaller=True`、HKLM Runキーあり)。インストール版エンジンは自動では立ち上がっていなかった(スクリプトの`health: unreachable`)ため手で起動し、`/health`=`v=0.2.24`・パスは`C:\Program Filesruaru-IME`であることを確認。**注意**: 再起動前は、開発用`F:ruaru-IME	arget
elease`(v0.2.14)がHKCU Runで先に立ち上がっていた(インストール版と別物)。TSF DLLは未起動時にエンジンを自動起動する設計。
- **これで aruaru-IME の未確認は、旧経路削除(2026-12-06)のみ**。
- **2026-11-08 旧経路削除の準備(aruaru-IME)**: 手元のコード・スクリプトに旧経路(`/key` `/session` ほか)の呼び出し元が残っていないことを確認(残りはeasy-webの互換2行のみ)。本番のeasy-webが旧`/ime/api/key|session`を受けた回数をjournalに数えるよう変更(`f7c5146`、入力内容は記録しない)し、VPSへ反映(`active`、新経路200・旧経路200・ログ1件を実測)。
  - **2026-12-06 の判断手順**: VPSで `journalctl -u open-easy-web --since "2026-11-08" | grep -c ime-legacy-route-hit` を見る。0に近ければ、easy-webの旧2行・daemonの旧match腕(`crates/aruaru-ime-daemon/src/main.rs`の`connect_route`以外)・Android(`crates/aruaru-ime-android`)の旧経路名を削除してv0.2.25としてリリース。多ければ期限を延ばす。
  - **この計測の限界**: 数えるのは easy-web 経由(Android旧版・古いページ)だけ。利用者PCにインストール済みの旧TSF DLL→手元エンジンの通信(127.0.0.1)は本番から見えない。TSFは0.2.24で更新されるため、削除前に自動更新の配布状況を確認すること。


## 2026-11-08 追記: open-redmine のローカル通し試験(認証付き)
- 最新ソース `6c884ac` をローカルでビルドし、開発用OTP(`RSCHIKETTO_DEV_LOG_OTP=true`、メール送信なし)で実サーバーを起動して確認: `Auth/RequestOtp`→`Auth/VerifyOtp`(トークン取得)→`Projects/Create`・`Projects/List`・`Projects/Get`(`id`指定)=すべて200、作成物を読み戻せた。旧 `/api/projects`=404、`Auth/Logout`=200。
- 試験中の400は、`Get` に `id` でなく `name` を渡した呼び出し側の誤りで、バグではない。
- **未確認**: ログアウト後にトークンが無効になるか(最後の呼び出しは本文不備で入力検査の400になり、判定できていない)。稼働中バイナリが `6c884ac` から作られたかのビルド再現。本番での認証付き呼び出し。

## 2026-11-08 RS-EC・RS-Blog 本番のログイン後の通し確認
- 本番にSMTPが未設定でOTPが送れなかったため、VPSの各サービスに drop-in(`/etc/systemd/system/rs-blog.service.d/20-smtp.conf`・`rs-ec.service.d/20-smtp.conf`、権限600)で open-easy-web と同じLolipop SMTP(info@aon.co.jp)を設定して再起動。なお open-redmine のGmail設定は 535 で拒否されたため使えなかった(open-redmine側の資格情報が失効している可能性、未調査)。
- 管理者メール宛のOTPでログインし、実呼び出しを確認: RS-Blog = Posts Create/Get/List/Delete(200、削除後Getは404)+Logout。RS-EC = Products Create/Get/List/Delete(200、削除後Getは404)+Cart/Get(200)+Logout。確認用データは削除済み。
- 未確認: Orders(Checkout等)、Categories/Pages/Tags/Comments、QRログイン、otp_qrモード。

## 2026-11-08 追記3: open-cosmo テスト成功・RPoem `/internal/db/mutate` の移行完了
- **open-cosmo のテスト**: `cargo test -p open-runo-gateway -p open-runo-router` 全て成功(37 / 178、失敗0)。続く `/internal/db/mutate` 移行後も gateway 37・router 179・proto 5 が成功。
- **`/internal/db/mutate` を移行**: RPoem `781c824`・open-cosmo `132e300`(同じ内容)で、旧 `POST /internal/db/mutate` を削除し `open_runo.admin.v1.Admin/DbMutate`(Connect/gRPC、`x-api-key` 認証)へ。呼び出し側は open-web-server の `Ledger`(`OPEN_RUNO_API_KEY` を `x-api-key` に付ける)を同時に変更して push(docs/integration.md も更新)。**旧経路は認証なしだったが、新経路は認証必須**になった。`admin.proto` への rpc 追加を忘れて統合テストが「unknown method」で落ちたため、追加して直した。
- **テスト**: RPoem は router 181・`ledger_fusion`(本物の `Ledger` から新経路で書き込み)・proto・gateway が成功、open-web-server-ledger 20 件成功。
- **VPS で実測**(RPoem を `/root/RPoem` で `git pull` → `cargo build -j2` の dev ビルドを 127.0.0.1:18099 に一時起動、確認後に停止。systemd サービスは追加していない): 旧 `/internal/db/mutate`=404、旧 `/api/schemas`=404、新 `Admin/DbMutate` は鍵なし401・不正本文400・正常200(受領票)。open-cosmo の VPS 側は紹介ページのみで未起動のため、open-cosmo 自体の VPS 実測は無い(同じコードを RPoem で確認)。
- **残る REST**: RPoem/open-cosmo は SCIM(RFC 7644)と `/health`・ACME・`/mcp`・`/graphql` 系のみ(例外)。`openapi.rs` の旧REST記述(`/internal/db/mutate` 含む)は未マウントの残置コードで未削除。

## 追記 (2026-11-08 夕)
- **version-control の集計改修**(`65bfa83`・`20f8adc`、VPS反映済み、`--dry-run` で確認・本物のタイマー実行は未確認): REST風ルート 251 → **179本**(総ルート 398 → 318)。テスト用コードと複製・別名(ows-*、atr-sonic 等)の二重計上を除外。
- **本番反映**: open-raid-z を反映(ロールバックなし)。open-easy-web とオンライン画面(aruaru-IME 新経路)は反映済みと確認。**RPoem・open-cosmo は VPS に稼働中のゲートウェイが無く(`rpoem-web`・`open-cosmo-web` は静的紹介ページのみ)、反映先なし**。ゲートウェイを稼働させる時に open-web-server `Ledger`(`OPEN_RUNO_API_KEY`)と同時に整合させる。
- 残り: 集計の実タイマー実行での確認、実機(Android/Windowsインストーラー)確認、aruaru-IME 旧経路の削除(2026-12-06)、小規模リポジトリの最終確認。


## 2026-11-09 追記: 「残り179本」の中身を調べ、集計を直した(179 → 115)
- **確認**: 2026-11-09 のメール「残り179本」で上位だった open-gitea 29・open-redmine 29 は、実際には移行済み。Connect の入口(`connect::endpoint`)の内側にある**外から届かない内部ルーター**を、集計が公開ルートとして数えていた(open-gitea は公開側が `/healthz`・`/ui`・zip/raw・git smart HTTP のみ、open-redmine も `connect::endpoint` 経由のみ)。bdg の `/api/channels/...` は試験用の偽Discord(`bdg-testkit`)、open-easy-web の `/api/auth/confirm-email-change` はメール内リンクの旧ページで、いずれも自前 REST ではない。
- **修正**: version-control `6304084` — `connect::endpoint(` を含むファイルのルートを内部ルーター扱いで除外し、`*testkit` ディレクトリを走査から外す(単体テスト追加、全7件成功)。WSLビルド(glibc 2.39)→VPSで `--dry-run` → 本番バイナリを入れ替え(元は `target/release/version-control.bak-20261109`)。結果: open-gitea 0・open-redmine 0・bdg 0、合計 **179 → 115**。
- **残り115本の内訳(未精査)**: aruaru.tokyo 15・RPoem 14・aruaru-IME 14・aon.tokyo 13・open-cosmo 13・open-easy-web-app 9 ほかは、記録上は HTML ページ・SCIM・ACME・未マウントの残置コード・旧経路の期限つき互換(aruaru-IME は2026-12-06まで)で、自前 REST ではないと判断している。ただし集計は静的な目安で、ページとAPIを区別できない。
- **注意**: 入れ替え前の `--dry-run` で VPS の `state.json`(進捗の履歴)に当日分の集計が書き込まれた(新しい集計方法の値)。通知は送っていない。次回12:20の実巡回の結果は未確認。

## 2026-11-09 追記2: 残り115本を精査 → 実質の残りは2本
- **精査結果**: 115本は、(a) テストコード内のルート(RPoem・open-cosmo の `hyper_compat.rs` など。文字列中の波括弧で除去が狂っていた)、(b) ACME規格のパス・GraphQL・SCIM・MCP・デモ画面、(c) 手書き橋渡し(aruaru-IME の daemon `connect_route`)、(d) 表示ページ・動画(aon.tokyo・aruaru.tokyo・audiocafe・e-gov・karu・runo.tokyo・fbi/icpo/nasa、RS-Guard の install スクリプト)、(e) コンテンツページ/フォント配信/catch-all のいずれかで、**自前の REST ではない**(aruaru.tokyo・e-gov は Connect の `/tokyo_aruaru.v1.Site/*`・`/e_gov.v1.Board/AddPost` が既にある)。
- **version-control の集計を修正**(`cc62c63` `a9b959c` `7bad1aa` `be72f33`): テストモジュールを文字列・コメントを飛ばす括弧対応で除去、Connect入口/手書き橋渡し/acme.rs は内部扱い、`*testkit` 除外、GraphQL/SCIM/MCP/demo・catch-all・`/page/`・`/ranking/`・`/fonts/` は例外、マウント接頭辞つきConnectパス(`/ime/api/<pkg>.Svc/Method`)を認識、API形(`/api/` `/admin/` `/vN/` `/:id`)でない素のページ・動画は別枠 `pages` に集計。VPS で `--dry-run` して **179 → 2**、本番バイナリ入れ替え(元は `version-control.bak-20261109b`)。
- **本当に残っている2本**: open-easy-web の `/ime/api/key`・`/ime/api/session`(aruaru-IME 旧経路の期限つき互換、**2026-12-06 に削除予定**)。本番ログに `ime-legacy-route-hit` が 2026-11-08〜09 で5件あり(最新 11-09 05:54)、まだ旧経路を叩く相手がいる → 期限前に消さない。
- **限界**: `pages` は「API形でないパス」という静的な推定で、`/users` のような名詞だけのREST経路は `pages` に落ちて見逃す。新規REST追加の監視には `/api/`・`/admin/`・`/vN/`・`/:id` が目印になる。**未確認**: 12:20 の実巡回で出るメールの本数(dry-runのみで確認)。`cargo test` 全体では `fix::script_tests` 1件が Windows の Git Bash でパスが壊れて失敗(今回の変更と無関係、WSL では従来どおり)。

## 2026-11-09 追記(夜)
- aruaru-db: 公開 `/graphql` から管理Mutationを外し、管理操作はConnectに一本化(`3b4a0f7`/`0faaaf2`、本番反映済み。ブラウザでの画面確認のみ未了)。
- aruaru-IME: 常駐エンジンの旧経路(`/key` `/session` `/convert` 等)を削除してpush済み(`6344880`)。ローカル実測で旧404・新200。**Release/VPS反映は保留**(旧TSF DLLが壊れる恐れ、猶予期限2026-12-06との整合を要判断)。Androidは APK内の接続先が新経路のみと確認、端末が叩いたURLの直接確認は未了。
- RPoemゲートウェイ(`open-runo-gateway.service`、127.0.0.1:8140)は担当が新規常駐。続行/停止は判断待ち。VPSのsystemd `Restart=always`変更も残す/戻すを判断待ち。
- version-control: 集計改修・誤検出修正をVPS反映。依存脆弱性は31件中2件(open-media `9cc2150`、aruaru-db `1c8a656`)のみ対応、残りはREST全廃の範囲外。
- atr-sonic(audiocafe-tokyo-rust)のsonic書き換えをpush・本番反映(全7ページ出力一致、test 15件成功)。
