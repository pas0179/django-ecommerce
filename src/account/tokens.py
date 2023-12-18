# import de tokens pour reset password
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Installer avec pip avant de declarer
import six  

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()