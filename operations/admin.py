from django.contrib import admin
from operations.models import ProgangUser, Consultation, Quotation, Proposal, Feedback


# class UserAdmin(admin.ModelAdmin):
#     readonly_fields = ["email", "password"]


admin.site.register(ProgangUser)
admin.site.register(Consultation)
admin.site.register(Quotation)
admin.site.register(Proposal)
admin.site.register(Feedback)


