from django.urls import reverse

from .url_names import (
    LOGOUT_URL_NAME,
    PASS_RESET_CONFIRM_URL_NAME,
    PASS_RESET_URL_NAME,
    REFRESH_TOKEN_URL_NAME,
    TOKEN_AUTH_URL_NAME,
    TOKEN_VERIFY_URL_NAME,
    USER_API_URL_NAME,
    USER_REGISTRATION_URL_NAME,
)

# urls
USER_REGISTRATION_URL = reverse(f"v0:{USER_REGISTRATION_URL_NAME}")
USER_API_URL = reverse(f"v0:{USER_API_URL_NAME}")
TOKEN_AUTH_URL = reverse(f"v0:{TOKEN_AUTH_URL_NAME}")
REFRESH_TOKEN_URL = reverse(f"v0:{REFRESH_TOKEN_URL_NAME}")
TOKEN_VERIFY_URL = reverse(f"v0:{TOKEN_VERIFY_URL_NAME}")
LOGOUT_URL = reverse(f"v0:{LOGOUT_URL_NAME}")
PASS_RESET_URL = reverse(f"v0:{PASS_RESET_URL_NAME}")
PASS_RESET_CONFIRM_URL = reverse(f"v0:{PASS_RESET_CONFIRM_URL_NAME}")
