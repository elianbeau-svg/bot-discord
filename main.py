import os
import time
import random
import discord

# Il faut activer l'intent pour lire les messages (Message Content Intent)
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True 

client = discord.Client(intents=intents)

# Configuration des salons vocaux
NOM_SALON_ORTHO = "👶 Orthophoniste 👶"
NOM_SALON_PIGNOLLE = "🍆Je me pignolle me dérangez pas 🍆"
NOM_SALON_RAGE = "😡 Rage bait 😡"

# ID de ton salon textuel 💬-ɢᴇ́ɴᴇ́ʀᴀʟ-💬
ID_SALON_TEXTE = 759884193042923544  

# Dictionnaires pour sauvegarder les données
sessions_pignolle = {}
victimes_rage_bait = {} # Stocke {id_utilisateur: reponse_attendue}

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
    # 3. GESTION DU PIÈGE : RAGE BAIT (Anti-fuite)
    # On met ça en premier pour empêcher toute fuite !
    # ==========================================
    if member.id in victimes_rage_bait:
        # Si la victime essaie de rejoindre un autre salon vocal...
        if after.channel and after.channel.name != NOM_SALON_RAGE:
            rage_channel = discord.utils.get(member.guild.voice_channels, name=NOM_SALON_RAGE)
            if rage_channel:
                await member.move_to(rage_channel) # Ramené de force !
                await text_channel.send(f"🛑 NOP ! {member.mention} essaie de fuir le rage bait ! Résous l'énigme d'abord ! 😈")
            return # On arrête l'exécution ici pour lui

    # Entrée dans le salon Rage Bait (Déclenchement du piège)
    if after.channel and after.channel.name == NOM_SALON_RAGE and (before.channel is None or before.channel.name != NOM_SALON_RAGE):
        # On génère un calcul aléatoire
        a = random.randint(4, 15)
        b = random.randint(3, 9)
        reponse = str(a * b)
        victimes_rage_bait[member.id] = reponse

        msg_piege = (
            f"🚨 **ALERTE RAGE BAIT** 🚨\n"
            f"Ah ! {member.mention} vient de tomber dans le piège ! Tu es maintenant **BLOQUÉ(E)** ici.\n"
            f"Pour regagner ta liberté et pouvoir changer de salon, tu dois répondre à ceci dans le chat :\n\n"
            f"🧠 **Combien font {a} x {b} ?**\n\n"
            f"*(Si tu essaies de fuir vers un autre salon, je te ramènerai ici de force 😈)*"
        )
        await text_channel.send(msg_piege)
        return


    # ==========================================
    # 1. GESTION DU SALON ORTHOPHONISTE
    # ==========================================
    
    if after.channel and after.channel.name == NOM_SALON_ORTHO and (before.channel is None or before.channel.name != NOM_SALON_ORTHO):
        msg_arrivee = (
            f"B-b-bonjour {member.mention}, b-b-bienvenue d-dans n-notre c-c-cabinet d'o-o-orthophoniste.\n\n"
            f"Exercice du jour : répétez 10 fois de suite 'Un chasseur sachant chasser doit savoir chasser sans son chien'. "
            f"Si vous bloquez, c'est 50€ la séance."
        )
        await text_channel.send(msg_arrivee)

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
    
    if after.channel and after.channel.name == NOM_SALON_PIGNOLLE and (before.channel is None or before.channel.name != NOM_SALON_PIGNOLLE):
        sessions_pignolle[member.id] = time.time()

    elif before.channel and before.channel.name == NOM_SALON_PIGNOLLE and (after.channel is None or after.channel.name != NOM_SALON_PIGNOLLE):
        if member.id in sessions_pignolle:
            debut = sessions_pignolle.pop(member.id)
            duree_secondes = time.time() - debut
            duree_texte = format_duree(duree_secondes)

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

# ==========================================
# 4. GESTION DES MESSAGES (Pour résoudre le mini-jeu)
# ==========================================
@client.event
async def on_message(message):
    # Éviter que le bot se réponde à lui-même
    if message.author == client.user:
        return

    # Vérifier si la personne qui écrit est actuellement piégée
    if message.author.id in victimes_rage_bait:
        reponse_attendue = victimes_rage_bait[message.author.id]

        # Si le message contient la bonne réponse
        if message.content.strip() == reponse_attendue:
            del victimes_rage_bait[message.author.id] # On le libère
            await message.channel.send(f"✅ Bien joué {message.author.mention}, réponse correcte ! La malédiction est levée, tu es libre de fuir ! 🕊️")
        else:
            # Petite moquerie si c'est faux (optionnel mais drôle)
            await message.channel.send(f"❌ Faux ! Calcule mieux que ça {message.author.mention}... (Rappel : tu es toujours bloqué(e) au cachot !)")

# Lancement du bot
token = os.getenv("DISCORD_TOKEN")
client.run(token)
