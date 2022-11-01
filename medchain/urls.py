

from .views import commit_wallet_transact, home,get_blockchain, mine_block, success,route_wallet_info,route_known_addresses,route_unmined_transactions,transaction_success
from django.urls import path
urlpatterns = [
    path('',home,name="home"),
    path('blockchain',get_blockchain,name="blockchain"),
    path('blockchain/mine',mine_block,name="mine"),
    path('blockchain/transaction',commit_wallet_transact,name="commit_wallet_transact"),
    path('blockchain/transaction/success',transaction_success,name="transaction_success"),
    path('blockchain/wallet/info',route_wallet_info,name="route_wallet_info"),
    path('blockchain/wallet/known',route_known_addresses,name="route_known_addresses"),
    path('blockchain/transaction/pool',route_unmined_transactions,name="route_transactions"),
]
