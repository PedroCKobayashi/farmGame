# services/market.py

import random
from config.constants import SELL_TIER_THRESHOLDS, SELL_TIER_MULTIPLIERS, TOOL_BONUS_MULTIPLIER
from models.player import Player

class Market:
    """Gerencia vendas e cálculo de preços"""
    
    @staticmethod
    def calculate_harvest_amount(min_amount: int, max_amount: int) -> int:
        """Calcula quantidade colhida (com variação)"""
        return random.randint(min_amount, max_amount)
    
    @staticmethod
    def calculate_sale_price(base_value: int, quantity: int, player: Player) -> int:
        """
        Calcula o preço total de venda com tiers
        
        Cada unidade tem uma chance de tier baseada em:
        - Roll aleatório (1-50)
        - Bônus da ferramenta do player
        - Nível do player
        """
        total_price = 0
        tool_bonus = 1.15 ** player.tool_level
        
        for _ in range(quantity):
            # Roll = (random 1-50) * tool_bonus + player_level
            roll = (random.randint(1, 50) * tool_bonus) + player.level
            
            # Determina tier baseado no roll
            tier = 1
            for i, threshold in enumerate(SELL_TIER_THRESHOLDS):
                if roll > threshold:
                    tier = i + 2
            
            # Aplica multiplicador de tier
            tier_multiplier = SELL_TIER_MULTIPLIERS[tier - 1]
            total_price += base_value * tier_multiplier
        
        return total_price
    
    @staticmethod
    def get_tier_distribution(base_value: int, quantity: int, player: Player) -> dict:
        """
        Calcula distribuição de tiers (útil para exibir ao jogador)
        Returns: {"tier_1": count, "tier_2": count, ...}
        """
        tiers = {1: 0, 2: 0, 3: 0, 4: 0}
        tool_bonus = 1.15 ** player.tool_level
        
        for _ in range(quantity):
            roll = (random.randint(1, 50) * tool_bonus) + player.level
            
            tier = 1
            for i, threshold in enumerate(SELL_TIER_THRESHOLDS):
                if roll > threshold:
                    tier = i + 2
            
            tiers[tier] += 1
        
        return tiers
