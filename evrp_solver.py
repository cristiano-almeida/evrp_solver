import numpy as np
import random
import time
from math import sqrt
from tqdm import tqdm
import csv
import os
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional, Set
import matplotlib.pyplot as plt

# --- Configuração (sem alterações) ---
@dataclass
class ConfigEVRP:
    pop_size: int = 150
    mutation_rate: float = 0.25
    crossover_rate: float = 0.90
    elitism_rate: float = 0.15
    tournament_size: int = 5
    max_stagnation: int = 100
    runs: int = 20
    diversity_threshold: float = 0.15

# --- Classe da Instância (sem alterações) ---
class InstanciaEVRP:
    def __init__(self, filename: str):
        self.filename = filename
        self.name = os.path.basename(filename)
        self.coords: Dict[int, Tuple[float, float]] = {}
        self.demands: Dict[int, int] = {}
        self.optimal_value: float = 0.0
        self.vehicles: int = 0
        self.customers: int = 0
        self.num_stations: int = 0
        self.station_nodes: Set[int] = set() # Adicionado para plotar estações
        self.depot: int = 1
        self.dist_matrix: np.ndarray = np.array([])
        
        self._load_instance()
        self._build_distance_matrix()
    
    def _load_instance(self):
        try:
            with open(self.filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]

            section = None
            for line in lines:
                if line.startswith("OPTIMAL_VALUE"): self.optimal_value = float(line.split()[-1])
                elif line.startswith("VEHICLES"): self.vehicles = int(line.split()[-1])
                elif line.startswith("DIMENSION"): self.customers = int(line.split()[-1]) - 1
                elif line.startswith("STATIONS:"): self.num_stations = int(line.split()[-1])
                elif line in ["NODE_COORD_SECTION", "DEMAND_SECTION", "STATIONS_COORD_SECTION", "DEPOT_SECTION"]:
                    section = line
                    continue
                elif line == "EOF": break
                elif section == "NODE_COORD_SECTION":
                    parts = line.split()
                    if len(parts) >= 3:
                        idx, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                        self.coords[idx] = (x, y)
                elif section == "STATIONS_COORD_SECTION":
                    self.station_nodes.add(int(line.split()[0]))
                elif section == "DEPOT_SECTION":
                     if line != "-1": self.depot = int(line)

            print(f"\nInstância carregada: {self.name}")
            print(f"Clientes: {self.customers}, Veículos: {self.vehicles}, Estações: {self.num_stations}")

        except (IOError, ValueError) as e:
            raise ValueError(f"Erro ao carregar ou processar o arquivo da instância '{self.filename}': {e}")
    
    def _build_distance_matrix(self):
        nodes = sorted(self.coords.keys())
        max_node_id = max(nodes)
        self.dist_matrix = np.full((max_node_id + 1, max_node_id + 1), fill_value=np.inf)
        coords_array = np.array([self.coords[i] for i in nodes])
        diff = coords_array[:, np.newaxis, :] - coords_array[np.newaxis, :, :]
        self.dist_matrix[np.ix_(nodes, nodes)] = np.sqrt(np.sum(diff**2, axis=-1))

    def calculate_route_distance(self, route: List[int]) -> float:
        if len(route) < 2: return 0.0
        return self.dist_matrix[route[:-1], route[1:]].sum()

# --- Classe do Cromossomo (sem alterações) ---
class CromossomoEVRP:
    # (Conteúdo da classe CromossomoEVRP permanece o mesmo)
    def __init__(self, solver: 'AlgoritmoGeneticoEVRP', genes: Optional[List[int]] = None):
        self.solver = solver
        self.genes = genes if genes is not None else self._generate_random_genes()
        self.route: List[int] = []
        self.fitness: float = float('inf')
        self.is_valid: bool = False
        
        self._decode()
        self._evaluate()
    
    def _generate_random_genes(self) -> List[int]:
        customers = list(range(2, 2 + self.solver.instance.customers))
        random.shuffle(customers)
        if self.solver.instance.vehicles > 1:
            num_splits = self.solver.instance.vehicles - 1
            if len(customers) > num_splits:
                split_points = sorted(random.sample(range(1, len(customers)), num_splits))
                offset = 0
                for pos in split_points:
                    customers.insert(pos + offset, self.solver.instance.depot)
                    offset += 1
        return customers
    
    def _decode(self):
        depot = self.solver.instance.depot
        decoded_genes = [depot]
        for gene in self.genes:
            if gene != depot or (decoded_genes and decoded_genes[-1] != depot):
                decoded_genes.append(gene)
        if not decoded_genes or decoded_genes[-1] != depot:
            decoded_genes.append(depot)
        self.route = decoded_genes
        self._validate()

    def _validate(self):
        depot = self.solver.instance.depot
        visited_customers = {node for node in self.route if node != depot}
        required_customers = set(range(2, 2 + self.solver.instance.customers))
        if visited_customers != required_customers:
            self.is_valid = False
            return
        vehicle_count = self.route.count(depot) - 1 if self.route else 0
        if vehicle_count > self.solver.instance.vehicles:
            self.is_valid = False
            return
        self.is_valid = True

    def _evaluate(self):
        if not self.is_valid:
            self.fitness = float('inf')
            return
        self.fitness = self.solver.instance.calculate_route_distance(self.route)
    
    def crossover(self, other: 'CromossomoEVRP') -> 'CromossomoEVRP':
        if random.random() >= self.solver.config.crossover_rate:
            return self

        p1_genes, p2_genes = self.genes, other.genes
        size = len(p1_genes)
        if len(p2_genes) != size:
            p2_genes = (p2_genes * (size // len(p2_genes) + 1))[:size]

        child_genes = [None] * size
        start, end = sorted(random.sample(range(size), 2))
        child_genes[start:end] = p1_genes[start:end]
        segment = set(p1_genes[start:end])
        
        p2_genes_to_fill = [gene for gene in p2_genes if gene not in segment]
        
        fill_idx = 0
        for i in range(size):
            if child_genes[i] is None:
                if fill_idx < len(p2_genes_to_fill):
                    child_genes[i] = p2_genes_to_fill[fill_idx]
                    fill_idx += 1
                else:
                    all_genes = set(range(2, 2 + self.solver.instance.customers)) | {self.solver.instance.depot}
                    available = list(all_genes - set(filter(None, child_genes)))
                    child_genes[i] = random.choice(available) if available else self.solver.instance.depot
        return CromossomoEVRP(self.solver, child_genes)

    def mutate(self) -> 'CromossomoEVRP':
        if random.random() >= self.solver.config.mutation_rate:
            return self
        mutated_genes = self.genes.copy()
        if len(mutated_genes) < 2: return self
        if random.random() < 0.5:
            idx1, idx2 = random.sample(range(len(mutated_genes)), 2)
            mutated_genes[idx1], mutated_genes[idx2] = mutated_genes[idx2], mutated_genes[idx1]
        else:
            start, end = sorted(random.sample(range(len(mutated_genes)), 2))
            if start < end:
                mutated_genes[start:end] = mutated_genes[start:end][::-1]
        return CromossomoEVRP(self.solver, mutated_genes)

    def repair(self) -> 'CromossomoEVRP':
        if self.is_valid: return self
        depot = self.solver.instance.depot
        required_customers = set(range(2, 2 + self.solver.instance.customers))
        repaired_genes, visited_customers = [], set()
        for gene in self.genes:
            if gene != depot and gene in required_customers and gene not in visited_customers:
                repaired_genes.append(gene)
                visited_customers.add(gene)
        missing = required_customers - visited_customers
        repaired_genes.extend(list(missing))
        random.shuffle(repaired_genes)
        num_vehicles = self.solver.instance.vehicles
        if num_vehicles > 1 and len(repaired_genes) >= num_vehicles:
            num_splits = num_vehicles - 1
            split_points = sorted(random.sample(range(1, len(repaired_genes)), num_splits))
            for i, pos in enumerate(split_points):
                repaired_genes.insert(pos + i, depot)
        return CromossomoEVRP(self.solver, repaired_genes)


# --- Classe do Algoritmo Genético (com função de plotagem) ---
class AlgoritmoGeneticoEVRP:
    def __init__(self, filename: str, config: Optional[ConfigEVRP] = None):
        self.instance = InstanciaEVRP(filename)
        self.config = config if config else ConfigEVRP()
        self.evaluation_count = 0
        os.makedirs('results', exist_ok=True)
        os.makedirs('plots', exist_ok=True)
    
    def _initialize_population(self) -> List[CromossomoEVRP]:
        # (Implementação sem alterações)
        population = []
        for _ in range(self.config.pop_size * 5):
            if len(population) == self.config.pop_size: break
            chromosome = CromossomoEVRP(self)
            if chromosome.is_valid:
                population.append(chromosome)
        if not population:
            raise RuntimeError("Não foi possível inicializar uma população com indivíduos válidos.")
        return population

    def _select_parent(self, population: List[CromossomoEVRP]) -> CromossomoEVRP:
        # (Implementação sem alterações)
        tournament_size = min(self.config.tournament_size, len(population))
        tournament = random.sample(population, tournament_size)
        return min(tournament, key=lambda ind: ind.fitness)

    def run(self) -> Dict:
        # (Implementação com a chamada para a nova função de plotagem)
        all_runs_results = []
        n = self.instance.customers + 1 + self.instance.num_stations
        max_evaluations = 25000 * n
        
        for run_num in range(1, self.config.runs + 1):
            print(f"\n--- Execução {run_num}/{self.config.runs} para a instância {self.instance.name} ---")
            print(f"Orçamento de avaliações: {max_evaluations:,}")
            start_time = time.time()
            
            try:
                population = self._initialize_population()
                self.evaluation_count = len(population)
                best_solution_so_far = min(population, key=lambda ind: ind.fitness)
                stagnation_counter, run_history = 0, []
                
                progress_bar = tqdm(total=max_evaluations, desc="Avaliações", unit="eval", initial=self.evaluation_count)
                
                while self.evaluation_count < max_evaluations:
                    elite_size = max(1, int(self.config.elitism_rate * self.config.pop_size))
                    population.sort(key=lambda ind: ind.fitness)
                    next_generation = population[:elite_size]
                    
                    while len(next_generation) < self.config.pop_size:
                        p1, p2 = self._select_parent(population), self._select_parent(population)
                        child = p1.crossover(p2).mutate()
                        if not child.is_valid: child = child.repair()
                        self.evaluation_count += 1
                        progress_bar.update(1)
                        next_generation.append(child if child.is_valid else random.choice(population))
                        if self.evaluation_count >= max_evaluations: break
                    
                    population = next_generation
                    current_best_in_gen = min(population, key=lambda ind: ind.fitness)
                    if current_best_in_gen.fitness < best_solution_so_far.fitness:
                        best_solution_so_far = current_best_in_gen
                        stagnation_counter = 0
                    else:
                        stagnation_counter += 1
                    
                    if [ind.fitness for ind in population if ind.is_valid]: run_history.append(current_best_in_gen.fitness)
                    
                    if stagnation_counter >= self.config.max_stagnation:
                        print(f"\nEstagnação máxima ({self.config.max_stagnation}) atingida. Parando a execução.")
                        break
                
                progress_bar.close()
                exec_time = time.time() - start_time
                gap = (best_solution_so_far.fitness - self.instance.optimal_value) / self.instance.optimal_value * 100
                print(f"Melhor fitness encontrado: {best_solution_so_far.fitness:.4f} (Gap: {gap:.2f}%)")
                
                run_result = {'run': run_num, 'fitness': best_solution_so_far.fitness, 'gap': gap, 'time': exec_time, 'route': best_solution_so_far.route, 'history': run_history}
                all_runs_results.append(run_result)
                
                # Chamadas para salvar resultados e gráficos
                self._save_run_results(run_result)
                self._plot_convergence(run_result)
                self._plot_solution_routes(run_result) # <<< NOVA CHAMADA AQUI

            except (RuntimeError, ValueError) as e:
                print(f"Erro crítico na execução {run_num}: {e}")
                continue
        
        self._save_summary_results(all_runs_results)
        self._plot_comparison(all_runs_results)
        return self._analyze_final_results(all_runs_results)
    
    # --- Nova Função de Plotagem de Rota ---
    def _plot_solution_routes(self, result: Dict):
        """Gera um gráfico visual da melhor rota encontrada em uma execução."""
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # 1. Plotar todos os nós para dar contexto
        # Clientes
        customer_nodes = set(range(2, 2 + self.instance.customers))
        cust_coords = np.array([self.instance.coords[c] for c in customer_nodes])
        ax.scatter(cust_coords[:, 0], cust_coords[:, 1], c='skyblue', label='Clientes', s=50, zorder=3)
        
        # Estações de Recarga
        if self.instance.station_nodes:
            stat_coords = np.array([self.instance.coords[s] for s in self.instance.station_nodes])
            ax.scatter(stat_coords[:, 0], stat_coords[:, 1], c='lightgreen', marker='s', label='Estações', s=60, zorder=2)

        # Depósito
        depot_coord = self.instance.coords[self.instance.depot]
        ax.scatter(depot_coord[0], depot_coord[1], c='red', marker='*', label='Depósito', s=200, zorder=5)

        # 2. Plotar as rotas dos veículos
        vehicle_tours = self._split_route_into_vehicle_tours(result['route'])
        colors = plt.cm.jet(np.linspace(0, 1, len(vehicle_tours))) # Cores diferentes para cada veículo

        for i, tour in enumerate(vehicle_tours):
            tour_coords = np.array([self.instance.coords[node] for node in tour])
            ax.plot(tour_coords[:, 0], tour_coords[:, 1], color=colors[i], 
                    label=f'Veículo {i+1} (Dist: {self.instance.calculate_route_distance(tour):.2f})',
                    zorder=4)
            # Adicionar anotações de texto para os nós na rota
            for node_id in tour:
                if node_id != self.instance.depot:
                    ax.text(self.instance.coords[node_id][0], self.instance.coords[node_id][1] + 1, str(node_id), fontsize=9)

        # 3. Configurações do Gráfico
        ax.set_title(f"Melhor Rota da Execução {result['run']} - {self.instance.name}\nFitness Total: {result['fitness']:.2f}", fontsize=16)
        ax.set_xlabel("Coordenada X")
        ax.set_ylabel("Coordenada Y")
        ax.legend(loc='best', bbox_to_anchor=(1, 1))
        ax.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()
        
        # Salvar o gráfico em um arquivo
        filename = f"plots/route_{self.instance.name}_run{result['run']}.png"
        plt.savefig(filename)
        plt.close(fig)
        print(f"Gráfico da melhor rota salvo em: {filename}")


    def _split_route_into_vehicle_tours(self, route: List[int]) -> List[List[int]]:
        # (Implementação sem alterações)
        tours, current_tour = [], []
        for node in route:
            current_tour.append(node)
            if len(current_tour) > 1 and node == self.instance.depot:
                tours.append(current_tour)
                current_tour = [self.instance.depot]
        return tours

    def _save_run_results(self, result: Dict):
        # (Implementação sem alterações)
        filename = f"results/{self.instance.name}_run{result['run']}.txt"
        with open(filename, 'w') as f:
            f.write(f"Resultados para Instância: {self.instance.name} - Execução {result['run']}\n"
                    f"{'='*40}\n"
                    f"Fitness Final: {result['fitness']:.4f}\n"
                    f"Gap Percentual: {result['gap']:.2f}%\n"
                    f"Tempo de Execução: {result['time']:.2f}s\n\n"
                    "Melhor Rota Encontrada:\n")
            vehicle_tours = self._split_route_into_vehicle_tours(result['route'])
            f.write(f"Total de Veículos Usados: {len(vehicle_tours)}\n")
            for i, tour in enumerate(vehicle_tours, 1):
                dist = self.instance.calculate_route_distance(tour)
                f.write(f"  Veículo {i}: {' -> '.join(map(str, tour))} (Distância: {dist:.2f})\n")

    def _plot_convergence(self, result: Dict):
        # (Implementação sem alterações)
        plt.figure(figsize=(12, 7))
        plt.plot(result['history'], label='Melhor Fitness por Geração')
        plt.axhline(y=self.instance.optimal_value, color='r', linestyle='--', label=f'Ótimo Conhecido ({self.instance.optimal_value:.2f})')
        plt.xlabel('Geração')
        plt.ylabel('Distância Total (Fitness)')
        plt.title(f"Convergência do AG - {self.instance.name} (Execução {result['run']})")
        plt.legend()
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(f"plots/convergence_{self.instance.name}_run{result['run']}.png")
        plt.close()
    
    def _save_summary_results(self, results: List[Dict]):
        # (Implementação sem alterações)
        if not results: return
        filename = f"results/summary_{self.instance.name}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['run', 'fitness', 'gap', 'time'])
            writer.writeheader()
            for res in results:
                writer.writerow({'run': res['run'], 'fitness': f"{res['fitness']:.4f}", 'gap': f"{res['gap']:.2f}", 'time': f"{res['time']:.2f}"})
        print(f"\nResumo salvo em: {filename}")
    
    def _plot_comparison(self, results: List[Dict]):
        # (Implementação sem alterações)
        if not results: return
        plt.figure(figsize=(12, 7))
        for res in results: plt.plot(res['history'], alpha=0.6)
        plt.axhline(y=self.instance.optimal_value, color='r', linestyle='--', linewidth=2, label=f'Ótimo Conhecido ({self.instance.optimal_value:.2f})')
        plt.xlabel('Geração')
        plt.ylabel('Distância Total (Fitness)')
        plt.title(f'Comparativo de Convergência (Todas as {len(results)} execuções) - {self.instance.name}')
        plt.legend()
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(f'plots/comparison_{self.instance.name}.png')
        plt.close()

    def _analyze_final_results(self, results: List[Dict]) -> Dict:
        # (Implementação sem alterações)
        if not results: return {}
        
        fitnesses, gaps, times = [r['fitness'] for r in results], [r['gap'] for r in results], [r['time'] for r in results]
        best_run = min(results, key=lambda r: r['fitness'])
        
        print("\n" + "="*25 + " Análise Final Consolidada " + "="*25)
        print(f"Instância: {self.instance.name}")
        print(f"Execuções: {len(results)}")
        print(f"Melhor fitness (Mínimo): {min(fitnesses):.4f} (Execução {best_run['run']})")
        print(f"Pior fitness (Máximo): {max(fitnesses):.4f}")
        print(f"Média de fitness: {np.mean(fitnesses):.4f}")
        print(f"Desvio Padrão (stdev): {np.std(fitnesses):.4f}")
        print(f"Média de Gap: {np.mean(gaps):.2f}%")
        print(f"Média de tempo/execução: {np.mean(times):.2f}s")
        print("="*75)
        
        return {'best_overall_fitness': best_run['fitness'], 'best_route': best_run['route']}

# --- Função Principal (sem alterações) ---
def main():
    config = ConfigEVRP(runs=20)
    instance_files = ["E-n23-k3.evrp", "E-n51-k5.evrp"] 
    
    for instance_file in instance_files:
        if not os.path.exists(instance_file):
            print(f"AVISO: Arquivo da instância '{instance_file}' não encontrado. Pulando...")
            continue
        try:
            solver = AlgoritmoGeneticoEVRP(filename=instance_file, config=config)
            solver.run()
        except (ValueError, RuntimeError) as e:
            print(f"\nERRO FATAL ao processar {instance_file}: {e}")

if __name__ == "__main__":
    main()
