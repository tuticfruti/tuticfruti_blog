# Pagination
PAGINATE_BY = 10
PAGINATE_ORPHANS = 1
ORDERING = '-created'

# Choices
DRAFT_STATUS = 'draft'
PUBLIC_STATUS = 'public'

STATUS_CHOICES = (
    (DRAFT_STATUS, 'Draft'),
    (PUBLIC_STATUS, 'Public'),
)

PYTHON_CATEGORY = 'python'
DJANGO_CATEGORY = 'django'
MISCELLANEOUS_CATEGORY = 'miscellaneous'

CATEGORY_CHOICES = (
    (PYTHON_CATEGORY, 'Python'),
    (DJANGO_CATEGORY, 'Django'),
    (MISCELLANEOUS_CATEGORY, 'Miscellaneous'),
)
