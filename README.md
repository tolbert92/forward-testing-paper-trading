# Forward Testing & Paper Trading

**Skill #7 — Portfolio Intelligence System**

**Version:** 1.0.0  
**Status:** Specification Published — Implementation Pending  
**Repository:** `forward-testing-paper-trading`

## 1. Project Overview

Forward Testing & Paper Trading is a portfolio intelligence skill designed to evaluate investment strategies using market observations that become available after a strategy decision.

The skill provides a controlled, hypothetical trading environment to assess strategy performance, risk exposure, execution assumptions, and benchmark-relative results before considering any real-world implementation.

It is designed to operate independently or as part of a multi-agent Portfolio Intelligence System.

**Important:** This skill is for research, analysis, and hypothetical simulation only. It does not execute real trades or connect to brokerage order-entry systems.

## 2. Core Capabilities

- Forward evaluation of frozen investment strategies
- Hypothetical portfolio and paper-trading simulation
- Buy-and-hold, scheduled rebalancing, threshold rebalancing, and rules-based strategies
- Simulated market, limit, stop, and stop-limit orders
- Execution modeling, including slippage, commissions, delays, and partial fills
- Portfolio accounting and immutable event-ledger tracking
- Performance, risk, and benchmark analysis
- Multiple benchmark and execution-scenario comparisons
- Portfolio visualization and reporting handoffs
- Stateful sessions, checkpoints, and recovery
- Data validation, audit trails, and reproducibility controls
- Integration with other portfolio intelligence skills

These capabilities describe the approved design. They are not yet implemented or independently verified.

## 3. Approved Design Decisions

All 10 design decisions were approved as **Option C**.

| Decision | Design Area | Approved Selection |
|---|---|---|
| D1 | Scope | Comprehensive Forward Testing & Paper Trading |
| D2 | Inputs | Hybrid standalone CSV/JSON and agent-to-agent contracts |
| D3 | Simulation | Comprehensive Hybrid Simulation Engine |
| D4 | Analytics | Comprehensive Performance Intelligence |
| D5 | Benchmarks | Dynamic Multi-Benchmark Intelligence |
| D6 | Execution | Comprehensive Market Execution Simulation |
| D7 | Outputs | Modular Reporting & Visualization Architecture |
| D8 | Governance | Comprehensive Validation & Simulation Governance |
| D9 | Operations | Dual-Mode Stateful Execution with Six-Phase Workflow |
| D10 | Testing | Comprehensive Testing with Three Acceptance Gates |

## 4. Six-Phase Workflow

The skill follows a structured six-phase workflow.

| Phase | Name | Primary Function |
|---|---|---|
| 1 | Initialize | Establish the simulation session, strategy, portfolio, and configuration |
| 2 | Validate | Verify inputs, market data, constraints, and strategy integrity |
| 3 | Monitor & Simulate | Evaluate market observations and process hypothetical trades |
| 4 | Analyze | Calculate portfolio performance, risk, and benchmark comparisons |
| 5 | Verify | Reconcile portfolio accounting, validate results, and check audit integrity |
| 6 | Deliver | Produce reports, machine-readable outputs, and agent handoffs |

Every phase must satisfy its applicable validation requirements before downstream results can be treated as verified.

## 5. Input Architecture

The skill supports two input methods.

### Standalone Input

- JSON files
- CSV files normalized to the canonical data contract
- Portfolio holdings and cash balances
- Strategy definitions and allocation targets
- Timestamped market observations
- Benchmark policies
- Risk constraints and execution assumptions

### Agent-to-Agent Input

The skill is designed to receive standardized, versioned information from other portfolio intelligence skills.

All inputs must pass the same validation rules regardless of their source.

### Required Data Controls

- Point-in-time market-data availability
- Versioned and frozen strategy definitions
- Valid instrument identifiers
- Consistent currencies and units
- Explicit timestamps and timezones
- Source provenance and input hashes
- Reproducible simulation assumptions

## 6. Simulation Engine

The planned simulation engine supports:

**Strategy evaluation**
- Buy-and-hold
- Scheduled rebalancing
- Threshold-based rebalancing
- Rules-based trading

**Hypothetical execution**
- Market orders
- Limit orders
- Stop orders
- Stop-limit orders
- Partial fills
- Order cancellations, rejections, and expiration

**Execution assumptions**
- Commission and transaction fees
- Bid-ask spread
- Slippage
- Execution delays
- Liquidity and volume participation
- Modeled market impact

**Portfolio accounting**
- Cash balances
- Holdings and position values
- Realized and unrealized profit/loss
- Dividends and stock splits
- External deposits and withdrawals
- Portfolio net asset value

All calculations must be traceable to an authoritative event ledger.

## 7. Performance Intelligence

The skill is designed to calculate the following metrics when sufficient valid data is available.

| Category | Metrics |
|---|---|
| Returns | Total return, periodic returns, CAGR, time-weighted return, money-weighted return |
| Risk | Volatility, maximum drawdown, concentration, exposure |
| Risk-Adjusted Performance | Sharpe ratio, Sortino ratio, Calmar ratio |
| Benchmark Comparison | Excess return, alpha, beta, tracking error, information ratio |
| Trading Performance | Turnover, execution costs, fill rate, realized and unrealized P&L |
| Portfolio Attribution | Allocation and security contribution |
| Governance | Rule adherence, validation findings, strategy drift |

Unavailable or statistically unreliable metrics must be reported as `null` with an explanation rather than estimated without support.

## 8. Benchmark Intelligence

The skill supports a versioned benchmark policy containing one or more:

- Equity benchmarks
- Fixed-income benchmarks
- Sector benchmarks
- International benchmarks
- Blended benchmarks
- User-defined benchmarks

Benchmark definitions must be established before the relevant forward-testing period.

Retroactively selecting the best-performing benchmark and presenting it as the original benchmark is prohibited.

## 9. Reporting and Visualization

The planned reporting architecture supports:

- Canonical JSON results
- CSV exports
- HTML reports
- PDF reports
- Portfolio performance summaries
- Risk and exposure summaries
- Benchmark comparisons
- Execution-quality reports
- Event-ledger extracts
- Visualization-ready datasets

### 3D Portfolio Visualization Integration

Skill #7 is designed to supply validated portfolio data to Skill #6 — 3D Portfolio Visualization.

Potential visualization dimensions include:

- Portfolio value over time
- Risk versus return
- Portfolio allocation and exposure
- Benchmark-relative performance
- Drawdown and volatility
- Strategy scenario comparisons

Visualization must preserve the underlying validated calculations and disclose any rendering simplifications.

## 10. Portfolio Intelligence Integration

| Connected Skill | Integration Purpose |
|---|---|
| Individual Investment Profile Builder | Investment objectives, restrictions, and investor constraints |
| Market Data Analyst | Timestamped prices, market observations, and corporate actions |
| Portfolio Optimization | Strategy definitions, target allocations, and portfolio rules |
| Portfolio Risk Assessment | Risk limits, exposure monitoring, and alerts |
| Historical Portfolio Backtesting | Historical reference performance and assumptions |
| 3D Portfolio Visualization | Interactive visualization of validated simulation results |
| Strategy Comparison | Comparative strategy evaluation |
| Decision Support | Research findings and decision-ready analysis |

Integration contracts must include schema versions, provenance, timestamps, identifiers, and validation results.

## 11. Validation and Governance

The skill uses three validation severity levels.

| Severity | Description | Required Response |
|---|---|---|
| Critical | Invalid data or conditions that compromise simulation integrity | Block affected operations |
| Warning | Limitations that may reduce reliability | Continue only when safe and disclose limitations |
| Informational | Expected conditions or noncritical observations | Record and report |

### Mandatory Safeguards

1. Prevent look-ahead bias and future-data leakage.
2. Maintain immutable simulation records.
3. Prevent duplicate order and cash-flow processing.
4. Enforce frozen strategy and benchmark definitions.
5. Reconcile cash, holdings, and portfolio valuations.
6. Preserve source provenance and execution assumptions.
7. Record errors and validation findings.
8. Never represent simulated trades as actual executions.

## 12. Execution Modes

### On-Demand Mode

A user or authorized agent initiates a defined evaluation.

The simulation processes the requested interval, validates the results, and produces reports.

### Stateful Recurring Mode

An external scheduler or event source initiates subsequent evaluation cycles.

The skill maintains session state, market-data watermarks, ledger checkpoints, and recovery information.

Recurring execution requires a separately configured runtime, durable storage, and operational controls.

## 13. Planned Repository Structure

```text
forward-testing-paper-trading/
├── README.md
├── SKILL.md
├── docs/
│   ├── METHODOLOGY.md
│   ├── VALIDATION_RULES.md
│   └── TEST_PLAN.md
├── schemas/
│   ├── forward-test-input.schema.json
│   ├── forward-test-output.schema.json
│   ├── order-event.schema.json
│   └── visualization-handoff.schema.json
├── examples/
│   ├── reference-input.json
│   ├── reference-output.json
│   └── reference-events.json
├── src/forward_testing/
│   ├── engine.py
│   ├── ledger.py
│   ├── execution.py
│   ├── analytics.py
│   └── validation.py
├── tests/
│   ├── test_contracts.py
│   ├── test_reference_cases.py
│   ├── test_order_lifecycle.py
│   ├── test_temporal_integrity.py
│   ├── test_recovery.py
│   └── test_integration.py
└── .github/workflows/test.yml
```

**Note:** This structure represents the planned implementation. The initial repository contains the README and SKILL specification only.

## 14. Testing Strategy

Testing will include:

- Input and output schema validation
- Deterministic portfolio accounting
- Hypothetical order lifecycle
- Fees and slippage calculations
- Partial fills and cancellations
- Insufficient cash and risk-limit rejection
- Point-in-time data integrity
- Benchmark governance
- External cash-flow accounting
- Corporate-action processing
- Session recovery and idempotency
- Agent-to-agent integration

The specification defines 12 reference test cases, FT-001 through FT-012.

Automated tests must use independently established expected results, deterministic fixtures, and reproducible execution environments.

## 15. Three Acceptance Gates

### Gate 1 — GitHub Publication and Contracts

Requirements:

- Published SKILL.md and README.md
- Versioned JSON schemas
- Valid reference input/output fixtures
- GitHub Actions testing workflow
- Passing automated contract tests
- Retained test logs and evidence

**Current status:** In progress.

### Gate 2 — Functional Simulation Engine

Requirements:

- Implemented simulation engine
- Verified portfolio ledger
- Deterministic order processing
- Validated portfolio accounting
- Point-in-time market-data protection
- Session recovery
- Passing independent numerical tests

**Current status:** Not started.

### Gate 3 — End-to-End Agent Integration

Requirements:

- Working agent-to-agent data exchanges
- Schema compatibility
- Integrated simulation and analytics
- Validated visualization handoff
- Fault handling and reproducibility
- Passing integration tests

**Current status:** Not started.

## 16. Implementation Roadmap

| Stage | Deliverable | Status |
|---|---|---|
| 1 | GitHub repository | Complete |
| 2 | SKILL.md specification | Complete |
| 3 | Expanded README.md | In progress |
| 4 | Canonical JSON schemas | Pending |
| 5 | Reference examples and contract tests | Pending |
| 6 | GitHub Actions testing | Pending |
| 7 | Portfolio ledger and simulation engine | Pending |
| 8 | Performance and benchmark analytics | Pending |
| 9 | Reporting and visualization adapters | Pending |
| 10 | Agent integration and final acceptance | Pending |

The roadmap reflects the initial publication stage and must be updated as implementation evidence becomes available.

## 17. Definition of Done

Skill #7 will be considered complete only when:

1. All required schemas and contracts are published.
2. The simulation engine passes independently verified tests.
3. Portfolio accounting and execution results reconcile.
4. Forward-testing controls prevent future-data leakage.
5. Performance and risk analytics are validated.
6. Visualization and reporting outputs match canonical results.
7. Agent-to-agent integration tests pass.
8. All three acceptance gates are satisfied with retained evidence.

Publishing the specification alone does not establish that the simulation engine is operational.

## 18. Investment Simulation Disclaimer

**Hypothetical simulation only.**

This project is intended for research, education, and portfolio strategy evaluation.

Simulated results do not represent actual brokerage executions or realized investment performance. Historical and simulated performance do not guarantee future results.

Execution assumptions, market liquidity, transaction costs, market-data quality, and model limitations may materially affect outcomes.

No live trading functionality is included.

---

**Skill #7 — Forward Testing & Paper Trading**  
**Version 1.0.0 | Specification Stage**  
**Portfolio Intelligence System**
