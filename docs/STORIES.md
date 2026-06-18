# STORIES.md
**Project:** critical-knowledge-graph  
**Owner:** Product & Engineering Lead  
**Target Release:** MVP (v0.1) → Full Release (v1.0)  

---  

## Table of Contents
1. [Epics Overview](#epics-overview)  
2. [User Story Backlog](#user-story-backlog)  
   - [Epic 1 – Knowledge Capture & Modeling](#epic-1-knowledge-capture--modeling)  
   - [Epic 2 – Knowledge Exploration & Retrieval](#epic-2-knowledge-exploration--retrieval)  
   - [Epic 3 – Collaboration & Dependency Mapping](#epic-3-collaboration--dependency-mapping)  
   - [Epic 4 – Administration & Governance](#epic-4-administration--governance)  
3. [Prioritisation & MVP Scope](#prioritisation--mvp-scope)  

---  

## Epics Overview  

| Epic | Description | MVP Inclusion |
|------|-------------|----------------|
| **E1** | Capture, structure, and version critical knowledge from diverse sources (docs, tickets, code, chats). | ✅ |
| **E2** | Provide fast, contextual search & graph‑based exploration for any employee. | ✅ |
| **E3** | Visualise dependencies, ownership, and knowledge gaps; enable collaborative editing & review. | ✅ |
| **E4** | Admin controls, RBAC, audit logging, and data import/export. | ❌ (post‑MVP) |

---  

## User Story Backlog  

### Epic 1 – Knowledge Capture & Modeling  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E1‑US1** | **As a** System Administrator, **I want** to define a knowledge schema (entity types, relationships, attributes) **so that** the graph enforces consistent data modeling. | 1. UI to create/edit schema with drag‑and‑drop.<br>2. Schema persisted in PostgreSQL + pgGraph.<br>3. Validation errors shown on invalid entity creation.<br>4. Exportable as JSON‑Schema. |
| **E1‑US2** | **As a** Knowledge Engineer, **I want** to ingest existing Markdown, Confluence pages, and ticket data automatically **so that** legacy knowledge becomes part of the graph without manual entry. | 1. Connectors for Git, Confluence API, Jira API.<br>2. Configurable mapping rules (e.g., headings → `Topic`, code blocks → `Artifact`).<br>3. Idempotent import – re‑run does not duplicate nodes.<br>4. Import logs with success/failure counts. |
| **E1‑US3** | **As a** Team Member, **I want** to create a new knowledge node via a web form **so that** I can document a critical process quickly. | 1. Form fields respect current schema.<br>2. Inline markdown editor with preview.<br>3. Auto‑generated UUID and timestamps.<br>4. Node appears in graph view within 2 seconds. |
| **E1‑US4** | **As a** Knowledge Engineer, **I want** version control for each node (auto‑incremented revision, change diff) **so that** we can track evolution and roll back if needed. | 1. Every edit creates a new revision record.<br>2. UI shows diff (markdown side‑by‑side).<br>3. “Revert to revision X” button restores prior state.<br>4. Audit trail stored in immutable log table. |
| **E1‑US5** | **As a** System Administrator, **I want** to schedule periodic re‑indexing of the graph **so that** search relevance stays up‑to‑date with new imports. | 1. Scheduler (cron‑style) configurable via admin UI.<br>2. Re‑index job logs success/failure.<br>3. No downtime – index built in a shadow table and swapped atomically. |

### Epic 2 – Knowledge Exploration & Retrieval  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E2‑US1** | **As a** Employee, **I want** a full‑text search bar with autocomplete **so that** I can find relevant knowledge instantly. | 1. Search powered by vLLM + pgVector semantic embeddings.<br>2. Top‑10 results returned < 200 ms.<br>3. Highlight matching snippets.<br>4. Autocomplete suggestions based on entity names and tags. |
| **E2‑US2** | **As a** Employee, **I want** graph‑based navigation (node‑link view) **so that** I can explore related concepts visually. | 1. Interactive D3.js canvas showing nodes/edges.<br>2. Pan, zoom, and click‑to‑expand neighbours up to 2 hops.<br>3. Edge types colour‑coded (e.g., “depends‑on”, “documents”). |
| **E2‑US3** | **As a** New Hire, **I want** a “knowledge onboarding” wizard that surfaces the most critical nodes for my team **so that** I ramp up faster. | 1. Wizard asks for team/role selection.<br>2. Recommends top‑N nodes by centrality & recent activity.<br>3. Marks nodes as “read” and tracks progress. |
| **E2‑US4** | **As a** Employee, **I want** to filter search results by entity type, owner, or tag **so that** I can narrow down to the exact artifact I need. | 1. Facet UI with multi‑select checkboxes.<br>2. Filter applied client‑side without full page reload.<br>3. URL reflects filter state for sharing. |
| **E2‑US5** | **As a** Knowledge Engineer, **I want** an API endpoint (`/api/v1/graph/query`) that accepts Cypher‑like queries **so that** downstream tools can programmatically retrieve sub‑graphs. | 1. Authenticated via JWT.<br>2. Returns JSON‑LD with nodes & edges.<br>3. Rate‑limited (100 req/min per token).<br>4. Swagger/OpenAPI docs auto‑generated. |

### Epic 3 – Collaboration & Dependency Mapping  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E3‑US1** | **As a** Team Lead, **I want** to see a dependency heat‑map that highlights nodes with few owners or no recent updates **so that** I can allocate resources to knowledge gaps. | 1. Heat‑map visual (node size = number of dependants, colour = freshness).<br>2. Exportable CSV of “stale” nodes (> 90 days no edit). |
| **E3‑US2** | **As a** Employee, **I want** to comment on a knowledge node and @‑mention teammates **so that** we can discuss nuances directly on the source. | 1. Threaded comments stored in `node_comments` table.<br>2. Real‑time updates via WebSocket.<br>3. Notification sent to mentioned users (email + in‑app). |
| **E3‑US3** | **As a** Knowledge Engineer, **I want** a “review workflow” where a node must be approved by a designated owner before becoming searchable **so that** we maintain quality. | 1. Draft → Pending Review → Published states.<br>2. Review UI lists pending nodes with “Approve/Reject”.<br>3. Rejected nodes return to draft with reviewer feedback. |
| **E3‑US4** | **As a** Employee, **I want** to “subscribe” to a node or tag **so that** I receive change notifications relevant to my work. | 1. Subscription management page.<br>2. Digest email (daily) and instant push for critical changes.<br>3. Unsubscribe link in every notification. |
| **E3‑US5** | **As a** Team Lead, **I want** to assign ownership of nodes to specific users or groups **so that** accountability is clear. | 1. Owner field editable in node UI.<br>2. Ownership reflected in dependency heat‑map.<br>3. Ownership change logged with timestamp and actor. |

### Epic 4 – Administration & Governance (Post‑MVP)  

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E4‑US1** | **As a** System Administrator, **I want** role‑based access control (RBAC) with custom permission sets **so that** we can enforce least‑privilege policies. | 1. Roles: Admin, Reviewer, Contributor, Viewer.<br>2. Permissions configurable per‑entity type.<br>3. UI for role assignment and audit log of changes. |
| **E4‑US2** | **As a** Compliance Officer, **I want** immutable audit logs of all CRUD operations on knowledge nodes **so that** we can satisfy regulatory requirements. | 1. Logs written to append‑only table with cryptographic hash chain.<br>2. Exportable in CSV/JSON format.<br>3. Retention policy configurable (e.g., 7 years). |
| **E4‑US3** | As a **System Administrator**, **I want** data import/export (GraphML, JSON‑LD) **so that** we can migrate or backup the knowledge graph. | 1. Export all nodes/edges with schema metadata.<br>2. Import validates against current schema and reports conflicts.<br>3. Progress bar for large datasets (> 1 M nodes). |
| **E4‑US4** | **As a** System Administrator, **I want** multi‑tenant isolation (optional) **so that** we can host multiple client organisations on the same SaaS instance. | 1. Tenant ID stored on every entity.<br>2. Queries automatically scoped to tenant context.<br>3. Admin UI to create/manage tenants. |

---  

## Prioritisation & MVP Scope  

| Priority | Epic | Stories Included in MVP |
|----------|------|--------------------------|
| **P1** | E1 – Knowledge Capture & Modeling | US1, US2, US3, US4 |
| **P2** | E2 – Knowledge Exploration & Retrieval | US1, US2, US4 |
| **P3** | E3 – Collaboration & Dependency Mapping | US1, US2, US3 |
| **P4** | E4 – Administration & Governance | *Deferred to post‑MVP* |

**MVP Definition (v0.1)**  
- Core schema definition & versioned node creation.  
- Automated ingestion from at least two sources (Git markdown & Jira tickets).  
- Semantic search with autocomplete and basic graph view.  
- Review workflow to gate publishing.  
- Dependency heat‑map for team leads.  

All MVP stories are **shippable within a single sprint** (2 weeks) by a cross‑functional squad (frontend, backend, data‑engineer, QA).  

---  

*End of document.*
