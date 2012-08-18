from django.template import Library

register = Library()


@register.inclusion_tag("includes/bootstrap_form.html", takes_context=True)
def bootstrap_form(context, form):
    context.update({
        "form": form,
    })
    return context