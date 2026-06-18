# REQUIREMENTS.md

## Project Overview
**Project Name:** critical-knowledge-graph  
**Product Category:** Knowledge Management & Employee Dependency Reduction Platform  
**Target Customers:** Small and medium businesses (SMBs) that need to capture, organize, and disseminate critical system knowledge across teams to mitigate single‑point‑of‑failure knowledge loss.  

The platform will ingest structured and unstructured knowledge sources, construct a graph‑based representation of critical concepts, dependencies, and ownership, and expose intuitive UI/UX and API endpoints for discovery, contribution, and impact analysis.

---

## 1. Functional Requirements  

| ID | Description | Acceptance Criteria |
|----|-------------|----------------------|
| **FR‑1** | **Knowledge Ingestion** – Import data from multiple sources (documents, code repositories, ticketing systems, wikis, chat logs). | • Connectors for Markdown, PDF, CSV, Git (via GitHub API), Jira, Confluence, Slack.<br>• Successful ingestion logs each source with timestamp and source metadata.<br>• Duplicate detection prevents re‑ingesting identical records. |
| **FR‑2** | **Entity Extraction & Classification** – Automatically extract entities (services, APIs, databases, configs, procedures) and classify them into a predefined taxonomy. | • Uses the internal `instr-resp` dataset + fine‑tuned LLM (vLLM) to achieve ≥ 85 % F1 on a held‑out validation set.<br>• Extraction results are stored with confidence scores. |
| **FR‑3** | **Graph Construction** – Build a directed knowledge graph where nodes represent entities and edges represent dependencies/relationships (e.g., “calls”, “stores data in”, “owned by”). | • Graph stored in a Neo4j (or open‑source equivalent) instance.<br>• Supports incremental updates without full recompute.<br>• Graph schema versioned; migration scripts provided. |
| **FR‑4** | **Ownership & Responsibility Mapping** – Associate each node with one or more owners (employees, teams). | • Owners can be linked via corporate directory integration (e.g., Azure AD, Okta).<br>• UI shows current owners and change‑history audit trail. |
| **FR‑5** | **Search & Discovery** – Provide full‑text and graph‑aware search for users to locate knowledge quickly. | • Keyword search returns ranked results with relevance scores.<br>• Graph traversal queries (e.g., “show all services downstream of Service X”). |
| **FR‑6** | **Impact Analysis** – When a node is marked as “critical” or “at risk”, automatically surface downstream dependencies and affected owners. | • UI visualizes impact heat‑map.<br>• Exportable report (PDF/CSV) summarizing risk exposure. |
| **FR‑7** | **Collaboration & Editing** – Allow authorized users to create, edit, and comment on nodes/edges. | • Real‑time collaborative editing with optimistic concurrency control.<br>• Version history with rollback capability. |
| **FR‑8** | **Access Control** – Role‑based permissions (Viewer, Contributor, Owner, Admin). | • Permissions enforced at API and UI layers.<br>• Auditable logs for all write actions. |
| **FR‑9** | **API Layer** – RESTful + GraphQL endpoints for external integration. | • CRUD operations for nodes/edges.<br>• Bulk import/export endpoints.<br>• Swagger/OpenAPI documentation. |
| **FR‑10** | **Reporting Dashboard** – Executive view showing knowledge coverage, criticality distribution, and knowledge‑gap metrics. | • Charts refreshed at most every 5 minutes.<br>• Exportable snapshots. |
| **FR‑11** | **Data Export/Import** – Enable full backup and restore, and migration from other KM tools (e.g., Confluence, Notion). | • Export in JSON‑LD and CSV formats.<br>• Import wizard validates schema compliance. |
| **FR‑12** | **Notification System** – Alert owners when their critical nodes are updated, deprecated, or flagged for review. | • Email + Slack webhook integrations.<br>• Configurable notification preferences per user. |

---

## 2. Non‑Functional Requirements  

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | • Ingestion pipeline processes ≥ 10 k records/minute on a standard 8‑core VM.<br>• Search latency ≤ 200 ms for typical queries (≤ 5 k results). |
| **NFR‑2** | **Scalability** | • Horizontal scaling of ingestion workers and graph DB up to 1 M nodes and 5 M edges without > 30 % performance degradation.<br>• Stateless API services behind a load balancer. |
| **NFR‑3** | **Reliability** | • 99.9 % uptime SLA for API endpoints.<br>• Automated daily backups with a 7‑day retention window.<br>• Graceful degradation: if graph DB is unavailable, fallback to read‑only cached search index. |
| **NFR‑4** | **Security** | • Data at rest encrypted (AES‑256).<br>• TLS 1.3 for all network traffic.<br>• OAuth 2.0 / OpenID Connect for authentication.<br>• Role‑based access control enforced per NFR‑8.<br>• Regular vulnerability scans (monthly) and penetration testing (quarterly). |
| **NFR‑5** | **Compliance** | • GDPR‑compatible data handling (right to be forgotten, data export).<br>• Support for SOC‑2 Type II controls (audit logs, change management). |
| **NFR‑6** | **Observability** | • Structured logging (JSON) with correlation IDs.<br>• Metrics exposed via Prometheus (ingestion rate, query latency, error rates).<br>• Grafana dashboards for ops monitoring. |
| **NFR‑7** | **Maintainability** | • Codebase follows Axentx’s Python/TypeScript style guide.<br>• 80 %+ unit test coverage; integration tests for all connectors.<br>• CI/CD pipeline with automated lint, test, and security checks. |
| **NFR‑8** | **Usability** | • UI complies with WCAG 2.1 AA accessibility standards.<br>• Responsive design for desktop and tablet browsers.<br>• Contextual help and onboarding tutorial for first‑time users. |
| **NFR‑9** | **Portability** | • Deployable via Docker Compose for local dev and Helm charts for Kubernetes (GKE/EKS/AKS). |
| **NFR‑10** | **Data Governance** | • Metadata tagging for source provenance, ingestion timestamp, and confidence score.<br>• Immutable audit trail for all edits (append‑only log). |

---

## 3. Constraints  

1. **Technology Stack** – Must leverage existing Axentx assets:  
   - Inference via **vLLM** for entity extraction.  
   - Graph storage using an open‑source solution compatible with Neo4j query language (Cypher).  
   - Front‑end built with React + TypeScript (aligned with other Axentx products).  

2. **Data Licensing** – Only datasets with permissive licenses (Apache‑2.0, MIT, CDLA‑Permissive‑2.0, CC‑BY‑4.0) may be used for model fine‑tuning.  

3. **Resource Limits** – Initial production environment limited to a single 8‑core VM (16 GB RAM) for ingestion; must scale out later via container orchestration.  

4. **Time‑to‑Market** – MVP (minimum viable product) must be deliverable within **12 weeks** from kickoff.  

5. **Integration Boundaries** – Must not duplicate functionality already shipped in **iceoryx2** (IPC library) or other Axentx products; focus strictly on knowledge graph capabilities.  

---

## 4. Assumptions  

| ID | Assumption |
|----|------------|
| **A‑1** | Customers have an existing corporate directory (Azure AD/Okta) that can be queried for user‑team mappings. |
| **A‑2** | Source documents are in English; multilingual support is out of scope for the MVP. |
| **A‑3** | Clients will provide API tokens/credentials for external systems (GitHub, Jira, Slack) during onboarding. |
| **A‑4** | The underlying LLM model fine‑tuned on `instr-resp` and `system‑user‑assistant` datasets will achieve the required extraction accuracy without additional domain data. |
| **A‑5** | Network connectivity between the platform and client‑hosted services is unrestricted (no outbound firewall blocking). |
| **A‑6** | Users will have modern browsers (Chrome ≥ 108, Edge ≥ 108, Firefox ≥ 107). |

--- 

*Document version: 1.0 – 2026‑06‑18*  
*Prepared by: Senior Product/Engineering Lead, Axentx*
