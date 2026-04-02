# main.py

from models.farm import Farm
from models.player import Player
from services.save_manager import SaveManager
from services.market import Market
from ui.display import (
    clear_screen, display_farm_status, display_menu, 
    get_menu_choice, display_crops_catalog, display_harvest_prompt
)

def create_new_game(player_name: str) -> Farm:
    """Cria um novo jogo"""
    player = Player(name=player_name)
    farm = Farm(player=player, fields=[])
    return farm

def main_menu():
    """Menu principal do jogo"""
    while True:
        clear_screen()
        print("="*60)
        print("  🌾 FARM GAME 🌾")
        print("="*60)
        print("1 - New Game")
        print("2 - Load Game")
        print("3 - Delete Save")
        print("4 - Exit")
        print()
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            player_name = input("Enter your farm name: ").strip()
            if player_name:
                game_loop(create_new_game(player_name))
        elif choice == "2":
            load_game_menu()
        elif choice == "3":
            delete_save_menu()
        elif choice == "4":
            print("Thanks for playing!")
            break
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")

def load_game_menu():
    """Menu para carregar um jogo"""
    clear_screen()
    saves = SaveManager.list_saves()
    
    if not saves:
        print("No saves found.")
        input("Press Enter to continue...")
        return
    
    print("Available saves:")
    for slot, player_name in saves.items():
        print(f"  Slot {slot}: {player_name}")
    
    while True:
        try:
            slot = int(input("\nEnter slot number (0 to cancel): "))
            if slot == 0:
                return
            
            success, result = SaveManager.load_game(slot)
            if success:
                game_loop(result)
                return
            else:
                print(f"Error: {result}")
                input("Press Enter to continue...")
                return
        except ValueError:
            print("Invalid input.")

def delete_save_menu():
    """Menu para deletar um save"""
    clear_screen()
    saves = SaveManager.list_saves()
    
    if not saves:
        print("No saves found.")
        input("Press Enter to continue...")
        return
    
    print("Available saves:")
    for slot, player_name in saves.items():
        print(f"  Slot {slot}: {player_name}")
    
    while True:
        try:
            slot = int(input("\nEnter slot number to delete (0 to cancel): "))
            if slot == 0:
                return
            
            confirm = input(f"Delete save in slot {slot}? (y/n): ").strip().lower()
            if confirm == 'y':
                success, message = SaveManager.delete_save(slot)
                print(message)
                input("Press Enter to continue...")
                return
        except ValueError:
            print("Invalid input.")

def game_loop(farm: Farm):
    """Loop principal do jogo"""
    running = True
    
    while running:
        clear_screen()
        display_farm_status(farm)
        display_menu()
        
        choice = get_menu_choice()
        
        if choice == 1:
            farm.advance_day()
            print(f"Day advanced to {farm.current_day}!")
            input("Press Enter to continue...")
        
        elif choice == 2:
            clear_screen()
            display_crops_catalog()
            crop_key = input("Enter crop name: ").strip().lower()
            try:
                field_id = int(input("Enter field number (1-6): "))
                success, message = farm.plant_crop(field_id, crop_key)
                print(message)
            except ValueError:
                print("Invalid input.")
            input("Press Enter to continue...")
        
        elif choice == 3:
            try:
                field_id = int(input("Enter field number to harvest (1-6): "))
                success, message, amount = farm.harvest_crop(field_id)
                
                if success and amount:
                    print(message)
                    quantity_to_sell = display_harvest_prompt(farm, field_id)
                    
                    if quantity_to_sell > 0 and quantity_to_sell <= amount:
                        harvest_amount = Market.calculate_harvest_amount(
                            farm.get_field(field_id).plant.min_harvest_amount,
                            farm.get_field(field_id).plant.max_harvest_amount
                        )
                        
                        # Aqui você venderia a colheita
                        print(f"Feature coming soon! You can sell {harvest_amount} items.")
                    else:
                        print(f"Kept all {amount} items.")
                else:
                    print(message)
            except ValueError:
                print("Invalid input.")
            input("Press Enter to continue...")
        
        elif choice == 4:
            clear_screen()
            display_crops_catalog()
            input("Press Enter to return...")
        
        elif choice == 5:
            if farm.player.level_up():
                print(f"Level up! You are now level {farm.player.level}")
            else:
                print(f"You are already at max level ({farm.player.level})")
            input("Press Enter to continue...")
        
        elif choice == 6:
            if farm.player.upgrade_tool():
                from config.constants import TOOLS
                print(f"Tool upgraded to {TOOLS[farm.player.tool_level]}!")
            else:
                print("You already have the best tool!")
            input("Press Enter to continue...")
        
        elif choice == 7:
            success, message = SaveManager.save_game(farm, 0)  # Slot 0 como padrão
            print(message)
            if success:
                running = False
        
        elif choice == 8:
            confirm = input("Quit without saving? (y/n): ").strip().lower()
            if confirm == 'y':
                running = False

if __name__ == "__main__":
    main_menu()
