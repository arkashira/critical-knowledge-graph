# TECH_SPEC.md

## Critical Knowledge Graph (CKG)

**Product**: AxentX knowledge‑management platform for small‑/medium‑businesses (SMBs)  
**Goal**: Enable teams to capture, model, and query critical system knowledge, reducing single‑point‑of‑failure dependencies and accelerating onboarding.  

---

### 1. Architecture Overview

```
+-------------------+        +-------------------+        +-------------------+
|   Front‑End UI    | <---> |   API Gateway     | <---> |   Auth Service    |
+-------------------+        +-------------------+        +-------------------+
                                 |
                                 v
+-------------------+   +-------------------+   +-------------------+
|   Graph Service   |   |   Ingestion Service|   |   Notification   |
|   (vLLM + SGLang) |   |   (ETL + Parser)   |   |   Service (Kafka)|
+-------------------+   +-------------------+   +-------------------+
                                 |
                                 v
+---------------------------------------------------------------+
|                     Knowledge Store (Neo4j)                  |
+---------------------------------------------------------------+
                                 |
                                 v
+-------------------+        +-------------------+        +-------------------+
|   Vector Store    | <----> |   Embedding Engine| <----> |   Data Lake (S3) |
|   (PGVector)      |        |   (vLLM)          |        +-------------------+
+-------------------+        +-------------------+
```

* **Front‑End** – React + TypeScript SPA, uses GraphQL for data fetching.  
* **API Gateway** – FastAPI (Python) exposing REST & GraphQL endpoints, handles request routing, rate‑limiting, and tracing.  
* **Auth Service** – OAuth2 / OpenID Connect (Keycloak) with RBAC per organization, team, and knowledge‑object.  
* **Ingestion Service** – Asynchronous workers (Celery + Redis) that pull source documents (Confluence, Git, PDFs, Slack export) → parse → chunk → embed → store.  
* **Graph Service** – Core knowledge graph built on Neo4j (v5). Business logic for entity/relationship creation, versioning, and lineage.  
* **Embedding Engine** – vLLM inference server (GPU‑accelerated) serving a fine‑tuned LLM (e.g., Mistral‑7B‑Instruct) for semantic embeddings and structured generation via SGLang.  
* **Vector Store** – PGVector extension on PostgreSQL for fast similarity search of embeddings.  
* **Notification Service** – Kafka topics for change events (new knowledge, updates, deprecations) consumed by UI and external webhooks.  
* **Data Lake** – S3‑compatible bucket (MinIO in dev) stores raw source files and intermediate artefacts for audit/compliance.

All services are containerised (Docker) and orchestrated via Kubernetes (v1.28) with Helm charts for reproducible deployments.

---

### 2. Core Components & Responsibilities

| Component | Language / Runtime | Key Libraries | Responsibilities |
|-----------|-------------------|---------------|------------------|
| **API Gateway** | Python 3.11 / FastAPI | `fastapi`, `uvicorn`, `strawberry-graphql`, `pydantic` | Request validation, auth, routing, OpenAPI docs |
| **Auth Service** | Java 21 / Spring Boot | `spring-security`, `keycloak-admin-client` | User/role management, token issuance, SSO |
| **Ingestion Workers** | Python 3.11 | `celery`, `redis`, `pdfminer.six`, `beautifulsoup4`, `langchain` | Source connectors, chunking, metadata extraction |
| **Embedding Engine** | C++/Python (vLLM) | `vllm`, `torch`, `transformers` | Real‑time embedding generation, structured output via SGLang |
| **Graph Service** | Kotlin 1.9 | `neo4j-java-driver`, `spring-data-neo4j` | CRUD on nodes/edges, versioning, lineage queries |
| **Vector Store** | PostgreSQL 15 + PGVector | `pgvector` | Approximate nearest‑neighbor search for embeddings |
| **Notification Service** | Go 1.22 | `segmentio/kafka-go` | Event streaming, webhook dispatch |
| **Front‑End** | TypeScript 5 | `react`, `apollo-client`, `mui`, `d3-force` | Knowledge graph visualisation, editors, dashboards |

---

### 3. Data Model

#### 3.1 Graph Schema (Neo4j)

| Label | Properties | Description |
|-------|------------|-------------|
| `KnowledgeObject` | `id: UUID`, `title: string`, `type: enum[DOC, CODE, PROCESS, POLICY]`, `version: int`, `createdAt`, `updatedAt`, `ownerTeamId` | Core knowledge artefact |
| `Entity` | `id`, `name`, `category`, `attributes: map` | Real‑world entity (service, DB, API) |
| `Relation` | `type: enum[DEPENDS_ON, PRODUCES, CONSUMES, DOCUMENTS]`, `weight: float` | Edge between `KnowledgeObject` ↔ `Entity` or `KnowledgeObject` ↔ `KnowledgeObject` |
| `Tag` | `name`, `color` | Tagging for search & UI |
| `Team` | `id`, `name`, `role` | Ownership & permission scoping |

**Versioning** – Each `KnowledgeObject` is immutable; updates create a new node linked via `PRECEDES` relationship.

#### 3.2 Vector Store Schema (PostgreSQL)

```sql
CREATE TABLE embeddings (
    id UUID PRIMARY KEY,
    knowledge_object_id UUID REFERENCES KnowledgeObject(id),
    embedding vector(768),   -- dimension matches LLM output
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

#### 3.3 API Contracts (OpenAPI v3)

* `GET /api/v1/knowledge/{id}` – retrieve full object with relationships.  
* `POST /api/v1/knowledge` – create new object (multipart for raw file + JSON metadata).  
* `GET /api/v1/search?query=...` – hybrid search (BM25 on text + ANN on embeddings).  
* `POST /api/v1/ingest` – trigger async ingestion of external source URL.  
* `GET /api/v1/graph?depth=n&nodeId=...` – sub‑graph extraction for visualisation.

All endpoints require Bearer JWT; scopes: `read:knowledge`, `write:knowledge`, `admin:org`.

---

### 4. Key APIs / Interfaces

#### 4.1 Embedding Service (gRPC)

```proto
service Embedding {
  rpc Encode (EncodeRequest) returns (EncodeResponse);
  rpc StructuredGenerate (GenerateRequest) returns (GenerateResponse);
}

message EncodeRequest {
  repeated string texts = 1;
}
message EncodeResponse {
  repeated vector embeddings = 1; // float32 array
}
message GenerateRequest {
  string prompt = 1;
  map<string, string> schema = 2; // SGLang schema for structured output
}
message GenerateResponse {
  string json_output = 1;
}
```

FastAPI gateway proxies HTTP → gRPC via `grpcio`.

#### 4.2 Event Schema (Kafka)

Topic: `ckg.events`

```json
{
  "event_id": "uuid",
  "type": "KNOWLEDGE_CREATED|UPDATED|DEPRECATED",
  "knowledge_id": "uuid",
  "timestamp": "ISO8601",
  "payload": { /* optional diff */ }
}
```

Consumers: UI (WebSocket), external webhook sink, analytics pipeline.

---

### 5. Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Orchestration | Kubernetes | 1.28 |
| Container Runtime | Docker | 24.0 |
| Service Mesh | Istio | 1.20 |
| API | FastAPI | 0.110 |
| Auth | Keycloak | 24.0 |
| Graph DB | Neo4j | 5.15 |
| Vector DB | PostgreSQL + PGVector | 15 |
| Embedding Engine | vLLM | 0.5 (GPU) |
| Structured Generation | SGLang | 0.3 |
| Message Bus | Kafka | 3.6 |
| Front‑End | React + TypeScript | 18 |
| CI/CD | GitHub Actions + ArgoCD | – |
| Monitoring | Prometheus + Grafana | – |
| Logging | Loki + Fluent Bit | – |
| Secrets | HashiCorp Vault | 1.15 |

All third‑party libraries are vetted for compatible licences (Apache‑2.0, MIT, BSD).

---

### 6. Dependencies & External Integrations

| Dependency | Purpose | Integration |
|------------|---------|-------------|
| Confluence API | Source docs | Ingestion connector (OAuth2) |
| GitHub API | Code docs, READMEs | Ingestion connector |
| Slack Export API | Conversational knowledge | Ingestion connector |
| S3 / MinIO | Raw artefact storage | Data Lake |
| OpenTelemetry | Tracing across services | Instrumentation in all services |
| Sentry | Error monitoring | SDK in each runtime |

All connectors are configurable via environment variables (`CKG_INGEST_<SOURCE>_TOKEN`).

---

### 7. Deployment & Operations

#### 7.1 Helm Chart Structure

```
ckg/
├─ charts/
│  ├─ api-gateway/
│  ├─ auth-service/
│  ├─ ingestion/
│  ├─ graph-service/
│  ├─ embedding/
│  ├─ vector-store/
│  └─ ui/
└─ values.yaml
```

* **Values** expose replica counts, resource limits, image tags, and external endpoint URLs.  
* **PodDisruptionBudgets** ensure high‑availability for stateful services (Neo4j, PostgreSQL).  
* **HorizontalPodAutoscaler** on API, Ingestion, and Embedding based on CPU & request latency.

#### 7.2 CI/CD Pipeline

1. **PR Validation** – unit tests (`pytest`, `junit`), lint (`ruff`, `ktlint`), static analysis (`sonarqube`).  
2. **Docker Build** – multi‑stage builds, SBOM generation (`syft`).  
3. **Integration Tests** – spin up a mini‑K8s (`kind`) with all services, run contract tests (`schemathesis`).  
4. **Release** – tag → ArgoCD sync → canary rollout (5% traffic) → full promotion after SLA checks.  

#### 7.3 Observability

* **Metrics** – Prometheus exporters on each service (request latency, error rates, queue depth).  
* **Tracing** – OpenTelemetry collector forwards to Jaeger UI.  
* **Logs** – Structured JSON logs to Loki; alerts via Grafana Alerting (CPU > 80% for >5m, ingestion lag > 30m).  

#### 7.4 Backup & DR

* Neo4j backups via `neo4j-admin backup` nightly to S3 (retention 30 days).  
* PostgreSQL logical backups (`pg_dump`) hourly, point‑in‑time recovery enabled.  
* All artefacts stored in encrypted S3 buckets (AES‑256).  

---

### 8. Security Considerations

| Area | Controls |
|------|----------|
| **Authentication** | OAuth2/OIDC via Keycloak, short‑lived JWT (15 min) with refresh tokens. |
| **Authorization** | RBAC per organization → team → knowledge object; enforced in API gateway and Neo4j queries. |
| **Data-in‑Transit** | mTLS between services, HTTPS for external traffic. |
| **Data-at‑Rest** | Disk encryption (dm‑crypt) on node volumes; S3 server‑side encryption. |
| **Secret Management** | Vault dynamic secrets for DB passwords, API keys. |
| **Vulnerability Scanning** | Trivy scan on images; nightly dependency audit. |
| **Compliance** | GDPR‑ready – ability to purge all data for a given user/team on request. |

---

### 9. Future Enhancements (Roadmap)

| Milestone | Feature | Impact |
|-----------|---------|--------|
| **v0.2** | Real‑time collaborative editing (CRDT) | Reduce duplication, improve knowledge freshness |
| **v0.3** | Automated impact analysis (graph traversal + risk scoring) | Proactively surface critical dependencies |
| **v0.4** | Multi‑modal ingestion (audio transcripts, video OCR) | Capture tacit knowledge from meetings |
| **v0.5** | Self‑service LLM fine‑tuning per org | Better domain relevance for embeddings |

---

### 10. Glossary

* **CKG** – Critical Knowledge Graph.  
* **Embedding** – Dense vector representation of text generated by LLM.  
* **SGLang** – Structured Generation Language for deterministic JSON/YAML output from LLMs.  
* **vLLM** – High‑throughput LLM inference engine used for embedding and generation.  
* **PGVector** – PostgreSQL extension for vector similarity search.  

--- 

*Prepared by:* Senior Product/Engineering Lead – AxentX  
*Date:* 2026‑06‑18  

---
