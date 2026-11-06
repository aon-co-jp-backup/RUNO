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
| **未移行・要判定** | **RS-EC 28(admin 28)** | 28 | なし | 朝の13から増加 → origin の方が新しい(**要確認**) |
| **未移行・要判定** | **RS-Blog 22(admin 22)** | 22 | なし | 朝の11から増加(**要確認**) |
| 未移行 | aruaru.tokyo | 17 | なし | — |
| 未移行 | aruaru-IME | 14 | LLM呼び出し元のみ別担当 | — |
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
