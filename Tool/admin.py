from django.contrib import admin
from django.apps import apps

# from guardian.admin import GuardedModelAdmin

# Register your models here.

models = apps.get_models()


for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass





# class ProjectAdmin(GuardedModelAdmin):
#     pass


# for model in models:
#     try:
#         admin.site.register(model, ProjectAdmin)
#     except admin.sites.AlreadyRegistered:
#         pass
