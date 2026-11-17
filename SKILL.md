---
name: forward-testing-paper-trading
description: Stateful, auditable forward-testing and hypothetical paper-trading capability for evaluating portfolio strategies against subsequently available market observations. Supports standalone CSV/JSON and standardized agent handoffs, simulated execution, risk and performance analysis, and reproducible reports. Never submits real orders.
version: 1.0.0
status: specification
---

# Skill #7 — Forward Testing & Paper Trading

**Version:** 1.0.0
**Maturity:** Specification only; implementation and acceptance gates remain outstanding.
**Purpose:** Evaluate frozen investment strategies on market information available after the strategy decision, using a controlled, stateful, hypothetical portfolio ledger.
**Boundary:** This skill must never place real orders, connect to brokerage order-entry endpoints, or describe simulated performance as live investment performance.

## 1. Approved design decisions

All ten decisions were approved as Option C:

| ID | Area | Approved selection |
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

## 2. Non-negotiable principles

1. Simulation only. No real orders, brokerage execution, or implied guarantee of returns.
2. Point-in-time correctness. A decision may use only observations whose `available_at` is at or before `decision_at`. Exchange/event timestamps alone do not establish availability.
3. Immutable decision provenance. Freeze and hash strategy, benchmark policy, cost assumptions, risk rules, and starting state before each evaluation period. Version authorized changes prospectively.
4. Orders are not fills. Separate signals, orders, acknowledgments, simulated fills, settlements, cash movements, and valuations.
5. Single authoritative ledger. Reconstruct holdings, cash, and P&L from accepted immutable events. Do not silently edit historical fills.
6. Reproducible results. Record input snapshot hashes, calendar, timezone, pricing policy, engine version, and deterministic random seed when applicable.
7. Fail closed. Critical validation failures stop affected operations; warnings are surfaced and preserved.
8. No unsupported precision. Unavailable or statistically unreliable metrics must be `null` with a reason; never fabricate prices, fills, benchmarks, or market conditions.

## 3. Capability boundaries

### Included

- Passive buy-and-hold and rule-based strategies.
- On-demand evaluation and scheduler/event-triggered sessions when an external runtime is provided.
- Market, limit, stop, and stop-limit hypothetical orders; configurable time-in-force.
- Partial fills, rejections, cancellations, expiration, execution delays, and configurable cost/liquidity models.
- Long-only by default; optional short positions only with explicitly configured margin, borrow, and risk policies.
- Deposits, withdrawals, dividends, splits, rebalancing, benchmark series, performance and risk analytics.
- Daily/weekly/monthly summaries; canonical JSON, CSV, HTML, PDF and visualization handoffs when corresponding renderers are installed.

### Excluded unless separately implemented and approved

- Live brokerage connectivity and actual trading.
- Guaranteed exchange-level fill reconstruction from daily OHLCV alone.
- Tax advice or tax-lot optimization beyond explicitly documented hypothetical accounting rules.
- Automatic corporate-action coverage without an authoritative point-in-time event feed.
- Unattended monitoring without a scheduler, durable storage, secrets management, and operational controls.

## 4. Repository layout

```text
forward-testing-paper-trading/
├── SKILL.md
├── README.md
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

The layout describes planned files; this SKILL.md does not imply they have been created.

## 5. Input contract (canonical JSON)

The implementation must publish JSON Schema Draft 2020-12 for this contract and pin `schema_version` to a supported semantic version. Standalone CSV adapters normalize into this same canonical representation; direct agent handoffs must use the same validator.

```json
{
  "schema_version": "1.0.0",
  "request_id": "req-reference-001",
  "session_id": "paper-reference-001",
  "mode": "on_demand",
  "base_currency": "USD",
  "timezone": "America/New_York",
  "strategy": {
    "strategy_id": "balanced-60-40",
    "version": "1.0.0",
    "frozen_at": "2026-01-02T14:00:00Z",
    "rules": {"type": "buy_and_hold"},
    "target_weights": {"EQUITY": 0.6, "BOND": 0.4}
  },
  "portfolio": {
    "as_of": "2026-01-02T14:00:00Z",
    "cash": "10000.00",
    "positions": [],
    "external_flows": []
  },
  "instruments": [
    {"instrument_id": "EQUITY", "currency": "USD", "asset_class": "equity"},
    {"instrument_id": "BOND", "currency": "USD", "asset_class": "fixed_income"}
  ],
  "market_observations": [
    {"instrument_id": "EQUITY", "observed_at": "2026-01-02T14:30:00Z", "available_at": "2026-01-02T14:30:01Z", "price": "100.00", "volume": "100000"},
    {"instrument_id": "BOND", "observed_at": "2026-01-02T14:30:00Z", "available_at": "2026-01-02T14:30:01Z", "price": "100.00", "volume": "100000"}
  ],
  "benchmark_policy": {
    "version": "1.0.0",
    "frozen_at": "2026-01-02T14:00:00Z",
    "components": [{"benchmark_id": "EQUITY", "weight": 0.6}, {"benchmark_id": "BOND", "weight": 0.4}],
    "rebalance_policy": "none"
  },
  "execution_policy": {
    "price_model": "next_eligible_observation",
    "commission_per_order": "0.00",
    "slippage_bps": "0",
    "max_volume_participation": 0.1,
    "allow_short": false
  },
  "risk_policy": {"max_gross_exposure": 1.0, "max_position_weight": 0.7},
  "evaluation": {"decision_at": "2026-01-02T14:30:02Z", "through": "2026-01-02T21:00:00Z"},
  "provenance": {"source": "standalone", "input_snapshot_hash": "to-be-computed"}
}
```

### 5.1 Mandatory input rules

- All timestamps must be ISO 8601 with explicit UTC offset; store normalized UTC values.
- Monetary values, quantities, prices, and costs use decimal strings internally to avoid binary floating-point ledger drift. Percentages/weights must have explicit unit definitions.
- IDs must be unique in scope; event IDs and request IDs must support idempotency.
- Starting positions require instrument, quantity, cost basis policy, and valuation mark; starting cash cannot be inferred.
- All traded instruments must have a validated instrument identifier, currency, trading calendar, lot-size/tick-size policy, and supported market-data source.
- The sum of target weights must equal 1 within a declared tolerance for fully invested strategies; otherwise explicit target cash weight is required.
- Source adapters must identify their provenance, data license, retrieval time, and whether quotes are adjusted or unadjusted.
- Incompatible schema versions, future information, negative invalid prices, impossible account state, and missing required market data are critical failures.
- CSV adapters must define header mapping, timestamp interpretation, numeric locale, encoding, and deterministic row order.

### 5.2 Agent inputs

| Producer | Input supplied | Required verification |
|---|---|---|
| Individual Investment Profile Builder | Objectives, restrictions, horizon, suitability constraints | Provenance and effective date |
| Market Data Analyst | Timestamped observations, corporate actions, calendars | `observed_at`, `available_at`, freshness, licensing |
| Portfolio Optimization | Strategy version, weights, trading rules | Frozen strategy and constraint compatibility |
| Portfolio Risk Assessment | Exposure and drawdown limits, risk alerts | Risk policy version and enforcement priority |
| Historical Portfolio Backtesting | Historical reference statistics and benchmark definitions | No leakage of future data into current decision |

Missing agents must not prevent standalone use if all required validated inputs are supplied.

## 6. Six-phase execution workflow

### Phase 1 — Initialize

- Accept `request_id`, session identifier, execution mode, starting portfolio and frozen strategy.
- Load or create a durable session with status `created`; resolve configuration versions and input snapshot hashes.
- Resolve calendar, market-data policy, instrument metadata, benchmark policy, cost model, and risk limits.
- Acquire a session lock or use optimistic concurrency with an expected ledger sequence number.
- Produce a run manifest and transition to `initialized`.

### Phase 2 — Validate

- Validate schemas, currency consistency, decimal precision, identifiers, permissions, and strategy restrictions.
- Confirm strategy/benchmark versions were fixed before evaluation and all decisions use point-in-time available information.
- Check observation freshness, calendar compatibility, data gaps, corporate actions, and eligible order types.
- Apply severity levels from Section 12. Critical findings block affected execution and produce a machine-readable failure result.
- Transition to `validated` only after critical gates pass.

### Phase 3 — Monitor & Simulate

- Consume only new observations whose availability time is not later than the current decision time.
- Apply strategy rules to a snapshot of the portfolio state and produce immutable decision/signal records.
- Validate hypothetical orders against market hours, available cash, lot sizes, limits, and configured exposure rules.
- Apply eligible simulated fills according to explicit execution assumptions; update the event ledger and derived holdings.
- Process external cash flows and supported corporate actions with effective dates and audit records.
- Record portfolio valuation snapshots and checkpoints. On-demand runs stop at the requested boundary; recurring runs await external triggers.

### Phase 4 — Analyze

- Calculate NAV, cash, holdings, realized/unrealized P&L, returns, risk metrics, benchmark-relative results, attribution, execution quality, and rule adherence.
- Use appropriate annualization and observation-frequency conventions; provide `null` and a reason where data is insufficient.
- Compare forward performance to frozen historical expectations without rewriting historical results.

### Phase 5 — Verify

- Independently reconcile opening equity + external cash flows + market/transaction effects to closing equity.
- Check that fills, fees, orders, positions, cash, valuations, and benchmarks agree within declared tolerances.
- Confirm no duplicated events, missing sequence numbers, future-data use, or unauthorized strategy changes.
- Produce a signed/hashable verification manifest; mark run `verified` only when all critical checks pass.

### Phase 6 — Deliver

- Publish canonical machine-readable output, ledger extracts, benchmark and risk summaries, and visualization handoff.
- Optionally render HTML/PDF/CSV using installed adapters; never claim an artifact was produced if its renderer is unavailable.
- Persist state and report references atomically; emit events for subscribed agents only after successful verification.
- Record warnings, limitations, and simulated-performance disclosure.

## 7. Session lifecycle and recovery

Allowed states: `created`, `initialized`, `validated`, `running`, `paused`, `verifying`, `verified`, `completed`, `failed`, `terminated`.

- Valid transitions must be enforced by a documented state machine. A terminal state is immutable except through an explicit correction/revision workflow.
- Every input event has a globally unique `event_id`, source ID, timestamp, and deterministic session sequence.
- A repeated `event_id` with identical payload is a no-op; a repeated ID with different payload is a critical conflict.
- Checkpoints store ledger offset, portfolio snapshot hash, strategy version, market-data watermark, and engine version.
- Recovery replays events after the last verified checkpoint; it cannot duplicate orders, fills, or cash flows.
- Pause prevents new strategy decisions but must define whether queued orders are canceled, frozen, or still evaluated. Default: cancel unfilled simulated orders unless policy explicitly says otherwise.
- On termination, cancel remaining open simulated orders, reconcile the ledger, and produce a final disclosure report.
- An external scheduler/event transport is required for ongoing operation; this specification does not create one.

## 8. Strategy and order simulation

### 8.1 Strategy modes

- `buy_and_hold`: establish holdings at eligible simulated execution prices, then track value and cash flows.
- `scheduled_rebalance`: evaluate target allocations at predeclared schedule boundaries.
- `threshold_rebalance`: trade when absolute or relative allocation drift breaches a predeclared threshold.
- `rules_based`: evaluate versioned, deterministic rules against point-in-time observations.

### 8.2 Order state machine

`created → submitted → accepted → partially_filled → filled` with permissible exits to `rejected`, `canceled`, or `expired` based on policy. A partially filled order can be canceled or expire with remaining quantity; filled quantity is never undone by cancellation. Any correction must be a separate reversing event.

- Market orders: use the next eligible observation after submission and configured delay; never fill at a previously known closing price merely because it is convenient.
- Limit orders: fill only if eligible executable-side quotes satisfy the limit; with OHLC-only data, apply a conservative documented bar-based approximation or mark fill uncertain/unavailable.
- Stop and stop-limit orders: trigger and execution must be separate events; gap-through behavior must follow declared assumptions.
- Partial fills: bounded by available volume and participation assumptions; volume is not a promise of executable liquidity.
- Cost model: commissions, fixed/variable fees, bid-ask spread, slippage, modeled market impact, and applicable borrow costs where enabled.
- Reject or resize orders with insufficient cash or violated limits according to explicit policy; never silently create leverage.
- Corporate actions: apply splits to shares and open-order prices/quantities; apply dividends on ex/record/pay dates per documented convention.

### 8.3 Execution scenario analysis

Run baseline, optimistic, and conservative assumptions on separate scenario IDs, each with its own event ledger and reports. Scenario assumptions must be declared before evaluation and cannot be selected retrospectively as the official result.

## 9. Portfolio accounting

- Equity/NAV at time `t`: `cash_t + Σ(quantity_i,t × eligible_mark_price_i,t × FX_i,t) − liabilities_t`.
- Cash updates: opening cash + deposits − withdrawals − buy settlement + sell settlement + dividends − fees − other modeled charges.
- Fees are charged exactly once at the defined event; partial fills allocate costs according to policy.
- Realized P&L requires a declared cost-basis method (e.g., FIFO or average cost). Unrealized P&L uses remaining basis and eligible marks.
- External cash flows must not be counted as investment return; report both flow-adjusted and dollar-value changes.
- FX conversions require point-in-time rates and an explicit missing-rate policy.
- If settlement is modeled, distinguish settled cash from unsettled proceeds and enforce buying-power rules.
- Use deterministic decimal arithmetic and documented rounding at transaction and report boundaries.

## 10. Analytics and benchmarks

### 10.1 Required analytics

| Category | Measures |
|---|---|
| Return | Total return, period returns, CAGR when meaningful, TWR, XIRR when well-defined, rolling returns |
| Risk adjusted | Sharpe, Sortino, Calmar with documented risk-free rate, MAR, annualization and sample thresholds |
| Risk | Volatility, maximum/current drawdown, concentration, exposures, leverage, allocation drift |
| Benchmark | Excess return, alpha, beta, tracking error, information ratio, rolling relative performance |
| Trading | Realized/unrealized P&L, turnover, commissions, slippage, fill rate, rejection rate, execution delay |
| Attribution | Security and allocation contribution, with explicit attribution methodology |
| Governance | Rule adherence, drift from frozen historical assumptions, validation findings |

- Return conventions must identify valuation timestamps, treatment of external flows, dividends, fees, and benchmark reinvestment.
- TWR segments at external cash-flow boundaries and geometrically links subperiod returns.
- XIRR is reported only where cash-flow sign and root/solver conditions permit a defensible solution; document multiple-root ambiguity.
- CAGR requires a positive valid starting value and meaningful elapsed period; do not annualize short/noisy samples without disclosure.
- Sharpe/Sortino/Calmar and regression-based alpha/beta must be `null` with reason if samples, benchmark alignment, or denominator are insufficient.
- Compare aligned calendars, timestamps, currencies, dividend treatment, and valuation frequency; avoid silently forward-filling untradable marks.

### 10.2 Benchmark governance

- Support one or more equity, bond, sector, international, blended, or user-defined benchmarks.
- Record benchmark IDs, weights, rebalance policy, inception/effective date, and policy version before the forward interval.
- Dynamic recommendations are permitted prospectively; no retroactive benchmark shopping.
- Benchmark constituent prices must satisfy the same point-in-time and data-quality gates as strategy prices.
- Publish both primary benchmark and optional supplemental comparisons, clearly labeled.

## 11. Output contract

Every completed or failed evaluation must return a versioned envelope. A completed run includes the following logical structure:

```json
{
  "schema_version": "1.0.0",
  "request_id": "req-reference-001",
  "session_id": "paper-reference-001",
  "run_id": "run-001",
  "status": "completed",
  "simulation_only": true,
  "strategy": {"strategy_id": "balanced-60-40", "version": "1.0.0"},
  "period": {"start": "2026-01-02T14:30:02Z", "end": "2026-01-02T21:00:00Z"},
  "portfolio": {
    "base_currency": "USD",
    "ending_nav": "10000.00",
    "cash": "0.00",
    "positions": [],
    "external_flows": "0.00"
  },
  "performance": {"total_return": 0.0, "twr": 0.0, "xirr": null, "xirr_unavailable_reason": "insufficient_cash_flow_history"},
  "risk": {"max_drawdown": 0.0, "sharpe": null, "sharpe_unavailable_reason": "insufficient_observations"},
  "benchmarks": [],
  "orders": [],
  "fills": [],
  "ledger_reference": "ledger://paper-reference-001/run-001",
  "validation": {"critical": [], "warnings": [], "info": []},
  "verification": {"passed": true, "ledger_reconciled": true},
  "provenance": {"engine_version": "implementation-required", "input_snapshot_hash": "to-be-computed"},
  "artifacts": [],
  "disclosure": "Hypothetical paper-trading simulation; not actual investment performance."
}
```

Illustrative shape only: The above numbers and empty arrays are placeholders showing field structure, not a valid completed result for the sample input. An implementation must generate outputs from its ledger and validator, never copy this example as a computed result. All outputs must conform to a published JSON Schema.

### 11.1 Required output datasets

1. Canonical result JSON with status, assumptions, metrics, quality findings, and provenance.
2. Ordered event ledger with order, fill, cash-flow, corporate-action, and valuation events.
3. Portfolio NAV/equity curve and position/cash snapshots.
4. Primary and supplemental benchmark curves with aligned time axes.
5. Trading/execution quality summary and risk-alert history.
6. Visualization handoff containing version, units, timestamp arrays, point counts, provenance, and disabled features when data is insufficient.
7. Optional CSV, HTML, and PDF exports; reports must match the canonical JSON.

## 12. Validation severity and failure rules

| Severity | Examples | Required behavior |
|---|---|---|
| Critical | Future-data use, conflicting event IDs, unsupported schema, negative invalid price, cash/holdings mismatch, unauthorized strategy change, impossible fill | Block affected simulation, preserve evidence, return structured failure |
| Warning | Incomplete benchmark, sparse return history, modeled liquidity, delayed data, uncertain OHLC fill | Continue only if safe, disable unreliable analytics, disclose limitations |
| Informational | No rebalance triggered, expected market closure, no orders generated | Record in audit log and report |

- Critical failures cannot be downgraded by a presentation layer.
- Validation findings include code, severity, message, field/event reference, detection time, remediation, and whether operation continued.
- Risk breaches may block new orders, freeze affected instruments, or terminate the session according to a predeclared risk policy.
- A stale-price warning cannot be ignored when stale pricing would materially affect order eligibility; elevate to critical for that operation.

## 13. Integration and visualization handoff

### Consumer outputs

| Consumer | Delivered data |
|---|---|
| Portfolio Optimization | Realized simulated performance, deviations, constraints, strategy feedback |
| Portfolio Risk Assessment | Holdings, exposures, risk metrics, alerts, valuation history |
| Historical Portfolio Backtesting | Comparable out-of-sample metrics and frozen assumption metadata |
| 3D Portfolio Visualization | Validated time-series, portfolio and benchmark curves, risk/return dimensions |
| Strategy Comparison | Consistent per-strategy performance and execution summaries |
| Decision Support | Decision-ready findings, uncertainties, warnings, and audit provenance |

- Use explicit `schema_version`, producer, consumer, `run_id`, correlation ID, UTC timestamp, payload hash, and status in every handoff.
- Reject incompatible versions and invalid units rather than coercing silently.
- A visualization adapter cannot change canonical calculations; if it downsamples, it must preserve original point count and describe the sampling method.
- All consumer systems must display the `simulation_only` disclosure.

## 14. Reference cases and acceptance tests

### FT-001 — Deterministic buy-and-hold accounting

Hypothetical input: Initial cash $10,000; zero fees/slippage; buy 60 shares of EQUITY at $100 and 40 shares of BOND at $100 at eligible simulated execution times. No flows. Later eligible marks: EQUITY $110 and BOND $105.

Independent expected results:

- Initial purchases: $6,000 + $4,000 = $10,000; remaining cash $0.
- Ending equity holding: 60 × $110 = $6,600.
- Ending bond holding: 40 × $105 = $4,200.
- Ending NAV: $10,800; total return: 8.00%; total unrealized P&L: $800.
- No order may fill before its submission and next eligible price availability.

This is a numerical acceptance test for a future engine, not evidence the engine exists.

### FT-002 — Fees and slippage

Buy 10 shares at an eligible modeled fill price of $101 and charge $2 commission. Starting cash $1,100. Expected ending cash: $1,100 − $1,010 − $2 = $88; holdings 10 shares; fee ledger exactly $2. Verify the execution model, not only fixture values.

### FT-003 — Insufficient cash

Attempt a $1,200 buy with $1,000 available and no leverage. Expected: reject or policy-defined downsize, no negative cash, immutable reason code.

### FT-004 — Point-in-time guard

Decision at 14:30:00Z; quote available at 14:30:01Z. Expected: quote inaccessible to that decision, even if `observed_at` is earlier.

### FT-005 — Partial fill and cancellation

Order 100 units; eligible modeled liquidity fills 30, then remaining 70 canceled. Expected: filled quantity 30, canceled remainder 70, only 30 shares and corresponding cash changes posted.

### FT-006 — Replay/idempotency

Apply same event twice. Expected: ledger, NAV, cash, and order counts unchanged on duplicate; conflicting duplicate ID fails.

### FT-007 — External cash flow and TWR

Deposit cash between valuation intervals. Expected: NAV increases by deposit, but investment return excludes external flow using independently computed subperiod returns.

### FT-008 — Benchmark integrity

Benchmark chosen after results are known. Expected: cannot be relabeled as precommitted primary benchmark for earlier period.

### FT-009 — Risk gates

Attempt trade exceeding frozen max-position or gross-exposure limit. Expected: blocked or resized per predeclared policy with audit finding.

### FT-010 — Missing data and metrics

Insufficient returns for Sharpe or missing benchmark dates. Expected: relevant metric `null`, reason code and visible warning; no fabricated result.

### FT-011 — Corporate action

Apply a 2-for-1 split. Expected: quantity doubles, unit cost basis halves, pre/post split portfolio economic value unchanged absent market movement.

### FT-012 — Agent integration

Pass versioned Portfolio Optimization strategy and Market Data Analyst quotes into forward testing, then deliver canonical outputs to Risk Assessment, 3D Visualization, and Strategy Comparison. Expected: valid schema, consistent units, reproducible values, simulation disclosure.

## 15. Testing requirements and GitHub Actions

- Run unit, schema, numerical reference, order-state, temporal-integrity, recovery, and integration tests as distinct suites.
- Include a nonzero test discovery assertion; `0 tests` must fail the CI job.
- Test expected values must be independently calculated or derived from separate reference implementations, not imported from the engine under test.
- CI must report actual test count, failures, skipped tests, environment, dependency lockfile hash, and engine version.
- Retain machine-readable JUnit XML or equivalent, plus human-readable logs, as downloadable workflow artifacts.
- Run negative tests for invalid data and unauthorized transitions, including replay and corrupted checkpoints.
- Use deterministic fixture dates and mock market feeds. External paid/live feeds must not be required for unit tests.
- Apply test thresholds for numerical tolerance, sample sufficiency, and reproducibility, with documented rationale.
- Require integration tests to verify actual exchange between skills, not merely JSON fixture conformance.

## 16. Three acceptance gates

### Gate 1 — GitHub publication and contracts

Required evidence: Public or designated repository; complete `SKILL.md` and `README.md`; versioned input/output/event/visualization schemas; valid example fixtures; GitHub Actions workflow; a nonzero count of passing automated contract tests; downloadable logs/artifacts; no unresolved critical contract failures.

Does not establish: A working simulation engine.

### Gate 2 — Independently verified functional engine

Required evidence: Implemented source modules; deterministic and repeatable simulation; independently verified FT-001 through FT-011 (or equivalent expanded suite); order lifecycle; cash/holdings reconciliation; look-ahead controls; checkpoint recovery; documented execution assumptions; automated numerical tests passing.

Does not establish: End-to-end agent integration.

### Gate 3 — End-to-end integration

Required evidence: Actual producer-to-consumer handoffs across relevant portfolio skills; schema/version compatibility; reproducible integrated test run; consistent metrics and simulation disclosure in outputs; fault/retry handling; published integration test evidence and acceptance signoff.

Release policy: A green contract-test badge must not be represented as Gate 2 or Gate 3 completion.

## 17. Implementation sequence

1. Publish specification and canonical JSON schemas.
2. Create independent, internally consistent reference fixtures and contract tests.
3. Implement decimal portfolio ledger, order lifecycle, and point-in-time market-data validation.
4. Implement deterministic passive strategy and FT-001 numerical test.
5. Add execution costs, partial fills, risk gates, cash flows, and corporate actions.
6. Add scheduled/rules-based strategies, benchmarks, performance/risk analytics, and reporting adapters.
7. Add persistent sessions, checkpoint recovery, idempotency, and external scheduler integration.
8. Complete agent handoffs and three-gate acceptance verification.

## 18. Required user-facing disclosures

Every report must state:

> **Hypothetical simulation only.** Results reflect modeled trades and assumptions, not actual brokerage executions or realized investment performance. Historical and simulated results do not guarantee future outcomes. Liquidity, data quality, market impact, and execution assumptions may materially affect results.

If market-data timestamps, liquidity, cost models, or sample sizes are insufficient, identify the limitation in the report and machine-readable output.

## 19. Definition of done

This skill is complete only when all three acceptance gates pass with retained evidence. Until then, label the repository and README accurately as specification, prototype, or integrated according to the highest verified gate, and explicitly identify outstanding implementation work.
