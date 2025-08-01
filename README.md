``` bash
uv sync
export WOL_BROADCAST_IP=192.168.150.255 
uv run uvicorn main:app --port 25555
```