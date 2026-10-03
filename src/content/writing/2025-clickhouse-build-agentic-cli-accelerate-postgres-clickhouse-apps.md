---
title: 'clickhouse.build: An agentic CLI to accelerate Postgres apps with ClickHouse'
date: '2025-12-02'
source: clickhouse
canonical_url: https://clickhouse.com/blog/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps
coauthors:
- Pete Hampton
- Al Brown
tags:
- product
summary: clickhouse.build is an open source, agentic CLI that accelerates the adoption of ClickHouse within your existing Postgres-backed TypeScript application.
reading_time: 1
content_hash: 2b368783d0cf6c7b
---

[clickhouse.build](https://github.com/ClickHouse/clickhouse.build) is an open source, agentic CLI that accelerates the adoption of ClickHouse within your existing Postgres-backed TypeScript application. The goal is not to replace Postgres, but to seamlessly combine it with ClickHouse for analytical workloads, using the strengths of each database together, within the same application.

It uses a multi-agent workflow that:

- Scans your Postgres-backed codebase to identify analytical queries (whether SQL in-line or ORM-based)
- Determines which tables are required to support those analytical queries and creates a plan.
- Helps to automatically sync the relevant tables to ClickHouse Cloud using ClickPipes API.
- Rewrites the relevant portions of the code so that it uses ClickHouse for analytics and Postgres for transactions, while keeping the application backwards-compatible by introducing a feature flag.

clickhouse.build is intended as an accelerator, and can help you to have a working proof of concept (PoC) in under an hour. You can use the PoC to evaluate how your application performs with a combined Postgres+ClickHouse backend.

Already evaluating Postgres + ClickHouse? [Skip to how it works](#how-clickhousebuild-works), or read on to understand why these two databases are so good together.

![chbuild.png](/writing/clickhouse-build-agentic-cli-accelerate-postgres-clickhouse-apps/chbuild_8f68f3f55e.png)
