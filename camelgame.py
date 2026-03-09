import random
from time import time
import os
import sys
import subprocess


refresh = 1  # True
CHUNK_SIZE = 40
COMMAND_EXPLAIN = '''
Warning! Commands are not for normal players

commands all start with a /
most of the commands are only available during game loop

/mapseed <float | int>
this command is only available before the game starts. 
It sets the map seed to the first argument in that command.

/stats [variable]
This will print out all variables when used without argument, other wise only print out the specified variable

/setvar <variable> <int>
This command will set the in-game variable to the specified `int` value.
This command accepts a few alias, Other variable name must be accurate.


/run <statement>
This will run the argument in python

/eval <expression>
The expression should be in python. The expression will be evaluated then printed

/set <variable> <value>
This sets game internal variable `variable` argument to `value` argument.
This command is only accepts a few variables.

/instant <user input>
User input will be done as normal, except that time will not elapse.

/restart
This game will relaunch and reload the script itself in maximized cmd window.

/summon <event>
The event from the events dictionary will have its value set to 1, which should causes the event to happen
'''

GAME_EXPLAIN = '''
You have stolen a camel to make your way across the great Mobi desert.
The natives want their camel back and are chasing you down! 
Your goal is to survive your desert trek and out run the natives.

You could do one of a few things in each round: 
Drink water, go ahead at medium speed, go ahead as fast as you can, stop and rest, check everything, or search for oasis
Drink water:
You will notice when you are thirsty, you will not die instantly but soon if you don't drink water and get more thirsty
If you found another canteen, you water capacity will increase, allowing you to carry more water when you found a oasis
The canteen you found on your way will all be empty

Medium speed:
You will go ahead for some distance, likely less than full speed. 
But your camel will also get less tiredness than full speed.

Full speed:
You will go ahead for very likely more distance than medium speed. But you camel will get tired.

Resting:
Resting will reset your camel tiredness.
Resting at night might cause you to fall asleep and take up the whole night instead of 1 hour.
Traveling during night will cause more tiredness

Checking:
Checking information will take a few minutes.
You don't have a very good sense of time therefore you could only tell the time is after a certain point like sun rise.
You eyes are not very sharp so without a spyglass you can't tell the exact distance between you and the natives.

Search for oasis:
During the search you will travel ahead at less than medium speed.
You will be more likely to see an oasis, keep in mind that you are a lot more likely to see a mirage as well
Keep in mind that without a spyglass you are not much more likely to see an oasis 

If you see an oasis. The oasis you saw could be real or it might be a mirage as well.
You will be refreshed if you went to a real oasis, but you would be more exhausted if it was a mirage

Vision:
Your vision is bad with bare eyes, but don't worry, it is spyglass are pretty easy to find
Spyglass could be found no matter what you are doing.
With spyglass you could see further, this helps with spotting oasis and knowing where the natives are
If you are lucky enough to find a drone, you vision range will be incredibly far
With drone you could theoretically averagely spot an oasis every round and you will not see mirage 

Sandstorm:
You might encounter sandstorms on your way as well.
if you weren't in good condition, 
it is very likely for you to die in the sandstorm,
because you will get really thirsty and your camel will get really exhausted during the sandstorm.
# sandstorm might be seen with spyglass, it is more likely to be seen with spyglass if you were checking.
Natives could encounter sandstorms that does not affect you.
if the natives encountered a sandstorm, they will move back several miles, and they will not be traveling for the next round
You cannot know if natives encountered a sandstorm if you are looking with bare eyes

Information:
you will see the total time you spend on the last round, including the ones that are shown (or not shown) in the middle of the previous round,
for example, accidental sleeps or time consuming events.

Time:
time table: 0:00 midnight, 6:00 sun rise, 12:00 high noon, 18:00 sun set, 22:00 night fall
Night time is the time after nightfall(22:00) and before sunrise(6:00)
The more tired you are, the more inaccurate you sense of time is

'''

GAME_TIPS = '''
Prepare ahead for night time because if you rest you might fall asleep
Don't search for oasis without spyglass because you are only more likely to see mirage
Don't search for oasis when you are too thirsty because you will be more likely to see mirage
Ignoring a mirage will cause you to travel forward by twice of your vision distance
Look for oasis could be a good choice during night since it takes more time than other options
Consider sleeping when natives encountered sandstorm because they can't chase you during that time
If you goto an mirage you will instantly lose the game if you are not in good condition
'''
on_windows = sys.platform == "win32"
if on_windows:
    startup = subprocess.STARTUPINFO()  # customize window startup info
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # enable window flag for maximizing
    startup.wShowWindow = 3  # window open maximized
if not sys.stdout.isatty():
    print("WARNING! screen refreshing feature may behave unstable outside of command terminal")
    if input("press enter to run in terminal. or enter 'N' only if you want to preceded in current environment") != 'N':
        if sys.platform == "win32":
            subprocess.Popen([sys.executable, os.path.abspath(__file__)],
                             creationflags=subprocess.CREATE_NEW_CONSOLE, startupinfo=startup)
            sys.exit()
        else:
            subprocess.Popen([sys.executable, os.path.abspath(__file__)],
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
            sys.exit()
    else:
        print('screen refreshing feature will be disabled by default')
        refresh = 0  # prevent screen clearing, avoid inconsistency



map_seed = time()

print('enter "help" for game explanation')
print('enter "command" for detailed command help')
print('enter "hints" for tips')
user_input = input('Or press enter to start!').lower()
os.system('cls' if on_windows else 'clear')

while user_input:
    if user_input == 'command':
        print(COMMAND_EXPLAIN)

    elif user_input == 'hints':
        print(GAME_TIPS)

    elif user_input.split(' ')[0] == '/mapseed':
        map_seed = float(user_input.split(' ')[1])

    else:
        print(GAME_EXPLAIN)
    print('enter "help" for game explanation')
    print('enter "command" for detailed command help')
    print('enter "hints" for tips')
    user_input = input('Or press enter to start!').lower()
    os.system('cls' if on_windows else 'clear')

map_gen = random.Random(map_seed)
random.seed(map_seed)

VAR_NAMES = ('miles_traveled', 'thirst', 'camel_tiredness', 'native_distance', 'canteen_cap', 'drinks_left',
             'clock_time', 'watch',
             'prev_oasis', 'luck', 'base_vision', 'vision', 'vision_level', 'instant', 'player_tiredness',
             'reachable_oases', 'time_used', 'time_passed', 'approx_time', 'approx_time_passed', 'user_input')
COMMAND_ALIAS = {'sleepy': 'player_tiredness', 'tired': 'camel_tiredness', 'pos': 'miles_traveled',
                 'native': 'native_distance', 'drinks': 'drinks_left', 'time': 'clock_time', '\time': 'time',
                 'camel': 'camel_tiredness', 'oases': 'reachable_oases'}

miles_traveled = 0
thirst = 0
camel_tiredness = 0
native_distance = -20
canteen_cap = 3
drinks_left = 2
prev_oasis = 0  # the index of the last found oasis
luck = 25
events = {'oasis found': 0, 'sandstorm': 0, 'mirage': 0, 'until sandstorm': -1, 'leak': 0, 'native sandstorm': 0,
          'caught': 0}
base_vision = 1
vision = 1
vision_level = 0
instant = 0
player_tiredness = 0.0
watch = 0

clock_time = 720
time_names = {0: 'mid night', 360: 'sun rise', 720: 'high noon', 1080: 'sun set', 1320: 'night fall'}


def generate(chunk, gen: random.Random, seed):
    chunk_size = CHUNK_SIZE
    oases = []
    for d in range(chunk_size):
        gen.seed(chunk + d + seed)
        if gen.randrange(0, 60) == 0:
            oases.append(d + chunk*chunk_size)

    return oases


def logging(info=(), file='camel.log'):
    with open(file, 'a') as log:
        if info:
            log.write((str(info)+"\n"))
        elif info == ():
            my_vars = VAR_NAMES
            [log.write(f'{v}: {globals()[v]}, ') for v in my_vars]
            log.write('\n')


def roughly(time, tiredness, rough=True):
    return time + (random.randrange(round(-tiredness), round(tiredness+1)) if rough else 0)


def output(out):
    print(out)
    with open("camel.log", 'a') as log:
        log.write(out + '\n')



logging(locals())
done = False
reachable_oases = generate(0, map_gen, map_seed)
messages = ["""Welcome to Camel!
You have stolen a camel to make your way across the great Mobi desert.
The natives want their camel back and are chasing you down! Survive your
desert trek and out run the natives.\n\n"""]


# per iteration varaibles
commands = [' ']
day_time = 1320 > clock_time > 360
movement = 0
time_passed = 0  # approximately relate to 'minutes'
time_used = 0
approx_time = 0
approx_time_passed = 0
if len(reachable_oases):
    last_loaded_oasis = reachable_oases[-1]
else:
    last_loaded_oasis = 0

while not done:  # --------------game loop----------------------------------------------------------------
    logging('\n')
    logging()
    logging(messages)
    os.system('cls' if on_windows else 'clear') if refresh else 0

    [print(m) for m in messages]



# initialize per-iteration variables==================================
    instant = 0
    commands = [' ']
    day_time = 1320 > clock_time > 360
    messages = []
    movement = 0
    time_passed = 0  # approximately relate to 'minutes'
    time_used = 0
    approx_time_passed = 0
    if len(reachable_oases):
        last_loaded_oasis = reachable_oases[-1]
    else:
        last_loaded_oasis = 0
    if (miles_traveled + 20) // CHUNK_SIZE > (last_loaded_oasis // CHUNK_SIZE):  # load possible oases
        reachable_oases += [o for o in generate(miles_traveled // CHUNK_SIZE, map_gen, map_seed) if o not in reachable_oases]




# event spawn and checks==============================================

    # events spawn----------------------------------------------------

    if player_tiredness >= 60 or \
       ((not random.randrange(round(60-player_tiredness))) and player_tiredness >= 30):
        time_passed += (time_used := round(player_tiredness * 5))
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        player_tiredness = 0
        output(f'You fell asleep for {"about " if not watch else ""}{approx_time} minutes because You are too tired')

    events['oasis found'] += len(
        [o for o in reachable_oases if miles_traveled - vision <= o <= miles_traveled + vision]) if not (
        events['oasis found']) else 0

    if not random.randrange(0, luck):
        events['sandstorm'] = 1

    # if random.randrange(max(luck-thirst**2, 1)) == 0:
    if random.randrange(max(luck - (thirst - 2), 1)) == 0:
        events['mirage'] = 1
        if vision_level == 2:
            events['mirage'] = 0

    if luck > 40 and (not random.randrange(max(55-luck, 1))):
        events['native sandstorm'] = 1

    if events['mirage'] and events['oasis found']:
        if user_input != 'F':
            events[random.choices(('mirage', 'oasis found'), weights=(25*5*3, luck*(7-thirst)*vision))] = 0
        else:
            events['oasis found'] = 0

    logging(events)




    # events evaluate-------------------------------------------------
    if events['oasis found']:
        prev_oasis += 1
        if (miles_traveled in reachable_oases) or (
            input('you saw an oasis ahead, enter "go" to go, enter nothing to ignore:').lower() == 'go'):
            output(f'you have found {"an oasis!" if events['oasis found'] == 1 else 
                  f"{events['oasis found']} oases in a row!"}')
            thirst = 0
            drinks_left = canteen_cap
            camel_tiredness = 0
            player_tiredness = 0
        else:
            output('you have ignored an oasis')
            movement += base_vision * 2 + 1
        events['oasis found'] = 0

    if events['sandstorm']:
        output("you have encountered a sandstorm!")
        camel_tiredness += 3
        thirst += 2
        player_tiredness += 10
        time_passed += (time_used := random.randrange(50-luck, 141-luck*2))
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        output(f'It blocked you for {"roughly" if not watch else 'exactly'} {approx_time} minutes')
        if thirst > 6:
            thirst = 6
        if camel_tiredness >= 8:
            camel_tiredness = 7
        if player_tiredness >= 60:
            player_tiredness = 59
        events['sandstorm'] = 0


    if random.randrange(luck, 150) >= 140:
        if not vision_level:
            vision_level = 1
            output("you have found a spyglass! Your vision improved")
            base_vision = 3
        elif vision_level == 1 and random.randrange(0, 100) <= luck/3 - 8:
            # 1% at natural luck, 17% with maxed luck
            vision_level = 2
            output('Congratulations! you have found a drone!')
            output("Now you can see further than you ever could!")
            base_vision = 10

    if (not watch) and random.randrange(100) <= luck - 16:
        # 10% at natural luck, 35% with maxed luck
        output('Congratulations! you have found a pocket watch!')
        if random.randrange(100) <= luck*2:
        # 5% working, or 35% with maxed luck
            output("It is in good condition! Now you can tell time accurately!")
            watch = 1
        else:
            output("Unfortunately, it is not functioning")

    if not random.randrange(max(120 - luck, 1)):
        canteen_cap += 3
        output('You have found another canteen! Your water capacity has increased')



    if events['mirage']:
        if input('you saw an oasis ahead, enter "go" to go, enter other to ignore:').lower() == 'go':
            output('Unfortunately, it was only a mirage. You are more exhausted')
            thirst += 2
            player_tiredness += 10
            camel_tiredness += 2
        else:
            output('you have ignored a mirage')
            movement += base_vision * 2 + 1
        events['mirage'] = 0

    if events['native sandstorm']:
        native_distance -= (back := random.randrange(round(luck/2), luck))
        if vision_level:
            output(f'The natives has encountered a sandstorm, they went back {back}')

        # event clears after native not move




# situation checks====================================================

    if player_tiredness >= 30:
        output("You are tired")
    elif player_tiredness >= 40:
        output("You are very tired. You can barely keep your eyes open.")


    output('you are thirsty!') if 6 >= thirst > 4 else 0
    if thirst > 6:
        output('you died of thirst!')
        done = True
        break

    if 8 >= camel_tiredness > 5:
        output('your camel is getting tired!')
    elif camel_tiredness > 8:
        output('your camel dead!')
        done = True
        break

    if native_distance >= 0:
        output('You are caught by the natives!')
        events['caught'] = 1
    elif native_distance >= -15:
        output('The natives are getting close!')

    if events['caught']:
        input('Press enter to attempt escaping')
        if random.randrange(0, 2):
            output("Congratulations! You are safe for now. You are 5 miles ahead of the natives")
            native_distance = -5
            events['caught'] = 0
        else:
            output('You failed to escape. You lost.')
            done = True
            break


    if miles_traveled >= 200:
        output('\nYou win!')
        done = True
        break


# user input==========================================================
    user_input = input(
f"""\n
A. Drink from your canteen.
B. Ahead moderate speed.
C. Ahead full speed.
{('D. Stop and rest.' if day_time else 'D. Stop for the night.')}
E. Status check. 
F. Search for oasis
Q. Quit.
Your choice? """)

    user_input = user_input.upper() if '/' not in user_input else user_input



    if not user_input:
        time_passed += (time_used := random.randrange(1, 6))
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        messages.append(f'you wasted {"about " if not watch else ""}{approx_time} minute doing nothing')


# commands------------------------------------------------------------
    elif user_input[0] == '/':
        commands = user_input.split(' ')
        if commands[0] == '/stats':
            if commands[1] in COMMAND_ALIAS:
                commands[1] = COMMAND_ALIAS[commands[1]]
            try:
                messages.append(locals() if len(commands) < 2 else locals()[commands[1]])
            except KeyError:
                messages.append('invalid variable name \'' + commands[1] + '\'')
        else:
            try:
                if commands[0] == '/setvar':
                    if commands[1] in COMMAND_ALIAS:
                        commands[1] = COMMAND_ALIAS[commands[1]]
                    if commands[1] in globals():
                        try:
                            globals()[commands[1]] = int(commands[2])
                        except ValueError as e:
                            messages.append(e)
                    else:
                        messages.append("variable not found")
                elif commands[0] == '/run':
                    exec(' '.join(commands[1:]))
                elif commands[0] == '/eval':
                    messages.append('evaluated: ' + str(eval(' '.join(commands[1:]))))
                elif commands[0] == '/set':
                    if commands[1] == 'refresh':
                        refresh = int(commands[2])
                elif commands[0] == '/instant':
                    user_input = ' '.join(commands[1:]).upper()
                    instant = 1
                elif commands[0] == '/restart':
                    subprocess.Popen([sys.executable, os.path.abspath(__file__)],
                                     creationflags=subprocess.CREATE_NEW_CONSOLE, startupinfo=startup)
                    sys.exit()
                elif commands[0] == '/summon':
                    events[commands[1]] = 1
                else:
                    messages.append(f'command: \'{commands[0]}\' not recognised')
            except IndexError:
                messages.append('command missing arguments')

# normal inputs-------------------------------------------------------
    if user_input == 'Q':
        done = True
        output("quitting")
        break
    elif user_input == 'E':
        messages.append(f'Miles traveled:  {miles_traveled} \nDrinks in canteen:  {drinks_left}')
        messages.append(f'You have {canteen_cap // 3} canteen{"s" if canteen_cap > 3 else ""}')
        if not vision_level:
            if -native_distance < 10:
                messages.append(f'The native are about '
                                f'{abs(round(-native_distance) + random.randrange(-2, 3))} miles behind you')
                # error with naked eye
            else:
                messages.append("The natives are more than 10 miles behind you")
        elif vision_level == 1:
            if -native_distance < 30:
                messages.append(
                    f'The native are about {round(-native_distance) + 
                    random.randrange(round(native_distance / 5), round((-native_distance) / 5))} miles behind you')
            else:
                messages.append("The natives are more than 30 miles behind you")
            messages.append('you have a spyglass')
        else:  # vision level 2, with drone
            messages.append(f'The natives are {round(-native_distance, 2)} miles behind you.')

        if not watch:
            messages.append(f'It is after {time_names[max(k for k in time_names if k <= clock_time)]}')
        else:
            messages.append(f'It is {clock_time // 60}:{clock_time % 60}')
        time_passed += (time_used := random.randrange(10, 16))
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        messages.append(f'you spent {"about " if not watch else ""}{approx_time} minutes checking everything')

    elif user_input == 'D':
        camel_tiredness = 0
        thirst -= random.choices((0, 1), (25, luck))[0]
        sleep_choice = input(f'Do you want to {"take a nap" if day_time else "sleep"}?(yes/no):').lower() == 'yes'
        if sleep_choice and not day_time:
            time_passed += (time_used := (clock_time >= 1320) * (1440 - clock_time + 360) + (clock_time < 1320) * (360 - clock_time))
            approx_time = roughly(time_used, player_tiredness, not watch)
            approx_time_passed += approx_time
            if time_used < 60:
                time_used += 60
                time_passed += 60
                approx_time = roughly(time_used, player_tiredness, not watch)
                approx_time_passed += approx_time
            player_tiredness = 0
            messages.append(f'You have spent {"about " if not watch else ""}{approx_time} minutes sleeping')
            messages.append(f'You feel energetic')
        elif sleep_choice and day_time:
            time_passed += (time_used := round(player_tiredness * 4))
            approx_time = roughly(time_used, player_tiredness, not watch)
            approx_time_passed += approx_time
            if time_used < 60:
                time_used += 60
                time_passed += 60
                approx_time = roughly(time_used, player_tiredness, not watch)
                approx_time_passed += approx_time
            player_tiredness = 0
            messages.append(f'You have spent {"about " if not watch else ""}{approx_time} minutes taking a nap')
            messages.append(f'You feel energetic')
        else:
            if player_tiredness >= 60 or \
               ((not random.randrange(round(30 - player_tiredness/2))) and player_tiredness >= 30):
                time_passed += (time_used := round(player_tiredness * 5))
                approx_time = roughly(time_used, player_tiredness, not watch)
                approx_time_passed += approx_time
                player_tiredness = 0
                output(f'You accidentally fell asleep for {"about " if not watch else ""}'
                      f'{approx_time} minutes because You are too tired')
            else:
                time_passed += (time_used := 60)
                approx_time = roughly(time_used, player_tiredness, not watch)
                approx_time_passed += approx_time
                player_tiredness /= 2
                messages.append(f'You feel less tired')
                messages.append(f'You have spent {"about " if not watch else ""}{approx_time} minutes resting')

        # 60 minutes if before sunset and after sun rise else:
        # sleep at night, time till day end plus time to sun rise; else if time before sun set, time till sun rise
        # if nap
        # simply: sleep for whole night

        messages.append('camel is happy')
    elif user_input == 'C':
        movement = random.randrange(10, 21)
        thirst += 1
        time_passed += (time_used := 60)
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        camel_tiredness += random.randrange(1, 4) + (random.choice((0, 0, 1)) if not day_time else 0)
        messages.append(f'you traveled full speed for {"about " if not watch else ""}{approx_time} minutes')
    elif user_input == 'B':
        movement = random.randrange(5, 13)
        thirst += 1
        time_passed += (time_used := 60)
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        camel_tiredness += 1 + (random.choice((0, 0, 0, 1)) if not day_time else 0)
        messages.append(f'you traveled medium speed for {"about " if not watch else ""}{approx_time} minutes')


    elif user_input == 'A':
        time_passed += (time_used := 5)
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        if drinks_left:
            thirst = 0
            drinks_left -= 1
            messages.append(f'You drunk some water')
            messages.append(f'you spent {"about " if not watch else ""}{approx_time} minutes to drink water')
        else:
            messages.append('You are out of drinks')
            messages.append(f'you spent {"about " if not watch else ""}{approx_time} minutes to check you canteen')
    elif user_input == 'F':
        movement = random.randrange(3, 11)
        events['oasis found'] += len(
            [o for o in reachable_oases
             if miles_traveled - vision * (vision_level + 1) <= o <= miles_traveled + vision * (vision_level + 1)])
        # if random.randrange(max(luck - (thirst-2), 1)) == 0:
        if vision_level != 2 and not random.randrange(max(round(luck - 2 ** (thirst - 1)), 1)):
            events['mirage'] = round(1 - random.random() * vision_level)
        time_passed += (time_used := 90)
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        camel_tiredness += 1 + (random.choice((0, 0, 0, 1)) if not day_time else 0)
        messages.append(f'you spent {"about " if not watch else ""}{approx_time} minutes looking for an oasis')



    elif commands[0][0] != '/' and user_input:
        time_passed += (time_used := random.randrange(1, 6))
        approx_time = roughly(time_used, player_tiredness, not watch)
        approx_time_passed += approx_time
        messages.append(f'you wasted {"about " if not watch else ""}{approx_time} minute doing nothing')

    messages.append(f'you traveled {movement} miles!') if user_input not in ('A', 'E', 'D') else 0


# movement==================and time==================================
    if not instant:
        miles_traveled += movement
        if not events['native sandstorm']:
            native_distance += random.randrange(7, 14) * time_passed / 60 - movement
        else:
            messages.append(f"The natives couldn't chase you in the past {approx_time_passed} minutes "
                            f'because they were blocked by a sandstorm')
            events['native sandstorm'] = 0
        if [t for t in time_names if t <= clock_time][-1] != [t for t in time_names if t <= (clock_time + time_passed) % 1440][-1]:
            messages.append(f'it is {time_names[[t for t in time_names if t <= (clock_time + time_passed) % 1440][-1]]}')

        clock_time = (clock_time + time_passed) % 1440

        player_tiredness += (random.random() / 5 * time_passed) if not day_time else 0.01 * time_passed
        messages.append(f'{"roughly" if not watch else "exactly"} {approx_time_passed} minutes has past')
        # adds per minute average of 0.1 during night or 0.01 per minute during day
        # which means 6 per hour for night; 0.6 per hour for day
        # which means about 48 for whole night


# adjustments=========================================================
    if -native_distance > 40:
        luck = 15
    elif -native_distance > 60:
        luck = 10
    elif -native_distance <= 15:
        luck = 50
    else:
        luck = 25

    vision_factors = (not events['sandstorm'], day_time, player_tiredness < 40)
    for f in vision_factors:
        vision = base_vision * f
# end of each iteration===============================================
input("press enter to exit")

