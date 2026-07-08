"""create vehicle readings table

Revision ID: bc2aff86199d
Revises: 20260703_0001
Create Date: 2026-07-08 09:43:34.463574
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'bc2aff86199d'
down_revision: Union[str, None] = '20260703_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "vehicle_readings",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),

        sa.Column("vehicle_id", sa.Integer(), sa.ForeignKey("vehicles.id"), nullable=True),
        sa.Column("trip_id", sa.Integer(), sa.ForeignKey("trips.id"), nullable=True),
        sa.Column("import_batch_id", sa.Integer(), sa.ForeignKey("import_batches.id"), nullable=True),

        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("source_record_id", sa.String(length=128), nullable=True),

        sa.Column("sheet_row_number", sa.Integer(), nullable=True),
        sa.Column("sheet_title", sa.String(length=255), nullable=True),

        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),

        sa.Column("battery_percent", sa.Float(), nullable=True),
        sa.Column("odometer_km", sa.Float(), nullable=True),
        sa.Column("trip_km", sa.Float(), nullable=True),
        sa.Column("range_km", sa.Float(), nullable=True),

        sa.Column("front_pressure_bar", sa.Float(), nullable=True),
        sa.Column("rear_pressure_bar", sa.Float(), nullable=True),

        sa.Column("energy_used_kwh", sa.Float(), nullable=True),
        sa.Column("distance_km", sa.Float(), nullable=True),

        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),

        sa.Column("raw_ocr_text", sa.Text(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(), nullable=True),

        sa.Column("sync_batch_id", sa.String(length=100), nullable=True),
        sa.Column("sync_status", sa.String(length=30), nullable=False, server_default="synced"),

        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),

        sa.UniqueConstraint("source", "source_record_id", name="uq_vehicle_readings_source_record"),
    )

    op.create_index("ix_vehicle_readings_vehicle_id", "vehicle_readings", ["vehicle_id"])
    op.create_index("ix_vehicle_readings_trip_id", "vehicle_readings", ["trip_id"])
    op.create_index("ix_vehicle_readings_import_batch_id", "vehicle_readings", ["import_batch_id"])
    op.create_index("ix_vehicle_readings_recorded_at", "vehicle_readings", ["recorded_at"])


def downgrade() -> None:
    op.drop_index("ix_vehicle_readings_recorded_at", table_name="vehicle_readings")
    op.drop_index("ix_vehicle_readings_import_batch_id", table_name="vehicle_readings")
    op.drop_index("ix_vehicle_readings_trip_id", table_name="vehicle_readings")
    op.drop_index("ix_vehicle_readings_vehicle_id", table_name="vehicle_readings")

    op.drop_table("vehicle_readings")
