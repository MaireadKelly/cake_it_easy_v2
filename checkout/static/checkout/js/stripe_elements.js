document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed"); // Debugging log to ensure script runs after DOM is ready

    // Retrieve public key and client secret from the hidden inputs in the checkout template
    var stripePublicKeyElement = document.getElementById('id_stripe_public_key');
    if (stripePublicKeyElement) {
        var stripePublicKey = stripePublicKeyElement.value || stripePublicKeyElement.getAttribute('value');
        if (stripePublicKey) {
            stripePublicKey = stripePublicKey.trim();
            console.log("Stripe Public Key Retrieved:", stripePublicKey);
        } else {
            console.error("Stripe Public Key value is empty");
            return;
        }
    } else {
        console.error("Stripe Public Key element not found in DOM");
        return;
    }

    var clientSecretElement = document.getElementById('id_client_secret');
    if (clientSecretElement) {
        var clientSecret = clientSecretElement.value || clientSecretElement.getAttribute('value');
        if (clientSecret) {
            clientSecret = clientSecret.trim();
            console.log("Client Secret Retrieved:", clientSecret);
        } else {
            console.error("Client Secret value is empty");
            return;
        }
    } else {
        console.error("Client Secret element not found in DOM");
        return;
    }

    // Initialize Stripe
    try {
        var stripe = Stripe(stripePublicKey);
        console.log("Stripe initialized:", stripe);
    } catch (error) {
        console.error("Error initializing Stripe:", error);
        return;
    }

    var elements = stripe.elements();
    console.log("Elements instance created:", elements);

    // Styling options for Stripe Elements
    var style = {
        base: {
            color: '#000',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#dc3545',
            iconColor: '#dc3545'
        }
    };
    console.log("Initializing Stripe card element with style:", style);

    // Create an instance of the card element
    var card = elements.create('card', { style: style });
    card.mount('#card-element');
    console.log("Card Element mounted successfully");

    // Handle real-time validation errors on the card element
    card.addEventListener('change', function (event) {
        console.log("Card element changed:", event);
        var errorDiv = document.getElementById('card-errors');
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            errorDiv.innerHTML = html;
            console.error("Validation Error:", event.error.message);
        } else {
            errorDiv.textContent = '';
            console.log("Card input is valid");
        }
    });

    // Handle form submission
    var form = document.getElementById('payment-form');
    if (form) {
        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            console.log("Form submitted, starting payment process");

            card.update({ 'disabled': true });
            document.getElementById('submit-button').setAttribute('disabled', true);
            document.getElementById('loading-overlay').classList.remove('d-none');

            var saveInfo = Boolean(document.getElementById('id-save-info').checked);
            console.log("Save info status:", saveInfo);

            var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            console.log("CSRF Token:", csrfToken);

            var postData = {
                'csrfmiddlewaretoken': csrfToken,
                'client_secret': clientSecret,
                'save_info': saveInfo,
            };
            console.log("Post Data:", postData);

            var url = '/checkout/cache_checkout_data/';
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(postData)
            })
                .then(function (response) {
                    console.log("Cache checkout data response:", response);
                    return response.json();
                })
                .then(function () {
                    console.log("Payment confirmed, starting Stripe confirmation");
                    stripe.confirmCardPayment(clientSecret, {
                        payment_method: {
                            card: card,
                            billing_details: {
                                name: form.full_name.value.trim(),
                                phone: form.phone_number.value.trim(),
                                email: form.email.value.trim(),
                                address: {
                                    line1: form.street_address1.value.trim(),
                                    line2: form.street_address2.value.trim(),
                                    city: form.town_or_city.value.trim(),
                                    state: form.county.value.trim(),
                                }
                            }
                        },
                        shipping: {
                            name: form.full_name.value.trim(),
                            phone: form.phone_number.value.trim(),
                            address: {
                                line1: form.street_address1.value.trim(),
                                line2: form.street_address2.value.trim(),
                                city: form.town_or_city.value.trim(),
                                postal_code: form.postcode.value.trim(),
                                state: form.county.value.trim(),
                            }
                        },
                    }).then(function (result) {
                        if (result.error) {
                            console.error("Payment Error:", result.error.message);
                            var errorDiv = document.getElementById('card-errors');
                            var html = `
                        <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                        </span>
                        <span>${result.error.message}</span>`;
                            errorDiv.innerHTML = html;
                            card.update({ 'disabled': false });
                            document.getElementById('submit-button').removeAttribute('disabled');
                            document.getElementById('loading-overlay').classList.add('d-none');
                        } else {
                            if (result.paymentIntent.status === 'succeeded') {
                                console.log("Payment Succeeded!");
                                form.submit();
                            }
                        }
                    });
                })
                .catch(function (error) {
                    console.error("Error during fetch or Stripe confirmation:", error);
                    location.reload();
                });
        });
    } else {
        console.error("Payment form not found in the DOM");
    }
});
