import discord


attributions = {'Spectacular Settlements': 'Powered by [Spectacular Settlements](https://nordgamesllc.com/product/spectacular-settlements-pdf/) copyright © Nord Games LLC',
                'Ironsworn': 'This work is based on [Ironsworn](https://www.ironswornrpg.com/), created by Shawn Tomkin, and licensed for our use under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-nc-sa/4.0/).',
                'Starforged': 'This work is based on [Ironsworn: Starforged](https://www.ironswornrpg.com/), created by Shawn Tomkin, and licensed for our use under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-nc-sa/4.0/)'}
def GenerateAttributionEmbed():
    embed = discord.Embed(title='Attributions', description='The following products power DICE!!')
    for attribution in attributions:
        embed.add_field(name=attribution, value = attributions[attribution])
    return embed