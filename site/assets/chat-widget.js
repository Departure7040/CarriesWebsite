/**
 * chat-widget.js — Carrie Billeaud site AI assistant (vanilla JS, no framework)
 * -----------------------------------------------------------------------------
 * Floating bubble bottom-right → opens an accessible chat panel that POSTs to
 * /api/chat. History is kept in memory only (nothing persisted). Matches the
 * site palette (teal / gold / cream). Does NOT auto-open.
 *
 * Feature-flagged for launch: this file is intentionally NOT wired into any
 * page yet. Include it with a single deferred <script> tag once the API key is
 * set and Carrie has signed off (see build/agent_setup.md).
 *
 * Compliance: the panel header carries a permanent one-line disclaimer. The real
 * guardrail is the server-side system prompt — this widget is just the surface.
 */
(function () {
  "use strict";
  if (window.__carrieChatLoaded) return; // guard against double-include
  window.__carrieChatLoaded = true;

  var ENDPOINT = "/api/chat";
  var DISCLAIMER = "Carrie's AI assistant · general info, not advice";

  // In-memory history: [{role:'user'|'assistant', content:'...'}]
  var history = [];
  var sending = false;
  var lastFocus = null; // element focused before the panel opened

  // ---- styles (scoped by .cbchat- prefix; uses site CSS vars with fallbacks) --
  var css =
    ".cbchat-fab{position:fixed;right:20px;bottom:20px;z-index:9999;width:60px;height:60px;border-radius:50%;border:none;cursor:pointer;background:var(--teal,#0f5c5a);color:#fff;box-shadow:0 4px 14px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center}" +
    ".cbchat-fab:hover{background:var(--teal-dark,#0b4442)}" +
    ".cbchat-fab:focus-visible{outline:3px solid var(--gold,#c9a24b);outline-offset:2px}" +
    ".cbchat-fab svg{width:28px;height:28px}" +
    "@media (max-width:720px){.cbchat-fab{bottom:74px}}" + /* clear sticky-call bar */
    ".cbchat-panel{position:fixed;right:20px;bottom:20px;z-index:10000;width:360px;max-width:calc(100vw - 32px);height:520px;max-height:calc(100vh - 40px);background:var(--cream,#faf7f2);border:1px solid var(--rule,#e3ded4);border-radius:14px;box-shadow:0 10px 34px rgba(0,0,0,.28);display:flex;flex-direction:column;overflow:hidden;font-family:system-ui,'Segoe UI',Roboto,sans-serif;color:var(--ink,#1a2332)}" +
    "@media (max-width:720px){.cbchat-panel{right:8px;left:8px;bottom:8px;width:auto;height:calc(100vh - 16px)}}" +
    ".cbchat-head{background:var(--teal,#0f5c5a);color:#fff;padding:.7rem .9rem;display:flex;align-items:flex-start;gap:.5rem}" +
    ".cbchat-head-txt{flex:1;min-width:0}" +
    ".cbchat-title{font-weight:700;font-size:.98rem;line-height:1.2}" +
    ".cbchat-disc{font-size:.72rem;opacity:.9;margin-top:.15rem;line-height:1.25}" +
    ".cbchat-x{background:transparent;border:none;color:#fff;font-size:1.4rem;line-height:1;cursor:pointer;padding:.1rem .3rem;border-radius:6px}" +
    ".cbchat-x:focus-visible{outline:2px solid var(--gold,#c9a24b);outline-offset:1px}" +
    ".cbchat-log{flex:1;overflow-y:auto;padding:.9rem;display:flex;flex-direction:column;gap:.6rem}" +
    ".cbchat-msg{max-width:85%;padding:.55rem .75rem;border-radius:12px;font-size:.92rem;line-height:1.45;white-space:pre-wrap;word-wrap:break-word}" +
    ".cbchat-msg.bot{background:var(--paper,#fff);border:1px solid var(--rule,#e3ded4);align-self:flex-start;border-bottom-left-radius:4px}" +
    ".cbchat-msg.me{background:var(--teal,#0f5c5a);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}" +
    ".cbchat-msg.err{background:#fdecea;border:1px solid #f3c0bb;color:#8a1c14;align-self:flex-start}" +
    ".cbchat-typing{align-self:flex-start;font-size:.85rem;color:#5a6472;font-style:italic}" +
    ".cbchat-foot{border-top:1px solid var(--rule,#e3ded4);padding:.6rem;display:flex;gap:.5rem;align-items:flex-end;background:var(--paper,#fff)}" +
    ".cbchat-input{flex:1;resize:none;border:1px solid var(--rule,#e3ded4);border-radius:8px;padding:.5rem .6rem;font:inherit;font-size:.92rem;max-height:96px;color:var(--ink,#1a2332)}" +
    ".cbchat-input:focus-visible{outline:2px solid var(--teal,#0f5c5a);outline-offset:0}" +
    ".cbchat-send{background:var(--gold,#c9a24b);color:var(--ink,#1a2332);border:none;border-radius:8px;padding:.55rem .9rem;font-weight:700;cursor:pointer;font:inherit}" +
    ".cbchat-send:disabled{opacity:.55;cursor:default}" +
    ".cbchat-send:focus-visible{outline:2px solid var(--teal,#0f5c5a);outline-offset:1px}" +
    ".cbchat-hidden{display:none!important}";

  var styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ---- build DOM (all via createElement/textContent — no HTML injection) -----
  var fab = document.createElement("button");
  fab.className = "cbchat-fab";
  fab.type = "button";
  fab.setAttribute("aria-label", "Open chat with Carrie's assistant");
  fab.setAttribute("aria-haspopup", "dialog");
  fab.setAttribute("aria-expanded", "false");
  fab.innerHTML =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-8.5 8.5 8.5 8.5 0 0 1-3.8-.9L3 21l1.9-5.7A8.38 8.38 0 0 1 4 11.5 8.5 8.5 0 0 1 12.5 3 8.38 8.38 0 0 1 21 11.5z"/></svg>';

  var panel = document.createElement("div");
  panel.className = "cbchat-panel cbchat-hidden";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-modal", "false");
  panel.setAttribute("aria-label", "Chat with Carrie Billeaud's assistant");

  // header
  var head = document.createElement("div");
  head.className = "cbchat-head";
  var headTxt = document.createElement("div");
  headTxt.className = "cbchat-head-txt";
  var title = document.createElement("div");
  title.className = "cbchat-title";
  title.textContent = "Chat with Carrie";
  var disc = document.createElement("div");
  disc.className = "cbchat-disc";
  disc.textContent = DISCLAIMER;
  headTxt.appendChild(title);
  headTxt.appendChild(disc);
  var xBtn = document.createElement("button");
  xBtn.className = "cbchat-x";
  xBtn.type = "button";
  xBtn.setAttribute("aria-label", "Close chat");
  xBtn.innerHTML = "&times;";
  head.appendChild(headTxt);
  head.appendChild(xBtn);

  // log (live region)
  var log = document.createElement("div");
  log.className = "cbchat-log";
  log.setAttribute("role", "log");
  log.setAttribute("aria-live", "polite");
  log.setAttribute("aria-atomic", "false");

  // footer / input
  var foot = document.createElement("div");
  foot.className = "cbchat-foot";
  var input = document.createElement("textarea");
  input.className = "cbchat-input";
  input.rows = 1;
  input.setAttribute("aria-label", "Type your message");
  input.setAttribute("placeholder", "Ask about buying or selling…");
  var send = document.createElement("button");
  send.className = "cbchat-send";
  send.type = "button";
  send.textContent = "Send";
  foot.appendChild(input);
  foot.appendChild(send);

  panel.appendChild(head);
  panel.appendChild(log);
  panel.appendChild(foot);

  document.body.appendChild(fab);
  document.body.appendChild(panel);

  // ---- helpers ---------------------------------------------------------------
  function addMsg(role, text) {
    var el = document.createElement("div");
    el.className =
      "cbchat-msg " + (role === "user" ? "me" : role === "error" ? "err" : "bot");
    el.textContent = text;
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  var typingEl = null;
  function showTyping() {
    typingEl = document.createElement("div");
    typingEl.className = "cbchat-typing";
    typingEl.textContent = "Carrie's assistant is typing…";
    log.appendChild(typingEl);
    log.scrollTop = log.scrollHeight;
  }
  function hideTyping() {
    if (typingEl && typingEl.parentNode) typingEl.parentNode.removeChild(typingEl);
    typingEl = null;
  }

  function openPanel() {
    lastFocus = document.activeElement;
    panel.classList.remove("cbchat-hidden");
    fab.classList.add("cbchat-hidden");
    fab.setAttribute("aria-expanded", "true");
    if (!history.length) {
      addMsg(
        "assistant",
        "Hey there! I'm Carrie's website assistant. Ask me a general question about buying or selling in the Lafayette area, or I can get your info to Carrie. (General info, not advice.)"
      );
    }
    setTimeout(function () {
      input.focus();
    }, 50);
  }

  function closePanel() {
    panel.classList.add("cbchat-hidden");
    fab.classList.remove("cbchat-hidden");
    fab.setAttribute("aria-expanded", "false");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
    else fab.focus();
  }

  function autosize() {
    input.style.height = "auto";
    input.style.height = Math.min(input.scrollHeight, 96) + "px";
  }

  async function sendMessage() {
    var text = input.value.trim();
    if (!text || sending) return;
    sending = true;
    send.disabled = true;

    addMsg("user", text);
    history.push({ role: "user", content: text });
    input.value = "";
    autosize();
    showTyping();

    try {
      var res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ messages: history, page: location.pathname }),
      });
      hideTyping();
      var data = await res.json().catch(function () {
        return null;
      });

      if (res.ok && data && typeof data.reply === "string") {
        addMsg("assistant", data.reply);
        history.push({ role: "assistant", content: data.reply });
      } else {
        addMsg(
          "error",
          "Sorry — I couldn't reach the assistant just now. Please call Carrie at 337-258-5379 or use the contact form."
        );
      }
    } catch (e) {
      hideTyping();
      addMsg(
        "error",
        "Sorry — a connection problem stopped that message. Please try again, or call 337-258-5379."
      );
    } finally {
      sending = false;
      send.disabled = false;
      input.focus();
    }
  }

  // ---- events ----------------------------------------------------------------
  fab.addEventListener("click", openPanel);
  xBtn.addEventListener("click", closePanel);
  send.addEventListener("click", sendMessage);
  input.addEventListener("input", autosize);

  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Esc closes the panel from anywhere inside it.
  panel.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      e.preventDefault();
      closePanel();
    }
  });

  // Simple focus trap: keep Tab within the panel while it's open.
  panel.addEventListener("keydown", function (e) {
    if (e.key !== "Tab") return;
    var focusables = panel.querySelectorAll(
      'button, [href], textarea, input, [tabindex]:not([tabindex="-1"])'
    );
    if (!focusables.length) return;
    var first = focusables[0];
    var last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
})();
