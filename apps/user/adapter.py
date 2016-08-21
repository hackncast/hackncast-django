from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    def __init__(self, request=None):
        super(CustomAccountAdapter, self).__init__(request)
        self.error_messages['email_taken'] = "Este email já está em uso"
