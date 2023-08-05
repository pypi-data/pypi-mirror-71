# packages
import numpy as np

WEIGTH = 2


def count_species(hist):
    specie = 0
    for i in range(len(hist)):
        if (hist[i] > 0):
            specie += 1
    return specie


def exclude_species(hist):
    new_histogram = []

    for i in range(len(hist)):
        if (hist[i] > 0):
            new_histogram.append(hist[i])

    return new_histogram


def diversity_index2D(hist):

    new_histogram = exclude_species(hist)
    # acumula a soma entre as distances e abundância de especies i e j
    sum_ = 0
    # recebe o total de especie
    amount_specie = count_species(new_histogram)

    for i in range(len(new_histogram)):
        for j in range(1, len(new_histogram)):
            if i == 0 and j == 1:
                distance = (j-i)+1
            else:
                distance = (j-i)+2

            product = distance*new_histogram[i]*new_histogram[j]
            sum_ += product

    if amount_specie > 1:

        index = sum_/((amount_specie*(amount_specie-1))/2)

    else:

        index = 0

    return index


def distinction_index2D(hist):

    new_histogram = exclude_species(hist)

    # acumula a soma entre as distances e abundância de especies i e j
    sum_1 = 0
    # acumula a soma entre a abundância de especies i e j
    sum_2 = 0
    # recebe o total de especie
    amount_specie = count_species(new_histogram)

    for i in range(len(new_histogram)):
        for j in range(1, len(new_histogram)):
            if i == 0 and j == 1:
                distance = (j-i)+1
            else:
                distance = (j-i)+2

            product = distance*new_histogram[i]*new_histogram[j]
            sum_1 += product
            sum_2 += new_histogram[i]*new_histogram[j]

    if sum_2 > 0:

        index = sum_1/sum_2

    else:

        index = 0

    return index

# baseado em riqueza de especies


def diversity_index(hist):
    """Esta função retorna o indice de diversidade da imagem"""

    # acumula a soma entre as distances e abundância de especies i e j
    summation = 0

    for i in range(len(hist)):
        if hist[i] == 0:
            continue
        for j in range(1, len(hist)):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            produto = distance*hist[i]*hist[j]
            summation += produto

    bin_central = len(hist)//2
    n = len(hist)*bin_central

    if n == 0:
        indice = 0
    else:
        indice = summation/n

    return indice


def distinction_index(hist):
    """Esta função retorna o indice de distinção da imagem"""

    # acumula a soma entre as distances e abundância de especies i e j
    summation1 = 0
    # acumula a soma entre a abundância de especies i e j
    summation2 = 0

    for i in range(len(hist)):
        if hist[i] == 0:
            continue
        for j in range(1, len(hist)):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            mult = distance*hist[i]*hist[j]
            summation1 += mult
            abun = hist[i]*hist[j]
            summation2 += abun

    if summation2 == 0:
        indice = 0
    else:
        indice = summation1/summation2

    return indice

# baseado na distance entre pares de espécies


def intensive_quadratic_entropy(hist):  # ok
    """Esta função retorna o indice de entropia quadratica intensiva (J) da imagem"""

    num_especies = len(hist)
    # acumula a soma entre as distances i, j
    summation = 0
    num_especies_null = 0
    # recebe o total de especie

    for i in range(num_especies):
        if hist[i] == 0:
            num_especies_null += 1
            continue
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            summation += distance

    # calculo das distances entre os pares, dividido pelo total_especie^2
    S = pow((num_especies-num_especies_null), 2)

    if S == 0:
        indiceJ = 0
    else:
        indiceJ = summation/S

    return indiceJ


def extensive_quadratic_entropy(hist):  # ok
    """Esta função retorna o indice de entropia quadratica extensiva (F) da imagem"""

    num_especies = len(hist)
    # acumula a soma entre as distances i, j
    summation = 0
    num_especies_null = 0

    for i in range(num_especies):
        if hist[i] == 0:
            num_especies_null += 1
            continue
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            summation += distance

    return summation


def average_taxonomic_distinction(hist):  # ok
    """Esta função retorna o indice de distinção taxonomica média (AvTD) da imagem"""

    num_especies = len(hist)
    # acumula a soma entre as distances de especies i e j
    summation = 0
    num_especies_null = 0

    for i in range(num_especies):
        if hist[i] == 0:
            num_especies_null += 1
            continue
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            summation += distance

    s = num_especies-num_especies_null

    if ((s*(s-1))/2) == 0:
        indiceAvTD = 0
    else:
        indiceAvTD = summation/((s*(s-1))/2)

    return indiceAvTD


def total_taxonomic_distinction(hist):  # ok
    """Esta função retorna o indice de distinção taxonomica total (TTD) da imagem"""

    num_especies = len(hist)
    # acumula a soma entre as distances de especies i e j
    summation = 0
    num_especies_null = 0

    for i in range(num_especies):
        if hist[i] == 0:
            num_especies_null += 1
            continue
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            summation += distance

    s = num_especies-num_especies_null

    if (s-1) == 0:
        indiceTTD = 0
    else:
        indiceTTD = summation/(s-1)

    return indiceTTD


def diversidadePura(hist):  # ok
    """Esta função retorna o indice de diversidade pura (DD) da imagem"""

    num_especies = len(hist)
    # acumula a soma entre as distances de especies i e j
    summation = 0

    for i in range(num_especies):
        if hist[i] == 0:
            continue
        minimun = 9999999
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*((j - i) + 1)
            elif j < i:
                distance = WEIGTH*((i - j) + 2)
            else:
                distance = WEIGTH*((j - i) + 2)

            if distance < minimun:
                minimun = distance

        summation += minimun

    return summation

# baseado em topologia


def index_q(hist):  # ok
    """Esta função retorna o indice Q da imagem"""

    num_especies = len(hist)
    raiz = len(hist) - 1
    #raiz = num_especies//2
    sumdistances = 0
    sumdistances2 = 0

    # calcula o somario total das distances de todas as especies para a raiz
    for i in range(0, num_especies):
        if hist[i] == 0:
            continue
        if i == raiz:
            continue

        if i == 0:
            sumdistances += WEIGTH*(raiz - i)
        else:
            sumdistances += WEIGTH*((raiz - i)+1)

    for i in range(0, num_especies):
        if hist[i] == 0:
            continue
        if i == raiz:
            continue

        dis1 = WEIGTH*(raiz - i)
        dis2 = WEIGTH*((raiz - i) + 1)
        if dis2 != 0:
            if i == 0:
                sumdistances2 += sumdistances/dis1
            elif i != raiz:
                sumdistances2 += sumdistances/dis2

    return sumdistances2


def index_w(hist):  # ok
    """Esta função retorna o indice W da imagem"""

    num_especies = len(hist)
    sumdistances = 0
    sumdistances2 = 0
    #raiz = num_especies//2
    raiz = num_especies - 1

    # calcula o somario total das distances de todas as especies para a raiz
    for i in range(0, num_especies):
        if hist[i] == 0:
            continue
        if i == raiz:
            continue

        if i == 0:
            sumdistances += WEIGTH*(raiz - i)
        else:
            sumdistances += WEIGTH*((raiz - i)+1)

    Qmin = 999999
    # busca o Qmin value
    for i in range(0, num_especies):
        if hist[i] == 0:
            continue
        if i == raiz:
            continue

        dis1 = WEIGTH*(raiz - i)
        dis2 = WEIGTH*((raiz - i) + 1)

        if dis2 != 0:
            if i == 0:
                aux = sumdistances/dis1
            elif i != raiz:
                aux = sumdistances/dis2

            if aux < Qmin:
                Qmin = aux

    # calcula o summation de Qi/Qmin, onde, Qi representa a diferenca entre a
    # sumdistances por a distance da folha i para raiz
    for i in range(0, num_especies):
        # se a especie nao tiver individuos passa para a proxima
        if hist[i] == 0:
            continue
        if i == raiz:
            continue

        dis1 = WEIGTH*(raiz - i)
        dis2 = WEIGTH*((raiz - i) + 1)

        if dis2 != 0:
            if i == 0:
                sumdistances2 += (sumdistances/dis1)/Qmin
            elif i != raiz:  # se for igual a raiz é zero, e nao precisa ser computada
                sumdistances2 += (sumdistances/dis2)/Qmin

    return sumdistances2

# baseado em caminho minimo


def index_pd_node(hist):  # ok
    """Esta função retorna o indice PDNode da imagem"""

    somadistances = 0
    num_especies = len(hist)

    # calcula a distance de todas as especies para os demais, sempre conservando a menor de todas
    for i in range(num_especies):
        if hist[i] == 0:
            continue
        minimun = 9999999
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*(j - i)
            elif j < i:
                distance = WEIGTH*((i - j) + 1)
            else:
                distance = WEIGTH*((j - i) + 1)

            if distance < minimun:
                minimun = distance

        somadistances += minimun

    return somadistances


def index_pd_root(hist):  # ok
    """Esta função retorna o indice PDRoot da imagem"""

    WEIGTH = 2
    num_especies = len(hist)
    raiz = num_especies - 1
    #raiz = num_especies//2
    sumdistances = 0

    # calcula o somatório total das distances de todas as especies para a raiz
    for i in range(num_especies):
        if hist[i] == 0:
            continue
        if i == raiz:
            continue

        if i == 0:
            sumdistances += WEIGTH*(raiz - i)
        else:
            sumdistances += WEIGTH*((raiz - i) + 1)

    return sumdistances


def index_pd_tree(hist):  # ok
    """Esta função retorna o indice AvPD da imagem"""

    num_especies = len(hist)
    num_especies_null = 0
    somadistances = 0

    # calcula a distance de todas as especies para os demais, sempre conservando a menor de todas
    for i in range(num_especies):
        if hist[i] == 0:
            num_especies_null += 1
            continue
        minimun = 9999999
        for j in range(num_especies):
            if hist[j] == 0:
                continue

            if i == j:
                continue

            if j == 0:
                distance = WEIGTH*(j - i)
            elif j < i:
                distance = WEIGTH*((i - j) + 1)
            else:
                distance = WEIGTH*((j - i) + 1)

            if distance < minimun:
                minimun = distance

        somadistances += minimun

    return somadistances/(num_especies-num_especies_null)


def get_phylogenetic_indexes(hist):

    diversity = diversity_index(hist)

    distinction = distinction_index(hist)

    indexJ = intensive_quadratic_entropy(hist)

    indexF = extensive_quadratic_entropy(hist)

    AvTD = average_taxonomic_distinction(hist)

    TTD = total_taxonomic_distinction(hist)

    DD = diversidadePura(hist)

    indexQ = index_q(hist)

    indexW = index_w(hist)

    PDNode = index_pd_node(hist)

    PDRoot = index_pd_root(hist)

    AvPD = index_pd_tree(hist)

    return [diversity, distinction, indexJ, indexF, AvTD, TTD, DD, indexQ, indexW, PDNode, PDRoot, AvPD]


def get_taxonomic_indexes(hist):

    diversity = diversity_index(hist)

    distinction = distinction_index(hist)

    AvTD = average_taxonomic_distinction(hist)

    TTD = total_taxonomic_distinction(hist)

    DD = diversidadePura(hist)

    return [diversity, distinction, AvTD, TTD, DD]
