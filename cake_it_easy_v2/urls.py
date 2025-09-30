"""
URL configuration for cake_it_easy_v2 project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.http import HttpResponse

from cake_it_easy_v2 import views as core_views


def robots_txt(_):
    return HttpResponse(
        (
            "User-agent: *\n"
            "Disallow:\n"
            "Sitemap: https://<YOUR-DOMAIN>/sitemap.xml\n"
        ),
        content_type="text/plain",
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("products/", include("products.urls")),
    path("custom_cake/", include("custom_cake.urls")),
    path("bag/", include("bag.urls")),
    path("checkout/", include("checkout.urls")),
    path("profile/", include("profiles.urls")),
    path(
        "about/",
        TemplateView.as_view(template_name="about.html"),
        name="about",
    ),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", core_views.sitemap_xml, name="sitemap_xml"),
    path("newsletter/", include("newsletter.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "cake_it_easy_v2.views.custom_404"
