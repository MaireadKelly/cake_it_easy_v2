// static/newsletter/newsletter.js
// Handles newsletter modal subscription and (only on first-time success) shows the WELCOME10 code.

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("nl-form");
    if (!form) return;

    const intro = document.getElementById("nl-intro");
    const successPanel = document.getElementById("nl-success");
    const hint = document.getElementById("nl-hint");
    const codeEl = document.getElementById("nl-code");
    const copyBtn = document.getElementById("nl-copy");
    const copiedMsg = document.getElementById("nl-copied");

    const setHint = (text) => {
        if (!hint) return;
        hint.textContent = text;
        hint.classList.remove("d-none");
    };

    const hideHint = () => {
        if (!hint) return;
        hint.classList.add("d-none");
    };

    const showSuccess = (code) => {
        // Show success panel, hide form/intro/hint
        if (codeEl && code) codeEl.textContent = code;
        if (successPanel) successPanel.classList.remove("d-none");
        if (intro) intro.classList.add("d-none");
        form.classList.add("d-none");
        hideHint();
    };

    const resetUIForRetry = (message) => {
        // Keep the form visible, show a helpful message
        if (successPanel) successPanel.classList.add("d-none");
        if (intro) intro.classList.remove("d-none");
        form.classList.remove("d-none");
        if (message) setHint(message);
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector("button[type='submit']");
        if (submitBtn) submitBtn.disabled = true;

        const formData = new FormData(form);

        try {
            const resp = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: { "X-Requested-With": "XMLHttpRequest" },
            });

            // Expect JSON from the view for AJAX requests
            const data = await resp.json().catch(() => null);

            if (!resp.ok) {
                // Invalid email or server-side validation
                resetUIForRetry((data && data.message) || "Please enter a valid email.");
                return;
            }

            // created === true => show the code panel
            if (data && data.created) {
                showSuccess(data.code || "WELCOME10");
                return;
            }

            // created === false => already subscribed (or no-op)
            resetUIForRetry(
                (data && data.message) || "You're already subscribed with that email."
            );
        } catch (error) {
            console.error("Newsletter subscribe error:", error);
            resetUIForRetry("Something went wrong. Please try again.");
        } finally {
            if (submitBtn) submitBtn.disabled = false;
        }
    });

    // "Copy code" button behaviour
    if (copyBtn && codeEl && copiedMsg) {
        copyBtn.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(codeEl.textContent.trim());
                copiedMsg.classList.remove("d-none");
                setTimeout(() => copiedMsg.classList.add("d-none"), 2000);
            } catch (err) {
                console.error("Clipboard error:", err);
            }
        });
    }
});
