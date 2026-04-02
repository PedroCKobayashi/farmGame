# models/farm.py

from dataclasses import dataclass
from typing import List, Optional
from models.field import Field
from models.player import Player
from models.plant import Plant
from config.constants import SEASONS, DAYS_PER_SEASON, CROPS_CATALOG, NUM_FIELDS

@dataclass
class Farm:
    """Representa a fazenda completa"""
    player: Player
    fields: List[Field]
    current_day: int = 0
    current_season_index: int = 0
    
    def __post_init__(self):
        """Inicializa campos vazios se não fornecidos"""
        if not self.fields:
            self.fields = [Field(id=i+1) for i in range(NUM_FIELDS)]
    
    @property
    def current_season(self) -> str:
        """Retorna a estação atual"""
        return SEASONS[self.current_season_index]
    
    @property
    def current_week_day(self) -> int:
        """Retorna o dia da semana (0-6)"""
        return self.current_day % 7
    
    def get_field(self, field_id: int) -> Optional[Field]:
        """Retorna um campo específico"""
        for field in self.fields:
            if field.id == field_id:
                return field
        return None
    
    def plant_crop(self, field_id: int, crop_key: str) -> tuple[bool, str]:
        """
        Tenta plantar uma cultura
        Returns: (sucesso, mensagem)
        """
        field = self.get_field(field_id)
        if not field:
            return False, f"Field {field_id} not found"
        
        if not field.is_empty():
            return False, f"Field {field_id} already has a crop"
        
        if crop_key not in CROPS_CATALOG:
            return False, f"Crop '{crop_key}' not found"
        
        crop_info = CROPS_CATALOG[crop_key]
        if crop_info["season"] != self.current_season:
            return False, f"{crop_info['name']} can only be planted in {crop_info['season']}"
        
        plant = Plant.from_crop_key(crop_key)
        field.plant_crop(plant)
        return True, f"Successfully planted {crop_info['name']} in field {field_id}"
    
    def harvest_crop(self, field_id: int) -> tuple[bool, str, Optional[int]]:
        """
        Tenta colher uma cultura
        Returns: (sucesso, mensagem, quantidade)
        """
        field = self.get_field(field_id)
        if not field:
            return False, f"Field {field_id} not found", None
        
        if field.is_empty():
            return False, f"Field {field_id} is empty", None
        
        plant = field.plant
        if plant.days_to_mature > 0:
            days_left = plant.days_to_mature
            return False, f"Crop will be ready in {days_left} days", None
        
        if plant.days_to_regrow > 0:
            days_left = plant.days_to_regrow
            return False, f"Crop will be ready to harvest in {days_left} days", None
        
        # Colheita bem-sucedida
        amount = plant.harvests_remaining
        crop_name = plant.get_name()
        
        # Reduz safras restantes
        if plant.harvests_remaining == 1:
            field.clear()
            message = f"Harvested {crop_name}. Field is now empty"
        else:
            plant.harvests_remaining -= 1
            plant.days_to_regrow = plant.get_crop_info()["regrowth_days"]
            message = f"Harvested {crop_name}. {plant.harvests_remaining} harvest(es) remaining"
        
        return True, message, amount
    
    def advance_day(self):
        """Avança um dia na fazenda"""
        self.current_day += 1
        
        # Atualiza estação
        old_season = self.current_season
        self.current_season_index = (self.current_day // DAYS_PER_SEASON) % len(SEASONS)
        
        if old_season != self.current_season:
            self._wither_out_of_season_crops()
        
        # Avança plantas
        for field in self.fields:
            field.advance_day()
    
    def _wither_out_of_season_crops(self):
        """Remove plantas que saem de estação"""
        current_season = self.current_season
        for field in self.fields:
            if not field.is_empty():
                if field.plant.season != current_season:
                    crop_name = field.plant.get_name()
                    field.clear()
                    print(f"⚠️ {crop_name} withered in field {field.id} (season changed)")
    
    def to_dict(self) -> dict:
        """Converte para dicionário (para JSON)"""
        return {
            "player": self.player.to_dict(),
            "fields": [field.to_dict() for field in self.fields],
            "current_day": self.current_day,
            "current_season_index": self.current_season_index
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Carrega a partir de dicionário"""
        player = Player.from_dict(data["player"])
        fields = [Field.from_dict(f) for f in data["fields"]]
        return cls(
            player=player,
            fields=fields,
            current_day=data["current_day"],
            current_season_index=data["current_season_index"]
        )
