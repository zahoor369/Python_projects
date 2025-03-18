import time

def intro():
    print("Welcome to 'The Rejected Revolution'!")
    time.sleep(1)
    print("\nYou are Muhammad Zahoor Ul Haq, a visionary rejected by traditional colleges.")
    time.sleep(1)
    print("But instead of giving up, you decide to create your own institute for the rejected.")
    time.sleep(1)
    print("\nYour choices will define the future of the Zahoor Institute of Innovation (ZII).\n")
    time.sleep(2)

def build_institute():
    print("You have secured an abandoned building for your institute.")
    time.sleep(1)
    print("How do you want to attract students?\n")
    print("1. Spread the word on social media.")
    print("2. Visit rejected students personally and recruit them.")
    
    choice = input("\nEnter 1 or 2: ")
    if choice == "1":
        print("\nYour social media campaign goes viral! Hundreds of students join within days!")
        return "fast_growth"
    elif choice == "2":
        print("\nBy personally meeting students, you gain their loyalty. They trust you completely.")
        return "strong_loyalty"
    else:
        print("\nInvalid choice. Let's try again.")
        return build_institute()

def defend_institute(strategy):
    print("\nAs ZII grows, Imperial Tech University sees you as a threat.")
    time.sleep(1)
    print("They try to shut you down! How will you respond?\n")
    print("1. Gather students and protest peacefully.")
    print("2. Find powerful investors to back your institute.")
    
    choice = input("\nEnter 1 or 2: ")
    if choice == "1":
        if strategy == "strong_loyalty":
            print("\nYour loyal students stand with you, and the protests force authorities to back off.")
            return "victory"
        else:
            print("\nThe protest gains media attention, but without strong student support, ZII struggles.")
            return "struggle"
    elif choice == "2":
        print("\nYou secure funding from visionary investors, making ZII legally untouchable!")
        return "victory"
    else:
        print("\nInvalid choice. Let's try again.")
        return defend_institute(strategy)

def game_ending(result):
    time.sleep(2)
    print("\n---------------------------")
    if result == "victory":
        print("🎉 Congratulations! ZII becomes a revolutionary institute, and you are recognized as a visionary CEO!")
    else:
        print("⚠️ ZII faces setbacks, but your dream lives on. Keep fighting!")
    print("---------------------------")

def main():
    intro()
    strategy = build_institute()
    result = defend_institute(strategy)
    game_ending(result)

if __name__ == "__main__":
    main()
