
def check_viewing_rights_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())