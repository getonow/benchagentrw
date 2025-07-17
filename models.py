from sqlalchemy import Column, String, Float, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class MasterFile(Base):
    __tablename__ = "MASTER_FILE"
    
    # Primary identification
    suppliernumber = Column(String(50), primary_key=True)
    partnumber = Column(String(50), primary_key=True)
    
    # Supplier information
    suppliername = Column(String(255))
    suppliercontactname = Column(String(255))
    suppliercontactemail = Column(String(255))
    suppliermanufacturinglocation = Column(String(255))
    
    # Part information
    partname = Column(String(255))
    material = Column(String(255))
    material2 = Column(String(255))
    currency = Column(String(10))
    
    # Volume data (2023-2025)
    voljan2023 = Column(Float)
    volfeb2023 = Column(Float)
    volmar2023 = Column(Float)
    volapr2023 = Column(Float)
    volmay2023 = Column(Float)
    voljun2023 = Column(Float)
    voljul2023 = Column(Float)
    volaug2023 = Column(Float)
    volsep2023 = Column(Float)
    voloct2023 = Column(Float)
    volnov2023 = Column(Float)
    voldec2023 = Column(Float)
    
    voljan2024 = Column(Float)
    volfeb2024 = Column(Float)
    volmar2024 = Column(Float)
    volapr2024 = Column(Float)
    volmay2024 = Column(Float)
    voljun2024 = Column(Float)
    voljul2024 = Column(Float)
    volaug2024 = Column(Float)
    volsep2024 = Column(Float)
    voloct2024 = Column(Float)
    volnov2024 = Column(Float)
    voldec2024 = Column(Float)
    
    voljan2025 = Column(Float)
    volfeb2025 = Column(Float)
    volmar2025 = Column(Float)
    volapr2025 = Column(Float)
    volmay2025 = Column(Float)
    voljun2025 = Column(Float)
    voljul2025 = Column(Float)
    volaug2025 = Column(Float)
    volsep2025 = Column(Float)
    voloct2025 = Column(Float)
    volnov2025 = Column(Float)
    voldec2025 = Column(Float)
    
    # Price data (2025)
    pricejan2025 = Column(Float)
    pricefeb2025 = Column(Float)
    pricemar2025 = Column(Float)
    priceapr2025 = Column(Float)
    pricemay2025 = Column(Float)
    pricejun2025 = Column(Float)
    pricejul2025 = Column(Float)
    priceaug2025 = Column(Float)
    pricesep2025 = Column(Float)
    priceoct2025 = Column(Float)
    pricenov2025 = Column(Float)
    pricedec2025 = Column(Float)

class PartsBenchmarks(Base):
    __tablename__ = "PARTS_BENCHMARKS"
    
    partnumber = Column(String(50), primary_key=True)
    currentsuppliernumber = Column(String(50))
    currentsuppliername = Column(String(255))
    partname = Column(String(255))
    currency = Column(String(10))
    
    # Benchmark supplier prices (example columns - adjust based on actual schema)
    SUP999 = Column(Float)
    SUP001 = Column(Float)
    SUP017 = Column(Float)
    SUP012 = Column(Float)
    # Add more supplier columns as needed

class SupplierPanelCatalog(Base):
    __tablename__ = "SUPPLIER_PANEL_CATALOG"
    
    suppliernumber = Column(String(50), primary_key=True)
    suppliername = Column(String(255))
    suppliercontactname = Column(String(255))
    suppliercontactemail = Column(String(255))
    suppliermanufacturinglocation = Column(String(255))
    website = Column(String(255))
    description = Column(Text) 