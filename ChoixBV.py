import matplotlib.pyplot as plt

#DONNEES VOITURE
PérimètreRoue = 1.765  #en m
Pont = 9/30
rapport1 = 0.38
RPMOptimalReprise = 5550
RPMMaxPourCoupleOptimal = 6700    #Le couple est maximal lorsqu'il est compris entre RPMOptimalReprise et RPMMaxPourCoupleOptimal
RPMChangementDeVitesse = 7450
RPMMaxDerniereVitesse = 1300

##DONNEES CIRCUIT:
vitessesReelles1 = [0, 22,30, 34,38,39,42,45,46,47,48,49,51,51,53,54,54,56,57,59,60,62,65,76,81,89,94,96,100,
                    104,107,111,114,116,119,121,123,125,128,130,133,136,139,139,141,144,146,148,151,153,
                    155,158,160,153,164,167,169,172,173,175,177,179,182,183,184,185,188,189,190,190,191,
                    192,192,192,193,194,195,196,196,196,197, 197]   #vitesse point par point
gear = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,
        4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,6,6,6,6,6]  #Gear correspondante point par point

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
        plt.text(VitesseDePassage[i], 7450, '{}'.format(int(VitesseDePassage[i])))
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


##Test boites 7/6/5
GearMaxDeReprise = 3

##Pour une boite déja définie comme boite 7
def CreationBoites7(vitesse, gear, GearMaxDeReprise):
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

    if (len(rapports) == 1 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport2Bas(vitesseGear2))
    if (len(rapports) == 2 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport3Bas(vitesseGear3, rapports[1]))
    if (len(rapports) == 3 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport4Bas(vitesseGear4, rapports[2]))
    if (len(rapports) == 4 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport5Bas(vitesseGear5, rapports[3]))
    if (len(rapports) == 5 and len(rapports) < GearMaxDeReprise):
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
    return rapports #

##Pour une boite deja définie comme boite 6:
def CreationBoites6(vitesse, gear, GearMaxDeReprise):
    vitesseGear1 = []
    vitesseGear2 = []
    vitesseGear3 = []
    vitesseGear4 = []
    vitesseGear5 = []
    vitesseGear6 = []
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


    ##CHOIX DES RAPPORTS DIMENSIONNES 'PAR LE BAS'

    if (len(rapports) == 1 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport2Bas(vitesseGear2))
    if (len(rapports) == 2 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport3Bas(vitesseGear3, rapports[1]))
    if (len(rapports) == 3 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport4Bas(vitesseGear4, rapports[2]))
    if (len(rapports) == 4 and len(rapports) < GearMaxDeReprise):
        rapports.append(choixRapport5Bas(vitesseGear5, rapports[3]))

    #DIMENSIONNEMENT DES RAPPORTS HAUTS: BOITE 6:
    nBoite = 6
    i = 0
    rapports.append(ChoixPignonHaut(max(vitesse), RPMChangementDeVitesse))
    i += 1
    if (nBoite - i  == GearMaxDeReprise):
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
    if (nBoite - i  == GearMaxDeReprise):
        return rapports
    rapports.insert(GearMaxDeReprise, choixRapport2Haut(vitesseGear2))
    return rapports

def CreationBoite7Depuis6(vitesse):
    listeRapports = []
    rapports = [0.38]


    while (abs(rapports[-1] - rapports[-2]) > 0.1):

        rapports = [0.38]
        rapport7 = ChoixPignonHaut(max(vitesse), RPMMaxDerniereVitesse)
        print(rapport7)
        rapports.append(rapport7)

        vMaxPignon1 = 60 * PérimètreRoue * Pont * 7450 * rapports[0]/1000
        r1 = 1000 * (vMaxPignon1 - erreur)/ (60 * Pont * PérimètreRoue*RPMOptimalReprise)
        rapports.insert(1, r1)
        vMaxPignon2 = 60 * PérimètreRoue * Pont * 7450 * rapports[1] /1000
        rapports.insert(len(rapports) - 1, 1000 * (vMaxPignon2 - erreur) / (60 * Pont * PérimètreRoue * RPMOptimalReprise))
        vMaxPignon3 = 60 * PérimètreRoue * Pont * 7450 * rapports[2] / 1000
        rapports.insert(len(rapports) - 1, 1000 * (vMaxPignon3 - erreur) / (60 * Pont * PérimètreRoue * RPMOptimalReprise))
        vMaxPignon4 = 60 * PérimètreRoue * Pont * 7450 * rapports[3] / (1000)
        rapports.insert(len(rapports) - 1, 1000 * (vMaxPignon4 - erreur) / (60 * Pont * PérimètreRoue * RPMOptimalReprise))
        vMaxPignon5 = 60 * PérimètreRoue * Pont * 7450 * rapports[4] / (1000)
        rapports.insert(len(rapports) - 1, 1000 * (vMaxPignon5 - erreur) / (60 * Pont * PérimètreRoue * RPMOptimalReprise))
        if(rapports[-1] - rapports[-2] < 0.2):
            listeRapports.append(rapports)


    return listeRapports

#res = CreationBoites6(vitessesReelles1,gear,4)
#print(res)
#traceGrapheVitesseRPM(res, [RPMChangementDeVitesse] * 6)

print(CreationBoite7Depuis6(vitessesReelles1))