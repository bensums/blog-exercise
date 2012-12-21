import logging

from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.http import HttpResponse, HttpResponseForbidden, \
    HttpResponseRedirect

from blog.models import BlogPost

from google.appengine.api import users
from google.appengine.ext import db

import string
import random

class BlogIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(BlogIndex, self).get_context_data(**kwargs)
        # Latest 10 posts.
        context['posts'] = BlogPost.all().order('-date').fetch(10)
        return context

class HelloWorld(TemplateView):
    template_name = "hello-world.html"
    
    def get_context_data(self, **kwargs):
        context = super(HelloWorld, self).get_context_data(**kwargs)        
        context['message'] = 'Hooray! Everything seems to work...'
        return context

def blog_key(blog_name=None):
    return db.Key.from_path('Blog', blog_name or 'nobody')

@db.transactional
def insert_post_with_unique_key(post_dict):
    """
    First we try to post the blog entry with key <author>-<slug of post title>.
    If this key is already taken we append a random two characters and repeat
    until a free key is generated. The blog post is then saved with this new
    key.

    In all queries we specify the parent as the blog with name the author's
    nickname. This means that all queries run on a single entity group so we
    don't have to use a cross-group transaction. Also this means two users can
    be posting at the same time as the transaction only locks the entity group
    corresponding to the current logged in user.
    """
    key_name_base = unicode(slugify(post_dict['title']))
    key_name = key_name_base
    parent_key = blog_key(post_dict['author'])
    while BlogPost.get_by_key_name(key_name, parent=parent_key):
        key_name = '%s-%s' % (key_name_base, ''.join([random.choice(
            string.ascii_letters + string.digits) for i in range(2)]))
    post = BlogPost(parent=parent_key, key_name=key_name, **post_dict)
    post.put()
    return post

def new_post(request):
    if request.method == 'POST':
        user = users.get_current_user()
        if not user:
            return HttpResponseForbidden()
        post_dict = {
            'title': request.POST['title'] or '(no title)',
            'author': user.nickname(),
            'content': request.POST['content'] or '(no content)'
        }
        try:
            insert_post_with_unique_key(post_dict)
            return HttpResponseRedirect('/')
        # This is probably a bad idea because the exception could reveal
        # sensitive information to the user.
        except Exception, e:
            context = {
                'post': post_dict,
                'errors': e
            }
    else:
        context = {}
    return render_to_response('post_form.html', context, RequestContext(request))

def post_detail(request, blog_name=None, post_key_name=None):
    post = BlogPost.get_by_key_name(post_key_name,
                                    parent=db.Key.from_path('Blog', blog_name))
    if not post:
        return HttpResponse404()
    return render_to_response('post_detail.html', {'post': post},
                              RequestContext(request))

def exception_test(request):
    logging.debug('Debug log')
    logging.warn('Warn log')
    logging.error('Error log')
    raise Exception()
    


    
