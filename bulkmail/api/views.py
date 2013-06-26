from django import http
from django.core.context_processors import csrf

from ..shortcuts import render_tpl
from ..auth import super_admin_required

from .models import ApiKey, generate_key
from .forms import ApiKeyForm

@super_admin_required
def key_list (request):
  c = {
    'keys': ApiKey.query()
  }
  return render_tpl(request, 'api/key_list.html', c)
  
def key_add (request):
  return key_edit_view(request)
  
@super_admin_required
def key_edit_view (request, kid=None):
  instance = None
  verb = 'Add'
  form = ApiKeyForm(request.POST or None)
  
  if request.method == 'POST':
    if form.is_valid():
      akey = ApiKey(
        name=form.cleaned_data['name'],
        akey=generate_key(),
        created_by=request.user.user
      )
      akey.put()
      return http.HttpResponseRedirect('../')
      
  c = {
    'instance': instance,
    'verb': verb,
    'form': form,
  }
  c.update(csrf(request))
  
  return render_tpl(request, 'api/key_edit.html', c)
  