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

