# models/player.py

from dataclasses import dataclass
from config.constants import MAX_LEVEL, MAX_TOOL_LEVEL

@dataclass
class Player:
    """Representa o jogador"""
    name: str
    level: int = 1
    money: int = 0
    tool_level: int = 0  # 0 = iron, 4 = iridium
    
    def add_money(self, amount: int):
        """Adiciona dinheiro"""
        if amount < 0:
            raise ValueError("Cannot add negative money")
        self.money += amount
    
    def spend_money(self, amount: int) -> bool:
        """Tenta gastar dinheiro. Retorna True se conseguir"""
        if amount > self.money:
            return False
        self.money -= amount
        return True
    
    def level_up(self) -> bool:
        """Aumenta o nível. Retorna True se conseguir"""
        if self.level < MAX_LEVEL:
            self.level += 1
            return True
        return False
    
    def upgrade_tool(self) -> bool:
        """Melhora a ferramenta. Retorna True se conseguir"""
        if self.tool_level < MAX_TOOL_LEVEL:
            self.tool_level += 1
            return True
        return False
    
    def get_tool_bonus(self) -> float:
        """Retorna o bônus da ferramenta para vendas"""
        return 1.15 ** self.tool_level
    
    def to_dict(self) -> dict:
        """Converte para dicionário (para JSON)"""
        return {
            "name": self.name,
            "level": self.level,
            "money": self.money,
            "tool_level": self.tool_level
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Carrega a partir de dicionário"""
        return cls(**data)
