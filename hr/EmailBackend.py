from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        logger.debug(f"Attempting to authenticate user with email: {username}")
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            logger.debug("User not found.")
            return None
        
        if user.check_password(password):
            logger.debug("Authentication successful.")
            return user
        
        logger.debug("Incorrect password.")
        return None
