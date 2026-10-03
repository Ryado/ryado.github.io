---
title: ClickPipes is Now Generally Available
date: '2023-09-26'
source: clickhouse
canonical_url: https://clickhouse.com/blog/clickpipes-is-generally-available
coauthors: []
tags:
- product
summary: Extracting valuable insights for real-time analytics applications often depends on the availability of fresh and clean data.
reading_time: 3
content_hash: 99a53f0085c2fda5
---

- [Blog](/blog)
- [Product](/blog?category=product)

![ryadh](/writing/clickpipes-is-generally-available/Ryadh_d50dc0546c.png)

[Ryadh Dahimene](/authors/ryadh-dahimene)

Sep 26, 2023 · 3 minutes read

Extracting valuable insights for real-time analytics applications often depends on the availability of fresh and clean data. Streamlined access to this data is a game changer for data-driven decision making.

Today at ClickHouse, we are thrilled to [announce the general availability of ClickPipes](/blog/clickhouse-announces-clickpipes?loc=clickpipes-ga-blog), our continuous data ingestion service for [ClickHouse Cloud](/cloud?loc=clickpipes-ga-blog).

This represents a significant milestone for ClickHouse Cloud. Since ClickPipes was initially announced mid-July in [private beta](/blog/clickhouse-cloud-clickpipes-for-kafka-managed-ingestion-service?loc=clickpipes-ga-blog), it has been used by organizations to successfully unlock real-time analytics use-cases, allowing them to ingest data easily and focus on the important part: extracting insights thanks to ClickHouse’s unparalleled performance.

For GA, we added the following features to ClickPipes:

- Support for Confluent Cloud’s schema registry (JSON_SR)
- Support for Amazon MSK
- ClickPipes specific metrics, available in the details panel to display count and size of ingested data + errors if any
- Support for more data types including FixedString, Date, DateTime, Tuple and Array, JSON
- UI/UX and reliability improvements

![clickpipes_1mn-min.gif](/writing/clickpipes-is-generally-available/clickpipes_1mn_min_0c61fc05dc.gif)

Key ClickPipes features include:

- **Easy and intuitive data onboarding**: Setting up a new ingestion pipeline takes just a few steps. Select an incoming data source and format, tune your schema, and let your pipeline run.
- **Built for continuous ingestion**: ClickPipes manages your continuous ingestion pipelines so that you don’t have to. Set up your pipeline and let us handle the rest.
- **Designed for speed and scale**: ClickPipes provides the scalability you need to handle increasing data volumes, ensuring your systems can handle future demands effortlessly.
- **Unlock your real time analytics**: Built leveraging our deep expertise in real time data management systems, ClickPipes handles the complexities of real time ingestion for optimal performance.

![Screenshot 2023-09-26 at 12.31.29.png](/writing/clickpipes-is-generally-available/Screenshot_2023_09_26_at_12_31_29_6f3bdb8962.png)

## Give ClickPipes a spin today!

You can find the documentation and a tutorial about how to [get started here](https://clickhouse.com/docs/en/integrations/clickpipes). As always, we’d love to hear your feedback and suggestions ([contact us](/company/contact?loc=clickpipes-ga-blog)).

## Links:

- [Press Release](/blog/clickhouse-announces-clickpipes?loc=clickpipes-ga-blog)
- [ClickPipes Website](/cloud/clickpipes?loc=clickpipes-ga-blog)
- [Video demonstration](/videos/clickpipes-demo?loc=clickpipes-ga-blog)
- [Documentation](https://clickhouse.com/docs/en/integrations/clickpipes)

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30-day trial, continue with a pay-as-you-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

---

Share this post

- [![Y Combinator icon](/writing/clickpipes-is-generally-available/ycombinator.37q2g-no9bowl.svg)](https://news.ycombinator.com/submitlink?u= "Share on Y Combinator")
- [![X icon](/writing/clickpipes-is-generally-available/x.3nm91lx52ia7n.svg)](https://x.com/intent/tweet?text= "Share on X")
- [![Bluesky icon](/writing/clickpipes-is-generally-available/bluesky.292c8t8kns7n1.svg)](https://bsky.app/intent/compose?text= "Share on Bluesky")
- [![Facebook icon](/writing/clickpipes-is-generally-available/facebook.32ysyflv7kktz.svg)](https://www.facebook.com/sharer/sharer.php?u= "Share on Facebook")
- [![LinkedIn icon](/writing/clickpipes-is-generally-available/linkedin.37911rnwi-sdg.svg)](https://www.linkedin.com/sharing/share-offsite/?url= "Share on LinkedIn")

### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!

## Recent posts

[View all Blogs](/blog)

![what is direct io and why does clickhouse managed postgres use it for backups](/writing/clickpipes-is-generally-available/What_is_Direct_IO_and_why_does_Click_House_Managed_Postgres_use_it_for_backups_d.png)

Engineering

### [What is direct I/O, and why does ClickHouse Managed Postgres use it for backups?](/blog/direct-io-managed-postgres-backups)

Kaushik Iska · Oct 2, 2026

![linkedin customer story cover](/writing/clickpipes-is-generally-available/Linked_In_Customer_Story_Cover_c89bdd42f7.jpg)

User stories

### [How LinkedIn extended ClickHouse from distributed tracing to metric discovery and analytics](/blog/linkedin-observability-at-scale)

ClickHouse · Oct 1, 2026

![introducing scim provisioning in clickhouse cloud](/writing/clickpipes-is-generally-available/Introducing_SCIM_Provisioning_in_Click_House_Cloud_410e5b1cf8.jpg)

Product

### [Introducing SCIM Provisioning in ClickHouse Cloud](/blog/introducing-scim-provisioning-in-clickhouse-cloud)

Raymond Lee · Sep 30, 2026

![gulcin updated the title](/writing/clickpipes-is-generally-available/gulcin_updated_the_title_54d37d322a.png)

Product

### [pg_clickhouse & chdb updates: Encoding, nesting, and types](/blog/pg_clickhouse-chdb)

David Wheeler · Sep 30, 2026

[View all Blogs](/blog)

## Follow us

[![X](/writing/clickpipes-is-generally-available/x.3nm91lx52ia7n.svg)](https://x.com/ClickhouseDB "X")[![Bluesky](/writing/clickpipes-is-generally-available/bluesky.292c8t8kns7n1.svg)](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/writing/clickpipes-is-generally-available/slack.2_pspehyws_jz.svg)](/slack "Slack")[![Github](/writing/clickpipes-is-generally-available/github.3ofxqpa2uzt_a.svg)](https://github.com/ClickHouse/ClickHouse "Github")[![Telegram](/writing/clickpipes-is-generally-available/telegram.0054ol1lpoidb.svg)](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/writing/clickpipes-is-generally-available/meetup.2tf1x11zaaepo.svg)](https://www.meetup.com/pro/clickhouse "Meetup")[![RSS](/writing/clickpipes-is-generally-available/rss.1pu3aqlsglh-q.svg)](/rss.xml "RSS")
