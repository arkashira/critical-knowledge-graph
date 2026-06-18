# Business Model Canvas – Critical Knowledge Graph

| **Key Partners** | **Key Activities** | **Key Resources** |
|------------------|--------------------|-------------------|
| • Cloud infrastructure providers (AWS, GCP, Azure) – compute, storage, managed DB services | • Product design & roadmap iteration based on validated customer pain | • Proprietary knowledge‑graph engine (graph DB + inference layer) |
| • Enterprise integration partners (Slack, Microsoft Teams, Jira, Confluence) | • Data ingestion pipelines (auto‑capture from code repos, ticketing systems, wikis) | • Large curated datasets (auto, instr‑resp, messages, system‑user‑assistant) |
| • AI model providers (vLLM, SGLang) for semantic search & summarisation | • Continuous training & fine‑tuning of domain‑specific LLMs | • Engineering talent (graph engineers, ML scientists, full‑stack devs) |
| • Security & compliance auditors (ISO 27001, SOC‑2) | • Customer onboarding, training, and support | • Documentation & knowledge‑capture templates |
| • Channel partners / MSPs for SMB outreach | • Monitoring, analytics, and feedback loops for product improvement | • IP & patents on dependency‑reduction algorithms |

| **Value Propositions** | **Customer Relationships** | **Customer Segments** |
|------------------------|----------------------------|-----------------------|
| • **Reduce single‑point‑of‑failure risk** – automatically map critical system knowledge and dependencies. | • Dedicated Customer Success Managers for SMBs (on‑boarding, quarterly health checks). | • Small‑to‑Medium Enterprises (10‑200 employees) with distributed engineering teams. |
| • **Accelerate onboarding & knowledge transfer** – searchable knowledge graph with AI‑augmented summaries. | • Self‑service portal with tutorials, community forum, and AI‑driven help‑desk. | • Remote‑first tech companies lacking formal documentation processes. |
| • **Lower operational cost** – prevent downtime by surfacing hidden dependencies before incidents. | • Proactive alerts & recommendations (e.g., “Component X has no owner”). | • Regulated industries (FinTech, HealthTech) needing audit‑ready documentation. |
| • **Compliance & audit readiness** – generate up‑to‑date dependency reports for auditors. | • Quarterly business reviews for enterprise‑tier customers. | • Managed Service Providers (MSPs) that need to maintain client knowledge bases. |
| • **AI‑enhanced insights** – leverage vLLM/SGLang for semantic search, gap detection, and impact analysis. | • In‑app chat assistance powered by fine‑tuned LLMs. | • Start‑ups scaling rapidly and fearing knowledge loss. |

| **Channels** | **Cost Structure** | **Revenue Streams** |
|--------------|--------------------|----------------------|
| • Direct sales (inside sales team targeting SMBs). | • Cloud compute & storage (pay‑as‑you‑go). | • **Subscription SaaS** – tiered plans (Starter, Growth, Enterprise). |
| • Marketplace integrations (Slack App Directory, Microsoft Teams Store). | • Personnel (engineers, data scientists, CSMs). | • **Professional Services** – onboarding, custom integration, training workshops. |
| • Partner‑led referrals (MSPs, VARs). | • Licensing fees for third‑party AI models (vLLM, SGLang). | • **Usage‑based add‑ons** – extra graph nodes, advanced analytics, compliance reporting. |
| • Content marketing (blog, webinars, case studies). | • R&D (model fine‑tuning, graph algorithm research). | • **Data Export Packages** – anonymized knowledge‑graph snapshots for research partners. |
| • Community & open‑source contributions (limited‑feature open core). | • Security & compliance audits (ISO, SOC). | • **Marketplace commissions** from partner integrations. |

---  

**Notes & Assumptions**

* The product leverages Axentx’s existing datasets (≈25 M pairs) to pre‑train domain‑agnostic LLMs, then fine‑tunes on customer‑specific knowledge sources.
* Initial MVP targets the “Starter” segment with a 30‑day free trial to prove ROI (downtime reduction >10%).
* Cost optimisation will use spot instances and serverless functions where possible; enterprise tier may require dedicated clusters.
* Revenue validation will be performed via pilot programs with 5‑10 SMBs before full market launch.
