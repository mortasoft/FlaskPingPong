import random
import time
from flask import Flask, request, jsonify,json

########################################################################################################################
# AQUÍ INICIALIZAMOS LAS VARIBLES Y EL APP.

app = Flask(__name__)
vectorPartida = []
vectorRespuesta = []
cantidadDeClientes = 0
descripcion = ""
jugador1 = ""
jugador2 = ""
historico = ""
contadorJugador1 = 0
contadorJugador2 = 0

########################################################################################################################
# AQUÍ SERÁ DONDE ALMACENAREMOS LOS HISTÓRICOS DE CADA JUGADOR (1 Y ) Y EL GLOBAL DE COMO QUEDÓ LA PARTIDA.

Resultado= [
    {
        'tipo': 'jugador1',
        'registro': ''

    },{
        'tipo': 'jugador2',
        'registro': ''
    },{
        'tipo': 'historico',
        'registro': ''
    }
]

########################################################################################################################
#LAS RUTAS DONDE NOS SERVIRÁ PARA EMPEZAR EL PARTIDO, Y PARA BUSCAR LOS HISTÓRICOS DE JUGADOR 1, 2 Y EL GLOBAL.

@app.route('/pingpong/api/start/<string:tipo_de_resultado>', methods = ['GET'])
def get_data(tipo_de_resultado):
    tipo = [tipo for tipo in Resultado if tipo['tipo'] == tipo_de_resultado]
    return jsonify({'Resultado':tipo[0]})


@app.route("/pingpong/api/start", methods=['GET'])
def start_game():
    global cantidadDeClientes
    cantidadDeClientes += 1
    if cantidadDeClientes == 2:
        print("JUGADOR = " + str(cantidadDeClientes))
        juego()
        cantidadDeClientes = 0
        return "TERMINO LA PARTIDA."
    else:
        print("JUGADOR = " + str(cantidadDeClientes))
        return jsonify("ESPERE EL JUGADOR 2 Y AUTOMATICAMENTE EMPEZARA LA PARTIDA")

########################################################################################################################
#   AQUÍ COMIENZA LA LÓGICA DEL JUEGO
def juego():
    global jugador1
    global jugador2
    global historico
    global contadorJugador1
    global contadorJugador2
    jugador1 = [tipo for tipo in Resultado if tipo['tipo'] == 'jugador1']
    jugador2 = [tipo for tipo in Resultado if tipo['tipo'] == 'jugador2']
    historico =[tipo for tipo in Resultado if tipo['tipo'] == 'historico']

    print('¡¡¡¡¡COMENZÓ EL JUEGO!!!!!')
    for puntoContador in range(0,3):
        punto = random.randint(0,1)
        print('---------------------------------------------------------------------')
        time.sleep(1)
        continuar_jugador1("PUNTO NUMERO = " + str(puntoContador+1) + ", ")

        lanzamientoJugador1 = random.randint(0,1)
        if lanzamientoJugador1 == 0:
            continuar_jugador1("EL JUGADOR 1 lanzo al lado izquierdo, ")
        else:
            continuar_jugador1("EL JUGADOR 1 lanzo al lado derecho, ")

        recepcionJugador2 = random.randint(0,1)
        if recepcionJugador2 == 0:
            continuar_jugador2("EL JUGADOR 2 recibe por el lado izquierdo, ")
        else:
            continuar_jugador2("EL JUGADOR 2 recibe por el lado derecho, ")

        if recepcionJugador2 != lanzamientoJugador1:
            contadorJugador1 += 1
            continuar_jugador1("PUNTO NUMERO = " + str(puntoContador+1) + " PARA JUGADOR 1 [{}/{}]".format(contadorJugador1,contadorJugador2) + ", ")
            if (puntoContador+1) == 3:
                if contadorJugador1 > contadorJugador2:
                    continuar_jugador1("EL GANADOR ES JUGADOR 1, ")
                else:
                    continuar_jugador2("EL GANADOR ES JUGADOR 2, ")
                return imprimaYEnvie()
        else:
            sigueEnJuego(puntoContador)
            if (puntoContador+1) == 3:
                if contadorJugador1 > contadorJugador2:
                    continuar_jugador1("EL GANADOR ES JUGADOR 1 [{}/{}]".format(contadorJugador1,contadorJugador2) + ", ")
                else:
                    continuar_jugador2("EL GANADOR ES JUGADOR 2 [{}/{}]".format(contadorJugador1,contadorJugador2) + ", ")
                return imprimaYEnvie()

def sigueEnJuego(punto):
    global contadorJugador1
    global contadorJugador2

    lanzamientoJugador2 = random.randint(0, 1)
    if lanzamientoJugador2 == 0:
        continuar_jugador2("EL JUGADOR 2 lanzo al lado izquierdo, ")
    else:
        continuar_jugador2("EL JUGADOR 2 lanzo al lado derecho, ")

    recepcionJugador1 = random.randint(0, 1)
    if recepcionJugador1 == 0:
        continuar_jugador1("EL JUGADOR 1 recibe por el lado izquierdo, ")
    else:
        continuar_jugador1("EL JUGADOR 1 recibe por el lado derecho, ")

    if recepcionJugador1 != lanzamientoJugador2:
        contadorJugador2 += 1
        continuar_jugador2("PUNTO NUMERO = " + str(punto + 1) + " PARA JUGADOR 2 [{}/{}]".format(contadorJugador1,contadorJugador2) + ", ")
        if (punto+1) == 3:
            print("\n\nTEEEEEERMINO EL JUEGO!!!!!\nEL JUEGO QUEDO ASI:\n")
            print(vectorRespuesta)
    else:
        sigueEnJuego(punto)

def imprima(descripcion):
        return jsonify(descripcion)

def continuar_jugador1(descripcion):
    global vectorRespuesta
    global jugador1
    global historico
    vectorRespuesta.append(descripcion)
    print(descripcion)
    imprima(descripcion)
    jugador1[0]['registro'] += descripcion
    historico[0]['registro'] += descripcion
    time.sleep(0.3)

def continuar_jugador2(descripcion):
    global vectorRespuesta
    global jugador2
    global historico
    vectorRespuesta.append(descripcion)
    print(descripcion)
    imprima(descripcion)
    jugador2[0]['registro'] += descripcion
    historico[0]['registro'] += descripcion
    time.sleep(0.3)

def imprimaYEnvie():
    global vectorRespuesta
    return jsonify(vectorRespuesta)


########################################################################################################################
#CORRER NUESTRO SERVER.
if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port = 5000)