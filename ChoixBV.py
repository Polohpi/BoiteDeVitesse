import matplotlib.pyplot as plt
PérimètreRoue = 1.765  #en m
Pont = 9/30
ListeRapport = [1, 1,2, 2, 2, 3, 3, 4, 4,5 ,5 , 5, 6, 6]
ListeVitesse = []

def ChoixPignonHaut(Vmax, num_pignon, RPMPassageHaut):  #Choix du pignon en fonction d'une vitesse maximale atteinte pour un régime maximal
    r = Vmax * 1000 / (60 * PérimètreRoue * Pont * RPMPassageHaut)
    return (num_pignon, r)

def ChoixPignonBas(Vmin, num_pignon, RPMPassageBas): #Choix du pignon en fonction d'une vitesse minimale atteinte avec une valleur de RPM permettant une bonne reprise.
    r = Vmin * 1000 / (60 * PérimètreRoue * Pont * RPMPassageBas)
    return(num_pignon, RPMPassageBas)

print(ChoixPignonHaut(207,6,7300))

def traceGrapheVitesseRPM(Rapports, RPMPassageHaut): #Rapports contient les rapports choisi (liste), RPMPassageHaut est le nombre de RPM souhaité au chgt de vitesse (liste aussi).
    VitesseDePassage  = []
    for i in range(len(Rapports)):
        VitesseDePassage.append(RPMPassageHaut[i] * Rapports[i] * Pont * PérimètreRoue * 60/1000)
    print(VitesseDePassage)
    X = [0]
    Y = [0]
    for i in range (len(VitesseDePassage) - 1):
        X.append(VitesseDePassage[i])
        X.append(VitesseDePassage[i])
        RPMPassageBas = VitesseDePassage[i] * 1000 / (PérimètreRoue * 60 * Pont * Rapports[i + 1])
        Y.append(RPMPassageHaut[i])
        Y.append(RPMPassageBas)
    X.append(VitesseDePassage[-1])
    Y.append(RPMPassageHaut[-1])
    plt.plot(X,Y)
    plt.xlabel("Vitesse en km/h")
    plt.ylabel("Régime en tr/min")
    plt.legend(loc = 'best')
    plt.grid()
    plt.show()

RapportsBV1 = [0.38, 0.51, 0.67, 0.727, 0.78, 0.87]
RPMPassageHautBV1 = [7450, 7450, 7450, 7450, 7450, 7450]
traceGrapheVitesseRPM(RapportsBV1, RPMPassageHautBV1)

