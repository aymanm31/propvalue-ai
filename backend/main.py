from fastapi import FastAPI
from pydantic import BaseModel
from services.roi_engine import ROIInput, calculate_roi
from services.market_data import get_market_data_by_zip, estimate_arv
from services.vision_analyzer import analyze_image_from_base64, analyze_multiple_images
from services.cost_estimator import estimate_total_rehab_cost
from services.property_analyzer import run_full_analysis
from fastapi.middleware.cors import CORSMiddleware
from services.comp_engine import get_comp_analysis
from fastapi.responses import Response
from services.report_generator import generate_roi_report
from fastapi import HTTPException
import base64

app = FastAPI(title="PropValue AI", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

MAX_IMAGE_SIZE_MB = 4
MAX_IMAGES = 10

@app.post("/api/analyze/full")
def full_analysis(request: FullAnalysisRequest):
    if not request.images:
        raise HTTPException(status_code=400, detail="At least one image is required")

    if len(request.images) > MAX_IMAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {MAX_IMAGES} images allowed per analysis"
        )

    for i, img in enumerate(request.images):
        try:
            decoded = base64.b64decode(img["base64"])
            size_mb = len(decoded) / (1024 * 1024)
            if size_mb > MAX_IMAGE_SIZE_MB:
                raise HTTPException(
                    status_code=400,
                    detail=f"Image {i+1} is {size_mb:.1f}MB. Maximum size is {MAX_IMAGE_SIZE_MB}MB per image."
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise HTTPException(status_code=400, detail=f"Image {i+1} could not be decoded")

    if not request.zip_code or len(request.zip_code) != 5 or not request.zip_code.isdigit():
        raise HTTPException(status_code=400, detail="ZIP code must be exactly 5 digits")

    if request.square_footage <= 0 or request.square_footage > 50000:
        raise HTTPException(status_code=400, detail="Square footage must be between 1 and 50,000")

    if request.purchase_price <= 0:
        raise HTTPException(status_code=400, detail="Purchase price must be greater than 0")

    if request.rehab_duration_months < 1 or request.rehab_duration_months > 60:
        raise HTTPException(status_code=400, detail="Rehab duration must be between 1 and 60 months")

    return run_full_analysis(
        images=request.images,
        zip_code=request.zip_code,
        square_footage=request.square_footage,
        purchase_price=request.purchase_price,
        monthly_taxes=request.monthly_taxes,
        monthly_insurance=request.monthly_insurance,
        rehab_duration_months=request.rehab_duration_months
    )

class CompRequest(BaseModel):
    zip_code: str
    square_footage: float

@app.post("/api/market/comps")
def comp_analysis(request: CompRequest):
    return get_comp_analysis(request.zip_code, request.square_footage)

@app.post("/api/report/generate")
def generate_report(analysis: dict):
    pdf_bytes = generate_roi_report(analysis)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=propvalue-report.pdf"}
    )