import time
import random

def print_delay(text, delay=2):
    print(text)
    time.sleep(delay)

def intro():
    print_delay("Welcome to Operation Shadow Code!")
    print_delay("You are Zahoor, a brilliant scientist deeply in love with your secretive girlfriend,")
    print_delay("whose code name is 'annonymous'.")
    print_delay("Your days were filled with interesting conversations, shared assignments, and dreams of the future...")
    print_delay("But behind her charming smile, secrets of espionage lurk.")
    input("Press Enter to continue...")

def scene_meeting():
    print_delay("\nScene 1: A Beautiful Beginning")
    print_delay("You both spend a wonderful day together—exchanging ideas, showing each other your projects,")
    print_delay("and building a connection that seems unbreakable.")
    input("Press Enter to continue...")

def scene_mission():
    print_delay("\nScene 2: The Sudden Departure")
    print_delay("Without warning, she tells you she must leave on a top-secret mission.")
    print_delay("Though she hides her true identity as a CIA agent, you sense that there is more than meets the eye.")
    input("Press Enter to continue...")

def scene_tracking():
    print_delay("\nScene 3: The Pursuit")
    print_delay("Unable to let her go, you discreetly install a tracker on her device.")
    print_delay("The tracker reveals her location... in Karachi!")
    print_delay("Driven by love and determination, you set off immediately for Karachi.")
    input("Press Enter to continue...")

def scene_kidnapping():
    print_delay("\nScene 4: The Ambush in Karachi")
    print_delay("Upon arriving in Karachi, fate takes a dark turn.")
    print_delay("You are ambushed and kidnapped by a notorious gang called 'The Cactus'.")
    print_delay("Their ruthless leader, Jhanghiz Khan, rules with an iron fist.")
    print_delay("You now find yourself confined in a secret facility, with danger lurking around every corner.")
    input("Press Enter to continue...")

def scene_interrogation():
    print_delay("\nScene 5: Confrontation with Jhanghiz Khan")
    print_delay("In a dim interrogation room, you finally come face-to-face with Jhanghiz Khan.")
    print_delay("With a sinister smile, he taunts, 'So, Zahoor, you thought you could track her without consequences?'")
    print_delay("He offers you a chance to prove your worth through a series of challenges.")
    print_delay("You sense that only your intelligence and quick wit can be your salvation.")
    input("Press Enter to continue...")
    print_delay("Choose your approach:")
    print_delay("1. Attempt to reason with Jhanghiz Khan using your scientific knowledge.")
    print_delay("2. Accept the challenge and tackle his puzzles head-on.")
    choice = input("Enter 1 or 2: ").strip()
    if choice == "1":
        print_delay("\nYou decide to reason with him.")
        if not reason_with_villain():
            print_delay("Jhanghiz Khan remains unmoved and forces you into the challenge regardless.")
            puzzle_challenge()
    elif choice == "2":
        print_delay("\nYou boldly accept the challenge!")
        puzzle_challenge()
    else:
        print_delay("\nIndecision is not an option. Jhanghiz Khan forces you into the challenge!")
        puzzle_challenge()

def reason_with_villain():
    print_delay("You present a logical argument about trust, innovation, and the value of knowledge.")
    if random.random() < 0.4:
        print_delay("Surprisingly, Jhanghiz Khan seems impressed and grants you a temporary reprieve.")
        return True
    else:
        print_delay("He scoffs at your words.")
        return False

def puzzle_challenge():
    print_delay("\nScene 6: The Puzzle Gauntlet")
    print_delay("Jhanghiz Khan presents you with a series of three challenging puzzles.")
    if not puzzle_one():
        print_delay("You failed the riddle. His henchmen close in.")
        game_over()
        exit()
    if not puzzle_two():
        print_delay("You failed the number lock challenge. The odds are now against you.")
        game_over()
        exit()
    if not puzzle_three():
        print_delay("You failed the final password challenge. Your escape slips away.")
        game_over()
        exit()
    print_delay("Jhanghiz Khan grudgingly nods in acknowledgment as you overcome all puzzles.")
    input("Press Enter to continue...")

def puzzle_one():
    print_delay("\nPuzzle 1: The Riddle of Shadows")
    print_delay("Riddle: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'")
    answer = input("Your answer: ").strip().lower()
    if answer == "echo":
        print_delay("Correct! The riddle is solved.")
        return True
    else:
        print_delay("Incorrect! The answer was 'echo'.")
        return False

def puzzle_two():
    print_delay("\nPuzzle 2: The Number Lock")
    print_delay("Jhanghiz Khan challenges, 'Guess the number I am thinking of between 1 and 10. You have 3 attempts.'")
    secret_number = random.randint(1, 10)
    attempts = 3
    while attempts > 0:
        try:
            guess = int(input("Your guess: ").strip())
        except ValueError:
            print_delay("Please enter a valid number.")
            continue
        if guess == secret_number:
            print_delay("Correct! You have unlocked the number lock.")
            return True
        else:
            attempts -= 1
            print_delay(f"Wrong guess. Attempts left: {attempts}")
    print_delay(f"You failed. The secret number was {secret_number}.")
    return False

def puzzle_three():
    print_delay("\nPuzzle 3: The DNA Sequence Code")
    print_delay("The final challenge: Unlock the high-security door with the correct 5-segment password.")
    print_delay("Clues:")
    print_delay("  - The first three segments come from your name: 'Zahoor'.")
    print_delay("  - The last two segments come from your girlfriend's code name: 'annonymous'.")
    print_delay("Each segment consists of 2 characters. Combine them in order with dashes (e.g., XX-XX-XX-XX-XX).")
    correct_password = "ZA-HO-OR-AN-US"
    attempts = 3
    while attempts > 0:
        user_input = input("Enter the 5-segment password: ").strip().upper()
        if user_input == correct_password:
            print_delay("Access granted! The door unlocks.")
            return True
        else:
            attempts -= 1
            print_delay(f"Incorrect password! Attempts left: {attempts}")
    return False

def scene_final_escape():
    print_delay("\nScene 7: The Final Escape")
    print_delay("Having bested Jhanghiz Khan's challenge, you find a hidden passage behind the unlocked door.")
    print_delay("With determination and quick thinking, you navigate a labyrinth of corridors,")
    print_delay("evading the remaining members of The Cactus.")
    print_delay("After overcoming various obstacles, you finally emerge into the freedom of the night.")
    input("Press Enter to continue...")

def game_over():
    print_delay("\nGame Over! Jhanghiz Khan and his gang, The Cactus, have claimed another victim.")
    input("Press Enter to exit...")

def ending():
    print_delay("\nCongratulations, Zahoor!")
    print_delay("You have not only escaped from the clutches of The Cactus,")
    print_delay("but also outsmarted the villain Jhanghiz Khan and his cruel challenges.")
    print_delay("Your journey has proven that determination, intellect, and love can overcome even the darkest adversaries.")
    print_delay("Perhaps one day, the full truth about your girlfriend's secret life will be revealed...")
    input("Press Enter to exit...")

def main():
    intro()
    scene_meeting()
    scene_mission()
    scene_tracking()
    scene_kidnapping()
    scene_interrogation()
    scene_final_escape()
    ending()

if __name__ == "__main__":
    main()
