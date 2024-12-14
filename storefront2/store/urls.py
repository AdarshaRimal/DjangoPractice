from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter,DefaultRouter

router = DefaultRouter()
router.register('products',viewset=views.ProductViewset)
router.register('collections',viewset=views.CollectionViewset)


urlpatterns = router.urls

# URLConf
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
    
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>', views.CollectionDetail.as_view()),

# ]
