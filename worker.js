/**
 * Cloudflare Worker Entrypoint for Antigravity Creator Studio
 * Serves Studio UI assets and Edge endpoints on Cloudflare Workers.
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Edge API health check
    if (url.pathname === '/api/health') {
      return new Response(JSON.stringify({
        status: "HEALTHY",
        engine: "Antigravity Creator Studio Enterprise v2.6",
        region: "Cloudflare Edge",
        timestamp: new Date().toISOString()
      }), {
        headers: { "content-type": "application/json" }
      });
    }

    // Serve static Studio assets via Cloudflare Workers Assets binding
    if (env.ASSETS) {
      return env.ASSETS.fetch(request);
    }

    return new Response('Antigravity Creator Studio Edge Ready', { status: 200 });
  }
};
