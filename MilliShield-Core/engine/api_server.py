from fastapi import FastAPI
from pydantic import BaseModel
from engine.ai_core_engine import DynamicHeuristicEngine

app = FastAPI(title="MilliShield Core Security API")
engine = DynamicHeuristicEngine()

class DomainCheckRequest(BaseModel):
    domain: str

@app.post("/analyze")
def analyze_domain(req: DomainCheckRequest):
    return engine.analyze_domain(req.domain)

@app.get("/health")
def health_check():
    return {"status": "ACTIVE", "system": "MilliShield Core Engine"}

@app.post("/inspect")
async def inspect_domain(payload: InspectionRequest):
    """Domain/Adres bazlı sezgisel AI analizi."""
    if not payload.domain:
        raise HTTPException(status_code=400, detail="Domain boş olamaz.")

    result = ai_engine.analyze_domain(payload.domain)
    return {
        "domain": payload.domain,
        "action": result["action"],
        "reason": result["reason"],
        "entropy": result["entropy"],
        "latency_ms": result["latency_ms"]
    }

@app.post("/sanitize")
async def sanitize_requests(payload: SanitizeRequest):
    """Sayfa içi arka plan sömürgeci script/tracker temizleme."""
    if not payload.urls:
        raise HTTPException(status_code=400, detail="URL listesi boş olamaz.")

    result = sanitizer.sanitize_page_requests(payload.urls)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")