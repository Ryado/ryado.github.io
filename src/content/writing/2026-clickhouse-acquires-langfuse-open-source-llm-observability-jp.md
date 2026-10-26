---
title: ClickHouse が Langfuse を歓迎:オープンソース LLM オブザーバビリティの未来
date: '2026-01-16'
source: clickhouse
canonical_url: https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability-jp
coauthors:
- Marc Klingen
- Max Deichmann
- Clemens Rawert
tags:
- company-and-culture
summary: ClickHouse は、LLM オブザーバビリティ、評価、プロンプト管理をリードするオープンソースプラットフォームである Langfuse を買収したことを喜んでお知らせします。
reading_time: 3
content_hash: 875ea7a3ad6bfcb6
---

ClickHouse が、LLM のオブザーバビリティ、評価、プロンプト管理における主要なオープンソースプラットフォームである [Langfuse](https://github.com/langfuse/langfuse) を買収したことをお知らせします。Marc Klingen、Max Deichmann、Clemens Rawert、そして Langfuse のチームおよびコミュニティ全体を ClickHouse ファミリーに迎えることができ、これ以上の喜びはありません。

AI の品質モニタリングに対する Langfuse の開発者ファーストなアプローチと、ClickHouse の圧倒的に高速なコア分析機能を組み合わせることで、大規模な AI アプリケーションの構築、モニタリング、最適化に向けた包括的なオープンソーススタックを提供します。

## AI ネイティブアプリケーションの台頭

LLM はもはや黎明期の技術ではなく広く普及しており、現代のほぼすべてのソフトウェアで機能や処理を支えています。例えば、新しい SaaS アプリケーションの多くは、対話型インターフェース、エージェントで強化されたワークフロー、自動化といった AI 機能をワークフローの中心に据えてリリースされています。開発者は、(コーディングエージェントや Copilot を通じて)AI の利用者であると同時に、AI を活用した体験の主要な構築者にもなりました。

ClickHouse では、[Agentic Data Stack](https://clickhouse.com/ai) の取り組みを通じてこの変化を直接目の当たりにしてきました。複雑な AI ワークフローは、実際のデータやインサイトに根差している必要があります。まさにここで、LLM と強力な分析データベースの相乗効果が不可欠になります。

しかし、依然として「信頼性」に関する重大なギャップが存在します。自社の AI アプリケーションが実際に意図通り動作しているかを、どうやって把握すればよいのでしょうか。

## AI 品質モニタリング

LLM を活用したアプリケーションは、非決定論的なブラックボックスです。まったく同じプロンプトであっても異なる応答が生成されることがあり、デバッグや品質保証は従来のソフトウェアとは根本的に異なります。

適切な可視性を持たずに運用することは、一部の実務者が「vibe-checking(雰囲気確認)」と呼ぶ状態に陥ります。測定する手段がないまま、出力品質に賭けているようなものです。コンシューマー向けアプリケーションであれば、ユーザー体験の悪化で済むかもしれません。しかし、財務上の判断、法務やコンプライアンスに関わる事項、顧客向けの対話を扱うエンタープライズアプリケーションでは、リスクははるかに高くなります。

この課題は、複雑さが増すにつれてさらに大きくなります。現代の AI アプリケーションには、複数ステップにわたるエージェント型ワークフロー、データエンリッチメントパイプライン、ツール呼び出し、ネストされた推論チェーン、マルチエージェントの連携などが含まれる場合があります。何らかの問題が発生した際、適切なツールがなければ原因の特定と改善はほぼ不可能です。

従来のオブザーバビリティツールは、サービスが稼働しているか、高速か、エラーがないかを教えてくれます。しかし、モデルの出力が正しいか、有用か、安全か、あるいはユーザーの意図に沿っているかについては何もわかりません。システム的な観点では完全に健全であっても、LLM が低品質な回答を一貫して生成し続けているケースもあるのです。

だからこそ、私たちは「AI 品質モニタリング」という枠組みが適切であると考えています。これは、「AI がユーザーにとって実際にどれほどうまく機能しているか」という、真に重要な成果に直接焦点を当てるアプローチです。

ClickHouse では常に、まず社内システムでソリューションを評価しています。私たちは、社内のデータウェアハウス AI エージェントである [DWAINE](https://clickhouse.com/blog/ai-first-data-warehouse) のモニタリングに Langfuse を社内利用してきました。LLM とのやり取りを適切に観測できたことは、エージェントがどこで成果を上げ、どこに改善が必要かを理解する上で非常に価値がありました。

![langfuse-screenshot-2.png](/writing/clickhouse-acquires-langfuse-open-source-llm-observability-jp/langfuse_screenshot_2_ae975a0ccc.png)

個々のやり取りをトレースし、ハルシネーション検出などの品質メトリクスでスコアリングし、長期的な傾向を分析できる機能によって、本番環境における AI 品質への考え方が根本から変わりました。

![langfuse-screenshot.png](/writing/clickhouse-acquires-langfuse-open-source-llm-observability-jp/langfuse_screenshot_a76076e363.png)

## なぜ Langfuse なのか？

AI オブザーバビリティの領域を評価した際、いくつかの点がすぐに明らかになりました。

**市場は細分化しているものの、Langfuse がリードを広げています。** 特化型のスタートアップから、LLM モニタリングへと領域を広げる MLOps ベンダー、AI 機能を追加する従来のオブザーバビリティプラットフォームまで、この分野には数多くのプレーヤーが存在します。その中で Langfuse は、オープンソースかつ開発者ファーストな LLM オブザーバビリティのリーダーとして頭角を現しています。

- 2万以上の GitHub スター
- 月間 2,310 万回以上の SDK インストール
- 600 万回以上の Docker プル
- Fortune 50 のうち 19 社、Fortune 500 のうち 63 社から信頼を獲得
- Intuit、Twilio、7-Eleven、Merck など多数の[エンタープライズ](https://langfuse.com/enterprise)ユーザー

昨年の成長を振り返る素晴らしいまとめとして、[Langfuse Wrapped 2025](https://langfuse.com/wrapped) もぜひご覧ください。

**Langfuse はすでに ClickHouse 上に構築されています。** Langfuse のアーキテクチャは、クラウド版とセルフホスト型のデプロイの両方において、[完全に ClickHouse 上で稼働](https://langfuse.com/blog/2024-12-langfuse-v3-infrastructure-evolution)しています。LLM オブザーバビリティの大規模なスケールとパフォーマンス要件には、大量の書き込みと高速な分析クエリを[処理できる](https://www.youtube.com/watch?v=NXYQ5odATrM)データベースが不可欠です。この既存の親和性により、より緊密な統合と、すべてのユーザーに向けたパフォーマンスの向上が実現します。

**オープンソースの DNA を共有しています。** 私たちは、オープンソースの優れた管理者であるということは、単にコードを維持することだけでなく、それに依存するコミュニティへ積極的に投資し、育てていくことだと考えています。Langfuse は、私たちが支援したいと心から願う、まさに活気ある開発者コミュニティを築き上げてきました。そこではコントリビューターが積極的にプロダクトを形作り、OpenTelemetry などのオープン標準を取り入れながら、草の根的な勢いによってエンタープライズへの導入が自然と進んでいます。これは現在の ClickHouse を形作った手法と同じであり、Langfuse コミュニティにもそのエネルギーをもたらせることを楽しみにしています。

**包括的なプロダクトです。** Langfuse は、AI オブザーバビリティ、プロンプト管理、評価、実験をカバーする[完全なプラットフォーム](https://langfuse.com/enterprise)です。データモデルと SDK レイヤーは、LLM アプリケーション特有の課題に合わせてきめ細かく設計されています。

![observability-image.png](/writing/clickhouse-acquires-langfuse-open-source-llm-observability-jp/observability_image_b64e9276e3.png)

> 「生成 AI がエンタープライズの信頼を獲得できるのは、水面下で何が起きているかを把握できるようになったときだけです。Langfuse を使用することで、すべてのプロンプト、応答、コスト、レイテンシをリアルタイムに追跡し、ブラックボックスだったモデルを監査可能かつ最適化可能な資産へと変えることができます」
>
> *Walid Mehanna 氏(Merck、Chief Data & AI Officer)* ([情報元](https://langfuse.com/customers/merckgroup))

## シナジー

今回の買収は、[PeerDB](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database)(Postgres CDC 向け)や [HyperDX](https://clickhouse.com/blog/clickhouse-acquires-hyperdx-the-future-of-open-source-observability)(インフラオブザーバビリティ向け)で成功を収めてきたのと同じ手法に沿ったものです。私たちは、すでに ClickHouse 上に構築されており、開発者体験とコミュニティファーストの開発へのこだわりを共有する、各カテゴリを代表するオープンソースプロジェクトと力を合わせています。

Langfuse に対しても、AI オブザーバビリティにおいて同様の取り組みを進めていきます。

- **Langfuse は 100% オープンソースのまま継続されます**。コア機能は既存の MIT ライセンスが維持され、本番規模(ClickHouse 上)でのセルフホストが可能です。
- **Langfuse Cloud は独立したサービスとして運用を継続します**。
- **コミュニティファーストの開発**も、これまでと同じ透明性とオープンさをもって継続されます。

Langfuse と ClickHouse のより緊密な統合により、データの収集から分析、アクションに至るスタック全体を共同で最適化できるようになります。これにより、パフォーマンス向上という形で Langfuse ユーザーに恩恵をもたらすとともに、AI ワークロード向けの最適化に役立つインサイトという形で ClickHouse ユーザーにも利益を還元するフィードバックループが生まれます。

> 「Langfuse のおかげで、開発者は非常に迅速なフィードバックを得られるようになりました。機能を構築してデプロイする際、その体験がどう推移しているかを素早く確認できます。Langfuse は、開発者が自身の AI 実装を理解する上で欠かせない存在です」
>
> *Walt Wells 氏(Khan Academy、Staff Software Engineer)*([情報元](https://langfuse.com/customers/khan-academy))

## Agentic Data Stack にとっての意味

[Agentic Data Stack](https://clickhouse.com/ai)(ClickHouse と LibreChat 上に構築される AI アプリケーションに向けた私たちのビジョン)に、極めて重要な新機能が加わります。それは、AI コンポーネント自体をモニタリングし、評価し、継続的に改善する能力です。

LibreChat を使用してデータウェアハウスにクエリを実行するデータアナリストや管理者に対して、Langfuse はエージェントがどれほどうまく機能しているかの可視性を提供します。また、私たちの API や MCP サーバーを使用してカスタムのエージェント型ワークフローを構築する開発者に対しては、自信を持ってリリースするために必要なデバッグおよび最適化ツールを提供します。

エージェント型アナリティクスにおける 3 つの主要なペルソナ(データベースを運用するデータ専門家、AI 機能を構築する開発者、インサイトを活用するビジネスユーザー)のすべてが、AI とのやり取りがモニタリングされ、評価され、時間とともに改善されていくという安心感を得られます。

## 今後の展開

**既存の Langfuse デプロイをご利用の場合:** 何も変わりません。Langfuse は現在とまったく同様に動作し続け、私たちはプラットフォームとコミュニティへの投資を継続することをお約束します。

**Langfuse Cloud の利用者の方へ:** サービスはこれまでと同じ SLA とサポートで運用を継続します。Langfuse チームは、現在機能しているものを崩すのではなく、ロードマップの拡充に注力しています。

**ClickHouse ユーザーの方へ:** 今後数か月にわたり、LLM オブザーバビリティを Agentic Data Stack 体験のネイティブな一部とする、より緊密な統合をリリースしていく予定です。自社の AI ワークロードと、それを把握するためのツールとのシームレスな連携にご期待ください。

**すべての皆様へ:** AI オブザーバビリティの未来を共に築くために、ぜひ [Slack](https://clickhouse.com/slack) のコミュニティにご参加ください。

## はじめに

**Langfuse ユーザーの方へ:** これまで通り Langfuse をご利用ください。初めての方は充実した[ドキュメント](https://langfuse.com/docs)をご確認いただくか、すでにご利用中の方は最新機能をお試しください。

**ClickHouse ユーザーの方へ:** AI を活用したアプリケーションを構築している場合は、[Langfuse を試して](https://langfuse.com) LLM とのやり取りにオブザーバビリティを導入してみてください。バックエンドストアとしての ClickHouse との連携は、すでにシームレスに実現されています。

**それ以外のすべての方へ:** AI がソフトウェアの動作の中核となるにつれて、AI 品質モニタリングの重要性は高まる一方です。今こそ、自社の AI システムの把握に本格的に取り組むタイミングです。

いつものように、ClickHouse チームは皆様の AI への取り組みにおいてパートナーとなれることを光栄に思います。すでに Langfuse をご利用中の方も、LLM オブザーバビリティの検討を始めたばかりの方も、ぜひ[お問い合わせ](https://clickhouse.com/company/contact)ください。
