from fastapi import APIRouter, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from io import BytesIO
from utils import convert_png_to_pdf, convert_pdf_to_png_streaming
from enums.type_enum import ConvertType

router = APIRouter(prefix="/convert", tags=["File Conversion"])

# 클라이언트별 진행률 저장
# progress_data = {}
@router.post("")
async def convert(
    file: UploadFile = File(...),
    convert_type: ConvertType = Query(...),
    client_id: str = Query(...)
):
    """파일을 변환하고 진행률을 WebSocket을 통해 전송"""
    if not file:
        return {"error": "No files uploaded."}

    # progress_data[client_id] = 0  # 진행률 초기화

    
    match convert_type:
        case ConvertType.PNG_TO_PDF:
            return await convert_png_to_pdf(file)
        case ConvertType.PDF_TO_PNG:
            return await convert_pdf_to_png_streaming(file)
        case _:
            return {"error": "Invalid conversion type."}

    # progress_data[client_id] = 100  # 변환 완료
    
    return "NONE"
