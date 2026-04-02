def migrate_old_save(old_data: dict) -> dict:
    """Converte um save antigo para o novo formato"""
    
    # Extrai dados do jogador do formato antigo
    new_fields = []
    for campo in old_data.get("campos", []):
        field_data = {
            "id": campo["id"],
            "plant": None
        }
        
        # Se não está vazio, converte a planta
        if campo["plantado"] != "Empty":
            field_data["plant"] = {
                "crop_key": campo["plantado"],
                "days_to_mature": campo["maturamento"],
                "harvests_remaining": campo["safras_restantes"],
                "days_to_regrow": campo["crescimento"],
                "min_harvest_amount": campo["colheita_min"],
                "max_harvest_amount": campo["colheita_max"],
                "base_value": campo["val"],
                "season": campo["estacao"]
            }
        
        new_fields.append(field_data)
    
    # Novo formato
    new_data = {
        "player": {
            "name": "Migrated Player",
            "level": old_data.get("level", 1),
            "money": 0,
            "tool_level": old_data.get("tool", 0)
        },
        "fields": new_fields,
        "current_day": old_data.get("dia_atual", 0),
        "current_season_index": (old_data.get("dia_atual", 0) // 10) % 4
    }
    
    return new_data