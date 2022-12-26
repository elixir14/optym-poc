import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, TIMESTAMP, func, BigInteger
from sqlalchemy_utils import UUIDType

from db.base import Base


class Loads(Base):
    __tablename__ = "loads"
    load_data_id = Column(BigInteger, primary_key=True, autoincrement=True)
    load_id = Column(String(255), nullable=False)
    load_creation_date_time = Column(String(255), nullable=False)
    business_unit = Column(String(255), nullable=False, default="ASSET")
    load_reference_number = Column(String(255), nullable=True)
    customer_id = Column(String(255), nullable=False)
    fuel_surcharge = Column(String(255), nullable=True)
    additional_charge = Column(String(255), nullable=True)
    number_of_stops = Column(String(255), nullable=False)
    total_loaded_miles = Column(String(255), nullable=False)
    last_segment_miles = Column(String(255), nullable=True)
    pickup_appointment_start_date_time = Column(String(255), nullable=False)
    pickup_appointment_end_date_time = Column(String(255), nullable=True)
    delivery_appointment_start_date_time = Column(String(255), nullable=False)
    delivery_appointment_end_date_time = Column(String(255), nullable=True)
    required_equipment = Column(String(255), nullable=False)
    hazmat = Column(String(255), nullable=False)
    commodity_type = Column(String(255), nullable=True, default="FAK")
    load_max_weight = Column(String(255), nullable=True)
    critical = Column(String(255), nullable=False)
    load_status = Column(String(255), nullable=False, default="AVAILABLE")
    pickup_status = Column(String(255), nullable=False)
    delivery_status = Column(String(255), nullable=False)
    pickup_arrival_actual_date_time = Column(String(255), nullable=True)
    delivery_arrival_actual_date_time = Column(String(255), nullable=True)
    created_at: datetime = Column(TIMESTAMP(timezone=True), server_default=func.now())
    scenario_id = Column(String(255), nullable=False)
    load_total_revenue = Column(String(255), nullable=True)
    linehaul_revenue = Column(String(255), nullable=True)
    pickup_location_id = Column(String(255), nullable=False)
    delivery_location_id = Column(String(255), nullable=False)
    active = Column(Boolean, nullable=True, default=True)
    associated_trip_ids = Column(String(255), nullable=True)
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    pickup_departure_actual_date_time = Column(String(255), nullable=True)
    delivery_departure_actual_date_time = Column(String(255), nullable=True)
    run_data_id = Column(String(255), nullable=False)
    timeoff = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)
    assigned_driver_id = Column(String(255), nullable=True)
    load_weight_on_last_segment = Column(String(255), nullable=True)
    pickup_arrival_eta = Column(String(255), nullable=True)
    pickup_departure_etd = Column(String(255), nullable=True)
    delivery_arrival_eta = Column(String(255), nullable=True)
    delivery_departure_etd = Column(String(255), nullable=True)
    trip_sequence = Column(String(255), nullable=True)
