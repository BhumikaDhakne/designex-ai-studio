import { useEffect, useState } from "react";
import {
  ArrowRight,
  Check,
  CheckCircle2,
  CircleAlert,
  Clock3,
  FileCheck2,
  Layers3,
  RefreshCw,
  ShieldCheck,
  Sparkles,
  Workflow,
  X,
} from "lucide-react";
import "./App.css";

type Evidence = {
  document_id: string;
  document_title: string;
  quote: string;
  verified: boolean;
};

type Risk = {
  title: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  cause: string;
  evidence: Evidence[];
  root_cause_tasks: string[];
  affected_tasks: string[];
  downstream_tasks: string[];
  downstream_impact: string[];
  recommended_actions: string[];
};

type ProjectAnalysis = {
  project_id: string;
  project_name: string;
  overall_risk: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  risks: Risk[];
};

const API_BASE = "/api";

function App() {
  const [activeSection, setActiveSection] = useState("intelligence");
  const [analysis, setAnalysis] = useState<ProjectAnalysis | null>(null);
  const [loadingAnalysis, setLoadingAnalysis] = useState(true);
  const [analysisError, setAnalysisError] = useState("");

  const [visualMode, setVisualMode] = useState<"original" | "refined">(
    "refined",
  );

  const [contentApproved, setContentApproved] = useState(false);

  useEffect(() => {
    loadAnalysis();
  }, []);

  async function loadAnalysis() {
    try {
      setLoadingAnalysis(true);
      setAnalysisError("");

      const response = await fetch(
        `${API_BASE}/projects/PRJ-001/analysis`,
      );

      if (!response.ok) {
        throw new Error("Unable to load project analysis.");
      }

      const data: ProjectAnalysis = await response.json();
      setAnalysis(data);
    } catch (error) {
      setAnalysisError(
        error instanceof Error
          ? error.message
          : "Unable to load project analysis.",
      );
    } finally {
      setLoadingAnalysis(false);
    }
  }

  const primaryRisk = analysis?.risks?.[0];

  const scrollTo = (id: string) => {
    setActiveSection(id);

    document.getElementById(id)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <div className="app-shell">
      {/* =====================================================
          HEADER
      ===================================================== */}

      <header className="site-header">
        <div className="brand">
          <span className="brand-mark">D</span>
          <span className="brand-name">DESIGNEX AI STUDIO</span>
        </div>

        <nav className="main-nav">
          <button
            className={activeSection === "intelligence" ? "active" : ""}
            onClick={() => scrollTo("intelligence")}
          >
            Intelligence
          </button>

          <button
            className={activeSection === "visuals" ? "active" : ""}
            onClick={() => scrollTo("visuals")}
          >
            Visual Studio
          </button>

          <button
            className={activeSection === "content" ? "active" : ""}
            onClick={() => scrollTo("content")}
          >
            Content Studio
          </button>

          <button
            className={activeSection === "operations" ? "active" : ""}
            onClick={() => scrollTo("operations")}
          >
            Operations
          </button>
        </nav>

        <div className="header-year">2026</div>
      </header>

      <main>
        {/* =====================================================
            HERO
        ===================================================== */}

        <section className="hero-section">
          <div className="hero-kicker">
            <span className="kicker-line" />
            INTELLIGENCE FOR THE BUILT ENVIRONMENT
          </div>

          <div className="hero-grid">
            <div>
              <h1>
                Design decisions,
                <br />
                <em>made intelligent.</em>
              </h1>
            </div>

            <div className="hero-description">
              <p>
                An AI-assisted operating layer for project intelligence,
                visual ideation, content creation and operational workflows.
              </p>

              <div className="hero-meta">
                <span>DESIGNEX</span>
                <span>AI STUDIO / POC</span>
                <span>DUBAI · 2026</span>
              </div>
            </div>
          </div>
        </section>

        {/* =====================================================
            PROJECT INTELLIGENCE
        ===================================================== */}

        <section id="intelligence" className="intelligence-section">
          <div className="section-inner">
            <div className="intelligence-heading">
              <div>
                <span className="eyebrow intelligence-eyebrow">
                  01 / PROJECT INTELLIGENCE
                </span>

                <h2>
                  Find what the
                  <br />
                  project data <em>misses.</em>
                </h2>
              </div>

              <div className="intelligence-heading-copy">
                <span>STRUCTURED + UNSTRUCTURED</span>

                <p>
                  Combines project tasks, dependencies and source documents to
                  surface hidden operational risk.
                </p>
              </div>
            </div>

            {loadingAnalysis && (
              <div className="analysis-loading">
                <RefreshCw size={17} className="spin" />
                Loading project intelligence…
              </div>
            )}

            {analysisError && (
              <div className="analysis-error">
                <CircleAlert size={18} />

                <div>
                  <strong>Analysis unavailable</strong>
                  <span>{analysisError}</span>
                </div>

                <button onClick={loadAnalysis}>Retry</button>
              </div>
            )}

            {analysis && primaryRisk && (
              <div className="intelligence-card">
                {/* FINDING */}

                <div className="finding-top">
                  <div className="project-context">
                    <span>PALM JUMEIRAH LUXURY VILLA</span>
                    <small>PRJ-001</small>
                  </div>

                  <div className="risk-badge">
                    <span />
                    {analysis.overall_risk} RISK
                  </div>
                </div>

                <div className="finding-section">
                  <div className="finding-label">
                    <CircleAlert size={16} />
                    FINDING
                  </div>

                  <h3>{primaryRisk.title}</h3>

                  <p className="finding-cause">
                    {primaryRisk.cause}
                  </p>
                </div>

                {/* EVIDENCE */}

                <div className="intelligence-divider" />

                <div className="evidence-section">
                  <div className="section-mini-heading">
                    <div>
                      <span className="mini-label">EVIDENCE</span>
                      <strong>What the source documents show</strong>
                    </div>

                    <span className="verified-status">
                      <ShieldCheck size={14} />
                      {primaryRisk.evidence.filter(
                        (evidence) => evidence.verified,
                      ).length}{" "}
                      SOURCE QUOTES VERIFIED
                    </span>
                  </div>

                  <div className="evidence-grid">
                    {primaryRisk.evidence.map((evidence) => (
                      <div
                        className="evidence-item"
                        key={evidence.document_id}
                      >
                        <div className="evidence-meta">
                          <span>{evidence.document_id}</span>

                          {evidence.verified && (
                            <CheckCircle2 size={14} />
                          )}
                        </div>

                        <strong>{evidence.document_title}</strong>

                        <blockquote>
                          “{evidence.quote}”
                        </blockquote>
                      </div>
                    ))}
                  </div>
                </div>

                {/* IMPACT */}

                <div className="intelligence-divider" />

                <div className="impact-section">
                  <div className="impact-column">
                    <span className="mini-label">PROJECT IMPACT</span>

                    <div className="task-flow">
                      <div className="task-node root">T-001</div>

                      <ArrowRight size={15} />

                      <div className="task-node">T-002</div>

                      <ArrowRight size={15} />

                      <div className="task-node">T-003</div>

                      <ArrowRight size={15} />

                      <div className="task-node">T-004</div>

                      <ArrowRight size={15} />

                      <div className="task-node">T-005</div>
                    </div>

                    <p>
                      Specification → BOQ → quotation → delivery →
                      installation
                    </p>
                  </div>

                  <div className="impact-column">
                    <span className="mini-label">IMMEDIATE CONSEQUENCE</span>

                    <p className="impact-statement">
                      Procurement may continue pricing against the old
                      material specification, creating cost and schedule
                      rework downstream.
                    </p>
                  </div>
                </div>

                {/* RECOMMENDATION */}

                <div className="intelligence-divider" />

                <div className="recommendation-section">
                  <div>
                    <span className="mini-label">RECOMMENDED ACTION</span>

                    <strong>
                      Resolve the specification before procurement proceeds.
                    </strong>
                  </div>

                  <div className="action-sequence">
                    {primaryRisk.recommended_actions
                      .slice(0, 3)
                      .map((action, index) => (
                        <div className="action-item" key={action}>
                          <span>
                            {String(index + 1).padStart(2, "0")}
                          </span>
                          <p>{action}</p>
                        </div>
                      ))}
                  </div>
                </div>

                {/* FOOTER */}

                <div className="intelligence-footer">
                  <span>
                    <FileCheck2 size={13} />
                    Evidence verified against source documents
                  </span>

                  <span>
                    REPRESENTATIVE POC DATA
                  </span>
                </div>
              </div>
            )}

            {analysis && !primaryRisk && (
              <div className="no-risk-state">
                <CheckCircle2 size={22} />

                <div>
                  <span>PROJECT STATUS</span>
                  <strong>No material risk identified</strong>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* =====================================================
            VISUAL STUDIO
        ===================================================== */}

        <section id="visuals" className="visual-section">
          <div className="visual-header">
            <div>
              <span className="eyebrow">02 / AI VISUAL STUDIO</span>

              <h2>
                From brief
                <br />
                to <em>concept.</em>
              </h2>
            </div>

            <div className="visual-header-copy">
              <p>
                Rapid concept ideation using generative visual AI. Designed to
                accelerate exploration before human design review.
              </p>

              <span className="studio-tag">
                HUMAN REVIEW REQUIRED
              </span>
            </div>
          </div>

          <div className="visual-workspace">
            <div className="visual-toolbar">
              <div className="visual-title">
                <Layers3 size={17} />
                <span>PALM JUMEIRAH / LUXURY VILLA</span>
              </div>

              <div className="visual-toggle">
                <button
                  className={visualMode === "original" ? "active" : ""}
                  onClick={() => setVisualMode("original")}
                >
                  Original
                </button>

                <button
                  className={visualMode === "refined" ? "active" : ""}
                  onClick={() => setVisualMode("refined")}
                >
                  Refined
                </button>
              </div>
            </div>

            <div className="visual-frame">
              <img
                src={
                  visualMode === "original"
                    ? "/generated/visuals/c21ca1dc-c310-4ca8-8cb8-aea11f7773ba.png"
                    : "/generated/visuals/0d040dbd-b6ef-4ce5-9dce-b62672ef9394.png"
                }
                alt={
                  visualMode === "original"
                    ? "Original architectural concept"
                    : "Refined architectural concept"
                }
              />

              <div className="visual-overlay">
                <span>
                  {visualMode === "original"
                    ? "INITIAL CONCEPT"
                    : "AI REFINED CONCEPT"}
                </span>
              </div>
            </div>

            <div className="visual-footer">
              <div>
                <span>MODE</span>
                <strong>CONCEPT IDEATION</strong>
              </div>

              <div>
                <span>OUTPUT</span>
                <strong>VISUAL REFERENCE</strong>
              </div>

              <div>
                <span>STATUS</span>
                <strong>READY FOR DESIGN REVIEW</strong>
              </div>
            </div>
          </div>
        </section>

        {/* =====================================================
            CONTENT STUDIO
        ===================================================== */}

        <section id="content" className="content-section">
          <div className="section-inner">
            <div className="section-heading">
              <div>
                <span className="eyebrow">03 / AI CONTENT STUDIO</span>

                <h2>
                  One project.
                  <br />
                  <em>Multiple narratives.</em>
                </h2>
              </div>

              <div className="section-heading-note">
                <span>HUMAN APPROVAL</span>

                <p>
                  Generate channel-specific project content while keeping the
                  final publishing decision with the team.
                </p>
              </div>
            </div>

            <div className="content-workspace">
              <aside className="content-sidebar">
                <span className="panel-label">CONTENT BRIEF</span>

                <div className="brief-item">
                  <span>PROJECT</span>
                  <strong>Palm Jumeirah Luxury Villa</strong>
                </div>

                <div className="brief-item">
                  <span>AUDIENCE</span>
                  <strong>Prospective clients</strong>
                </div>

                <div className="brief-item">
                  <span>PRIMARY CHANNEL</span>
                  <strong>Facebook</strong>
                </div>

                <div className="brief-item">
                  <span>SECONDARY</span>
                  <strong>LinkedIn</strong>
                </div>

                <div
                  className={`approval-state ${
                    contentApproved ? "approved" : ""
                  }`}
                >
                  {contentApproved ? (
                    <CheckCircle2 size={18} />
                  ) : (
                    <Clock3 size={18} />
                  )}

                  <div>
                    <span>STATUS</span>

                    <strong>
                      {contentApproved
                        ? "READY TO PUBLISH"
                        : "PENDING APPROVAL"}
                    </strong>
                  </div>
                </div>
              </aside>

              <div className="content-preview">
                <div className="content-preview-header">
                  <div className="platform">
                    <span className="platform-dot">f</span>

                    <div>
                      <strong>Facebook</strong>
                      <span>Social preview</span>
                    </div>
                  </div>

                  <span className="preview-label">AI GENERATED</span>
                </div>

                <div className="social-post">
                  <img
                    src="/generated/visuals/0d040dbd-b6ef-4ce5-9dce-b62672ef9394.png"
                    alt="Architectural project concept"
                  />

                  <div className="post-copy">
                    <strong>
                      A refined expression of contemporary luxury.
                    </strong>

                    <p>
                      Designed around light, proportion and a warm material
                      palette, this Palm Jumeirah residence brings together
                      architecture and landscape to create a calm, considered
                      living experience.
                    </p>

                    <span>
                      #Designex #DubaiArchitecture #LuxuryInteriors
                    </span>
                  </div>
                </div>

                <div className="linkedin-variant">
                  <div>
                    <span className="platform-label">
                      LINKEDIN VARIANT
                    </span>

                    <p>
                      Exploring how materiality, natural light and landscape
                      can shape a more considered residential experience.
                    </p>
                  </div>
                </div>

                <div className="content-actions">
                  <button
                    className="secondary-action"
                    onClick={() => setContentApproved(false)}
                  >
                    <X size={16} />
                    Request Changes
                  </button>

                  <button
                    className={`primary-action ${
                      contentApproved ? "approved-button" : ""
                    }`}
                    onClick={() => setContentApproved(true)}
                  >
                    {contentApproved ? (
                      <>
                        <Check size={16} />
                        Ready to Publish
                      </>
                    ) : (
                      <>
                        <Check size={16} />
                        Approve Content
                      </>
                    )}
                  </button>
                </div>

                <div className="simulation-note">
                  <ShieldCheck size={14} />
                  POC simulation · Nothing is published to social platforms
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =====================================================
            OPERATIONS
        ===================================================== */}

        <section id="operations" className="operations-section">
          <div className="section-inner">
            <div className="operations-header">
              <div>
                <span className="eyebrow olive-dark">
                  04 / DAILY OPERATIONS
                </span>

                <h2>
                  Automation that
                  <br />
                  <em>keeps moving.</em>
                </h2>
              </div>

              <div className="automation-status">
                <span className="pulse-dot" />
                AUTOMATION ACTIVE
              </div>
            </div>

            <div className="operations-console">
              <div className="operations-summary">
                <div className="operation-stat">
                  <span>LAST AUTOMATED CHECK</span>
                  <strong>07 OCT 2026 · 10:00 AM</strong>
                  <small>Asia / Dubai</small>
                </div>

                <div className="operation-stat attention">
                  <span>ATTENTION REQUIRED</span>
                  <strong>2</strong>
                  <small>tasks requiring action</small>
                </div>

                <div className="operation-stat">
                  <span>NEXT CHECK</span>
                  <strong>08 OCT 2026 · 10:00 AM</strong>
                  <small>Daily schedule</small>
                </div>
              </div>

              <div className="operations-table">
                <div className="operations-row operations-row-head">
                  <span>TASK</span>
                  <span>OWNER</span>
                  <span>STATUS</span>
                  <span>ACTION</span>
                </div>

                <div className="operations-row">
                  <div>
                    <strong>Update BOQ for marble works</strong>
                    <span>T-002 · PRJ-001</span>
                  </div>

                  <span>QS Team</span>

                  <span className="operation-badge high">
                    DUE TOMORROW
                  </span>

                  <span className="action-text">
                    Owner + PM notified
                  </span>
                </div>

                <div className="operations-row">
                  <div>
                    <strong>Obtain supplier quotation</strong>
                    <span>T-003 · PRJ-001</span>
                  </div>

                  <span>Procurement Team</span>

                  <span className="operation-badge medium">
                    DUE IN 3 DAYS
                  </span>

                  <span className="action-text">
                    Owner notified
                  </span>
                </div>
              </div>

              <div className="operations-footer">
                <div>
                  <Workflow size={17} />
                  <span>
                    Deterministic deadline rules executed by n8n
                  </span>
                </div>

                <span>
                  POC notification · No external message was sent
                </span>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="site-footer">
        <div>
          <span className="footer-mark">D</span>
          <strong>DESIGNEX AI STUDIO</strong>
        </div>

        <span>
          AI-assisted decision intelligence · Built as a proof of concept
        </span>

        <span>© 2026 DESIGNEX</span>
      </footer>
    </div>
  );
}

export default App;