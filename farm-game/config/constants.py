# config/constants.py

SEASONS = ["summer", "fall", "winter", "spring"]
DAYS_PER_SEASON = 10
WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
TOOLS = ["iron", "bronze", "silver", "gold", "iridium"]

# Estrutura de planta melhorada
CROPS_CATALOG = {
    # SUMMER
    "tomato": {
        "id": 1,
        "name": "Tomato",
        "maturation_days": 6,
        "harvestable_times": 5,
        "regrowth_days": 2,
        "min_harvest": 4,
        "max_harvest": 6,
        "base_value": 3,
        "season": "summer"
    },
    "beet": {
        "id": 2,
        "name": "Beet",
        "maturation_days": 5,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 8,
        "max_harvest": 12,
        "base_value": 4,
        "season": "summer"
    },
    "corn": {
        "id": 3,
        "name": "Corn",
        "maturation_days": 3,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 5,
        "max_harvest": 11,
        "base_value": 4,
        "season": "summer"
    },
    "watermelon": {
        "id": 4,
        "name": "Watermelon",
        "maturation_days": 8,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 1,
        "max_harvest": 3,
        "base_value": 30,
        "season": "summer"
    },

    # FALL
    "grape": {
        "id": 5,
        "name": "Grape",
        "maturation_days": 7,
        "harvestable_times": 7,
        "regrowth_days": 1,
        "min_harvest": 3,
        "max_harvest": 8,
        "base_value": 2,
        "season": "fall"
    },
    "pumpkin": {
        "id": 6,
        "name": "Pumpkin",
        "maturation_days": 9,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 2,
        "max_harvest": 4,
        "base_value": 23,
        "season": "fall"
    },
    "potato": {
        "id": 7,
        "name": "Potato",
        "maturation_days": 5,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 8,
        "max_harvest": 20,
        "base_value": 3,
        "season": "fall"
    },
    "sweet_potato": {
        "id": 8,
        "name": "Sweet Potato",
        "maturation_days": 2,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 8,
        "max_harvest": 12,
        "base_value": 3,
        "season": "fall"
    },

    # WINTER
    "coffee": {
        "id": 9,
        "name": "Coffee",
        "maturation_days": 2,
        "harvestable_times": 15,
        "regrowth_days": 1,
        "min_harvest": 2,
        "max_harvest": 2,
        "base_value": 2,
        "season": "winter"
    },
    "lime": {
        "id": 10,
        "name": "Lime",
        "maturation_days": 9,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 4,
        "max_harvest": 6,
        "base_value": 20,
        "season": "winter"
    },
    "orange": {
        "id": 11,
        "name": "Orange",
        "maturation_days": 3,
        "harvestable_times": 2,
        "regrowth_days": 4,
        "min_harvest": 2,
        "max_harvest": 8,
        "base_value": 5,
        "season": "winter"
    },
    "garlic": {
        "id": 12,
        "name": "Garlic",
        "maturation_days": 2,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 4,
        "max_harvest": 6,
        "base_value": 6,
        "season": "winter"
    },

    # SPRING
    "wheat": {
        "id": 13,
        "name": "Wheat",
        "maturation_days": 4,
        "harvestable_times": 1,
        "regrowth_days": 0,
        "min_harvest": 4,
        "max_harvest": 12,
        "base_value": 5,
        "season": "spring"
    },
    "lettuce": {
        "id": 14,
        "name": "Lettuce",
        "maturation_days": 2,
        "harvestable_times": 3,
        "regrowth_days": 1,
        "min_harvest": 7,
        "max_harvest": 10,
        "base_value": 1,
        "season": "spring"
    },
    "carrot": {
        "id": 15,
        "name": "Carrot",
        "maturation_days": 6,
        "harvestable_times": 2,
        "regrowth_days": 2,
        "min_harvest": 16,
        "max_harvest": 18,
        "base_value": 2,
        "season": "spring"
    },
    "strawberry": {
        "id": 16,
        "name": "Strawberry",
        "maturation_days": 3,
        "harvestable_times": 7,
        "regrowth_days": 2,
        "min_harvest": 2,
        "max_harvest": 8,
        "base_value": 2,
        "season": "spring"
    },
}

# Configurações do jogo
MAX_LEVEL = 20
NUM_FIELDS = 6
MAX_TOOL_LEVEL = 4

# Configurações de venda
SELL_TIER_THRESHOLDS = [50, 80, 100]  # Limites de tier
SELL_TIER_MULTIPLIERS = [1, 2, 3, 4]  # Multiplicadores por tier
TOOL_BONUS_MULTIPLIER = 1.15
