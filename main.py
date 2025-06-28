from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import tempfile
import os
from datetime import datetime

# Import our modules
from utils.config import config
from modules.object_detection import detector
from modules.pdf_parser import parser
from modules.violation_checker import checker
from modules.report_generator import generator
from utils.helpers import validate_image_file, validate_pdf_file, generate_unique_filename

# Initialize FastAPI app
app = FastAPI(
    title="Violation Detection API",
    description="AI-powered violation detection and reporting system for Residence Life",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ViolationRequest(BaseModel):
    staff_name: Optional[str] = ""
    room_number: Optional[str] = ""
    building_name: Optional[str] = ""
    user_notes: Optional[str] = ""
    confidence_threshold: Optional[float] = 0.3

class ViolationResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ReportRequest(BaseModel):
    image_path: str
    detected_objects: List[Dict[str, Any]]
    violation_assessment: Dict[str, Any]
    policy_rules: List[Dict[str, Any]]
    staff_name: Optional[str] = ""
    room_number: Optional[str] = ""
    building_name: Optional[str] = ""
    user_notes: Optional[str] = ""

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    try:
        config.validate()
        print("✅ Configuration validated successfully")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Violation Detection API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze": "/analyze",
            "generate_report": "/generate_report",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Basic health checks
        config.validate()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "config": "ok",
                "object_detection": "ok",
                "pdf_parser": "ok",
                "violation_checker": "ok"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/analyze", response_model=ViolationResponse)
async def analyze_violation(
    image: UploadFile = File(...),
    policy_pdf: UploadFile = File(...),
    staff_name: str = Form(""),
    room_number: str = Form(""),
    building_name: str = Form(""),
    user_notes: str = Form(""),
    confidence_threshold: float = Form(0.3)
):
    """
    Analyze an image for policy violations using uploaded policy document.
    
    Args:
        image: Image file to analyze
        policy_pdf: Policy PDF document
        staff_name: Name of the reporting staff member
        room_number: Room number where violation occurred
        building_name: Building name
        user_notes: Additional notes from staff
        confidence_threshold: Minimum confidence for object detection
    
    Returns:
        Analysis results including detected objects and violation assessment
    """
    try:
        # Validate uploaded files
        if not image.filename or not policy_pdf.filename:
            raise HTTPException(status_code=400, detail="Both image and PDF files are required")
        
        # Save uploaded files
        image_path = None
        pdf_path = None
        
        try:
            # Save image
            if not validate_image_file(image.filename):
                raise HTTPException(status_code=400, detail="Invalid image file format")
            
            image_filename = generate_unique_filename(image.filename, "img_")
            image_path = config.get_upload_path(image_filename)
            
            with open(image_path, "wb") as f:
                f.write(image.file.read())
            
            # Save PDF
            if not validate_pdf_file(policy_pdf.filename):
                raise HTTPException(status_code=400, detail="Invalid PDF file format")
            
            pdf_filename = generate_unique_filename(policy_pdf.filename, "pdf_")
            pdf_path = config.get_upload_path(pdf_filename)
            
            with open(pdf_path, "wb") as f:
                f.write(policy_pdf.file.read())
                
        except Exception as e:
            # Cleanup on error
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise HTTPException(status_code=500, detail=f"Error saving uploaded files: {str(e)}")
        
        # Perform analysis
        try:
            # Detect objects with custom confidence threshold
            detected_objects = detector.detect_objects(image_path, confidence_threshold)
            
            # Extract and index policy rules
            policy_summary = parser.get_policy_summary(pdf_path)
            parser.index_policy_rules(pdf_path, "uploaded_policy")
            
            # Search for relevant rules
            relevant_rules = []
            if detected_objects:
                for obj in detected_objects:
                    query = f"{obj['object']} {obj['category']}"
                    rules = parser.search_relevant_rules(query, n_results=2)
                    relevant_rules.extend(rules)
            
            # Remove duplicates
            unique_rules = []
            seen_texts = set()
            for rule in relevant_rules:
                if rule["rule_text"] not in seen_texts:
                    seen_texts.add(rule["rule_text"])
                    unique_rules.append(rule)
            
            # Assess violations
            image_context = detector.analyze_image_context(image_path)
            violation_assessment = checker.assess_violation(detected_objects, unique_rules, image_context)
            
            # Prepare response data
            analysis_results = {
                "image_analysis": {
                    "detected_objects": detected_objects,
                    "detection_summary": detector.get_detection_summary(detected_objects),
                    "image_context": image_context
                },
                "policy_analysis": {
                    "policy_summary": policy_summary,
                    "relevant_rules": unique_rules
                },
                "violation_assessment": violation_assessment,
                "compliance_status": "compliant" if not violation_assessment.get("violation_found", False) else "non_compliant",
                "metadata": {
                    "staff_name": staff_name,
                    "room_number": room_number,
                    "building_name": building_name,
                    "user_notes": user_notes,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "image_filename": image_filename,
                    "pdf_filename": pdf_filename
                }
            }
            
            return ViolationResponse(
                success=True,
                message="Analysis completed successfully",
                data=analysis_results
            )
            
        except Exception as e:
            # Cleanup on analysis error
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/generate_report", response_model=ViolationResponse)
async def generate_incident_report(request: ReportRequest):
    """
    Generate an incident report PDF based on analysis results.
    
    Args:
        request: ReportRequest containing all necessary data
    
    Returns:
        Path to the generated PDF report
    """
    try:
        # Validate that image path exists
        if not os.path.exists(request.image_path):
            raise HTTPException(status_code=400, detail="Image file not found")
        
        # Generate report
        report_path = generator.generate_incident_report(
            image_path=request.image_path,
            detected_objects=request.detected_objects,
            violation_assessment=request.violation_assessment,
            policy_rules=request.policy_rules,
            user_notes=request.user_notes,
            staff_name=request.staff_name,
            room_number=request.room_number,
            building_name=request.building_name
        )
        
        return ViolationResponse(
            success=True,
            message="Report generated successfully",
            data={
                "report_path": report_path,
                "report_filename": os.path.basename(report_path),
                "generated_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@app.get("/download_report/{filename}")
async def download_report(filename: str):
    """
    Download a generated incident report.
    
    Args:
        filename: Name of the report file to download
    
    Returns:
        PDF file for download
    """
    try:
        report_path = config.get_report_path(filename)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Report file not found")
        
        return FileResponse(
            path=report_path,
            filename=filename,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading report: {str(e)}")

@app.get("/reports")
async def list_reports():
    """List all generated reports."""
    try:
        reports_dir = config.REPORTS_DIR
        if not os.path.exists(reports_dir):
            return {"reports": []}
        
        reports = []
        for filename in os.listdir(reports_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(reports_dir, filename)
                file_stat = os.stat(file_path)
                
                reports.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    "modified_at": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
        
        # Sort by creation date (newest first)
        reports.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {"reports": reports}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing reports: {str(e)}")

@app.delete("/reports/{filename}")
async def delete_report(filename: str):
    """
    Delete a generated report.
    
    Args:
        filename: Name of the report file to delete
    """
    try:
        report_path = config.get_report_path(filename)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="Report file not found")
        
        os.remove(report_path)
        
        return {"message": f"Report {filename} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")

@app.post("/clear_database")
async def clear_policy_database():
    """Clear all indexed policy rules from the database."""
    try:
        parser.clear_database()
        return {"message": "Policy database cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing database: {str(e)}")

@app.get("/stats")
async def get_system_stats():
    """Get system statistics."""
    try:
        # Count files in uploads and reports directories
        uploads_count = len([f for f in os.listdir(config.UPLOAD_DIR) if os.path.isfile(os.path.join(config.UPLOAD_DIR, f))])
        reports_count = len([f for f in os.listdir(config.REPORTS_DIR) if os.path.isfile(os.path.join(config.REPORTS_DIR, f))])
        
        return {
            "uploaded_files": uploads_count,
            "generated_reports": reports_count,
            "system_status": "operational",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    ) 