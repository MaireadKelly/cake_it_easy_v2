from django import template

register = template.Library()


@register.filter
def cloudinary_thumb(url, options="w_600,h_450,c_fill,f_auto,q_auto"):
    """
    If a Cloudinary delivery URL, inject transformation options after /upload/.
    Otherwise return the original URL unchanged.
    """
    try:
        if not url:
            return url
        marker = "/upload/"
        if marker in url and "res.cloudinary.com" in url:
            parts = url.split(marker)
            # Avoid double options if already present
            tail = parts[1]
            if not tail.startswith("c_") and not tail.startswith("w_"):
                return parts[0] + marker + options + "/" + tail
    except Exception:
        pass
    return url
