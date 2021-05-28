import matplotlib.pyplot as plt

#DONNEES VOITURE
PérimètreRoue = 1.765  #en m
Pont = 9/30
rapport1 = 0.38
RPMOptimalReprise = 5550
RPMMaxPourCoupleOptimal = 6700    #Le couple est maximal lorsqu'il est compris entre RPMOptimalReprise et RPMMaxPourCoupleOptimal
RPMChangementDeVitesse = 7450

##DONNEES CIRCUIT:
vitessesReelles1 = [0, 22,30, 34,38,39,42,45,46,47,48,49,51,51,53,54,54,56,57,59,60,62,65,76,81,89,94,96,100,
                    104,107,111,114,116,119,121,123,125,128,130,133,136,139,139,141,144,146,148,151,153,
                    155,158,160,153,164,167,169,172,173,175,177,179,182,183,184,185,188,189,190,190,191,
                    192,192,192,193,194,195,196,196,196,197, 197]   #vitesse point par point
gear = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,
        4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6]  #Gear correspondante point par point

#FONCTION PRINCIPALE:
def CreationBoite(vitesse, gear):
    vitesseGear1 = []
    vitesseGear2 = []
    vitesseGear3 = []
    vitesseGear4 = []
    vitesseGear5 = []
    vitesseGear6 = []
    for i in range(len(gear)):   ##Tri des vitesses en fonction de la gear dans laquelle elles sont atteintes
        if gear[i] == 1:
            vitesseGear1.append(vitesse[i])
        if gear[i] == 2:
            vitesseGear2.append(vitesse[i])
        if gear[i] == 3:
            vitesseGear3.append(vitesse[i])
        if gear[i] == 4:
            vitesseGear4.append(vitesse[i])
        if gear[i] == 5:
            vitesseGear5.append(vitesse[i])
        if gear[i] == 6:
            vitesseGear6.append(vitesse[i])

    ##CHOIX DES RAPPORTS:
    print("rapport 1:")
    print(rapport1)
    rapport2 = choixRapport2Bas(vitesseGear2)
    print("rapport 2 :")
    print(rapport2)
    rapport3 = choixRapport3Bas(vitesseGear3,rapport2)
    print("rapport 3 :")
    print(rapport3)
    rapport4 = choixRapport4Bas(vitesseGear4, rapport3)  ##CHOIX "par le bas" jusqu'a la gear 4: on s'arrange pour obtenir une retombée de rpm a 5550 tr/min au changement de vitesse, ce qui correpond au max du couple dispo et donc à la meilleure reprise.
    print("rapport 4  :")
    print(rapport4)
    rapport6 = ChoixPignonHaut(max(vitessesReelles1), RPMChangementDeVitesse)  ##Choix des autres rapport "par le haut": On prend le rapport max et n s'assure qu'il permette d'atteindre la Vmax avec un taux de rpm satisfaisant, soit autour de 1400 tr/min
    print("rapport 6 :")
    print(rapport6)
    rapport5 = choixRapport5Haut(vitesseGear5)
    print("rapport 5 :")
    print(rapport5)
    #Tracé du graphe RPM = f(Vitesse)
    rapports = [rapport1,rapport2, rapport3, rapport4, rapport5, rapport6]
    traceGrapheVitesseRPM(rapports, [RPMChangementDeVitesse] * 6)

#FONCTIONS ANNEXES:
def ChoixPignonHaut(Vmax, RPMPassageHaut):  #Choix du pignon en fonction d'une vitesse que l'on veut atteinte pour un régime maximal et ainsi exploiter pleinement la gear sans sous ou sur dimensionner
    r = Vmax * 1000 / (60 * PérimètreRoue * Pont * RPMPassageHaut) # rapportGear = Vmax * 1000 / (60 * PérimètreDeLaRoue * Pont * RPMmaxSouhaitéAvecCetteGear)
    return r
def ChoixPignonBas(Vmin, RPMPassageBas): #Choix du pignon en fonction d'une vitesse minimale atteinte avec une valleur de RPM permettant une bonne reprise.
    r = Vmin * 1000 / (60 * PérimètreRoue * Pont * RPMPassageBas) #Même formule que ChoixPignonHaut mais le choix est fait en fonction du plus bas RPM souhaité
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

def choixRapport2Bas(vitesseGear2):
    vMin = min(vitesseGear2)
    if(RPMOptimalReprise < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport1)) < RPMMaxPourCoupleOptimal):  #On test si la vitesse 1 est adapté pour cette vitesse ie si le nombre de RPM avec la gear 1 ofrre un couple satisfisant. au dessus du pic mais en dessous du rupteur.
        vitesseGear2.remove(vMin)
        choixRapport2Bas(vitesseGear2, rapport1)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,RPMOptimalReprise)
    return r
def choixRapport3Bas(vitesseGear3, rapport2):
    vMin = min(vitesseGear3)
    if(RPMOptimalReprise < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport2)) < RPMMaxPourCoupleOptimal):  #On test si la vitesse 2 est adapté pour cette vitesse
        vitesseGear3.remove(vMin)
        choixRapport3Bas(vitesseGear3, rapport2)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,RPMOptimalReprise)
    return r
def choixRapport4Bas(vitesseGear4, rapport3):
    vMin = min(vitesseGear4)
    if(RPMOptimalReprise < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport3)) < RPMMaxPourCoupleOptimal):  # 6500 à affiner, revoir: valeur qui decend a 5550 apres chgt. On test si la vitesse 1 est adapté pour cette vitesse
        vitesseGear4.remove(vMin)
        choixRapport4Bas(vitesseGear4, rapport3)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,RPMOptimalReprise)
    return r
def choixRapport5Bas(vitesseGear5, rapport4):
    vMin = min(vitesseGear5)
    if(RPMOptimalReprise < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport4)) < RPMMaxPourCoupleOptimal):  # 6500 à affiner, revoir: valeur qui decend a 5550 apres chgt. On test si la vitesse 1 est adapté pour cette vitesse
        vitesseGear5.remove(vMin)
        choixRapport5Bas(vitesseGear5,rapport4)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,RPMOptimalReprise)
    return r
def choixRapport6Bas(vitesseGear6, rapport5):
    vMin = min(vitesseGear6)
    if(RPMOptimalReprise < (vMin * 1000 / (60 * PérimètreRoue * Pont * rapport5)) < RPMMaxPourCoupleOptimal):  # 6500 à affiner, revoir: valeur qui decend a 5550 apres chgt. On test si la vitesse 1 est adapté pour cette vitesse
        vitesseGear6.remove(vMin)
        choixRapport6Bas(vitesseGear6, rapport5)
    else: #La 1 n'est pas adpaté pour cette vitesse, on dimensionne la 2 sur le min pour avoir la meilleure reprise en couple.
        r = ChoixPignonBas(vMin,RPMOptimalReprise)
    return r

def choixRapport2Haut(vitesseGear2):
    vMax = max(vitesseGear2)
    r = ChoixPignonHaut(vMax, RPMChangementDeVitesse)
    return r
def choixRapport3Haut(vitesseGear3):
    vMax = max(vitesseGear3)
    r = ChoixPignonHaut(vMax, RPMChangementDeVitesse)
    return r
def choixRapport4Haut(vitesseGear4):
    vMax = max(vitesseGear4)
    r = ChoixPignonHaut(vMax, RPMChangementDeVitesse)
    return r
def choixRapport5Haut(vitesseGear5):
    vMax = max(vitesseGear5)
    r = ChoixPignonHaut(vMax, RPMChangementDeVitesse)
    return r
def choixRapport6Haut(vitesseGear6):
    vMax = max(vitesseGear6)
    r = ChoixPignonHaut(vMax, RPMChangementDeVitesse)
    return r

CreationBoite(vitessesReelles1, gear)

##Test boites 7/6/5
GearMaxDeReprise = 3
def CreationBoites7_6_5(vitesse, gear, GearMaxDeReprise):
    vitesseGear1 = []
    vitesseGear2 = []
    vitesseGear3 = []
    vitesseGear4 = []
    vitesseGear5 = []
    vitesseGear6 = []
    vitesseGear7 = []
    rapports = [rapport1]
    for i in range(len(gear)):   ##Tri des vitesses en fonction de la gear dans laquelle elles sont atteintes
        if gear[i] == 1:
            vitesseGear1.append(vitesse[i])
        if gear[i] == 2:
            vitesseGear2.append(vitesse[i])
        if gear[i] == 3:
            vitesseGear3.append(vitesse[i])
        if gear[i] == 4:
            vitesseGear4.append(vitesse[i])
        if gear[i] == 5:
            vitesseGear5.append(vitesse[i])
        if gear[i] == 6:
            vitesseGear6.append(vitesse[i])
        if gear[i] == 7:
            vitesseGear7.append(vitesse[i])

    ##CHOIX DES RAPPORTS DIMENSIONNES 'PAR LE BAS'
    while(len(rapports) < GearMaxDeReprise ):
        if (len(rapports) == 1):
            rapports.append(choixRapport2Bas(vitesseGear2))
        if (len(rapports) == 2):
            rapports.append(choixRapport3Bas(vitesseGear3, rapports[1]))
        if (len(rapports) == 3):
            rapports.append(choixRapport4Bas(vitesseGear4, rapports[2]))
        if (len(rapports) == 4):
            rapports.append(choixRapport5Bas(vitesseGear5, rapports[3]))
        if (len(rapports) == 5):
            rapports.append(choixRapport6Bas(vitesseGear6, rapports[4]))

    #DIMENSIONNEMENT DES RAPPORTS HAUTS: 3 CAS : BOITE 7, 6 ou 5:
    nBoite = 7
    i = 0
    rapports.append(ChoixPignonHaut(max(vitesse), RPMChangementDeVitesse))
    i += 1
    if(nBoite - i == GearMaxDeReprise):
        return rapports
    rapports.insert(GearMaxDeReprise, choixRapport6Haut(vitesseGear6))
    i += 1
    if (nBoite - i == GearMaxDeReprise):
        return rapports
    rapports.insert(GearMaxDeReprise, choixRapport5Haut(vitesseGear5))
    i += 1
    if (nBoite - i == GearMaxDeReprise):
        return rapports
    rapports.insert(GearMaxDeReprise, choixRapport4Haut(vitesseGear4))
    i += 1
    if (nBoite - i == GearMaxDeReprise):
        return rapports
    rapports.insert(GearMaxDeReprise, choixRapport3Haut(vitesseGear3))
    i += 1
    if (nBoite - i == GearMaxDeReprise):
        return rapports
    rapports.insert(GearMaxDeReprise, choixRapport2Haut(vitesseGear2))
    return rapports

print(CreationBoites7_6_5(vitessesReelles1,gear,1))