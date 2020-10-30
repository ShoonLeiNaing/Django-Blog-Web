from django.urls import path
from . import views

app_name="blog"
urlpatterns = [
    path('',views.PostListView.as_view(),name="post_list" ),
    path('create',views.PostCreateView.as_view(),name="post_create"),
    path('detail/<int:pk>',views.PostDetailView.as_view(),name="post_detail"),
    path('post_picture/<int:pk>',views.stream_file,name="post_picture"),
    path('comment/<int:pk>',views.CommentCreateView.as_view(),name="comment_create"),
    path('comment/<int:pk>/delete',views.CommentDeleteView.as_view(),name="comment_delete"),
    path('post/<int:pk>/favorite',views.AddFavoriteView.as_view(),name="post_favorite"),
    path('post/<int:pk>/unfavorite',views.DeleteFavoriteView.as_view(),name="post_unfavorite"),
]