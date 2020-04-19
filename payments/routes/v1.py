from typing import List

from fastapi import APIRouter

from controllers.token import token_create
from controllers.transfer import transfer_create, transfer_list
from controllers.user import user_create, user_get
from controllers.wallet import wallet_list
from views.token import TokenView
from views.transfer import TransferView
from views.user import UserView
from views.wallet import WalletView

router = APIRouter()

router.add_api_route(
    '/token',
    token_create,
    tags=['token'],
    methods=['POST'],
    response_model=TokenView,
)

router.add_api_route(
    '/user',
    user_create,
    tags=['user'],
    methods=['POST'],
    response_model=UserView,
)
router.add_api_route(
    '/user/me',
    user_get,
    tags=['user'],
    methods=['GET'],
    response_model=UserView,
)

router.add_api_route(
    '/wallet',
    wallet_list,
    tags=['wallet'],
    methods=['GET'],
    response_model=List[WalletView],
)

router.add_api_route(
    '/transfer',
    transfer_create,
    tags=['transfer'],
    methods=['POST'],
    response_model=TransferView,
)
router.add_api_route(
    '/transfer',
    transfer_list,
    tags=['transfer'],
    methods=['GET'],
    response_model=List[TransferView],
)
