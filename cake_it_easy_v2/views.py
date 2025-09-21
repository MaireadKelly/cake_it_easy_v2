from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

def robots_txt(_request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def sitemap_xml(request):
    """
    Minimal, hand-rolled sitemap for key pages.
    If a URL name below doesn't exist in your project, remove it.
    """
    url_names = [
        "product_list",
        "product_cakes",
        "product_accessories",
        "product_offers",
        "my_orders",      # auth required; still okay to list
        "about",
    ]
    urls = []
    for name in url_names:
        try:
            urls.append(request.build_absolute_uri(reverse(name)))
        except Exception:
            # Ignore missing routes
            pass

    body = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        body += ["  <url>", f"    <loc>{u}</loc>", "  </url>"]
    body += ["</urlset>"]
    return HttpResponse("\n".join(body), content_type="application/xml")

def custom_404(request, exception):
    """Render templates/404.html when DEBUG=False."""
    return render(request, "404.html", status=404)
