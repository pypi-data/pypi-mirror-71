# -*- coding: utf-8 -*-
# flake8: noqa

"""
MIT License

Copyright (c) 2019-2020 Terbau

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '2.0.7'

import asyncio
from sys import platform, version_info

from .client import Client, run_multiple, start_multiple, close_multiple
from .auth import (Auth, EmailAndPasswordAuth, ExchangeCodeAuth,
                   AuthorizationCodeAuth, DeviceAuth, RefreshTokenAuth,
                   AdvancedAuth)
from .friend import Friend, PendingFriend
from .message import FriendMessage, PartyMessage
from .party import (DefaultPartyConfig, DefaultPartyMemberConfig, PartyMember,
                    ClientPartyMember, JustChattingClientPartyMember, Party, 
                    ClientParty, ReceivedPartyInvitation, SentPartyInvitation,
                    PartyJoinConfirmation)
from .presence import Presence, PresenceGameplayStats, PresenceParty
from .user import (ClientUser, User, BlockedUser, ExternalAuth,
                   ProfileSearchEntryUser, SacSearchEntryUser)
from .stats import StatsV2
from .enums import *
from .errors import *
from .store import Store, FeaturedStoreItem, DailyStoreItem
from .news import BattleRoyaleNewsPost
from .playlist import Playlist
from .kairos import Avatar

# fix for python 3.8
loop = asyncio._get_running_loop()
if loop is not None:
    if isinstance(asyncio.get_event_loop_policy(), asyncio.WindowsProactorEventLoopPolicy):
        raise RuntimeError(
            'Incompatible event loop running. Read more here: '
            'https://fortnitepy.readthedocs.io/en/latest/faq.html#python-3-8-why-does-other-asynchronous-libraries-suddenly-break-when-using-fortnitepy'
        )

if platform == 'win32' and version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
