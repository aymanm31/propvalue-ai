from fastapi import FastAPI
from pydantic import BaseModel
from services.roi_engine import ROIInput, calculate_roi
from services.market_data import get_market_data_by_zip, estimate_arv
from services.vision_analyzer import analyze_image_from_base64, analyze_multiple_images
from services.cost_estimator import estimate_total_rehab_cost
from services.property_analyzer import run_full_analysis

app = FastAPI(title="PropValue AI", version="0.1.0")

class ROIRequest(BaseModel):
    purchase_price: float
    rehab_cost: float
    arv: float
    monthly_taxes: float
    monthly_insurance: float
    rehab_duration_months: int

class ARVRequest(BaseModel):
    zip_code: str
    square_footage: float

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

@app.get("/api/market/{zip_code}")
def market_data(zip_code: str):
    return get_market_data_by_zip(zip_code)

@app.post("/api/market/estimate-arv")
def arv_estimate(request: ARVRequest):
    return estimate_arv(request.zip_code, request.square_footage)

class ImageAnalysisRequest(BaseModel):
    images: list[dict]

@app.post("/api/analyze/photos")
def analyze_photos(request: ImageAnalysisRequest):
    return analyze_multiple_images(request.images)

class CostEstimateRequest(BaseModel):
    room_analyses: list[dict]

@app.post("/api/estimate/rehab-cost")
def rehab_cost_estimate(request: CostEstimateRequest):
    return estimate_total_rehab_cost(request.room_analyses)

class FullAnalysisRequest(BaseModel):
    images: list[dict]
    zip_code: str
    square_footage: float
    purchase_price: float
    monthly_taxes: float
    monthly_insurance: float
    rehab_duration_months: int

@app.post("/api/analyze/full")
def full_analysis(request: FullAnalysisRequest):
    return run_full_analysis(
        images=request.images,
        zip_code=request.zip_code,
        square_footage=request.square_footage,
        purchase_price=request.purchase_price,
        monthly_taxes=request.monthly_taxes,
        monthly_insurance=request.monthly_insurance,
        rehab_duration_months=request.rehab_duration_months
    )