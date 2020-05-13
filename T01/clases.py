import jsonReader
import random

class Jugador():
    def __init__(self,name,password,indicador_nuevo):
        #usuario elige si es un nuevo jugador o no (indicado_nuevo)
        #En el caso de que no lo sea se debe veridicar previamente si es que pass y name son correctos
           
        if indicador_nuevo==False:
            #leemos el json del jugador seleccionado
            dict_jugador=jsonReader.jsonToDict(str(name)+'.json')['id_jugador']
            self.name=dict_jugador['name']
            self.password=dict_jugador['password']
            self.medals=dict_jugador['medals']
            self.money=dict_jugador['money']
            self.team=dict_jugador['team']
            self.battles=dict_jugador['battles']
            self.qty_prograbolas=dict_jugador['qty_prograbolas']
            self.programon=[]
            ##generar metodo que genere de diccionario a programon
            for dict_mono in dict_jugador['programon']:
                self.programon.append(Programon(dict_mono['id'],dict_mono['level'],dict_mono['iv'],dict_mono['ev']))

            self.progradex=dict_jugador['progradex']
            ##generar metodo en ciudad o ruta que entregue intancia a partir de dict
            self.actual_location=dict_jugador['actual_location']
        

        else:
            #inicializamos un jugador desde cero
            self.name=name
            self.password=password
            self.medals=[]
            self.money=1000
            list_programones=jsonReader.jsonToDict('programones.json')
            #consultar que pokemon inicial quiere
            while True:
                pokemon_inicial=input('Selecciona un programon inicial:\n (0) Charmander \n (1) Squirtle \n (2) Bulbasaur :\n')
                if pokemon_inicial=='0':
                    nombre_inicial="Charmander"
                    break
                elif pokemon_inicial=='1':
                    nombre_inicial="Squirtle"
                    break
                elif pokemon_inicial=='2':
                    nombre_inicial="Bulbasaur"
                    break
                else:
                    print('Selecione un numero válido')
            #realizar clase de creación de programon para inicilizar
            dict_programon =[programon for programon in list_programones if programon['name']==nombre_inicial][0]
            #realizar clase de creación de programon para inicilizar self.programones
            self.programon=[Programon(dict_programon['id'],level=5)]
            #Definimos el team como una lista con los id de cada programon
            self.team=[dict_programon['id']]
            #se inicia la lista de progradex con el pokemon elegido
            self.progradex=[dict_programon['id']]
            #batallas lista de diccionarios de registros
            self.battles=[]
            self.qty_prograbolas=10
            # crear instancia de ciudad pueblo paleta  
            self.actual_location=0
    
    
    def jugador_json(self):
        dict_returned={'id_jugador':{}}
        dict_returned_id=dict_returned['id_jugador']
        dict_returned_id['name']=self.name
        dict_returned_id['password']=self.password    
        dict_returned_id['medals']= self.medals
        dict_returned_id['money']= self.money
        dict_returned_id['team']= self.team
        dict_returned_id['battles']=self.battles
        dict_returned_id['programon']=[ins_programon.programon_dict() for ins_programon in self.programon] 
        #instancia de programon a un diccionario, tambien generar un metodo
        #que lo cargue de dict a instancia
        dict_returned_id['qty_prograbolas']=self.qty_prograbolas
        dict_returned_id['progradex']=self.progradex
        #generar metodo que cambie de ciudad o ruta a dict correspondiente
        dict_returned_id['actual_location']=self.actual_location
        jsonReader.dictToJson(self.name + '.json',dict_returned)
        return None

    def ver_progradex(self):
        #funcion progradex del menu inicial
        #programones con capturados y vistos
        pass

    def datos_jugador(self):
        #funcion datos del jugador menu inicial
        pass

    def consultas(self):
        #funciones concultas de menu inicial
        pass
    
    
    
    def avanzar(self):
            self.actual_location+=1

    def retroceder(self):
            self.actual_location-=1

    #definir cambio de lugar en el caso de hierba o city
    def change_position(self):
        pass
        '''if mapa[self.actual_location].__class__.__name__ == 'Route':
            prob=random.randint(0,100)
            if prob<=30:
                ##pelear con prob 0.3
                self.pelea_salvaje()
        elif  mapa[self.actual_location].__class__.__name__ == 'City' and mapa[self.actual_location]==0:
            ##Lo que se puede realizar en ciudad pueblo paleta def ciudad solo pueblo paleta
            #self.action_pallet_town
        elif mapa[self.actual_location].__class__.__name__ == 'City' and mapa[self.actual_location]!=0:
            #self.action_city()'''
    def programon_factible_route(self):
        #límites de la ruta
        low_limit=mapa[self.actual_location].levels[0]
        up_limit=mapa[self.actual_location].levels[1]

        list_programones=jsonReader.jsonToDict('programones.json')
        #programones con evolucion
        programones_ce=[i for i in list_programones if 'evolveTo' in i.keys()]
        #programones sin evolucion
        programones_se=[i for i in list_programones if not('evolveTo' in i.keys())]
        list_programones_factibles=[]
        #retorna el pokemon anterior a el si es que tiene
        def evolucion_de(programon,list_programones):
            viene_de=None
            for i in list_programones:
                if programon['id']==i['evolveTo']:
                    viene_de=i
            return viene_de

        #los que tienen evolucion
        for programono in programones_ce:
            #si no es evolucion de nadie y su nivel de evolucion es mayor a low
            if evolucion_de(programono,programones_ce)==None and programono['evolveLevel']>low_limit:
                arriba=min(up_limit,programono['evolveLevel'])
                abajo=low_limit
                list_programones_factibles.append((abajo,arriba,programono))
            #si es evolucion de alguien y su nivel de evolucion es mayor a low 
            elif programono['evolveLevel']>low_limit and evolucion_de(programono,programones_ce)!=None:
                arriba=min(up_limit,programono['evolveLevel'])
                abajo=max(evolucion_de(programono,programones_ce)['evolveLevel'],low_limit)
                list_programones_factibles.append((abajo,arriba,programono))
        # para programon sin evolucion
        for programono in programones_se:
            if evolucion_de(programono,programones_ce)==None:
                #si no es evolucion de alguien
                arriba=up_limit
                abajo=low_limit
                list_programones_factibles.append((abajo,arriba,programono))
            elif evolucion_de(programono,programones_ce)!=None and evolucion_de(programono,programones_ce)['evolveLevel']<up_limit:
                # es evolucion de alguien
                arriba=up_limit
                abajo=max(evolucion_de(programono,programones_ce)['evolveLevel'],low_limit)
                list_programones_factibles.append((abajo,arriba,programono))
        #Elegir un progrmamon al azar
        random_programon=random.choice(list_programones_factibles)
        random_nivel=random.randint(random_programon[0],random_programon[1])
        id=random_programon[2]['id']

        return Programon(id,random_nivel)
                


            
    def do_damage(self,programon_a,programon_def):
        #elección de ataque del programon actual
        mensaje='Elige el ataque a realizar: \n'
        if programon_a.mov_disp():
            for i,move in enumerate(programon_a.mov_disp()):
                mensaje+='('+str(i)+') '+ move.name + ',Poder: '+str(move.power)+',Tipo: '+move.type+ ',Pp: '+str(move.pp)+',Accuracy:'+ str(move.accuracy)+',Daño aproximado: ' +str(move.calculo_daño(programon_a,programon_def))+'\n'
            mensaje+='Selecciona un ataque \n'
            indice_mov=int(input(mensaje))
            move=programon_a.mov_disp()[indice_mov]
            if  random.random() <= move.accuracy:
                daño=move.calculo_daño(programon_a,programon_def)
                print(programon_a.name+' realizó '+ move.name)
                print(programon_a.name+' realizó '+str(daño) +' de daño a '+programon_def.name+'\n')
                programon_def.hp-=daño
                print('A '+programon_def.name + ' le queda HP:'+str(programon_def.hp))
                move.pp-=1
            else:
                move.pp-=1
                print('El ataque falló \n')
        



        
        
            

    #funcion de recibir daño de un pokemon
    def recieve_damage(self,programon_a,programon_def):
        if programon_a.mov_disp()!=[]:
            move=random.choice(programon_a.mov_disp())
            if  random.random() <= move.accuracy:
                daño=move.calculo_daño(programon_a,programon_def)
                print(programon_a.name+' realizo '+move.name)
                print(programon_a.name+' realizo '+str(daño) +' de daño a '+programon_def.name +'\n')
                programon_def.hp-=daño
                move.pp-=1
            else:
                move.pp-=1
                print('El ataque falló \n')
        else:
            print('No hay ataques con pp \n')





    def prepare_team(self):
        self.team_battle=[]
        for id in self.team:
            for programono in self.programon:
                if id==programono.id:
                    programono.ready_to_fight()
                    self.team_battle.append(programono)

    def list_alive(self):
        return [programon for programon in self.team_battle if programon.hp>0]

    def pp_disponible(self):
        return True in [programon.mov_disp!=[] for programon in self.list_alive()]

    def add_progradex(self, programon):
        if not (programon.id in self.progradex):
            self.progradex.append(programon.id)
    
    def change_in_battle(self):
        if self.list_alive()!=[]:
            mensaje='Cambiar '+self.programon_in_battle.name+ ' por:\n'
            for i, programon in enumerate(self.list_alive()):
                mensaje+='('+str(i)+')'+programon.name+ ',level:'+str(programon.level)+',HP:'+str(programon.hp)+'\n'
            mensaje+='selecciona el indice \n'
            indice_cambio=int(input(mensaje))
            self.programon_in_battle=self.list_alive()[indice_cambio]
            print('Cambiaste a '+self.programon_in_battle.name +'\n')


    def catch_programon(self,programono):
        if self.qty_prograbolas>0:
            #probabilidad de atraparlo
            prob=(programono.initial_hp-programono.hp)/programono.initial_hp*0.8+0.2
            if prob>=random.random():
                self.qty_prograbolas-=1
                self.programon.append(programono)
                if len(self.team)<6:
                    self.team.append(programono.id)
                print('Muy bien atrapaste a '+programono.name+' Lvl '+ str(programono.level)+'\n')
                return True
            else:
                self.qty_prograbolas-=1
                print('Fallaste en atraparlo \n')
                return False
        else:
            print('No tienes prograbolas disponibles \n')
            return False
    

        


   
                
         
            
    def pelea_salvaje(self):
        #pokemon salvaje random
        salvaje=self.programon_factible_route()
        print('Encontraste un '+ salvaje.name + ' ,nivel ' +str(salvaje.level)+ ', a batallar! \n')
        #registrar en progradex
        self.add_progradex(salvaje)
        #creamos sus stats ,hp y mov
        salvaje.ready_to_fight()
        #guardamos el hp inicial que tenia el pokemon, para el calculo de la probabilidad de atraparlo 
        salvaje.initial_hp=int(salvaje.hp)
        #preparamos nuestro team en una lista de programones ocn sus stats creados
        self.prepare_team()
        #parte el prgramon mas rapido
        self.programon_in_battle=self.team_battle[0]
        self.programon_in_battle.peleo=True
        
        self.turno=True if self.programon_in_battle.speed>salvaje.speed else False
        #pelea se efectua mientras le quede hp a tu equipo y al salvaje

        while self.list_alive!= [] and salvaje.hp>0 and self.pp_disponible():
            if self.turno==True:
                print('Turno de '+self.name + '\n')
                print('Tu programon peleando es '+self.programon_in_battle.name+' Lvl:' +str(self.programon_in_battle.level)+ ' con HP: '+str(self.programon_in_battle.hp))
                #acciones del turno del jugador
                opcion=input('Que desea hacer en batalla:\n (0)Atacar \n (1)Cambio de programon \n (2)Intentar atrapar con prograbola disponibles:'+str(self.qty_prograbolas)  +'\n (3)Abandonar pelea \n')
                #al final del turno cambiar a turno salvaje 
                if opcion=='0':
                    self.do_damage(self.programon_in_battle,salvaje)

                elif opcion=='1':
                    self.change_in_battle()
                    if self.list_alive()==[]:

                        continue
                    self.programon_in_battle.peleo=True

                elif opcion=='2':
                    succes=self.catch_programon(salvaje)
                    if succes:
                        break

                elif opcion=='3':
                    print('abandonaste la pelea \n')
                    break
                    
                self.turno=False
            else:
                print('Turno de '+salvaje.name + '\n')
                self.recieve_damage(salvaje,self.programon_in_battle)
                if self.programon_in_battle.hp<0:
                    self.programon_in_battle.hp=0
                    print( self.programon_in_battle.name + ' ha quedado sin HP. \n')
                    #Agregar metodo de cambiar de pokemon
                    #ese metodo debe tener una condicion de si todos los del equipo tienen hp=0
                    self.change_in_battle()
                    self.programon_in_battle.peleo=True
                #cambiamos al turno de el jugador
                self.turno=True
        else:
            ##else de while que deja un registro
            dict_battle={'tipo':'salvaje'}
            dict_battle['equipo']=[programon.programon_dict_regis() for programon in self.team_battle]
            dict_battle['programon']=[salvaje.programon_dict()]
            if self.list_alive == [] or not(self.pp_disponible()):
                print('Fuiste derrotado por '+salvaje.name+'\n')
                dict_battle['victoria']=False
                self.money-=100
                dict_battle['dinero']=-100
                
            elif salvaje.hp<=0:
                print('Derrotaste a ' + salvaje.name)
                dict_battle['victoria']=True
                self.money+=100
                dict_battle['dinero']=100
                print('Ganaste $100')
                for programon in self.team_battle:
                    if programon.peleo:
                        programon.level+=1
                        print(programon.name +' subio a nivel '+str(programon.level) +'\n')
                        # Metodo de evolucion de programon

            self.battles.append(dict_battle)
            #reser del registro
            for programon in self.team_battle:
                programon.peleo=False
            
    def battle_gym(self):
        print('Entraste al gimnasio\n')
        #Elección de entrenador
        mensaje='A quien deseas batallar:\n'
        #instancia de ciudad en la que se está
        city=mapa[self.actual_location]
        #creamos el mensaje para la opcion de trainer a batallar
        mensaje+= '(0) Lider :'+city.leader['name']+ '\n'
        for i,trainer in enumerate(city.trainers):
            mensaje+= '('+str(i+1)+')'+' Trainer :'+trainer['name'] +'\n'
        selec=input(mensaje)
        #en el caso de que se quiera batallar al lider
        if selec=='0':
            trainer=Trainer(city.name,leader=True)
        #en el caso de que sea otro entrenador
        else:
            dict_trainer=city.trainers[int(selec)-1]
            trainer=Trainer(city.name,False,dict_trainer['name'])
        self.prepare_team()
        trainer.prepare_team()
        self.programon_in_battle=self.team_battle[0]
        trainer.programon_in_battle=trainer.team_battle[0]
        self.add_progradex(trainer.programon_in_battle)
        self.programon_in_battle.peleo=True
        trainer.programon_in_battle.peleo=True
        self.turno=True if self.programon_in_battle.speed>=trainer.programon_in_battle.speed else False
        
        while self.list_alive()!=0 and trainer.list_alive()!=0 and self.pp_disponible() and trainer.pp_disponible():
            if self.turno==True:
                print('Turno de '+self.name + '\n')
                print('Tu programon peleando es '+self.programon_in_battle.name+' Lvl:' +str(self.programon_in_battle.level)+ ' con HP: '+str(self.programon_in_battle.hp))
                print('Su programon peleando es '+trainer.programon_in_battle.name+' Lvl:' +str(trainer.programon_in_battle.level)+ ' con HP: '+str(trainer.programon_in_battle.hp)+'\n')
                #acciones del turno del jugador
                opcion=input('Que desea hacer en batalla:\n (0)Atacar \n (1)Cambio de programon \n (2)Abandonar pelea \n')
                #al final del turno cambiar a turno salvaje 
                if opcion=='0':
                    self.do_damage(self.programon_in_battle,trainer.programon_in_battle)
                    if trainer.programon_in_battle.hp<0:
                        trainer.programon_in_battle.hp=0
                        print( trainer.programon_in_battle.name + ' ha quedado sin HP. \n')
                    #Agregar metodo de cambiar de pokemon
                    #ese metodo debe tener una condicion de si todos los del equipo tienen hp=0
                        trainer.change_in_battle()
                        self.add_progradex(trainer.programon_in_battle)
                        trainer.programon_in_battle.peleo=True

                elif opcion=='1':
                    self.change_in_battle()
                    if self.list_alive()==[]:
                        continue
                    self.programon_in_battle.peleo=True

                elif opcion=='2':
                    print('abandonaste la pelea \n')
                    break
                    
                self.turno=False
            else:
                print('Turno de '+trainer.name + '\n')
                print('Su programon peleando es '+trainer.programon_in_battle.name+' Lvl:' +str(trainer.programon_in_battle.level)+ ' con HP: '+str(trainer.programon_in_battle.hp))
                print('Tu programon peleando es '+self.programon_in_battle.name+' Lvl:' +str(self.programon_in_battle.level)+ ' con HP: '+str(self.programon_in_battle.hp)+'\n')
                self.recieve_damage(trainer.programon_in_battle,self.programon_in_battle)
                if self.programon_in_battle.hp<0:
                    self.programon_in_battle.hp=0
                    print( self.programon_in_battle.name + ' ha quedado sin HP. \n')
                    #Agregar metodo de cambiar de pokemon
                    #ese metodo debe tener una condicion de si todos los del equipo tienen hp=0
                    self.change_in_battle()
                    self.programon_in_battle.peleo=True
                #cambiamos al turno de el jugador
                self.turno=True
        else:
            ##else de while que deja un registro
            dict_battle={'tipo':'trainer','name':trainer.name}
            dict_battle['equipo']=[programon.programon_dict_regis() for programon in self.team_battle]
            dict_battle['programon']=[programon.programon_dict_regis() for programon in trainer.team_battle]
            if self.list_alive == [] or not(self.pp_disponible()):
                print('Fuiste derrotado por '+trainer.name+'\n')
                dict_battle['victoria']=False
                self.money-=100
                dict_battle['dinero']=-100
                
            elif trainer.list_alive == [] or not(trainer.pp_disponible()):
                print('Derrotaste a ' + trainer.name)
                dict_battle['victoria']=True
                self.money+=200
                dict_battle['dinero']=200
                print('Ganaste $200')
                for programon in self.team_battle:
                    if programon.peleo:
                        programon.level+=1
                        print(programon.name +' subio a nivel '+str(programon.level) +'\n')
                        # Metodo de evolucion de programon
                if trainer.leader==True:
                    self.medals.append[mapa[self.actual_location].id]

            self.battles.append(dict_battle)
            #reser del registro
            for programon in self.team_battle:
                programon.peleo=False





 


            

        

        
        

    
    def action_pallet_town(self):
        ##funcion relacionada con acciones en Pallet town
        while True:
            selec_city=input('Qué deseas hacer en la ciudad: \n (0) Ir a Centro Programon: \n (1) Volver al menu principal')
            if selec_city=='0':
                #funcion relacionada con el centro programon
                self.centro_programon()
            if selec_city=='1':
                break
    
    def action_city(self):
        
        while True:
            selec_city=input('Qué deseas hacer en la ciudad: \n (0) Ir a Centro Programon: \n (1) Batallar el Gimnasio: \n (2) Ir a la tienda de prograbolas: \n (3) Volver al menu principal')
            if selec_city=='0':
                #funcion realcionada con el centro programon
                self.centro_programon()
            if selec_city=='1':
                #funcionar para batallar con el gimnasio
                self.battle_gym()
            if selec_city=='2':
                #funcionar para ir a tienda de prograbolas
                self.tienda_prograbolas() 
            if selec_city=='3':
                break

    def buscar_por_id(self,id):
         return [programon for programon in self.programon if programon.id==id][0]

    def centro_programon(self):
        #funcion relacionada con cambiar el equipo actual del jugador para batalla
        mensaje='Cual de los programones en tu equipo deseas cambiar?\n'
        for i,id in enumerate(self.team):
            programon=self.buscar_por_id(id)
            mensaje+='('+str(i)+') '+programon.name+' lvl: '+str(programon.level)+'\n'
        programon_a_salir=int(input(mensaje))

        mensaje='Cambiar por:\n '
        for i,programon in enumerate(self.programon):
            mensaje+='('+str(i)+') '+programon.name+' lvl: '+str(programon.level)+'\n'
        
        del self.team[programon_a_salir]
        while True:
            programon_a_entrar=int(input(mensaje))
            if self.programon[programon_a_entrar].id in self.team:
                print('No puede entrar un programon que ya esta en tu equipo!\n')
            else:
                self.team.append(self.programon[programon_a_entrar].id)
                print('Programon cambiado')
                break
        
            

    
    
    def tienda_prograbolas(self):
        #funcion donde se opta a comprar prograbolas
        print('Bienvenido a la tienda de prograbolas\n')
        while True:
            print('Dinero disponible: ' + str(self.money))
            print('Te alcanzan para '+str(round(self.money/100)))

            opcion=input('¿Cuantas prograbolas deseas comprar?\n (0)Salir') 
            if opcion=='0':
                print('Vuelve pronto!')
                break
            elif int(opcion)*100>self.money:
                print('No tienes dinero suficiente')
            else:
                self.money-=int(opcion)*100
                self.qty_prograbolas+=int(opcion) 
                break

class Trainer(Jugador):
    def __init__(self, city, leader, name=None):
        dict_city=[dict for dict in jsonReader.jsonToDict('gyms.json') if dict['city']==city][0]
        if leader==True:
            dict_trainer=dict_city['leader']
        else:
            dict_trainer= [dict for dict in dict_city['trainers'] if dict['name']==name][0]
        self.name=dict_trainer['name']
        self.programon=[Programon(programon['id'],programon['level']) for programon in dict_trainer['programones']]
        self.team=[programon['id'] for programon in dict_trainer['programones']]
        if leader==True:
            self.leader=True
        else:
            self.leader=False
    def change_in_battle(self):
        if self.list_alive()!=[]:
            self.programon_in_battle=random.choice(self.list_alive())
            print(self.name + ' cambio su programon a '+self.programon_in_battle.name +'\n')



class Programon():
    def __init__(self,id,level,iv=random.randint(0,15),ev=random.randint(0,65535)):
        #buscamos el diccionario del programon en programones.json
        dict_programon=[programon for programon in jsonReader.jsonToDict('programones.json') if programon['id']==id][0]
        self.id=dict_programon['id']
        self.type=dict_programon['type']
        self.level=level
        self.name=dict_programon['name']
        #asignar evolucion si es que tiene en el caso de que no tenga entregar none
        if 'evolveLevel' in dict_programon.keys():
            self.evolveLevel=dict_programon['evolveLevel']
            self.evolveTo=dict_programon['evolveTo']
        #se dejara como none en los que no tengan evolucion
        else:
            self.evolveLevel=None
            self.evolveTo=None
        self.base_hp=dict_programon['hp']
        self.base_special_defense=dict_programon['special_defense']
        self.base_special_attack=dict_programon['special_attack']
        self.base_defense=dict_programon['defense']
        self.base_attack=dict_programon['attack']
        self.base_speed=dict_programon['speed']
        self.moves=dict_programon['moves']
        self.iv=iv
        self.ev=ev
        self.peleo=False

    #funcion que dejara en dict a los programones del jugador 
    def programon_dict(self):
        dic_programon={}
        dic_programon['id']=self.id
        dic_programon['iv']=self.iv
        dic_programon['ev']=self.ev
        dic_programon['level']=self.level
        return dic_programon

    def programon_dict_regis(self):
        dict=self.programon_dict()
        dict['peleo']=True if self.peleo==True else False
        return dict


    def get_stats(self):
        self.defense=5+(self.level*((self.base_defense+self.iv)*2+((self.ev**0.5)/4))/100)
        self.attack=5+(self.level*((self.base_attack+self.iv)*2+((self.ev**0.5)/4))/100)
        self.special_attack=5+(self.level*((self.base_special_attack+self.iv)*2+((self.ev**0.5)/4))/100)
        self.special_defense=5+(self.level*((self.base_special_defense+self.iv)*2+((self.ev**0.5)/4))/100)
        self.speed=5+(self.level*((self.defense+self.iv)*2+((self.ev**0.5)/4))/100)

    def get_hp(self):
        self.hp=10+self.level+(self.level*((self.base_hp+self.iv)*2+((self.ev**0.5)/4))/100)
    
    def get_moves(self):
        self.moves_battle=[Move(name) for name in self.moves]

    def ready_to_fight(self):
        self.get_hp()
        self.get_stats()
        self.get_moves()

    def mov_disp(self):
       return [mov for mov in self.moves_battle if mov.pp>0]






class City():
    def __init__(self,id):
        if id==0:
            self.name='Pallet Town'
            self.id=0
            self.leader=None
            self.trainers=None
        else:
            city_dict=[city for city in jsonReader.jsonToDict('gyms.json') if city['id']==id][0]
            self.name=city_dict['city']
            self.id=city_dict['id']
            self.leader=city_dict['leader']
            self.trainers=city_dict['trainers']
    #def __repr__(self):
        #return 'city '+str(self.name)
    



class Route():
    def __init__(self,route,i):
        rout_dict=[ruta for ruta in jsonReader.jsonToDict('routes.json') if ruta['route']==route][0]
        self.starting_point=rout_dict['starting_point']
        self.destination=rout_dict['destination']
        self.name=rout_dict['route']
        self.levels=rout_dict['levels']
        self.pos=i
    #def __repr__(self):
        #return 'ruta '+str(self.route)+'pos '+str(self.pos)

#Creamos mapa del juego
mapa=[City(0)]
for e in range(1,9):
    mapa+=[Route(e,i) for i in range(0,3)]+[City(e)]


class Move():
    # move es el string con el nombre del movimiento
    def __init__(self,move):
        #lista de todos lo moves lista de diccionarios
        lista_moves=jsonReader.jsonToDict('programonMoves.json')
        dict_mov=[i for i in lista_moves if i['name']==move][0]
        self.pp=dict_mov['pp']
        self.accuracy=dict_mov['accuracy']
        self.type=dict_mov['type']
        self.power=dict_mov['power']
        self.name=dict_mov['name']

    def calculo_daño(self,p_atacante,p_defensor):
        #calculamos el modificador primero
        #potenciador si ataque es del mismo tipo que el programon que ataca
        STAB= 1.5 if self.type==p_atacante.type else 1
        #modificador de daños segun tipo del ataque y tipo de programon defensor
        lista_types=jsonReader.jsonToDict('types.json')
        Tipo=lista_types[self.type][p_defensor.type] if p_defensor.type in lista_types[self.type].keys() else 1 
        #factor de ataque crítico
        T=p_atacante.base_speed/2
        P=random.randint(0, 256)
        Critico= 2 if P<=T else 1
        #numero random de ataque
        num_random=random.randint(85,100)/100
        #valor modificador
        modificador=STAB*Tipo*Critico*num_random
        #definir si es que el ataque es de algún tipo especial        
        dict_category=jsonReader.jsonToDict('moveCategories.json')
        especial=True if self.type in dict_category["special_moves"] else False
        #calculo daño
        if especial:
            daño=((2*p_atacante.level+10)/250*(p_atacante.special_attack/p_defensor.special_defense)*self.power+2)*modificador
        else:
            daño=((2*p_atacante.level+10)/250*(p_atacante.attack/p_defensor.defense)*self.power+2)*modificador
        return daño
        



#Testing
if __name__ == '__main__':
    #inicializar jugador nuevo correcto
    #jugador=Jugador('Felipe','uvfla831',True)
    #print(jugador.name,jugador.password,jugador.medals,jugador.money,jugador.team,jugador.progradex,
    #jugador.battles,jugador.qty_prograbolas,jugador.actual_location,[(programon.name,programon.level,programon.iv,
    #programon.ev,programon.evolveTo,programon.moves) for programon in jugador.programon])

    #random programon salvaje
    #jugador.actual_location=31
    #random_pro=jugador.programon_factible_route()
    #print(mapa[jugador.actual_location].levels)
    #random_pro.get_stats()
    #print(random_pro.name)
    #print(random_pro.attack,random_pro.defense,random_pro.speed)
    #random_pro.get_hp()
    #print(random_pro.hp)
    #random_pro.get_moves()
    
    #calculo daño de ataque
    #pok1=Programon(101,30)
    #pok1.get_hp()
    #pok1.get_stats()
    #pok1.get_moves()
    #pok2=Programon(96,30)
    #pok2.get_hp()
    #pok2.get_stats()
    #print(pok2.hp)
    #print(pok1.moves_battle[1].calculo_daño(pok1,pok2))






    #inicializar cargado
    #jugador=Jugador('Florencia','tucontrasena',False)
    #print(jugador.name,jugador.password,jugador.medals,jugador.money,jugador.team,jugador.progradex,
    #jugador.battles,jugador.qty_prograbolas,[(programon.name,programon.level,programon.iv,
    #programon.ev,programon.evolveTo,programon.moves) for programon in jugador.programon])
    
    #guardar partida
    #jugador.jugador_json()

    #iniciar ciudad
    #ciudad=City(0)
    #print(ciudad.name,ciudad.id,ciudad.leader)
    
    #iniciar route
    #ruta=Route(8,1)
    #print(ruta.levels)
    #jugador.actual_location=4
    #jugador.programon.append(Programon(107,100))
    #jugador.team.append(107)
    #jugador.programon.append(Programon(25,100))
    #jugador.team.append(25)
    
    
    #jugador.battle_gym()
        
    for inst in mapa:
        print(inst.name)