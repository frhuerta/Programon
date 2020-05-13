import clases
import jsonReader
import random

#iniciar con consulta de nueva partida o partida existente
#pedir usuario y contraseña (al crear partida pedir contraseña dos veces)
while True:
    opcion=input('¡Juego Programon!\n (0)Nueva partida\n (1)Cargar partida\n')
    if opcion=='0':
        name=input('Cual es tu nombre:\n')
        while True:
            password=input('Crea una contraseña:\n')
            verificar=input('Confirma tu contraseña:\n')
            if password==verificar:
                jugador=clases.Jugador(name,password,True)
                break
            else:
                print('Fallaste en verificar tu contraseña\n')
        break
    elif opcion=='1':
        name=input('Cual es tu nombre:\n')
        while True:
            password=input('Cual es la contraseña de la partida\n')
            try:
                dict_jugador=jsonReader.jsonToDict(str(name)+'.json')['id_jugador']
            except:
                print('Partida no existe\n')
            if dict_jugador['password']==password:
                jugador=clases.Jugador(name,password,False)
                print('Partida cargada\n')
                break
            else:
                print('Contraseña incorrecta\n')
                continue
        break

    else:
        print('opcion inválida\n')
print('\n\n')
while True:
    menu=input('Menu principal:\n (0)Caminar\n (1)Ver progradex\n (2)Datos del jugador\n (3)Salir del sistema')

    if menu=='0':
        direccion=input('Caminar hacia:\n (0)Adelante\n (1)Atrás\n')
        if direccion=='0' and jugador.actual_location==32:
            print('Estas al final del mapa no puedes avanzar')
        elif direccion=='1' and jugador.actual_location==0:
            print('Estas al inicio del mapa no puedes retroceder')
        else:
            direct=1 if direccion=='0' else -1
            jugador.actual_location+=direct
            
            if clases.mapa[jugador.actual_location].__class__.__name__=='Route':
                print('\nEstas en ruta'+ ' '+str(clases.mapa[jugador.actual_location].name)+'\n')
                prob=random.randint(0,100)
                if prob<=30:
                    jugador.pelea_salvaje()
                else:
                    print('avanzaste')
            elif clases.mapa[jugador.actual_location].__class__.__name__=='City' and jugador.actual_location!=0:
                print('\nEstas en '+ str(jugador.actual_location)+' '+clases.mapa[jugador.actual_location].name+'\n')
                jugador.action_city()
            elif clases.mapa[jugador.actual_location].__class__.__name__=='City' and jugador.actual_location==0:
                print('\nEstas en '+ str(jugador.actual_location)+' '+clases.mapa[jugador.actual_location].name+'\n')
                jugador.action_pallet_town()
        

    
    elif menu=='1':
        jugador.ver_progradex()
    
    elif menu=='2':
        jugador.datos_jugador()
    
    elif menu=='3':
        jugador.jugador_json()
        print('Partida guardada\nSaliste de la partida')
        break
    
    else:
        print('Opcion no valida, intente de nuevo\n')
        continue