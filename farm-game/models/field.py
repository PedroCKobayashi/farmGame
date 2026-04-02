# models/field.py

from dataclasses import dataclass
from typing import Optional
from models.plant import Plant

@dataclass
class Field:
    """Representa um campo individual da fazenda"""
    id: int
    plant: Optional[Plant] = None
    
    def is_empty(self) -> bool:
        """Verifica se o campo está vazio"""
        return self.plant is None
    
    def plant_crop(self, plant: Plant):
        """Planta uma cultura no campo"""
        if not self.is_empty():
            raise ValueError(f"Field {self.id} already has a crop")
        self.plant = plant
    
    def harvest(self) -> Optional[int]:
        """Colhe a planta. Retorna quantidade ou None se não estiver pronta"""
        if self.is_empty():
            return None
        
        if not self.plant.is_ready_to_harvest():
            return None
        
        return self.plant.harvests_remaining
    
    def clear(self):
        """Remove a planta do campo"""
        self.plant = None
    
    def advance_day(self):
        """Avança um dia para a planta neste campo"""
        if not self.is_empty():
            if self.plant.days_to_mature > 0:
                self.plant.mature_one_day()
            elif self.plant.days_to_regrow > 0:
                self.plant.regrow_one_day()
    
    def get_progress(self) -> tuple[float, str]:
        """
        Retorna o progresso e status da planta
        Returns: (progresso de 0 a 100, status_text)
        """
        if self.is_empty():
            return 0, "EMPTY"
        
        plant = self.plant
        
        if plant.days_to_mature > 0:
            total = plant.get_crop_info()["maturation_days"]
            current = total - plant.days_to_mature
            progress = (current / total) * 100
            return progress, "GROWING"
        
        elif plant.days_to_regrow > 0:
            total = plant.get_crop_info()["regrowth_days"]
            current = total - plant.days_to_regrow
            progress = (current / total) * 100
            return progress, "REGROWING"
        
        else:
            return 100, "READY"
    
    def to_dict(self) -> dict:
        """Converte para dicionário (para JSON)"""
        return {
            "id": self.id,
            "plant": self.plant.to_dict() if self.plant else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Carrega a partir de dicionário"""
        plant = Plant.from_dict(data["plant"]) if data["plant"] else None
        return cls(id=data["id"], plant=plant)
