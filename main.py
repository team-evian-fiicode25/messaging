#!/usr/bin/env python3

import asyncio
import os
import sys
from typing import AsyncIterator
from graphql_client import Client
from graphql_client.login_created import LoginCreated
from graphql_client.email_verification_requested import EmailVerificationRequested
from graphql_client.phone_verification_requested import PhoneVerificationRequested

async def main():
    client = Client(
        ws_url=get_service_url()
    )

    tasks = [
        handle_login_created(client.login_created()),
        handle_email_verification(client.email_verification_requested()),
        handle_phone_verification(client.phone_verification_requested()),
    ]

    tasks = [asyncio.create_task(t) for t in tasks]

    for task in tasks:
        await task


async def handle_login_created(subscription: AsyncIterator[LoginCreated]):
    async for res in subscription:
        print(res)


async def handle_email_verification(subscription: AsyncIterator[EmailVerificationRequested]):
    async for res in subscription:
        print(res)


async def handle_phone_verification(subscription: AsyncIterator[PhoneVerificationRequested]):
    async for res in subscription:
        print(res)


def get_service_url():
    try:
        return os.environ["AUTH_URL"]
    except KeyError:
        print("Missing required env variable: AUTH_URL", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
