import { Hono } from "hono"
import { getCookie, setCookie } from "hono/cookie"
import crypto from "crypto"

const app = new Hono()
const app2 = new Hono()

const FLAG = process.env.FLAG ?? "fwectf{You_Won!_Sample_Flag}"
const DUMMY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}"
const FLAG_LEN = FLAG.length

let pwned = false

type Session = { idx: number }
const sessions = new Map<string, Session>()
const isAllowedURL = (u: URL) => u.protocol === "http:" && !["localhost", "0.0.0.0", "127.0.0.1"].includes(u.hostname)
const PAGE = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AED</title>
<link rel="icon" href="/favicon.ico?v=3" type="image/x-icon" sizes="any">
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root{
    --bg: #ffffff;
    --fg: #1f1f27ff;
    --muted: #555555;
    --accent: #00bfff;
  }
  html,body{height:100%;}
  body{
    margin:0;
    background:var(--bg);
    color:var(--fg);
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    position:relative;
    overflow:hidden;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans";
  }
  .stage{
    position:relative;
    width:min(560px, 90vw);
    height:min(560px, 90vh);
    display:flex;
    align-items:center;
    justify-content:center;
  }

  /* Heart */
  #heart{
    width: min(38vmin, 220px);
    height: auto;
    display:block;
    color: var(--accent);
    filter: drop-shadow(0 6px 18px rgba(0, 191, 255, 0.32));
    transition: transform .25s ease, filter .25s ease, opacity .25s ease;
  }
  @keyframes beat {
    0%   { transform: scale(1);   }
    15%  { transform: scale(1.12);}
    30%  { transform: scale(1);   }
    45%  { transform: scale(1.12);}
    60%  { transform: scale(1);   }
    100% { transform: scale(1);   }
  }

  #flag{
    position:absolute;
    top:60%;
    left:50%;
    transform: translate(-50%, -50%);
    font-size: clamp(20px, 3vmax, 36px);
    letter-spacing:.08em;
    font-weight:600;
    color: var(--muted);
    white-space: nowrap;
    overflow-x: auto;
    max-width: 90vw;
  }

  body.mode-pwned #heart{
    animation: beat 1.2s ease-in-out infinite;
    filter: drop-shadow(0 0 22px rgba(0,191,255,.65));
  }
  body.mode-pwned #flag{
    color: #151227ff;
  }

  #out{ display:none; }
</style>
</head>
<body class="mode-safe">
  <div class="stage">
    <svg id="heart" viewBox="0 0 512 512" aria-label="heart" role="img">
      <path fill="currentColor" d="M471.6 73.1c-54.5-46.4-136-38.7-186.4 13.7L256 116l-29.2-29.2C176.4 34.4 94.9 26.7 40.4 73.1-21.4 125.8-13.4 227.8 43 285.5l187.2 190c7.5 7.6 19.6 7.6 27.1 0l187.2-190c56.4-57.7 64.4-159.7 26.9-212.4z"/>
    </svg>
    <div id="flag">????????????????</div>
    <div id="out"></div>
  </div>

<script>
const flagEl = document.getElementById('flag');
let live=false;
let len=0;
let buf=[];

async function beat(){
  const r = await fetch('/heartbeat');
  const d = await r.json();
  document.body.classList.toggle('mode-pwned', d.pwned === true);
  document.body.classList.toggle('mode-safe',  !(d.pwned === true));

const TALL_NARROW = "Iljtf{}"; 
if (!d.pwned) {
  buf.push(d.char);
  if (buf.length > 30) buf.shift();
  const html = buf.map(function (ch) {
    let pct;
    if (Math.random() < 1/2) {
      pct = 150;
    } else {
      pct = 100;
    }

    return '<span style="display:inline-block;color:#f00;font-size:' + pct + '%;">'
         + esc(ch)
         + '</span>';
  }).join('');

  flagEl.innerHTML = html;
  return;
}
  
function esc(s){
  return String(s).replace(/[&<>"']/g, function(m){
    return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]);
  });
}

  if(!live){
    live=true;
    len=d.len;
    buf=Array(len).fill('?');
  }
  buf[d.pos]=d.char;
  flagEl.textContent = buf.join('');
  if(buf.includes('?')) setTimeout(retryMissing,500);
}

function retryMissing(){
  if(!buf.includes('?')) return;
  fetch('/heartbeat').then(r=>r.json()).then(d=>{
    document.body.classList.toggle('mode-pwned', d.pwned === true);
    document.body.classList.toggle('mode-safe',  !(d.pwned === true));
    if(!d.pwned) return;
    if(buf[d.pos]==='?'){
      buf[d.pos]=d.char;
      flagEl.textContent = buf.join('');
    }
    if(buf.includes('?')) setTimeout(retryMissing,500);
  });
}

setInterval(beat,1000);
</script>
</body>
</html>`;

const getSid = (c: any) => {
  let sid = getCookie(c, "sid")
  if (!sid) {
    sid = crypto.randomUUID()
    setCookie(c, "sid", sid, { httpOnly: true, secure: false, sameSite: "Lax", path: "/" })
  }
  return sid
}

const getSession = (sid: string) => {
  let s = sessions.get(sid)
  if (!s) {
    s = { idx: -1 }
    sessions.set(sid, s)
  }
  return s
}

app.get('/favicon.ico', () => {
  const file = Bun.file('./public/favicon.ico')
  return new Response(file, {
    headers: {
      'Content-Type': 'image/x-icon',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  })
})

app.use("*", (c, next) => {
  c.set("sid", getSid(c))
  return next()
})

app.get("/", c => {
  getSession(c.get("sid")).idx = -1
  return c.html(PAGE)
})

app.get("/heartbeat", c => {
  const s = getSession(c.get("sid"))
  if (!pwned) {
    const char = DUMMY[Math.floor(Math.random() * DUMMY.length)]
    return c.json({ pwned: false, char })
  }
  if (s.idx === -1) s.idx = 0
  const pos = s.idx
  const char = FLAG[pos]
  s.idx = (s.idx + 1) % FLAG_LEN
  return c.json({ pwned: true, char, pos, len: FLAG_LEN })
})

app2.get("/toggle", c => {
  pwned = true
  sessions.forEach(s => (s.idx = -1))
  return c.text("OK")
})

app.get("/fetch", async c => {
  const raw = c.req.query("url")
  if (!raw) return c.text("missing url", 400)
  let u: URL
  try {
    u = new URL(raw)
  } catch {
    return c.text("bad url", 400)
  }
  if (!isAllowedURL(u)) return c.text("forbidden", 403)
  const r = await fetch(u.toString(), { redirect: "manual" }).catch(() => null)
  if (!r) return c.text("upstream error", 502)
  if (r.status >= 300 && r.status < 400) return c.text("redirect blocked", 403)
  return c.text(await r.text())
})

const handler = (req: Request, server: any) => {
  const ip = server.requestIP(req)?.address ?? ""
  return app.fetch(req, { REMOTE_ADDR: ip })
}

const handler2 = (req: Request, server: any) => {
  const ip = server.requestIP(req)?.address ?? ""
  return app2.fetch(req, { REMOTE_ADDR: ip })
}

Bun.serve({ port: 3000, reusePort: true, fetch: handler })
Bun.serve({ port: 4000, reusePort: true, fetch: handler2 })
console.log(`Started server: http://localhost:3000`)
