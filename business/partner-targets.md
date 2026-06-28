# partner‑targets.md  
**Critical Knowledge Graph – Partner Integration Roadmap**  

| # | SaaS / API | Primary Use‑Case (user job solved) | Free‑Tier Limits* | Integration Effort | Affiliate / Revenue‑Share Program | Rationale & Value‑Add |
|---|------------|-----------------------------------|-------------------|--------------------|-----------------------------------|-----------------------|
| 1 | **Atlassian Confluence** (REST API) | *Document & centralise critical procedures* – users can pull existing Confluence pages into the graph and push newly‑generated knowledge nodes back to Confluence for versioned docs. | 10 users, 2 GB storage, API rate‑limit 60 req/min. | **M** – OAuth + webhook sync, mapping of page hierarchy to graph nodes. | Atlassian Marketplace partner program (30 % revenue share on paid add‑ons). | Confluence is the de‑facto wiki for SMBs; integration gives instant knowledge ingestion and a familiar publishing surface, reducing adoption friction. |
| 2 | **Notion** (official API) | *Capture ad‑hoc knowledge* – allow team members to select Notion pages/blocks and auto‑link them to graph entities (e.g., SOPs, runbooks). | 1,000 API calls / month, 5 MB upload, 5 users. | **S** – simple OAuth, page‑to‑node transformer. | Notion Partner Program (referral commission up to 20 %). | Notion’s flexible workspace is popular with startups; the integration turns any Notion note into a “critical” node, encouraging habit formation. |
| 3 | **Slack** (Events API & Bot) | *Real‑time knowledge capture & alerts* – users can `@ckg` a message to create a node, and the system can push dependency‑risk alerts to relevant channels. | 10,000 events / month, 1 bot token. | **S** – Bot registration, event subscription, message parsing. | Slack App Directory (no direct revenue share, but co‑marketing & referral incentives). | Embeds knowledge work into daily communication, lowering the barrier to capture tacit knowledge and surfacing bus‑factor risks instantly. |
| 4 | **GitHub** (GraphQL & REST) | *Link code artefacts to knowledge* – map repository files, issues, PRs to graph nodes (e.g., “deployment script X is critical”). | Unlimited public repos, 2,000 API calls / hour for private. | **M** – OAuth, webhook for repo events, schema mapping. | GitHub Marketplace (15 % revenue share on paid apps). | Bridges dev‑ops knowledge with operational knowledge, helping engineering managers see who owns critical code paths. |
| 5 | **Google Workspace** (Drive, Docs API) | *Import existing docs & drive files* – bulk ingest of Google Docs/Sheets that contain SOPs, runbooks, architecture diagrams. | 15 GB total storage, 1 GB per file, 1 M API calls / day. | **M** – Service‑account auth, file‑type detection, OCR for images. | Google Cloud Partner Advantage (referral bonuses, joint go‑to‑market). | Most SMBs already store docs in Drive; auto‑ingest eliminates manual copy‑paste and keeps knowledge up‑to‑date. |
| 6 | **Zapier** (Platform API) | *No‑code workflow extensions* – let users trigger actions (e.g., create a ticket in Jira when a critical node is flagged) without code. | 100 tasks / month, 5 Zaps. | **S** – Zapier CLI app, trigger/action definitions. | Zapier Partner Program (up‑to 20 % revenue share on paid Zaps). | Extends CK‑Graph’s reach into any of the 5,000+ Zapier‑connected apps, making the platform “plug‑and‑play” for non‑technical teams. |
| 7 | **Microsoft Teams / SharePoint** (Graph API) | *Enterprise‑grade collaboration* – sync critical nodes to SharePoint lists and surface them in Teams tabs. | 5 GB per user, 10 K API calls / day. | **L** – Complex auth (Azure AD), permission scopes, Teams tab UI. | Microsoft Partner Network (co‑sell incentives, up to 25 % of Azure Marketplace revenue). | Provides a native experience for organizations already on Microsoft 365, unlocking enterprise contracts and compliance features. |
| 8 | **ServiceNow** (Table API) | *ITSM knowledge coupling* – attach CK‑Graph nodes to ServiceNow knowledge articles and incident records. | 1,000 API calls / month (developer instance). | **L** – Enterprise auth, data model mapping, change‑management workflow. | ServiceNow Store (15 % revenue share). | Aligns operational risk knowledge with incident management, appealing to IT departments that need to reduce single‑point‑of‑failure risk. |

\*Free‑tier limits are current as of **June 2026** and are subject to change. All limits are sufficient for pilot/SMB usage; scaling to paid tiers is straightforward.

---

## Integration Roadmap (Quarterly Milestones)

| Quarter | Target Integrations | Milestone Deliverables | Success Metrics |
|---------|--------------------|-----------------------|-----------------|
| **Q1 2026** | 1️⃣ Confluence, 2️⃣ Notion, 3️⃣ Slack | • OAuth flows & secure token storage<br>• Bi‑directional sync pipelines (doc ↔ graph)<br>• Slack bot with `@ckg create` command | • 5 SMB beta customers onboarded<br>• ≥ 80 % of captured knowledge originates from these channels |
| **Q2 2026** | 4️⃣ GitHub, 5️⃣ Google Workspace | • Repository‑event webhook processor<br>• Bulk Drive/Docs ingestion UI<br>• Mapping UI for code‑to‑knowledge links | • 30 % of critical nodes linked to code artefacts<br>• 1 GB of imported docs processed |
| **Q3 2026** | 6️⃣ Zapier, 7️⃣ Teams/SharePoint | • Publish CK‑Graph Zapier app (public)<br>• Teams tab prototype + SharePoint list sync<br>• Affiliate referral tracking dashboard | • 200 Zapier installs (free tier)<br>• 3 enterprise pilots on Teams |
| **Q4 2026** | 8️⃣ ServiceNow (optional stretch) | • ServiceNow connector (knowledge article ↔ graph)<br>• Incident‑risk alert workflow<br>• Joint go‑to‑market co‑sell kit | • 2 ITSM customers in pilot<br>• Reduction of “single‑owner” incidents by 15 % |

**Prioritisation Logic**  
1. **Adoption velocity** – Confluence, Notion, Slack have the lowest effort and highest daily‑user exposure, driving rapid data capture.  
2. **Revenue‑share potential** – Atlassian, GitHub, Zapier, Microsoft, ServiceNow all offer partner programs that can generate recurring referral income.  
3. **Strategic lock‑in** – Google Workspace and Microsoft 365 cover the two dominant productivity suites, ensuring coverage of > 80 % of SMBs.  
4. **Risk mitigation** – ServiceNow integration is deferred to Q4 because of higher effort and enterprise sales cycle; it will be pursued only if early‑stage adoption validates the bus‑factor reduction value proposition.

---  

### Next Steps for Business‑Synthesis Team
1. **Secure partner agreements** – initiate contact with Atlassian, Notion, Zapier, and Microsoft partner managers to lock in revenue‑share terms.  
2. **Scope engineering resources** – allocate 1 FTE (full‑stack) per “M” effort integration, 0.5 FTE for “S” integrations, and a senior architect for “L” integrations (Teams, ServiceNow).  
3. **Define KPI dashboard** – track “knowledge nodes created per integration”, “user active days”, and “affiliate revenue per month”.  

*End of document.*