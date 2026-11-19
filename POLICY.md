# POLICY (aon-co-jp 共通方針の索引)

- API方針の正本: [API-POLICY.md](API-POLICY.md)(日英独露)
- 共通指示書: [API-MIGRATION-BRIEF.md](API-MIGRATION-BRIEF.md)
- 言語変換の共通の形(IR)の方針: [`pl2pl`](https://github.com/aon-co-jp/pl2pl) の `src/ir.rs`(入力側)と `src/ir_emit.rs`(書き出し側)。変換できない所は黙って消さず TODO で残す。出力を変えない変更は、前後の出力の diff が空で確かめる。(2026-11-19)
- Policy for the shared shape (IR) of language conversion: `src/ir.rs` (input side) and `src/ir_emit.rs` (writer side) in [`pl2pl`](https://github.com/aon-co-jp/pl2pl). Parts that cannot be converted are never dropped silently; they stay as TODO notes. A change that must not alter the output is proven by an empty diff of the output before and after. (2026-11-19)

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
