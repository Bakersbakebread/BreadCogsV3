from typing import Optional

import aiohttp
import discord
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class CheckEndpointResponseModel:
    bad_domain: bool
    detection: Optional[str] = None

    def to_report_embed(self, message: discord.Message) -> discord.Embed:
        embed = discord.Embed()

        embed.set_author(
            name=f"{message.author} - {message.author.id}",
            icon_url=message.author.avatar_url
        )
        embed.add_field(
            inline=False,
            name="Message",
            value=f"{message.clean_content}\n\n"
        )
        embed.add_field(
            name="Unsure domain",
            value="This domain has been flagged as a potential risk. "
                  "Click the button below to report the domain as bad, if not just ignore."
        )

        return embed


class Api:
    def __init__(self):
        self.base_url = "https://bad-domains.walshy.dev"
        self.check_path = "/check"
        self.report_path = "/report"

    async def check(self, domain_to_check: str):
        """
        Posts to the check_path which will return CheckEndpointResponseModel

        Parameters
        ----------
        domain_to_check: The domain to check if is in list

        Returns
        -------
        CheckEndpointResponseModel
        """

        check_url = self.base_url + self.check_path
        json = {"domain": domain_to_check}
        async with aiohttp.ClientSession() as session:
            async with session.post(check_url, json=json) as resp:
                json_response = await resp.json()
                response_model = CheckEndpointResponseModel.from_dict(json_response)

        return response_model

    async def report(self, domain_to_report: str):

        report_url = self.base_url + self.report_path
        json = {"domain": domain_to_report}

        async with aiohttp.ClientSession() as session:
            async with session.post(report_url, json=json) as resp:
                json_response = await resp.json()
