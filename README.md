# break-dice-bot
A Discord.py Bot that handles check and contest mechanics for the TTRPG BREAK!!,<br>
self-hosted by the user to enable uptime whenever they want.

### How to Host
If you want to run and host it for your own server, follow the next few steps.<br>
It is a bit technical and an in-depth explanation on setting up a Discord Bot won't be explained here.

<b>Requirements:</b>
<ul>
    <li>Python 3.x with the <code>discord.py</code> package</li>
    <li>Git</li>
    <li>A Discord Bot setup</li>
</ul>

<b>Links:</b>
<ul>
    <li>Python: https://www.python.org/downloads/</li>
    <li>Discord.py: https://pypi.org/project/discord.py/</li>
    <li>Git: https://git-scm.com/</li>
</ul>

<b>Steps:</b>
1. Run <code>git clone https://github.com/qu-gg/break-dice-bot.git </code> in the command line (cmd)
2. Add a file to the folder called <code>bot_token.py</code>
3. In that file, add the line <code>BOT_TOKEN = "XXX"</code> where XXX is your client secret key
4. Invite the bot with your bot link in the Discord Developer Portal.
5. Run the bot via <code>python main.py</code>

Example of an appropriate bot link, changing CLIENT_ID_HERE with the Client ID from the Discord Bot Portal: https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID_HERE&permissions=2048&scope=bot

### Command Examples
Check and Contest mechanics are provided out of the box, with parameters in Discord to set stats, edges, and bonuses.<br>
Technically, there is code for in-Discord visualization of all the player and area conditions, however given the 3rd Party License,
I cannot provide the .json files with their text. You can make your own .jsons (e.g. <code>conditions.json</code> and <code>battlefield.json</code>) and add them yourself if you'd like that functionality.

Check Mechanics:<br>
<img src="https://github.com/qu-gg/break-dice-bot/assets/32918812/892f2003-282b-47a3-a125-074e297b699e">

Contest Mechanics:<br>
<img src="https://github.com/qu-gg/break-dice-bot/assets/32918812/8fbd1c1a-ef05-4987-a05e-059336e9bb85">

Player Condition Visualization:<br>
<img src="https://github.com/qu-gg/break-dice-bot/assets/32918812/66d427b4-0e27-461c-828d-3b4ad395f0dc">
