import os
import time
import random
import discord

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

# Dictionnaires de sauvegarde en mémoire
sessions_pignolle = {}
victimes_rage_bait = {} 

def format_duree(secondes):
    """Transforme les secondes en un format lisible."""
    minutes, secs = divmod(int(secondes), 60)
    heures, minutes = divmod(minutes, 60)
    parts = []
    if heures > 0: parts.append(f"{heures} h")
    if minutes > 0: parts.append(f"{minutes} min")
    parts.append(f"{secs} sec")
    return " et ".join(parts)

def generer_defi():
    """Génère un défi aléatoire (La fameuse roulette)"""
    jeux = ["math", "copie", "envers", "devinette"]
    choix = random.choice(jeux)

    if choix == "math":
        a = random.randint(4, 15)
        b = random.randint(3, 9)
        return (f"🧠 **Combien font {a} x {b} ?**", str(a * b), "math")

    elif choix == "copie":
        phrases = [
            "Je jure solennellement que je suis un gros noob.",
            "Le créateur de ce bot est mon maître absolu.",
            "J'ai cliqué sur le salon rage bait comme un pigeon."
        ]
        phrase = random.choice(phrases)
        return (f"✍️ **Recopie EXACTEMENT cette phrase (avec la majuscule et le point) :**\n`{phrase}`", phrase, "copie")

    elif choix == "envers":
        mots = ["Discord", "Troll", "Raquette", "Pignolle", "Chouquette", "Saucisson"]
        mot = random.choice(mots)
        reponse = mot[::-1].lower() # Le mot inversé, en minuscules
        return (f"🔄 **Écris ce mot complètement à l'envers :** `{mot}`", reponse, "envers")

    elif choix == "devinette":
        devinettes = [
            ("Combien de mois ont 28 jours dans une année ?", ["12", "douze", "tous"]),
            ("Je suis grand quand je suis jeune, et petit quand je suis vieux. Qui suis-je ?", ["un crayon", "crayon", "une bougie", "bougie"]),
            ("Qu'est-ce qui a des clés mais ne peut pas ouvrir de portes ?", ["un piano", "piano", "le piano", "clavier", "un clavier"])
        ]
        dev, reponses_valides = random.choice(devinettes)
        return (f"❓ **Énigme :** {dev}", reponses_valides, "devinette")


@client.event
async def on_ready():
    print(f"Bot connecté en tant que {client.user}")

@client.event
async def on_voice_state_update(member, before, after):
    text_channel = client.get_channel(ID_SALON_TEXTE)
    if not text_channel: return

    # ==========================================
    # 3. GESTION DU PIÈGE : RAGE BAIT
    # ==========================================
    if member.id in victimes_rage_bait:
        # Anti-fuite : On le ramène s'il essaie de fuir ailleurs
        if after.channel and after.channel.name != NOM_SALON_RAGE:
            rage_channel = discord.utils.get(member.guild.voice_channels, name=NOM_SALON_RAGE)
            if rage_channel:
                await member.move_to(rage_channel)
                await text_channel.send(f"🛑 NOP ! {member.mention} essaie de fuir ! Retourne dans ta cage et finis l'épreuve ! 😈")
            return 

    # Entrée dans le piège
    if after.channel and after.channel.name == NOM_SALON_RAGE and (before.channel is None or before.channel.name != NOM_SALON_RAGE):
        
        # S'il était déjà piégé et qu'on l'a ramené (ou qu'il s'est reco), on ne change pas le défi !
        if member.id in victimes_rage_bait:
            await text_channel.send(f"Tu croyais m'échapper {member.mention} ? Résous d'abord ton défi en cours ! 😈")
            return
            
        # Si c'est une nouvelle victime, on génère la roulette
        texte_defi, reponse_attendue, type_jeu = generer_defi()
        
        # On sauvegarde sa punition
        victimes_rage_bait[member.id] = {
            'reponse': reponse_attendue,
            'type': type_jeu
        }

        msg_piege = (
            f"🚨 **ALERTE RAGE BAIT** 🚨\n"
            f"Ah ! {member.mention} vient de tomber dans le piège ! Tu es **BLOQUÉ(E)** ici.\n"
            f"Pour regagner ta liberté, tu dois réussir cette épreuve :\n\n"
            f"{texte_defi}\n\n"
            f"*(Toute tentative de fuite sera punie par un retour de force 😈)*"
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
    # 2. GESTION DU SALON PIGNOLLE
    # ==========================================
    if after.channel and after.channel.name == NOM_SALON_PIGNOLLE and (before.channel is None or before.channel.name != NOM_SALON_PIGNOLLE):
        sessions_pignolle[member.id] = time.time()

    elif before.channel and before.channel.name == NOM_SALON_PIGNOLLE and (after.channel is None or after.channel.name != NOM_SALON_PIGNOLLE):
        if member.id in sessions_pignolle:
            duree_secondes = time.time() - sessions_pignolle.pop(member.id)
            duree_texte = format_duree(duree_secondes)

            if duree_secondes < 30:
                commentaire = "⚡ Un record du monde de vitesse ! Même pas le temps de chauffer."
            elif duree_secondes < 180:
                commentaire = "⏱️ Rapide et efficace, la pause café est respectée."
            elif duree_secondes < 900:
                commentaire = "🧘 Belle endurance, séance accomplie dans les règles de l'art."
            else:
                commentaire = "🚨 Attention aux crampes et aux brûlures au second degré à ce stade !"

            await text_channel.send(f"📊 **Bilan de la séance de {member.mention} :**\nS'est pignollé(e) pendant exactement **{duree_texte}** !\n{commentaire}")

# ==========================================
# 4. GESTION DES MESSAGES (Résolution du mini-jeu)
# ==========================================
@client.event
async def on_message(message):
    if message.author == client.user: 
        return

    if message.author.id in victimes_rage_bait:
        donnees_jeu = victimes_rage_bait[message.author.id]
        
        # Sécurité au cas où il reste une vieille version en mémoire
        if isinstance(donnees_jeu, str):
            reponse_attendue = donnees_jeu
            type_jeu = "math"
        else:
            reponse_attendue = donnees_jeu['reponse']
            type_jeu = donnees_jeu['type']
        
        reponse_utilisateur = message.content.strip()
        reussite = False

        # Vérification selon le type de jeu
        if type_jeu == "copie":
            if reponse_utilisateur == reponse_attendue:
                reussite = True
        elif type_jeu == "devinette":
            if reponse_utilisateur.lower() in [r.lower() for r in reponse_attendue]:
                reussite = True
        else: # Pour "math" et "envers"
            if reponse_utilisateur.lower() == reponse_attendue:
                reussite = True

        # Résultat
        if reussite:
            del victimes_rage_bait[message.author.id]
            await message.channel.send(f"✅ Bien joué {message.author.mention}, c'est exact ! Tu es libre de fuir le cachot ! 🕊️")
        else:
            await message.channel.send(f"❌ Faux ! Essaie encore {message.author.mention} 🤡 (Rappel : tu es toujours bloqué(e) !)")

# Lancement du bot
token = os.getenv("DISCORD_TOKEN")
client.run(token)
