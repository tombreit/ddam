
from ddam.organization.models import Branding


def branding(request):
    """Make branding settings available for all requests."""
    branding = Branding.load()
    return {"branding": branding}
