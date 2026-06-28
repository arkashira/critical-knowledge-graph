# tech-spec.md — critical-knowledge-graph (v1)

## Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | **TypeScript 5.x** (strict) | One language across API + web; large hiring pool for SMB-targeted SaaS |
| API framework | **Fastify 4** (Node 20 LTS) | ~2–3× Express throughput, schema-first validation via JSON Schema, first-class TS types |
| Web/UI | **Next.js 14 (App Router) + React 18** | SSR for SEO landing + auth'd app in one deploy; React Flow for the graph canvas |
| Graph viz | **React Flow 11** | Mature, free; renders the dependency/knowledge graph without a license fee |
| ORM | **Prisma 5** | Type-safe Postgres access; migrations baked in; pgvector via `Unsupported("vector")` |
| Background jobs | **BullMQ** on Redis | Embedding generation, staleness sweeps, digest emails |
| Search/embeddings | **pgvector** + `text-embedding-3-small` (OpenAI) | "Who knows X?" / semantic doc search without standing up a separate vector DB. Reuse Axentx BRAIN pattern |
| Auth | **Lucia v3** (or Clerk free tier if speed > control) | Session-based, no per-MAU cost at v1 scale |

**Decision:** Postgres is the single source of truth — relational (people, systems, ownership edges) **and** vector (pgvector) in one DB. No Neo4j at v1; graph depth is shallow (≤3 hops: person→system→knowledge-doc), so recursive CTEs outperform the operational cost of a dedicated graph DB. Revisit Neo4j only if traversal queries exceed ~4 hops or 50k+ edges.

## Hosting (free-tier-first)

| Component | Platform | Free tier | Upgrade trigger |
|---|---|---|---|
| Web + API | **Railway** (monorepo, 2 services) | $5 credit/mo, sleeps idle | >500 MAU → Hobby $5/svc |
| Postgres + pgvector | **Neon** | 0.5 GB, autoscale-to-zero, branching | >10 GB or >190 compute-hrs |
| Redis (jobs) | **Upstash Redis** | 10k cmd/day, 256 MB | >10k cmd/day |
| Object storage (attachments) | **Cloudflare R2** | 10 GB + zero egress | >10 GB |
| Email (digests, invites) | **Resend** | 3k emails/mo, 100/day | >3k/mo → $20 |
| DNS/CDN/WAF | **Cloudflare** | Free | n/a |

**Total v1 infra cost: $0** until ~first paying cohort. Neon branching gives every PR an isolated DB for CI.

## Data model

`orgs` — id, name, plan (`free|team|business`), seat_limit, created_at
`users` — id, org_id (FK), email (unique), name, role (`admin|editor|viewer`), title, department, status (`active|departing|offboarded`), last_active_at
`systems` — id, org_id, name, type (`service|tool|process|vendor|account`), criticality (`1-5`), description, repo_url, runbook_url, created_at
`ownerships` — id, system_id (FK), user_id (FK), role (`primary|backup|contributor`), confidence (`0-1`), **bus_factor_flag** (bool, derived), created_at — *the dependency edge*
`knowledge_docs` — id, org_id, system_id (FK, nullable), author_id, title, body (markdown), embedding `vector(1536)`, status (`draft|reviewed|stale`), reviewed_at, version, created_at
`doc_links` — id, doc_id, target_type (`system|user|doc`), target_id — *the knowledge graph edges*
`questions` — id, org_id, asker_id, system_id (nullable), title, body, answered_doc_id (nullable), status, created_at — *captures tacit knowledge on demand*
`risk_snapshots` — id, org_id, period (date), bus_factor_score, single_owner_systems (jsonb), coverage_pct — *time-series for the dashboard*
`audit_log` — id, org_id, actor_id, action, entity_type, entity_id, meta (jsonb), created_at

**Key derived metric — `bus_factor`:** per `system`, count of distinct `primary`/`backup` owners with ≥1 reviewed `knowledge_doc`. A system with 1 owner and 0 reviewed docs = **critical single point of failure** → drives the headline dashboard number that sells the product.

Indexes: `knowledge_docs.embedding` → HNSW (pgvector); `ownerships(system_id, user_id)`; `knowledge_docs.status` partial on `stale`.

## API surface

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/systems` | Register a critical system/process |
| `GET` | `/v1/systems/:id/risk` | Bus-factor + owner coverage + stale-doc count for one system |
| `POST` | `/v1/ownerships` | Assign person→system owner edge (primary/backup) |
| `POST` | `/v1/docs` | Create knowledge doc; async-embeds + links to system/people |
| `GET` | `/v1/search?q=` | Semantic "who/what knows X" — pgvector cosine over docs + owners |
| `GET` | `/v1/graph?org_id=` | Full nodes+edges payload for the React Flow dependency canvas |
| `GET` | `/v1/risk/dashboard` | Org-wide bus-factor score, single-owner systems, coverage % trend |
| `POST` | `/v1/offboarding/:userId/plan` | Generate knowledge-transfer checklist for a departing employee |
| `POST` | `/v1/questions` | Ask a question; routes to likely owner, captures answer as a doc |
| `GET` | `/v1/digest/preview` | Weekly "knowledge-risk" email content (stale docs, new SPOFs) |

All routes JSON-Schema validated (Fastify), org-scoped, paginated via cursor where list-returning.

## Security model

- **Auth:** Session cookies (HttpOnly, Secure, SameSite=Lax) via Lucia; 30-day rolling sessions. Email magic-link + password. OAuth (Google Workspace) at v1.1 — most SMB targets are GWS shops.
- **Tenancy isolation:** Every query carries `org_id` from the session, enforced at the Prisma middleware layer (not just app code) + Postgres **Row-Level Security** policies as defense-in-depth. No cross-org reads possible even on a query bug.
- **RBAC:** `admin` (billing, seats, delete), `editor` (CRUD docs/systems), `viewer` (read + ask). Offboarding actions require `admin`.
- **Secrets:** Railway/Neon env vars only; never in repo. `dotenv-vault` for local. OpenAI key server-side only — embeddings never called from the browser.
- **IAM:** Least-privilege service tokens — R2 scoped to one bucket, Neon role without superuser, Resend domain-restricted sending key.
- **Data:** Encryption at rest (Neon/R2 default) + TLS in transit. PII minimized — store names/titles/emails only; offboarding data deletable on request (GDPR/contractual). Rate-limit auth + search endpoints (Fastify `@fastify/rate-limit`, Redis-backed).

## Observability

- **Logs:** **Pino** (Fastify-native) → structured JSON, shipped to **Axiom** (free 500 GB/mo). Every log line carries `org_id`, `req_id`, `user_id`. Audit-relevant mutations also written to `audit_log` table.
- **Metrics:** **Prometheus** endpoint (`/metrics`, internal) scraped by **Grafana Cloud free**. Golden signals + product KPIs: `bus_factor_score`, `docs_created`, `stale_doc_ratio`, embedding-job latency, search p95.
- **Traces:** **OpenTelemetry** SDK auto-instrumenting Fastify + Prisma + BullMQ → **Grafana Tempo** (free tier). Trace the slow path: `/v1/search` → embed → pgvector → rank.
- **Errors:** **Sentry** free (5k events/mo) for both Next.js and API, source-mapped.
- **Uptime:** Cloudflare health check → `/healthz` (DB + Redis ping).

## Build/CI

- **Monorepo:** **Turborepo** + pnpm workspaces (`apps/web`, `apps/api`, `packages/db`, `packages/ui`).
- **CI:** GitHub Actions on PR — lint (Biome), typecheck (`tsc --noEmit`), test (Vitest + Testcontainers Postgres+pgvector), Prisma migrate-diff check, build. Neon branch DB per PR for integration tests.
- **CD:** Railway auto-deploys `main`; PR previews on Railway environments. DB migrations gated via `prisma migrate deploy` as a pre-deploy step (fails closed).
- **Quality gates:** Block merge on type errors, <60% coverage on `packages/db` + API handlers, or failing migration check. Dependabot weekly; `pnpm audit` in CI (high/critical = fail).
- **Release:** Trunk-based, squash-merge, conventional commits → auto-changelog.