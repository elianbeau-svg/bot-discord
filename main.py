import os
import time
import discord

intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)

# Configuration des salons vocaux
NOM_SALON_ORTHO = "👶 Orthophoniste 👶"
NOM_SALON_PIGNOLLE = "🍆Je me pignolle me dérangez pas 🍆"

# ID de ton salon textuel 💬-ɢᴇ́ɴᴇ́ʀᴀʟ-💬
ID_SALON_TEXTE = 759884193042923544  

# Dictionnaire pour sauvegarder l'heure d'entrée dans le salon pignolle
sessions_pignolle = {}

def format_duree(secondes):
    """Transforme les secondes en un format lisible (ex: 2 min et 15 sec)."""
    minutes, secs = divmod(int(secondes), 60)
    heures, minutes = divmod(minutes, 60)
    
    parts = []
    if heures > 0:
        parts.append(f"{heures} h")
    if minutes > 0:
        parts.append(f"{minutes} min")
    parts.append(f"{secs} sec")
    
    return " et ".join(parts)

@client.event
async def on_ready():
    print(f"Bot connecté en tant que {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    text_channel = client.get_channel(ID_SALON_TEXTE)
    if not text_channel:
        return

    # ==========================================
    # 1. GESTION DU SALON ORTHOPHONISTE
    # ==========================================
    
    # Arrivée chez l'orthophoniste
    if after.channel and after.channel.name == NOM_SALON_ORTHO and (before.channel is None or before.channel.name != NOM_SALON_ORTHO):
        msg_arrivee = (
            f"B-b-bonjour {member.mention}, b-b-bienvenue d-dans n-notre c-c-cabinet d'o-o-orthophoniste.\n\n"
            f"Exercice du jour : répétez 10 fois de suite 'Un chasseur sachant chasser doit savoir chasser sans son chien'. "
            f"Si vous bloquez, c'est 50€ la séance."
        )
        await text_channel.send(msg_arrivee)

    # Départ de chez l'orthophoniste
    elif before.channel and before.channel.name == NOM_SALON_ORTHO and (after.channel is None or after.channel.name != NOM_SALON_ORTHO):
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

    # ==========================================
    # 2. GESTION DU SALON PIGNOLLE (CHRONO)
    # ==========================================
    
    # Entrée dans le salon Pignolle
    if after.channel and after.channel.name == NOM_SALON_PIGNOLLE and (before.channel is None or before.channel.name != NOM_SALON_PIGNOLLE):
        sessions_pignolle[member.id] = time.time()

    # Sortie du salon Pignolle
    elif before.channel and before.channel.name == NOM_SALON_PIGNOLLE and (after.channel is None or after.channel.name != NOM_SALON_PIGNOLLE):
        if member.id in sessions_pignolle:
            debut = sessions_pignolle.pop(member.id)
            duree_secondes = time.time() - debut
            duree_texte = format_duree(duree_secondes)

            # Commentaire selon la durée
            if duree_secondes < 30:
                commentaire = "⚡ Un record du monde de vitesse ! Même pas le temps de chauffer."
            elif duree_secondes < 180:
                commentaire = "⏱️ Rapide et efficace, la pause café est respectée."
            elif duree_secondes < 900:
                commentaire = "🧘 Belle endurance, séance accomplie dans les règles de l'art."
            else:
                commentaire = "🚨 Attention aux crampes et aux brûlures au second degré à ce stade !"

            msg_pignolle = (
                f"📊 **Bilan de la séance de {member.mention} :**\n"
                f"S'est pignollé(e) pendant exactement **{duree_texte}** !\n"
                f"{commentaire}"
            )
            await text_channel.send(msg_pignolle)

# Lancement du bot
token = os.getenv("DISCORD_TOKEN")
client.run(token)
