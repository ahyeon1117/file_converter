from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

router = APIRouter()

# 클라이언트별 진행률 저장
progress_data = {}

@router.websocket("/progress/{client_id}")
async def progress_websocket(websocket: WebSocket, client_id: str):
    """각 클라이언트의 업로드 진행률을 WebSocket을 통해 전송"""
    await websocket.accept()

    try:
        while True:
            progress = progress_data.get(client_id, 0)
            await websocket.send_text(str(progress))

            if progress >= 100:
                break
            
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print(f"WebSocket connection closed for client {client_id}")
