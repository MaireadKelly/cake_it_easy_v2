from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def robots_txt(request):
    """Robots rules for the deployed site.

    Note:
    - Bag / Checkout / Accounts / Admin are not meant to be indexed.
    - Sitemap location is provided as an absolute URL for best compatibility.
    """
    sitemap_url = request.build_absolute_uri(reverse("sitemap_xml"))
    lines = [
        "User-agent: *",
        "Disallow: /bag/",
        "Disallow: /checkout/",
        "Disallow: /accounts/",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """Minimal sitemap for public, indexable pages."""
    url_names = [
        "home",  # if your home URL name differs, update/remove this
        "product_list",
        "product_cakes",
        "product_accessories",
        "product_offers",
        "about",
    ]

    urls = []
    for name in url_names:
        try:
            urls.append(request.build_absolute_uri(reverse(name)))
        except Exception:
            # Ignore missing routes (keeps this view safe during refactors)
            continue

    body = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        body.extend(
            [
                "  <url>",
                f"    <loc>{u}</loc>",
                "  </url>",
            ]
        )
    body.append("</urlset>")

    return HttpResponse("\n".join(body), content_type="application/xml")


def custom_404(request, exception):
    """Render templates/404.html when DEBUG=False."""
    return render(request, "404.html", status=404)
