import logging

from django.views.generic import TemplateView
from django.conf import settings


class HelloWorld(TemplateView):
    template_name = "hello-world.html"
    
    def get_context_data(self, **kwargs):
        context = super(HelloWorld, self).get_context_data(**kwargs)        
        context['message'] = 'Hooray! Everything seems to work...'
        return context


def exception_test(request):
    logging.debug('Debug log')
    logging.warn('Warn log')
    logging.error('Error log')
    raise Exception()
    


    
