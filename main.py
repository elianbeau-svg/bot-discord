import os
import discord

intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)

# Nom exact du salon vocal à surveiller
NOM_SALON_VOCAL = "👶 Orthophoniste 👶"

# Nom ou ID du salon textuel où envoyer les messages
# (Tu peux mettre l'ID du salon textuel sous forme de nombre si tu préfères, ex: 123456789)
NOM_SALON_TEXTE = "orthophoniste" 

@client.event
async def on_ready():
    print(f"Bot connecté en tant que {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    # Récupération du salon textuel où poster
    # Si tu as mis un ID, utilise client.get_channel(ID)
    text_channel = discord.utils.get(member.guild.text_channels, name=NOM_SALON_TEXTE)
    if not text_channel:
        return

    # 1. QUAND UN MEMBRE ARRIVE DANS LE SALON VOCAL
    if after.channel and after.channel.name == NOM_SALON_VOCAL and (before.channel is None or before.channel.name != NOM_SALON_VOCAL):
        msg_arrivee = (
            f"B-b-bonjour {member.mention}, b-b-bienvenue d-dans n-notre c-c-cabinet d'o-o-orthophoniste.\n\n"
            f"Exercice du jour : répétez 10 fois de suite 'Un chasseur sachant chasser doit savoir chasser sans son chien'. "
            f"Si vous bloquez, c'est 50€ la séance."
        )
        await text_channel.send(msg_arrivee)

    # 2. QUAND UN MEMBRE QUITTE LE SALON VOCAL
    elif before.channel and before.channel.name == NOM_SALON_VOCAL and (after.channel is None or after.channel.name != NOM_SALON_VOCAL):
        msg_depart = (
            f"Merci {member.display_name} pour votre visite, vous trouverez ci joint votre compte-rendu médical.\n"
            f"À bientôt!\n\n"
            f"**Compte-Rendu Médical :**\n\n"
            f"**Titre :** Bilan d'Évaluation du Bégaiement\n"
            f"**Patient :** {member.display_name}\n"
            f"**Diagnostic :** Articulation d'un moteur à deux temps par temps froid.\n"
            f"**Prescription :** 15 minutes d'exercices de respiration avant d'ouvrir son micro."
        )
        await text_channel.send(msg_depart)

# Récupère le Token depuis les variables d'environnement de Render
token = os.getenv("DISCORD_TOKEN")
client.run(token)
