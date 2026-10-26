---
title: 'ClickHouseエージェント: Claudeを活用したエージェント型アナリティクスがパブリックベータで登場'
date: '2026-06-09'
source: clickhouse
canonical_url: https://clickhouse.com/blog/clickhouse-agents-beta-jp
coauthors: []
tags:
- product
summary: ClickHouseでは1年以上にわたって本番環境でエージェント型分析を運用してきましたが、サンフランシスコで開催された Open House 2026 において、Claudeを搭載したClickHouse Cloudのフルマネージド型エージェント分析サービスである ClickHouse Agents のパブリックベータを発表しました。 ClickHouse Agentsは、ClickHouse Cloudに統合されたネイティブなAI体験です。ClickHouse…
reading_time: 2
content_hash: 0961ff3bf4195631
---

ClickHouseでは1年以上にわたって本番環境でエージェント型分析を運用してきましたが、サンフランシスコで開催された [Open House 2026](https://clickhouse.com/blog/open-house-2026-day-1) において、Claudeを搭載したClickHouse Cloudのフルマネージド型エージェント分析サービスである [ClickHouse Agents](https://clickhouse.com/docs/cloud/features/ai-ml/agents) のパブリックベータを発表しました。

ClickHouse Agentsは、ClickHouse Cloudに統合されたネイティブなAI体験です。ClickHouse Agentsを使えば、コード不要で簡単にエージェントを構築でき、SQLやセットアップなしで、ライブなClickHouseデータに基づいたエージェントをユーザーが展開できます。これらのエージェントは、Cloudコンソール内のフルマネージド型チャット体験を通じて活用でき、セットアップも別のホスティング環境も不要です。

## ClickHouse Agentsとは

ClickHouse Agentsは、実績のあるオープンソースAIプラットフォームである [LibreChat](https://github.com/danny-avila/LibreChat) 上に構築されており、ClickHouse Cloud内でフルマネージドとして動作します。その中核にあるのは、ノーコードのエージェントビルダーで、アナリスト、PM、データエンジニア、エグゼクティブを問わず、誰もがClickHouseデータに基づいたエージェントを定義、設定、展開できます。ClickHouse Agentsには、すぐに使えるチャットインターフェース、サンドボックス化されたコードインタープリター、共有可能なアーティファクト、スキル、メモリ、マルチエージェントワークフローも備わっています。エージェントはClickHouseおよびあらゆるMCP互換システムにネイティブに接続し、すでに存在する場所からコンテキストを取り込みます。

Loading video...

<video controls preload="none" playsinline src="/writing/clickhouse-agents-beta-jp/Ryadh_Keynote_Web_407d0cb26c.mp4"></video>

含まれるもの:

- **ノーコードエージェントビルダー**: カスタム指示、スキル、コンテキストファイル、MCPツールアクセスを備えたエージェントを定義可能。Cloud RBACによって管理されます。
- **チャットインターフェース**: フルマネージドのマルチテナント対応チャット体験。自然言語で質問し、SQLや可視化を生成し、アーティファクトを構築し、データに対してマルチターン会話を実行できます。
- **サンドボックス化されたコードインタープリター**: 任意の会話の中で、Bash、Python、JavaScriptを安全に[実行](https://clickhouse.com/docs/cloud/features/ai-ml/agents/builder/code-interpreter)。チャットを離れることなく、ライブのクエリ結果に対して実行されます。
- **事前設定されたClaude**: すべてのCloudユーザーに対し、Claudeモデル(SonnetおよびHaiku)がデフォルトモデルとして組み込まれています。
- **スキル、メモリ、アーティファクト**: 反復可能なワークフローやコンテキストをスキルとしてパッケージ化し、メモリでコンテキストを永続化し、チャートやダッシュボードをアーティファクトとして共有可能。
- **マルチエージェントワークフロー**: エンドツーエンドの分析タスクをまたいでサブエージェントをオーケストレーション。
- **エンタープライズセキュリティ**: SSO、暗号化されたメッセージストレージ、ガバナンスの効いたデータアクセスを、マネージドランタイムに組み込み済み。

## AI向けClickHouseプラットフォーム

ClickHouse Agentsは、私たちが「AI向けClickHouseプラットフォーム(ClickHouse Platform for AI)」と呼ぶものの一部です。

主要なクラウドデータプラットフォームはこぞってAIをネイティブ機能に組み込もうとしていますが、その多くは同じやり方を取っています。すなわち、データとAIをバンドルし、プロプライエタリで高価、データ構造、モデル、エージェント、ツールが単一のエコシステムにロックインされた「壁に囲まれた庭(ウォールドガーデン)」型です。この領域の進化の速さを考えると、これは間違った方向であり、オープン性と相互運用性こそが鍵だと私たちは考えています。ClickHouse Platform for AIはオープンスタックで、データ層から積み上げ、アプリ、エージェント、ユーザー、APIに提供されます:

- **データ層**: オープンソースのカラムナエンジンであるClickHouse。[Shopify](https://clickhouse.com/videos/shopify-open-source-network-monitoring)、[Uber](https://www.uber.com/us/en/blog/logging/)、[Ramp](https://clickhouse.com/videos/ramp)、[Anthropic](https://clickhouse.com/blog/how-anthropic-is-using-clickhouse-to-scale-observability-for-ai-era)、[Tesla](https://clickhouse.com/blog/how-tesla-built-quadrillion-scale-observability-platform-on-clickhouse)、[Deutsche Bank](https://clickhouse.com/videos/big-sensitive-data-warehouse-deutsche-bank-clickhouse)のような企業がすでに大規模なリアルタイム分析に使用しており、トランザクションデータ用のマネージドPostgresも併設します。マネージドな取り込みにより、オープンテーブルフォーマット、データレイク、その他のソースからデータを取り込み、コンテキスト管理層(スキル)がエージェントを自社の定義に基づいて接地させます。
- **接続層**: マネージドのClickHouse MCPサーバー、加えてクライアント、CLI、プラグイン。お客様は接続したい任意のMCP互換アプリやエージェントに対する柔軟性と完全な制御を維持できます。すでにお客様はClaude Code、Cursor、Amazon Bedrockエージェント、独自のカスタムエージェントを接続しています。
- **エージェント層**: SQLコンソール内で簡単な質問に答えるClickHouse Assistantと、サンドボックス化されたコードインタープリターを備えたフルエージェント型ワークフロー用のClickHouse Agents。
- **エンドツーエンドの可観測性と評価**: ClickHouseには、可観測性のためのClickStackと、LLM可観測性および評価のためのLangfuseも含まれます。これによりエージェントが何をしているかを可視化し、本番環境で信頼性高く運用できます。

![](/writing/clickhouse-agents-beta-jp/clickhouse_agents_jun2026_image3_8315470075.png)

目標は、ポータブルで拡張可能、ロックインのない最高のリアルタイム分析プラットフォームによってAIの力を享受していただくことです。お客様は、マネージドエージェントをそのまま利用したり、ノーコードビルダーで独自に構築したり、ご自身のフレームワークを持ち込んでClickHouseをその下のオープンデータ層として活用したりと、柔軟に選択できます。

このアプローチで何が違うかというと、ClickHouseはお客様にファーストパーティかサードパーティかの二者択一を迫らないことです。ご自身のエージェント、モデル、ツールをClickHouseに持ち込み、私たちの接続層上で実行することも、ClickHouse Agentsのようなファーストパーティ機能を利用することも可能です。どちらの道も同じオープンなデータ基盤の上に成り立っており、片方を選ばせるのではなく、お客様のいる場所に寄り添います。

![](/writing/clickhouse-agents-beta-jp/clickhouse_agents_jun2026_image4_33e7a643e2.png)

*ClickHouse CloudにおけるMCP採用状況(上記グラフは、リモートMCP機能を利用しているユニークなサービス数の時系列推移を示しています)*

これを示すため、私たちはAmazon Web Servicesと緊密に連携し、ClickHouse Agentsに対するAgentCore Registryとのネイティブ統合を出荷しました。これによりユーザーは、AgentCoreで管理されているエージェント、ツール、スキルをMCP経由で持ち込み、ClickHouse Agentsで利用できます。

![](/writing/clickhouse-agents-beta-jp/clickhouse_agents_jun2026_image5_9d4230b8e1.png)

私たちはClickHouseをAIのためのオープンなデータプラットフォームとして構築しています。ClickHouse Agents、LibreChat、MCP、そしてAWS Agent Registryのようなシステムとの取り組みはすべて、同じ信念を反映しています。すなわち、オープン性、コンポーザビリティ、相互運用性こそが、AIが求めるスピードで企業を動かす力になるという信念です。単一ベンダーが完全なAIスタックを十分に速く、十分に完全に統合することはできず、それを試みる者はユーザーをウォールドガーデンに閉じ込めることになります。ClickHouseのオープンでコミュニティ主導のDNAこそが、すべてのお客様にとってエージェント時代の基盤となる理由です。

## ここに至るまで: 自社経験のプロダクト化

2025年3月、私たちは自社のデータウェアハウスをAIファーストにし、その上に社内分析エージェントを構築しました。そのすべてを[社内データウェアハウスをAIファーストにした方法](https://clickhouse.com/blog/ai-first-data-warehouse)に記録しました。要約すれば、急速に普及したということです。現在、ClickHouseの従業員の約80%が日常的にLibreChatを利用し、当社のプラットフォームだけで社内データウェアハウスクエリの約70%を処理し、1日あたり4,500万トークン以上を処理しています。圧倒的に、最も使われている社内ツールです。

チャット層の選定は、本格的な「自作 vs 購入」の判断でした。要件は妥協できないものでした。任意のLLMプロバイダーに対応すること、堅実なMCPサポート、SSOや監査ログなどのエンタープライズ機能の搭載、アーティファクトのレンダリング、そして単一ベンダーへのロックインがないこと。[LibreChat](https://github.com/danny-avila/LibreChat)はすべての項目を満たしていました。ご存じない方のために説明すると、LibreChatは主要なオープンソースAIチャットプラットフォームで、ほぼすべてのLLMプロバイダーの前段に立てるセルフホスト可能な単一UIを提供し、エンタープライズSSO、RBAC、MCPサポート、エージェント、アーティファクト、サンドボックス化されたコードインタープリターを内蔵しています。

LibreChatが正しいプラットフォームだと確信させたのは、すでに本番運用している企業のリストでもありました。Shopify CEOのTobi Lütke氏は[率直にこう述べています](https://x.com/tobi/status/1932846291794510241):

「Shopifyは社内のlibrechatフォークを運用しており、ほぼすべての変更を本家にマージし戻している。社内LLMシステムを検討している企業には、このプロジェクトを強くお勧めしたい。我々にとっては非常にうまく機能している。」

[Daimler Truck](https://www.daimlertruck.com/en/newsroom/stories/daimler-truck-makes-artificial-intelligence-accessible-to-all-employees-worldwide-with-librechat)は、何千人もの従業員と3,000を超える本番エージェントを擁する全社AIプラットフォームをLibreChat上で運用しています。ヘルスケア分野では、cBioPortalがClickHouse、MCP、LibreChatスタック上で[cBioAgent](https://chat.cbioportal.org/)を出荷し、がん研究者が自然言語でゲノミクスデータセットを照会できるようにしました。同団体でバイオインフォマティクスのソフトウェアエンジニアリングを率いるIno de Bruijn氏は、これは「がん研究者の指先に発見をもたらす」と述べています。2025年11月、[私たちはLibreChatを買収し](https://clickhouse.com/blog/clickhouse-acquires-librechat)、Danny Avila氏とそのチームをClickHouseに迎えました。ClickHouse AgentsはLibreChatの本番品質をそのまま受け継いでいます。

社内ユースケースを運用することで、エージェント分析の実ワークロードの大きなコーパスも得られました。実際のスキーマに対する実際の質問、対応するSQLおよびツール利用のトレースです。これにより、汎用ベンチマークではなく実タスクそのものに対して、利用可能な事実上すべてのモデルを評価できました。Claudeファミリーは、SQL生成、スキーマ推論、ツール利用にわたって一貫してトップでした。コードのリーディングモデルであり、SQLとスキーマの作業はその強みの自然な延長です。これがClaudeをClickHouse Agentsのデフォルトに組み込んだ理由です。

![](/writing/clickhouse-agents-beta-jp/clickhouse_agents_jun2026_image6_0be9866d16.png)

## エージェント向けリアルタイムOLAP

1年以上前、私たちは[エージェント向け分析(agent-facing analytics)](https://clickhouse.com/blog/agent-facing-analytics)について書きました。AIエージェントはリアルタイムデータベースにとって新しいユーザーペルソナである、というアイデアです。眠らず、休まず、SQLを際限なく生成するユーザーです。私たちの主張は、リアルタイム分析データベースこそがこうしたエージェントにとって自然なコンテキストプロバイダーである、というものでした。なぜなら、新鮮なデータに対して高速で並行的かつ探索的なクエリを提供できるからで、これはまさにエージェントが依存するアクセスパターンです。1年間本番運用し、アーリーアダプターと緊密に連携した結果、この仮説は裏付けられました。

![](/writing/clickhouse-agents-beta-jp/clickhouse_agents_jun2026_image7_e65251f928.png)

エージェントは人間のアナリストの10〜100倍のクエリ量をバースト的に発火させ、リトライやタイムアウトはトークンを消費し負荷を増やします。数十億行に対するサブ秒レイテンシ、ペタバイト規模のストレージ、数千の並行クエリ、そしてエージェントトラフィックが拡大しても手頃なコスト効率、これらはClickHouseのようなプラットフォームの重要な特性です。最近のエンジン改善によりさらに良くなっており、過去1年で[最大6倍高速になったJoin](https://clickhouse.com/blog/join-me-if-you-can-clickhouse-vs-databricks-snowflake-join-performance)、[多段階の分散クエリ実行](https://clickhouse.com/blog/multi-stage-distributed-query-execution-clickhouse-cloud)、[全文検索のGA](https://clickhouse.com/blog/full-text-search-ga-release)などが含まれます。

これによりインサイトまでの時間が短縮されます。従来のパスはハンドオフを伴います。データエンジニアがクエリを書き、アナリストがダッシュボードを作り、ビジネスユーザーが結果を解釈する、各ステップが時間や日単位で測られます。ClickHouse Agentsを使えば、PMが「先週の解約急増の要因は?」と質問すれば、答え、その背後のクエリ、チャート、そして次に探求すべき質問が数秒で得られます。

## 次にやること

エキサイティングな新発表に加え、私たちは以下に向けてお客様と協力しています:

- より深いCloud統合。チャット内のより豊富な可視化と、SQLコンソールとのより緊密な結合。
- Agent API。ClickHouse Agentsで構築したエージェントへのプログラム的アクセス。
- 信頼性のフィードバックループ。[2026年1月にClickHouseに加わった](https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability)Langfuseとのネイティブ統合を活用し、ユーザーが評価を実行しコンテキストに影響を与えられるようにする。

## 今すぐ始める

ClickHouse Agentsは、すべてのClickHouse Cloudユーザーにパブリックベータとして提供されています。ClickHouseアカウントをお持ちであれば、SQLコンソール経由でClickHouse Agentsにアクセスするか、単に<https://ai.clickhouse.cloud/>を利用開始できます。ベータ版ですので、皆様のフィードバックだけが改善の道です。フォームや[コミュニティSlack](https://clickhouse.com/slack)からお寄せください。

ClickHouse上でエージェント分析を構築していてデザインパートナーになりたい方は、[ご連絡ください](https://clickhouse.com/company/contact)。

*AI/MLチーム、Danny Avila氏とLibreChatコミュニティ、基調講演ステージで一緒に登壇してくれたAnthropicとAWSの仲間たち、そしてエージェント分析で共に取り組んでくださっているすべてのお客様に大きな感謝を。私たちはまだ始まったばかりです。*
