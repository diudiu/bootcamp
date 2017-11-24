from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy

import markdown
from articles.forms import ArticleForm
from articles.models import Article, ArticleComment
from decorators import ajax_required


def _articles(request, articles):
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    try:
        article = paginator.page(page)

    except PageNotAnInteger:
        articles = paginator.page(1)

    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    popular_tags = Article.get_counted_tags()

    return render(request, 'articles/articles.html', {
        'articles': articles,
        'popular_tags': popular_tags
    })


class CreateArticle(LoginRequiredMixin, CreateView):
    template_name = 'articles/write.html'
    form_class = ArticleForm
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        return super(CreateArticle, self).form_invalid(form)


class EditArticle(LoginRequiredMixin, UpdateView):
    template_name = 'articles/edit.html'
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('articles')


@login_required
def articles(request):
    all_articles = Article.get_published()
    return _articles(request, all_articles)

@login_required
def article(request, slug):
    article = get_object_or_404(Article, slug=slug, status=Article.PUBLISHED)
    return render(request, 'articles/article.html', {'article': article})


@login_required
def tag(request, tag_name):
    articles = Article.objects.filter(tags__name=tag_name).filter(status="P")
    return _articles(request, articles)


@login_required
def drafts(request):
    drafts = Article.objects.filter(create_user=request.user,
                                    status=Article.DRAFT)
    return render(request, 'articles/drafts.html', {'drafts': drafts})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            html = "Nothing to display:("
            if len(content.strip()) > 0:
                html = markdown.markdown(content, safe_mode='escape')
            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()


