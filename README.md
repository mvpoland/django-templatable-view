templatable_view decorator
==========================

This decorator is a simple, clean shortcut for not having to write the
very verbose render_to_respone code in Django.


Instead of this:

```python
def view(request):
    context = { }
    return render_to_response(template_name, context,  context_instance=RequestContext(request))
```

you can write:

```python
@templatable_view(template_name)
def view(request):
    return { }
```

When the templatable_view decorator detects that a normal HttpResponse object
has been returned, it won't touch it and pass it to the Django middleware.


Some other examples
-------------------


1. Defining a default dictionary. (Variables to be passed to the template,
   if the view doesn't return any of these.)

```python
@templatable_view('app/template.html', { 'param1': 4, 'param2': 5 })
def view(request):
    return { ... }
```

2. Returning a HttpResponse

```python
@templatable_view('app/template.html')
def view(request):
    if condition:
        return HttpResponseRedirect(reverse('home'))
    else
        return {'form': form }
```

3. Overriding the template in the view

```python
@templatable_view('app/template.html')
def view(request):
    if condition:
        return  { ... }
    else:
        return  'app/other-template.html', { ... }
```
