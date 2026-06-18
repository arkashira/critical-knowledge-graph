# Critical Knowledge Graph (CKG) – Product Requirements Document (PRD)

**Document Version:** 1.0  
**Last Updated:** 2026‑06‑18  
**Author:** Senior Product/Engineering Lead, Axentx  

---  

## 1. Overview  

The **Critical Knowledge Graph (CKG)** is a knowledge‑management platform designed to help small‑ and medium‑size businesses (SMBs) capture, organize, and share the most critical operational knowledge that resides across people, processes, and systems. By turning tacit expertise into a structured, queryable graph, CKG reduces employee dependency risk, accelerates onboarding, and improves continuity when key personnel leave or shift roles.

---

## 2. Problem Statement  

| Symptom | Root Cause | Business Impact |
|---------|------------|-----------------|
| **Knowledge silos** – critical procedures, configs, and troubleshooting steps exist only in the heads of a few “subject‑matter experts”. | No central, searchable repository; knowledge is stored in ad‑hoc docs, chat logs, or personal notes. | High onboarding time, increased error rate, and costly downtime when experts are unavailable. |
| **Employee turnover risk** – loss of key staff leads to loss of institutional memory. | Lack of explicit documentation and hand‑off processes. | Project delays, missed SLAs, and revenue loss. |
| **Inefficient knowledge reuse** – teams reinvent solutions instead of reusing existing ones. | Knowledge is not discoverable or linked to related assets. | Duplicate effort, wasted engineering hours, slower product cycles. |

**Resulting Need:** A lightweight, graph‑based knowledge platform that captures *critical* information, surfaces dependencies, and enables rapid retrieval and sharing across the organization.

---

## 3. Target Users & Personas  

| Persona | Role | Primary Pain Point | How CKG Helps |
|---------|------|--------------------|---------------|
| **Operations Manager** | Oversees day‑to‑day processes | Cannot quickly locate SOPs or escalation paths. | Provides a searchable graph of processes, owners, and dependencies. |
| **Engineering Lead** | Manages codebases & infra | Knowledge about legacy systems is scattered. | Links code repositories, configs, and runbooks to graph nodes. |
| **HR / Talent Development** | Handles onboarding & succession planning | New hires spend weeks learning undocumented workflows. | Generates onboarding pathways and identifies knowledge gaps. |
| **Support Engineer** | Handles incidents | Needs fast access to troubleshooting steps and system topology. | Offers contextual, step‑by‑step guides tied to affected services. |

**Primary Market:** SMBs (10–250 employees) in SaaS, fintech, and IoT sectors that cannot afford large knowledge‑management teams but face high turnover or rapid scaling.

---

## 4. Product Goals  

| Goal | Success Metric (KPIs) | Target |
|------|-----------------------|--------|
| **Reduce knowledge‑dependency risk** | % of critical processes with ≥2 documented owners | ≥ 90% within 6 months |
| **Accelerate onboarding** | Avg. time to competency for new hires (days) | ↓ 30% vs baseline |
| **Improve incident resolution** | Mean Time To Resolve (MTTR) for support tickets | ↓ 20% vs baseline |
| **Drive usage adoption** | Active users / total seats (weekly) | ≥ 70% after 3 months |
| **Maintain data quality** | % of graph nodes with ≥1 source reference | ≥ 95% |

---

## 5. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **Graph Core Engine** | Store knowledge as nodes (entity, process, document, person) and edges (depends‑on, authored‑by, related‑to). Powered by a Neo4j‑compatible embedded store with ACID guarantees. | - CRUD API for nodes/edges.<br>- Graph can be exported/imported as JSON‑LD.<br>- Supports queries: shortest‑path, sub‑graph extraction, and attribute filters. |
| **P1** | **Criticality Tagging** | Ability to mark nodes/edges as *critical* (e.g., “must‑know for compliance”). Criticality propagates to dependent nodes. | - UI toggle to set critical flag.<br>- Automated propagation algorithm updates dependent nodes.<br>- Criticality view lists all critical items. |
| **P1** | **Source Integration Connectors** | Out‑of‑the‑box connectors for: <br>• Git repositories (code, config) <br>• Confluence / Notion pages <br>• Slack / Teams message archives <br>• CSV/Excel uploads | - Users can configure a connector via UI.<br>- Data is ingested, parsed, and linked to graph nodes.<br>- Connector runs on a schedule (default daily). |
| **P2** | **Contextual Search & Recommendations** | Full‑text search across node attributes with relevance ranking; recommendation engine suggests related nodes based on current query. | - Search bar returns results within 200 ms for 1 M node graph.<br>- Recommendations displayed for each result (≥2 related nodes). |
| **P2** | **Role‑Based Access Control (RBAC)** | Granular permissions at node/edge level (view, edit, tag critical). | - Admin can define roles & assign to users.<br>- Permissions enforced in API and UI. |
| **P2** | **Onboarding Path Builder** | Wizard that creates a learning path (ordered list of nodes) for a new role, tracking completion. | - Path can be exported as PDF.<br>- Completion % displayed per user. |
| **P3** | **Change Impact Analyzer** | When a node is edited, visualizes downstream dependencies that may be affected. | - Impact view highlights affected nodes/edges.<br>- Exportable impact report (PDF/CSV). |
| **P3** | **Mobile‑Friendly UI** | Responsive web UI with offline read‑only mode for field engineers. | - Core navigation works on iOS/Android browsers.<br>- Offline cache of last 7 days of viewed nodes. |
| **P4** | **AI‑Assisted Knowledge Extraction** | Leverage Axentx’s LLM (vLLM) to auto‑summarize long documents and suggest graph entities/relations. | - Summaries achieve ≥85 % ROUGE‑L vs human baseline.<br>- Auto‑suggested entities can be accepted/rejected. |

---

## 6. Scope  

### In‑Scope (Phase 1 – MVP)  
* Graph Core Engine, Criticality Tagging, Source Integration Connectors (Git & Confluence), RBAC, Contextual Search, Onboarding Path Builder, basic UI (desktop).  
* Deployment as a SaaS multi‑tenant service with per‑tenant data isolation.  

### Out‑of‑Scope (Phase 1)  
* Mobile‑only native apps (covered by responsive UI).  
* Full AI‑assisted extraction (deferred to Phase 2).  
* Advanced analytics dashboards beyond the KPI widgets listed.  

---

## 7. Technical Requirements  

| Area | Requirement |
|------|-------------|
| **Platform** | Node.js (v20) backend, Express, TypeScript. |
| **Graph Store** | Neo4j 5.x embedded (or Aura for cloud). Must support ACID transactions and graph algorithms. |
| **Connectors** | Use Axentx’s existing data ingestion framework (Python 3.11, asyncio). |
| **Search** | ElasticSearch 8.x for full‑text indexing; sync with graph via change streams. |
| **Auth** | OAuth2 / OpenID Connect; support SSO (Okta, Azure AD). |
| **Scalability** | Horizontal scaling of API tier; graph store sharding optional for >10 M nodes. |
| **Observability** | OpenTelemetry tracing, Prometheus metrics, Grafana dashboards. |
| **Compliance** | GDPR‑compliant data deletion per tenant request; audit logs for all edits. |
| **CI/CD** | GitHub Actions pipelines; automated unit, integration, and contract tests. |
| **Testing** | 80 % code coverage; end‑to‑end tests with Cypress for UI flows. |

---

## 8. Success Metrics & Measurement  

| Metric | Measurement Method | Target (12 weeks) |
|--------|--------------------|-------------------|
| **Criticality Coverage** | % of nodes tagged critical vs total critical processes identified by Ops leads. | ≥ 80% |
| **Onboarding Time** | Survey + ticket system timestamps (first task completion). | ↓ 30% |
| **MTTR Reduction** | Compare average ticket resolution time pre‑ vs post‑deployment (support logs). | ↓ 20% |
| **User Adoption** | Weekly active users / total seats (analytics). | ≥ 70% |
| **Data Freshness** | % of connector runs completed without errors. | ≥ 95% |
| **System Reliability** | 99.5 % uptime SLA (excluding planned maintenance). | Achieved |

---

## 9. Milestones & Timeline  

| Milestone | Duration | Owner |
|-----------|----------|-------|
| **Discovery & Architecture** | 2 weeks | Lead Architect |
| **Graph Engine & API** | 3 weeks | Backend Team |
| **Criticality Tagging & RBAC** | 2 weeks | Backend + Security |
| **Connectors (Git, Confluence)** | 3 weeks | Data Ingestion Squad |
| **Search Integration** | 2 weeks | Search Team |
| **Frontend MVP (Desktop)** | 4 weeks | Frontend Squad |
| **Onboarding Path Builder** | 2 weeks | Product Team |
| **QA & Security Testing** | 2 weeks | QA Lead |
| **Beta Release (Pilot 3 SMBs)** | 1 week | PM |
| **Feedback Incorporation** | 2 weeks | All Squads |
| **Public Launch** | — | PM & Marketing |

*Total estimated time to MVP: 12 weeks.*

---

## 10. Risks & Mitigations  

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Graph performance degrades >200 ms** | Poor UX, low adoption | Benchmark early; implement pagination & caching; plan for sharding. |
| **Data privacy breach** | Legal & reputational damage | End‑to‑end encryption at rest/in‑flight; strict RBAC; regular audits. |
| **Connector failures (e.g., Git auth)** | Stale knowledge, loss of trust | Retry logic with exponential back‑off; alerting on failure; UI for manual re‑sync. |
| **Scope creep (AI extraction too early)** | Delayed launch | Enforce phase gates; lock AI features to Phase 2 backlog. |
| **Low SMB willingness to pay** | Revenue risk | Early pricing validation during pilot; bundle with onboarding consulting. |

---

## 11. Open Questions  

1. **Pricing Model:** Subscription tier vs per‑seat vs usage‑based (graph size).  
2. **Tenant Isolation:** Will we use separate Neo4j instances per tenant or multi‑tenant with label segregation?  
3. **Export Formats:** Need for compliance‑grade PDF/A or XML exports?  

*These will be resolved in the next sprint planning session.*

---  

*Prepared for internal review. All stakeholders are invited to comment within the next 5 business days.*
