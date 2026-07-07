"""Initial Phase 5 MVP schema.

Revision ID: 20260703_0001
Revises:
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260703_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(100), nullable=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("license_plate", sa.String(50), nullable=False),
        sa.Column("battery_capacity_kwh", sa.Float(), nullable=False),
        sa.Column("minimum_soc_percent", sa.Float(), nullable=False, server_default="20"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *timestamps(),
        sa.UniqueConstraint("external_id"),
        sa.UniqueConstraint("license_plate"),
    )
    op.create_index("ix_vehicles_external_id", "vehicles", ["external_id"])
    op.create_index("ix_vehicles_license_plate", "vehicles", ["license_plate"])

    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(100), nullable=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("license_number", sa.String(100), nullable=True),
        *timestamps(),
        sa.UniqueConstraint("external_id"),
        sa.UniqueConstraint("license_number"),
    )
    op.create_index("ix_drivers_external_id", "drivers", ["external_id"])

    op.create_table(
        "charging_stations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("external_id", sa.String(100), nullable=True),
        sa.Column("name", sa.String(150), nullable=False),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("max_power_kw", sa.Float(), nullable=True),
        *timestamps(),
        sa.UniqueConstraint("external_id"),
    )
    op.create_index("ix_charging_stations_external_id", "charging_stations", ["external_id"])

    op.create_table(
        "import_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("sheet_id", sa.String(255), nullable=True),
        sa.Column("sheet_range", sa.String(255), nullable=True),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("imported_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("skipped_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "trips",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vehicle_id", sa.Integer(), sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column("driver_id", sa.Integer(), sa.ForeignKey("drivers.id"), nullable=True),
        sa.Column("external_id", sa.String(100), nullable=True),
        sa.Column("origin", sa.String(255), nullable=False),
        sa.Column("destination", sa.String(255), nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="planned"),
        sa.Column("planned_distance_km", sa.Float(), nullable=False),
        sa.Column("actual_distance_km", sa.Float(), nullable=True),
        sa.Column("planned_energy_kwh", sa.Float(), nullable=False),
        sa.Column("actual_energy_kwh", sa.Float(), nullable=True),
        sa.Column("starting_soc_percent", sa.Float(), nullable=True),
        sa.Column("ending_soc_percent", sa.Float(), nullable=True),
        sa.Column("scheduled_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("actual_end", sa.DateTime(timezone=True), nullable=True),
        *timestamps(),
        sa.UniqueConstraint("external_id"),
    )
    op.create_index("ix_trips_vehicle_id", "trips", ["vehicle_id"])
    op.create_index("ix_trips_driver_id", "trips", ["driver_id"])
    op.create_index("ix_trips_external_id", "trips", ["external_id"])

    op.create_table(
        "vehicle_readings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vehicle_id", sa.Integer(), sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column("trip_id", sa.Integer(), sa.ForeignKey("trips.id"), nullable=True),
        sa.Column("import_batch_id", sa.Integer(), sa.ForeignKey("import_batches.id"), nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("source_record_id", sa.String(128), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("soc_percent", sa.Float(), nullable=True),
        sa.Column("energy_used_kwh", sa.Float(), nullable=True),
        sa.Column("distance_km", sa.Float(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.UniqueConstraint("source", "source_record_id", name="uq_reading_source_record"),
    )
    op.create_index("ix_vehicle_readings_vehicle_id", "vehicle_readings", ["vehicle_id"])
    op.create_index("ix_vehicle_readings_trip_id", "vehicle_readings", ["trip_id"])
    op.create_index("ix_vehicle_readings_import_batch_id", "vehicle_readings", ["import_batch_id"])
    op.create_index("ix_vehicle_readings_recorded_at", "vehicle_readings", ["recorded_at"])

    op.create_table(
        "optimization_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trip_id", sa.Integer(), sa.ForeignKey("trips.id"), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("energy_variance_threshold_percent", sa.Float(), nullable=False, server_default="10"),
        sa.Column("distance_variance_threshold_percent", sa.Float(), nullable=False, server_default="10"),
        sa.Column("minimum_soc_percent", sa.Float(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_optimization_jobs_trip_id", "optimization_jobs", ["trip_id"])

    op.create_table(
        "optimization_recommendations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("optimization_jobs.id"), nullable=False),
        sa.Column("rule_code", sa.String(80), nullable=False),
        sa.Column("severity", sa.String(20), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("observed_value", sa.Float(), nullable=True),
        sa.Column("threshold_value", sa.Float(), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_optimization_recommendations_job_id", "optimization_recommendations", ["job_id"])


def downgrade() -> None:
    op.drop_table("optimization_recommendations")
    op.drop_table("optimization_jobs")
    op.drop_table("vehicle_readings")
    op.drop_table("trips")
    op.drop_table("import_batches")
    op.drop_table("charging_stations")
    op.drop_table("drivers")
    op.drop_table("vehicles")
