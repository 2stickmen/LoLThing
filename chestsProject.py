import random
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np 
import os
import pandas
from PIL import Image
#%%
mySkinsCSV = pandas.read_csv('https://raw.githubusercontent.com/2stickmen/LoLThing/master/MySkins.csv')

mySkins = [i for i in mySkinsCSV.columns]
 #%%
cwd = os.getcwd()
 
def mean(aList):
    return sum(aList)/len(aList)

def getAllSkins():
    response = requests.get('http://ddragon.leagueoflegends.com/cdn/9.24.2/data/en_US/champion.json').json()
    skins = []
    for champion in response['data']:
        url = 'http://ddragon.leagueoflegends.com/cdn/9.24.2/data/en_US/champion/{}.json'.format(champion)
        champData = requests.get(url)
        champJson = champData.json()
        champSkins = champJson['data'][champion]['skins']
        for i in range(1,len(champSkins)):
            skinName = champSkins[i]['name']
            skins.append(skinName)
    return skins
 #%%
def seperate(skins):
	skinsOut = skins.copy()
	prestige = []
	victorious = []
	unobtainable = ['Annie-Versary','Unchained Alistar', 'UFO Corki','Rusty Blitzcrank','PAX Jax','Judgment Kayle','King Rammus','Championship Riven','Riot Squad Singed','PAX Sivir','Riot Girl Tristana','PAX Twisted Fate','Urf the Manatee']
	mythic = ['Hextech Alistar','Hextech Annie','Hextech Amumu','Hextech Jarvan IV','Hextech Kog\'Maw','Hextech Malzahar','Hextech Poppy','Hextech Rammus','Hextech Renekton','Dark Star Cho\'Gath','Dreadnova Darius','Lancer Zero Hecarim','Neo PAX Sivir','Soulstealer Vayne']
	ultimate = ['Pulsefire Ezreal', 'Spirit Guard Udyr','Gun Goddess Miss Fortune','DJ Sona','Elementalist Lux']
	for i in skins:
		if 'Prestige Edition' in i:
			prestige.append(i)
			skinsOut.remove(i)
		if 'Victorious' in i:
			victorious.append(i)
			skinsOut.remove(i)
	unobtainable = list(set(unobtainable).intersection(set(skins)))
	mythic = list(set(mythic).intersection(set(skins)))
	for i in mythic + unobtainable:
		skinsOut.remove(i)
	return skinsOut, prestige, mythic, unobtainable, ultimate, victorious
#%%
AllSkins = getAllSkins()
skinTuple = seperate(AllSkins)
skins = skinTuple[0]
prest = skinTuple[1]
myth = skinTuple[2]
unob = skinTuple[3]
ult = skinTuple[4]
vict = skinTuple[5]
ultraRare = prest + myth

#%%
myskinTuple = seperate(mySkins)
myRegSkins = myskinTuple[0]
myPrest = myskinTuple[1]
myMyth = myskinTuple[2]
myUnob = myskinTuple[3]
myUlt = myskinTuple[4]
myVict = myskinTuple[5]
 #%%
def openMasterChests(n,bl):
    chestCount = n
    rolledChest = 0
    test = 0
    loot = []
    chestLoot = ['Skin Shard','Essence','Emote','Ward']
    blProt = bl
    for i in range(chestCount):
        test +=1
        getLoot = random.choices(chestLoot,[0.7,0.1,0.1,0.1])
        chestBonus = random.randint(1,100)
        gemBonus = random.randint(1,1000)
        loot.extend(getLoot)
        if chestBonus <= 10:
            rolledChest +=1
            chestCount +=1
        if gemBonus <= 36 or blProt == 50:
            loot.append('Gemstone')
            blProt =    0
        else:
            blProt+=1
    return [loot, rolledChest, blProt]
 
def openWithBonus(n):
    totalOpened = n
    loots = openMasterChests(n, 0)
    extraChests = loots[1]
    while extraChests != 0:
        totalOpened += extraChests
        lootExtra = openMasterChests(extraChests, loots[2])
        loots.extend(lootExtra[0])
        extraChests = lootExtra[1]
    gems = loots[0].count('Gemstone')
    totShards = loots[0].count('Skin Shard')
    totBonusChest = (totalOpened-n)
    return totShards, gems, totBonusChest
 
 
def rollShard(shards):
    get = []
    for i in range(shards):
        lootTab = random.choices([skins, ultraRare],[1999/2000,1/2000])
        loot = lootTab[0][random.randint(0,len(lootTab[0])-1)]
        get.append(loot)
    perms = []
    for i in get:
        if i in ult or i in ultraRare:
            perms.append(i)
            get.remove(i)
    return get, perms
       
def rollSkins(shards,inv):
    skinsToRoll = len(shards)//3
    gainedSkins = []
    for i in range(skinsToRoll):
        loot = inv[0]
        regSkinChoice = list(set(skins).difference(set(inv)))
        ultraRareSkinChoice = list(set(ultraRare).difference(set(inv)))
        while loot in inv:
            lootTab = random.choices([regSkinChoice, ultraRareSkinChoice],[1999/2000,1/2000],k=2)
            if len(lootTab[0]) == 0 and len(lootTab[1]) == 0:
                loot = 'You have everything!'
            elif len(lootTab[0]) == 0:
                loot = lootTab[1][random.randint(0,len(lootTab[1])-1)]
            else:
                loot = lootTab[0][random.randint(0,len(lootTab[0])-1)]
            
        inv.append(loot)
        gainedSkins.append(loot)
    return inv, gainedSkins
 
def displaySkin(skins):
    for i in skins:
        j = i.replace(':','').replace('/','')
        imgName = j+'.jpg'
        img = Image.open(imgName)
        img.show()
        
def allTheThings(n,inv):
    bonus = openWithBonus(n)
    shards = rollShard(bonus[0])
    inv += shards[1]
    skinsOut = rollSkins(shards[0],inv)
    displaySkin(skinsOut[9])
    return skinsOut
#%%
 
#out = 'From {} chests you obtained {} skins, with {} left over. You also got {} gemstones.'.format(totalOpened,skinsTotal,leftoverShards,)
#   print(out)
 
#totSkins.sort()
#totGems.sort()
#totBonusChest.sort()
#plt.figure('Skins')
#plt.bar(range(1,run+1),totSkins)
#plt.plot(range(1,run+1), [mean(totSkins) for i in range(run)])
#plt.figure('Gems')
#plt.bar(range(1,run+1),totGems)
#plt.plot(range(1,run+1), [mean(totGems) for i in range(run)])
#plt.figure('Bonus Chests')
#plt.bar(range(1,run+1),totBonusChest)
#plt.plot(range(1,run+1), [mean(totBonusChest) for i in range(run)])
 
#n = 0
#inv = []
#skinsChest = allTheThings(n,inv)
#count = 1
#while set(skinsChest).intersection(set(ultraRare)) == set():
    #count+=1
    #inv += list(set(skinsChest) - (set(skinsChest)&set(inv)))
    #skinsChest = allTheThings(n,inv)
#print(set(inv).intersection(set(ultraRare)), count)
#%%
def percent(lista,listb):
	matches = len(set(lista).intersection(set(listb)))
	return matches*100/len(listb) 

out = 'You own {}% of the regular skins, {}% of Mythic skins, {}% of the Prestige skins, {}% of unobtainable skins, {}% of the ultimate skins, and {}% of the Victorious skins. That means you own {}% of all skins in the game!'.format(percent(myRegSkins,skins),percent(myMyth,myth),percent(myPrest,prest),percent(myUnob,unob),percent(myUlt,ult),percent(myVict,vict),percent(mySkins,AllSkins))

print(out)
testSkin = mySkins.copy()
#%%