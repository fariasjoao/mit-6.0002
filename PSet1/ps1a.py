###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """ 
    # Inicializa o dicionário chamada data para colocar os dados do arquivo de texto
    data = {}

    # Abre o arquivo e lê suas informações
    with open(filename, "r", encoding="utf-8") as file:
        for row in file:
            # Coloca as informações da linha do documento nas variáveis name e weight
            # O módulo .strip() funciona para retirar possíveis espaços e quebras de linhas
            # O módulo .split serve para separar a string da linha na metade a cada vírgula, separando o nome do peso
            name, weight = row.strip().split(",")

            # coloca as variáveis name e weight no dicionário data, além de transformar weight em int
            data[name] = int(weight)

    return data

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    # Organiza os dados do data baseado no maior peso e coloca em um novo dicionário chamado data_organized
    data_organized = dict(sorted(cows.items(), key=lambda item: item[1], reverse=True))

    # Uma lista que irá conter, no futuro, todas as viagens uma por uma 
    all_trips =  []


    # Percorrer o número do tamanho do dicionário organizado, afinal se o dicionário tiver 5 vacas e todas estiverem 
    # com o peso próximo do limite, seria necessário fazer 5 viagens
    while data_organized:
        # Uma lista que irá conter as vacas de uma viagem
        trip = []
        # Uma variável que irá conter o peso total da viagem
        total_weight = 0

        # Percorrer por todas as vacas do dicionário organizado, e colocar as vacas na viagem enquanto o peso total da
        # viagem mais o peso da vaca atual for menor ou igual ao limite
        for name, weight in data_organized.copy().items():
            # O nome da vaca não pode estar na lista de nomes usados, pois assim ela já foi transportada
            if total_weight + weight <= limit:
                # Adiciona o nome da vaca na viagem
                trip.append(name)
                # Adiciona o peso da vaca ao peso total da viagem
                total_weight += weight
                # Remove a vaca do dicionário organizado, pois ela já foi transportada
                del data_organized[name]
            # Caso o peso da vaca seja maior que o limite, imprime um aviso de que a vaca não pode ser transportada
            elif weight > limit:
                print(f"Warning: Cow {name} has a weight of {weight} which exceeds the limit of {limit}. This cow cannot be transported.")

  
        all_trips.append(trip) 

    return all_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    data = get_partitions(cows)
    # Uma variável que irá conter o menor número de viagens possíveis encontradas
    # A variável é inicializada com o valor infinito, pois qualquer número de viagens encontrado será menor que infinito
    best_num_trips = float('inf')
    # Busca todas as partições possíveis com os dados do dicionário cows, e coloca em uma variável chamada data
    for partition in data:
        # Cria um loop para percorrer todas as viagens possíveis da partição atual
        for trip in partition:
            # Caso falso, não há necessidade de pular para a próxima partição, pois a partição atual é válida
            skip_external = False            
            total_weight = sum(cows[cow] for cow in trip)
            # Caso o peso total da viagem seja maior que o limite, pula para a próxima partição
            if total_weight > limit:
                skip_external = True
                break

        # Caso seja True, pula para a próxima partição, pois a partição atual é inválida
        if skip_external:
            continue
        # Caso contrário, a partição atual é válida, então podemos usar ela
        num_trips = len(partition)
        # Se o número de viagens da partição atual for menor que o melhor número de viagens encontrado até agora, atualiza 
        # o melhor número de viagens
        if num_trips < best_num_trips:
            best_num_trips = num_trips
            # Atualiza a  melhor partição encontrada até agora
            best_partition = partition

    return best_partition
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # Abre um arquivo de texto e coloca todas as informações em um dicionário
    cows = load_cows("ps1_cow_data.txt")

    # Começa a contagem do tempo para a função greedy_cow_transport
    start_time_greedy = time.time()
    # Chama a função greedy_cow_transport
    greedy_result = greedy_cow_transport(cows, limit=10)
    print(greedy_result)
    # Termina a contagem do tempo para a função greedy_cow_transport
    end_time_greedy = time.time()
    print(f"Greedy algorithm time: {end_time_greedy - start_time_greedy:.6f} seconds")

    # Começa a contagem do tempo para a função brute_force_cow_transport
    start_time_brute = time.time()
    # Chama a função brute_force_cow_transport
    brute_force_result = brute_force_cow_transport(cows, limit=10)
    print(brute_force_result)
    # Termina a contagem do tempo para a função brute_force_cow_transport
    end_time_brute = time.time()
    print(f"Brute force algorithm time: {end_time_brute - start_time_brute:.6f} seconds")


compare_cow_transport_algorithms()