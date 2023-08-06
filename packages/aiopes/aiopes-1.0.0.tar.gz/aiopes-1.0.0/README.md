##### Version 1 is not compatible with 0.1.0

# Index
- [Install](#install)
- [Example](#example)
- [Documentation](/docs/README.md)

# Install
- Pypi: ``pip3 install aiopes``
- Git: ``pip3 install git+https://github.com/WardPearce/aiopes.git``

# Example
```python
import asyncio
import aiopes


PES = aiopes.client(
    api_key="..."
)


async def example():
    try:
        async for data, server in PES.servers():
            print(data.id)
            server_target = server
    except aiopes.exceptions.InvalidAuthorization:
        print("Invalid API Key.")
    else:
        async for location in PES.locations():
            print(location.city)

        async for group in PES.mapgroups():
            print(group.name)

            for map_details in group.maps():
                print(map_details.name)

        print(await PES.mods())

        print(await PES.plugins())

        print(await PES.tickrates())

        async for gamemode in PES.gamemodes():
            print(gamemode.name)

        async for file in PES.files():
            print(file.name)

        if await PES.validate.settings(rcon="new_rcon"):
            print("Setting is valid")

loop = asyncio.get_event_loop()
loop.run_until_complete(example())
```