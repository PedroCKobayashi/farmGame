# services/save_manager.py

import json
import os
from pathlib import Path
from models.farm import Farm

class SaveManager:
    """Gerencia salvamento e carregamento de partidas"""
    
    SAVE_DIR = Path("data/saves")
    
    @classmethod
    def _ensure_save_dir(cls):
        """Cria pasta de saves se não existir"""
        cls.SAVE_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_save_path(cls, slot: int) -> Path:
        """Retorna caminho do arquivo de save"""
        cls._ensure_save_dir()
        return cls.SAVE_DIR / f"farm_slot_{slot}.json"
    
    @classmethod
    def save_game(cls, farm: Farm, slot: int) -> tuple[bool, str]:
        """
        Salva a partida em um slot
        Returns: (sucesso, mensagem)
        """
        try:
            cls._ensure_save_dir()
            save_path = cls.get_save_path(slot)
            
            with open(save_path, 'w') as f:
                json.dump(farm.to_dict(), f, indent=4)
            
            return True, f"Game saved to slot {slot}"
        except Exception as e:
            return False, f"Error saving game: {str(e)}"
    
    @classmethod
    def load_game(cls, slot: int) -> tuple[bool, Farm | str]:
        """Carrega uma partida, com suporte a saves antigos"""
        try:
            save_path = cls.get_save_path(slot)
        
            if not save_path.exists():
                return False, f"No save found in slot {slot}"

            with open(save_path, 'r') as f:
                data = json.load(f)
        
            # Detecta se é um save antigo
            if "campos" in data and "player" not in data:
                print("⚠️  Old save format detected. Migrating...")
                from services.migration import migrate_old_save
                data = migrate_old_save(data)
                # Salva no novo formato
                cls.save_game(Farm.from_dict(data), slot)
        
            farm = Farm.from_dict(data)
            return True, farm
        except Exception as e:
            return False, f"Error loading game: {str(e)}"
    
    @classmethod
    def list_saves(cls) -> dict:
        """
        Lista todos os saves disponíveis
        Returns: {slot: player_name} ou vazio se não houver saves
        """
        cls._ensure_save_dir()
        saves = {}
        
        for save_file in cls.SAVE_DIR.glob("farm_slot_*.json"):
            try:
                with open(save_file, 'r') as f:
                    data = json.load(f)
                    slot = int(save_file.stem.split('_')[-1])
                    player_name = data.get("player", {}).get("name", "Unknown")
                    saves[slot] = player_name
            except:
                pass
        
        return dict(sorted(saves.items()))
    
    @classmethod
    def delete_save(cls, slot: int) -> tuple[bool, str]:
        """
        Deleta um save
        Returns: (sucesso, mensagem)
        """
        try:
            save_path = cls.get_save_path(slot)
            if save_path.exists():
                save_path.unlink()
                return True, f"Save slot {slot} deleted"
            else:
                return False, f"No save found in slot {slot}"
        except Exception as e:
            return False, f"Error deleting save: {str(e)}"
