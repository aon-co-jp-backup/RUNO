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
| aruaru-db-archive(非公開) | — | [aon-co-jp/aruaru-db-archive](https://github.com/aon-co-jp/aruaru-db-archive) | [README](https://github.com/aon-co-jp/aruaru-db-archive/blob/main/README.md) | — | — | `aruaru-db`(VPS高速キャッシュ層)から古くなったデータをGit-on-SQL経由で自動バックアップする非公開アーカイブ先。`open-LiveKit`のノードルーティング状態管理(DUAL DB構成)で使用予定。**2026-09-26時点は雛形のみ、自動同期の実装は未着手**。 |
| open-github-backup(非公開) | — | [aon-co-jp/open-github-backup](https://github.com/aon-co-jp/open-github-backup) | [README](https://github.com/aon-co-jp/open-github-backup/blob/main/README.md) | — | — | `aon-co-jp`の全リポジトリを GitHub Actions で`runo-aruaru`(非公開)へ自動ミラーするバックアップ。RS-Syncの同期とVPS cronを置き換えた。2026-10-08に全件成功、以降はGitHub課金/利用上限でジョブ未開始(要Billing確認、残る課題はこれのみ)。VPSデータの暗号化バックアップ(毎日03:30)も稼働中。 |
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
| open-raid-z | — | [aon-co-jp/open-raid-z](https://github.com/aon-co-jp/open-raid-z) | [README](https://github.com/aon-co-jp/open-raid-z/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-raid-z/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-raid-z/blob/main/CLAUDE.md) | Rust製の実マウント可能なRAID-Z/Z2/Z3ストレージプール実装(ZFS「風」のCoW/チェックサム/スナップショット。ZFS自体・OpenZFSへの依存やオンディスク互換性はなし)。**エコシステム開発ルールの正本**リポジトリ。 |
| maid-cafe-se | — | [aon-co-jp/maid-cafe-se](https://github.com/aon-co-jp/maid-cafe-se) | [README](https://github.com/aon-co-jp/maid-cafe-se/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/maid-cafe-se/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/maid-cafe-se/blob/main/CLAUDE.md) | maid-cafeによる秘書サービス(secretary)。Androidスマホ向け。定型スケジュール(毎日/平日/土日祝/曜日/第N週/N週ごと)で著作権フリー音のアラーム、または入力文章をメイドカフェ風/低い男性声で読み上げ。Googleカレンダー連動+30分前予告。**2026-09-30時点でv0.4.0(Android署名つきAPK+Windows版インストーラー`maid-cafe-se-installer.exe`、`installer/`に入手・ビルド方法)。アプリ本体のRust(+RPoem)化を進行中**。 |
| open-tv-chat | — | [aon-co-jp/open-tv-chat](https://github.com/aon-co-jp/open-tv-chat) | [README](https://github.com/aon-co-jp/open-tv-chat/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-tv-chat/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-tv-chat/blob/main/CLAUDE.md) | Skype風「世界約130ヶ国語リアルタイム音声翻訳」対応のTV会議/ビデオチャットアプリ構想(Windows/macOS/Linux/Android/iPhone向け)。`open-web-server`+Rust/`RPoem`(Cosmo互換)構成。**2026-09-26時点は設計ドキュメント段階、実装は未着手**。 |
| open-vsc-claude | — | [aon-co-jp/open-vsc-claude](https://github.com/aon-co-jp/open-vsc-claude) | [README](https://github.com/aon-co-jp/open-vsc-claude/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-vsc-claude/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-vsc-claude/blob/main/CLAUDE.md) | 言語・フレームワーク(GraphQL+WunderGraph Cosmo/RPoem、TypeScript+Node+REST、または言葉で自由指定)を選んで生成コードをプレビューし、Claudeで改良して保存できるVS Code拡張。Web拡張(vscode.dev等)とブラウザデモ(PWA・オフライン可、[easy-web.tokyo/open-vps-claude](https://easy-web.tokyo/open-vps-claude/))付き、自動更新確認、README/CLAUDE/PORTINGは12言語。**2026-10-18時点でv0.1.1。Marketplace公開・Cosmo Router実起動・実機iOS/Androidは未了**。 |
| 360-speaker | — | [aon-co-jp/360-speaker](https://github.com/aon-co-jp/360-speaker) | [README](https://github.com/aon-co-jp/360-speaker/blob/main/README.md) | — | — | 360度全方位5WAYトールボーイスピーカー(1〜5WAY・通常/スーパーツィーター/サブウーファーの3版、アンプ内蔵またはアンプ無し+別売プリ)の設計案・調査・製品比較と、Rust→WASMのWebシミュレーター(指向性・T/S箱設計・ポート・壁材・ボリューム方式別コスト)。受動ネットワーク設計図(PDF/JPG)付き。公開: [easy-web.tokyo/360-speaker](https://easy-web.tokyo/360-speaker/)。**2026-10-25時点で設計初版。実機試作・実測は未了、コストは推定値**。 |
| version-control | — | [aon-co-jp/version-control](https://github.com/aon-co-jp/version-control) | [README](https://github.com/aon-co-jp/version-control/blob/main/README.md) | — | — | 全リポジトリが最新のライブラリ(crates.io/npm/packagist)・クローンを使っているかを走査し、`open-cuda`/`aruaru-llm`/`open-cpu`/`open-directx`の自動保守で足りないものを、Claude向けの貼り付けメッセージにしてメールとLINE(Messaging API)で通知。依存の書き換え・`git pull`はしない。運用: [easy-web.tokyo/version-control](https://easy-web.tokyo/version-control/)、デモ: [/demo/](https://easy-web.tokyo/version-control/demo/)。**2026-10-26時点で初版・単体テストと画面の表示のみ確認、メール/LINE送信とVPS配置は未了**。 |
| open-web-server | — | [aon-co-jp/open-web-server](https://github.com/aon-co-jp/open-web-server) | [README](https://github.com/aon-co-jp/open-web-server/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/open-web-server/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/open-web-server/blob/main/CLAUDE.md) | Rust + tokio/hyper自前実装のWebサーバー — 課金アイテム・金融データを「消失させない」ために設計。`open-runo`・`aruaru-db`と4層防御通信で連携するミッションクリティカル向け。 |
| realdata.pro | — | [aon-co-jp/realdata.pro](https://github.com/aon-co-jp/realdata.pro) | [README](https://github.com/aon-co-jp/realdata.pro/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/realdata.pro/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/realdata.pro/blob/main/CLAUDE.md) | SAS Viyaを参考にした、誰でも使えるRust製オープンソースのデータ分析プラットフォーム(旧名rs-real-data)。open-cuda・RPoem・open-web-server・aruaru-llm等のエコシステム上に構築し、CSV・検索ワード(Google/YouTube/GitHub)・URLからの取り込み、クレンジング・集計・グラフ・重回帰、AIによる多言語説明を提供する。公開予定ドメインはrealdata.pro。 |
| webeditor-sftp | — | [aon-co-jp/webeditor-sftp](https://github.com/aon-co-jp/webeditor-sftp) | [README](https://github.com/aon-co-jp/webeditor-sftp/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/webeditor-sftp/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/webeditor-sftp/blob/main/CLAUDE.md) | ブログ感覚のWEB文章編集エディター(HTMLタグ非表示のブログモード/生コード編集のコーディングモード切替)と、秘密鍵・公開鍵を安全に受け渡しできるSFTPツールをハイブリッド統合したクロスプラットフォームアプリ(Tauri採用、Android/Windows/将来のiOS・macOS/Linux対応)。最初の実地検証対象は`audiocafe.tokyo`(Rust+Poem)。**2026-09-28時点は設計ドキュメント+最小プロトタイプ段階**。 |
| rs-to-readme | — | [aon-co-jp/rs-to-readme](https://github.com/aon-co-jp/rs-to-readme) | [README](https://github.com/aon-co-jp/rs-to-readme/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/rs-to-readme/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/rs-to-readme/blob/main/CLAUDE.md) | Rustクレートの`Cargo.toml`メタデータからREADME.mdを自動生成するCLIツール([crates.io](https://crates.io/crates/rs-to-readme)公開)。 |
| RS-JSON | — | [aon-co-jp/RS-JSON](https://github.com/aon-co-jp/RS-JSON) | [README](https://github.com/aon-co-jp/RS-JSON/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/RS-JSON/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/RS-JSON/blob/main/CLAUDE.md) | RustのJSON処理ライブラリ。寛容モード(JSON5風)・厳密モード・部分抽出に加え、信頼できない入力向けの安全モード`parse_secure`(サイズ・深さ上限、重複キー拒否)と、速い値の型で読む`parse_secure_sonic`(`fast`機能、実測で`serde_json`の約2.4倍速い)を提供。旧`sonic-rs`(評価記録)を統合済み。型付き読み書き`fast::from_str`等と、RS-JSON<->JSON変換(最大約7倍速い)も提供。 |
| rs-dpiAwareness | — | [aon-co-jp/rs-dpiAwareness](https://github.com/aon-co-jp/rs-dpiAwareness) | [README](https://github.com/aon-co-jp/rs-dpiAwareness/blob/main/README.md) | [PORTING](https://github.com/aon-co-jp/rs-dpiAwareness/blob/main/PORTING.md) | [CLAUDE.md](https://github.com/aon-co-jp/rs-dpiAwareness/blob/main/CLAUDE.md) | WindowsのDPI認識(PerMonitorV2)を依存ゼロのRustで扱う小さなクレート+診断CLI(段階的な代替つきの`init()`、モニターごとのDPI、`WM_DPICHANGED`、マニフェストの生成・埋め込み・読み出し)。Microsoftの公開仕様へのリスペクト版で、Microsoftとは無関係。実機(Windows 11・4K 200%)で確認済み、複数モニター間の移動は未確認。 |
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
