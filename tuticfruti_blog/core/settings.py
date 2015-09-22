# Pagination
PAGINATE_BY = 10
PAGINATE_ORPHANS = 1
ORDERING = '-created'

# Choices
POST_DRAFT_STATUS = 'draft'
POST_PUBLIC_STATUS = 'published'

POST_STATUS_CHOICES = (
    (POST_DRAFT_STATUS, 'Draft'),
    (POST_PUBLIC_STATUS, 'Published'),
)

COMMENT_PENDING_STATUS = 'pending'
COMMENT_PUBLISHED_STATUS = 'published'

COMMENT_STATUS_CHOICES = (
    (COMMENT_PENDING_STATUS, 'Pending'),
    (COMMENT_PUBLISHED_STATUS, 'Published'),
)

PYTHON_CATEGORY = 'python'
DJANGO_CATEGORY = 'django'
MISCELLANEOUS_CATEGORY = 'miscellaneous'

CATEGORY_CHOICES = (
    (PYTHON_CATEGORY, 'Python'),
    (DJANGO_CATEGORY, 'Django'),
    (MISCELLANEOUS_CATEGORY, 'Miscellaneous'),
)

FUZZY_TEXTS = [
    'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Nam cursus. Morbi ut mi. Nullam enim leo, egestas id, condimentum at, laoreet mattis, massa.',
    'Sed eleifend nonummy diam. Praesent mauris ante, elementum et, bibendum at, posuere sit amet, nibh. Duis tincidunt lectus quis dui viverra vestibulum.',
    'Suspendisse vulputate aliquam dui. Nulla elementum dui ut augue. Aliquam vehicula mi at mauris. Maecenas placerat, nisl at consequat rhoncus, sem nunc gravida justo, quis eleifend arcu velit quis lacus. Morbi magna magna, tincidunt a, mattis non, imperdiet vitae, tellus.',
    'Sed odio est, auctor ac, sollicitudin in, consequat vitae, orci. Fusce id felis. Vivamus sollicitudin metus eget eros.Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In posuere felis nec tortor. Pellentesque faucibus. Ut accumsan ultricies elit.',
    'Maecenas at justo id velit placerat molestie. Donec dictum lectus non odio. Cras a ante vitae enim iaculis aliquam. Mauris nunc quam, venenatis nec, euismod sit amet, egestas placerat, est.',
    'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras id elit. Integer quis urna. Ut ante enim, dapibus malesuada,fringilla eu, condimentum quis, tellus. Aenean porttitor eros vel dolor. Donec convallis pede venenatis nibh. Duis quam. Nam eget lacus. Aliquam erat volutpat.']
