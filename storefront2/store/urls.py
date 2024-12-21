from django.urls import path
from . import views
#from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers       #using drf-nested-routers

router = routers.DefaultRouter()
router.register('products',viewset=views.ProductViewset,basename='products')
router.register('collections',viewset=views.CollectionViewset)
router.register('carts',viewset=views.CartViewset)

products_router = routers.NestedDefaultRouter(router,'products',lookup='product') 
products_router.register('reviews',views.ReviewViewset,basename='product-reviews')
cartitem_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cartitem_router.register('items',views.CartItemViewset,basename='cart-items')

urlpatterns = router.urls + products_router.urls + cartitem_router.urls

# URLConf
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
    
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>', views.CollectionDetail.as_view()),

# ]
