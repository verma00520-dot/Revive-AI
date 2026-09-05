import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API = "https://revive-ai-1-aqsu.onrender.com";

function App() {
  const [metrics, setMetrics] = useState({});
  const [payments, setPayments] = useState([]);
  const [activePage, setActivePage] = useState("Dashboard");
  const [selectedPayment, setSelectedPayment] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const loadDashboard = async () => {
    try {
      const metricsResponse = await fetch(API + "/metrics");
      const paymentsResponse = await fetch(API + "/payments");

      const metricsData = await metricsResponse.json();
      const paymentsData = await paymentsResponse.json();

      setMetrics(metricsData);
      setPayments(paymentsData);
      setLastUpdated(new Date());
    } catch (error) {
      console.error("Dashboard connection error:", error);
    }
  };

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(loadDashboard, 5000);

    return () => clearInterval(interval);
  }, []);

  const actionDistribution = useMemo(() => {
    const distribution = {};

    payments.forEach((payment) => {
      const action = payment.final_action || "UNKNOWN";
      distribution[action] = (distribution[action] || 0) + 1;
    });

    return distribution;
  }, [payments]);

  const failureDistribution = useMemo(() => {
    const distribution = {};

    payments.forEach((payment) => {
      const failure = payment.failure_type || "unknown";
      distribution[failure] = (distribution[failure] || 0) + 1;
    });

    return distribution;
  }, [payments]);

  const formatCurrency = (value) =>
    `₹${Number(value || 0).toLocaleString("en-IN")}`;

  const formatAction = (action) => {
    if (!action) return "UNKNOWN";

    return action
      .replaceAll("_", " ")
      .replace("SEND REMINDER AND RETRY", "REMINDER + RETRY");
  };

  const getActionClass = (action) => {
    if (
      action === "SEND_REMINDER_AND_RETRY" ||
      action === "RETRY_NOW"
    ) {
      return "action retry";
    }

    if (action === "RETRY_LATER") return "action later";
    if (action === "UPDATE_PAYMENT_METHOD") return "action update";
    if (action === "ESCALATE") return "action escalate";

    return "action stop";
  };

  const getStatusClass = (status) => {
    if (status === "SUCCESS") return "status success";
    if (status === "FAILED") return "status failed";
    if (status === "ESCALATED") return "status escalated";
    if (status === "STOPPED") return "status stopped";

    return "status";
  };

  const getProbabilityClass = (probability) => {
    const value = Number(probability || 0) * 100;

    if (value >= 80) return "prob-high";
    if (value >= 60) return "prob-medium-high";
    if (value >= 40) return "prob-medium";
    if (value >= 20) return "prob-low";

    return "prob-very-low";
  };

  const getProbabilityLevel = (probability) => {
    const value = Number(probability || 0) * 100;

    if (value >= 80) return "HIGH";
    if (value >= 60) return "MEDIUM-HIGH";
    if (value >= 40) return "MEDIUM";
    if (value >= 20) return "LOW";

    return "VERY LOW";
  };

  const getFailureLabel = (failure) => {
    if (!failure) return "Unknown";

    return failure
      .replaceAll("_", " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());
  };

  const remainingRisk =
    Number(metrics.revenue_at_risk || 0) -
    Number(metrics.recovered_revenue || 0);

  const navItems = [
    {
      section: "MAIN",
      items: [
        ["Dashboard", "◈"],
        ["Recovery Center", "↗"],
        ["Transactions", "▣"],
        ["AI Insights", "◉"],
        ["Audit Trail", "⌁"],
      ],
    },
  ];

  return (
    <div className="app-shell">

      {/* ================= SIDEBAR ================= */}

      <aside className="sidebar">

        <div className="sidebar-brand">
          <div className="brand-logo">R</div>

          <div className="brand-text">
            <strong>REVIVE AI</strong>
            <span>AI Revenue Recovery</span>
          </div>
        </div>

        <div className="sidebar-menu">

          {navItems.map((section) => (
            <div className="nav-section" key={section.section}>

              <div className="nav-section-title">
                {section.section}
              </div>

              {section.items.map(([name, icon]) => (
                <button
                  key={name}
                  className={`nav-item ${activePage === name ? "active" : ""
                    }`}
                  onClick={() => setActivePage(name)}
                >
                  <span className="nav-icon">{icon}</span>
                  <span>{name}</span>
                </button>
              ))}

            </div>
          ))}

        </div>

        <div className="sidebar-bottom">

          <button className="light-mode">
            <span>☀</span>
            Light Mode
          </button>

          <div className="sidebar-system">
            <div className="online-dot"></div>

            <div>
              <strong>System Online</strong>
              <small>Recovery engine active</small>
            </div>
          </div>

        </div>

      </aside>


      {/* ================= MAIN AREA ================= */}

      <div className="main-area">

        {/* TOP BAR */}

        <header className="topbar">

          <div>
            <span className="topbar-label">
              REVIVE AI
            </span>

            <span className="topbar-divider">
              /
            </span>

            <span className="topbar-page">
              {activePage}
            </span>
          </div>

          <div className="topbar-right">

            <span className="test-badge">
              ● DEMO SIMULATION
            </span>

            <span className="razorpay-badge">
              RAZORPAY TEST MODE
            </span>

            <span className="live-status">
              <span></span>
              LIVE
            </span>

          </div>

        </header>


        {/* ================= CONTENT ================= */}

        <main className="page-content">

          {activePage === "Dashboard" && (

            <>

              {/* PAGE TITLE */}

              <section className="page-heading">

                <div>

                  <p className="eyebrow">
                    AI REVENUE RECOVERY
                  </p>

                  <h1>
                    Dashboard
                  </h1>

                  <p>
                    Autonomous recovery decisions, bounded by
                    merchant controls.
                  </p>

                </div>

                <div className="last-updated">
                  ● LIVE DATA
                  <small>
                    {lastUpdated
                      ? `Updated ${lastUpdated.toLocaleTimeString()}`
                      : "Connecting..."}
                  </small>
                </div>

              </section>


              {/* KPI CARDS */}

              <section className="stats-grid">

                <div className="metric-card">

                  <span className="metric-label">
                    REVENUE AT RISK
                  </span>

                  <strong>
                    {formatCurrency(
                      metrics.revenue_at_risk
                    )}
                  </strong>

                  <small>
                    Across failed payments
                  </small>

                </div>


                <div className="metric-card recovered">

                  <span className="metric-label">
                    RECOVERED REVENUE
                  </span>

                  <strong>
                    {formatCurrency(
                      metrics.recovered_revenue
                    )}
                  </strong>

                  <small>
                    Simulated recovery
                  </small>

                </div>


                <div className="metric-card">

                  <span className="metric-label">
                    RECOVERY RATE
                  </span>

                  <strong>
                    {metrics.recovery_rate || 0}%
                  </strong>

                  <small>
                    Batch performance
                  </small>

                </div>


                <div className="metric-card">

                  <span className="metric-label">
                    TRANSACTIONS ANALYZED
                  </span>

                  <strong>
                    {metrics.total_payments || 0}
                  </strong>

                  <small>
                    AI recovery decisions
                  </small>

                </div>

              </section>


              {/* RECOVERY FUNNEL */}

              <section className="card">

                <div className="card-heading">

                  <div>

                    <span>
                      RECOVERY FUNNEL
                    </span>

                    <h2>
                      From failed payment to measured recovery
                    </h2>

                  </div>

                </div>


                <div className="funnel">

                  <div className="funnel-step">

                    <span>01</span>

                    <div className="funnel-icon">
                      !
                    </div>

                    <strong>
                      Detect
                    </strong>

                    <small>
                      Identify payment failure
                    </small>

                  </div>


                  <div className="funnel-arrow">
                    →
                  </div>


                  <div className="funnel-step">

                    <span>02</span>

                    <div className="funnel-icon">
                      ◌
                    </div>

                    <strong>
                      Score
                    </strong>

                    <small>
                      Estimate recovery probability
                    </small>

                  </div>


                  <div className="funnel-arrow">
                    →
                  </div>


                  <div className="funnel-step">

                    <span>03</span>

                    <div className="funnel-icon">
                      AI
                    </div>

                    <strong>
                      Intervene
                    </strong>

                    <small>
                      Choose bounded action
                    </small>

                  </div>


                  <div className="funnel-arrow">
                    →
                  </div>


                  <div className="funnel-step">

                    <span>04</span>

                    <div className="funnel-icon">
                      ₹
                    </div>

                    <strong>
                      Recover
                    </strong>

                    <small>
                      Measure outcome
                    </small>

                  </div>

                </div>

              </section>


              {/* TWO COLUMN */}

              <section className="two-column">


                {/* POLICY */}

                <div className="card">

                  <div className="card-heading">

                    <div>

                      <span>
                        AGENT DECISION POLICY
                      </span>

                      <h2>
                        Every action is bounded
                      </h2>

                    </div>

                  </div>


                  <div className="policy-list">

                    <div className="policy-item">

                      <strong>80+</strong>

                      <div>
                        <span>High Recovery</span>
                        <small>Automatic retry</small>
                      </div>

                    </div>


                    <div className="policy-item">

                      <strong>60–79</strong>

                      <div>
                        <span>Reminder</span>
                        <small>Customer intervention</small>
                      </div>

                    </div>


                    <div className="policy-item">

                      <strong>40–59</strong>

                      <div>
                        <span>Merchant Escalation</span>
                        <small>Human review</small>
                      </div>

                    </div>


                    <div className="policy-item">

                      <strong>&lt;40</strong>

                      <div>
                        <span>Stop Automation</span>
                        <small>Protect customer experience</small>
                      </div>

                    </div>

                  </div>

                </div>


                {/* ACTION DISTRIBUTION */}

                <div className="card">

                  <div className="card-heading">

                    <div>

                      <span>
                        AI ACTIONS
                      </span>

                      <h2>
                        Decision distribution
                      </h2>

                    </div>

                  </div>


                  <div className="action-list">

                    {Object.keys(actionDistribution).length === 0 ? (

                      <p className="empty-text">
                        Waiting for payment events...
                      </p>

                    ) : (

                      Object.entries(actionDistribution).map(
                        ([action, count]) => (

                          <div
                            className="action-row"
                            key={action}
                          >

                            <div>

                              <span
                                className={getActionClass(action)}
                              >
                                {formatAction(action)}
                              </span>

                              <div className="action-track">

                                <div
                                  style={{
                                    width: `${(count /
                                      Math.max(
                                        ...Object.values(
                                          actionDistribution
                                        )
                                      )) *
                                      100
                                      }%`,
                                  }}
                                />

                              </div>

                            </div>

                            <strong>
                              {count}
                            </strong>

                          </div>

                        )
                      )

                    )}

                  </div>

                </div>

              </section>


              {/* RECOVERY QUEUE */}

              <section className="card">

                <div className="card-heading">

                  <div>

                    <span>
                      RECOVERY QUEUE
                    </span>

                    <h2>
                      AI-generated recovery decisions
                    </h2>

                  </div>

                  <button
                    className="refresh-button"
                    onClick={loadDashboard}
                  >
                    ↻ Refresh
                  </button>

                </div>


                <div className="table-wrapper">

                  {payments.length === 0 ? (

                    <div className="empty-text">
                      No payment events found.
                    </div>

                  ) : (

                    <table>

                      <thead>

                        <tr>

                          <th>CUSTOMER</th>
                          <th>AMOUNT</th>
                          <th>FAILURE</th>
                          <th>AI SCORE</th>
                          <th>ACTION</th>
                          <th>GUARDRAIL</th>
                          <th>RESULT</th>

                        </tr>

                      </thead>


                      <tbody>

                        {payments.map((payment) => {

                          const probability =
                            Number(
                              payment.recovery_probability || 0
                            ) * 100;

                          return (

                            <tr
                              key={payment.id}
                              onClick={() =>
                                setSelectedPayment(payment)
                              }
                            >

                              <td>

                                <div className="customer-cell">

                                  <div className="customer-avatar">
                                    {(payment.customer_name ||
                                      "C")[0].toUpperCase()}
                                  </div>

                                  <div>

                                    <strong>
                                      {payment.customer_name ||
                                        "Customer"}
                                    </strong>

                                    <small>
                                      {payment.payment_id}
                                    </small>

                                  </div>

                                </div>

                              </td>


                              <td className="amount">
                                {formatCurrency(
                                  payment.amount
                                )}
                              </td>


                              <td>
                                <span className="failure">
                                  {getFailureLabel(
                                    payment.failure_type
                                  )}
                                </span>
                              </td>


                              <td>

                                <div className="score-cell">

                                  <strong
                                    className={getProbabilityClass(
                                      payment.recovery_probability
                                    )}
                                  >
                                    {probability.toFixed(2)}%
                                  </strong>

                                  <small>
                                    {getProbabilityLevel(
                                      payment.recovery_probability
                                    )}
                                  </small>

                                </div>

                              </td>


                              <td>

                                <span
                                  className={getActionClass(
                                    payment.final_action
                                  )}
                                >
                                  {formatAction(
                                    payment.final_action
                                  )}
                                </span>

                              </td>


                              <td>

                                {payment.guardrail_allowed ? (

                                  <span className="guardrail passed">
                                    ✓ PASSED
                                  </span>

                                ) : (

                                  <span className="guardrail blocked">
                                    ✕ BLOCKED
                                  </span>

                                )}

                              </td>


                              <td>

                                <span
                                  className={getStatusClass(
                                    payment.status
                                  )}
                                >
                                  {payment.status ||
                                    "UNKNOWN"}
                                </span>

                                {Number(
                                  payment.recovered_amount || 0
                                ) > 0 && (

                                    <small className="recovered-amount">
                                      +
                                      {formatCurrency(
                                        payment.recovered_amount
                                      )}
                                    </small>

                                  )}

                              </td>

                            </tr>

                          );

                        })}

                      </tbody>

                    </table>

                  )}

                </div>

              </section>

            </>

          )}


          {/* ================= RECOVERY CENTER ================= */}

          {activePage === "Recovery Center" && (

            <section className="module-page">

              <p className="eyebrow">
                AI REVENUE RECOVERY
              </p>

              <h1>
                Recovery Center
              </h1>

              <p>
                Monitor every automated recovery action
                generated by REVIVE AI.
              </p>

              <div className="module-grid">

                <div className="metric-card">
                  <span>RECOVERY RATE</span>
                  <strong>
                    {metrics.recovery_rate || 0}%
                  </strong>
                </div>

                <div className="metric-card recovered">
                  <span>RECOVERED REVENUE</span>
                  <strong>
                    {formatCurrency(
                      metrics.recovered_revenue
                    )}
                  </strong>
                </div>

                <div className="metric-card">
                  <span>PAYMENTS RECOVERED</span>
                  <strong>
                    {metrics.recovered_count || 0}
                  </strong>
                </div>

              </div>

            </section>

          )}


          {/* ================= TRANSACTIONS ================= */}

          {activePage === "Transactions" && (

            <section className="module-page">

              <p className="eyebrow">
                PAYMENT INTELLIGENCE
              </p>

              <h1>
                Transactions
              </h1>

              <p>
                Every payment failure entering the REVIVE AI
                recovery engine.
              </p>

              <div className="card transaction-card">

                <div className="table-wrapper">

                  <table>

                    <thead>

                      <tr>
                        <th>PAYMENT ID</th>
                        <th>CUSTOMER</th>
                        <th>AMOUNT</th>
                        <th>FAILURE</th>
                        <th>STATUS</th>
                      </tr>

                    </thead>

                    <tbody>

                      {payments.map((payment) => (

                        <tr
                          key={payment.id}
                          onClick={() =>
                            setSelectedPayment(payment)
                          }
                        >

                          <td>
                            <strong>
                              {payment.payment_id}
                            </strong>
                          </td>

                          <td>
                            {payment.customer_name ||
                              "Customer"}
                          </td>

                          <td className="amount">
                            {formatCurrency(payment.amount)}
                          </td>

                          <td>
                            {getFailureLabel(
                              payment.failure_type
                            )}
                          </td>

                          <td>
                            <span
                              className={getStatusClass(
                                payment.status
                              )}
                            >
                              {payment.status}
                            </span>
                          </td>

                        </tr>

                      ))}

                    </tbody>

                  </table>

                </div>

              </div>

            </section>

          )}


          {/* ================= AI INSIGHTS ================= */}

          {activePage === "AI Insights" && (

            <section className="module-page">

              <p className="eyebrow">
                INTELLIGENCE ENGINE
              </p>

              <h1>
                AI Insights
              </h1>

              <p>
                Recovery probabilities and AI-generated
                decision patterns across failed payments.
              </p>

              <div className="module-grid">

                <div className="metric-card">
                  <span>PAYMENTS ANALYZED</span>
                  <strong>
                    {metrics.total_payments || 0}
                  </strong>
                </div>

                <div className="metric-card">
                  <span>REVENUE AT RISK</span>
                  <strong>
                    {formatCurrency(
                      metrics.revenue_at_risk
                    )}
                  </strong>
                </div>

                <div className="metric-card recovered">
                  <span>RECOVERED</span>
                  <strong>
                    {formatCurrency(
                      metrics.recovered_revenue
                    )}
                  </strong>
                </div>

              </div>

              <div className="card insight-card">

                <div className="card-heading">

                  <div>
                    <span>FAILURE INTELLIGENCE</span>
                    <h2>
                      Payment failure patterns
                    </h2>
                  </div>

                </div>

                {Object.entries(failureDistribution).map(
                  ([failure, count]) => (

                    <div
                      className="insight-row"
                      key={failure}
                    >

                      <span>
                        {getFailureLabel(failure)}
                      </span>

                      <strong>
                        {count}
                      </strong>

                    </div>

                  )
                )}

              </div>

            </section>

          )}


          {/* ================= AUDIT TRAIL ================= */}

          {activePage === "Audit Trail" && (

            <section className="module-page">

              <p className="eyebrow">
                SYSTEM TRANSPARENCY
              </p>

              <h1>
                Audit Trail
              </h1>

              <p>
                Review AI decisions, guardrail outcomes,
                and recovery results.
              </p>

              <div className="card">

                {payments.map((payment) => (

                  <div
                    className="audit-row"
                    key={payment.id}
                  >

                    <div className="audit-dot"></div>

                    <div>

                      <strong>
                        {payment.payment_id}
                      </strong>

                      <small>
                        AI selected{" "}
                        {formatAction(
                          payment.final_action
                        )}{" "}
                        • Guardrail{" "}
                        {payment.guardrail_allowed
                          ? "PASSED"
                          : "BLOCKED"}
                      </small>

                    </div>

                    <span>
                      {payment.status}
                    </span>

                  </div>

                ))}

              </div>

            </section>

          )}

        </main>


        {/* ================= MODAL ================= */}

        {selectedPayment && (

          <div
            className="modal-overlay"
            onClick={() => setSelectedPayment(null)}
          >

            <div
              className="payment-modal"
              onClick={(event) =>
                event.stopPropagation()
              }
            >

              <button
                className="modal-close"
                onClick={() =>
                  setSelectedPayment(null)
                }
              >
                ×
              </button>

              <p className="eyebrow">
                AI DECISION EXPLANATION
              </p>

              <h2>
                {selectedPayment.payment_id}
              </h2>

              <div className="modal-details">

                <div>
                  <span>Customer</span>
                  <strong>
                    {selectedPayment.customer_name ||
                      "Customer"}
                  </strong>
                </div>

                <div>
                  <span>Amount</span>
                  <strong>
                    {formatCurrency(
                      selectedPayment.amount
                    )}
                  </strong>
                </div>

                <div>
                  <span>Failure</span>
                  <strong>
                    {getFailureLabel(
                      selectedPayment.failure_type
                    )}
                  </strong>
                </div>

                <div>
                  <span>Recovery Probability</span>
                  <strong>
                    {(
                      Number(
                        selectedPayment.recovery_probability ||
                        0
                      ) * 100
                    ).toFixed(2)}
                    %
                  </strong>
                </div>

                <div>
                  <span>AI Action</span>
                  <strong>
                    {formatAction(
                      selectedPayment.final_action
                    )}
                  </strong>
                </div>

                <div>
                  <span>Guardrail</span>
                  <strong>
                    {selectedPayment.guardrail_allowed
                      ? "✓ PASSED"
                      : "✕ BLOCKED"}
                  </strong>
                </div>

              </div>

              <div className="decision-box">

                <span>
                  DECISION FLOW
                </span>

                <p>
                  Payment failure detected → Recovery
                  probability calculated → Guardrail
                  evaluated → Final recovery action selected.
                </p>

              </div>

            </div>

          </div>

        )}

      </div>

    </div>
  );
}

export default App;