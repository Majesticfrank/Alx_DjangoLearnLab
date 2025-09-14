My first Django project with ALX

# Permissions Setup
Custom permissions are defined in `Book` model:
- can_view → allows viewing books
- can_create → allows creating books
- can_edit → allows editing books
- can_delete → allows deleting books

Groups:
- Viewers → [can_view]
- Editors → [can_view, can_create, can_edit]
- Admins → [can_view, can_create, can_edit, can_delete]

Views enforce permissions using @permission_required decorators.
