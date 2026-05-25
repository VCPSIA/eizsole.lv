import secrets
from django.conf import settings


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        nonce = secrets.token_urlsafe(16)
        request.csp_nonce = nonce
        response = self.get_response(request)
        policy = getattr(settings, 'CONTENT_SECURITY_POLICY', '')
        if policy:
            response['Content-Security-Policy'] = policy.replace('{csp_nonce}', nonce)
        return response
