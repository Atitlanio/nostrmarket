import asyncio
from asyncio import Task
from typing import List

from fastapi import APIRouter
from starlette.staticfiles import StaticFiles

from lnbits.db import Database
from lnbits.helpers import template_renderer
from lnbits.tasks import catch_everything_and_restart

db = Database("ext_nostrmarket")

nostrmarket_ext: APIRouter = APIRouter(prefix="/nostrmarket", tags=["nostrmarket"])

nostrmarket_static_files = [
    {
        "path": "/nostrmarket/static",
        "app": StaticFiles(directory="lnbits/extensions/nostrmarket/static"),
        "name": "nostrmarket_static",
    }
]


def nostrmarket_renderer():
    return template_renderer(["lnbits/extensions/nostrmarket/templates"])


scheduled_tasks: List[Task] = []

from .tasks import subscribe_nostrclient, wait_for_nostr_events, wait_for_paid_invoices
from .views import *  # noqa
from .views_api import *  # noqa


def nostrmarket_start():
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(catch_everything_and_restart(wait_for_paid_invoices))
    task2 = loop.create_task(catch_everything_and_restart(subscribe_nostrclient))
    task3 = loop.create_task(catch_everything_and_restart(wait_for_nostr_events))
    scheduled_tasks.append([task1, task2, task3])
