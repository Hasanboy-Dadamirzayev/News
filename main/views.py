from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *
from django.http import HttpResponse


class HomeView(View):
    def get(self, request):
        articles = Article.publisheds.order_by('-important', '-view')
        top_article = Article.publisheds.order_by('-view')[:2]
        latest_news = Article.publisheds.order_by('view')[:1]
        news = Article.publisheds.order_by('-created_at')
        context = {
            'articles': articles,
            'top_article': top_article,
            'latest_news': latest_news,
            'news': news,
        }
        return render(request, 'index.html', context)


class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)


        related_articles = Article.publisheds.filter(
            category=article.category
        ).exclude(id=article.id)[:5]


        comments = article.article_comments.filter(published=True)

        articles = Article.objects.all()

        context = {
            'article': article,
            'related_articles': related_articles,
            'comments': comments,
            'articles': articles,
        }
        return render(request, 'detail-page.html', context)

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        Comment.objects.create(
            name=request.POST.get('name'),
            text=request.POST.get('text'),
            email=request.POST.get('email'),
            article=article,
            published=True
        )
        return self.get(request, slug)

class Page404View(View):
    def get(self, request):
        return render(request, '404.html')

class CategoryArticleView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        artciles = Article.objects.filter(category=category)
        categories = Category.objects.all()
        context = {
            'category': category,
            'articles': artciles,
            'categories': categories,
        }
        return render(request, 'category_article.html', context)


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')


    def post(self, request):
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        return HttpResponse("""
            <!DOCTYPE html>
            <html lang="uz">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Xabar yuborildi</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    body {
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    }
                    .success-card {
                        background: white;
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                        padding: 40px;
                        max-width: 600px;
                        width: 100%;
                        text-align: center;
                        animation: fadeIn 0.5s ease-out;
                    }
                    .success-icon {
                        color: #28a745;
                        font-size: 5rem;
                        margin-bottom: 20px;
                        animation: bounce 1s infinite alternate;
                    }
                    .btn-home {
                        background: #007bff;
                        color: white;
                        padding: 10px 25px;
                        border-radius: 50px;
                        text-decoration: none;
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        transition: all 0.3s ease;
                        margin-top: 20px;
                    }
                    .btn-home:hover {
                        background: #0069d9;
                        transform: translateY(-3px);
                        box-shadow: 0 5px 15px rgba(0, 123, 255, 0.3);
                    }
                    @keyframes fadeIn {
                        from { opacity: 0; transform: translateY(20px); }
                        to { opacity: 1; transform: translateY(0); }
                    }
                    @keyframes bounce {
                        from { transform: translateY(0); }
                        to { transform: translateY(-10px); }
                    }
                </style>
            </head>
            <body>
                <div class="success-card">
                    <div class="success-icon">
                        <i class="fas fa-check-circle"></i>
                    </div>
                    <h1 class="mb-3">Xabaringiz muvaffaqiyatli yuborildi!</h1>
                    <p class="lead mb-4">Tez orada siz bilan bog'lanamiz. E'tiboringiz uchun rahmat!</p>
                    <a href="/" class="btn-home">
                        <i class="fas fa-home"></i> Bosh sahifaga qaytish
                    </a>
                </div>
            </body>
            </html>
            """)
