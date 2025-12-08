// static/newsletter/newsletter.js
// Handles newsletter modal subscription and shows the WELCOME10 code.

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("nl-form");
    if (!form) {
        // Modal not on this page; nothing to do.
        return;
    }

    const emailInput = document.getElementById("nl-email");
    const successPanel = document.getElementById("nl-success");
    const hint = document.getElementById("nl-hint");
    const codeEl = document.getElementById("nl-code");
    const copyBtn = document.getElementById("nl-copy");
    const copiedMsg = document.getElementById("nl-copied");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector("button[type='submit']");
        if (submitBtn) {
            submitBtn.disabled = true;
        }

        const formData = new FormData(form);

        try {
            // Send the subscription to the backend.
            // We do not rely on the response body to show the discount code,
            // so this works whether the view returns HTML or JSON.
            await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });
        } catch (error) {
            console.error("Newsletter subscribe error:", error);
            // Even if the request fails, we still show the code for UX.
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
            }

            // Update UI: show success, hide form and hint.
            if (codeEl) {
                // Always show this discount code
                codeEl.textContent = "WELCOME10";
            }
            if (successPanel) {
                successPanel.classList.remove("d-none");
            }
            if (form) {
                form.classList.add("d-none");
            }
            if (hint) {
                hint.classList.add("d-none");
            }
        }
    });

    // "Copy code" button behaviour
    if (copyBtn && codeEl && copiedMsg) {
        copyBtn.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(codeEl.textContent.trim());
                copiedMsg.classList.remove("d-none");
                setTimeout(() => {
                    copiedMsg.classList.add("d-none");
                }, 2000);
            } catch (err) {
                console.error("Clipboard error:", err);
            }
        });
    }
});
