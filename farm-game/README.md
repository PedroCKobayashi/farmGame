# 🌾 Farm Game

Um jogo de simulação de fazenda inspirado em Stardew Valley, onde você planta, cuida e colhe suas plantações!

## Features

✅ Dinâmica de estações (verão, outono, inverno, primavera)
✅ Sistema de plantação e colheita
✅ Múltiplos tipos de plantas com características diferentes
✅ Sistema de level e ferramentas
✅ Vendas com sistema de tiers de qualidade
✅ Múltiplos slots de save
✅ Sistema de dias que progride automaticamente

## Instalação

### Pré-requisitos
- Python 3.8+

### Setup

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/farm-game.git
cd farm-game
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o jogo:
```bash
python main.py
```

## Como Jogar

### Menu Principal
- **New Game**: Criar uma nova partida
- **Load Game**: Carregar uma partida salva
- **Delete Save**: Deletar um arquivo de save
- **Exit**: Sair do jogo

### Durante o Jogo

1. **Pass Day**: Avança um dia. As plantas crescem e você se aproxima da colheita.
2. **Plant Crop**: Escolha uma plantação e um campo para plantá-la.
3. **Harvest Crop**: Colha plantas prontas e venda pelo melhor preço!
4. **Check Catalog**: Veja todas as plantas disponíveis e suas características.
5. **Level Up**: Aumenta seu nível (máx. 20) para melhores preços na venda.
6. **Upgrade Tool**: Melhora sua ferramenta para bônus nas vendas (up to Iridium).

### Sistema de Estações

Cada estação dura 10 dias (total de 40 dias por ciclo):
- **Summer (Dias 0-9)**: Tomate, Beterraba, Milho, Melancia
- **Fall (Dias 10-19)**: Uva, Abóbora, Batata, Batata-doce
- **Winter (Dias 20-29)**: Café, Limão, Laranja, Alho
- **Spring (Dias 30-39)**: Trigo, Alface, Cenoura, Morango

⚠️ **Atenção**: Plantas morrem se saírem de estação!

### Sistema de Vendas

Cada item vendido tem uma chance de ser um tier diferente:
- **Tier 1**: 1x valor base
- **Tier 2**: 2x valor base
- **Tier 3**: 3x valor base
- **Tier 4**: 4x valor base

O bônus aumenta com seu **level** e **tool level**!

## Estrutura do Projeto

```
farm-game/
├── main.py                 # Entry point
├── requirements.txt        # Dependências
├── .gitignore             # Arquivos ignorar
├── config/
│   ├── constants.py       # Constantes do jogo
│   └── settings.py        # Configurações
├── models/
│   ├── plant.py          # Classe Plant
│   ├── field.py          # Classe Field
│   ├── farm.py           # Classe Farm
│   └── player.py         # Classe Player
├── services/
│   ├── save_manager.py   # Sistema de save/load
│   └── market.py         # Sistema de vendas
├── ui/
│   └── display.py        # Interface do usuário
├── data/
│   └── saves/            # Arquivos de save (gerados automaticamente)
└── tests/                # Testes unitários (futuro)
```

## Desenvolvendo

### Adicionar uma Nova Planta

Edite `config/constants.py` e adicione ao dicionário `CROPS_CATALOG`:

```python
"sua_planta": {
    "id": 17,
    "name": "Sua Planta",
    "maturation_days": 5,
    "harvestable_times": 3,
    "regrowth_days": 2,
    "min_harvest": 4,
    "max_harvest": 8,
    "base_value": 10,
    "season": "summer",
    "description": "Uma descrição bacana"
}
```

### Adicionar Novas Features

1. Crie uma classe no módulo `models/` se for um novo objeto
2. Crie um serviço no módulo `services/` se for lógica de negócio
3. Atualize `ui/display.py` se precisar de novo visual
4. Atualize `main.py` para integrar ao loop principal

## Roadmap

- [ ] Sistema de inventário completo
- [ ] Fertilizantes e pesticidas
- [ ] Animais da fazenda
- [ ] Missões e objetivos
- [ ] Tela de estatísticas
- [ ] Modo multiplayer (futuro distante)

## Contribuindo

Pull requests são bem-vindas! Para mudanças maiores, abra uma issue primeiro para discutir as alterações propostas.

## Licença

MIT License - veja LICENSE para detalhes.

## Autor

Feito com ❤️ para amigos que amam farming sims
