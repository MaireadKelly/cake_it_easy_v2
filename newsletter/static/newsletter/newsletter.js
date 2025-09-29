// newsletter.js
// Works for BOTH the inline card and the Bootstrap modal.
// Key fixes:
// 1) Scope success UI updates to the modal when present.
// 2) Clean the URL after showing success so it doesn't re-trigger.

(function () {
    // Utility: safely find elements either inside the modal or in the document
    function getScopedRefs() {
        var modalEl = document.getElementById("newsletterModal");
        var root = modalEl || document;

        return {
            modalEl: modalEl,
            root: root,
            form: root.querySelector("#nl-form"),
            success: root.querySelector("#nl-success"),
            codeEl: root.querySelector("#nl-code"),
            copyBtn: root.querySelector("#nl-copy"),
            copied: root.querySelector("#nl-copied"),
            hint: root.querySelector("#nl-hint"),
        };
    }

    function showSuccess(code) {
        var { modalEl, root, form, success, codeEl, copyBtn, copied, hint } = getScopedRefs();

        if (codeEl) codeEl.textContent = code || "";
        if (form) form.classList.add("d-none");
        if (hint) hint.classList.add("d-none");
        if (success) success.classList.remove("d-none");

        // Auto-open only if we actually updated the modal’s own nodes
        if (modalEl && success && modalEl.contains(success) && typeof bootstrap !== "undefined") {
            var modal = bootstrap.Modal.getOrCreateInstance(modalEl);
            modal.show();
        }

        // Clean URL so this doesn't re-trigger on refresh/back
        if (history && history.replaceState) {
            var newUrl = window.location.pathname + window.location.hash;
            history.replaceState(null, "", newUrl);
        }
    }

    function wireCopy() {
        var { root, copyBtn, codeEl, copied } = getScopedRefs();
        if (!root) return;

        // Support both inline + modal via delegation (in case there are two buttons)
        root.addEventListener("click", async function (e) {
            var target = e.target;
            if (!(target && (target.id === "nl-copy" || target.closest && target.closest("#nl-copy")))) return;

            var codeNode = codeEl || root.querySelector("#nl-code");
            if (!codeNode || !navigator.clipboard) return;

            try {
                await navigator.clipboard.writeText(codeNode.textContent.trim());
                if (target.innerText) {
                    var old = target.innerText;
                    target.innerText = "Copied!";
                    setTimeout(function () { target.innerText = old; }, 1200);
                }
                if (copied) {
                    copied.classList.remove("d-none");
                    setTimeout(function () { copied.classList.add("d-none"); }, 1200);
                }
            } catch (_) { /* no-op */ }
        });
    }

    function maybeShowSuccessFromUrl() {
        var params = new URLSearchParams(window.location.search || "");
        // Expect ?nl=1&code=XXXX  only after a confirmed subscribe redirect
        var nl = params.get("nl");
        var code = params.get("code");
        if (nl === "1" && code) {
            showSuccess(code);
        }
    }

    // Initialize once DOM is parsed
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", onReady);
    } else {
        onReady();
    }

    function onReady() {
        wireCopy();
        maybeShowSuccessFromUrl();
    }
})();
