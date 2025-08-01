import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import socket
import re

# 환경변수
WOL_BROADCAST_IP = os.getenv("WOL_BROADCAST_IP", "255.255.255.255")

# 앱 설정
app = FastAPI()


# 라우터 정의
class WolRequest(BaseModel):
    mac: str

def send_magic_packet(mac: str):
    # MAC 주소 유효성 검사
    if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac):
        raise ValueError("Invalid MAC address format")
    mac_bytes = bytes.fromhex(mac.replace(":", "").replace("-", ""))
    packet = b'\xff' * 6 + mac_bytes * 16
    # 브로드캐스트 주소 환경변수에서 가져오기
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(packet, (WOL_BROADCAST_IP, 9))

@app.post("/wol")
def wol(req: WolRequest):
    try:
        send_magic_packet(req.mac)
        return {"result": "Magic packet sent", "mac": req.mac}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send magic packet") from e


@app.get("/")
def read_root():
    return {"Hello": "World"}
