"""
4D-MGRFF Web Platform Backend
FastAPI server providing:
- Interactive portal serving
- PDF Monograph download
- Slide deck JSON API
- Model verification metrics API
"""

import os
import re
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).resolve().parent.parent
THESIS_DIR = ROOT_DIR / "thesis"
RESULTS_DIR = ROOT_DIR / "results"
DOCS_DIR = ROOT_DIR / "docs"
STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(
    title="4D-MGRFF Research Platform",
    description="Four-Dimensional Multidisciplinary Global Risk Forecasting Framework API & Research Portal",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount figures and results
if (RESULTS_DIR / "figures").exists():
    app.mount("/figures", StaticFiles(directory=str(RESULTS_DIR / "figures")), name="figures")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "4D-MGRFF Research Platform",
        "version": "1.0.0",
        "domain": "4dglobalrisk.izhaanintellect.fun"
    }


@app.get("/api/metrics")
def get_metrics():
    """Returns summarized model benchmark metrics for both real FRED and simulation panels."""
    table5a_path = RESULTS_DIR / "tables" / "table_5_real_fred_performance.csv"
    table5b_path = RESULTS_DIR / "tables" / "table_5_forecast_performance.csv"

    def parse_csv(path):
        if not path.exists():
            return []
        import csv
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    return {
        "real_fred_panel": parse_csv(table5a_path),
        "simulation_panel": parse_csv(table5b_path),
        "headline_insights": {
            "best_discrimination_1d": {"model": "M4 Dynamic AR", "bss": "+0.2874", "pr_auc": "0.5849"},
            "best_calibration_1d": {"model": "M7 Full 4D DLM", "ece": "0.0430"},
            "highest_decision_value_14d": {"model": "M7 Full 4D DLM", "value_score": "+0.2969"},
            "dgrs_persistence": {"rho": 0.85, "p_value": "< 0.001"},
            "records_analyzed": 43707,
            "trading_days": 733,
            "rolling_origins": 211
        }
    }


@app.get("/api/slides")
def get_slides():
    """Parses DOCTORAL_DEFENSE_PRESENTATION.md into structured slide objects."""
    slides_path = DOCS_DIR / "DOCTORAL_DEFENSE_PRESENTATION.md"
    if not slides_path.exists():
        raise HTTPException(status_code=404, detail="Slide deck markdown not found")

    with open(slides_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split by horizontal rules
    raw_slides = re.split(r"\n---\n", text)
    structured_slides = []

    for idx, raw in enumerate(raw_slides):
        raw = raw.strip()
        if not raw:
            continue
        
        # Extract title
        title_match = re.search(r"^##?\s+(.*)", raw, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f"Slide {idx + 1}"
        
        structured_slides.append({
            "slide_number": idx + 1,
            "title": title,
            "markdown_content": raw
        })

    return {"total_slides": len(structured_slides), "slides": structured_slides}


@app.get("/download/pdf")
def download_pdf():
    """Direct download for the 2.95 MB compiled dissertation PDF."""
    pdf_path = THESIS_DIR / "DISSERTATION_MONOGRAPH.pdf"
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Compiled PDF monograph not found")
    
    return FileResponse(
        path=str(pdf_path),
        filename="4D-MGRFF_Doctoral_Dissertation_Monograph.pdf",
        media_type="application/pdf"
    )


@app.get("/monograph", response_class=HTMLResponse)
def view_monograph():
    """Serves the standalone HTML monograph."""
    html_path = THESIS_DIR / "DISSERTATION_MONOGRAPH.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="HTML monograph not found")
    
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/", response_class=HTMLResponse)
def index():
    """Serves the main research portal."""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return HTMLResponse("<h1>4D-MGRFF Research Platform</h1><p>Static index not found.</p>")
    
    with open(index_file, "r", encoding="utf-8") as f:
        return f.read()
