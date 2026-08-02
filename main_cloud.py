import asyncio
import logging
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

BOTS = [
    {
        "name": "bot1_channels",
        "cmd": [sys.executable, "main_bot1.py"],
        "cwd": "."
    },
    {
        "name": "bot2_library",
        "cmd": [sys.executable, "main.py"],
        "cwd": "bot2"
    }
]

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.getenv("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logging.info(f"Health server listening on port {port}")

async def run_bot(name, cmd, cwd):
    while True:
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            logging.info(f"[{name}] started (pid {proc.pid})")
            async for line in proc.stdout:
                logging.info(f"[{name}] {line.decode('utf-8', errors='replace').strip()}")
            await proc.wait()
        except Exception as e:
            logging.error(f"[{name}] failed to start: {e}")
        logging.error(f"[{name}] exited, restarting in 15s")
        await asyncio.sleep(15)

async def main():
    tasks = [asyncio.create_task(run_bot(**b)) for b in BOTS]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        start_health_server()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Cloud supervisor stopped")
