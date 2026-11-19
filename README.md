# RUNO (旧称: open-aruaru-runo-iLumi → aon → RUNO)

🏢 GitHub organization: **[aon-co-jp](https://github.com/aon-co-jp)**

このリポジトリは、`aon-co-jp` organization配下に分散する複数プロジェクト
全体の**「プロジェクトシリーズ索引」を担うメタリポジトリ**です。このリポジトリ
自体は個別の実装コードを持たず、各プロジェクトへの入口(README・
CLAUDE.md・PORTING.md・役割の要約)をまとめて一覧できることだけを目的と
しています。ローカルの作業ドライブは`F:\runo`。

対応する実装は [`aruaru-tokyo`](https://github.com/aon-co-jp/aruaru-tokyo)
(Rust + [Poem](https://github.com/poem-web/poem)製)側にもあり、
`/open-aruaru-runo-iLumi`(および互換パス`/open-aruaru-runo`)で
このメタ索引と同じ内容をWebページとして13ヶ国語・GitHub API連携付きで
閲覧できます。

## プロジェクトシリーズ一覧

`F:\runo`配下で実際にgitリポジトリとして存在し、GitHub(`aon-co-jp`)上に
リモートが確認できるプロジェクトを掲載しています。
各プロジェクトの役割説明は、それぞれのリポジトリの実際の
`README.md`/`CLAUDE.md`の記載に基づく要約です(推測での記載はしていません)。

| プロジェクト | ジャンル (Category / Genre) | GitHub | README | PORTING | WEBアプリ設計思想、開発方針、開発環境ルール | 役割 |
|---|---|---|---|---|---|---|
| RCosmo | — | [aon-co-jp/RCosmo](https://github.com/aon-co-jp/RCosmo) | [README](https://github.com/aon-co-jp/RCosmo/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RCosmo/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RCosmo/blob/main/CLAUDE.md) | Rust製GraphQL Federationプラットフォーム(Poem/Tauri/Cosmoは非依存・互換自前実装)。WunderGraph Cosmoの有料版機能をOSS・Pure Rustで実現し、独自の自己学習AIを搭載(外部LLM契約不要)。姉妹リポジトリ`poem-cosmo-tauri`と並行開発。 |
| RFrontEnd | — | [aon-co-jp/RFrontEnd](https://github.com/aon-co-jp/RFrontEnd) | [README](https://github.com/aon-co-jp/RFrontEnd/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RFrontEnd/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RFrontEnd/blob/main/CLAUDE.md) | HTML5/CSS3/TypeScript/React相当を、既存実装のコードを一切流用せず一から開発する複数プロジェクト(RHTML/RCSS/RTypeScript等)を束ねる親リポジトリ。 |
| RPoem | — | [aon-co-jp/RPoem](https://github.com/aon-co-jp/RPoem) | [README](https://github.com/aon-co-jp/RPoem/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RPoem/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RPoem/blob/main/CLAUDE.md) | RCosmoと同種のRust製GraphQL Federationプラットフォーム(Poem/Tauri/Cosmo非依存の互換自前実装)。`open-runo`を正本として分岐した`poem-runo`をさらにリネーム・統合した後継リポジトリ。 |
| gRPC-web-Connect(RPoemへ統合済み) | — | [RPoem/crates/open-runo-connect-*](https://github.com/aon-co-jp/RPoem/tree/main/crates) | [説明](https://github.com/aon-co-jp/RPoem/blob/main/docs/connect-hybrid.md) | — | — | ConnectとgRPC-webのハイブリッド(core/server/client)。2026-11-01にRPoem内へ統合。旧リポジトリは2026-11-02に削除済み(履歴はRPoemへ統合) |
| aruaru-db-archive(非公開) | — | [aon-co-jp/aruaru-db-archive](https://github.com/aon-co-jp/aruaru-db-archive) | [README](https://github.com/aon-co-jp/aruaru-db-archive/blob/main/README.md) | — | — | `aruaru-db`(VPS高速キャッシュ層)から古くなったデータをGit-on-SQL経由で自動バックアップする非公開アーカイブ先。`open-LiveKit`のノードルーティング状態管理(DUAL DB構成)で使用予定。**2026-09-26時点は雛形のみ、自動同期の実装は未着手**。 |
| open-github-backup(非公開) | — | [aon-co-jp/open-github-backup](https://github.com/aon-co-jp/open-github-backup) | [README](https://github.com/aon-co-jp/open-github-backup/blob/main/README.md) | — | — | `aon-co-jp`の全リポジトリを GitHub Actions で`runo-aruaru`(非公開)へ自動ミラーするバックアップ。RS-Syncの同期とVPS cronを置き換えた。2026-10-08に全件成功、以降はGitHub課金/利用上限でジョブ未開始(要Billing確認、残る課題はこれのみ)。VPSデータの暗号化バックアップ(毎日03:30)も稼働中。 |
| backup-to-discord-by-github | — | [aon-co-jp/backup-to-discord-by-github](https://github.com/aon-co-jp/backup-to-discord-by-github) | [README](https://github.com/aon-co-jp/backup-to-discord-by-github/blob/main/README.md) | — | — | GitHubのリポジトリ(公開・非公開)を`git bundle`にして**クライアント側で暗号化**・分割し、**非公開のDiscordサーバー**へ保存/復元するバックアップ(Rust+RPoem)。CLI`bdg`(doctor/backup/list/restore/prune/run)と、管理API+GitHub Webhook受信の`bdg-server`。2026-10-26に本物のDiscordで往復を実機確認(公開repo1つ)。非公開repo・大容量・`easy-web.tokyo`配置は未了。Discordの規約リスクがあるため唯一のバックアップにはしない。RPoemに`webhook`/`body_limit`/`multipart_stream`を同時追加。 |
| aruaru-db | — | [aon-co-jp/aruaru-db](https://github.com/aon-co-jp/aruaru-db) | [README](https://github.com/aon-co-jp/aruaru-db/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/aruaru-db/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/aruaru-db/blob/main/CLAUDE.md) | CockroachDBの分散強整合×Snowflakeのストレージ/コンピュート分離×Git-on-SQLバージョン管理を、すべてPure Rustで実装するハイブリッド分散データベース。 |
| aruaru-llm | — | [aon-co-jp/aruaru-llm](https://github.com/aon-co-jp/aruaru-llm) | [README](https://github.com/aon-co-jp/aruaru-llm/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/aruaru-llm/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/aruaru-llm/blob/main/CLAUDE.md) | `aruaru`エコシステム(aruaru-tokyo・aruaru-db・e-gov.info・karu.tokyo等)共通の「AIチャットコマース」応答サービス。リポジトリ名は「LLM」を冠するが、実際のLLM推論への差し替えは今後という正直な開示がREADMEに明記されている。 |
| aruaru-search | — | [aon-co-jp/aruaru-search](https://github.com/aon-co-jp/aruaru-search) | [README](https://github.com/aon-co-jp/aruaru-search/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/aruaru-search/blob/main/CLAUDE.md) | Rust製の自前メタ検索(APIキー不要・VPSで完全無料)。Bing・Brave・Yahoo! JAPAN等の公開ページを解析・統合し、世界約130言語で英語圏に偏らないよう並べ替える。検索元の変更は`aruaru-llm`の無料AIで毎朝自動保守し、`aruaru-llm`の検索の第一候補として連動する。 |
| aruaru-tokyo | — | [aon-co-jp/aruaru-tokyo](https://github.com/aon-co-jp/aruaru-tokyo) | [README](https://github.com/aon-co-jp/aruaru-tokyo/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/aruaru-tokyo/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/aruaru-tokyo/blob/main/CLAUDE.md) | [aruaru.tokyo](https://aruaru.tokyo/)のTOPページ。Rust + Poem製、DB非依存・1バイナリ完結。`audiocafe.tokyo`(PHP)とは別ドメイン・別スタックの姉妹サイト。 |
| aruaru-vpn | — | [aon-co-jp/aruaru-vpn](https://github.com/aon-co-jp/aruaru-vpn) | [README](https://github.com/aon-co-jp/aruaru-vpn/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/aruaru-vpn/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/aruaru-vpn/blob/main/CLAUDE.md) | [Outline VPN](https://getoutline.org/)/[Algo VPN](https://github.com/trailofbits/algo)を参考に、コードは流用せず一からRust+`open-web-server`で再実装する、利用者が自分で借りたVPS上に自分専用のプライバシー中継を立てられるOSSテンプレート。**aon-co-jpは中継サーバーを運営しない**(用途を隠さない透明性方針)。**2026-09-27時点は設計ドキュメント段階、実装は未着手**。 |
| aruaru-IME | — | [aon-co-jp/aruaru-IME](https://github.com/aon-co-jp/aruaru-IME) | [README](https://github.com/aon-co-jp/aruaru-IME/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/aruaru-IME/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/aruaru-IME/blob/main/CLAUDE.md) | 画面の文脈から入力モードを予測し、漢字に変換することを前提に打つそばから変換結果を出す AI IME(Windows、**2026-10-12 v0.2.0 アルファ公開**、オンライン画面 https://easy-web.tokyo/ime)。Mozc OSS 辞書+Viterbi、日本語⇔英語の相互翻訳(JMdict)、単語・熟語・用語辞書(検索で作成)、プログラミング言語/フレームワークの補完と訂正、Google ドライブへの自動バックアップ。`aruaru-llm`・`open-cuda`・`open-easy-web` と連携。中国語(ピンイン)・季節用語・優先順位の調整・世界132言語の一覧に対応。準備中言語の入力エンジン・macOS/Linux/Android のIME本体は未了。 |
| audiocafe-tokyo-rust | — | [aon-co-jp/audiocafe-tokyo-rust](https://github.com/aon-co-jp/audiocafe-tokyo-rust) | [README](https://github.com/aon-co-jp/audiocafe-tokyo-rust/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/audiocafe-tokyo-rust/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/audiocafe-tokyo-rust/blob/main/CLAUDE.md) | `audiocafe.tokyo`の既存PHPモノリスをRust + Poemへ段階的に移行するプロジェクト(第一段)。既存PHP実装は`audiocafe-tokyo`リポジトリのまま並行運用。 |
| audiocafe.tokyo | — | [aon-co-jp/audiocafe-tokyo](https://github.com/aon-co-jp/audiocafe-tokyo) | [README](https://github.com/aon-co-jp/audiocafe-tokyo/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/audiocafe-tokyo/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/audiocafe-tokyo/blob/main/CLAUDE.md) | PHP製のマルチコンテンツサイト。IT/建築系求人情報(`aruaru`)・女性向け求人/夜間エンターテインメント情報(`aruaru-lady`)・楽天モバイル関連情報・会社案内などを扱う。 |
| e-gov.info | — | [aon-co-jp/e-gov](https://github.com/aon-co-jp/e-gov) | [README](https://github.com/aon-co-jp/e-gov/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/e-gov/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/e-gov/blob/main/CLAUDE.md) | 行政のデジタル化と、個人〜貿易商社まで対応するオンライン貿易・不動産プラットフォームを、LINEアプリ・WEBサイト・コンビニ端末という複数の入口から利用できる形で統合するプロジェクト。**まだサンプル・デモンストレーション段階**(READMEに明記)。 |
| karu.tokyo | — | [aon-co-jp/karu-tokyo](https://github.com/aon-co-jp/karu-tokyo) | [README](https://github.com/aon-co-jp/karu-tokyo/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/karu-tokyo/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/karu-tokyo/blob/main/CLAUDE.md) | `karu.tokyo`のTOPページ。Rust + Poem製、DB非依存の1バイナリ完結サーバー。軽井沢・あきる野市・東京の観光とリモートワーク、IT・AI・AUDIO・貿易産業を紹介。 |
| open-audio-sr | AUDIO | [aon-co-jp/open-audio-sr](https://github.com/aon-co-jp/open-audio-sr) | [README](https://github.com/aon-co-jp/open-audio-sr/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/open-audio-sr/blob/main/CLAUDE.md) | AudioSR(実在する拡散モデル、コードMIT・重みApache-2.0)による音声帯域拡張(超解像)をRust+RPoemでラップ。ライブラリ呼び出し・HTTP API双方で実機検証済み(単純補間との定量比較で高域エネルギー生成を確認)。 |
| open-av | AUDIO/VIDEO | [aon-co-jp/open-av](https://github.com/aon-co-jp/open-av) | [README](https://github.com/aon-co-jp/open-av/blob/main/README.md) | — | — | MP4/MKV映像+DSD音声+イマーシブ配置メタデータを1ファイルにまとめるオープンな映像コンテナ仕様。音声専用プロファイルは`open-mqa-dsd`へ2026-09-26に統合済み、本体は映像プロファイル専用の薄いクレート。 |
| open-bar | AUDIO | [aon-co-jp/open-bar](https://github.com/aon-co-jp/open-bar) | [README](https://github.com/aon-co-jp/open-bar/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-bar/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-bar/blob/main/CLAUDE.md) | foobar2000をリスペクトした高音質・高画質プレーヤー(共有/排他/DoP再生モード、DSD対応、open-mqa-dsdのopen-audioコンテナ再生対応)。 |
| open-cuda | — | [aon-co-jp/open-cuda](https://github.com/aon-co-jp/open-cuda) | — (README.mdは無く`README-Japan.md`等が代わりに存在) | — (PORTING.mdは未整備) | — (CLAUDE.mdは未整備) | OmniGPU設計文書(`OmniGPU-Design.md`)等を含むGPUランタイム関連プロジェクト(現時点で標準構成のREADME.md/CLAUDE.md/PORTING.mdは未整備)。 |
| open-directx | — | [aon-co-jp/open-directx](https://github.com/aon-co-jp/open-directx) | — (リポジトリ自体は存在するが空、README.md未整備) | — (未整備) | — (未整備) | ローカルドライブには実体(git clone)が無く、GitHub上に空リポジトリとして存在するのみを確認(`git ls-remote`で疎通確認、refなし)。DirectX関連プロジェクトと推測されるが、内容が無いため役割は未確認・推測で埋めない。 |
| open-mqa-dsd | AUDIO | [aon-co-jp/open-mqa-dsd](https://github.com/aon-co-jp/open-mqa-dsd) | [README](https://github.com/aon-co-jp/open-mqa-dsd/blob/main/README.md) | — | — | DSD(DSF/DSDIFF)読み込み・DSD⇄PCM変換・DoPパッキングのRust実装(`open-mqa`のDSD版相棒、MQA互換ではない)。2026-09-26に`open-av`の音声専用コンテナ実装(`container`モジュール、旧称open-audio)を統合。 |
| open-music-llm | AUDIO | [aon-co-jp/open-music-llm](https://github.com/aon-co-jp/open-music-llm) | [README](https://github.com/aon-co-jp/open-music-llm/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/open-music-llm/blob/main/CLAUDE.md) | MusicGen(実在するオーディオLLM、EnCodecトークン+Transformer次トークン予測)をRust+RPoemでラップしテキストから音楽・効果音を生成する。**2026-09-26時点は環境構築のみで実際の生成は未検証**、学習済み重みはCC-BY-NC 4.0(非商用限定)。 |
| open-easy-web | — | [aon-co-jp/open-easy-web](https://github.com/aon-co-jp/open-easy-web) | [README](https://github.com/aon-co-jp/open-easy-web/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-easy-web/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-easy-web/blob/main/CLAUDE.md) | 「第二のKUSANAGI」——アプリのアップロード後にIPアドレスで起動し、ドメイン登録・HTTPS化を簡単に自動適用できる運用ツール(Rust → WebAssembly、フレームワーク不使用)。 |
| open-LiveKit | — | [aon-co-jp/open-LiveKit](https://github.com/aon-co-jp/open-LiveKit) | [README](https://github.com/aon-co-jp/open-LiveKit/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-LiveKit/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-LiveKit/blob/main/CLAUDE.md) | [LiveKit](https://github.com/livekit/livekit)(Go+Pion製)のSFUアーキテクチャを参考に、コードは流用せず一からRust+`RPoem`で再実装するWebRTC SFU/リアルタイム通信基盤。`open-tv-chat`のリレーサーバーとして使う。**2026-09-26時点は設計ドキュメント段階、実装は未着手**。 |
| open-english | 学習 (Study) | [aon-co-jp/open-english](https://github.com/aon-co-jp/open-english) | [README](https://github.com/aon-co-jp/open-english/blob/master/README.md) | [PORTING](https://github.com/aon-co-jp/open-english/blob/master/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-english/blob/master/CLAUDE.md) | 【2026-10-21 `maid-cafe-english` へ改名・お引越し。この旧名のリポジトリも永久に残し、リンク・リリース・自動更新はそのまま使える】ブラウザ製の静的フロントエンド+`aruaru-llm`のローカル常駐サーバーを組み合わせた「PC/Android向け英会話AI学習アプリ」。オンライン/オフライン両対応のハイブリッド構成、Windows/Android用インストーラー・アンインストーラー・バージョン管理付き。 |
| maid-cafe-english | 学習 (Study) | [aon-co-jp/maid-cafe-english](https://github.com/aon-co-jp/maid-cafe-english) | [README](https://github.com/aon-co-jp/maid-cafe-english/blob/master/README.md) | [PORTING](https://github.com/aon-co-jp/maid-cafe-english/blob/master/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/maid-cafe-english/blob/master/CLAUDE.md) | `open-english` の改名・お引越し先(2026-10-21、同一の履歴・内容)。更新は新旧の両方で配布する(アプリは両方を確認して新しい版を採用)。経緯・多言語の告知は旧リポジトリの`RENAMED.md`。 |
| Java_to | 変換ツール | [aon-co-jp/Java_to](https://github.com/aon-co-jp/Java_to) | [README](https://github.com/aon-co-jp/Java_to/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/Java_to/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/Java_to/blob/main/CLAUDE.md) | Java(2000年頃〜2026年のSpring・JAX-RS・Servlet・Spark等)を自動判定し、FastAPI/MFastAPI/Poem/RPoemへ変換するRust製CLI(2026-11-18新設、Windows/Linux/macOSインストーラーのCI定義あり、CI未実行)。 |
| pl2pl | 変換ツール(構想) | [aon-co-jp/pl2pl](https://github.com/aon-co-jp/pl2pl) | [README](https://github.com/aon-co-jp/pl2pl/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/pl2pl/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/pl2pl/blob/main/CLAUDE.md) | COBOL_to・Java_to・2FastAPI・2MFastAPI・2Poemを共通の中間表現で統合・融合する構想リポジトリ(2026-11-18新設、設計は少しずつ記述、コードなし)。 |
| open-raid-z | — | [aon-co-jp/open-raid-z](https://github.com/aon-co-jp/open-raid-z) | [README](https://github.com/aon-co-jp/open-raid-z/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-raid-z/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-raid-z/blob/main/CLAUDE.md) | Rust製の実マウント可能なRAID-Z/Z2/Z3ストレージプール実装(ZFS「風」のCoW/チェックサム/スナップショット。ZFS自体・OpenZFSへの依存やオンディスク互換性はなし)。**エコシステム開発ルールの正本**リポジトリ。 |
| maid-cafe-se | — | [aon-co-jp/maid-cafe-se](https://github.com/aon-co-jp/maid-cafe-se) | [README](https://github.com/aon-co-jp/maid-cafe-se/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/maid-cafe-se/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/maid-cafe-se/blob/main/CLAUDE.md) | maid-cafeによる秘書サービス(secretary)。Androidスマホ向け。定型スケジュール(毎日/平日/土日祝/曜日/第N週/N週ごと)で著作権フリー音のアラーム、または入力文章をメイドカフェ風/低い男性声で読み上げ。Googleカレンダー連動+30分前予告。**2026-09-30時点でv0.4.0(Android署名つきAPK+Windows版インストーラー`maid-cafe-se-installer.exe`、`installer/`に入手・ビルド方法)。アプリ本体のRust(+RPoem)化を進行中**。 |
| open-tv-chat | — | [aon-co-jp/open-tv-chat](https://github.com/aon-co-jp/open-tv-chat) | [README](https://github.com/aon-co-jp/open-tv-chat/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-tv-chat/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-tv-chat/blob/main/CLAUDE.md) | Skype風「世界約130ヶ国語リアルタイム音声翻訳」対応のTV会議/ビデオチャットアプリ構想(Windows/macOS/Linux/Android/iPhone向け)。`open-web-server`+Rust/`RPoem`(Cosmo互換)構成。**2026-09-26時点は設計ドキュメント段階、実装は未着手**。 |
| open-vsc-claude | — | [aon-co-jp/open-vsc-claude](https://github.com/aon-co-jp/open-vsc-claude) | [README](https://github.com/aon-co-jp/open-vsc-claude/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-vsc-claude/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-vsc-claude/blob/main/CLAUDE.md) | 言語・フレームワーク(GraphQL+WunderGraph Cosmo/RPoem、TypeScript+Node+REST、または言葉で自由指定)を選んで生成コードをプレビューし、Claudeで改良して保存できるVS Code拡張。Web拡張(vscode.dev等)とブラウザデモ(PWA・オフライン可、[easy-web.tokyo/open-vps-claude](https://easy-web.tokyo/open-vps-claude/))付き、自動更新確認、README/CLAUDE/PORTINGは12言語。**2026-10-18時点でv0.1.1。Marketplace公開・Cosmo Router実起動・実機iOS/Androidは未了**。 |
| 360-speaker | — | [aon-co-jp/360-speaker](https://github.com/aon-co-jp/360-speaker) | [README](https://github.com/aon-co-jp/360-speaker/blob/main/README.md) | — | — | 360度全方位5WAYトールボーイスピーカー(1〜5WAY・通常/スーパーツィーター/サブウーファーの3版、アンプ内蔵またはアンプ無し+別売プリ)の設計案・調査・製品比較と、Rust→WASMのWebシミュレーター(指向性・T/S箱設計・ポート・壁材・ボリューム方式別コスト)。受動ネットワーク設計図(PDF/JPG)付き。公開: [easy-web.tokyo/360-speaker](https://easy-web.tokyo/360-speaker/)。**2026-10-25時点で設計初版。実機試作・実測は未了、コストは推定値**。 |
| version-control | — | [aon-co-jp/version-control](https://github.com/aon-co-jp/version-control) | [README](https://github.com/aon-co-jp/version-control/blob/main/README.md) | — | — | 全リポジトリが最新のライブラリ(crates.io/npm/packagist)・クローンを使っているかを走査し、`open-cuda`/`aruaru-llm`/`open-cpu`/`open-directx`の自動保守で足りないものを、Claude向けの貼り付けメッセージにしてメールとLINE(Messaging API)で通知。依存の書き換え・`git pull`はしない。運用: [easy-web.tokyo/version-control](https://easy-web.tokyo/version-control/)、デモ: [/demo/](https://easy-web.tokyo/version-control/demo/)。**2026-10-26時点で初版・単体テスト・画面表示・VPS配置を確認、メール/LINE送信は未確認(宛先・トークン未設定)、VPSには配置済み**。 |
| open-web-server | — | [aon-co-jp/open-web-server](https://github.com/aon-co-jp/open-web-server) | [README](https://github.com/aon-co-jp/open-web-server/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-web-server/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-web-server/blob/main/CLAUDE.md) | Rust + tokio/hyper自前実装のWebサーバー — 課金アイテム・金融データを「消失させない」ために設計。`open-runo`・`aruaru-db`と4層防御通信で連携するミッションクリティカル向け。**2026-11-18**: 管理2FA統合は`main`・本番反映済み、`loopback`切替は本人のOTP+TOTPログイン確認待ち(再開用メッセージは`PORTING.md`末尾、日英)。 |
| realdata.pro | — | [aon-co-jp/realdata.pro](https://github.com/aon-co-jp/realdata.pro) | [README](https://github.com/aon-co-jp/realdata.pro/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/realdata.pro/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/realdata.pro/blob/main/CLAUDE.md) | SAS Viyaを参考にした、誰でも使えるRust製オープンソースのデータ分析プラットフォーム(旧名rs-real-data)。open-cuda・RPoem・open-web-server・aruaru-llm等のエコシステム上に構築し、CSV・検索ワード(Google/YouTube/GitHub)・URLからの取り込み、クレンジング・集計・グラフ・重回帰、AIによる多言語説明を提供する。公開予定ドメインはrealdata.pro。 |
| webeditor-sftp | — | [aon-co-jp/webeditor-sftp](https://github.com/aon-co-jp/webeditor-sftp) | [README](https://github.com/aon-co-jp/webeditor-sftp/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/webeditor-sftp/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/webeditor-sftp/blob/main/CLAUDE.md) | ブログ感覚のWEB文章編集エディター(HTMLタグ非表示のブログモード/生コード編集のコーディングモード切替)と、秘密鍵・公開鍵を安全に受け渡しできるSFTPツールをハイブリッド統合したクロスプラットフォームアプリ(Tauri採用、Android/Windows/将来のiOS・macOS/Linux対応)。最初の実地検証対象は`audiocafe.tokyo`(Rust+Poem)。**2026-11-08時点: Rust製ブログ⇔HTML変換器・実SFTPサーバーへの通し試験(9件)・VS Code拡張(実VS Codeで自動試験6件)まで動作確認済み。未了=VSIX公開・Android・iOS/macOS**。 |
| rs-to-readme | — | [aon-co-jp/rs-to-readme](https://github.com/aon-co-jp/rs-to-readme) | [README](https://github.com/aon-co-jp/rs-to-readme/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/rs-to-readme/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/rs-to-readme/blob/main/CLAUDE.md) | Rustクレートの`Cargo.toml`メタデータからREADME.mdを自動生成するCLIツール([crates.io](https://crates.io/crates/rs-to-readme)公開)。 |
| RS-JSON | — | [aon-co-jp/RS-JSON](https://github.com/aon-co-jp/RS-JSON) | [README](https://github.com/aon-co-jp/RS-JSON/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RS-JSON/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RS-JSON/blob/main/CLAUDE.md) | RustのJSON処理ライブラリ。寛容モード(JSON5風)・厳密モード・部分抽出に加え、信頼できない入力向けの安全モード`parse_secure`(サイズ・深さ上限、重複キー拒否)と、速い値の型で読む`parse_secure_sonic`(`fast`機能、実測で`serde_json`の約2.4倍速い)を提供。旧`sonic-rs`(評価記録)を統合済み。型付き読み書き`fast::from_str`等と、RS-JSON<->JSON変換(最大約7倍速い)も提供。 |
| rs-dpiAwareness | — | [aon-co-jp/rs-dpiAwareness](https://github.com/aon-co-jp/rs-dpiAwareness) | [README](https://github.com/aon-co-jp/rs-dpiAwareness/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/rs-dpiAwareness/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/rs-dpiAwareness/blob/main/CLAUDE.md) | WindowsのDPI認識(PerMonitorV2)を依存ゼロのRustで扱う小さなクレート+診断CLI(段階的な代替つきの`init()`、モニターごとのDPI、`WM_DPICHANGED`、マニフェストの生成・埋め込み・読み出し)。Microsoftの公開仕様へのリスペクト版で、Microsoftとは無関係。実機(Windows 11・4K 200%)で確認済み、複数モニター間の移動は未確認。 |
| open-mirror | — | [aon-co-jp/open-mirror](https://github.com/aon-co-jp/open-mirror) | [README](https://github.com/aon-co-jp/open-mirror/blob/main/README.md) | — | — | 必要なものだけを選んでバックアップ・ミラーするツール。**稼働中**: GitHubの公開リポジトリを毎日GitLabへ一方向ミラー(GitHub Actions、公開リポジトリなので無料)と、VPSの厳選バックアップ(`deploy/`)。予定(未実装): PC・スマホ・タブレット等からの自動バックアップ、保存先の選択、厳選リスト、暗号化。紹介・デモは [easy-web.tokyo/open-mirror](https://easy-web.tokyo/open-mirror)。 |
| vps-backup | — | [aon-co-jp/vps-backup](https://github.com/aon-co-jp/vps-backup) | [README](https://github.com/aon-co-jp/vps-backup/blob/main/README.md) | — | — | VPSの厳選バックアップ(秘密情報・個人情報を除いた設定とDB構造のみ、最新1つ)。`open-mirror`の`deploy/vps-curated-backup.sh`が毎日自動生成。暗号化が要るものは手元に別置き。 |
| open-fudousan | — | [aon-co-jp/open-fudousan](https://github.com/aon-co-jp/open-fudousan) | [README](https://github.com/aon-co-jp/open-fudousan/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-fudousan/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-fudousan/blob/main/CLAUDE.md) | 土地・物件検索API(ダミーデータのみ、`limit`/`offset`対応)と`open-cg-cad`向けのエクスポート。v0.1.0。aruaru-db永続化・認証は未着手。 |
| open-cg-cad | — | [aon-co-jp/open-cg-cad](https://github.com/aon-co-jp/open-cg-cad) | [README](https://github.com/aon-co-jp/open-cg-cad/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-cg-cad/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-cg-cad/blob/main/CLAUDE.md) | 建築・住宅向けのAI支援3D CAD(建築基準・構造・施工方法の判断を支える**下書き用の補助ツール**、有資格者の確認の代わりではない)。v0.1.0、ビルドには兄弟リポジトリが必要。 |
| runo.tokyo | — | [aon-co-jp/runo.tokyo](https://github.com/aon-co-jp/runo.tokyo) | [README](https://github.com/aon-co-jp/runo.tokyo/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/runo.tokyo/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/runo.tokyo/blob/main/CLAUDE.md) | 東京都西部の暮らし・テレワークとopen-runo/open-aruaruエコシステムの入口となるWebサイト(Poem製)。v0.1.0。桧原村公式URL・ドローン動画は未提供のため準備中。 |
| RS-Guard | — | [aon-co-jp/RS-Guard](https://github.com/aon-co-jp/RS-Guard) | [README](https://github.com/aon-co-jp/RS-Guard/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/RS-Guard/blob/main/CLAUDE.md) | サプライチェーン(依存・スクリプト)のマルウェアパターンを事前スキャンするツール+任意でClamAV連携(Windows/Linux)。v0.1.0。Android版は未着手。 |
| RS-Sync | — | [aon-co-jp/RS-Sync](https://github.com/aon-co-jp/RS-Sync) | [README](https://github.com/aon-co-jp/RS-Sync/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RS-Sync/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RS-Sync/blob/main/CLAUDE.md) | GitHub/RS-Git/Gitea/Gitbucketなどの間でGitリポジトリやフォルダを同期・バックアップするツール(MVP)。`docs/github-actions-backup/`に、GitHub Actionsだけで自動バックアップするスクリプトと日英の使い方。 |
| runo-scanner | — | [aon-co-jp/runo-scanner](https://github.com/aon-co-jp/runo-scanner) | [README](https://github.com/aon-co-jp/runo-scanner/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/runo-scanner/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/runo-scanner/blob/main/CLAUDE.md) | ディレクトリ配下のプロジェクト(リポジトリ/ドメイン名のフォルダ)を列挙するRust製CLI(更新日時の差分キャッシュ付き)。v0.1.0。 |
| RS-BootStrap | — | [aon-co-jp/RS-BootStrap](https://github.com/aon-co-jp/RS-BootStrap) | [README](https://github.com/aon-co-jp/RS-BootStrap/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RS-BootStrap/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RS-BootStrap/blob/main/CLAUDE.md) | Bootstrap相当のグリッド+button/card/navbarのクラス名→CSS宣言変換(RS-CSS/rcss3上、26テスト)。ライブラリ。対話コンポーネント・実flexbox計算は未着手。 |
| sample-mario | — | [aon-co-jp/sample-mario](https://github.com/aon-co-jp/sample-mario) | [README](https://github.com/aon-co-jp/sample-mario/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/sample-mario/blob/main/CLAUDE.md) | マリオ風2Dプラットフォーマーの試作(Phase 0)。`open-directx`のスプライト経路を再利用。既存作品とは無関係。v0.1.0。 |
| sample-harrier | — | [aon-co-jp/sample-harrier](https://github.com/aon-co-jp/sample-harrier) | [README](https://github.com/aon-co-jp/sample-harrier/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/sample-harrier/blob/main/CLAUDE.md) | スペースハリアー風の擬似3Dスケーリングの試作(Phase 0)。`open-directx`を再利用。既存作品とは無関係。v0.1.0。 |
| sample-maid | — | [aon-co-jp/sample-maid](https://github.com/aon-co-jp/sample-maid) | [README](https://github.com/aon-co-jp/sample-maid/blob/main/README.md) | — | [CLAUDE.md](https://github.com/aon-co-jp/sample-maid/blob/main/CLAUDE.md) | 魔法少女メイドカフェの3Dゲームの試作(Phase 0、2Dプレースホルダー)。`open-directx`を再利用。既存作品とは無関係。v0.1.0。 |
| **RUNO**(このリポジトリ、旧称: open-aruaru-runo-iLumi → aon) | — | [aon-co-jp/RUNO](https://github.com/aon-co-jp/RUNO) | [README](https://github.com/aon-co-jp/RUNO/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RUNO/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RUNO/blob/main/CLAUDE.md) | このエコシステム全体の「プロジェクトシリーズ索引」を担うメタリポジトリ。個別のコード実装は持たない。 |

> 📝 **正直な開示**: 上表はローカル作業ドライブ(`F:\runo`)配下に実在し、
> `.git/config`のリモートURLで`aon-co-jp`上の存在を確認できた
> プロジェクトのみを掲載しています。`poem-cosmo-tauri`のようにドキュメント
> 上は言及されるものの本ドライブ上にローカルclone・実体が確認できなかった
> プロジェクトは、確認が取れ次第この表へ追加します。VPS(conoha)上の実体に
> ついてはこの索引では未追跡です。

## Overview (English)

This repository is a **meta index for the entire `aon-co-jp` project
ecosystem**, rooted at the local working drive `F:\runo`. It holds no
implementation code of its own — its sole purpose is to provide a single
place listing, for every sibling project actually present as a Git
repository under `aon-co-jp`, its README, PORTING.md (if any), development
policy document (`CLAUDE.md`), and a short, source-based summary of its
role. See the table above (labels in Japanese, links work regardless of
language).

The same content is also served as a live, 13-language web page with
live GitHub API lookups from
[`aruaru-tokyo`](https://github.com/aon-co-jp/aruaru-tokyo) at
`/open-aruaru-runo-iLumi` (alias: `/open-aruaru-runo`).

## GitHub organization

🏢 https://github.com/aon-co-jp

## 引き継ぎ(2026-10-14)
別アカウントで作業を続けるための引き継ぎは [`PORTING.md`](PORTING.md) の「アカウント引っ越しのための引き継ぎ」を参照(秘密の値は書いていない)。

## Hand-off (2026-10-14)
For continuing the work on another account, see "Hand-off for moving to another account" in [`PORTING.md`](PORTING.md) (no secret values are written there).

## 個人情報の扱い(2026-10-16)
公開リポジトリのコミットの作者は匿名(`aon-co-jp`)です。第三者(他の開発者)の作者表示は、本人が公開したものとして残しています。詳細・引き継ぎは [`PORTING.md`](PORTING.md) の「公開リポジトリの個人情報の取り除き」を参照してください。

## Privacy (2026-10-16)
Commit authors in the public repositories are anonymous (`aon-co-jp`). Other developers' attribution is kept because they published it themselves. For details and the hand-off, see "Removing personal information from public repositories" in [`PORTING.md`](PORTING.md).

---

作者 / Author: 石 塚 正 浩（MASAHIRO ISHIZUKA） (https://github.com/aon-co-jp)

> **再開用 / Resume (2026-11-15)**: REST全廃の本番確認・反映の到達点と貼り付け用の再開用メッセージ(日英)は [`PORTING.md`](PORTING.md) 末尾「2026-11-15 別アカウントでの再開用メモ(REST全廃の本番確認・反映…)」。 / Production verification status and the paste-ready resume message (JA/EN) are at the end of [`PORTING.md`](PORTING.md).

> **再開用 / Resume (2026-11-17)**: open-cosmo・RPoem・aruaru-db のREST全廃の仕上げ(`/internal/db/mutate`→`Admin/DbMutate`)の到達点と貼り付け用の再開用メッセージ(日英)は [`PORTING.md`](PORTING.md) 末尾「2026-11-17 別アカウントでの再開用メモ(open-cosmo・RPoem・aruaru-db …)」。 / Status and the paste-ready resume message (JA/EN) for finishing REST abolition in open-cosmo, RPoem and aruaru-db are at the end of [`PORTING.md`](PORTING.md).

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
- **実施状況(origin 基準の静的な目安)**: REST風ルート 509(11-04)→481(11-05)→**318(11-06)**。移行済み: open-english・aruaru-search・aruaru-llm・open-web-server・RS-Sync。ほぼ移行: aruaru-db(残8)。作業中: open-cosmo(残22)、RPoem(23、第1段階)。**2026-11-15 追記**: aruaru-db・open-cosmoは自前RESTが0本(例外のみ)、aruaru-dbは本番反映・管理画面のブラウザ確認済み(再開用メッセージは`PORTING.md`末尾、日英)。
- **未移行**: RS-EC 28 / RS-Blog 22 / aruaru.tokyo 17 / aruaru-IME 14 / aon.tokyo 13 / backup-to-discord-by-github 11 ほか小規模。**判定済み**: open-gitea・open-redmine は自前で Connect 移行済み・本番反映済み(2026-11-08、open-giteaの`/`が404の件は未了)。**例外か自前かの判定待ち**: ows-base・ows-stream(管理APIは自前なら移行)。
- **進め方**: 各リポジトリで 調査 → 分類(移す/例外/ブラウザGET) → 開発 → TEST → 記録(README/CLAUDE/PORTING/POLICY) → 本番反映。同時に動かす担当は最大2つ。例外は理由と規格URLつきで `version-control` の台帳へ。
- **正直な注意**: この節は記録であり、全リポジトリの完了を意味しない。各リポジトリへの同内容の追記は、担当セッションがそのリポジトリを移行する際に行う。本番反映済みと確認できたのは open-english(直接確認)と RS-Sync(担当報告)のみ。

### English
- **Decision (2026-11-04, user)**: abolish REST across all aon-co-jp repositories; move to Connect (browser/`curl`) and gRPC / gRPC-web (service-to-service). Policy source: `API-POLICY.md`; shared instructions: `API-MIGRATION-BRIEF.md`; remaining list: `API-REST-REMAINING-20261106.md`.
- **Status (static estimate, origin-based)**: REST-like routes 509 (11-04) → 481 (11-05) → **318 (11-06)**. Migrated: open-english, aruaru-search, aruaru-llm, open-web-server, RS-Sync. Nearly: aruaru-db (8 left). In progress: open-cosmo (22), RPoem (23, stage 1). **2026-11-15 update**: aruaru-db and open-cosmo have 0 own REST routes (exceptions only); aruaru-db is deployed and its admin UI was checked in a browser (resume message at the end of `PORTING.md`, JA/EN).
- **Not migrated**: RS-EC 28, RS-Blog 22, aruaru.tokyo 17, aruaru-IME 14, aon.tokyo 13, backup-to-discord-by-github 11, and small ones. **Decided**: open-gitea and open-redmine are own APIs, migrated to Connect and deployed (2026-11-08; open-gitea `/` returning 404 is open). **Exception-or-own undecided**: ows-base, ows-stream.
- **Process**: per repository: survey → classify → build → test → record (README/CLAUDE/PORTING/POLICY) → deploy. At most two assignees at a time. Exceptions go to the `version-control` ledger with reason and standard URL.
- **Caveat**: this is a record, not a claim that every repository is done; each repository's own docs are updated by its assignee when it is migrated. Production deployment is confirmed only for open-english and RS-Sync.


## 再開用メッセージ / Resume message (2026-11-15)

**追記 / Addendum**: Android同梱バイナリ(`open-english` v0.8.18)の再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 追記: Android同梱バイナリ」(日英)。/ The resume message for the Android bundled binaries (`open-english` v0.8.18) is at the end of [`PORTING.md`](PORTING.md) ("2026-11-15 追記").

**日本語**: 別のアカウントで再開するときは、[`PORTING.md`](PORTING.md)末尾の「2026-11-15 再開用メッセージ」と「2026-11-15 別アカウントでの再開用メモ」をそのまま貼り付ける。再開するリポジトリは`runo`(本リポジトリ)・`version-control`・`aruaru-search`・`aruaru-llm`(別件は`2FastAPI`・`2FastAPI-VSC`・`RMojo`)。本リポジトリは索引であり、コード実装は持たない。

**English**: To resume on another account, paste "2026-11-15 再開用メッセージ" and "2026-11-15 別アカウントでの再開用メモ" from the end of [`PORTING.md`](PORTING.md) as they are. Repositories to resume: `runo` (this one), `version-control`, `aruaru-search`, `aruaru-llm` (the other thread: `2FastAPI`, `2FastAPI-VSC`, `RMojo`). This repository is an index and holds no implementation code.

**追記 / Addendum (2026-11-17)**: 各担当の最新報告のまとめと貼り付け用の再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-17 到達点のまとめと再開用メッセージ」(日英)。再開するリポジトリ: `open-raid-z-installer`・`RPoem`・`open-easy-web`・`aruaru-IME`・`open-gitea`・`open-bar`・`version-control`。/ The latest reports and a paste-ready resume message are at the end of [`PORTING.md`](PORTING.md) ("2026-11-17 到達点のまとめと再開用メッセージ"). Repositories to resume: `open-raid-z-installer`, `RPoem`, `open-easy-web`, `aruaru-IME`, `open-gitea`, `open-bar`, `version-control`.

**追記 / Addendum (2026-11-15, open-bar・version-control・installer)**: open-bar・version-control・`open-raid-z-installer`の通し試験・RPoemゲートウェイの再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 追記: open-bar・version-control・…」(日英)。再開するリポジトリ: `open-raid-z-installer`・`aruaru-llm`(参照: `open-bar`・`version-control`・`open-web-server`・`RPoem`・`aruaru-IME`)。/ The resume message for open-bar, version-control, the `open-raid-z-installer` end-to-end test and the RPoem gateway is at the end of [`PORTING.md`](PORTING.md). Repositories to resume: `open-raid-z-installer`, `aruaru-llm` (see also `open-bar`, `version-control`, `open-web-server`, `RPoem`, `aruaru-IME`).

**2026-11-15 追記 / Addendum**: Android実機確認(REST全廃後)の結果と再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 Android実機確認」(日英)。再開するリポジトリ: `aruaru-IME`・`open-redmine`(`android/`)・`maid-cafe-english`(旧`open-english`)・`open-media`・`runo`(本リポジトリ、索引のみ)。 / Results of the post-REST Android device verification and the resume message are at the end of [`PORTING.md`](PORTING.md) ("2026-11-15 Android実機確認", JA/EN). Repositories to resume: `aruaru-IME`, `open-redmine` (`android/`), `maid-cafe-english` (formerly `open-english`), `open-media`, `runo` (this index repo).

2026-11-15: appserver系REST10本(RPoem・open-cosmo)とopen-raid-z管理UIをConnect化(push済み、VPS未反映)。再開するリポジトリ: `RPoem`・`open-cosmo`・`open-raid-z`・`open-easy-web`・`runo`。再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 再開用メモ: appserver系REST・open-raid-z管理UIのConnect化」(日英)。 / 2026-11-15: the 10 appserver REST routes (RPoem, open-cosmo) and the open-raid-z admin UI are on Connect (pushed, not yet deployed to the VPS). Repositories to resume: `RPoem`, `open-cosmo`, `open-raid-z`, `open-easy-web`, `runo`. The resume message is at the end of [`PORTING.md`](PORTING.md) ("2026-11-15 再開用メモ: appserver系REST・open-raid-z管理UIのConnect化", JA/EN).

**REST全廃の仕上げ(ストリーミング・bdg・open-cg-cad・e-gov)の再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 別アカウントでの再開用メモ(REST全廃の仕上げ…)」(日英)。再開するリポジトリ: `RPoem`・`backup-to-discord-by-github`・`open-cg-cad`・`e-gov`(新規clone)・`runo`(本リポジトリ、索引のみ)。** / The resume message for the REST-abolition finish (streaming, bdg, open-cg-cad, e-gov) is at the end of [`PORTING.md`](PORTING.md) ("2026-11-15 別アカウントでの再開用メモ(REST全廃の仕上げ…)", JA/EN). Repositories to resume: `RPoem`, `backup-to-discord-by-github`, `open-cg-cad`, `e-gov` (fresh clone) and `runo` (this index repo).


## 依存更新の状況(2026-11-17) / Dependency update status (2026-11-17)

**日本語**: version-controlの通知14件のうち、脆弱性(open-gitea・open-redmine・aruaru-llm)とメジャー更新(RS-Blog・RS-EC・audiocafe-tokyo-rust)は対応済みでVPS反映・再起動まで確認した。保留はaruaru-IMEの`windows-core`(`windows`クレートの新版待ち)。再開するときは[`PORTING.md`](PORTING.md)末尾「2026-11-17 再開用メッセージ(依存更新)」を貼り付ける。本リポジトリは索引であり、コード実装は持たない。

**English**: Of the 14 version-control items, the vulnerabilities (open-gitea, open-redmine, aruaru-llm) and the major updates (RS-Blog, RS-EC, audiocafe-tokyo-rust) are done, deployed to the VPS and restarted. On hold: `windows-core` in aruaru-IME (waiting for a newer `windows` crate). To resume, paste "2026-11-17 再開用メッセージ(依存更新)" from the end of [`PORTING.md`](PORTING.md). This repository is an index and holds no implementation code.

## 引き継ぎ・再開(2026-11-15 RS-Sync依存更新と検証調査) / Hand-off (RS-Sync dependency update and verification research)

**日本語**: RS-Syncの依存更新とテスト失敗原因の調査(日英)を完了。未了(稀に落ちる結合テストの原因特定、Android実機確認)と再開用メッセージは[`PORTING.md`](PORTING.md)末尾と`F:\RS-Sync\PORTING.md`末尾。

**English**: The RS-Sync dependency update and the research on why tests fail (English/Japanese) are done. Open items (root cause of the flaky integration test, Android device check) and the resume messages are at the end of [`PORTING.md`](PORTING.md) and `F:\RS-Sync\PORTING.md`.

**追記 / Addendum (2026-11-17, aruaru-db)**: aruaru-dbのWeb管理画面の白画面4件を修正しブラウザで全画面を確認(`aca3fca`)、`admin.rs`の警告を0に(`9a390b8`)。再開用メッセージは[`PORTING.md`](PORTING.md)末尾(日英)。再開するリポジトリ: `aruaru-db`・`open-cosmo`。/ Fixed four white-screen bugs in the aruaru-db admin web app and verified every page in a browser (`aca3fca`); `admin.rs` now has 0 warnings (`9a390b8`). Resume message at the end of [`PORTING.md`](PORTING.md) (JA/EN). Repositories to resume: `aruaru-db`, `open-cosmo`.

> 2026-11-17: RPoemゲートウェイ(appserver系Connect化)をVPSへ反映済み。再開用メッセージは[`PORTING.md`](PORTING.md)末尾(日英)。 / RPoem gateway deployed to the VPS; resume message at the end of PORTING.md (JA/EN).

> **再開用 / Resume (2026-11-17, RPoemゲートウェイのDB化)**: 到達点・未了・貼り付け用メッセージ(日英)は [`PORTING.md`](PORTING.md) 末尾「2026-11-17 追記: RPoemゲートウェイのDB化…」。 / Status, open items and the paste-ready message (JA/EN) are at the end of [`PORTING.md`](PORTING.md).

2026-11-15: Ledger→RPoemゲートウェイの接続を本番で通し確認(`Admin/DbMutate`の実書き込み・冪等)。再開するリポジトリ: `runo`・`RPoem`・`open-web-server`・`open-cosmo`・`RS-EC`・`RS-Blog`・`aruaru-IME`。再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 再開用メモ: Ledger→RPoem接続の通し確認と残り」(日英)。 / 2026-11-15: the Ledger→RPoem gateway wiring was verified in production (a real `Admin/DbMutate` write, idempotent). Repositories to resume: `runo`, `RPoem`, `open-web-server`, `open-cosmo`, `RS-EC`, `RS-Blog`, `aruaru-IME`. The resume message is at the end of [`PORTING.md`](PORTING.md) ("2026-11-15 再開用メモ: Ledger→RPoem接続の通し確認と残り", JA/EN).

2026-11-15: easy-web.tokyo に9製品の紹介・ダウンロードページを公開(`aruaru-llm`・`aruaru-IME`・`open-easy-web`・`RS-EC`・`RS-Blog`・`RS-Ops`・`open-cosmo`・`RS-Red`は`/<repo>/`、`open-gitea`は`/open-gitea/intro/`)。再開用メッセージは[`PORTING.md`](PORTING.md)末尾「2026-11-15 再開用メモ: easy-web.tokyo の製品紹介ページ」(日英)。 / 2026-11-15: nine product intro/download pages are live on easy-web.tokyo (`open-gitea` at `/open-gitea/intro/`). The resume message is at the end of [`PORTING.md`](PORTING.md) (JA/EN).

2026-11-17: aruaru-IME v0.2.23 のインストーラーを管理者権限で入れ直した(実入力・常駐エンジンの確認と最新版かの確認が未了)。再開するリポジトリは`aruaru-IME`・`runo`。再開用メッセージは[`PORTING.md`](PORTING.md)末尾(日英)。 / 2026-11-17: the aruaru-IME v0.2.23 installer was re-installed with admin rights (resident engine, real typing and whether it is the latest version are unverified). Repos to resume: `aruaru-IME`, `runo`. The resume message is at the end of [`PORTING.md`](PORTING.md) (JA/EN).

## 再開用メッセージ / Resume message (2026-11-17, VPSクローンの最新化 / VPS clone refresh)

**日本語**: version-controlの通知(RUNO・aon.tokyo・backup-to-discord-by-github・rs-syncのクローン遅れ)に対応し、VPSの4クローンを最新化・4サービスを再起動済み(全active)。未了=bdgのGitHub Webhook実受信の確認、VPS bdgの`Cargo.lock`未コミット差分の扱い。再開するリポジトリは`F:
uno`と、VPSの`backup-to-discord-by-github`・`rs-sync`・`aon.tokyo`。**貼り付け用メッセージと詳細は[`PORTING.md`](PORTING.md)末尾「version-control通知の対応」(日英)**。`git pull`はせず`git fetch`+`merge --ff-only`。

**English**: The version-control clone-lag notice (RUNO, aon.tokyo, backup-to-discord-by-github, rs-sync) was handled: four VPS clones refreshed and four services restarted (all active). Open: a real GitHub webhook into bdg and the uncommitted `Cargo.lock` diff on the VPS bdg clone. Repos to resume: `F:
uno` and, on the VPS, `backup-to-discord-by-github`, `rs-sync`, `aon.tokyo`. **The paste-ready message and details are at the end of [`PORTING.md`](PORTING.md) ("Resume memo: clone-lag notice", JA/EN)**. No `git pull`; use `git fetch` + `merge --ff-only`.

**再開用メッセージ(2026-11-17 統合版)**: [`PORTING.md`](PORTING.md)末尾「2026-11-17 全セッション統合の再開用メモ」(日英)。 *Consolidated resume message: end of PORTING.md (JA/EN).*

## 2026-11-18 Cloud9からの引っ越しセッションの記録 / Session record (moved from the Cloud9 account)
**日本語**
- **開発の場所のルール**: プログラムの開発・TEST・DEBUGはこのローカルPC(WSL含む)で行う。VPSは配備(バックアップ付き差し替え)と実測確認だけに使い、負荷をかける試験やデバッグはしない(ユーザー指示)。
- **aruaru-llm / RPoem: OCRフォント配信のConnect化の完了**。`GET /v1/ocr/fonts/:name` を廃止し `POST /aruaru_llm.v1.Llm/OcrFont`(JSON `{name}` → `{name, content_type, sha256, data_base64}`)へ移した。本番VPSは別セッションで反映済みで、手元ビルドとSHA256が一致、`OcrFont` 200・不明名404・旧経路404・エラーログ0を実測した。aruaru-llm・RPoemとも`main`反映済み、version-controlの例外追記は`3863140`で取り消し済み。
- **pdf-r2l-rs v1.3.2(告知とバグ修正)**: 古いクライアント(v1.3.1以前、`open-runo-pdf-ocr` rev `3b644db`)は新サーバーからフォントを取得できなくなるため、README/CLAUDE/PORTINGに日英で告知を追記した(`c346c8b`)。rev更新後に実フォント取得を試すと、`OcrFont`の応答(約13MB)が`ureq` 3の既定上限10MBを超えて失敗する不具合を発見。RPoem `bb3af78`で上限を256MBへ引き上げ(`open-runo-pdf-ocr`の`client.rs`)、revを更新して、本番から`NotoSansJP-VF.ttf`(9.59MB、sha256照合つき)の取得に成功した。v1.3.2をタグ公開し、リリースCIは全ジョブ成功(exe・setup・deb・tar.gz・apk)。macOS向けの添付はない。
- **RS-Sync 本番反映**: `88a90b6`(ログイン方式otp/otp_qr/qrとQR確認ログイン)をWSLでビルドし(glibc 2.39)、VPSの`rs-sync`と`rs-sync-demo`を、バックアップ(`rs-sync.before-login-20261118`)と失敗時の自動ロールバック付きで入れ替えた。`GetLoginMode`200・認証なし`ListAccounts`401(デモは200)・旧`/api/accounts`404・`/healthz`200・`/qr-confirm.html`200・エラーログ0を実測。未了=実スマホのQR撮影、実SMTPでの`otp_qr`通し、`login_mode`の永続化。**注意**: VPSの`rs-sync.service`にSMTPパスワードが平文の環境変数で書かれている(`EnvironmentFile=`+権限600への移設を推奨)。
- **aruaru-llm Generate遅延の調査(原因は未特定)**: 本番VPSで8トークンのGenerateが3回連続で150秒を超え、切断後も4コアが100%のまま計算が続き、`dispatch end`のログが25分以上出なかった。知識文脈(`Known facts`/ニュース)は最大3+3件で短く、プロンプト長は原因ではない。`idle_background_fold`は35秒ごとに動作。測定でVPSに負荷を積んだため、以後の再現・修正はローカルPCで行う。
- **maid-cafe-tokyo**: `aon-co-jp/maid-cafe-tokyo`(open-englishとrealdata.proの融合、運用先https://maid-cafe.tokyo)は既に存在する(新規作成は不要)。次の作業「質問に答えられないとき、GitHubのニュース・知識DBとaruaru-searchから類義語でも拾って答える補完」はこのリポジトリに入れる(未着手)。
- **未了(優先順)**: (1)Generate遅延の原因特定(WSLでローカル再現)と、要約が`llm_timeout_secs=45`に収まるかの確認、(2)答えられないときの補完(maid-cafe-tokyo)、(3)RS-Syncの実スマホQR・実SMTP試験、(4)VPSのaruaru-llmに積み上がった計算の解消(再起動するかはユーザー判断)。

**English**
- **Where to develop**: development, TEST and DEBUG happen on this local PC (including WSL). The VPS is used only for deployment (swap with a backup) and verification, never for load tests or debugging (user instruction).
- **aruaru-llm / RPoem: OCR font delivery moved to Connect (done)**. `GET /v1/ocr/fonts/:name` was removed and replaced by `POST /aruaru_llm.v1.Llm/OcrFont` (JSON `{name}` -> `{name, content_type, sha256, data_base64}`). Production had already been swapped by another session; its SHA256 matches the local build, and `OcrFont` 200, unknown name 404, old route 404 and zero error logs were measured. Both repos are on `main`, and the version-control exception entry was reverted (`3863140`).
- **pdf-r2l-rs v1.3.2 (notice and bug fix)**: old clients (v1.3.1 and earlier, `open-runo-pdf-ocr` rev `3b644db`) can no longer fetch fonts from the new server, so a bilingual notice was added to README/CLAUDE/PORTING (`c346c8b`). After bumping the rev, a real font fetch revealed that the ~13 MB `OcrFont` response exceeded `ureq` 3's default 10 MB body limit. RPoem `bb3af78` raises it to 256 MB (`client.rs` in `open-runo-pdf-ocr`); after the rev bump, `NotoSansJP-VF.ttf` (9.59 MB, sha256-verified) was fetched from production. v1.3.2 was tagged and all release CI jobs passed (exe, setup, deb, tar.gz, apk); there is no macOS asset.
- **RS-Sync production deploy**: `88a90b6` (login modes otp/otp_qr/qr and QR confirm login) was built in WSL (glibc 2.39) and swapped into `rs-sync` and `rs-sync-demo` on the VPS with a backup (`rs-sync.before-login-20261118`) and automatic rollback. Verified: `GetLoginMode` 200, unauthenticated `ListAccounts` 401 (200 on the demo), old `/api/accounts` 404, `/healthz` 200, `/qr-confirm.html` 200, no error logs. Open: a real phone-camera QR test, `otp_qr` with real SMTP, persisting `login_mode`. **Caution**: the VPS `rs-sync.service` holds the SMTP password as a plain environment variable (move it to `EnvironmentFile=` with mode 600).
- **aruaru-llm Generate slowness (cause not yet found)**: on the production VPS an 8-token Generate exceeded 150 s three times in a row; the four cores stayed at 100% after the clients disconnected and no `dispatch end` log appeared for over 25 minutes. The knowledge context (`Known facts` / news) is at most 3+3 items, so prompt length is not the cause. `idle_background_fold` runs every 35 s. The probing piled load onto the VPS, so reproduction and fixes now happen on the local PC.
- **maid-cafe-tokyo**: `aon-co-jp/maid-cafe-tokyo` (fusion of open-english and realdata.pro, served at https://maid-cafe.tokyo) already exists, so no new repository is needed. The next feature, answering with similar-word matches from the GitHub-stocked news / knowledge DB and aruaru-search when a question cannot be answered well, goes into that repository (not started).
- **Open (in priority order)**: (1) find the cause of the Generate slowness (reproduce in WSL) and check whether summaries fit `llm_timeout_secs=45`; (2) the answer-fallback feature (maid-cafe-tokyo); (3) real-phone QR and real-SMTP tests for RS-Sync; (4) clear the piled-up computation on the VPS aruaru-llm (restart is the user's call).

### 再開用メッセージ(2026-11-18、別アカウントでそのまま貼り付け) / Resume message
**日本語**: 前のセッションの続きです。開発・TEST・DEBUGはこのローカルPC(WSL含む)で行い、VPSは配備と実測確認だけに使ってください。`F:\runo\PORTING.md` 末尾「2026-11-18 Cloud9からの引っ越しセッションの記録」を読んでから再開します。完了済み=aruaru-llm OCRフォントのConnect化(本番・main反映・例外取り消し)、pdf-r2l-rs v1.3.2(告知とOcrFont応答上限の修正、RPoem `bb3af78`)、RS-Sync `88a90b6` の本番反映。未了(この順で): (1)aruaru-llm Generate遅延の原因特定をWSLのローカルで再現して行う(VPSで8トークンが150秒超・切断後も4コア100%、`dispatch end`が出ない。知識文脈は短く原因ではない)と、要約が`llm_timeout_secs=45`に収まるかの確認、(2)`aon-co-jp/maid-cafe-tokyo`(既存。open-englishとrealdata.proの融合、運用先https://maid-cafe.tokyo)に「質問に答えられないとき、GitHubのニュース・知識DBとaruaru-searchから類義語でも拾って答える補完」を実装、(3)RS-Syncの実スマホQR撮影・実SMTPでの`otp_qr`通し・`login_mode`永続化(`rs-sync.service`のSMTPパスワードの`EnvironmentFile=`移設も)、(4)VPSのaruaru-llmに積み上がった計算の解消(再起動はユーザーに確認してから)。決まり: 新しいRESTは作らない(Connectのみ)、秘密は表示しない、実機で確認してから完了と報告する、返答は日本語のみ、pushやタグは確認してから。
**English**: Continuing from the previous session. Develop, TEST and DEBUG on this local PC (including WSL); use the VPS only for deployment and verification. Read "2026-11-18 Cloud9からの引っ越しセッションの記録" at the end of `F:\runo\PORTING.md` first. Done: aruaru-llm OCR font delivery on Connect (production, main, exception reverted), pdf-r2l-rs v1.3.2 (notice and the OcrFont response-limit fix, RPoem `bb3af78`), RS-Sync `88a90b6` deployed. Open (in this order): (1) find the cause of the aruaru-llm Generate slowness by reproducing it locally in WSL (on the VPS 8 tokens took over 150 s, four cores stayed at 100% after disconnect, no `dispatch end`; the knowledge context is short and not the cause), then check whether summaries fit `llm_timeout_secs=45`; (2) in `aon-co-jp/maid-cafe-tokyo` (existing; fusion of open-english and realdata.pro, served at https://maid-cafe.tokyo) implement the answer fallback that draws on the GitHub-stocked news / knowledge DB and aruaru-search, including similar words, when a question cannot be answered well; (3) RS-Sync: a real phone-camera QR test, an `otp_qr` run with real SMTP, persisting `login_mode` (and move the SMTP password in `rs-sync.service` to `EnvironmentFile=`); (4) clear the piled-up computation on the VPS aruaru-llm (ask the user before restarting). Rules: no new REST (Connect only), never print secrets, verify on real systems before reporting done, reply in Japanese only, confirm before pushing or tagging.

## 2026-11-19 方針: Node.js・REST API を使わない / JSONはRS-JSONだけ(日本語)
- **やること**: Node.js と REST API をやめます。JSONは `RS-JSON` だけで読み書きし、ほかのJSON部品(`serde_json`・`nlohmann` など)と**二重に使いません**。
- **済んだこと**: `whisper.cpp` の fork(`aon-co-jp/whisper.cpp`)から Node.js アドオン `examples/addon.node` と専用CIを消しました。洗い出しの結果は [`NODEJS-REMAINING-20261119.md`](NODEJS-REMAINING-20261119.md)。
- **まだのこと**: (1)置き換えられるもの(`open-upstream-watch` の試験、`Reaxt/clients/js`、`2Poem` の例)、(2)JSONの二重使用の洗い出し、(3)Node.jsが必須のもの(VS Code拡張、Tauriの画面ビルド)は、やめてよいか本人の判断待ち、(4)`whisper.cpp` の `examples/server`(REST+nlohmann)。
- **VPS**: `whisper.cpp` のVPSのクローンは2コミット遅れのまま(未更新)。


### English (simple words, easy to read)
- **What we do**: We stop using Node.js and REST APIs. We read and write JSON with `RS-JSON` only. We do **not** use two JSON tools at the same time (for example `serde_json` or `nlohmann` together with RS-JSON).
- **What is done**: In our copy of `whisper.cpp` (`aon-co-jp/whisper.cpp`), we deleted the Node.js add-on `examples/addon.node` and the tests that only ran it. The full list is in [`NODEJS-REMAINING-20261119.md`](NODEJS-REMAINING-20261119.md).
- **What is not done yet**: (1) things we can replace now (the `open-upstream-watch` test, `Reaxt/clients/js`, the `2Poem` example); (2) finding places that use two JSON tools; (3) things that really need Node.js (VS Code extensions, Tauri screen builds) - we wait for the owner to decide; (4) `examples/server` in `whisper.cpp` (REST + nlohmann).
- **VPS**: the VPS copy of `whisper.cpp` is still 2 commits behind (not updated).

## 2026-11-19 大きなモデル対応の調査と分割重み対応 / Large-model research and sharded weights (10 languages)

### 日本語
- **結論**: 東芝のシミュレーテッド分岐(SB)は**組合せ最適化(イジング/QUBO)の高速解法**で、LLMの推論そのものを速める技術ではない。使えるとすれば「どのエキスパート/層をGPU・RAM・ディスクのどこへ置くか」の配置計画をQUBOにする案だが、**効果は未検証**。DeepSeekの「折り畳み」に当たる技術は特定できていない。候補はMLA(KVキャッシュの低ランク圧縮)、MoE、FP8(論文では学習用)。MLA・MoEの遅延読み込みは`open-cuda`の`deepseek_arch.rs`に実装済み。
- **実装済み(main)**: Qwen2.5の分割重み(`model.safetensors.index.json`+複数ファイル)の取得(`aruaru-llm`、単一ファイルが404のときだけ分割取得、ストリーム書き込み)と読み込み(`open-cuda-llm`)。モックと合成データのテスト成功。実在の3Bは2分割・6.17GBと確認。
- **未了**: 実3Bの読み込み実測(f32展開で約12GB+生6GB、空きRAM約15GBでは危険)、7B(約15GB)はf32では32GB機に入らず遅延読み込み/量子化が必要、SB配置案の試作、DeepSeekの指す技術の確認(**ユーザーに要確認**)、CPU速度の実測。

### English
- **Findings**: Toshiba's Simulated Bifurcation (SB) is a fast solver for **combinatorial optimization (Ising/QUBO)**; it does not speed up LLM inference itself. The only plausible use is planning where experts/layers live (GPU, RAM, disk) as a QUBO, which is **unproven**. We could not identify what "DeepSeek folding" means; candidates are MLA (low-rank KV-cache compression), MoE, and FP8 (training-side in the paper). MLA and lazy MoE loading already exist in `open-cuda`'s `deepseek_arch.rs`.
- **Done (main)**: sharded Qwen2.5 weights (`model.safetensors.index.json` plus several files): download in `aruaru-llm` (only when the single file returns 404, streamed to disk) and loading in `open-cuda-llm`. Mock and synthetic tests pass. The real 3B model is confirmed to be 2 shards, 6.17 GB.
- **Open**: a real 3B load measurement (f32 expansion is about 12 GB plus 6 GB raw; risky with about 15 GB free), 7B (about 15 GB) does not fit a 32 GB machine in f32 and needs lazy loading or quantization, a prototype of SB placement, confirming what DeepSeek technique is meant (**ask the user**), CPU speed measurements.

### 简体中文
- **结论**:东芝的模拟分岔(SB)是**组合优化(Ising/QUBO)的快速求解方法**,并不能直接加速大模型推理。唯一可能的用法是把专家/层放在GPU、内存、磁盘哪里的规划写成QUBO,**效果未验证**。"DeepSeek折叠"具体指什么尚未确定,候选有MLA(KV缓存低秩压缩)、MoE、FP8(论文中用于训练)。MLA与MoE延迟加载已在`open-cuda`的`deepseek_arch.rs`中实现。
- **已完成(main)**:支持分片权重(`model.safetensors.index.json`+多个文件)的下载(`aruaru-llm`,仅在单文件返回404时启用,流式写盘)与加载(`open-cuda-llm`);模拟与合成测试通过。真实3B为2个分片、6.17GB。
- **未完成**:真实3B加载实测、7B(约15GB)需延迟加载或量化、SB配置原型、向用户确认DeepSeek所指技术、CPU速度实测。

### 繁體中文
- **結論**:東芝的模擬分岔(SB)是**組合最佳化(Ising/QUBO)的快速求解法**,並不能直接加速大型模型推論。唯一可能的用途是把專家/層放在GPU、記憶體、磁碟何處的規劃寫成QUBO,**效果未驗證**。「DeepSeek摺疊」具體指什麼尚未確定,候選為MLA(KV快取低秩壓縮)、MoE、FP8(論文中用於訓練)。MLA與MoE延遲載入已在`open-cuda`的`deepseek_arch.rs`實作。
- **已完成(main)**:支援分片權重(`model.safetensors.index.json`+多個檔案)的下載(`aruaru-llm`,僅在單檔回傳404時啟用,串流寫入)與載入(`open-cuda-llm`);模擬與合成測試通過。真實3B為2個分片、6.17GB。
- **未完成**:真實3B載入實測、7B(約15GB)需延遲載入或量化、SB配置原型、向使用者確認DeepSeek所指技術、CPU速度實測。

### 한국어
- **결론**: 도시바의 시뮬레이티드 분기(SB)는 **조합 최적화(Ising/QUBO)의 빠른 풀이법**이며 LLM 추론 자체를 빠르게 하지는 않습니다. 전문가/레이어를 GPU·RAM·디스크 어디에 둘지의 배치 계획을 QUBO로 만드는 용도만 생각할 수 있고 **효과는 검증되지 않았습니다**. "DeepSeek 접기"가 무엇인지는 특정하지 못했으며 후보는 MLA(KV 캐시 저랭크 압축), MoE, FP8(논문에서는 학습용)입니다. MLA와 MoE 지연 로딩은 `open-cuda`의 `deepseek_arch.rs`에 이미 구현되어 있습니다.
- **완료(main)**: 분할 가중치(`model.safetensors.index.json`+여러 파일)의 다운로드(`aruaru-llm`, 단일 파일이 404일 때만, 스트리밍 저장)와 로딩(`open-cuda-llm`). 모의·합성 테스트 통과. 실제 3B는 2분할, 6.17GB.
- **미완료**: 실제 3B 로딩 측정, 7B(약 15GB)는 지연 로딩/양자화 필요, SB 배치 시제품, DeepSeek가 가리키는 기술 확인(사용자에게 질문 필요), CPU 속도 측정.

### Deutsch
- **Ergebnis**: Toshibas Simulated Bifurcation (SB) ist ein schneller Löser für **kombinatorische Optimierung (Ising/QUBO)** und beschleunigt die LLM-Inferenz selbst nicht. Denkbar ist nur, die Platzierung von Experten/Schichten (GPU, RAM, Festplatte) als QUBO zu planen; **die Wirkung ist ungeprüft**. Was mit „DeepSeek-Faltung“ gemeint ist, konnten wir nicht klären; Kandidaten sind MLA (Low-Rank-Kompression des KV-Caches), MoE und FP8 (im Paper fürs Training). MLA und verzögertes MoE-Laden gibt es bereits in `deepseek_arch.rs` von `open-cuda`.
- **Erledigt (main)**: geteilte Gewichte (`model.safetensors.index.json` plus mehrere Dateien): Download in `aruaru-llm` (nur wenn die Einzeldatei 404 liefert, gestreamt) und Laden in `open-cuda-llm`. Mock- und Synthetiktests bestehen. Das echte 3B-Modell hat 2 Teile, 6,17 GB.
- **Offen**: Messung mit echtem 3B, 7B (ca. 15 GB) braucht verzögertes Laden oder Quantisierung, SB-Prototyp, Klärung der gemeinten DeepSeek-Technik (Nutzer fragen), CPU-Geschwindigkeit.

### Français
- **Conclusion** : la bifurcation simulée (SB) de Toshiba est un solveur rapide d'**optimisation combinatoire (Ising/QUBO)** ; elle n'accélère pas l'inférence des LLM elle-même. Seul usage plausible : planifier le placement des experts/couches (GPU, RAM, disque) sous forme de QUBO, **non vérifié**. Nous n'avons pas pu identifier ce que désigne le « pliage DeepSeek » ; candidats : MLA (compression de rang faible du cache KV), MoE, FP8 (pour l'entraînement dans l'article). MLA et le chargement paresseux du MoE existent déjà dans `deepseek_arch.rs` d'`open-cuda`.
- **Fait (main)** : poids fragmentés (`model.safetensors.index.json` et plusieurs fichiers) : téléchargement dans `aruaru-llm` (seulement si le fichier unique renvoie 404, écriture en flux) et chargement dans `open-cuda-llm`. Tests simulés et synthétiques réussis. Le vrai 3B compte 2 fragments, 6,17 Go.
- **À faire** : mesure avec le vrai 3B, le 7B (≈15 Go) exige chargement paresseux ou quantification, prototype SB, confirmer la technique DeepSeek visée (demander à l'utilisateur), vitesse CPU.

### Español
- **Conclusión**: la bifurcación simulada (SB) de Toshiba es un solucionador rápido de **optimización combinatoria (Ising/QUBO)**; no acelera la inferencia del LLM en sí. Lo único plausible es planificar dónde colocar expertos/capas (GPU, RAM, disco) como QUBO, **sin verificar**. No pudimos identificar qué es el «plegado de DeepSeek»; candidatos: MLA (compresión de rango bajo de la caché KV), MoE y FP8 (en el artículo, para entrenamiento). MLA y la carga perezosa de MoE ya existen en `deepseek_arch.rs` de `open-cuda`.
- **Hecho (main)**: pesos fragmentados (`model.safetensors.index.json` y varios archivos): descarga en `aruaru-llm` (solo si el archivo único da 404, en flujo) y carga en `open-cuda-llm`. Pruebas simuladas y sintéticas correctas. El 3B real tiene 2 fragmentos, 6,17 GB.
- **Pendiente**: medir con el 3B real, el 7B (≈15 GB) requiere carga perezosa o cuantización, prototipo SB, confirmar qué técnica de DeepSeek se pretende (preguntar al usuario), velocidad en CPU.

### Português
- **Conclusão**: a bifurcação simulada (SB) da Toshiba é um solucionador rápido de **otimização combinatória (Ising/QUBO)**; ela não acelera a inferência do LLM em si. O único uso plausível é planejar onde colocar especialistas/camadas (GPU, RAM, disco) como QUBO, **não verificado**. Não conseguimos identificar o que é o «dobramento da DeepSeek»; candidatos: MLA (compressão de baixo posto do cache KV), MoE e FP8 (no artigo, para treino). MLA e o carregamento preguiçoso de MoE já existem em `deepseek_arch.rs` do `open-cuda`.
- **Feito (main)**: pesos fragmentados (`model.safetensors.index.json` e vários arquivos): download no `aruaru-llm` (só se o arquivo único retornar 404, em fluxo) e carregamento no `open-cuda-llm`. Testes simulados e sintéticos passam. O 3B real tem 2 fragmentos, 6,17 GB.
- **Pendente**: medição com o 3B real, o 7B (≈15 GB) exige carregamento preguiçoso ou quantização, protótipo SB, confirmar a técnica da DeepSeek pretendida (perguntar ao usuário), velocidade em CPU.

### Русский
- **Вывод**: имитация бифуркации (SB) Toshiba — быстрый решатель **комбинаторной оптимизации (Ising/QUBO)**, она не ускоряет сам вывод LLM. Единственное правдоподобное применение — планирование размещения экспертов/слоёв (GPU, ОЗУ, диск) в виде QUBO, **не проверено**. Что такое «складывание DeepSeek», выяснить не удалось; кандидаты: MLA (низкоранговое сжатие KV-кэша), MoE и FP8 (в статье — для обучения). MLA и отложенная загрузка MoE уже есть в `deepseek_arch.rs` проекта `open-cuda`.
- **Готово (main)**: разделённые веса (`model.safetensors.index.json` и несколько файлов): загрузка в `aruaru-llm` (только если одиночный файл даёт 404, потоковая запись) и чтение в `open-cuda-llm`. Тесты на имитации и синтетике проходят. Настоящая 3B — 2 части, 6,17 ГБ.
- **Не сделано**: замер на настоящей 3B, 7B (≈15 ГБ) требует отложенной загрузки или квантования, прототип SB, уточнить у пользователя, какая техника DeepSeek имеется в виду, скорость на CPU.

## 2026-11-19 大きなAIモデルを動かす取り組みの現状 / Running bigger AI models: status and plan

### 日本語(やさしい説明)
**いまできること**
- 大きなAIモデルは、重さが1つのファイルでなく「いくつかに分かれたファイル」で配られることがあります。これを**自動で全部ダウンロードして、読み込める**ようになりました(`aruaru-llm` と `open-cuda`)。
- 本物の Qwen2.5-3B(約6GB、2つに分割)を、このパソコン(メモリ32GB、GPUなし)で**実際に読み込んで文章を作れる**ことを確かめました。読み込み約48秒、文章づくりは1秒に約0.6語(遅いけれど動きます)。
- 読み込みは「ファイルを丸ごとメモリに入れず、必要な所だけ読む」やり方に変えたので、メモリの使いすぎが減りました。

**調べて分かったこと**
- 東芝の「シミュレーテッド分岐」や富士通の「デジタルアニーラ」は、「たくさんの選択肢から一番よい組み合わせを探す」道具です。AIの文章づくりを直接速くする道具ではありません。使うなら「どの部品をどこに置くか」「どの部分を何ビットに縮めるか」を決める所です(研究論文はまだ少ない)。
- 「折り畳み(Model Folding)」は、似た部分をまとめてモデルを小さくする方法です。DeepSeek の MLA(記憶の圧縮)・MoE(専門家を必要な分だけ使う)・FP8(数を小さく表す)も同じ仲間の工夫です。
- 実験: 学習済みの Qwen に後からMLA圧縮をかけると、記憶を25%減らしただけで品質が落ち(迷い度 7.1→12.7)、50%減らすと文が壊れました。**後付けのMLAは使えない**と分かりました(DeepSeekは最初からその形で学習しています)。

**これから作るもの(確認なしで順に進めます)**
1. 重みを小さい数(f16や量子化)のまま使って、7B級(約12GB)もこのパソコンで動かす。
2. 層ごと・専門家ごとに「何ビットにするか」を自動で決める(まずは普通の計算、あとで焼きなましやSBも試す)。
3. 似た層をまとめる「折り畳み」を試し、品質と速さを必ず測る。
4. 速さの測定を毎回記録し、実用になるまで作る・試す・直すを何度も繰り返す。

**約束**: 未了の作業は、危険でない限り**いちいち確認せず進めます**。ただし、取り返しのつかない削除や、秘密の公開はしません。結果が悪かったときは、悪かったと正直に書きます。

### English (plain words, easy to read)
**What works now**
- Big AI models are often shipped as **several files** instead of one. The program can now **download all the parts and load them** (`aruaru-llm` and `open-cuda`).
- We loaded the real Qwen2.5-3B model (about 6 GB, 2 parts) on this PC (32 GB memory, no GPU) and **it wrote text**. Loading took about 48 seconds; writing was about 0.6 words per second (slow, but it works).
- Loading now reads only the parts it needs instead of copying whole files into memory, so it uses less memory.

**What we learned**
- Toshiba's "Simulated Bifurcation" and Fujitsu's "Digital Annealer" help **pick the best combination from many choices**. They do not make an AI write faster by themselves. They could help decide where to put each part, or how many bits each part gets (papers on this are still few).
- "Model folding" means merging similar parts to make a model smaller. DeepSeek's MLA (memory compression), MoE (use only the needed experts) and FP8 (small numbers) are cousins of this idea.
- Our test: adding MLA compression to an already-trained Qwen cut memory by 25% but made quality worse (perplexity 7.1 to 12.7), and a 50% cut broke the text. **Adding MLA afterwards does not work** (DeepSeek trains with it from the start).

**What we will build next (we go on without asking)**
1. Keep weights in small numbers (f16 or quantized) so 7B-size models (about 12 GB) can run on this PC.
2. Choose bits per layer and per expert automatically (plain math first, annealing or SB later).
3. Try "folding" similar layers, and always measure quality and speed.
4. Record every speed test, then build, test and fix again and again until it is truly useful.

**Promise**: for unfinished work we **go on without asking each time**, unless it is dangerous. We never do irreversible deletes or publish secrets. If a result is bad, we say so honestly.

## 2026-11-19 大きなAIを小さなパソコンで動かす / Running big AI on a small PC (10 languages, easy words)

### 日本語
**できたこと**: 大きなAIは、重さが「いくつかのファイル」に分かれていることがあります。それを自動でぜんぶダウンロードして、読めるようになりました。本物のAI(Qwen 3B、約6GB)を、GPUのないふつうのパソコンで動かして、文章を作れました。ちょっと遅いけれど、ちゃんと動きます。
**わかったこと**: 東芝や富士通の「最適な組み合わせを探す機械」は、AIを直接速くする道具ではありません。「どの部品を何ビットに縮めるか」を決める手伝いに使えるかもしれません。作ったあとの記憶の圧縮(MLA)は、品質が落ちるので使えませんでした。
**これから**: AIの重さを小さい数で持って、もっと大きなAI(約12GB)も動かします。「確認しないで進める」ので、止まらずに作って、試して、直します。

### English
**Done**: Big AI models often come in several files. The program now downloads every part and loads them. We ran a real AI (Qwen 3B, about 6 GB) on an ordinary PC without a GPU, and it wrote text. It is a bit slow, but it works.
**Learned**: The "best-combination finder" machines from Toshiba and Fujitsu do not make AI faster by themselves. They might help decide how many bits each part gets. Squeezing the memory afterwards (MLA) hurt quality, so we cannot use it.
**Next**: Keep the AI's weights in small numbers so even bigger AI (about 12 GB) can run. We go on without asking each time: build, test and fix again and again.

### 简体中文
**已完成**:大型AI的权重常被拆成好几个文件。现在程序能自动全部下载并读取。我们在没有显卡的普通电脑上运行了真正的AI(Qwen 3B,约6GB),它能写出文字。虽然有点慢,但是能用。
**发现**:东芝和富士通那种"找最佳组合的机器"不能直接让AI变快,也许能帮忙决定每个部分用几位数。事后压缩记忆(MLA)会让质量变差,所以不能用。
**接下来**:用更小的数字保存权重,让更大的AI(约12GB)也能运行。我们不会每次都问,而是不停地做、测、改。

### 繁體中文
**已完成**:大型AI的權重常被拆成好幾個檔案。現在程式能自動全部下載並讀取。我們在沒有顯示卡的一般電腦上執行了真正的AI(Qwen 3B,約6GB),它能寫出文字。雖然有點慢,但可以用。
**發現**:東芝和富士通那種「找最佳組合的機器」不能直接讓AI變快,也許能幫忙決定每個部分用幾位元。事後壓縮記憶(MLA)會讓品質變差,所以不能用。
**接下來**:用更小的數字保存權重,讓更大的AI(約12GB)也能執行。我們不會每次都詢問,而是不停地做、測、改。

### 한국어
**해낸 일**: 큰 AI는 무게(가중치)가 여러 파일로 나뉘어 있을 때가 많아요. 이제 프로그램이 전부 자동으로 내려받아 읽을 수 있어요. 그래픽카드가 없는 보통 컴퓨터에서 진짜 AI(Qwen 3B, 약 6GB)를 돌려 글을 만들었어요. 조금 느리지만 잘 돼요.
**알게 된 것**: 도시바와 후지쯔의 "가장 좋은 조합을 찾는 기계"는 AI를 직접 빠르게 하지는 않아요. 각 부분을 몇 비트로 줄일지 정하는 데 도움이 될 수는 있어요. 나중에 기억을 줄이는 방법(MLA)은 품질이 떨어져서 쓸 수 없었어요.
**앞으로**: 무게를 더 작은 숫자로 들고 있어서 더 큰 AI(약 12GB)도 돌릴 거예요. 매번 묻지 않고 만들고, 시험하고, 고치기를 계속해요.

### Deutsch
**Geschafft**: Große KI-Modelle bestehen oft aus mehreren Dateien. Das Programm lädt jetzt alle Teile selbst herunter und liest sie. Wir haben eine echte KI (Qwen 3B, etwa 6 GB) auf einem normalen PC ohne Grafikkarte laufen lassen, und sie hat Text geschrieben. Etwas langsam, aber es klappt.
**Gelernt**: Die „Maschinen, die die beste Kombination suchen“ von Toshiba und Fujitsu machen eine KI nicht von selbst schneller. Sie könnten helfen zu entscheiden, wie viele Bits jeder Teil bekommt. Das nachträgliche Zusammendrücken des Gedächtnisses (MLA) machte die Qualität schlechter, deshalb nutzen wir es nicht.
**Als Nächstes**: Die Gewichte in kleineren Zahlen speichern, damit noch größere KI (etwa 12 GB) läuft. Wir machen ohne Rückfrage weiter: bauen, testen, verbessern, immer wieder.

### Français
**Fait** : Les grosses IA sont souvent livrées en plusieurs fichiers. Le programme télécharge maintenant toutes les parties et les lit. Nous avons fait tourner une vraie IA (Qwen 3B, environ 6 Go) sur un PC ordinaire sans carte graphique, et elle a écrit du texte. C'est un peu lent, mais ça marche.
**Appris** : Les « machines qui cherchent la meilleure combinaison » de Toshiba et Fujitsu ne rendent pas l'IA plus rapide toutes seules. Elles pourraient aider à choisir combien de bits donner à chaque partie. Compresser la mémoire après coup (MLA) a abîmé la qualité, donc nous ne l'utilisons pas.
**Ensuite** : Garder les poids en plus petits nombres pour faire tourner de plus grosses IA (environ 12 Go). Nous continuons sans demander à chaque fois : construire, tester, corriger, encore et encore.

### Español
**Hecho**: Las IA grandes suelen venir en varios archivos. Ahora el programa descarga todas las partes y las lee. Ejecutamos una IA real (Qwen 3B, unos 6 GB) en un PC normal sin tarjeta gráfica y escribió texto. Es un poco lento, pero funciona.
**Aprendido**: Las «máquinas que buscan la mejor combinación» de Toshiba y Fujitsu no hacen más rápida a la IA por sí solas. Podrían ayudar a decidir cuántos bits da cada parte. Comprimir la memoria después (MLA) empeoró la calidad, así que no lo usamos.
**Siguiente**: Guardar los pesos con números más pequeños para que corran IA aún más grandes (unos 12 GB). Seguimos sin preguntar cada vez: construir, probar y arreglar una y otra vez.

### Português
**Feito**: As IAs grandes costumam vir em vários arquivos. Agora o programa baixa todas as partes e as lê. Rodamos uma IA de verdade (Qwen 3B, cerca de 6 GB) num PC comum sem placa de vídeo, e ela escreveu texto. É um pouco lento, mas funciona.
**Aprendido**: As «máquinas que procuram a melhor combinação» da Toshiba e da Fujitsu não deixam a IA mais rápida sozinhas. Elas podem ajudar a decidir quantos bits cada parte recebe. Comprimir a memória depois (MLA) piorou a qualidade, então não usamos.
**Próximo**: Guardar os pesos em números menores para rodar IAs ainda maiores (cerca de 12 GB). Seguimos sem perguntar toda vez: construir, testar e consertar, de novo e de novo.

### Русский
**Сделано**: Большие ИИ часто поставляются в нескольких файлах. Теперь программа сама скачивает все части и читает их. Мы запустили настоящий ИИ (Qwen 3B, около 6 ГБ) на обычном компьютере без видеокарты, и он написал текст. Немного медленно, но работает.
**Узнали**: «Машины, которые ищут лучшую комбинацию» от Toshiba и Fujitsu сами по себе ИИ не ускоряют. Возможно, они помогут решить, сколько бит дать каждой части. Сжатие памяти задним числом (MLA) ухудшило качество, поэтому мы его не используем.
**Дальше**: Хранить веса в меньших числах, чтобы запускать ещё более крупные ИИ (около 12 ГБ). Мы продолжаем без вопросов каждый раз: строим, проверяем, исправляем снова и снова.
