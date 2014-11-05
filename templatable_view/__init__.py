# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template import loader
from django.template import RequestContext
from functools import wraps

# Remember which templates are actually in use.
__registered_templates = set()  # list of template names
__registered_templates_views = {} # mapping from template name to list of views.


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
            __registered_templates_views[path] = [view_func]


def templatable_view(default_template_name, default_context=None, render_func=False):
    """
    Creates a decorator which
     - Extracts the `context` and `template_name` params from the view.
     - Call the view without those parameters
     - Render the template. Use the default template if none was passed to the view.

    The `render_func` parameter is optional and can be used to customize the rendering procedure.
    it should look like:

    ::

        def render_func(request, template_name, context):
            pass

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
        def _view(request, *args, **kwargs):
            """
            Wrapper around the view
            """
            # Start from the default context and update this one every step
            context = default_context or {}

            # Pop decorator parameters
            context.update(kwargs.pop('context', {}))
            template_name = kwargs.pop('template_name', default_template_name)

            # Call original view function
            view_result = view_func(request, *args, **kwargs)

            def _render_func(request, template_name, context):
                context_instance = RequestContext(request)
                context_instance.update(context)
                result = loader.get_template(template_name).render(context_instance)
                return HttpResponse(result)
            render = render_func or _render_func

            if isinstance(view_result, dict):
                # and if the result was a dict, update context and render template
                context.update(view_result)
                return render(request, template_name, context)

            elif isinstance(view_result, tuple):
                # If the result was a tuple, it's like: (template_name_override, context)
                view_result_template, view_result_context = view_result
                context.update(view_result_context)
                return render(request, view_result_template, context)
            else:
                # otherwise, just return the HttpResponseRedirect or whatever the view returned
                return view_result

        return _view
    return decorator


templatable_view.get_registered_templates = lambda: __registered_templates
templatable_view.get_registered_template_views = lambda template: __registered_templates_views.get(template, [])
