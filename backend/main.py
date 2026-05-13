from fastapi import FastAPI
from pydantic import BaseModel
from services.roi_engine import ROIInput, calculate_roi

app = FastAPI(title="PropValue AI", version="0.1.0")

class ROIRequest(BaseModel):
    purchase_price: float
    rehab_cost: float
    arv: float
    monthly_taxes: float
    monthly_insurance: float
    rehab_duration_months: int

@app.get("/")
def root():
    return {"status": "PropValue AI backend is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/roi/calculate")
def roi_calculate(request: ROIRequest):
    input = ROIInput(
        purchase_price=request.purchase_price,
        rehab_cost=request.rehab_cost,
        arv=request.arv,
        monthly_taxes=request.monthly_taxes,
        monthly_insurance=request.monthly_insurance,
        rehab_duration_months=request.rehab_duration_months
    )
    result = calculate_roi(input)
    return result.breakdown