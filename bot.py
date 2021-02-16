#Required libs
import discord
from discord.ext import commands
import r6sapi
import getpass

# list of all ops
opnamelist = ["aruni", "zero", "ace", "melusi", "oryx", "iana", "wamai", "kali", "amaru", "goyo", "nokk", "warden",
              "mozzie", "gridlock", "nomad", "kaid", "clash", "maverick", "maestro", "alibi", "lion", "finka", "vigil",
              "dokkaebi", "zofia", "ela", "ying", "lesion", "mira", "jackal", "hibana", "echo",
              "caveira", "capitao", "blackbeard", "valkyrie", "buck", "frost", "mute", "sledge", "smoke", "thatcher",
              "ash", "castle", "pulse", "thermite", "montagne", "twitch",
              "doc", "rook", "jager", "bandit", "blitz", "iq", "fuze", "glaz", "tachanka", "kapkan"]

# get uplay username and password for API
username = input("Username: ")
password = getpass.getpass('Password: ')

# get client object
bot = commands.Bot(command_prefix='!')

# stat lookup command
@bot.command(help="Looks up the stats for a player")
async def stat(ctx, arg):
    # TODO:add handler for null arg
    auth = r6sapi.Auth(username, password)
    player = await auth.get_player(arg, r6sapi.Platforms.UPLAY)
    await r6sapi.Player.load_general(player)
    await r6sapi.Player.load_queues(player)
    n = len(opnamelist)
    sorted_dict = {}
    PTdict = {}
    for i in range(n):
        operator = await player.get_operator(opnamelist[i])
        PTdict[operator.name] = operator.time_played

    sorted_keys = sorted(PTdict, key=PTdict.get)
    for w in sorted_keys:
        sorted_dict[w] = PTdict[w]
    j = len(sorted_keys)
    combine = sorted_keys[j - 1] + ', ' + sorted_keys[j - 2] + ', ' + sorted_keys[j - 3]
    region = r6sapi.RankedRegions.NA
    Rank = await player.get_rank(region)
    rankstats = player.ranked
    if rankstats.deaths == 0:
        rankkd = 0
    else:
        rankkd = (round((rankstats.kills / rankstats.deaths), 2))
    if player.deaths == 0:
        kd = 0
    else:
        kd = (round((player.kills / player.deaths), 2))
    mmr = Rank.mmr
    rankurl = Rank.get_icon_url()
    embed = discord.Embed(colour=discord.Colour(0xe75e15), description="Here are the stats for %s" % arg)
    staturlbase = "https://tabstats.com/siege/search/uplay/replace"
    newurl = staturlbase.replace('replace', arg)

    # embed here
    embed.set_thumbnail(url=rankurl)
    embed.set_author(name=arg, url=newurl)
    embed.add_field(name="Overall K/D", value=kd)
    embed.add_field(name="Ranked K/D", value=rankkd)
    embed.add_field(name="Top Operators", value=combine)
    embed.add_field(name="Current MMR", value=mmr)

    await ctx.send(embed=embed)
    await auth.close()


# Event Listener for when bot comes online
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


bot.run('insertcodehere')
