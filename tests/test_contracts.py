
"""
Skill #7 — Forward Testing & Paper Trading
Acceptance Gate 1: Contract and Reference Fixture Tests

Run:
    python -m pip install "jsonschema[format]>=4.23,<5" pytest
    python -m pytest -v tests/test_contracts.py

Scope:
- JSON Schema Draft 2020-12 validity
- Reference fixture contract compliance
- Individual event validation
- Event ordering and lifecycle
- Fill reconciliation
- Portfolio NAV and return
- Negative contract tests

These tests do not implement or verify a trading engine.
"""

import json
from collections import Counter
from decimal import Decimal
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"

SCHEMA_FILES = {
    "input": "forward-test-input.schema.json",
    "output": "forward-test-output.schema.json",
    "event": "order-event.schema.json",
    "handoff": "visualization-handoff.schema.json",
}

D = Decimal


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="module")
def schemas():
    return {
        name: load_json(SCHEMAS / filename)
        for name, filename in SCHEMA_FILES.items()
    }


@pytest.fixture(scope="module")
def fixtures():
    return {
        "input": load_json(EXAMPLES / "reference-input.json"),
        "output": load_json(EXAMPLES / "reference-output.json"),
        "events": load_json(EXAMPLES / "reference-events.json"),
    }


def validator(schema):
    return Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )


def assert_valid(instance, schema):
    errors = sorted(
        validator(schema).iter_errors(instance),
        key=lambda error: str(error.absolute_path),
    )
    assert not errors, "\n".join(
        f"{list(error.absolute_path)}: {error.message}"
        for error in errors
    )


# ------------------------------------------------------------
# 1. Schema validity
# ------------------------------------------------------------

@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_is_valid(name, schemas):
    Draft202012Validator.check_schema(schemas[name])


# ------------------------------------------------------------
# 2. Reference fixture contract compliance
# ------------------------------------------------------------

def test_reference_input_contract(fixtures, schemas):
    assert_valid(fixtures["input"], schemas["input"])


def test_reference_output_contract(fixtures, schemas):
    assert_valid(fixtures["output"], schemas["output"])


def test_reference_events_contract(fixtures, schemas):
    events = fixtures["events"]

    assert isinstance(events, list)
    assert len(events) == 11

    for event in events:
        assert_valid(event, schemas["event"])


# ------------------------------------------------------------
# 3. Reference identity and simulation safety
# ------------------------------------------------------------

def test_reference_identity(fixtures):
    source = fixtures["input"]
    result = fixtures["output"]
    events = fixtures["events"]

    assert source["request_id"] == result["request_id"]
    assert source["session_id"] == result["session_id"]

    assert all(
        event["session_id"] == result["session_id"]
        for event in events
    )

    assert all(
        event["run_id"] == result["run_id"]
        for event in events
    )


def test_simulation_only(fixtures):
    assert fixtures["output"]["simulation_only"] is True

    for event in fixtures["events"]:
        assert event["simulation_only"] is True


# ------------------------------------------------------------
# 4. Event sequence integrity
# ------------------------------------------------------------

def test_event_identifiers_unique(fixtures):
    events = fixtures["events"]
    ids = [event["event_id"] for event in events]

    assert len(ids) == len(set(ids))


def test_event_sequence_unique_and_contiguous(fixtures):
    events = fixtures["events"]
    sequences = [event["sequence"] for event in events]

    assert sequences == list(range(1, len(events) + 1))


def test_event_chronology(fixtures):
    events = fixtures["events"]

    occurred = [
        event["occurred_at"]
        for event in events
    ]

    assert occurred == sorted(occurred)

    for event in events:
        assert event["recorded_at"] >= event["occurred_at"]

        if "available_at" in event:
            assert event["available_at"] <= event["occurred_at"]


# ------------------------------------------------------------
# 5. Order lifecycle
# ------------------------------------------------------------

def test_order_lifecycle(fixtures):
    events = fixtures["events"]

    allowed = {
        None: {"order_created"},
        "order_created": {"order_submitted"},
        "order_submitted": {
            "order_accepted",
            "order_rejected",
        },
        "order_accepted": {
            "order_partially_filled",
            "order_filled",
            "order_canceled",
            "order_expired",
        },
        "order_partially_filled": {
            "order_partially_filled",
            "order_filled",
            "order_canceled",
            "order_expired",
        },
    }

    state = {}

    for event in events:
        event_type = event["event_type"]

        if not event_type.startswith("order_"):
            continue

        order_id = event["order_id"]
        previous = state.get(order_id)

        assert event_type in allowed.get(previous, set()), (
            f"Invalid transition for {order_id}: "
            f"{previous} -> {event_type}"
        )

        state[order_id] = event_type

    assert len(state) == 2
    assert all(value == "order_filled" for value in state.values())


# ------------------------------------------------------------
# 6. Fill quantities and expected orders
# ------------------------------------------------------------

def test_fills_match_orders(fixtures):
    result = fixtures["output"]
    events = fixtures["events"]

    expected = {
        order["order_id"]: D(order["quantity"])
        for order in result["orders"]
    }

    filled = Counter()

    for event in events:
        if event["event_type"] in {
            "order_filled",
            "order_partially_filled",
        }:
            filled[event["order_id"]] += D(
                event["payload"]["quantity"]
            )

    assert set(filled) == set(expected)

    for order_id, quantity in expected.items():
        assert filled[order_id] == quantity


def test_output_fills_match_events(fixtures):
    result = fixtures["output"]
    events = fixtures["events"]

    event_fills = {
        event["payload"]["fill_id"]: event
        for event in events
        if event["event_type"] in {
            "order_filled",
            "order_partially_filled",
        }
    }

    assert len(event_fills) == len(result["fills"])

    for fill in result["fills"]:
        event = event_fills[fill["fill_id"]]

        assert fill["order_id"] == event["order_id"]
        assert D(fill["quantity"]) == D(
            event["payload"]["quantity"]
        )
        assert D(fill["price"]) == D(
            event["payload"]["price"]
        )


# ------------------------------------------------------------
# 7. Portfolio accounting
# ------------------------------------------------------------

def test_initial_cash(fixtures):
    source = fixtures["input"]

    assert D(source["portfolio"]["cash"]) == D("10000.00")


def test_cash_reconciliation(fixtures):
    source = fixtures["input"]
    events = fixtures["events"]
    result = fixtures["output"]

    cash = D(source["portfolio"]["cash"])

    for event in events:
        if event["event_type"] not in {
            "order_filled",
            "order_partially_filled",
        }:
            continue

        payload = event["payload"]

        gross = (
            D(payload["quantity"])
            * D(payload["price"])
        )

        commission = D(payload["commission"])

        if payload["side"] == "buy":
            cash -= gross + commission
        else:
            cash += gross - commission

    assert cash == D("0.00")
    assert cash == D(result["portfolio"]["cash"])


def test_position_reconciliation(fixtures):
    result = fixtures["output"]

    positions = {
        position["instrument_id"]: position
        for position in result["portfolio"]["positions"]
    }

    assert D(positions["ETF-A"]["quantity"]) == D("60")
    assert D(positions["ETF-B"]["quantity"]) == D("80")

    assert D(positions["ETF-A"]["market_value"]) == D("6600")
    assert D(positions["ETF-B"]["market_value"]) == D("4200")


def test_portfolio_nav(fixtures):
    result = fixtures["output"]
    portfolio = result["portfolio"]

    positions_value = sum(
        (
            D(position["market_value"])
            for position in portfolio["positions"]
        ),
        D("0"),
    )

    cash = D(portfolio["cash"])
    nav = positions_value + cash

    assert nav == D("10800.00")
    assert nav == D(portfolio["ending_nav"])


def test_expected_return(fixtures):
    result = fixtures["output"]

    initial = D("10000.00")
    ending = D(result["portfolio"]["ending_nav"])

    calculated_return = (ending / initial) - D("1")

    assert calculated_return == D("0.08")
    assert D(str(result["performance"]["total_return"])) == (
        calculated_return
    )


def test_unrealized_pnl(fixtures):
    result = fixtures["output"]

    unrealized = sum(
        (
            D(position["unrealized_pnl"])
            for position in result["portfolio"]["positions"]
        ),
        D("0"),
    )

    assert unrealized == D("800.00")
    assert unrealized == D(
        result["performance"]["unrealized_pnl"]
    )


def test_final_valuation_event(fixtures):
    result = fixtures["output"]
    events = fixtures["events"]

    valuations = [
        event
        for event in events
        if event["event_type"] == "valuation_recorded"
    ]

    assert len(valuations) >= 1

    final = valuations[-1]["payload"]

    assert D(final["nav"]) == D(
        result["portfolio"]["ending_nav"]
    )
    assert D(final["cash"]) == D(
        result["portfolio"]["cash"]
    )


# ------------------------------------------------------------
# 8. Negative schema tests
# ------------------------------------------------------------

def test_rejects_live_trading_output(fixtures, schemas):
    invalid = dict(fixtures["output"])
    invalid["simulation_only"] = False

    with pytest.raises(ValidationError):
        validator(schemas["output"]).validate(invalid)


def test_rejects_negative_event_sequence(fixtures, schemas):
    invalid = dict(fixtures["events"][0])
    invalid["sequence"] = -1

    with pytest.raises(ValidationError):
        validator(schemas["event"]).validate(invalid)


def test_rejects_invalid_event_type(fixtures, schemas):
    invalid = dict(fixtures["events"][0])
    invalid["event_type"] = "execute_real_trade"

    with pytest.raises(ValidationError):
        validator(schemas["event"]).validate(invalid)


def test_rejects_missing_output_identity(fixtures, schemas):
    invalid = dict(fixtures["output"])
    invalid.pop("run_id")

    with pytest.raises(ValidationError):
        validator(schemas["output"]).validate(invalid)


# ------------------------------------------------------------
# 9. Fixture verification boundaries
# ------------------------------------------------------------

def test_reference_is_not_engine_evidence(fixtures):
    result = fixtures["output"]

    assert result["provenance"]["engine_version"].startswith(
        "reference-expected-"
    )

    assert "PENDING" in result["provenance"]["input_snapshot_hash"]

    assert result["simulation_only"] is True


def test_reference_disclosure(fixtures):
    disclosure = fixtures["output"]["disclosure"].lower()

    assert "hypothetical" in disclosure
    assert "no actual trades" in disclosure


# ------------------------------------------------------------
# 10. Expected reference totals
# ------------------------------------------------------------

def test_reference_event_counts(fixtures):
    counts = Counter(
        event["event_type"]
        for event in fixtures["events"]
    )

    assert counts["order_created"] == 2
    assert counts["order_submitted"] == 2
    assert counts["order_accepted"] == 2
    assert counts["order_filled"] == 2
    assert counts["valuation_recorded"] == 2
    assert counts["checkpoint_created"] == 1


def test_reference_case_identifier(fixtures):
    assert fixtures["input"]["request_id"] == "FT-001"
    assert fixtures["output"]["run_id"] == "RUN-FT-001"
