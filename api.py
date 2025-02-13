import asyncio
from autogenstudio.teammanager import TeamManager

async def main():
    manager = TeamManager()

    response = await manager.run(
        team_config="team.json",
        task=" write a story about a goblin who ascend to godhood."
    )

    print(response)

asyncio.run(main())