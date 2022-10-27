from .views import home,get_blockchain, mine_block
from django.urls import path

urlpatterns = [
    path('',home,name="home"),
    path('blockchain',get_blockchain,name="blockchain"),
    path('blockchain/mine',mine_block,name="blockchain")
]
