import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def plotGraph(graph, color_map):
  # Fixe as posições dos nós usando spring_layout
  fixed_layout = nx.spring_layout(graph, seed=42)

  # Plote o grafo
  plt.figure(figsize=(10, 10))
  nx.draw(graph, pos=fixed_layout, with_labels=True, node_size=1000, node_color=color_map, font_size=10)
  plt.title("Grafo do Tabuleiro constxconst (Não Direcionado)")
  plt.show()

def make_graph(N):
  # Crie um grafo não direcionado
  G = nx.Graph()
  
  # Adicione vértices ao grafo
  for i in range(N):
      for j in range(N):
          vertex = (i, j)
          G.add_node(vertex)
  
  # Adicione arestas horizontais e verticais
  for i in range(N):
      for j in range(N):
          for k in range(j + 1, N):
              G.add_edge((i, j), (i, k))  # arestas horizontais
              G.add_edge((j, i), (k, i))  # arestas verticais
  
  # Adicione arestas nas diagonais
  for i in range(N):
      for j in range(N):
          for k in range(1, min(N - i, N - j)):
              G.add_edge((i, j), (i + k, j + k))  # diagonal principal
  
          for k in range(1, min(N - i, j + 1)):
              G.add_edge((i, j), (i + k, j - k))  # diagonal secundária
  
  return G

def preprocess_graph(graph, initial_vertex):
  visited = set()
  queue = deque([initial_vertex])

  while queue:
      vertex = queue.popleft()

      # Verifica se o  vertice atual ja foi visitado
      if vertex not in visited:
          visited.add(vertex)
          queue.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)

  # Retorna uma deque contendo os vértices visitados durante a travessia em largura,
  # convertendo o conjunto de vértices visitados para uma lista antes de criar a deque.
  return deque(list(visited))

def queens_placement_bfs(graph, target_node, numQueens, solution, color_map, q, colored_nodes):
  global cont  # Declare a variável cont como global
  
  # Encontre o índice do nó de destino
  target_index = list(graph.nodes).index(target_node)
  
  # Mude a cor do nó de destino para 'yellow'
  color_map[target_index] = 'yellow'
  solution.append(target_node)
  # plotGraph(G, color_map)
  
  colored_nodes += 1
  
  numQueens += 1
  # Verifica se já foi encontrada uma solução
  if numQueens == N:
      cont += 1
      # plotGraph(G, color_map)
      print(cont, solution, "\n")
      solution.pop()
      return
  
  # Encontre todos os vizinhos do nó de destino
  neighbors = set(graph.neighbors(target_node))
  
  # Mude a cor de todos os vizinhos para 'green'
  for neighbor in neighbors:
      neighbor_index = list(graph.nodes).index(neighbor)
  
      if color_map[neighbor_index] == 'skyblue':
          color_map[neighbor_index] = 'green'
          colored_nodes += 1
  
  # plotGraph(G, color_map)
  
  # Caso o número de vértices azuis seja menor que o número de rainhas a serem adicionadas, a solução é impossível.
  if ((N * N) - colored_nodes < N - numQueens):
      solution.pop()
      return
  
  # Marca o vértice verificado e seus vizinhos como visitados
  visited = set(neighbors)
  visited.add(target_node)
  
  queue = deque(q)  # Criando uma cópia independente
  
  while queue:
      vertex = queue.popleft()
  
      # Verifica se o vértice atual já foi visitado
      if vertex not in visited:
          visited.add(vertex)
          vertex_index = list(graph.nodes).index(vertex)
  
          # Verifica se o vértice atual é azul e se o vértice possui uma posição à direita em relação ao vértice da última rainha colocada no tabuleiro.
          if color_map[vertex_index] == 'skyblue' and target_node[0] + 1 == vertex[0]:
              queens_placement_bfs(graph, vertex, numQueens, solution, color_map[:], q, colored_nodes)
  
  solution.pop()

N = 8
cont = 0

# Cria um grafo não direcionado
G = make_graph(N)

# Cria uma fila auxiliar para auxiliar o caminhamento no grafo
aux_queue = preprocess_graph(G, (0,0))

for i in range(N):
      # Seleciona o local inicial onde será inserido uma rainha
      initial_node = (0, i)

      # Crie um mapa de cores, inicialmente com todas as cores como 'skyblue'
      color_map = ['skyblue'] * nx.number_of_nodes(G)

      # Chama a função para buscar as soluções do problema das n-Queens
      queens_placement_bfs(G, initial_node, 0, [], color_map, aux_queue, 0)