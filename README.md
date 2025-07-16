# Algoritmo Genético para o Problema de Roteamento de Veículos (VRP)

## Visão Geral do Projeto

Este projeto apresenta a implementação de um **Algoritmo Genético (AG)** em Python para resolver o **Problema de Roteamento de Veículos (VRP)**. O objetivo é encontrar as rotas de menor distância total para uma frota de veículos atender a um conjunto de clientes a partir de um depósito central.

Esta implementação foi desenvolvida como parte do primeiro trabalho da disciplina de [Nome da Disciplina], focando na resolução de uma versão simplificada do *Electric Vehicle Routing Problem (EVRP)*, onde as restrições de capacidade de carga e bateria foram desconsideradas.

O código é capaz de:
- Ler instâncias de problemas no formato `.evrp`.
- Executar um AG com representação por permutação e operadores clássicos (seleção por torneio, crossover de ordem, mutação por troca/inversão).
- Rodar múltiplas execuções independentes, respeitando um orçamento computacional.
- Gerar relatórios de resultados, estatísticas consolidadas e gráficos de convergência e de rotas.

## Estrutura de Pastas e Arquivos

O projeto está organizado da seguinte forma para garantir clareza e separação de responsabilidades:
Use code with caution.
Markdown
.
├── E-n23-k3.evrp # Arquivo de dados da primeira instância
├── E-n51-k5.evrp # Arquivo de dados da segunda instância
├── evrp_solver.py # Script principal contendo todo o código da solução
├── plots/ # Pasta para salvar os gráficos gerados
│ ├── comparison_...png
│ ├── convergence_...png
│ └── route_...png
├── results/ # Pasta para salvar os resultados em texto e CSV
│ ├── summary_...csv
│ └── ..._runN.txt
└── README.md # Este arquivo de documentação
Generated code
- **`evrp_solver.py`**: O coração do projeto. Contém as classes `ConfigEVRP`, `InstanciaEVRP`, `CromossomoEVRP` e `AlgoritmoGeneticoEVRP`.
- **Arquivos `.evrp`**: Devem estar na raiz do projeto para que o script possa encontrá-los.
- **Pasta `plots/`**: Criada automaticamente pelo script para armazenar todas as visualizações gráficas geradas, como gráficos de convergência e mapas de rotas.
- **Pasta `results/`**: Criada automaticamente para salvar os resultados detalhados de cada execução em arquivos `.txt` e um resumo estatístico em formato `.csv`.

## Configuração e Execução (Windows)

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### 1. Pré-requisitos
- [Python 3.8+](https://www.python.org/downloads/) instalado. Certifique-se de marcar a opção "Add Python to PATH" durante a instalação.

### 2. Criar e Ativar o Ambiente Virtual (`venv`)

O uso de um ambiente virtual é altamente recomendado para isolar as dependências do projeto.

Abra o **Prompt de Comando (CMD)** ou o **PowerShell** no diretório raiz do projeto e execute os seguintes comandos:

```shell
# 1. Criar o ambiente virtual (uma pasta chamada 'venv' será criada)
python -m venv venv

# 2. Ativar o ambiente virtual
.\venv\Scripts\activate
Use code with caution.
Após a ativação, o nome do seu prompt deve ser prefixado com (venv), indicando que o ambiente virtual está ativo.
3. Instalar as Dependências
Com o ambiente virtual ativo, instale as bibliotecas necessárias. Crie um arquivo chamado requirements.txt na pasta raiz do projeto com o seguinte conteúdo:
requirements.txt:
Generated code
numpy
matplotlib
tqdm
Use code with caution.
Agora, instale essas dependências com um único comando:
Generated shell
pip install -r requirements.txt
Use code with caution.
Shell
4. Executar o Algoritmo
Para executar o solver, basta rodar o script principal. Ele processará automaticamente todas as instâncias listadas na função main():
Generated shell
python evrp_solver.py
Use code with caution.
Shell
O script irá imprimir o progresso da execução no console e, ao final, salvará todos os arquivos de resultado e gráficos nas pastas results/ e plots/.
5. Desativar o Ambiente Virtual
Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual com o comando:
Generated shell
deactivate
