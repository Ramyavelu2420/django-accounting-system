from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # If the social account is already linked, do nothing
        if sociallogin.is_existing:
            return
        
        email = sociallogin.user.email
        if not email:
            return
        
        UserModel = get_user_model()
        try:
            # Look up existing user by email
            user = UserModel.objects.get(email__iexact=email)
            # Link the social account to this user
            sociallogin.connect(request, user)
        except UserModel.DoesNotExist:
            pass
