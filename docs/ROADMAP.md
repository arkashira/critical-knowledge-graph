# ROADMAP.md – critical-knowledge-graph

## Vision
Create a **knowledge‑management platform** that lets small‑ and medium‑size businesses **capture, organize, and surface critical system knowledge** so teams can operate with minimal dependency on any single employee.  

The product will evolve from a **lean MVP** that validates the core value‑prop (knowledge capture + search) into a **full‑featured knowledge graph** with automated dependency mapping, contextual recommendations, and enterprise‑grade governance.

---

## MVP (Must‑Have for Launch) – **Critical Knowledge Capture & Search**
| Milestone | Scope | Success Criteria |
|-----------|-------|------------------|
| **M1 – Core Data Model** | • Entity types: *System*, *Component*, *Process*, *Person*, *Document*.<br>• Relationships: *owns*, *depends_on*, *documents*, *maintains*.<br>• Store in a **Neo4j** graph (or open‑source equivalent) with versioned schema migrations. | ✅ Schema validated by integration tests.<br>✅ Ability to import/export JSON‑LD snapshots. |
| **M2 – Knowledge Ingestion UI** | • Web UI (React + Vite) for manual entry of entities & relationships.<br>• Bulk CSV/JSON import wizard (templates provided).<br>• Markdown editor with attachment support. | ✅ 100 % of fields editable inline.<br>✅ Import of ≥10 k rows without errors. |
| **M3 – Full‑Text & Graph Search** | • ElasticSearch (or OpenSearch) for text indexing.<br>• Graph traversal API to answer “who owns this component?” and “what depends on X?”.<br>• UI search bar with filters (type, owner, tag). | ✅ <200 ms query latency on 1 M node graph.<br>✅ Search results ranked by relevance & dependency depth. |
| **M4 – Access Control (MVP)** | • Role‑based permissions: *Admin*, *Editor*, *Viewer*.<br>• OAuth2 integration (Google, Azure AD). | ✅ Admin can manage roles.<br>✅ Editors can edit but not delete core entities. |
| **M5 – Deployment & Ops** | • Docker‑Compose for local dev.<br>• Helm chart for Kubernetes (GKE/EKS) with autoscaling.<br>• Basic health‑checks, logging, and Prometheus metrics. | ✅ One‑click deploy to staging.<br>✅ 99.5 % uptime in CI smoke test. |
| **M6 – Validation & Feedback Loop** | • In‑app “knowledge usefulness” rating (thumbs up/down).<br>• Automated email survey after 30 days of usage. | ✅ ≥70 % of pilot users rate knowledge items as “useful”. |

**MVP Completion Target:** **8 weeks** from kickoff (2 sprints for core, 1 sprint for UI, 1 sprint for search & auth, 1 sprint for ops & validation).

---

## Post‑MVP Roadmap

### Phase 1 – **v1.0: Collaboration & Automation** (Weeks 9‑20)

| Theme | Deliverables | KPI |
|-------|--------------|-----|
| **Real‑time Collaboration** | • Inline comments & change history.<br>• @‑mentions & notifications (Slack/Webhook). | ≥80 % of edits accompanied by a comment in pilot. |
| **Automated Dependency Discovery** | • Agent that parses code repositories (GitHub, GitLab) to auto‑create *Component* & *depends_on* edges.<br>• Schedule nightly scans. | ≥60 % of dependencies auto‑populated after first scan. |
| **Knowledge Validation Engine** | • ML model (fine‑tuned on `system-user-assistant` dataset) to flag stale or orphaned nodes.<br>• Dashboard for “At‑Risk Knowledge”. | Reduce orphaned nodes by 40 % in 30 days. |
| **Export & Integration** | • REST & GraphQL APIs.<br>• Export to Confluence, Notion, and CSV.<br>• Webhooks for external ticketing (Jira). | ≥3 integrations active in beta customers. |
| **Enhanced Security** | • SSO SAML + MFA.<br>• Row‑level security for sensitive components. | Pass internal security audit. |

**Release Goal:** **v1.0** – a collaborative, semi‑automated knowledge graph ready for broader beta (≈30 SMB customers).

---

### Phase 2 – **v2.0: Intelligence & Enterprise‑Ready** (Weeks 21‑36)

| Theme | Deliverables | KPI |
|-------|--------------|-----|
| **Contextual Recommendations** | • Knowledge‑graph‑driven suggestions (e.g., “When editing Component X, also review Document Y”).<br>• Personalised feed per user based on role & activity. | ↑ 20 % of recommended items accessed. |
| **Advanced Analytics** | • Dependency impact analysis (what breaks if X is removed).<br>• Heatmaps of knowledge usage per team. | Reduce incident time‑to‑resolution by 15 %. |
| **Enterprise Governance** | • Approval workflows for critical knowledge changes.<br>• Auditable change logs with tamper‑evidence (hash chaining). | ≥95 % compliance in enterprise pilot. |
| **Scalable Architecture** | • Migrate graph store to **Neo4j Aura** or **Amazon Neptune** for multi‑region replication.<br>• Event‑driven pipeline (Kafka) for ingest scaling. | Support ≥10 M nodes with <300 ms query latency. |
| **Self‑Service Onboarding** | • Guided product tour & template libraries (IT ops, DevOps, Finance).<br>• Marketplace of community‑contributed knowledge packs. | ≤5 min to create first knowledge graph. |

**Release Goal:** **v2.0** – an intelligent, secure platform suitable for enterprise contracts and large‑scale deployments.

---

## Milestone Timeline (High‑Level)

| Week | Milestone |
|------|-----------|
| 1‑2  | Project kickoff, team alignment, infrastructure provisioning |
| 3‑6  | MVP Core Data Model & Ingestion UI |
| 7‑8  | Search, Auth, Ops, Validation loop |
| 9‑12 | Real‑time Collaboration & Notification system |
| 13‑16| Automated Dependency Discovery & Validation Engine |
| 17‑20| Export APIs, Security hardening, Beta release (v1.0) |
| 21‑24| Recommendation engine prototype |
| 25‑28| Analytics dashboards & impact analysis |
| 29‑32| Enterprise governance & audit trails |
| 33‑36| Scaling infra, self‑service onboarding, v2.0 GA |

---

## Success Metrics (Post‑Launch)

| Metric | Target (12 mo) |
|--------|----------------|
| **Customer Retention** | ≥85 % |
| **Net Revenue Retention** | ≥110 % |
| **Knowledge Capture Rate** | ≥200 new entities / month per customer |
| **Search Satisfaction (CSAT)** | ≥4.5 / 5 |
| **Time‑to‑Onboard** | ≤15 min for first graph |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| **Graph performance at scale** | Early benchmark with synthetic 10 M node dataset; adopt sharding strategy in Phase 2. |
| **User adoption (knowledge entry friction)** | Provide import templates, AI‑assisted entity extraction, and gamified contribution rewards. |
| **Data security & compliance** | Implement SSO/MFA from MVP; add audit logs and encryption in Phase 2. |
| **Dependency discovery accuracy** | Start with language‑agnostic regex parsers; iterate with ML models trained on `auto` and `instr-resp` datasets. |

---

*Prepared by the Critical Knowledge Graph product team – Axentx*
