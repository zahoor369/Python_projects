import random
import time
import requests
from hijri_converter import Hijri, Gregorian
from colorama import Fore, Style, init

init(autoreset=True)

# ----------------------
#   1. INPUT VALIDATION
# ----------------------
def get_valid_input(prompt, options):
    """
    Safely gets input from the user, ensuring it matches one of the valid 'options'.
    Repeats until a valid choice is entered.
    """
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(Fore.RED + "Invalid input! Please try again." + Style.RESET_ALL)


# ----------------------
#   2. KARACHI MOSQUES DATA
# ----------------------
KARACHI_MOSQUES = {
    "Masjid-e-Tooba": {
        "taraweeh_time": "8:30 PM",
        "rakats": 20,
        "imam": "Maulana Tariq Jameel",
        "special": "Quran completion in 27 nights"
    },
    "Memon Masjid": {
        "taraweeh_time": "9:00 PM",
        "rakats": 8,
        "imam": "Mufti Usmani",
        "special": "Daily tafsir session"
    },
    "Jamia Binoria": {
        "taraweeh_time": "8:45 PM",
        "rakats": 20,
        "imam": "Maulana Noman",
        "special": "Special Qirat competition"
    },
    "Bahadurabad Masjid": {
        "taraweeh_time": "8:15 PM",
        "rakats": 20,
        "imam": "Qari Basit",
        "special": "Children's Quran program"
    }
}


# ----------------------
#   3. QURAN COMPLETION SCHEDULE
# ----------------------
QURAN_SCHEDULE = {
    day: f"Juz {day} ({(day*20)+1} - {day*20+20})"
    for day in range(1, 31)
}
QURAN_SCHEDULE[27] += " - Khatam-ul-Quran Night"


# ----------------------
#   4. PLAYER CLASS
# ----------------------
class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.gender = ""
        self.mode = ""  # village, city, child, itikaf
        self.health = 100
        self.spirituality = 0
        self.discipline = 0
        self.responsibility = 0
        self.day = 1
        self.ashra = 1
        self.score = {"spiritual": 0, "discipline": 0, "charity": 0}
        self.inventory = {
            "dates": 5,
            "quran_knowledge": 0,
            "eid_gifts": 0
        }


# ----------------------
#   5. MULTIPLAYER MODE
# ----------------------
class Multiplayer:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def charity_competition(self):
        print(Fore.YELLOW + "\n===== Charity Competition =====")
        donations = []
        for p in self.players:
            amount = random.randint(100, 1000)
            donations.append({"name": p.name, "amount": amount})
        winner = max(donations, key=lambda x: x["amount"])
        print(f"{Fore.GREEN}Winner: {winner['name']} donated {winner['amount']}!")
        for p in self.players:
            if p.name == winner['name']:
                p.score["charity"] += 50


# ----------------------
#   6. ASCII ART & UI
# ----------------------
def print_mosque():
    print(Fore.CYAN + r"""
      /\
     /  \
    /____\
    |    |
    |    |
    |____|
    /_\/_\
    """ + Style.RESET_ALL)

def print_progress_bar(day):
    bar_length = 30
    filled = "🕋" * day
    empty = " " * (bar_length - day) if day <= bar_length else ""
    bar = "[" + filled + empty + "]"
    print(f"{Fore.MAGENTA}Progress: {bar}{Style.RESET_ALL}")

def show_roles_info():
    print("\n[Common Ramadan Roles]")
    print("Men: Mosque prayers, Iftar preparation help, Community service")
    print("Women: Suhoor cooking, Household management, Teaching children")
    print("*Cultural variations exist. This is a generalized view*\n")


# ----------------------
#   7. REAL-TIME FEATURES
# ----------------------
def get_hijri_date():
    today = Hijri.today()
    print(f"{Fore.YELLOW}Hijri Date: {today.day} {today.month_name()} {today.year} AH{Style.RESET_ALL}")

def get_prayer_times(city="Karachi", country="Pakistan"):
    try:
        url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}"
        response = requests.get(url)
        data = response.json()
        timings = data["data"]["timings"]
        print(Fore.CYAN + f"\nToday's Prayer Times for {city}, {country}:")
        print(f"Fajr:   {timings['Fajr']}")
        print(f"Dhuhr:  {timings['Dhuhr']}")
        print(f"Asr:    {timings['Asr']}")
        print(f"Maghrib:{timings['Maghrib']}")
        print(f"Isha:   {timings['Isha']}" + Style.RESET_ALL)
    except Exception:
        print(Fore.RED + "Failed to get prayer times. Check your internet or city name." + Style.RESET_ALL)


# ----------------------
#   8. ISLAMIC TIPS
# ----------------------
islamic_tips = [
    "The first 10 days of Ramadan are for Mercy (Rahmat).",
    "Eating dates for Suhoor or Iftar is a Sunnah.",
    "Controlling anger is essential during fasting.",
    "Search for Laylatul Qadr in the last 10 nights."
]

def show_islamic_tip():
    tip = random.choice(islamic_tips)
    print(Fore.GREEN + f"\n💡 Islamic Tip: {tip}" + Style.RESET_ALL)


# ----------------------
#   9. MINI-GAMES
# ----------------------
quran_verses = {
    "Al-Fatihah": "Bismillahir Rahmanir Rahim",
    "Al-Ikhlas": "Qul huwallahu ahad"
}

def quran_memorization_game(player):
    verse_name = random.choice(list(quran_verses.keys()))
    verse_text = quran_verses[verse_name]
    partial = verse_text[:5] + "..."
    print(Fore.YELLOW + f"Complete this verse from {verse_name}: {partial}")
    answer = input("> ")
    if answer.strip() == verse_text:
        print(Fore.GREEN + "Correct! You gained 50 spiritual points!" + Style.RESET_ALL)
        player.spirituality += 50
    else:
        print(Fore.RED + f"Wrong. The correct answer is: {verse_text}" + Style.RESET_ALL)


# ----------------------
#   10. LAYLATUL QADR EVENT
# ----------------------
def laylatul_qadr_event(player):
    if 21 <= player.day <= 30:
        print(Fore.MAGENTA + "\n✨ Laylatul Qadr Nights! ✨" + Style.RESET_ALL)
        choice = input("1. Worship all night 🌙\n2. Sleep early 😴\n> ")
        if choice == "1":
            print(Fore.GREEN + "You seized the Night of Power! Spiritual points x10!" + Style.RESET_ALL)
            player.spirituality *= 10


# ----------------------
#   11. EID PREPARATION
# ----------------------
eid_tasks = ["Buy new clothes", "Make sweets", "Decorate the house"]

def eid_countdown(player):
    days_left = 30 - player.day
    if days_left > 0:
        print(Fore.BLUE + f"\nEid is {days_left} days away! What will you do?" + Style.RESET_ALL)
        for idx, task in enumerate(eid_tasks, 1):
            print(f"{idx}. {task}")
        choice = get_valid_input("> ", [str(i) for i in range(1, len(eid_tasks)+1)])
        chosen_task = eid_tasks[int(choice)-1]
        print(Fore.GREEN + f"Great! You completed: {chosen_task}" + Style.RESET_ALL)


# ----------------------
#   12. SEHRI PHASE
# ----------------------
def sehri_phase(player):
    print(Fore.CYAN + f"\n=== DAY {player.day}: SEHRI ===" + Style.RESET_ALL)
    print_mosque()
    if player.gender == "m":
        choice = get_valid_input("1. Attend Fajr at mosque 🕌\n2. Help prepare suhoor 🥘\n> ", ["1", "2"])
        if choice == "1":
            print(Fore.GREEN + "Earned spiritual rewards for congregation prayer" + Style.RESET_ALL)
            player.spirituality += 25
        else:
            print(Fore.YELLOW + "Helped family with meal preparation" + Style.RESET_ALL)
            player.score["charity"] += 15
    elif player.gender == "f":
        choice = get_valid_input("1. Cook special suhoor meal 🍳\n2. Wake up family members 👪\n> ", ["1", "2"])
        if choice == "1":
            print(Fore.GREEN + "Family loves the delicious suhoor!" + Style.RESET_ALL)
            player.health += 10
        else:
            print(Fore.YELLOW + "Everyone is awake on time!" + Style.RESET_ALL)
            player.responsibility += 20


# ----------------------
#   13. ROZA PHASE
# ----------------------
def roza_phase(player):
    print(Fore.BLUE + f"\n=== DAY {player.day}: ROZA ===" + Style.RESET_ALL)
    challenge = random.choice([
        {"text": "Someone argued with you", "good": "1. Stay calm 🤲", "bad": "2. Shout back 😡"},
        {"text": "Saw delicious food", "good": "1. Remember fasting purpose 🕋", "bad": "2. Sneak a bite 🥘"}
    ])
    print(Fore.YELLOW + f"Challenge: {challenge['text']}" + Style.RESET_ALL)
    choice = get_valid_input(f"{challenge['good']}\n{challenge['bad']}\n> ", ["1", "2"])
    if choice == "1":
        print(Fore.GREEN + "Self-control maintained!" + Style.RESET_ALL)
        player.discipline += 20
    else:
        print(Fore.RED + "Fasting spirit broken" + Style.RESET_ALL)
        player.spirituality -= 10


# ----------------------
#   14. IFTAR PHASE
# ----------------------
def iftar_phase(player):
    print(Fore.MAGENTA + f"\n=== DAY {player.day}: IFTAR ===" + Style.RESET_ALL)
    if player.gender == "m":
        choice = get_valid_input("1. Buy dates/milk from market 🛒\n2. Lead Maghrib prayer 🧎\n> ", ["1", "2"])
        if choice == "2":
            print(Fore.GREEN + "Blessings for leading prayer" + Style.RESET_ALL)
            player.spirituality += 30
        else:
            print(Fore.YELLOW + "You contributed by buying iftar items." + Style.RESET_ALL)
    elif player.gender == "f":
        choice = get_valid_input("1. Manage cooking timings ⏲️\n2. Teach kids Ramadan etiquette 🧒\n> ", ["1", "2"])
        player.score["charity"] += 25
        if choice == "2":
            print(Fore.GREEN + "Children learn Ramadan values!" + Style.RESET_ALL)


# ----------------------
#   15. CHILD MODE
# ----------------------
def child_mode(player):
    tasks = {
        "star": "Help mom at Suhoor 🌟",
        "moon": "After fasting, learn Quran 🌙",
        "eid": "Make Eid greeting cards 🎨"
    }
    key = random.choice(list(tasks.keys()))
    print(Fore.YELLOW + "\n===== Child Mode =====" + Style.RESET_ALL)
    print(f"Today's Task: {tasks[key]}")
    print(Fore.GREEN + "You gained +10 spiritual points for helping!" + Style.RESET_ALL)
    player.spirituality += 10


# ----------------------
#   16. ITIKAF MODE
# ----------------------
def itikaf_mode(player):
    if 21 <= player.day <= 30:
        print(Fore.CYAN + "\n=== ITIKAF MODE ===" + Style.RESET_ALL)
        print("Rules: No mobile usage, focus on Quran, and stay in the mosque for itikaf (10 days: day 21 to Eid).")
        choice = get_valid_input("Did you strictly follow itikaf rules today? (y/n): ", ["y", "n"])
        if choice == "y":
            print(Fore.GREEN + "Great! Deep spiritual reflection achieved." + Style.RESET_ALL)
            player.spirituality += 100
        else:
            print(Fore.RED + "You did not fully commit to itikaf today." + Style.RESET_ALL)
            player.spirituality += 20
    else:
        print(Fore.YELLOW + "Itikaf mode is only available from day 21 to Eid." + Style.RESET_ALL)


# ----------------------
#   17. VILLAGE MODE
# ----------------------
def village_mode(player):
    print(Fore.YELLOW + "\n=== Village Mode Activities ===" + Style.RESET_ALL)
    print("In the village, traditions run deep and community is at the heart of Ramadan.")
    choice = get_valid_input(
        "1. Join a communal Iftar with neighbors 🍽️\n2. Help prepare traditional dishes for the community 🍲\n> ",
        ["1", "2"]
    )
    if choice == "1":
        print(Fore.GREEN + "You enjoyed a heartfelt Iftar with your neighbors. Spirituality increased!" + Style.RESET_ALL)
        player.spirituality += 35
    else:
        print(Fore.GREEN + "Your culinary skills brought joy to the community. Responsibility increased!" + Style.RESET_ALL)
        player.responsibility += 35


# ----------------------
#   18. CITY MODE
# ----------------------
def city_mode(player):
    print(Fore.YELLOW + "\n=== City Mode Activities ===" + Style.RESET_ALL)
    print("In the city, Ramadan blends modern challenges with traditional values.")
    choice = get_valid_input(
        "1. Attend a large mosque congregation in the city 🕌\n2. Participate in an urban charity drive 🍲\n> ",
        ["1", "2"]
    )
    if choice == "1":
        print(Fore.GREEN + "You prayed with thousands in the city. Spirituality increased!" + Style.RESET_ALL)
        player.spirituality += 40
    else:
        print(Fore.GREEN + "Your urban charity efforts made a difference. Charity points increased!" + Style.RESET_ALL)
        player.score["charity"] += 40


# ----------------------
#   19. CHAND RAAT EVENT
# ----------------------
def chand_raat_event():
    print(Fore.CYAN + "\n✨ Chand Raat Excitement! ✨" + Style.RESET_ALL)
    print("People are excited to sight the Ramadan moon! 🌙")
    choice = get_valid_input(
        "1. Look for the moon with family 👨‍👩‍👧‍👦\n2. Start Eid shopping 🛍️\n> ",
        ["1", "2"]
    )
    if choice == "1":
        print(Fore.GREEN + "You admired the moon with your loved ones!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "You began planning for Eid celebrations!" + Style.RESET_ALL)


# ----------------------
#   20. TARAWEEH PHASE
# ----------------------
def taraweeh_phase(player):
    print(Fore.CYAN + f"\n=== NIGHT {player.day}: TARAWEEH ===" + Style.RESET_ALL)
    
    # Display Karachi mosque schedule
    print(Fore.YELLOW + "\nKarachi Major Mosques Schedule:" + Style.RESET_ALL)
    for mosque, details in KARACHI_MOSQUES.items():
        print(f"{mosque}:")
        print(f"  Time: {details['taraweeh_time']}")
        print(f"  Rakats: {details['rakats']}")
        print(f"  Today's Quran: {QURAN_SCHEDULE.get(player.day, 'Special Prayers')}")
        print(f"  Special: {details['special']}\n")
    
    # Enhanced Taraweeh attendance logic
    if player.gender == "m":
        choice = get_valid_input("1. Join Jamia Binoria congregation\n2. Attend local mosque\n> ", ["1", "2"])
        if choice == "1":
            print(Fore.GREEN + "Experienced beautiful Qirat at Binoria!" + Style.RESET_ALL)
            player.spirituality += 50
        else:
            print(Fore.YELLOW + "Prayed at neighborhood mosque" + Style.RESET_ALL)
            player.spirituality += 30
        print(Fore.MAGENTA + f"\nToday's Recitation: {QURAN_SCHEDULE.get(player.day)}" + Style.RESET_ALL)
    elif player.gender == "f":
        choice = get_valid_input("1. Home taraweeh\n2. Quran study circle\n> ", ["1", "2"])
        if choice == "2":
            print(Fore.GREEN + "Learned tafsir of today's juz!" + Style.RESET_ALL)
            player.spirituality += 40
            player.inventory["quran_knowledge"] += 1
        else:
            print(Fore.YELLOW + "Performed taraweeh at home" + Style.RESET_ALL)
            player.spirituality += 25

    # Special events during Taraweeh
    if player.day == 27:
        print(Fore.GREEN + "\n✨ Khatam-ul-Quran Night! Special prayers held in all mosques!" + Style.RESET_ALL)
    elif player.day == 29:
        print(Fore.CYAN + "Qiyam-ul-Layl arranged in major mosques after taraweeh!" + Style.RESET_ALL)


# ----------------------
#   21. ASHRA SYSTEM
# ----------------------
def update_ashra(player):
    if player.day <= 10:
        player.ashra = 1  # Rahmat
        return 2.0
    elif player.day <= 20:
        player.ashra = 2  # Maghfirat
        return 1.5
    else:
        player.ashra = 3  # Nijaat
        return 3.0


# ----------------------
#   22. MAIN GAME LOOP
# ----------------------
def main():
    print(Fore.YELLOW + "\nWelcome to the Ramadan Game!" + Style.RESET_ALL)
    get_hijri_date()
    get_prayer_times()
    show_islamic_tip()

    name = input("Enter your name: ")
    player = Player(name)
    player.gender = get_valid_input("Choose gender (m/f): ", ["m", "f"])
    player.mode = get_valid_input("Choose mode (village/city/child/itikaf): ", ["village", "city", "child", "itikaf"])

    multi = Multiplayer()
    multi.add_player(player)
    show_roles_info()

    for day in range(1, 31):
        player.day = day
        multiplier = update_ashra(player)

        # 1) Show progress bar & Eid countdown
        print_progress_bar(day)
        eid_countdown(player)

        # 2) Chand Raat event on day 29
        if day == 29:
            chand_raat_event()

        # 3) Daily phases
        sehri_phase(player)
        roza_phase(player)
        iftar_phase(player)
        taraweeh_phase(player)

        # 4) Mode-specific event
        if player.mode == "itikaf":
            itikaf_mode(player)
        elif player.mode == "child":
            child_mode(player)
        elif player.mode == "village":
            village_mode(player)
        elif player.mode == "city":
            city_mode(player)

        # 5) Laylatul Qadr event
        laylatul_qadr_event(player)

        # 6) Occasional mini-game
        if random.random() < 0.1:
            print(Fore.YELLOW + "\nMini-Game: Quran Memorization" + Style.RESET_ALL)
            quran_memorization_game(player)

        # 7) Keep multiplier consistent
        player.spirituality = int(player.spirituality * multiplier / multiplier)

        # 8) Occasional Islamic tip
        if random.random() < 0.15:
            show_islamic_tip()

        # Short pause for realism
        time.sleep(0.3)

    # 9) Final results
    print(Fore.MAGENTA + "\n=== FINAL RESULTS ===" + Style.RESET_ALL)
    print(f"Name: {player.name}")
    print(f"Spirituality: {player.spirituality}")
    print(f"Discipline: {player.discipline}")
    print(f"Charity: {player.score['charity']}")
    if player.spirituality >= 100:
        print(Fore.GREEN + "Eid Mubarak! You truly embraced the spirit of Ramadan!" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Reflect and improve next year. Ramadan is a journey!" + Style.RESET_ALL)

    # 10) Check for multiplayer charity competition
    if len(multi.players) > 1:
        multi.charity_competition()


# ----------------------
#   23. LAUNCH
# ----------------------
if __name__ == "__main__":
    main()