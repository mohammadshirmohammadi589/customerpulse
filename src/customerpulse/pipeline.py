"""End-to-end orchestration pipeline for CustomerPulse."""

from pathlib import Path
from pathlib import Path
import duckdb

from customerpulse.analytics.customer_metrics import (
    build_customer_metrics,
)
from customerpulse.analytics.historical_value import (
    build_historical_customer_value,
)
from customerpulse.analytics.rfm import (
    build_rfm,
)
from customerpulse.analytics.rfm_scoring import (
    build_rfm_scoring,
)
from customerpulse.analytics.retention import (
    build_retention_matrix,
)
from customerpulse.analytics.segmentation import (
    build_customer_segments,
)
from customerpulse.config.loader import load_config
from customerpulse.database.connection import get_connection
from customerpulse.decision.pipeline import (
    build_decision_layer,
)
from customerpulse.ingestion.pipeline import (
    ingest_from_config,
)
from customerpulse.standardization.identifiers import (
    normalize_customer_id,
)
from customerpulse.standardization.qualification import (
    qualify_transactions,
)
from customerpulse.standardization.schema import (
    validate_standardized_schema,
)
from customerpulse.standardization.transactions import (
    aggregate_to_transaction_level,
)
from customerpulse.validation.gate import (
    has_blocking_errors,
)
from customerpulse.validation.runner import (
    validate_data,
)


def _execute_sql_file(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path,
) -> None:
    """Execute a SQL file against the active DuckDB connection."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)

def _project_root() -> Path:
    """Return the CustomerPulse project root."""
    return Path(__file__).resolve().parents[2]


def run_pipeline(
    config_path: str | Path = "configs/default.yaml",
) -> duckdb.DuckDBPyConnection:
    """
    Run the complete CustomerPulse analytical pipeline.

    Pipeline stages:

    1. Configuration
    2. Ingestion
    3. Transaction qualification
    4. Identifier normalization
    5. Post-qualification validation
    6. Transaction-level standardization
    7. DuckDB staging
    8. Analytical layer
    9. Decision layer
    """

    # ------------------------------------------------------------------
    # 1. Configuration
    # ------------------------------------------------------------------

    config = load_config(
        config_path
    )

    # ------------------------------------------------------------------
    # 2. Ingestion
    # ------------------------------------------------------------------

    ingestion_result = ingest_from_config(
        config,
        config_path=str(config_path),
    )

    # ------------------------------------------------------------------
    # 3. Qualification
    #
    # Raw source data may contain invalid rows.
    # These rows are intentionally filtered before the blocking
    # validation gate.
    # ------------------------------------------------------------------

    prefixes = tuple(
        config.get(
            "qualification",
            {},
        ).get(
            "exclude_transaction_id_prefixes",
            [],
        )
    )

    qualified = qualify_transactions(
        ingestion_result.data,
        exclude_transaction_id_prefixes=prefixes,
    )

    # ------------------------------------------------------------------
    # 4. Identifier normalization
    # ------------------------------------------------------------------

    qualified["customer_id"] = normalize_customer_id(
        qualified["customer_id"]
    )

    # ------------------------------------------------------------------
    # 5. Post-qualification validation
    #
    # Validation is performed after row-level qualification.
    # This prevents expected invalid source rows, such as missing
    # CustomerID rows, from blocking otherwise usable data.
    # ------------------------------------------------------------------

    validation_issues = validate_data(
        qualified
    )

    if has_blocking_errors(
        validation_issues
    ):
        raise ValueError(
            "Pipeline blocked because critical data-quality errors "
            "remain after transaction qualification."
        )

    # ------------------------------------------------------------------
    # 6. Transaction-level standardization
    # ------------------------------------------------------------------

    standardized = aggregate_to_transaction_level(
        qualified
    )

    schema_issues = validate_standardized_schema(
        standardized
    )

    if schema_issues:
        raise ValueError(
            "Standardized schema validation failed: "
            f"{schema_issues}"
        )

    # ------------------------------------------------------------------
    # 7. Database
    # ------------------------------------------------------------------

    database_path = config.get(
        "database",
        {},
    ).get(
        "path",
        "data/processed/customerpulse.duckdb",
    )

    connection = get_connection(
        database_path
    )

    # ------------------------------------------------------------------
    # 8. Staging
    # ------------------------------------------------------------------

    from customerpulse.database.staging import (
        load_standardized_transactions,
    )

    load_standardized_transactions(
        connection,
        standardized,
    )

    # ------------------------------------------------------------------
    # 9. Analytical layer
    # ------------------------------------------------------------------

    build_customer_metrics(
        connection
    )

    build_rfm(
        connection
    )

    build_rfm_scoring(
        connection
    )

    # ------------------------------------------------------------------
    # Cohort and retention
    # ------------------------------------------------------------------

    _execute_sql_file(
        connection,
        "sql/analytics/cohort.sql",
    )

    _execute_sql_file(
        connection,
        "sql/analytics/cohort_activity.sql",
    )

    _execute_sql_file(
        connection,
        "sql/analytics/cohort_periods.sql",
    )

    project_root = _project_root()

    _execute_sql_file(
        connection,
        project_root / "sql/analytics/cohort_retention.sql",
    )

    build_retention_matrix(
        connection
    )

    # ------------------------------------------------------------------
    # Historical customer value
    # ------------------------------------------------------------------

    build_historical_customer_value(
        connection
    )

    # ------------------------------------------------------------------
    # Customer segmentation
    # ------------------------------------------------------------------

    build_customer_segments(
        connection
    )

    # ------------------------------------------------------------------
    # 10. Decision layer
    # ------------------------------------------------------------------

    build_decision_layer(
        connection
    )

    return connection
