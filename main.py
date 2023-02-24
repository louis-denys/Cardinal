import interactions
#import discord
from interactions import ActionRow, Button
from data import token
from random import randint
import asyncio
from fonction_sql import *
import sqlite3
import os


### EDIT A FAIRE ###
# Modifier l'id de la guild et du rôle everyone 


bot = interactions.Client(token=os.read["DISCORD_TOKEN"], intents=interactions.Intents.ALL, presence=interactions.ClientPresence(
    status=interactions.StatusType.ONLINE, activities = [ interactions.PresenceActivity(
        name= "Régir l'humanité.", 
        type=interactions. PresenceActivityType.GAME
)]))

guild_id = 1071867748805775500
everyone_id = 1071867748805775500
"""
Note:
On pour généraliser les commandes, il faut supprimer le paramettre scope= des commandes,
automatiquement la commande sera déployé (environs 1h d'attente)

@bot.command(
    name= '',
    description= '', 
    scope=guild_id,
    options = [
        interactions.Option(
            name='',
            description= '', 
            type = interactions.OptionType.STRING,
            required = True
        )
    ] 
)
"""

### RP ###

# Carte 
@bot.command(
        name = 'carte',
        description = 'La carte du monde mais manque le nom mdr',
        scope=guild_id
)
async def carte(ctx: interactions.CommandContext):
    await ctx.send(embeds =
        interactions.Embed(
            title = 'Carte de Ryudh',
            color = 221932,
            image = interactions.EmbedImageStruct(
                url = "https://media.discordapp.net/attachments/1071869565757308938/1073336423597481994/Train_1.jpg?width=745&height=559"
            )
        )
    )

# Roll
@bot.command(
        name = 'roll',
        description = 'nombre aléatoire',
        scope=guild_id,
        options = [
            interactions.Option(
                name="max",
                description="le maximum obtenable au lancé de dés",
                type= interactions.OptionType.INTEGER,    #Le type d'entrée
                required=True,                          #Si elle est obligatoire.
            ),
        ]
)
async def roll(ctx: interactions.CommandContext, max:str):
    await ctx.send(f"{ctx.user.mention} vient de tirer un: {randint(0, max)} :game_die: !")

#Plan
@bot.command(
        name = 'plan',
        description = 'déchainez votre psychisme et libérez votre plan',
        scope = guild_id,
        options=[
            interactions.Option(
                name = 'nom',
                description = 'Le nom de votre plan',
                type = interactions.OptionType.STRING,
                required = True
            )
        ]
)
async def plan (ctx: interactions.CommandContext, nom):
    await ctx.send('**Vous déchainez votre volonté et votre maitrise du Shinjian pour ouvrir un plan.** \nhttps://tenor.com/view/raiden-shogun-baal-genshin-impact-raiden-ei-euthymia-gif-23060356')
    salon = await ctx.get_channel()
    if salon.name.startswith('Plan euthémique de'):
        await ctx.send("**Votre pouvoir se déchaine au sein d'un plan déjà existant, votre volonté est désormais la seul limite à ce monde.** ")
    else:
        fil = await salon.create_thread(name = f'Plan euthémique de {nom}')
        await fil.send(f'**Bienvenue dans votre plan euthémique {ctx.user.mention} .**')

### MODERATION ###

# Ban
@bot.command(
    name= 'ban',
    description= 'reduire a néant un membre de la surface du serveur', 
    scope=guild_id,
    default_member_permissions=interactions.Permissions.BAN_MEMBERS,
    options = [
        interactions.Option(
            name='utilisateur',
            description= "mention de l'utilisateur à bannir", 
            type = interactions.OptionType.USER,
            required = True
        ),
        interactions.Option(
            name='raison',
            description= 'raison du bannissement', 
            type = interactions.OptionType.STRING,
            required = False
        )
    ] 
)
async def ban(ctx : interactions.CommandContext, utilisateur, raison : str = ''):
    """
    J'ai aucune idée de comment cette connerie marche,
    J'arrive pas à faire en sorte que ça suprime les messages c'est frustrant ><
    """
    await utilisateur.ban(guild_id = ctx.guild_id, reason = raison )
    await ctx.send(f'{utilisateur.mention} a été rayé de la surface du serveur. \n https://tenor.com/bGns7.gif')


# Kick

@bot.command(
    name= 'kick',
    description= 'reduire a néant un membre de la surface du serveur', 
    scope=guild_id,
    default_member_permissions=interactions.Permissions.KICK_MEMBERS,
    options = [
        interactions.Option(
            name='utilisateur',
            description= "mention de l'utilisateur à expulser", 
            type = interactions.OptionType.USER,
            required = True
        ),
    ] 
)
async def kick(ctx : interactions.CommandContext, utilisateur, raison : str = ''):
    await utilisateur.kick(guild_id = ctx.guild_id)
    await ctx.send(f'{utilisateur.mention} à été expulsé du serveur.')

# Mute


# Warn
@bot.command(
    name = 'warn',
    description='Avertir un membre',
    scope=guild_id,
    default_member_permissions=interactions.Permissions.MANAGE_MESSAGES,
    options= [
        interactions.Option(
            name = 'utilisateur',
            description= "mention de l'utilisateur à avertir",
            type = interactions.OptionType.USER, 
            required= True
        ),
    ]
)
async def warn(ctx: interactions.CommandContext, utilisateur):
    if look_in_bdd(utilisateur.id) == []:
        add_to_bdd(utilisateur.id, 0, 0)
        
    membre = look_in_bdd(utilisateur.id)
    maj_warn(id = utilisateur.id, warn = membre[0][1]+1)
    await ctx.send(f"{utilisateur.mention} à été avertis.")
    if membre [0][1] >= 3:
        await utilisateur.ban(guild_id = ctx.guild_id, reason = f'3 avertissement atteint' )
        await ctx.send(f"{utilisateur.mention} à subit 3 avertissement et à été bannis.")
        maj_warn(id = utilisateur.id, warn = 0)

# Unwarn
@bot.command(
    name = 'unwarn',
    description='Avertir un membre',
    scope=guild_id,
    default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    options= [
        interactions.Option(
            name = 'utilisateur',
            description= "mention de l'utilisateur à unwarn",
            type = interactions.OptionType.USER, 
            required= True
        ),
    ]
)
async def unwarn(ctx: interactions.CommandContext, utilisateur):
    membre = look_in_bdd(utilisateur.id)
    if look_in_bdd(utilisateur.id) == []:
        await ctx.send("L'utilisateur n'a jamais était subit d'avertissement.")
    elif membre[0][1] == 0:
        await ctx.send("L'utilisateur à 0 avertissment.")
    else:
        maj_warn(id = utilisateur.id, warn = membre[0][1]-1)
        await ctx.send(f"{utilisateur.mention} à maintenant {membre[0][1]-1} avertissement.")




### ASSISTANCE ###

# Tickets
open_ticket_buttun = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="🎫| Nouveau Ticket",
    custom_id="ticket"
)

close_ticket_buttun = interactions.Button(
    style= interactions.ButtonStyle.DANGER,
    label= "❌| Fermer le ticket",
    custom_id= "fermer"
)

@bot.component("ticket")
async def button_response(ctx: interactions.CommandContext):
    serveur = await ctx.get_guild()
    salon = await serveur.create_channel(name = f'ticket de {ctx.user.username}', parent_id=1071867749866942496, type= interactions.ChannelType.GUILD_TEXT)
    await ctx.send(f"Votre ticket à été créé: {salon.mention}", ephemeral=True)
    message = await salon.send(embeds = interactions.Embed(
        title = 'Bienvenue dans le ticket',
        color = 221932,
        description = f'Ticket de {ctx.user.mention}'
    ), components=close_ticket_buttun)

    #Permissions du salons:
    await salon.add_permission_overwrite(id = ctx.user.id, type = '1', allow = interactions.Permissions.VIEW_CHANNEL)
    await salon.add_permission_overwrite(id = everyone_id, type = '0', deny = interactions.Permissions.VIEW_CHANNEL)
    #await salon.pin_message(message_id=message.id)

@bot.component('fermer')
async def supr_ticket(ctx: interactions.CommandContext):
    await ctx.send('Le ticket est fermé et le salon sera suprimé dans 5s.')
    await asyncio.sleep(5)
    await ctx.channel.delete()

@bot.command(
    name= 'admin_ticket',
    description= 'envoyer un embed pour générer des tickets', 
    default_member_permissions= interactions.Permissions.ADMINISTRATOR,
    options = [
        interactions.Option(
            name='message',
            description= "message decrivant l'utilisation des tickets", 
            type = interactions.OptionType.STRING,
            required = True
        )
    ],
    scope=guild_id
)
async def tickets(ctx, message):
    await ctx.send(embeds = interactions.Embed(
        title = f'{message}',
        color = 221932,
        description = 'Clique ci-dessous pour ouvrir un ticket !',
    ), components=open_ticket_buttun)

#Auto rôles
Il = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="💙| Il",
    custom_id="Il"
)

@bot.component('Il')
async def il(ctx: interactions.CommandContext):
    member = ctx.member
    present = False
    role = await interactions.get(bot, interactions.Role, guild_id=guild_id, object_id=1075124943232172123)
    for i in member.roles:
        if i == 1075124943232172123:
            present = True
    if not present:
        await member.add_role(role)
        await ctx.send(f"Vous avez obtenue le rôle {role.mention} !", ephemeral=True)
    else:
        await member.remove_role(role= role)
        await ctx.send("Le rôle a été retiré !", ephemeral=True)


Elle = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="❤️| Elle",
    custom_id="Elle"
)

@bot.component('Elle')
async def elle(ctx: interactions.CommandContext):
    member = ctx.member
    present = False
    role = await interactions.get(bot, interactions.Role, guild_id=guild_id, object_id=1075125015978184758)
    for i in member.roles:
        if i == 1075125015978184758:
            present = True
    if not present:
        await member.add_role(role)
        await ctx.send(f"Vous avez obtenue le rôle {role.mention} !", ephemeral=True)
    else:
        await member.remove_role(role= role)
        await ctx.send("Le rôle a été retiré !", ephemeral=True)


Iel = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="💛| Iel",
    custom_id="Iel"
)

@bot.component('Iel')
async def iel(ctx: interactions.CommandContext):
    member = ctx.member
    present = False
    role = await interactions.get(bot, interactions.Role, guild_id=guild_id, object_id=1075125083351302154)
    for i in member.roles:
        if i == 1075125083351302154:
            present = True
    if not present:
        await member.add_role(role)
        await ctx.send(f"Vous avez obtenue le rôle {role.mention} !", ephemeral=True)
    else:
        await member.remove_role(role= role)
        await ctx.send("Le rôle a été retiré !", ephemeral=True)

spectate = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="👀| Spéctateur",
    custom_id="spec"
)

    
@bot.component('spec')
async def spec(ctx: interactions.CommandContext):
    member = ctx.member
    present = False
    role = await interactions.get(bot, interactions.Role, guild_id=guild_id, object_id=1075139115386933368)
    for i in member.roles:
        if i == 1075139115386933368:
            present = True
    if not present:
        await member.add_role(role)
        await ctx.send(f"Vous avez obtenue le rôle {role.mention} !", ephemeral=True)
    else:
        await member.remove_role(role= role)
        await ctx.send("Le rôle a été retiré !", ephemeral=True)


row = interactions.spread_to_rows(Il, Elle, Iel)

@bot.command(
    name= 'genre',
    description= 'roles de genre', 
    default_member_permissions= interactions.Permissions.ADMINISTRATOR,
    scope=guild_id
)
async def genre(ctx):
    await ctx.send(embeds = interactions.Embed(
        title = 'Genre',
        color = 221932,
        description = 'Choisissez quel pronom vous correspond le plus !',
    ), components=row)

@bot.command(
    name= 'spec',
    description= 'roles de spec', 
    default_member_permissions= interactions.Permissions.ADMINISTRATOR,
    scope=guild_id
)
async def spec(ctx):
    await ctx.send(embeds = interactions.Embed(
        title = 'Spéctateur',
        color = 221932,
        description = 'Cliquez ici pour acceder au rp en tant que spéctateur !',
    ), components=spectate)

# Règlement !
check = interactions.Button(
    style=interactions.ButtonStyle.SUCCESS,
    label="✅| Valider le règlement !",
    custom_id="Valid"
)
@bot.component('Valid')
async def spec(ctx: interactions.CommandContext):
    member = ctx.member
    present = False
    role = await interactions.get(bot, interactions.Role, guild_id=guild_id, object_id=1071867748868698218)
    for i in member.roles:
        if i == 1071867748868698218:
            present = True
    if not present:
        await member.add_role(role)
        await ctx.send(f"Vous avez obtenue le rôle {role.mention} ! Bienvenue sur le serveur ;)", ephemeral=True)
    else:
        await member.remove_role(role= role)
        await ctx.send("Sans le rôle, vous ne pouvez plus acceder au serveur :/", ephemeral=True)

@bot.command(
    name= 'admin_reglement',
    description= 'acces serveur', 
    default_member_permissions= interactions.Permissions.ADMINISTRATOR,
    scope=guild_id
)
async def admin_reglement(ctx):
    await ctx.send(embeds = interactions.Embed(
        title = 'Valider le Règlement ✨',
        color = 221932,
        description = 'Cliquez ici pour confirmer avoir lu et accepter le règlement !',
    ), components=check)


#Clear
@bot.command(
        name = 'clear',
        description= 'Supprimer X messages',
        scope = guild_id,
        default_member_permissions = interactions.Permissions.MANAGE_MESSAGES,
        options= [
            interactions.Option(
                name = 'nombre',
                description = 'Nombre de message à supprimer',
                type = interactions.OptionType.INTEGER,
                required= True
            )
        ]
)
async def clear(ctx: interactions.CommandContext, nombre):
    channel = await ctx.get_channel()
    await channel.purge(nombre)
    message = await ctx.send(f"{nombre} messages ont été supprimé !")
    await asyncio.sleep(2)
    await message.delete()

# Aide
@bot.command(
    name = 'help',
    description= 'liste des commandes',
    scope = guild_id
)
async def help(ctx):
    await ctx.send(embeds = interactions.Embed(
        title = 'Système Cardinal',
        color = 221932,
        fields = [
            interactions.EmbedField(
            name="/Carte",
            value="Affiche la carte du monde.",
            inline=False,
                    ),
            interactions.EmbedField(
            name="/roll `max:`",
            value="Choisit un nombre aléatoire entre 0 et `max`.",
            inline=False,
                    ),
            interactions.EmbedField(
            name="/kick `utilisateur` ",
            value="Expluse un membre du serveur.",
            inline=False,
                    ),
            interactions.EmbedField(
            name="/ban `utilisateur` `raison:`",
            value="Bannis un membre du serveur en spécifiant sa `raison` (optionnel)",
            inline=False,
                    ),
            interactions.EmbedField(
            name="Warn `utilisateur`",
            value="Avertis un utilisateur, 3 warn = Ban",
            inline=False,
                    ),
            interactions.EmbedField(
            name="Unwarn `utilisateur`",
            value="Retire un avertissement",
            inline=False,
                    ),
            interactions.EmbedField(
            name="/Rank",
            value="Affiche le classement du serveur.",
            inline=False,
                    ),
            interactions.EmbedField(
            name="/Clear `nb_message`",
            value="Supprime un certain nombre de messages parmis les derniers messages du salon.",
            inline=False,
                    ),
            interactions.EmbedField(
            name="/Plan `Nom_Du_Plan:`",
            value="Permet d'interragir dans le RP pour ouvrir un plan.",
            inline=False,
                    )
        ]
    ))
### FUN ###


### EVENT ###
@bot.event
async def on_ready():
    print('Le bot est connecté !')

@bot.event
async def on_guild_member_add(member):
    try:
        add_to_bdd(member.id, 0, 0)
    except:
        print('Membre déjà enregistré.')
    channel = await interactions.get(bot, interactions.Channel, object_id=1071867749866942499)  #ID du salon
    stat = await interactions.get(bot, interactions.Channel, object_id=1071867749527195649)
    serveur = await interactions.get(bot, interactions.Guild, object_id=member.guild_id)
    await stat.modify(name=f"🔱•Members: {serveur.member_count}")
    await channel.send(f"Salut {member.mention} ! Bienvenue sur le serveur !")

@bot.event
async def on_guild_member_remove(member):
    #await member.add_role(1037771838387916874)
    channel = await interactions.get(bot, interactions.Channel, object_id=1071867749866942499)  #ID du salon
    stat = await interactions.get(bot, interactions.Channel, object_id=1071867749527195649)
    serveur = await interactions.get(bot, interactions.Guild, object_id=member.guild_id)
    await stat.modify(name=f"🔱•Members: {serveur.member_count}")
    await channel.send(f"{member.mention} a succombé à l'érosion du temps...")


### XP (aled) ###

#Gain d'xp
@bot.event
async def on_message_create(msg: interactions.Message):
    try:
        user = msg.author
        if not user.bot:
            xp = len(msg.content) / 10
            curent_xp = look_in_bdd(user.id)[0][2]
            maj_xp(user.id, curent_xp+xp)
            
            #Check lvl up
            if (xp+curent_xp) /1000 >= 1:
                lvl = look_in_bdd(user.id)[0][3]
                reste = look_in_bdd(user.id)[0][2] - 1000 + len(msg.content) / 10
                lvl_up(user.id, lvl+1)
                maj_xp(user.id, round(reste, 1))
    except:
        if look_in_bdd(user.id) == []:
            add_to_bdd(user.id, 0, 0)


@bot.command(
    name= 'rank',
    description= 'Le leaderboard du serveur !', 
    scope=guild_id
)
async def rank(ctx: interactions.CommandContext):
    data = bdd_rank()
    await ctx.send(embeds = interactions.Embed(
        title = 'Rank',
        color = 221932,
        fields = [
            interactions.EmbedField(
            name="1.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[0][0])).mention} **LVL** {data[0][2]} **|** {data[0][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="2.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[1][0])).mention} **LVL** {data[1][2]} **|** {data[1][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="3.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[2][0])).mention} **LVL** {data[2][2]} **|** {data[2][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="4.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[3][0])).mention} **LVL** {data[3][2]} **|** {data[3][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="5.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[4][0])).mention} **LVL** {data[4][2]} **|** {data[4][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="6.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[5][0])).mention} **LVL** {data[5][2]} **|** {data[5][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="7.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[6][0])).mention} **LVL** {data[6][2]} **|** {data[6][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="8.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[7][0])).mention} **LVL** {data[7][2]} **|** {data[7][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="9.",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[8][0])).mention} **LVL** {data[8][2]} **|** {data[8][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="10:",
            value=f"{(await interactions.get(bot, interactions.User, object_id=data[9][0])).mention} **LVL** {data[9][2]} **|** {data[9][1]}**/1000 XP**",
            inline=False
                    ),
            interactions.EmbedField(
            name="Vous:",
            value=f"{(await interactions.get(bot, interactions.Member, parent_id=guild_id, object_id=ctx.user.id)).mention} **LVL** {look_in_bdd(ctx.user.id)[0][3]} **|** {look_in_bdd(ctx.user.id)[0][2]}**/1000 Xp**",
            inline=False)
        ]
    ))

    
bot.start()
