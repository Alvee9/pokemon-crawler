from platform import platform
import aiohttp
import asyncio
import requests
import platform

from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async

from pokemon_crawler.models import Pokemon


class Command(BaseCommand):
    api_url = "https://pokeapi.co/api/v2/pokemon/"

    def handle(self, *args, **options):
        response = requests.get(Command.api_url)
        pokemon_count = response.json()["count"]

        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.run_tasks(pokemon_count))
        self.stdout.write(self.style.SUCCESS("Pokemons caught!!"))

    # Async method to fetch Pokemon data from the API and save it to the DB
    async def get_and_insert(self, session, offset, limit):
        response = await session.get(Command.api_url + "?offset={}&limit={}".format(offset, limit), ssl=False)
        resp_json = await response.json()
        pokemons_list = resp_json["results"]
        for p in pokemons_list:
            response = await session.get(p["url"])
            pokemon = await response.json()
            await sync_to_async(Pokemon.objects.get_or_create)(
                name=pokemon["name"],
                weight=pokemon["weight"],
                height=pokemon["height"]
            )
        print("get_and_inserted done ", offset, limit)
        return

    def get_tasks(self, session, pokemon_count):
        tasks = []
        for offset in range(0, (pokemon_count // 50) * 50, 50):
            tasks.append(asyncio.create_task(self.get_and_insert(session, offset, 50)))
        
        return tasks

    async def run_tasks(self, pokemon_count):
        print("run tast started..")
        session = aiohttp.ClientSession()
        tasks = self.get_tasks(session, pokemon_count)
        await asyncio.gather(*tasks)
        print("asyncio gathered")
        await session.close()
        

