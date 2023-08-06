Polls
=====

A RESTful blog app for django that you can use with any frontend framework.



Quick start
-----------

1. Add these apps to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        "rest_framework",
        "rest_framework.authtoken",
        'blog',
    ]
2. Include the polls URLconf in your project urls.py like this::

    path('api/blog/', include('blog.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a blog post (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/api/blog/posts to view posts