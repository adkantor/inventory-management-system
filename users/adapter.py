from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form):
        user = super(CustomAccountAdapter, self).save_user(request, user, form)
        return user