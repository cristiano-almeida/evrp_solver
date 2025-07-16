Algoritmo Genético para o Problema de Roteamento de Veículos (VRP)
📌 Visão Geral do Projeto
Este projeto apresenta a implementação de um Algoritmo Genético (AG) em Python para resolver o Problema de Roteamento de Veículos (VRP). O objetivo é encontrar as rotas de menor distância total para uma frota de veículos atender a um conjunto de clientes a partir de um depósito central.

Esta implementação foi desenvolvida como parte do primeiro trabalho da disciplina de [Nome da Disciplina], focando na resolução de uma versão simplificada do Electric Vehicle Routing Problem (EVRP), onde as restrições de capacidade de carga e bateria foram desconsideradas.

O código é capaz de:

Ler instâncias de problemas no formato .evrp

Executar um AG com representação por permutação e operadores clássicos (seleção por torneio, crossover de ordem, mutação por troca/inversão)

Rodar múltiplas execuções independentes, respeitando um orçamento computacional

Gerar relatórios de resultados, estatísticas consolidadas e gráficos de convergência e de rotas

📁 Estrutura de Pastas e Arquivos
plaintext
Copiar
Editar
.
├── E-n23-k3.evrp         # Arquivo de dados da primeira instância
├── E-n51-k5.evrp         # Arquivo de dados da segunda instância
├── evrp_solver.py        # Script principal contendo todo o código da solução
├── plots/                # Pasta para salvar os gráficos gerados
│   ├── comparison_...png
│   ├── convergence_...png
│   └── route_...png
├── results/              # Pasta para salvar os resultados em texto e CSV
│   ├── summary_...csv
│   └── ..._runN.txt
└── README.md             # Este arquivo de documentação
Descrição dos Arquivos
evrp_solver.py: O coração do projeto. Contém as classes ConfigEVRP, InstanciaEVRP, CromossomoEVRP e AlgoritmoGeneticoEVRP.

Arquivos .evrp: Devem estar na raiz do projeto para que o script possa encontrá-los.

Pasta plots/: Criada automaticamente pelo script para armazenar todas as visualizações gráficas geradas, como gráficos de convergência e mapas de rotas.

Pasta results/: Criada automaticamente para salvar os resultados detalhados de cada execução em arquivos .txt e um resumo estatístico em formato .csv.

⚙️ Configuração e Execução (Windows)
1. Pré-requisitos
Python 3.8+ instalado

⚠️ Marque a opção "Add Python to PATH" durante a instalação.

2. Criar e Ativar o Ambiente Virtual (venv)
Abra o Prompt de Comando (CMD) ou o PowerShell no diretório raiz do projeto e execute:

bash
Copiar
Editar
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\activate
Após a ativação, o nome do seu prompt deve estar prefixado com (venv).

3. Instalar as Dependências
Crie um arquivo chamado requirements.txt na raiz do projeto com o seguinte conteúdo:

txt
Copiar
Editar
numpy
matplotlib
tqdm
Em seguida, instale as dependências com:

bash
Copiar
Editar
pip install -r requirements.txt
4. Executar o Algoritmo
Para rodar o solver:

bash
Copiar
Editar
python evrp_solver.py
O script imprimirá o progresso no console e salvará os arquivos de resultado nas pastas results/ e plots/.

5. Desativar o Ambiente Virtual
Quando finalizar, você pode desativar o ambiente virtual com:

bash
Copiar
Editar
deactivate
📊 Análise dos Resultados
Os resultados de cada execução são salvos em três formatos:

Relatório Detalhado (.txt)
Para cada execução, um arquivo em results/ exibe o fitness final, o gap em relação ao valor ótimo conhecido e a rota detalhada de cada veículo.

Resumo Estatístico (.csv)
O arquivo summary_...csv consolida os resultados das 20 execuções, com métricas como mínimo, máximo, média e desvio padrão.

Gráficos Visuais (.png)
Armazenados em plots/, incluem:

Gráfico de Rota: Visual da melhor solução encontrada

Gráfico de Convergência: Evolução do melhor fitness por execução

Gráfico de Comparação: Curva de convergência de todas as execuções
