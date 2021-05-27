import matplotlib.pyplot as plt
PérimètreRoue = 1.765  #en m
Pont = 9/30
rapport1 = 0.38
vitessesReelles1 = [0, 22,30, 34,38,39,42,45,46,47,48,49,51,51,53,54,54,56,57,59,60,62,65,76,81,89,94,96,100,
                    104,107,111,114,116,119,121,123,125,128,130,133,136,139,139,141,144,146,148,151,153,
                    155,158,160,153,164,167,169,172,173,175,177,179,182,183,184,185,188,189,190,190,191,
                    192,192,192,193,194,195,196,196,196,197, 197]

gear = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,
        4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6]

def CreationBoite():
    vitesseGear1 = []
    vitesseGear2 = []
    vitesseGear3 = []
    vitesseGear4 = []
    vitesseGear5 = []
    vitesseGear6 = []
    for i in range(len(gear)):
        if gear[i] == 1:
            vitesseGear1.append(vitessesReelles1[i])
        if gear[i] == 2:
            vitesseGear2.append(vitessesReelles1[i])
        if gear[i] == 3:
            vitesseGear3.append(vitessesReelles1[i])
        if gear[i] == 4:
            vitesseGear4.append(vitessesReelles1[i])
        if gear[i] == 5:
            vitesseGear5.append(vitessesReelles1[i])
        if gear[i] == 6:
            vitesseGear6.append(vitessesReelles1[i])
    #Choix du rapport 2:

    rapport2 = choixRapport2(vitesseGear2)
    print("rapport 1:")
    print(rapport1)
    print("rapport 2 :")
    print(rapport2)
    rapport3 = choixRapport3(vitesseGear3,rapport2)
    print("rapport 3 :")
    print(rapport3)
    rapport4 = choixRapport4(vitesseGear4, rapport3)
    print("rapport 4  :")
    print(rapport4)
    rapport6 = ChoixPignonHaut(max(vitessesReelles1), 7450)
    print("rapport 6 :")
    print(rapport6)
    rapport5 = choixRapport5(vitesseGear5)
    print("rapport 5 :")
    print(rapport5)

def ChoixPignonHaut(Vmax, RPMPassageHaut):  #Choix du pignon en fonction d'une vitesse maximale atteinte pour un régime maximal
    r = Vmax * 1000 / (60 * PérimètreRoue * Pont * RPMPassageHaut)
    return r

def ChoixPignonBas(Vmin, RPMPassageBas): #Choix du pignon en fonction d'une vitesse minimale atteinte avec une valleur de RPM permettant une bonne reprise.
    r = Vmin * 1000 / (60 * PérimètreRoue * Pont * RPMPassageBas)
    return r

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

def choixRapport2(vitesseGear2):
    vMin = min(vitesseGear2)
    if(5550 < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport1)) < 6500):  #On test si la vitesse 1 est adapté pour cette vitesse
        vitesseGear2.remove(vMin)
        choixRapport2(vitesseGear2)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,5550)
    return r
def choixRapport3(vitesseGear3, rapport2):
    vMin = min(vitesseGear3)
    if(5550 < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport2)) < 6500):  #On test si la vitesse 1 est adapté pour cette vitesse
        vitesseGear3.remove(vMin)
        choixRapport3(vitesseGear3)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,5550)
    return r
def choixRapport4(vitesseGear4, rapport3):
    vMin = min(vitesseGear4)
    if(5550 < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport3)) < 6500):  # 6500 à affiner, revoir: valeur qui decend a 5550 apres chgt. On test si la vitesse 1 est adapté pour cette vitesse
        vitesseGear4.remove(vMin)
        choixRapport4(vitesseGear4)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,5550)
    return r

def choixRapport5(vitesseGear5):
    vMax = max(vitesseGear5)
    r = ChoixPignonHaut(vMax, 7450)
    return r
#RapportsBV1 = [0.38, 0.51, 0.67, 0.727, 0.78, 0.87]
#RPMPassageHautBV1 = [7450, 7450, 7450, 7450, 7450, 7450]
#traceGrapheVitesseRPM(RapportsBV1, RPMPassageHautBV1)

CreationBoite()