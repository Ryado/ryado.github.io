---
title: 'ClickHouse Agents: Claude-powered agentic analytics, now in public beta'
date: '2026-06-09'
source: clickhouse
canonical_url: https://clickhouse.com/blog/clickhouse-agents-beta
coauthors: []
tags:
- product
summary: text
reading_time: 1
content_hash: 5b1c36f5d69669f2
---

After running agentic analytics in production for more than a year at ClickHouse, at [Open House 2026](https://clickhouse.com/blog/open-house-2026-day-1) in San Francisco, we announced the public beta of [ClickHouse Agents](https://clickhouse.com/docs/cloud/features/ai-ml/agents), a fully managed agentic analytics service in ClickHouse Cloud, powered by Claude.

ClickHouse Agents is a native AI experience inside ClickHouse Cloud. With ClickHouse Agents, you can build agents easily with no code required where users can ship agents grounded in their live ClickHouse data, with no SQL or setup required. You put those agents to work through a fully managed chat experience right in the Cloud console, with no setup and no separate environment to host.

## What ClickHouse Agents is

ClickHouse Agents is built on [LibreChat](https://github.com/danny-avila/LibreChat), the battle-tested open-source AI platform, and runs fully managed inside ClickHouse Cloud. At its core is the no-code agent builder, which lets anyone, whether analyst, PM, data engineer, or executive, define, configure, and ship agents grounded in their ClickHouse data. ClickHouse Agents also comes with an out-of-box chat interface, a sandboxed code interpreter, shareable artifacts, skills, memories, and multi-agent workflows. Agents connect natively to ClickHouse and to any MCP-compatible system, pulling context from wherever it already lives.
