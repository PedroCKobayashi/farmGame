# ui/display.py

import os
from models.farm import Farm
from config.constants import TOOLS, CROPS_CATALOG

def clear_screen():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_farm_status(farm: Farm):
    """Exibe o status completo da fazenda"""
    print("\n" + "="*60)
    print(f"  🌾 {farm.player.name.upper()}'S FARM")
    print(f"  Day {farm.current_day} | Season: {farm.current_season.upper()}")
    print("="*60)
    
    print(f"💰 Money: ${farm.player.money:,}")
    print(f"⬆️  Level: {farm.player.level}")
    print(f"🔧 Tool: {TOOLS[farm.player.tool_level].upper()}")
    print("="*60)
    
    for field in farm.fields:
        display_field_status(field)
    
    print("="*60 + "\n")

def display_field_status(field):
    """Exibe o status de um campo"""
    if field.is_empty():
        print(f"[Field {field.id}] ⬜ EMPTY")
    else:
        plant = field.plant
        crop_info = plant.get_crop_info()
        progress, status = field.get_progress()
        
        # Cria barra de progresso
        bar_length = 15
        filled = int(progress / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Informações adicionais
        harvests_info = ""
        if plant.harvests_remaining > 1:
            harvests_info = f" ({plant.harvests_remaining} harvests left)"
        
        status_emoji = "🌱" if status == "GROWING" else "🌿" if status == "REGROWING" else "✅"
        
        print(f"[Field {field.id}] {status_emoji} {plant.get_name()}{harvests_info}")
        print(f"              [{bar}] {int(progress)}% - {status}")

def display_crops_catalog():
    """Exibe catálogo de plantas disponíveis"""
    print("\n" + "="*60)
    print("  🌾 CROPS CATALOG")
    print("="*60)
    
    current_season = None
    
    for crop_key, crop_info in sorted(CROPS_CATALOG.items(), key=lambda x: x[1]["season"]):
        if current_season != crop_info["season"]:
            current_season = crop_info["season"]
            print(f"\n📍 {current_season.upper()}")
            print("-" * 60)
        
        name = crop_info["name"]
        mat_days = crop_info["maturation_days"]
        harvests = crop_info["harvestable_times"]
        min_h = crop_info["min_harvest"]
        max_h = crop_info["max_harvest"]
        value = crop_info["base_value"]
        
        print(f"  {crop_key:<15} | {name:<15} | {mat_days}d | "
              f"Harvest: {min_h}-{max_h} | Value: ${value}")
    
    print("\n" + "="*60 + "\n")

def display_menu():
    """Exibe menu principal"""
    print("What would you like to do?")
    print("1️⃣  - Pass Day")
    print("2️⃣  - Plant Crop")
    print("3️⃣  - Harvest Crop")
    print("4️⃣  - Check Crops Catalog")
    print("5️⃣  - Level Up")
    print("6️⃣  - Upgrade Tool")
    print("7️⃣  - Save and Quit")
    print("8️⃣  - Quit Without Saving")
    print()

def get_menu_choice() -> int:
    """Obtém escolha do menu do usuário"""
    while True:
        try:
            choice = int(input("Enter your choice (1-8): "))
            if 1 <= choice <= 8:
                return choice
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_harvest_prompt(farm: Farm, field_id: int) -> int:
    """Exibe prompt de venda após colheita"""
    field = farm.get_field(field_id)
    if not field or field.is_empty():
        print("Invalid field.")
        return 0
    
    plant = field.plant
    crop_name = plant.get_name()
    base_value = plant.base_value
    
    print(f"\nYou harvested {crop_name}!")
    
    while True:
        try:
            quantity = int(input("How many units would you like to sell? (0 to keep all): "))
            if quantity >= 0:
                return quantity
            else:
                print("Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
