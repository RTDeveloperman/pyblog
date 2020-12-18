from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.IndexPage.as_view(), name='index'),
    url(r'^contact/$',views.ContactPage.as_view(), name='contact'),
    url(r'^article/all/$',views.AllArticleAPIView.as_view(),name="all_articles"),
    url(r'^article/search/$',views.SearchArticlePIView.as_view(),name="search_articles"),
    url(r'^article/submit/$',views.SubmitArticlePIView.as_view(),name="submit_articles"),
    url(r'^article/update_cover/$',views.UpdateArticlePIView.as_view(),name="updatecover_articles"),
    url(r'^article/delete/$',views.DeleteArticlePIView.as_view(),name="delete_articles"),
    url(r'^article/$',views.SingleArticleAPIView.as_view(),name="single_article"),
]