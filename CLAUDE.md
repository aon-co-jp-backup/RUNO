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
open-raid-z/open-tv-chat/open-LiveKit/open-web-server/rs-to-readme等)への
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
- **2026-10-14 audiocafe.tokyoのVPSお引越し準備(日英)**: 2026-10-08にVPS上だけで直したPHP(毎朝クロールの`--cron-tech`、AIの価格訂正、`aruaru-llm`連携、中間証明書)を、
  [`audiocafe-tokyo`](https://github.com/aon-co-jp/audiocafe-tokyo)の最新版へ3方向マージして保存(衝突0)。systemd・nginxの設定を`deploy/vps/`へ、手順を同リポジトリの`PORTING.md`
  「VPS お引越し手順」(日英)へ。`aruaru-llm`の知識はGitHubへ自動バックアップ・起動時に自動復元(実測済み)。**新品VPSでの通し試験は未実施**。
  同日、`aruaru-llm`(日本語検索)・`RS-JSON`(`parse_secure`、実測+14%・SIMD版は約5.8倍速い)・`open-easy-web`(ロリポップ向けオートクロール)・`aruaru-tokyo`・`audiocafe-tokyo-rust`の
  README/CLAUDE/PORTINGを日英で更新。**未了**: AI学習リンクのRust版表示、「無料」表記の検証、`RS-JSON`の入口への適用。
  **注意**: `audiocafe-tokyo`のPHPは本番より新しい部分がある(`rakuten-mobile`の言語切替ほか)。本番のファイルをそのままコピーしない。
- **2026-10-14 open-github-backup新設(GitHub Actionsで`aon-co-jp`→`runo-aruaru`自動バックアップ) / new**: 詳細は本リポジトリ`PORTING.md`末尾と`open-github-backup/CLAUDE.md`。10/8に全件成功したが、以降はGitHubの課金/利用上限でジョブ未開始(要Billing確認)。VPSデータの暗号化バックアップは未配置。/ Full mirror OK on 10/8; jobs not starting since (billing); encrypted VPS data backup not yet deployed.
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
  個人情報の疑いは`aruaru-db-archive/quarantine/`(非公開)へ退避(`ARCHIVE_PAT`登録済み)。トークンは`F:ackup-token.txt`/`F:rchive-token.txt`(値は出さない)。
  **二次判定は見送り(ユーザー判断A)**: aruaru-llmの`POST /v1/classify-pii`は実装・push済み(5d65774)だがVPS未反映・非公開のまま、ルール検出のみで運用。
  **未了/再開ポイント**: (1)最後の変更(OnlineTimeRecorder系`db.sqlite3`の例外=架空データ、ユーザー確認済み)がGitHubへ未pushの可能性。ネットワーク不調(TLS timeout)で確認できず。
  `F:ackup-system-unpushed.bundle`に全コミットを退避済み(`git clone`して`aon-co-jp-backup/backup-system`へpush、`gh workflow run mirror.yml`)。
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
