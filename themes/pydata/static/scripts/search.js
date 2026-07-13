/**
 * Hugo search using Fuse.js
 * Powers both the inline search dialog (pst-search-dialog) and the /search/ page.
 */
(function () {
  "use strict";

  // Fuse.js loaded from CDN in head.html when search is enabled.
  // We wait for it to be available.
  var FUSE_CDN = "https://cdn.jsdelivr.net/npm/fuse.js@7/dist/fuse.min.js";
  var INDEX_URL = (window.pstSearchIndexUrl || "/index.json");

  var fuseInstance = null;
  var indexData = null;

  function loadFuse(callback) {
    if (window.Fuse) { callback(); return; }
    var s = document.createElement("script");
    s.src = FUSE_CDN;
    s.onload = callback;
    document.head.appendChild(s);
  }

  function loadIndex(callback) {
    if (indexData) { callback(indexData); return; }
    fetch(INDEX_URL)
      .then(function (r) { return r.json(); })
      .then(function (data) {
        indexData = data;
        callback(data);
      })
      .catch(function (e) { console.warn("[PST search] Failed to load index:", e); });
  }

  function buildFuse(data) {
    fuseInstance = new Fuse(data, {
      keys: [
        { name: "title",   weight: 0.7 },
        { name: "summary", weight: 0.3 },
        { name: "content", weight: 0.2 },
        { name: "tags",    weight: 0.1 },
      ],
      includeScore: true,
      threshold: 0.4,
      minMatchCharLength: 2,
    });
  }

  function runSearch(query) {
    if (!fuseInstance || !query || query.length < 2) return [];
    return fuseInstance.search(query).slice(0, 15);
  }

  function resultHTML(results, query) {
    if (!query || query.length < 2) {
      return "<p class=\"search-empty\">Type to search&hellip;</p>";
    }
    if (results.length === 0) {
      return "<p class=\"search-empty\">No results for <strong>" + escapeHTML(query) + "</strong>.</p>";
    }
    var html = "<ul class=\"search-results-list\">";
    results.forEach(function (r) {
      var item = r.item;
      html += "<li class=\"search-result-item\">" +
        "<a href=\"" + escapeHTML(item.url) + "\">" +
          "<span class=\"search-result-title\">" + escapeHTML(item.title) + "</span>" +
          "<span class=\"search-result-summary\">" + escapeHTML(item.summary || "") + "</span>" +
        "</a></li>";
    });
    html += "</ul>";
    return html;
  }

  function escapeHTML(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function wireInput(inputEl, resultsEl) {
    if (!inputEl || !resultsEl) return;
    var debounceTimer;
    inputEl.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      var query = inputEl.value.trim();
      debounceTimer = setTimeout(function () {
        loadFuse(function () {
          loadIndex(function (data) {
            if (!fuseInstance) buildFuse(data);
            var results = runSearch(query);
            resultsEl.innerHTML = resultHTML(results, query);
          });
        });
      }, 150);
    });
  }

  // Wire up the search dialog (pst-search-dialog)
  function setupDialogSearch() {
    var dialogInput = document.getElementById("pst-search-input");
    if (!dialogInput) return;
    var resultsEl = document.getElementById("pst-dialog-search-results");
    if (!resultsEl) {
      resultsEl = document.createElement("div");
      resultsEl.id = "pst-dialog-search-results";
      resultsEl.className = "search-results";
      dialogInput.closest("form").insertAdjacentElement("afterend", resultsEl);
    }
    wireInput(dialogInput, resultsEl);
  }

  // Wire up the /search/ page
  function setupPageSearch() {
    var pageInput = document.getElementById("search-input");
    var pageResults = document.getElementById("search-results");
    if (!pageInput || !pageResults) return;
    // Pre-fill from query param
    var params = new URLSearchParams(window.location.search);
    var q = params.get("q") || "";
    if (q) {
      pageInput.value = q;
      loadFuse(function () {
        loadIndex(function (data) {
          if (!fuseInstance) buildFuse(data);
          pageResults.innerHTML = resultHTML(runSearch(q), q);
        });
      });
    }
    wireInput(pageInput, pageResults);
  }

  // Open search dialog on Ctrl+K / Cmd+K
  function setupKeyboardShortcut() {
    document.addEventListener("keydown", function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        var dialog = document.getElementById("pst-search-dialog");
        if (dialog) {
          if (dialog.open) {
            dialog.close();
          } else {
            dialog.showModal();
            var input = dialog.querySelector("input[type=search]");
            if (input) input.focus();
          }
        }
      }
    });
  }

  // Open dialog when the search button is clicked
  function setupSearchButtons() {
    document.querySelectorAll(".search-button__button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var dialog = document.getElementById("pst-search-dialog");
        if (dialog) {
          dialog.showModal();
          var input = dialog.querySelector("input[type=search]");
          if (input) { input.focus(); input.select(); }
        }
      });
    });
  }

  function init() {
    setupDialogSearch();
    setupPageSearch();
    // setupKeyboardShortcut() — handled by pydata-sphinx-theme.js (Ctrl+K)
    // setupSearchButtons()    — handled by pydata-sphinx-theme.js (onclick=y toggle)
  }

  if (document.readyState !== "loading") {
    init();
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
