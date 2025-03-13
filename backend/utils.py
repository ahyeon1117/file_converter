import img2pdf
import zipfile
import pdf2image
from io import BytesIO
from urllib.parse import quote
from fastapi import UploadFile
from fastapi.responses import StreamingResponse

path = "C:\\poppler-24.08.0\\Library\\bin"

from urllib.parse import quote
from fastapi.responses import StreamingResponse

async def convert_png_to_pdf(file: UploadFile) -> StreamingResponse:
    """하나의 PNG 이미지를 PDF로 변환하는 함수"""
    pdf_bytes = BytesIO()
    image = await file.read()  # PNG 파일 읽기
    pdf_bytes.write(img2pdf.convert(image))
    pdf_bytes.seek(0)

    # 원본 파일명(한글 포함)을 그대로 사용 (URL 인코딩)
    original_filename = file.filename
    encoded_filename = quote(original_filename)  # UTF-8 URL 인코딩

    return StreamingResponse(
        pdf_bytes,
        media_type="application/pdf",
        headers={
            # filename* 에 UTF-8 인코딩된 파일명을 그대로 넣습니다.
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}.pdf",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

async def convert_pdf_to_png_streaming(file: UploadFile) -> StreamingResponse:
    pdf_bytes = await file.read()
    images = convert_pdf_to_images(pdf_bytes)
    base_filename = file.filename.rsplit(".", 1)[0] if file.filename else "converted_file"
    
    if len(images) == 1:
        # 페이지가 하나면 단일 PNG 반환
        return create_png_response(images[0], base_filename)
    else:
        # 페이지가 여러 개면 ZIP 파일로 묶어서 반환
        zip_buffer = create_zip_from_images(images, base_filename)
        return create_zip_response(zip_buffer, base_filename)
      

def convert_pdf_to_images(pdf_bytes: bytes) -> list:
    try:
        images = pdf2image.convert_from_bytes(pdf_bytes, poppler_path=path)
        return images
    except Exception as e:
        print(f"🚨 PDF 변환 오류 발생: {e}")
        raise
      
def create_zip_from_images(images: list, base_filename: str) -> BytesIO:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for i, img in enumerate(images):
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            file_name = f"{base_filename}_page_{i+1}.png"
            zip_file.writestr(file_name, img_bytes.getvalue())
            print(f"📄 {file_name} 추가 완료")
    zip_buffer.seek(0)
    return zip_buffer


def create_png_response(image, filename: str) -> StreamingResponse:

    img_bytes = BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    encoded_filename = quote(filename)
    return StreamingResponse(
        img_bytes,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}.png",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

def create_zip_response(zip_buffer: BytesIO, filename: str) -> StreamingResponse:

    encoded_filename = quote(filename)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}.zip",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )