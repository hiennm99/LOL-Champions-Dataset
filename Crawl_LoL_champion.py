import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import numpy as np
import requests
import time
import regex as re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import concurrent.futures
from sqlalchemy import create_engine
import configparser

def connect_MySQL():
    #MySQL connection information
    config=configparser.ConfigParser()
    config.read('config.ini')
    
    mysql_engine=create_engine(f"{config['MySQL']['driver']}://{config['MySQL']['username']}:{config['MySQL']['password']}@{config['MySQL']['host']}/{config['MySQL']['database']}") 
    return mysql_engine

def connect_AWSRedshift():
    #AWSRedshift connection information
    config=configparser.ConfigParser()
    config.read('config.ini')
  
    AWSRedshift_engine=create_engine(f"{config['AWSRedshift']['driver']}://{config['AWSRedshift']['username']}:{config['AWSRedshift']['password']}@{config['AWSRedshift']['host']}:{config['AWSRedshift']['port']}/{config['AWSRedshift']['database']}")
    return AWSRedshift_engine

def convert_to_str(lst=[]):
    res=''
    for val in lst:
        res=res+str(val)+'/'
    res=res[0:-1]
    return res


def Champion_Information_API():
    
    url = "https://op.gg/api/v1.0/internal/bypass/meta/champions?hl=en_US"
    payload={ 
            
    }
    headers = {
    'authority': 'op.gg',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'if-none-match': 'W/"1a7688-4EXDwhv77MGYD9umSmmUAy9rhgU"',
    'origin': 'https://www.op.gg',
    'referer': 'https://www.op.gg/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.json().get('data')
    
    for i in range(len(data)):
        infor_=[]  
        name_=data[i]['name']
        image_=data[i]['image_url']
        
        skill_passive_=data[i]['passive']['name']
        skill_passive_des_=data[i]['passive']['description']
        skill_passive_image_=data[i]['passive']['image_url']
        skill_Q_=data[i]['spells'][0]['name']
        skill_Q_des_=data[i]['spells'][0]['description']
        cooldown_Q_=convert_to_str(data[i]['spells'][0]['cooldown_burn'])
        cost_Q_=convert_to_str(data[i]['spells'][0]['cost_burn'])
        range_Q_=convert_to_str(data[i]['spells'][0]['range_burn'])
        skill_Q_image_=data[i]['spells'][0]['image_url']
        
        skill_W_=data[i]['spells'][1]['name']
        skill_W_des_=data[i]['spells'][1]['description']
        cooldown_W_=convert_to_str(data[i]['spells'][1]['cooldown_burn'])
        cost_W_=convert_to_str(data[i]['spells'][1]['cost_burn'])
        range_W_=convert_to_str(data[i]['spells'][1]['range_burn'])
        skill_W_image_=data[i]['spells'][1]['image_url']
        
        skill_E_=data[i]['spells'][2]['name']
        skill_E_des_=data[i]['spells'][2]['description']
        cooldown_E_=convert_to_str(data[i]['spells'][2]['cooldown_burn'])
        cost_E_=convert_to_str(data[i]['spells'][2]['cost_burn'])
        range_E_=convert_to_str(data[i]['spells'][2]['range_burn'])
        skill_E_image_=data[i]['spells'][2]['image_url']
        
        skill_R_=data[i]['spells'][3]['name']
        skill_R_des_=data[i]['spells'][3]['description']
        cooldown_R_=convert_to_str(data[i]['spells'][3]['cooldown_burn'])
        cost_R_=convert_to_str(data[i]['spells'][3]['cost_burn'])
        range_R_=convert_to_str(data[i]['spells'][3]['range_burn'])
        skill_R_image_=data[i]['spells'][3]['image_url']
        
        infor_.append(name_)
        infor_.append(image_)

        infor_.append(skill_passive_)
        infor_.append(skill_passive_des_)
        infor_.append(skill_passive_image_)
        
        infor_.append(skill_Q_)
        infor_.append(skill_Q_des_)
        infor_.append(cooldown_Q_)
        infor_.append(cost_Q_)
        infor_.append(range_Q_)
        infor_.append(skill_Q_image_)
        
        infor_.append(skill_W_)
        infor_.append(skill_W_des_)
        infor_.append(cooldown_W_)
        infor_.append(cost_W_)
        infor_.append(range_W_)
        infor_.append(skill_W_image_)
        
        infor_.append(skill_E_)
        infor_.append(skill_E_des_)
        infor_.append(cooldown_E_)
        infor_.append(cost_E_)
        infor_.append(range_E_)
        infor_.append(skill_E_image_)
        
        infor_.append(skill_R_)
        infor_.append(skill_R_des_)
        infor_.append(cooldown_R_)
        infor_.append(cost_R_)
        infor_.append(range_R_)
        infor_.append(skill_R_image_)

        API_Information.append(infor_)
        fandom_format_name.append(name_)

def Open_Multi_Driver():
    for i in range(10):
        driver=webdriver.Chrome('chromedriver.exe')
        sleep(0.5)
        drivers.append(driver)
        
def Champion_Information_Crawl(driver,name):
    name_format=name.replace(" ","_").replace("'","%27") #Convert champion name to correct format
    url=f'https://leagueoflegends.fandom.com/wiki/{name}/LoL'
    infor_=[]
    driver.get(url)
    sleep(5)
    
    #Nickname
    try:  
        nickname_elem=driver.find_element(By.CSS_SELECTOR,'.pi-data-value.pi-font')
        nickname=nickname_elem.text
    except NoSuchElementException as e:
        nickname='N/A'
        
    #Heath 
    
    try:
        health_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="health"]')
        health=health_elem.find_elements(By.TAG_NAME,'span')[1].text
    except NoSuchElementException as e: 
        health='N/A'
        
    #Heath regen
    try:
        healthRegen_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="health regen"]')
        healthRegen=healthRegen_elem.find_elements(By.TAG_NAME,'span')[1].text
    except NoSuchElementException as e:
        healthRegen='N/A'
    
    #Armor  
    try:
        armor_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="armor"]')
        armor=armor_elem.find_elements(By.TAG_NAME,'span')[1].text
    except NoSuchElementException as e:
        armor='N/A'
    
    #Magic resist  
    try:
        magicResist_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="mr"]')
        magicResist=magicResist_elem.find_elements(By.TAG_NAME,'span')[1].text
    except NoSuchElementException as e:
        magicResist='N/A'
    
    #Move speed  
    try:
        moveSpeed_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="ms"]')
        moveSpeed=moveSpeed_elem.find_elements(By.TAG_NAME,'span')[0].text
    except NoSuchElementException as e:
        moveSpeed='N/A'
    
    #Mana   
    mana='N/A' 
    try:
        mana_elems=driver.find_elements(By.CSS_SELECTOR,'div[data-source="resource"]')
    except NoSuchElementException as e:
        e
    if mana_elems[1].find_elements(By.TAG_NAME,'span')==[]:
        mana='N/A'
    else:
        mana=mana_elems[1].find_elements(By.TAG_NAME,'span')[1].text    
    
    #Mana regen 
    manaRegen='N/A'   
    try:
        manaRegen_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="resource regen"]')
        manaRegen_check=manaRegen_elem.find_elements(By.TAG_NAME,'span')
    except NoSuchElementException as e:
        e 
    if len(manaRegen_check)==1:
        manaRegen=manaRegen_check[0].text
    elif len(manaRegen_check)==2:
        manaRegen=manaRegen_check[1].text
    
    #Attack damage    
    try:
        atkDamage_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="attack damage"]')
        atkDamage=atkDamage_elem.find_elements(By.TAG_NAME,"span")[1].text
    except NoSuchElementException as e:
        atkDamage='N/A'
    
    #Attack range   
    try:    
        atkRange_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="range"]')
        atkRange=atkRange_elem.find_element(By.TAG_NAME,"span").text
    except NoSuchElementException as e:
        atkRange='N/A'
    
    #Background Image    
    try:
        image_elem=driver.find_element(By.CSS_SELECTOR,'.FullWidthImage [href]')
        image_url=image_elem.get_attribute('href')
    except NoSuchElementException as e:
        e
        
    #Classes
    try:
        classes_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="role"]')
        temp_elems=classes_elem.find_elements(By.TAG_NAME,'span')
    except NoSuchElementException as e:
        e
    classes_=[elem.get_attribute("data-tip") for elem in temp_elems]
    classes=''
    for cla in classes_:
        classes+=cla+','
    classes=classes[0:-1]
    
    #Positions
    try:
        positions_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="position"]')
        temp_elems=positions_elem.find_elements(By.TAG_NAME,'span')
    except NoSuchElementException as e:
        e
    positions_=[elem.get_attribute("data-tip") for elem in temp_elems]
    positions=''
    for pos in positions_:
        positions+=pos+','
    positions=positions[0:-1]

    #Rangetype
    try:
        rangetype_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="rangetype"]')
        temp_elems=rangetype_elem.find_elements(By.TAG_NAME,'span')
    except NoSuchElementException as e:
        e
    rangetype_=[elem.get_attribute("data-tip") for elem in temp_elems]
    rangetype=''
    for type in rangetype_:
        rangetype+=type+','
    rangetype=rangetype[0:-1]

    #Difficulty
    try:
        difficulty_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="difficulty"]')
        temp_elem=difficulty_elem.find_element(By.TAG_NAME,'div')
        temp_elem2=temp_elem.find_element(By.TAG_NAME,'div')
    except NoSuchElementException as e:
        e

    difficulty_=temp_elem2.get_attribute("title")
    difficulty=int(re.findall('[0-9]+',difficulty_)[0])
        
    infor_.append(name)
    infor_.append(nickname)
    infor_.append(health)
    infor_.append(healthRegen)
    infor_.append(mana)
    infor_.append(manaRegen)
    infor_.append(atkDamage)
    infor_.append(atkRange)
    infor_.append(armor)
    infor_.append(magicResist)
    infor_.append(moveSpeed)
    infor_.append(image_url)
    infor_.append(classes)
    infor_.append(positions)
    infor_.append(rangetype)
    infor_.append(difficulty)
    Crawl_Information.append(infor_)

def Crawl_Multi_Driver():
    for i in range(0,len(fandom_format_name),10):
        group_name=fandom_format_name[i:i+10]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(Champion_Information_Crawl,drivers,group_name)

def Check_Missing_Data(df):
    missing_champions=[]
    name_list=df['Champion name'].values.tolist()
    nickname_list=df['Difficulty'].values.tolist()

    for i in range(len(name_list)):
        if np.isnan(nickname_list[i])==True:
            missing_champions.append(name_list[i])
    
    return missing_champions

def Update_Champion_Information(missing_champions):
    driver=webdriver.Chrome('chromedriver.exe')
    for name in missing_champions:
        name_format=name.replace(" ","_").replace("'","%27") #Convert champion name to correct format
        url=f'https://leagueoflegends.fandom.com/wiki/{name}/LoL'
        infor_=[]
        driver.get(url)
        sleep(5)
        
        #Nickname
        try:  
            nickname_elem=driver.find_element(By.CSS_SELECTOR,'.pi-data-value.pi-font')
            nickname=nickname_elem.text
        except NoSuchElementException as e:
            nickname='N/A'
        #Heath    
        try:
            health_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="health"]')
            health=health_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            
            
            health='N/A'
            
        #Heath regen
        try:
            healthRegen_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="health regen"]')
            healthRegen=healthRegen_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            healthRegen='N/A'
        
        #Armor  
        try:
            armor_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="armor"]')
            armor=armor_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            armor='N/A'
        
        #Magic resist  
        try:
            magicResist_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="mr"]')
            magicResist=magicResist_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            magicResist='N/A'
        
        #Move speed  
        try:
            moveSpeed_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="ms"]')
            moveSpeed=moveSpeed_elem.find_elements(By.TAG_NAME,'span')[0].text
        except NoSuchElementException as e:
            moveSpeed='N/A'
        
        #Mana 
        mana='N/A'   
        try:
            mana_elems=driver.find_elements(By.CSS_SELECTOR,'div[data-source="resource"]')
        except NoSuchElementException as e:
            e
        if mana_elems[1].find_elements(By.TAG_NAME,'span')==[]:
            mana='N/A'
        else:
            mana=mana_elems[1].find_elements(By.TAG_NAME,'span')[1].text    
        
        #Mana regen 
        manaRegen='N/A'   
        try:
            manaRegen_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="resource regen"]')
            manaRegen_check=manaRegen_elem.find_elements(By.TAG_NAME,'span')
        except NoSuchElementException as e:
            e 
        if len(manaRegen_check)==1:
            manaRegen=manaRegen_check[0].text
        elif len(manaRegen_check)==2:
            manaRegen=manaRegen_check[1].text
        
        #Attack damage    
        try:
            atkDamage_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="attack damage"]')
            atkDamage=atkDamage_elem.find_elements(By.TAG_NAME,"span")[1].text
        except NoSuchElementException as e:
            atkDamage='N/A'
        
        #Attack range   
        try:    
            atkRange_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="range"]')
            atkRange=atkRange_elem.find_element(By.TAG_NAME,"span").text
        except NoSuchElementException as e:
            atkRange='N/A'
        
        #Background Image    
        try:
            image_elem=driver.find_element(By.CSS_SELECTOR,'.FullWidthImage [href]')
            image_url=image_elem.get_attribute('href')
        except NoSuchElementException as e:
            e
            
        #Classes
        try:
            classes_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="role"]')
            temp_elems=classes_elem.find_elements(By.TAG_NAME,'span')
        except NoSuchElementException as e:
            e
        classes_=[elem.get_attribute("data-tip") for elem in temp_elems]
        classes=''
        for cla in classes_:
            classes+=cla+','
        classes=classes[0:-1]
        
        #Positions
        try:
            positions_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="position"]')
            temp_elems=positions_elem.find_elements(By.TAG_NAME,'span')
        except NoSuchElementException as e:
            e
        positions_=[elem.get_attribute("data-tip") for elem in temp_elems]
        positions=''
        for pos in positions_:
            positions+=pos+','
        positions=positions[0:-1]

        #Rangetype
        try:
            rangetype_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="rangetype"]')
            temp_elems=rangetype_elem.find_elements(By.TAG_NAME,'span')
        except NoSuchElementException as e:
            e
        rangetype_=[elem.get_attribute("data-tip") for elem in temp_elems]
        rangetype=''
        for type in rangetype_:
            rangetype+=type+','
        rangetype=rangetype[0:-1]

        #Difficulty
        try:
            difficulty_elem=driver.find_element(By.CSS_SELECTOR,'[data-source="difficulty"]')
            temp_elem=difficulty_elem.find_element(By.TAG_NAME,'div')
            temp_elem2=temp_elem.find_element(By.TAG_NAME,'div')
        except NoSuchElementException as e:
            e

        difficulty_=temp_elem2.get_attribute("title")
        difficulty=int(re.findall('[0-9]+',difficulty_)[0])
            
        infor_.append(name)
        infor_.append(nickname)
        infor_.append(health)
        infor_.append(healthRegen)
        infor_.append(mana)
        infor_.append(manaRegen)
        infor_.append(atkDamage)
        infor_.append(atkRange)
        infor_.append(armor)
        infor_.append(magicResist)
        infor_.append(moveSpeed)
        infor_.append(image_url)
        infor_.append(classes)
        infor_.append(positions)
        infor_.append(rangetype)
        infor_.append(difficulty)
        Update_Information.append(infor_)

def Clean_Champion_Information():
    df_API=pd.DataFrame(data=API_Information,
                        columns=['Champion_name','Champion_image',
                                'Skill_Passive','Skill_Passive_description','Skill_Passive_image',
                                'Skill_Q','Skill_Q_description','Cooldown_Q','Cost_Q','Range_Q','Skill_Q_image',
                                'Skill_W','Skill_W_description','Cooldown_W','Cost_W','Range_W','Skill_W_image',
                                'Skill_E','Skill_E_description','Cooldown_E','Cost_E','Range_E','Skill_E_image',
                                'Skill_R','Skill_R_description','Cooldown_R','Cost_R','Range_R','Skill_R_image'])

    df_Crawl=pd.DataFrame(data=Crawl_Information,
                          columns=  ['Champion_name','Champion_nickname',
                                     'Health','Health_regen','Resource','Resource_regen','Attack_damage','Attack_range','Armor','Magic_resist','Move_speed',
                                     'Background_image','Classes','Positions','Rangetype','Difficulty'])
    
    df_check=pd.merge(left=df_API,right=df_Crawl,how="left",on=['Champion name','Champion name'])
    
    missing_list=Check_Missing_Data(df_check)
    Update_Champion_Information(missing_list)
    
    df_Update=pd.DataFrame(data=Update_Information,
                          columns=  ['Champion_name','Champion_nickname',
                                     'Health','Health_regen','Resource','Resource_regen','Attack_damage','Attack_range','Armor','Magic_resist','Move_speed',
                                     'Background_image','Classes','Positions','Rangetype','Difficulty'])
    
    df_Sum_Crawl=df_Crawl.append(df_Update)
    
    df=pd.merge(left=df_API,right=df_Sum_Crawl,how="left",on=['Champion name','Champion name'])
    
    #Clean data
    df['Skill_Passive_description'] =[re.sub(r'<[^>]+>','', str(x)) for x in df['Skill_Passive_description']]
    df['Skill_Q_description']       =[re.sub(r'<[^>]+>','', str(x)) for x in df['Skill_Q_description']]  
    df['Skill_W_description']       =[re.sub(r'<[^>]+>','', str(x)) for x in df['Skill_W_description']]   
    df['Skill_E_description']       =[re.sub(r'<[^>]+>','', str(x)) for x in df['Skill_E_description']]   
    df['Skill_R_description']       =[re.sub(r'<[^>]+>','', str(x)) for x in df['Skill_R_description']]      
    
    return df  

def Load_Data(df):
    #DataFrame to MySQL
    df.to_excel('Champions Information.xlsx')
    print('-----Insert all champions information to excel file successfully!!!-----')
    
    #DataFrame to MySQL
    mysql_engine=connect_MySQL()
    df.to_sql('lol_champions',con=mysql_engine,if_exists='replace',index=False)
    print('-----Insert all champions information to MySQL successfully!!!-----')
    # #DataFrame to AWS Redshift
    # redshift_engine=connect_AWSRedshift()
    # df.to_sql('lol_champions',con=redshift_engine,if_exists='append',index=False)
    # print('-----Insert all champions information to AWS Redshift successfully!!!-----')
    
if __name__ == "__main__":
    start=time.time()
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-logging')
    options.add_argument('log-level=3')
    
    fandom_format_name=[]
    API_Information=[]
    Champion_Information_API()
    
    
    drivers=[]
    Update_Information=[]
    Crawl_Information=[]
    Open_Multi_Driver()
    Crawl_Multi_Driver()
    
    df=Clean_Champion_Information()
    Load_Data(df)
    
    end=time.time()-start
    print(f'Execute time: {end}')