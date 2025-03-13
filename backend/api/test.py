from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["File Conversion"])

@router.get("test")
def test():
  return "test"