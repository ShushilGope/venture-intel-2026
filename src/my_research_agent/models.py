from pydantic import BaseModel, Field
from typing import List, Dict

class RiskMitigation(BaseModel):
    risk_factor: str
    impact: str # Low/Medium/High
    mitigation_strategy: str

class MarketSizing(BaseModel):
    tam: str = Field(description="Total Addressable Market (Global)")
    sam: str = Field(description="Serviceable Addressable Market (Segment)")
    som: str = Field(description="Serviceable Obtainable Market (Target Year 1)")

class VCReadyOutput(BaseModel):
    product_concept: str
    market_sizing: MarketSizing
    top_competitors: List[Dict[str, str]]
    strategic_risks: List[RiskMitigation]
    investment_thesis: str = Field(description="The 'Why Now' argument for an investor")
    market_white_space: str