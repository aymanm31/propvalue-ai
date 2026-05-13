from sqlalchemy import Column, String, Float, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    square_footage = Column(Float, nullable=True)
    year_built = Column(Integer, nullable=True)
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Float, nullable=True)
    asking_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = Column(String, nullable=False)
    arv = Column(Float, nullable=True)
    estimated_rehab_cost = Column(Float, nullable=True)
    estimated_holding_cost = Column(Float, nullable=True)
    roi_percentage = Column(Float, nullable=True)
    seventy_percent_rule_max = Column(Float, nullable=True)
    is_good_deal = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CostEstimate(Base):
    __tablename__ = "cost_estimates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, nullable=False)
    category = Column(String, nullable=False)
    item = Column(String, nullable=False)
    low_estimate = Column(Float, nullable=False)
    high_estimate = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Comp(Base):
    __tablename__ = "comps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    property_id = Column(String, nullable=False)
    address = Column(String, nullable=True)
    zip_code = Column(String, nullable=False)
    sale_price = Column(Float, nullable=False)
    square_footage = Column(Float, nullable=True)
    price_per_sqft = Column(Float, nullable=True)
    sale_date = Column(String, nullable=True)
    source = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)