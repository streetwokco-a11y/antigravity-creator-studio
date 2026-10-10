"""
mcp_server.py - Model Context Protocol Engine for Antigravity Studio.
Exposes media QA, audio DSP normalization, and outlier analytics over MCP.
"""

import sys
import json
import os

WORKSPACE_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, WORKSPACE_ROOT)

from services.media_service import audit_video_compliance, auto_normalize_audio
from services.analytics_service import get_outliers
from services.qa_service import run_full_preflight_audit

try:
    from mcp.server.fastmcp import FastMCP
    HAS_FASTMCP = True
except ImportError:
    HAS_FASTMCP = False

# ----------------- FASTMCP MODE -----------------
if HAS_FASTMCP:
    mcp = FastMCP("Antigravity-Studio-Engine")

    @mcp.tool()
    def audit_video(file_path: str) -> str:
        """Inspect video file for 60fps and EBU R128 (-14 LUFS) broadcast compliance."""
        res = audit_video_compliance(file_path)
        return json.dumps(res, indent=2)

    @mcp.tool()
    def autofix_loudness(file_path: str) -> str:
        """Apply lossless FFmpeg loudnorm normalization to target -14.0 LUFS."""
        out = auto_normalize_audio(file_path)
        return f"Normalized file saved to: {out}"

    @mcp.tool()
    def analyze_niche(file_path: str = "data/sample_collected.json", min_mult: float = 2.0) -> str:
        """Find video outliers beating channel median views and classify by 21 formulas."""
        res = get_outliers(file_path, min_mult)
        return json.dumps(res, indent=2)

    @mcp.resource("studio://status")
    def get_status() -> str:
        """Get pre-flight pipeline and skill registry health."""
        return json.dumps(run_full_preflight_audit(), indent=2)

    def run_server():
        mcp.run()

# ----------------- STDIO JSON-RPC 2.0 FALLBACK MODE -----------------
else:
    def handle_rpc_request(req: dict) -> dict:
        method = req.get("method")
        params = req.get("params", {})
        req_id = req.get("id")

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {"name": "audit_video", "description": "Audit video for -14 LUFS and 60fps."},
                        {"name": "autofix_loudness", "description": "Normalize audio to -14 LUFS."},
                        {"name": "analyze_niche", "description": "Calculate niche outliers and formulas."}
                    ]
                }
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if tool_name == "audit_video":
                res = audit_video_compliance(args.get("file_path", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
            elif tool_name == "autofix_loudness":
                out = auto_normalize_audio(args.get("file_path", ""))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": out}]}}
            elif tool_name == "analyze_niche":
                res = get_outliers(args.get("file_path", "data/sample_collected.json"), args.get("min_mult", 2.0))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

    def run_server():
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                req = json.loads(line)
                resp = handle_rpc_request(req)
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
            except Exception as e:
                err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()

if __name__ == "__main__":
    run_server()
