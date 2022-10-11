import asyncio
import contextlib
import importlib

import naff

import common.models as models
import common.utils as utils


class RealmsPremiumWatch(utils.Extension):
    def __init__(self, bot: utils.AGBotBase):
        self.name = "Realms Playerlist Premium Watch"
        self.bot: utils.AGBotBase = bot
        self.premium_role: naff.Role = None  # type: ignore

        asyncio.create_task(self.async_init())

    async def async_init(self):
        await self.bot.fully_ready.wait()
        self.premium_role = await self.bot.guild.fetch_role(1007868499772846081)  # type: ignore

    @naff.listen()
    async def on_member_update(self, event: naff.events.MemberUpdate):
        if not self.premium_role:
            return

        if event.before._role_ids == event.after._role_ids:
            return

        if event.before.has_role(self.premium_role) and not event.after.has_role(
            self.premium_role
        ):
            await models.PremiumCode.filter(user_id=int(event.before.id)).delete()

        elif not event.before.has_role(self.premium_role) and event.after.has_role(
            self.premium_role
        ):
            with contextlib.suppress(naff.errors.HTTPException):
                await event.after.send(
                    "Hey! Thank you for donating and getting Realms Playerlist"
                    " Premium!\n\nTo get your Premium code, check out"
                    " <#1029164782617632768> and open a ticket. Astrea will be able to"
                    " give your code from there."
                )

    @naff.listen()
    async def on_member_remove(self, event: naff.events.MemberRemove):
        if not self.premium_role:
            return

        if not isinstance(event.member, naff.Member) or event.member.has_role(
            self.premium_role
        ):
            await models.PremiumCode.filter(user_id=int(event.member.id)).delete()


def setup(bot):
    importlib.reload(utils)
    RealmsPremiumWatch(bot)
