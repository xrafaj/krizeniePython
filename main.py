import random

POCET_JEDINCOV = 250
CURRENT_BEST_FITNESS = 0
CURRENT_BEST_JEDINEC = []
selection = '1'
elitarism = '0'
pop_count = 80


class Poklad(object):                                       # Trieda na inicializaciu pokladu
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Mapa(object):                                          # Trieda ktora otvara a spracuje mapu
    def __init__(self):                                      # a obsahuje instancie pokladu
        temp = 0
        self.poklady = []
        f = open("mapa.txt", "r")                            # Otvorenie suboru
        data = f.read().split('\n')                          # Oddelenie riadkov
        for i in range(7):                                   # Cyklus na spracovanie mapy iba 7x7
            for j in range(7):
                if data[i][j] == 'x':
                    temp = temp + 1
                    self.poklady.append(Poklad(i, j))
        f.close()

    def get_poklady(self):              # Metoda, ktora vracia poklady
        return self.poklady

    def is_this_poklad(self, x, y):     # Metoda, ktora urcuje, ci zadane X a Y obhasuju poklad, ak sa najde, vymaze sa
        for i in range(len(self.poklady)):
            if self.poklady[i].x == x and self.poklady[i].y == y:
                self.poklady.pop(i)
                if len(self.poklady) == 0:
                    return 2
                return 1
        return 0


class Jedinec(object):                  # Trieda ktora obsahuje FITNESS a data / pamat (64 buniek) Jedinca
    def __init__(self):
        self.vFitness = 1000
        self.data_set = []
        for i in range(64):
            self.data_set.append(random.randint(0, 255))

    def mutation(self):                 # Gettery, settery a mutacna funkcia
        self.data_set[random.randint(0, 63)] = random.randint(0, 255)

    def myfunc(self):                   # Vypis jedincovej
        print(self.data_set)

    def return_init(self):
        return self

    def get_bunka(self, i):
        return self.data_set[i]

    def return_data(self):
        return self.data_set

    def set_data(self, data):
        self.data_set = data

    def set_bunka(self, x, i):
        self.data_set[x] = i

    def fitness_move(self):
        self.vFitness = self.vFitness - 1

    def fitness_found(self):
        self.vFitness = self.vFitness + 1000

    def get_fitness(self):
        return self.vFitness


def search_solution(jedinec_local, vypis):          # Virtualny stroj
    global CURRENT_BEST_FITNESS                     # Uchovanie doposial najlepsieho fitness-u
    global CURRENT_BEST_JEDINEC                     # Uchovanie doposial dataset-u jedinca s najlepsim fitness
    dataset = []
    for i in range(64):                             # Ulozenie este nepozmenej datovej konfiguracie jedinca
        dataset.append(jedinec_local.get_bunka(i))

    inc = 0                                         # 0000 00000
    dec = 64                                        # 0100 00000
    jmp = 128                                       # 1000 00000
    pnt = 192                                       # 1100 00000
    max_instructions = 500                          # Urcenie MAX poctu instrukcii
    counter = 0                                     # Pomocne premenne
    current_index = 0
    mapa = Mapa()                                   # Nacitanie mapy a jej pokladov

    starting_x = 6                                  # Definicia startovnej pozicie
    starting_y = 3

    while counter < max_instructions:               # While cyklus do 500 ( max pocet instr. )
        counter = counter + 1
        current = jedinec_local.get_bunka(current_index)        # Ziskanie jedinca na aktualnom indexe
        current_index = current_index + 1                       # Inkrementacia / doprava posun / v stroji
        if current_index >= 63:                                 # AK prideme na koniec, vratime sa na zaciatok
            current_index = 0                                   # teda nekoncime
        operative = current & 192                               # 1100 0000
        number_of_bunka = current & 63                          # 0011 1111
        if str(operative) == str(inc):                          # Inkrementacia
            value = jedinec_local.get_bunka(number_of_bunka)
            value = value + 1
            if value > 255:
                value = 0
            jedinec_local.set_bunka(number_of_bunka, value)
        if str(operative) == str(dec):                          # Dekrementacia
            value = jedinec_local.get_bunka(number_of_bunka)
            value = value - 1
            if value < 0:
                value = 255
            jedinec_local.set_bunka(number_of_bunka, value)
        if str(operative) == str(jmp):                          # Jump
            current_index = number_of_bunka
        if str(operative) == str(pnt):                          # Print
            value = jedinec_local.get_bunka(number_of_bunka)
            value = value % 4                                   # Riesime posledne 2 bity { 00 01 10 11 } a na zaklade
            if value == 0:                                      # toho sa pohybujeme UP DOWN RIGHT LEFT
                if vypis is True:
                    print("U")
                jedinec_local.fitness_move()                             # Dekrementacia fitness o 1
                starting_x = starting_x - 1
                if starting_x < 0:                                      # 4x osetrenie vybocenie z mapy
                    if vypis is True:
                        print('Out of range.')
                    break
                temp = mapa.is_this_poklad(starting_x, starting_y)      # Kontrola, ci nie je poklad
                if temp == 1:
                    jedinec_local.fitness_found()                        # Inkrementacia fintes o 1000
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                if temp == 2:
                    jedinec_local.fitness_found()                        # Ukoncenie programu
                    jedinec_local.set_data(dataset)                     # ak islo o posledny poklad a u ostatnych
                    if vypis is True:                                   # DOWN, RIGHT, LEFT je logika rovnaka
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                        print('Najdene vsetky poklady. Koncim program.')
                    return 2
            if value == 1:
                if vypis is True:
                    print("D")
                jedinec_local.fitness_move()
                starting_x = starting_x + 1
                if starting_x > 6:
                    if vypis is True:
                        print('Out of range.')
                    break
                temp = mapa.is_this_poklad(starting_x, starting_y)
                if temp == 1:
                    jedinec_local.fitness_found()
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                if temp == 2:
                    jedinec_local.fitness_found()
                    jedinec_local.set_data(dataset)
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                        print('Najdene vsetky poklady. Koncim program.')
                    return 2
            if value == 2:
                if vypis is True:
                    print("R")
                jedinec_local.fitness_move()
                starting_y = starting_y + 1
                if starting_y > 6:
                    if vypis is True:
                        print('Out of range.')
                    break
                temp = mapa.is_this_poklad(starting_x, starting_y)
                if temp == 1:
                    jedinec_local.fitness_found()
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                if temp == 2:
                    jedinec_local.fitness_found()
                    jedinec_local.set_data(dataset)
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                        print('Najdene vsetky poklady. Koncim program.')
                    return 2
            if value == 3:
                if vypis is True:
                    print("L")
                jedinec_local.fitness_move()
                starting_y = starting_y - 1
                if starting_y < 0:
                    if vypis is True:
                        print('Out of range.')
                    break
                temp = mapa.is_this_poklad(starting_x, starting_y)
                if temp == 1:
                    jedinec_local.fitness_found()
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                if temp == 2:
                    jedinec_local.fitness_found()
                    jedinec_local.set_data(dataset)
                    if vypis is True:
                        print('Poklad X '+str(starting_x+1)+' Y '+str(starting_y+1))
                        print('Najdene vsetky poklady. Koncim program.')
                    return 2

    if counter == 500:                  # V pripade, ze sme dosli nakoniec poctu instrukcii, koncime stroj. hladanie
        if vypis is True:
            print('Reached max')

    if CURRENT_BEST_FITNESS < jedinec_local.get_fitness():       # Update best jedinca doposial
        CURRENT_BEST_FITNESS = jedinec_local.get_fitness()
        CURRENT_BEST_JEDINEC = dataset

    jedinec_local.set_data(dataset)                             # Navrat nezmeneneho datasetu do objektu Jedinca


def krizenie(temp_population, argument, elity):                 # Funkcia krizenie a generovanie novych populacii
    new_population = []
    maximum = -1
    dataset1 = []
    dataset2 = []
    cnt = 0
    for i in range(POCET_JEDINCOV):                             # Ulozenie fitnes a indexov
        dataset1.append(str(i))
        dataset2.append(temp_population[i].get_fitness())

    dataset = zip(dataset2, dataset1)
    dataset_vr = [x for _, x in (sorted(dataset))]              # Sortnutie jedincov pre zmysel elit

    amount_of_elites = 0
    if elity == '1':                                            # V pripade povolenych elit, priblizne 10%
        amount_of_elites = len(temp_population) // 10

    elity_array = []                                            # Naplnenie novej populacie predoslymi elitami
    if amount_of_elites > 0:
        while cnt < amount_of_elites:
            elity_array.append(dataset_vr[-1-cnt])
            cnt = cnt + 1

    for i in range(POCET_JEDINCOV):                             # Zistenie maxima
        if maximum < temp_population[i].get_fitness():
            maximum = temp_population[i].get_fitness()

    if argument == 1:                                           # Pripad 1 - Ruleta
        ruleta = []

        for i in range(POCET_JEDINCOV):                         # Kazdemu jedincovi
            temp_jedinec = temp_population[i].return_init()     # dame cast rulety podla jeho fitness
            fitnes = temp_jedinec.get_fitness() / maximum
            fitnes = fitnes * 70
            fitnes = round(fitnes)
            for k in range(fitnes):
                ruleta.append(temp_jedinec)

        for k in range(POCET_JEDINCOV):                         # vyberieme nahodnych rodicov
            size_of = len(ruleta)                               # z rulety a nasledne vytvorime
            size_of = size_of - 1                               # krizenca
            r1 = random.randint(0, size_of)
            r2 = random.randint(0, size_of)
            rodic_1 = ruleta[r1]
            rodic_2 = ruleta[r2]
            krizenec = Jedinec()

            how_much_parent1 = random.randint(0, 63)            # Cast, kde urcime aku cast tvori rodic 1 a rodic 2

            for i in range(how_much_parent1 - amount_of_elites):      # Samotne zaplnenie hodnot krizenca
                krizenec.set_bunka(i + amount_of_elites, rodic_1.data_set[i + amount_of_elites])
            for i in range(64-how_much_parent1 - amount_of_elites):
                krizenec.set_bunka(i + how_much_parent1 + amount_of_elites,
                                   rodic_2.data_set[i + how_much_parent1 + amount_of_elites])

            if random.randint(1, 100) < 5:                      # 5% šanca mutácie
                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

            new_population.append(krizenec)                     # Pridame krizenca do populacie

    if argument == 2:
        for i in range(POCET_JEDINCOV):                         # Vyberieme 3 jedincov nahodne
            parent1 = temp_population[random.randint(0, POCET_JEDINCOV-1)]
            parent2 = temp_population[random.randint(0, POCET_JEDINCOV-1)]
            parent3 = temp_population[random.randint(0, POCET_JEDINCOV-1)]

            if parent1.get_fitness() < parent2.get_fitness() and parent3.get_fitness() < parent2.get_fitness():
                final_parent1 = parent2
            elif parent1.get_fitness() < parent3.get_fitness():
                final_parent1 = parent3
            else:
                final_parent1 = parent1                         # Najlepsi z nich je rodic 1

            parent1 = temp_population[random.randint(0, POCET_JEDINCOV-1)]
            parent2 = temp_population[random.randint(0, POCET_JEDINCOV-1)]
            parent3 = temp_population[random.randint(0, POCET_JEDINCOV-1)]

            if parent1.get_fitness() < parent2.get_fitness() and parent3.get_fitness() < parent2.get_fitness():
                final_parent2 = parent2
            elif parent1.get_fitness() < parent3.get_fitness():
                final_parent2 = parent3
            else:
                final_parent2 = parent1                         # Obdobny postup, najlepsi z nich je rodic 2

            krizenec = Jedinec()

            how_much_parent1 = random.randint(0, 63)            # Cast, kde urcime aku cast tvori rodic 1 a rodic 2

            for k in range(how_much_parent1 - amount_of_elites):
                krizenec.set_bunka(k + amount_of_elites, final_parent1.data_set[k + amount_of_elites])
            for k in range(64 - how_much_parent1 - amount_of_elites):
                krizenec.set_bunka(k + how_much_parent1 + amount_of_elites,
                                   final_parent2.data_set[k + how_much_parent1 + amount_of_elites])

            if random.randint(1, 100) < 5:                      # Sanca mutacie 5%
                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

                index = random.randint(0, 63)
                local_mutation = random.randint(0, 255)
                krizenec.set_bunka(index, local_mutation)

            new_population.append(krizenec)                     # Pridanie krizenca do populacie

    return new_population


def menu():
    global selection
    global elitarism
    global pop_count
    global POCET_JEDINCOV

    print('Zdravim')
    print('Co potrebujes zmenit ?\n1 - Selekciu,\n2 - Elitarizmus,\n'
          '3 - Pocet generacii\n4 - Pocet jedincov\n!q pre navrat do povodneho menu')
    local_input = input()
    if local_input == '1':
        selection = input('Zadaj typ hladania (1-Ruleta, 2-Turnaj)\n')
        print(selection)
        if selection != '1' and selection != '2':
            print('Error, chybny vstup. Recompiluj program.')
            exit(0)
        print('Zmenena hodnota ' + selection)
        menu()
    elif local_input == '2':
        elitarism = input('Zadaj, ci sa bude vykonavat elitarizmus (0-Nie, 1-Ano)\n')
        if elitarism != '0' and elitarism != '1':
            print('Error, chybny vstup. Recompiluj program.')
            exit(0)
        print('Zmenena hodnota ' + elitarism)
        menu()
    elif local_input == '3':
        pop_count = int(input('Zadaj maximalny pocet generacii, realne cislo { 1,2,3,4... }\n'))
        if pop_count <= 0:
            print('Error, chybny vstup. Recompiluj program.')
            exit(0)
        print('Zmenena hodnota ' + str(pop_count))
        menu()
    elif local_input == '4':
        POCET_JEDINCOV = int(input('Zadaj pocet jedincov, realne cislo { 20,21,22,23... }\n'))
        if POCET_JEDINCOV <= 19:
            print('Error, chybny vstup. Recompiluj program.')
            exit(0)
        print('Zmenena hodnota ' + str(POCET_JEDINCOV))
        menu()
    elif local_input == '!q':
        main_function()
    else:
        print('Error, chybny vstup. Recompiluj program.')
        exit(0)
    return 0


def main_function():
    global CURRENT_BEST_FITNESS
    global CURRENT_BEST_JEDINEC
    global selection
    global elitarism
    global pop_count

    my_population = []

    print('--------------------------------')
    print('Vysvetlivky')
    print('Selekcia\n1 - Ruleta\t2 - Turnaj')
    print('Elitarizmus\n1 - ON\t0 - OFF')
    print('--------------------------------')

    input_start = input('Aktualne nastavenia\nSelekcia\t\t\t\t\t' + selection +
                        '\nElitarizmus\t\t\t\t\t' + elitarism + '\n'
                        'Maximalny pocet generacii\t' + str(pop_count) +
                        '\nPocet jedincov\t\t\t\t'+str(POCET_JEDINCOV)+'\nV pripade ze chces ponechat '
                        'a pokracovat vloz !s inak !q pre vypnutie alebo !e pre editaciu\n')

    if input_start == '!q':
        print('Vypinam program.')
        return 0

    if input_start == '!e':
        menu()

    if input_start == '!s':
        for i in range(POCET_JEDINCOV):
            jedinec_a = Jedinec()
            my_population.append(jedinec_a)

        notfound = True

        for pocetGen in range(pop_count):
            if pocetGen == 0:
                for i in range(POCET_JEDINCOV):
                    if search_solution(my_population[i], False) == 2:
                        print('Pocet generacii:')
                        print(pocetGen + 1)
                        print('Cesta')
                        search_solution(my_population[i], True)
                        notfound = False
                        break
            else:
                if notfound is True:
                    my_population = krizenie(my_population, int(selection), elitarism)
                    for i in range(POCET_JEDINCOV):
                        if search_solution(my_population[i], False) == 2:
                            print('Pocet generacii:')
                            print(pocetGen + 1)
                            print('Cesta')
                            search_solution(my_population[i], True)
                            notfound = False
                            break

        if notfound is True:
            print('Nenajdene riesenie so vsetkymi. Ukoncujem hladanie.')
            print('Najlepsi najdedny fitness:')
            print(CURRENT_BEST_FITNESS)
            print('Najlepsi najdedny jedinec:')
            print(str(CURRENT_BEST_JEDINEC)+'\n')
            temp_jedinec = Jedinec()
            temp_jedinec.set_data(CURRENT_BEST_JEDINEC)
            search_solution(temp_jedinec, True)

        input_continue = input('Mam pokracovat ? Y - Ano, N - Nie\n')
        if input_continue == 'Y':
            CURRENT_BEST_FITNESS = 0
            CURRENT_BEST_JEDINEC = []
            main_function()
        elif input_continue == 'N':
            return 0


main_function()
