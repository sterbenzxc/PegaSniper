import discord
import json
import requests
from discord.ext import tasks

with open('variables.json') as f:
        env_vars = json.load(f)

client = discord.Client()

def updatelist(new_data, filename='listings.json'):
    with open(filename, 'w') as json_file:
      json.dump(new_data, json_file, 
                        indent=2,  
                        separators=(',',': '))

@tasks.loop(seconds=30)
async def pegasnipe():
  with open('listings.json') as fp:
        listObj = json.load(fp)
  printed = []
  for x in listObj:
    values_view = x.values()
    value_iterator = iter(values_view)
    id = next(value_iterator)
    printed.append(id)
  channel = client.get_channel(958256615994322954)
  channel2 = client.get_channel(953958278608584704)
  channel3 = client.get_channel(958275953631567933)
  response1 = requests.get("https://api-apollo.pegaxy.io/v1/pegas/prices/floor?maxBreedCount=" + str(env_vars['BREEDCOUNT']) + "&minBreedCount=0&breedCountFilter=0," + str(env_vars['BREEDCOUNT']) + "&breedType=" + str(env_vars['breedType']))
  json_data1 = json.loads(response1.text)

  for x in json_data1:
    if str(x["listingIds"][0]) not in printed:
      response = requests.get("https://api-apollo.pegaxy.io/v1/pegas/" + str(x["pegaIds"][0]))
      json_data = json.loads(response.text)
      totalstats = float(json_data['speed']) + float(json_data['strength']) + float(json_data['wind']) + float(json_data['fire']) + float(json_data['water']) + float(json_data['lightning'])
      if(totalstats >= int(env_vars['stats'])):
        listObj.append({"id": str(x["listingIds"][0]) })
        embed=discord.Embed(
        title="**Snipe this PEGA**",
            url="",
            description="",
            color=discord.Color.blue())
        embed.add_field(name="**Pega ID**", value=str(x["pegaIds"][0]), inline=False)
        embed.add_field(name="**Blood Line**", value=str(x["bloodLine"]), inline=False)
        embed.add_field(name="**Total Stats**", value=str(totalstats), inline=False)
        embed.add_field(name="**Marketplace link**", value="https://play.pegaxy.io/marketplace/listing/" + str(x["listingIds"][0]), inline=False)
        embed.set_footer(text="Created By: Renzxc#6896")
        await channel.send(embed=embed)
        await channel2.send(embed=embed)
        await channel3.send(embed=embed)
  updatelist(listObj)

@client.event
async def on_ready():
  pegasnipe.start()

my_secret = env_vars['TOKEN']
client.run(my_secret)