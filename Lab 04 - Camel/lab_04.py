import random
import os


def title_bar():
    """
    Displays the title and description of the game so that it can easily be shown at all times.
    """
    os.system('cls')
    print("Welcome to Camel!")
    print("You have stolen a camel to make your way across the great Mobi desert.")
    print("The natives want their camel back and are chasing you down! Survive your")
    print("desert trek and out run the natives.")


def display_choices():
    print("\nA. Drink from your canteen.")
    print("B. Ahead moderate speed.")
    print("C. Ahead full speed.")
    print("D. Stop for the night.")
    print("E. Status check.")
    print("Q. Quit.")


def main():
    done = False
    choice_invalid = False
    miles_traveled = 0
    thirst = 0
    camel_tiredness = 0
    miles_natives_traveled = -20
    canteen_level = 3

    while not done:
        title_bar()
        display_choices()
        traveling = False
        if not choice_invalid:
            user_choice = input("What do you wish to do?: ")
        else:
            user_choice = input("That is not a valid choice. Please try again: ")
        if user_choice.lower() == 'q':
            done = True
            print("You have successfully quit the game! Thanks for playing.")
        elif user_choice.lower() == 'e':
            print("\nYou have traveled %d miles, and have %d drinks left in your canteen."
                  % (miles_traveled, canteen_level))
            print("Your thirst level is %d and your camel tiredness is %d" % (thirst, camel_tiredness))
            print("The natives are %d miles behind you." % (miles_traveled - miles_natives_traveled))
        elif user_choice.lower() == 'd':
            camel_tiredness = 0
            print("The camel is very happy you gave it a break!")
            miles_natives_traveled += random.randint(7, 14)
        elif user_choice.lower() == 'c':
            miles_to_add = random.randint(10, 20)
            print("You go as fast as you can, travelling %d miles!" % miles_to_add)
            miles_traveled += miles_to_add
            thirst += 1
            camel_tiredness += random.randint(1, 3)
            miles_natives_traveled += random.randint(7, 14)
            traveling = True
        elif user_choice.lower() == 'b':
            miles_to_add = random.randint(5, 12)
            print("You travel at a moderate pace, travelling %d miles!" % miles_to_add)
            miles_traveled += miles_to_add
            thirst += 1
            camel_tiredness += 1
            miles_natives_traveled += random.randint(7, 14)
            traveling = True
        elif user_choice.lower() == 'a':
            if canteen_level > 0:
                canteen_level -= 1
                thirst = 0
                print("You drink from your canteen. The water is very refreshing!")
            else:
                print("You're out of water! Hopefully you run into an oasis soon.")

        if thirst > 6:
            print("You've died of thirst!")
            done = True
        elif thirst > 4:
            print("You're thirsty!")

        if camel_tiredness > 8:
            print("Your camel has died from exhaustion. You're not a very good person.")
            done = True
        elif camel_tiredness > 5:
            print("Your camel is getting tired.")

        if miles_natives_traveled >= miles_traveled:
            print("The natives have caught you. You shouldn't have stolen their camel!")
        elif miles_traveled - miles_natives_traveled <= 15:
            print("The natives are getting close!")

        if miles_traveled >= 200 and not done:
            print("\nYou've traveled far and wide, and the natives have given up the chase!")
            print("You win!")
            done = True

        if random.randint(1, 20) == 20 and traveling and not done:
            print("You've found an oasis! You've fully rested and filled your water.")
            canteen_level = 3
            thirst = 0
            camel_tiredness = 0

        input("\nPress enter to continue... ")


main()
