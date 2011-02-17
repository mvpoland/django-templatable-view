# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import loader, TemplateDoesNotExist
from django.template import RequestContext
from functools import wraps

# Author: Jonathan Slenders, CityLive

# Remember which templates are actually in use.
__registered_templates = set()  # list of template names
__registered_templates_views = { } # mapping from template name to list of views.


def register_template(path, view_func=None):
    """
    Register this template as one which is called somewhere from a view.
    (Is also a candidate for template compilation.)
    """
    if path:
        __registered_templates.add(path)

    if view_func:
        if path in __registered_templates_views:
            __registered_templates_views[path].append(view_func)
        else:
            __registered_templates_views[path] = [ view_func ]


def templatable_view(default_template_name, default_context=None):
    """
    Creates a decorator which
    - Extracts the `context` and `template_name` params from the view.
    - Call the view without those parameters
    - Render the template. Use the default template if none was passed to the view.

    The decorated view should return either:
    - a context dictionary; or
    - a tuple (template_name, context dictionary); or
    - a HttpResponse
    """
    # Create decorator
    def decorator(view_func):
        # When the decorator wraps around a view function
        if default_template_name:
            # Remember template and view function
            register_template(default_template_name, view_func)

        # New view
        @wraps(view_func)
        def decorate(request, *args, **kwargs):
            """
            Wrapper around the view
            """
            # Start from the default context and update this one every step
            context = default_context or {}

            # Pop decorator parameters
            context.update(kwargs.pop('context', { }))
            template_name = kwargs.pop('template_name', default_template_name)

            # Call original view function
            view_result = view_func(request, *args, **kwargs)

            if isinstance(view_result, dict):
                # and if the result was a dict, update context and render template
                context.update(view_result)

                # Make sure templates are rendered in strict mode.
                # see: cl_utils/django_patches/patch_resolve_to_not_fail_silently.p
                context.update({'strict': True })

                return render_to_response(template_name, context,  context_instance=RequestContext(request))
            elif isinstance(view_result, tuple):
                view_result_template, view_result_context = view_result
                context.update(view_result_context)
                return render_to_response(view_result_template, context,  context_instance=RequestContext(request))
            else:
                # otherwise, just return the HttpResponseRedirect or whatever the view returned
                return view_result

        return decorate
    return decorator


templatable_view.get_registered_templates = lambda: __registered_templates
templatable_view.get_registered_template_views = lambda template: __registered_templates_views.get(template, [])
