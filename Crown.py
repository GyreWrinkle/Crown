from captcha.image import ImageCaptcha
import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image
import io
import random
import string

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Streaming(name="/authenticate",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    print("Crown is ready.")

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Event", emoji="✨", style=discord.ButtonStyle.grey)
    async def menu1(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = discord.utils.get(interaction.user.guild.roles, id=1255932511360647238)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('The position has been removed. ❌', ephemeral=True)
        else:
            await interaction.response.send_message('The position has been given. ✅', ephemeral=True)
            await interaction.user.add_roles(role)

    @discord.ui.button(label="Giveaway", emoji="🎁", style=discord.ButtonStyle.grey)
    async def menu2(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = discord.utils.get(interaction.user.guild.roles, id=1255932075719135333)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('The position has been removed. ❌', ephemeral=True)
        else:
            await interaction.response.send_message('The position has been given. ✅', ephemeral=True)
            await interaction.user.add_roles(role)

    @discord.ui.button(label="Server Update", emoji="🔨", style=discord.ButtonStyle.grey)
    async def menu3(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = discord.utils.get(interaction.user.guild.roles, id=1255931994643103896)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message('The position has been removed. ❌', ephemeral=True)
        else:
            await interaction.response.send_message('The position has been given. ✅', ephemeral=True)
            await interaction.user.add_roles(role)


@bot.command()
@commands.has_permissions(administrator=True)
async def menu(ctx):
    view = Menu()

    embed = discord.Embed(title="Server Positions 📌", description="Please select your options for which server notifications you would like. If you would like to unselect an option, click again.", colour=discord.Colour.light_grey())
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/907377645493305455/1253775462153322587/Laurel_1.png?ex=667e5524&is=667d03a4&hm=24c635c6fa8df9c85a67f3eb4fa9a7f410a70267875020692d06b25d3f8e67ef&")
    await ctx.send(embed=embed, view=view)

@menu.error
async def menu_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    raise error
    

@bot.command()
async def authenticate(ctx):
    # Replace 'channel_id' with the ID of the channel where you want the command to work
    if ctx.channel.id != 1251680289420218490:
        return

    # Check if the user has no roles (excluding the @everyone role)
    if len(ctx.author.roles) == 1:
        # Generate a random CAPTCHA text
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # Generate a CAPTCHA image
        image = ImageCaptcha().generate_image(captcha_text)


        bot_message = await ctx.reply('Please check your direct messages for authentication.')
        await bot_message.delete(delay=8)
        await ctx.message.delete(delay=8)

        # Save the image to a BytesIO object
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)

            # Send the image to the user
            file = discord.File(output, 'captcha.png')
            embed = discord.Embed(title="Authenticate 🔒", description="Please utilise the image to answer the CAPTCHA. It must exactly match the image.", colour=discord.Colour.light_grey())
            embed.set_image(url="attachment://captcha.png")
            await ctx.author.send(embed=embed, file=file)

        # Wait for a message from the user
        def check(m):
            return m.author == ctx.author and m.guild is None

        message = await bot.wait_for('message', check=check)

        # Check if the message content matches the CAPTCHA text
        if message.content == captcha_text:
            role = discord.utils.get(ctx.guild.roles, id=1251676388230955079)  # Replace 'Role Name' with the name of the role you want to assign
            await ctx.author.add_roles(role)
            embed = discord.Embed(title="Welcome to Crown! 👋", description="You have been authenticated! 🔓\n\n**Guide** 📌\nBegin in <#1251671775495061524>!\nPurchase a service from us using ⁠<#1251951621651566662>.\nStart trading with ⁠<#1252358896627089428>.\nUse <#1251672663114514535> for discussion!", colour=discord.Colour.light_grey())
            await ctx.author.send(embed=embed)
        else:
            embed = discord.Embed(title="Unable to Authenticate 🔒", description="You were unable to authenticate your account. Please visit <#1251680289420218490> and request another CAPTCHA. If this persists, contact an administrator.", colour=discord.Colour.from_rgb(203,195,227))
            await ctx.author.send(embed=embed)
    else:
        embed = discord.Embed(title="Error ❌", description="Please do not use this command if you are already authenticated.", colour=discord.Colour.light_grey())
        await ctx.send(embed=embed, ephemeral=True)

@bot.tree.command(name="clear", description="Used for clearing a channel.")
@app_commands.describe(number = "Number of messages.")
@app_commands.describe(purpose = "Purpose for clearing the channel.")
@app_commands.checks.has_permissions(manage_messages=True)

async def clear(interaction: discord.Interaction, number: int, purpose: str):
    if number > 512:
        return await interaction.response.send_message("Failed. Please use a number that is less than 512.",ephemeral=True)

    await interaction.channel.purge(limit=number, reason=purpose)
    await interaction.response.send_message("Successful.", ephemeral=True)

bot.run("MTEwMzEwNDMzNjA3NjIyNjY2MQ.GPnOjg.Ke_cwRf2ThRkw-Yf0ofQZHrFt4WAHoTwXqrgMc")