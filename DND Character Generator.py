'''
The D&D Character Creation Program

Author: David Holmes
Coauthor: Bryce Valley



Current Goals:
1. GUI, improve interface



Create function for:
*making lists from Files
    -data_lists
    -race/class Lists
    -descriptions lists


Things to work on:

[Mechanics]
*GUI, improve interface
*clean up code for readability
    -if needed, make functions
        >function to make lists based on a few parameters?
*half-elf (manual) - clean up stat customization option
    >Maybe create a function for both manual and auto in StatBuilder
*stat manual assignment - reiterate values and current stat after invalid response
*still printing out 'yes' after write to file question
*create function to clear out character bios folder
    >Make user triple check their answer
*reads and assigns additional race/class info for both manual and auto; right now it's just the same code copied in a different spot
    >asjusting this may cause a need to readjust the auto result printing as well
*allow manual entry the rename option
*move results functions to a new class and try to simplify the printing
*print stat allocation after assignments (manual)
    >for both, offer re-allocation

[Content]
*expand random name bank to include names from different races
*add additional info for manual vs automatic creation
*add subclasses from Xanathar's
*include skill proficiencies
*expand weapon, tool, etc. proficiency details
*race/class feats

[Big Ideas]
*Within manual, allow user to enter "Random"/"Auto" if they want to randomly choose a specific
-This could theoretically lead to a merging of the manual and automated system
    >simply setting each option to have the option of automation, and then offering an opt-in to do completely random
    >half-elf custom will be a pain, but it always is
*Set up Larger function that has subfunctions:
-Character Creation
-Character input (allowing user to enter in data from a preexisting character *insert stats manually*)
-leveling up a preset character
'''

#Import Tools
import random
import os
from StatBuilder import *
from Information import *
from pathlib import Path
direct = os.getcwd()

#Yes or No Questions
def boolean(prompt):
    boolean_answered = False
    while boolean_answered == False:
        response = input(prompt)
        if response.lower() == 'yes' or response.lower() == 'y':
            answer = True
            boolean_answered = True
        elif response.lower() == 'no' or response.lower() == 'n':
            answer = False
            boolean_answered = True
        else:
            print()
            print("Please answer Yes or No.")
    return answer

def main():

    #Retrieve Data from Files
    race_data = open(direct + "\DND Data\RaceInfo.txt", 'r')
    race_descriptions = open(direct + "\DND Data\RaceDescriptions.txt", 'r')
    class_data = open(direct + "\DND Data\ClassInfo.txt", 'r')
    class_descriptions = open(direct + "\DND Data\ClassDescriptions.txt", 'r')

    #Read Files into Lists
    race_data_list = []
    for line in race_data:
        stripped_line = line.strip()
        entry_list = stripped_line.split(',')
        race_data_list.append(entry_list)

    class_data_list = []
    for line in class_data:
        stripped_line = line.strip()
        entry_list = stripped_line.split(',')
        class_data_list.append(entry_list)

    race_list = []
    for i in range(1,len(race_data_list)):
        if race_data_list[i][0] not in race_list:
            race_list.append(race_data_list[i][0])

    class_list = []
    for i in range(1,len(class_data_list)):
        class_list.append(class_data_list[i][0])

    race_descriptions_list = []
    for line in race_descriptions:
        stripped_line = line.strip()
        race_descriptions_list.append(stripped_line)

    class_descriptions_list = []
    for line in class_descriptions:
        stripped_line = line.strip()
        class_descriptions_list.append(stripped_line)

    '''''''''''''''
    Begin Program
    '''''''''''''''
    #Restart Option
    restart = True
    while restart == True:
        add_info = Information()
        for i in range(10):
            print()
        print("Welcome to The D&D Character Creation Program!")
        print()

        #Opt-In for Tutorial
        if boolean("Would you like assistance using this program? ") == True:
            tutorial = True
        else:
            tutorial = False
        print()

        #Tutorial for More Information
        if tutorial == True:
            add_info.general()
            print()

        '''''''''''''''''
        Automatic Generator
        '''''''''''''''''
        if boolean("Use automatic generator? ") == True:
            auto_stats = Stats()
            print()

            #Race & Subrace
            auto_race = race_list[random.randint(0,len(race_list)-1)]
            subrace_list = []
            for i in range(len(race_data_list)):
                if race_data_list[i][0] == auto_race:
                    if race_data_list[i][1] != 'NA':
                        subrace = True
                        subrace_list.append(race_data_list[i][1])
                        auto_subrace = subrace_list[random.randint(0,len(subrace_list)-1)]
                    else:
                        auto_subrace = 'NA'

            #Auto Class
            auto_class = class_list[random.randint(0,len(class_list)-1)]
            for i in range(len(class_list)):
                if auto_class == class_list[i]:
                    class_index = i

            #Auto Roll Stats
            auto_stats.roll_stats()

            #Race Indices
            race_index = 0
            for index in range(len(race_data_list)):
                if race_data_list[index][0] == auto_race and race_data_list[index][1] == auto_subrace:
                    race_index = index
            rec_age = int(race_data_list[race_index][10])
            speed = race_data_list[race_index][8]

            #Race Bonuses (Half-Elves Special)
            if auto_race != 'Half-Elf':
                for i in range(6):
                    boost = int(race_data_list[race_index][i+2])
                    auto_stats.boost_list[i] = boost
            else:
                auto_stats.boost_list[5] = 2

            #Assigning Class Data
            main_stat = class_data_list[class_index+1][1]
            main_index = ''
            for i in range(6):
                if main_stat == auto_stats.ordered_list[i]:
                    main_index = i
            armor = class_data_list[class_index+1][5]
            shield = class_data_list[class_index+1][6]
            weapons = class_data_list[class_index+1][7]
            base_hp = int(class_data_list[class_index+1][2])

            #Hill Dwarf Extra Health
            if race_index == 1:
                base_hp +=1

            #Auto Age & Name
            age = random.randint(18,round(.6*rec_age))
            name_list = ['Jane Doe', 'John Doe']
            name = random.choice(name_list)

            #Auto Stats
            print("(Your primary stat is ", main_stat, " and your rolled stats are: ", auto_stats.my_stats, ")", sep='')
            auto_stats.assign_stats_auto(main_stat)
            print()

            #Race Bonuses
            for i in range(6):
                auto_stats.assigned_list[i] += auto_stats.boost_list[i]

            #Half-Elf Optimization
            if auto_race == "Half-Elf":
                auto_stats.half_elf_auto(main_index)

            #Print Automated Results
            auto_stats.results_data(name, auto_race, auto_subrace, speed, age, auto_class, base_hp, armor, shield, weapons)
            auto_stats.print_results()

            #Allow Name Change
            name_change = True
            while name_change == True:
                if boolean("Would you like to change your character name? ") == True:
                    print()
                    name = input("What is the name of your character? ")
                    print()
                    auto_stats.results_data(name, auto_race, auto_subrace, speed, age, auto_class, base_hp, armor, shield, weapons)
                    auto_stats.print_results()
                else:
                    name_change = False
                print()
            final = auto_stats



        else:
            '''''''''''''''
            Manual Builder
            '''''''''''''''
            #Choose Your Race
            print()
            stat_values = Stats()
            repeat_race = True
            while repeat_race == True:
                print("We are going to start by choosing a race from the D&D Player's Handbook.")
                if tutorial == True:
                    add_info.race()
                    print()
                    for entry in race_descriptions_list:
                        print(entry)
                    print()

                #Race Options
                race_chosen = False
                while race_chosen == False:
                    print("Choose a race from the following list:")
                    for i in range(len(race_list)):
                        if i < len(race_list)-1:
                            print(race_list[i], ', ', sep='', end='')
                        else:
                            print(race_list[i])
                    print()
                    my_race = input("My race: ")
                    for race in race_list:
                        if my_race.lower() == race.lower():
                            my_race = race
                            race_chosen = True
                    if race_chosen == False:
                        print("Try again.")
                        print()

                #Subrace Options
                subrace = False
                subrace_options = []
                subrace_bonuses = []
                for i in range(len(race_data_list)):
                    if race_data_list[i][0] == my_race:
                        if race_data_list[i][1] != 'NA':
                            subrace = True
                            subrace_options.append(race_data_list[i][1])
                            subrace_bonuses.append(race_data_list[i][11])
                        else:
                            my_subrace = 'NA'

                #Choose Subrace
                if subrace == True:
                    print()
                    print("The race you chose has additional subrace options!")
                    subrace_chosen = False
                    while subrace_chosen == False:
                        print("Please choose one of the following:")
                        for i in range(len(subrace_options)):
                            print(subrace_options[i], ": ", subrace_bonuses[i], sep='')
                        print()
                        my_subrace = input("My subrace: ")
                        for subrace in subrace_options:
                            if my_subrace[:4].lower() == subrace[:4].lower():
                                my_subrace = subrace
                                subrace_chosen = True
                        if subrace_chosen == False:
                            print("Try again.")
                            print()

                #Display Decision
                    print("You have chosen to be a ", my_subrace, " ", my_race, "!", sep='')
                elif subrace == False:
                    print("You have chosen to be a ", my_race, "!", sep='')
                print()
                if boolean("Would you like to choose a different race? ") == False:
                    repeat_race = False
                print()

            #Choose Your Class
            repeat_class = True
            while repeat_class == True:
                print("Next, you will choose a class for your character.")
                if tutorial == True:
                    add_info.dnd_class()
                    print()
                    for entry in class_descriptions_list:
                        print(entry)
                print()

                #Class Options
                class_chosen = False
                while class_chosen == False:
                    print("Choose a class from the following list:")
                    for i in range(1,len(class_data_list)):
                        if i < len(class_data_list)-1:
                            print(class_data_list[i][0], ', ', sep='', end='')
                        else:
                            print(class_data_list[i][0])
                    print()
                    my_class = input("My class: ")
                    for entry in class_list:
                        if my_class.lower() == entry.lower():
                            my_class = entry
                            class_index = class_list.index(entry)
                            class_chosen = True
                    if class_chosen == False:
                        print("Try again.")
                        print()

                #Display Decision
                print("You have chosen to be a ", my_class, "!", sep='')
                print()
                if boolean("Would you like to choose a different class? ") == False:
                    repeat_class = False
                print()

            #Data From Race & Class
            race_index = 0
            for index in range(len(race_data_list)):
                if race_data_list[index][0] == my_race and race_data_list[index][1] == my_subrace:
                    race_index = index
            rec_age = int(race_data_list[race_index][10])
            speed = race_data_list[race_index][8]
            main_stat = class_data_list[class_index+1][1]
            armor = class_data_list[class_index+1][5]
            shield = class_data_list[class_index+1][6]
            weapons = class_data_list[class_index+1][7]
            base_hp = int(class_data_list[class_index+1][2])

            #Race Bonuses (Half-Elf Special)
            if my_race != 'Half-Elf':
                for i in range(6):
                    boost = int(race_data_list[race_index][i+2])
                    stat_values.boost_list[i] = boost
            else:
                stat_values.boost_list[5] = 2

            #Hill Dwarf Extra Health
            if race_index == 1:
                base_hp +=1

            #Setting Stats
            print("Now we are going to determine your character stats for Strength (STR), Dexterity (DEX),")
            print("Constitution (CON), Intelligence (INT), Wisdom (WIS), and Charisma (CHA).")
            print()
            if tutorial == True:
                add_info.stats()
            print()

            #Display Defaults
            print("The default stats are:")
            for i in stat_values.my_stats:
                print(i, '', end='')
            print()
            print()

            #Roll for Stats
            if boolean("Would you like to roll for your stats? ") == True:
                stat_values.roll_stats()
            else:
                print("You have chosen the default values.")
            print()

            #Assigning Stats
            print("Now, choose which value you want for each stat.")
            print("Each value can only be used once.")
            print()
            print("The most important stat for a ", my_class, " is ", main_stat, ".", sep='')
            print()
            stat_values.assign_stats()

            #Half-Elf Customization
            if my_race == 'Half-Elf':
                stat_values.half_elf_manual()

            #Choose Age
            print("Looks good! Now all you need is to set your age and choose a name!")
            print("The average lifespan of a", my_race, "is", rec_age, "years.")
            print()
            age_chosen = False
            while age_chosen == False:
                try:
                    age = int(input("Your age: "))
                    if age > rec_age:
                        if boolean("You have chosen an age past your average lifespan. Are you sure? ") == True:
                            age_chosen = True
                    elif age > 0:
                        age_chosen = True
                    else:
                        print("Please enter an age above 0.")
                except:
                    print("Please enter a whole number.")
                print()

            #Choose Character Name
            name = input("What is the name of your character? ")
            print()

            #Print Results
            stat_values.results_data(name, my_race, my_subrace, speed, age, my_class, base_hp, armor, shield, weapons)
            stat_values.print_results()
            final = stat_values

        #Create New File for Bio
        if boolean("Would you like to write this bio into a file? ") != False:
            final.print_results_to_file(name, direct)

        #End of Program
        print()
        if boolean("Thank you for using the Character Creation Program! Would you like to start over? ") == False:
            restart = False
            print()
            print("Goodbye!")

    #Close Files
    race_data.close()
    race_descriptions.close()
    class_data.close()
    class_descriptions.close()
main()
