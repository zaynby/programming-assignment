from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    try:
        map_file = open(filename, 'r')
        global MAP_WIDTH
        global MAP_HEIGHT
    except FileNotFoundError:
        print('File is not found')
        
    map_struct.clear()
    
    # TODO: Add your map loading code here
    for line in map_file:
        row = line.strip('\n')
        map_struct.append(row)
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)
    
    map_file.close()
# This function clears the fog of war at the 3x3 square around the player
def clear_fog(player, fog):
    for row in range(player['y'] - 1, player['y'] + 2):
        if row == -1 or row == len(fog):
            continue
        for col in range(player['x']- 1, player['x'] + 2):
            if col == -1 or col == len(fog[0]):
                continue
            elif row == player['y'] and col == player['x']:
                fog[row] = fog[row][0:col+1] + 'M' + fog[row][col+2:]
            else:
                fog[row] = fog[row][0:col + 1] + game_map[row][col] + fog[row][col+2:]
    mine_map()
    return
#initialize the game
def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)
    # TODO: initialize fog
#actual fog
    
    for row in range(MAP_HEIGHT):
        fog_row = '|'
        for col in range(MAP_WIDTH):
            fog_row += '?'
        fog_row += '|'
        fog.append(fog_row)
        fog_row = '|'
    # TODO: initialize player
    #You will probably add other entries into the player dictionary
    player['pickaxe_level'] = 1
    player['mining_type'] = 'copper'
    player['day'] = 1
    player['name'] = str(input("Greetings, miner! What is your name? "))
    print(f'Pleased to meet you, {player['name']}. Welcome to Sundrop Town!')
    player['GP'] = 0
    player['x'] = 0
    player['y'] = 0
    player['copper_collected'] = 0
    player['silver_collected'] = 0
    player['gold_collected'] = 0
    player['turns'] = TURNS_PER_DAY
    player['steps'] = 0
    player['current_load'] = 0
    player['bag_capacity'] = 10
    player['portal'] = (player['x'], player['y'])
    player['latest_mine'] = [0,' ']
    player['copper_sales'] = 0
    player['silver_sales'] = 0
    player['gold_sales'] = 0
#GP calculator per node
def GP_calculator():
    cp_sale = player['copper_collected'] * randint(prices['copper'][0],prices['copper'][1])
    player['copper_sales'] += cp_sale
    sl_sale =  player['silver_collected'] * randint(prices['silver'][0],prices['silver'][1])
    player['silver_sales'] += sl_sale
    g_sale =  player['gold_collected'] * randint(prices['gold'][0],prices['gold'][1])  
    player['gold_sales'] += g_sale
    player['GP'] += player['copper_sales']+player['silver_sales']+player['gold_sales']
    return    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
     for y in range(MAP_HEIGHT):
        row = ''
        for x in range(MAP_WIDTH):
            # Player's current position
            if x == player['x'] and y == player['y']:
                row += 'M'

            # Portal location — show only if already visible
            elif (x, y) == player['portal']:
                if fog[y][x] != '?':  # Revealed tile
                    row += 'P'
                else:
                    row += '?'
            # Revealed or hidden map cell
            else:
                row += fog[y][x]
        print(game_map)
        return
# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):    
    print(f'Day {player['day']}')
    fog_of_war = '+---+\n'
    for y in range(player['y'] - 1 ,player['y'] + 2):  
        fog_of_war += '|'
        if y == -1:
            fog_of_war += '###|\n'
            continue
        elif y == len(game_map):
            fog_of_war += '###|\n'
            break
        for x in range(player['x'] - 1 ,player['x'] + 2):
            if x == -1:
                fog_of_war += '#'
            elif x == player['x'] and y == player['y']:
                fog_of_war += 'M'
            elif x == len(game_map[0]):
                fog_of_war += '#'
            else:
                fog_of_war += game_map[y][x]
        fog_of_war += "|\n"
    fog_of_war += '+---+'
    print(fog_of_war)
    return
# This function shows the information for the player
def show_information(player):
    print('----- Player Information -----')
    print(f'Name: {player['name']}')
    print(f'portal position: ({player['x'] - 1},{player['y']})')
    print(f'pickaxe level: {player['pickaxe_level']} ({player['mining_type']})')
    print(f'Gold: {player['gold_collected']}')
    print(f'Silver: {player['silver_collected']}')
    print(f'Copper: {player['copper_collected']}')
    print('------------------------------')
    print(f'Load: {player['current_load']}/{player['bag_capacity']}')
    print('------------------------------')
    print(f'GP: {player['GP']}')
    print(f'Steps taken: {player['steps']}')
    print('------------------------------')
    return
# This function saves the game
def save_game(game_map, fog, player):
    map_files = open('map_state.txt','w')
    player_file = open('player_state.txt','w')
    fog_files = open('fog_state.txt','w')
    # save map
    map_files.write(str(game_map))
    # save fog
    fog_files.write(str(fog))
    # save player
    player_file.write(str(player))
    map_files.close()
    player_file.close()
    fog_files.close()        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    try:
        map_struct = []
        load_map('map_state.txt', map_struct)
    except FileNotFoundError:
        print("File not found")
    # load fog

    # load player
    try:
        player_file = open('player_state.txt','r')
        load_player = player_file.readlines()
        player == load_player
    except FileNotFoundError:
        print("file is not found")
        return
#main menu
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")
#2 town menu
def show_town_menu():
    print()
    print(f'DAY {player['day']}')
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
#2.1 Town shop menu
def show_general_shop_menu():
    print('----------------------- Shop Menu -------------------------')
    print('(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP')
    print(f'(B)ackpack upgrade to carry {player['bag_capacity'] + 2} items for {player['bag_capacity'] * 2} GP')
    print('(L)eave shop')
    print('-----------------------------------------------------------')
    print(f'GP: {player['GP']}')
    print('-----------------------------------------------------------')
    shop_action_choice = str(input('Your choice? '))
    if shop_action_choice.lower() == 'b':
        in_backpack_shop = True
        while in_backpack_shop == True:
            show_backpack_shop_menu()
            backpack_shop_action = str(input("Your Choice? "))
            if backpack_shop_action.lower() == 'b':
                if player['GP'] >= player['bag_capacity'] * 2:
                    print(f"Congratulations! You can now carry {player['bag_capacity'] + 2} items!")
                    player['GP'] = player['GP'] - (player['bag_capacity'] * 2)
                    player['bag_capacity'] = player['bag_capacity'] + 2
                else:
                    print("You do not enough GP go and mine for more.")
            elif backpack_shop_action.lower() == 'l':
                in_backpack_shop = False
                return
    elif shop_action_choice.lower() == 'p':
        if player['mining_type'] == 'copper':
            if player['GP'] >= pickaxe_price[0]:
                print("Congratulations! You can now mine silver!")
                player['GP'] = player['GP'] - pickaxe_price[0]
                player['mining_type'] = 'silver'
            else:
                print("You do not have enough GP go out and mine for more")
        elif player['mining_type'] == 'silver':
            if player['GP'] >= pickaxe_price[1]:
                print("Congratulations! You can now mine silver!")
                player['GP'] = player['GP'] - pickaxe_price[1]
                player['mining_type'] = 'gold'
            else:
                print("You do not have enough GP go out and mine for more")
    else:
        print("Your pickaxe is already at max level")            
#2.1.1 Backpack upgrade menu
def show_backpack_shop_menu():
    print('----------------------- Shop Menu -------------------------')
    print(f'(B)ackpack upgrade to carry {player['bag_capacity'] + 2} items for {player['bag_capacity'] * 2} GP')
    print('(L)eave shop')
    print('-----------------------------------------------------------')
    print(f'GP: {player['GP']}')
    print('-----------------------------------------------------------')   
#Portal stone function
def portal_stone():
    if player['turns'] == 0:
        print("-----------------------------------------------------")
        print("You can't carry any more, so you can't go that way.")
        print('You are exhausted.')
        print("You place your portal stone here and zap back to town.")
        GP_calculator()
        print(f"You sell {player['copper_collected']} copper ore for {player['copper_sales']} GP.")
        print(f"You sell {player['silver_collected']} copper ore for {player['silver_sales']} GP.")
        print(f"You sell {player['gold_collected']} copper ore for {player['gold_sales']} GP.")
        print(f"You now have {player['GP']} GP.")
        fog[player['y']] = fog[player['y']][:player['x']] + 'P' + fog[player['y']][player['x'] + 1:]
        player['day'] = player['day'] + 1
        player['copper_collected'] = 0
        player['silver_collected'] = 0
        player['gold_collected'] = 0
        player['current_load'] = 0
    elif player['GP'] >= WIN_GP:
        print("-----------------------------------------------------")
        print(f"Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
        print("You now have enough to retire and play video games every day.")
        print(f"And it only took you player {player['days']} days and {player['steps']} steps! You win!")
        print('---------------------------------------------------')
        highscore = open('high_score.txt','w')
        highscore.write(f'{player['day']+player['steps']}\n')
    else:
        print("-----------------------------------------------------")
        print("-")
        print("You place your portal stone here and zap back to town.")
        fog[player['y']] = fog[player['y']][:player['x']] + 'P' + fog[player['y']][player['x'] + 1:]
        player['day'] = player['day'] + 1
        player['copper_collected'] = 0
        player['silver_collected'] = 0
        player['gold_collected'] = 0
        player['current_load'] = 0
    return
#shows mine map
def mine_map():
#Border lines
    border = '+'
    for wid in range(30):
        border += '-'
    border += '+'
    print(border)
#fog
    for row in range(len(fog)):
        if fog[row] != MAP_WIDTH:
            print(fog[row])
        else:
            print(fog[row])
#Border lines
    border = '+'
    for wid in range(30):
        border += '-'
    border += '+'
    print(border)
#mining information 
def mining_info():
    draw_view(game_map,fog,player)
    print(f"Turns Left: {TURNS_PER_DAY-player['steps']}          Load: {player['current_load']}/{player['bag_capacity']}          steps: {player['steps'] + 1}")
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")
    mining_checker()
    mining_action = input("Action? ")
    print()
    if game_map[player['y']][player['x']] != ' ':
        print('---------------------------------------------------')
        print(f'You mined {player['latest_mine'][0]} piece(s) of {player['latest_mine'][1]}.')
        print(f"...but you can only carry {player['bag_capacity'] - player['current_load']} more piece(s)!")
        game_map[player['y']] = game_map[player['y']][:player['x']] + ' ' + game_map[player['y']][player['x'] + 1:]
    return mining_action
#mining checker
def mining_checker():
        if game_map[player['y']][player['x']] == 'C':
            player['latest_mine'] = [randint(1,5), 'copper']
            if int(player['latest_mine'][0]) >= int(player['bag_capacity']) - int(player['current_load']):
                player['latest_mine'][0] = (player['bag_capacity'] - player['current_load'])
                player['copper_collected'] = player['copper_collected'] + (player['bag_capacity'] - player['current_load'])
                player['current_load'] = player['bag_capacity']
                return
            else:
                player['copper_collected'] = int(player['latest_mine'][0]) + player['copper_collected']
        elif game_map[player['y']][player['x']] == 'S':
            if player['mining_type'] == 'copper':
                print('you need to upgrade your pickaxe to mine silver')
            else:
                player['latest_mine'] = [randint(1,3), 'silver']
                if player['latest_mine'][0] >= player['bag_capacity'] - player['current_load']:
                    player['latest_mine'][0] = (player['bag_capacity'] - player['current_load'])
                    player['silver_collected'] = (player['bag_capacity'] - player['current_load'])
                    return
                else:
                    player['silver_collected'] = int(player['latest_mine'][0]) + player['silver_collected']
        elif game_map[player['y']][player['x']] == 'G':
            if player['mining_type'] == 'copper' or player['mining_type'] == 'silver':
                print('you need to upgrade your pickaxe to mine silver')
            else:
                player['latest_mine'] = [randint(1,2), 'gold']
                if player['latest_mine'][0] >= player['bag_capacity'] - player['current_load']:
                    player['latest_mine'][0] = (player['bag_capacity'] - player['current_load'])
                    player['gold_collected'] = (player['bag_capacity'] - player['current_load'])
                    return
                else:    
                    player['gold_collected'] = int(player['latest_mine'][0]) + player['gold_collected']
        player['current_load'] = int(player['copper_collected']) + int(player['silver_collected']) + int(player['gold_collected'])
        return
#mine movement
def mine_actions():
    in_mine = True
    print("---------------------------------------------------")
    print('{:^51}'.format('Day ' + str(player['day'])))
    print("---------------------------------------------------")
    while in_mine == True:
        mining_action = mining_info()
        if game_map[player['y']][player['x']] == 'T':
            player['day'] = player['day'] + 1
            in_mine == False
        elif player['turns'] == 0:
            portal_stone()
            in_mine = False
        elif mining_action.lower() == 'm':
            clear_fog(player,fog)
        elif mining_action.lower() == 'i':
            show_information(player)
        elif mining_action.lower() == 'q':
            show_main_menu()
            game_choice = str(input('Your choice? '))
            break
        elif mining_action.lower() == 'p':
            portal_stone()
            in_mine = False
        elif player['bag_capacity'] == player['current_load']:
            print("-----------------------------------------------------")
            print("You can't carry any more, so you can't go that way.")
            print("Press 'p' to portal back to town to sell your nodes")
        elif mining_action.lower() == 'w':
            if player['y'] == 0:
                print("You are already at the top")
                player['y'] == 0
                continue
            else:
                player['y'] = player['y'] - 1
                player['turns'] = player['turns'] - 1
                player['steps'] = player['steps'] + 1
        elif mining_action.lower() == 'a':
            if player['x'] == 0:
                print("You are at the edge already")
                player['x'] == 0
                continue
            else:
                player['x'] = player['x'] - 1
                player['turns'] = player['turns'] - 1
                player['steps'] = player['steps'] + 1
        elif mining_action.lower() == 's':
            if player['y'] == len(game_map) - 1:
                print("You are at the edge already")
                player['y'] == len(game_map) - 1
                continue
            else:
                player['y'] = player['y'] + 1
                player['turns'] = player['turns'] - 1
                player['steps'] = player['steps'] + 1
        elif mining_action.lower() == 'd':
            if player['x'] == len(game_map[0]) - 1:
                print("You are at the edge already")
                player['x'] == len(game_map[0]) - 1
                continue
            else: 
                player['x'] = player['x'] + 1
                player['turns'] = player['turns'] - 1
                player['steps'] = player['steps'] + 1



#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
quit_game = False
while quit_game == False:
    show_main_menu()
    game_choice = str(input('Your choice? '))
    if game_choice.lower() == 'n':
        #initialize game
        initialize_game(game_map, fog, player)
        #ensures that the person is in town
        in_town = True
        while in_town == True:
            player['turns'] = TURNS_PER_DAY
            show_town_menu()
            town_action_choice = str(input('Your choice? '))
            #2.1 Buy Stuff  
            if town_action_choice.lower() == 'b':                  
                show_general_shop_menu()
            #2.2. See Player Information
            elif town_action_choice.lower() == 'i':
                show_information(player)
                continue
            #2.3 Mine map
            elif town_action_choice.lower() == 'm':
                clear_fog(player,fog)
            #2.4 Enter mine
            elif town_action_choice.lower() == 'e':
                mine_actions()
            #save game
            elif town_action_choice.lower() == 'v':
                save_game(game_map,fog,player)
                print('game saved')
            #quit to main menu
            elif town_action_choice.lower() == 'q':
                break
    elif game_choice.lower() == 'l':
        load_game(game_map,fog,player)
                #ensures that the person is in town
        in_town = True
        while in_town == True:
            player['turns'] = TURNS_PER_DAY
            show_town_menu()
            town_action_choice = str(input('Your choice? '))
            #2.1 Buy Stuff  
            if town_action_choice.lower() == 'b':                  
                show_general_shop_menu()
            #2.2. See Player Information
            elif town_action_choice.lower() == 'i':
                show_information(player)
                continue
            #2.3 Mine map
            elif town_action_choice.lower() == 'm':
                clear_fog(player,fog)
            #2.4 Enter mine
            elif town_action_choice.lower() == 'e':
                mine_actions()
            #save game
            elif town_action_choice.lower() == 'v':
                save_game(game_map,fog,player)
                print('game saved')
            #quit to main menu
            elif town_action_choice.lower() == 'q':
                break
    elif game_choice.lower() == 'q':
        break