# models/plant.py

from dataclasses import dataclass, asdict
from config.constants import CROPS_CATALOG

@dataclass
class Plant:
    """Representa uma planta em um campo"""
    crop_key: str
    days_to_mature: int
    harvests_remaining: int
    days_to_regrow: int
    min_harvest_amount: int
    max_harvest_amount: int
    base_value: int
    season: str
    
    @classmethod
    def from_crop_key(cls, crop_key: str):
        """Cria uma planta a partir da chave do catálogo"""
        if crop_key not in CROPS_CATALOG:
            raise ValueError(f"Crop '{crop_key}' not found in catalog")
        
        crop = CROPS_CATALOG[crop_key]
        return cls(
            crop_key=crop_key,
            days_to_mature=crop["maturation_days"],
            harvests_remaining=crop["harvestable_times"],
            days_to_regrow=crop["regrowth_days"],
            min_harvest_amount=crop["min_harvest"],
            max_harvest_amount=crop["max_harvest"],
            base_value=crop["base_value"],
            season=crop["season"]
        )
    
    def is_ready_to_harvest(self) -> bool:
        """Verifica se a planta está pronta para colheita"""
        return self.days_to_mature == 0 and self.days_to_regrow == 0
    
    def mature_one_day(self):
        """Avança um dia no crescimento"""
        if self.days_to_mature > 0:
            self.days_to_mature -= 1
    
    def regrow_one_day(self):
        """Avança um dia no recrescimento após colheita"""
        if self.days_to_regrow > 0:
            self.days_to_regrow -= 1
    
    def get_crop_info(self) -> dict:
        """Retorna informações da planta"""
        return CROPS_CATALOG[self.crop_key]
    
    def get_name(self) -> str:
        """Retorna nome da planta"""
        return self.get_crop_info()["name"]
    
    def to_dict(self) -> dict:
        """Converte para dicionário (para JSON)"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Carrega a partir de dicionário"""
        return cls(**data)
