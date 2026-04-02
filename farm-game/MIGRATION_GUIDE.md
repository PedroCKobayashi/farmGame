# 📊 Guia de Migração: JSON Antigo vs Novo

## Comparação de Estrutura

### JSON ANTIGO (seu código original)

```json
{
  "campos": [
    {
      "id": 1,
      "plantado": "Empty",
      "maturamento": 0,
      "safras_restantes": 0,
      "crescimento": 0,
      "colheita_min": 0,
      "colheita_max": 0,
      "val": 0,
      "estacao": ""
    }
  ],
  "dia_atual": 0,
  "dia_semana": "mon",
  "estacao_atual": "summer",
  "level": 1,
  "tool": 0
}
```

### JSON NOVO (refatorado)

```json
{
  "player": {
    "name": "Seu Nome",
    "level": 1,
    "money": 0,
    "tool_level": 0
  },
  "fields": [
    {
      "id": 1,
      "plant": {
        "crop_key": "tomato",
        "days_to_mature": 6,
        "harvests_remaining": 5,
        "days_to_regrow": 2,
        "min_harvest_amount": 4,
        "max_harvest_amount": 6,
        "base_value": 3,
        "season": "summer"
      }
    }
  ],
  "current_day": 0,
  "current_season_index": 0
}
```

## Mudanças Principais

### ✅ Melhorias

| Aspecto | Antigo | Novo | Razão |
|---------|--------|------|-------|
| **Nomes** | Português misto (plantado, maturamento) | Inglês padronizado | Consistência e profissionalismo |
| **Organização Player** | Espalho no root | `player` object | Melhor lógica de domínio |
| **Plant Data** | String "Empty" | `plant: null` | Mais robusto |
| **Dias da semana** | `dia_semana` salvo | Calculado dinamicamente | Menos redundância |
| **Crescimento** | Dois campos (`maturamento` + `crescimento`) | Um sistema unificado | Mais simples |
| **Nomenclatura** | Abreviado (`val`, `colheita_min`) | Completo (`base_value`, `min_harvest_amount`) | Mais legível |

---

## Se Quiser MANTER Compatibilidade com Antigos Saves

Você pode criar um **migration script** que converte saves antigos para novos:

### Opção 1: Migration Automática (Recomendado)

```python
# services/migration.py

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


# No SaveManager, adicione isto:
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
```

---

## Mudanças de Nomenclatura Recomendadas

### Você PRECISA mudar se quer usar o código novo:

| Antigo | Novo | Onde |
|--------|------|------|
| `plantado` | `crop_key` | Dentro de `plant` |
| `campos` | `fields` | Raiz do JSON |
| `maturamento` | `days_to_mature` | Dentro de `plant` |
| `safras_restantes` | `harvests_remaining` | Dentro de `plant` |
| `crescimento` | `days_to_regrow` | Dentro de `plant` |
| `colheita_min` | `min_harvest_amount` | Dentro de `plant` |
| `colheita_max` | `max_harvest_amount` | Dentro de `plant` |
| `val` | `base_value` | Dentro de `plant` |
| `estacao` | `season` | Dentro de `plant` |
| `dia_atual` | `current_day` | Raiz do JSON |
| `estacao_atual` | `current_season_index` | Raiz do JSON |
| `level` | `player.level` | Dentro de `player` |
| `tool` | `player.tool_level` | Dentro de `player` |

---

## Se Quiser MANTER Nomenclatura Antiga

Você pode customizar o SaveManager:

```python
# Edite o método to_dict() na classe Farm para gerar formato antigo:

def to_dict_legacy(self) -> dict:
    """Exporta no formato antigo para compatibilidade"""
    campos = []
    for field in self.fields:
        campo = {
            "id": field.id,
            "plantado": field.plant.crop_key if field.plant else "Empty",
            "maturamento": field.plant.days_to_mature if field.plant else 0,
            "safras_restantes": field.plant.harvests_remaining if field.plant else 0,
            "crescimento": field.plant.days_to_regrow if field.plant else 0,
            "colheita_min": field.plant.min_harvest_amount if field.plant else 0,
            "colheita_max": field.plant.max_harvest_amount if field.plant else 0,
            "val": field.plant.base_value if field.plant else 0,
            "estacao": field.plant.season if field.plant else ""
        }
        campos.append(campo)
    
    return {
        "campos": campos,
        "dia_atual": self.current_day,
        "estacao_atual": self.current_season,
        "level": self.player.level,
        "tool": self.player.tool_level
    }
```

---

## Minha Recomendação

### 🎯 **Opção A: Usar o novo formato (RECOMENDADO)**

- ✅ Mais limpo e profissional
- ✅ Melhor OOP
- ✅ Código novo é totalmente compatível
- ❌ Precisa converter saves antigos
- **Ação**: Use o migration script acima

### 🔄 **Opção B: Adaptar o novo código para formato antigo**

- ✅ Compatibilidade 100% com saves antigos
- ❌ Código novo precisa de adaptar
- ❌ Menos Pythônico
- **Ação**: Crie custom `to_dict()` e `from_dict()`

---

## Qual Escolher?

Se você está **refazendo tudo**, **eu recomendo a Opção A** (novo formato):
1. Seus saves antigos podem ser deletados (é um novo projeto!)
2. O código novo é muito mais limpo
3. Você aprende boas práticas de design

Se você quer **manter compatibilidade**, use a **Opção B**:
1. Seus saves continuam funcionando
2. Já que refatorou, pode fazer migration depois
