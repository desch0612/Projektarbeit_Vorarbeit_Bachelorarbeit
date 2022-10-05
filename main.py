# Klasse der Farben
class Farbe:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def __repr__(self):
        return self.name

print("Bitte geben Sie die kleinste Gebindegröße an: ")
kleines_Gebinde = int(input())

print("Bitte geben Sie die nächst größere Gebindegröße an: ")
grosses_Gebinde = int(input())

# Klasse der Gebinde
class Gebinde:
    def __init__( self, color, kleines_Gebinde = kleines_Gebinde, grosses_Gebinde= grosses_Gebinde):
        self.kleines_Gebinde = int(kleines_Gebinde)
        self.grosses_Gebinde = int(grosses_Gebinde)
        self.color = color

    def isFarbe( self, f ):
        return True if f.getName() == self.color.getName() else False

# Objekte der Klasse Farbe
R = Farbe('R')
B = Farbe('B')
G = Farbe('G')

# Objekte der Klasse Gebinde
R3 = Gebinde( R )
G3 = Gebinde( G )
B3 = Gebinde( B )

# Zuordnung der Objekte Farbe zu den Objekten der Klasse Gebinde
Farbe_zu_Gebinde = {
    R : R3,
    B : B3,
    G : G3
}

# Klasse der Kisten
class Kisten:
    def __init__(self, content, name):
        self.content = content
        self.name = name

    def getContent(self):
        return self. content

    def printContent(self):
        print( '[')
        for c in self.content:
            print( c.getName() )
        print( ']')

    def __repr__(self):
        return self.name

# Erstellung der Kundenaufträge
K1 = Kisten([R,G], 'K1')
K2 = Kisten([B], 'K2')

kisten = [K1, K2]

# job ist List von Kisten
# jede Kiste enthält eine vorgegebene Reihenfolge von Arbeitsgängen (farbe, Station)
# die Simulation verwendet für die Arbeitsgänge so lange wie möglich
# ein bereits aufgestecktes Gebinde
def compute_Simulation( task ):
    Verlust = 0                                                                          # Der Verlust an Kugeln
    Wechsel_Gebinde = 0                                                                  # Wechsel der Gebinde
    mp1_rest_klein,mp1_rest_gross,mp2_rest_klein,mp2_rest_gross = 0,0,0,0                # Restwerte auf den Gebinden
    mp1_farbe_klein,mp1_farbe_gross,mp2_farbe_klein,mp2_farbe_gross = R,R,R,R            # Farben der Gebinde (Startwert)

    for a in task:
        farbe = a[1]
        station = a[2]
        size = a[3]
        if station == 0:
            if size == kleines_Gebinde:
                if mp1_rest_klein > 0 and mp1_farbe_klein == farbe:
                    mp1_rest_klein -= 1
                    continue
                else:
                    Wechsel_Gebinde += 1
                    Verlust += mp1_rest_klein
                    mp1_farbe_klein = farbe
                    mp1_rest_klein = Farbe_zu_Gebinde[farbe].kleines_Gebinde - 1
                    if mp1_rest_gross > 0:
                        Verlust += mp1_rest_gross
            elif size == grosses_Gebinde:
                if mp1_rest_gross > 0 and mp1_farbe_gross == farbe:
                    mp1_rest_gross -= 1
                    continue
                else:
                    Wechsel_Gebinde += 1
                    Verlust += mp1_rest_gross
                    mp1_farbe_gross = farbe
                    mp1_rest_gross = Farbe_zu_Gebinde[farbe].grosses_Gebinde -1
                    if mp1_rest_klein > 0:
                        Verlust += mp1_rest_klein

        else:

            if size == kleines_Gebinde:
                if mp2_rest_klein > 0 and mp2_farbe_klein == farbe:
                    mp2_rest_klein -= 1
                    continue
                else:
                    Wechsel_Gebinde += 1
                    Verlust += mp2_rest_klein
                    mp2_farbe_klein = farbe
                    mp2_rest_klein = Farbe_zu_Gebinde[farbe].kleines_Gebinde -1
                    if mp2_rest_gross  > 0:
                        Verlust += mp2_rest_gross
            if size == grosses_Gebinde:
                if mp2_rest_gross > 0 and mp2_farbe_gross == farbe:
                    mp2_rest_gross -= 1
                    continue
                else:
                    Wechsel_Gebinde += 1
                    Verlust += mp2_rest_gross
                    mp2_farbe_gross = farbe
                    mp2_rest_gross = Farbe_zu_Gebinde[farbe].grosses_Gebinde - 1
                    if mp2_rest_klein > 0:
                        Verlust += mp2_rest_klein

    return (Wechsel_Gebinde, Verlust)

mVerlust = 100000
mWechsel = 100000
Anzahl_Ablaufplaene = 0

# Diese Fkt. hat zwei Aufgaben
# 1. Sie bekommt die Bewertungsmaße übergeben und entscheidet auf dieser Grundlage ob der Ablaufplan ausgegeben wird.
# 2. Sie erstellt die Permutationen innerhalb der Kisten ((R,B,G), (B,R,G))
def generateTaskSchedule( jobSchedule, curJobIndex, curJobTasks, taskSchedule, evalFkt):
    global mVerlust
    global mWechsel
    global Anzahl_Ablaufplaene

    if curJobIndex == len( jobSchedule ) and len( curJobTasks ) == 0:
        rest = compute_Simulation(taskSchedule)
        if rest[1] <= mVerlust:
            mVerlust = rest[1]
            #print("Für den folgenden Ablaufplan: ")
            #print(taskSchedule)
            #print('ist ein minimaler Verlust von:' + str(rest[1]))
        if rest[0] < mWechsel:
            mWechsel = rest[0]
            #print( 'und ein minimaler Wechsel von: ' + str(mWechsel) + " entstanden")
        return

    if len( curJobTasks ) == 0 :
        curJobTasks = jobSchedule[curJobIndex].content
        curJobIndex+=1

    container_sizes= [kleines_Gebinde, grosses_Gebinde]
    for size in container_sizes:
        for j in curJobTasks:
            task = (jobSchedule[curJobIndex - 1], j, 1, size)
            taskSchedule+=[task]
            Anzahl_Ablaufplaene += 1
            #print(Anzahl_Ablaufplaene)
            print(taskSchedule)
            remainingTask = curJobTasks[:]
            remainingTask.remove(j)
            generateTaskSchedule(jobSchedule, curJobIndex, remainingTask, taskSchedule, evalFkt)
            taskSchedule.remove(task)

        for j in curJobTasks:
            task = (jobSchedule[curJobIndex - 1], j, 0, size)
            taskSchedule+=[task]
            Anzahl_Ablaufplaene += 1
            #print(Anzahl_Ablaufplaene)
            print(taskSchedule)
            remainingTask = curJobTasks[:]
            remainingTask.remove(j)
            generateTaskSchedule(jobSchedule, curJobIndex, remainingTask, taskSchedule, evalFkt)
            taskSchedule.remove(task)



# Die Fkt. erstellt die Permutationen der Kisten ((K1, K2, K3), (K2,K1,K3)) und übergibt
# diese an die Fkt. generateTaskSchedule
def generateJobSchedule( kisten, evalFkt, schedule ):
    if len(kisten) == 0:
        generateTaskSchedule(schedule, 0, [], [], evalFkt)
    for k in kisten:
        schedule+=[k]
        remainingKisten = kisten[:]
        remainingKisten.remove(k)
        generateJobSchedule(remainingKisten, evalFkt, schedule)
        schedule.remove(k)

# Aufruf des Programms
generateJobSchedule(kisten, compute_Simulation, [])
