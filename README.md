
# 🚚 Algoritmo Genético para o Problema de Roteamento de Veículos (VRP)

## 🔍 Resumo

Este projeto apresenta a implementação de um **Algoritmo Genético (AG)** em Python para resolver o **Problema de Roteamento de Veículos (VRP)**. O objetivo é encontrar as rotas de menor distância total para uma frota de veículos atender a um conjunto de clientes a partir de um depósito central.

A implementação foi desenvolvida como parte de um trabalho acadêmico e também resolve uma versão simplificada do **EVRP (Electric Vehicle Routing Problem)**, desconsiderando as restrições de bateria e capacidade de carga.

- ✅ **Representação por permutação**
- ✅ **Operadores clássicos**: torneio, crossover de ordem (OX), mutações por troca/inversão
- ✅ **Relatórios, gráficos e estatísticas completas geradas automaticamente**

---

## 📁 Estrutura do Projeto

```
.
├── E-n23-k3.evrp                # Instância 1 do problema
├── E-n51-k5.evrp                # Instância 2 do problema
├── evrp_solver.py               # Script principal com toda a lógica do algoritmo genético
├── plots/                       # Gráficos gerados pelo algoritmo
│   ├── convergence_*.png
│   ├── route_*.png
│   └── comparison_*.png
├── results/                     # Relatórios de execução
│   ├── summary_*.csv
│   └── run*_output.txt
└── README.md                    # Este arquivo de documentação
```

---

## ⚙️ Pré-requisitos

- ✅ **Python 3.8 ou superior**  
  🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

> ⚠️ No Windows, marque a opção **"Add Python to PATH"** durante a instalação.

---

## 🚀 Como Executar (Passo a Passo)

### 1. Clone ou baixe o repositório

- GitHub: https://github.com/cristiano-almeida/evrp_solver
- Ou clique em **Code** > **Download ZIP**

### 2. Crie o ambiente virtual

Abra o terminal na pasta do projeto e digite:

```
python -m venv venv
```

### 3. Ative o ambiente virtual

- **Windows**:
```
venv\Scripts\activate
```

- **Linux/Mac**:
```
source venv/bin/activate
```

### 4. Instale as dependências

Crie o arquivo `requirements.txt` com o seguinte conteúdo (caso não exista):

```
numpy
matplotlib
tqdm
```

E execute:

```
pip install -r requirements.txt
```

### 5. Execute o algoritmo

```
python evrp_solver.py
```

Os resultados serão impressos no terminal e salvos nas pastas `results/` e `plots/`.

---

## 📊 Resultados

O algoritmo produz:

- 📄 **Relatórios (`.txt`)** com rotas, fitness e gap
- 📈 **Resumo estatístico (`.csv`)** com média, desvio, melhor e pior solução
- 🗺️ **Gráficos (`.png`)**:
  - Rotas das melhores soluções
  - Convergência por execução
  - Comparação entre execuções

---

## 📚 Referências

- Trabalhos acadêmicos sobre VRP e EVRP
- Métodos genéticos com representação por permutação
- Heurísticas aplicadas a problemas logísticos

---

🔧 Projeto desenvolvido para experimentação em otimização de rotas com algoritmos bio-inspirados.
