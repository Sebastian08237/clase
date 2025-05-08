from flask import Flask, request, jsonify
import math
from EstudianteGestion import EstudianteEjemplo
from flask_cors import CORS
#from flask_oidc import OpenIDConnect
#from keycloak import KeycloakOpenID
#import json
#import os
#from functools import wraps


app = Flask(__name__)
CORS(app)

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
#KEYCLOAK_CONFIG_PATH = os.path.join(BASE_DIR, "keycloak.json")


#with open(KEYCLOAK_CONFIG_PATH, "r") as f:
#    keycloak_config = json.load(f)

#print("Contenido de keycloak.json:", keycloak_config)

#app.config.update({
 #   "OIDC_CLIENT_SECRETS": KEYCLOAK_CONFIG_PATH,  
  #  "OIDC_SCOPES": ["openid", "profile", "email"],
   # "OIDC_INTROSPECTION_AUTH_METHOD": "client_secret_post"
#})

#oidc = OpenIDConnect(app)

#def token_required(func):
    #@wraps(func)  
    #def wrapper(*args, **kwargs):
    #    if not oidc.user_loggedin:
   #         return jsonify({"mensaje": "No autorizado"}), 401
  #      return func(*args, **kwargs)
 #   return wrapper
estudiantes = []

@app.route('/listaEstudiantes', methods=['GET'])
#@token_required
def lista_estudiantes():
    estudiante = EstudianteEjemplo("1","Jorge","30")
    estudiante1 = EstudianteEjemplo("2","Ana","23")
    estudiante2 = EstudianteEjemplo("3","Luis","28")
    estudiante3 = EstudianteEjemplo("4","Gabriel","25")
    estudiante4 = EstudianteEjemplo("5","Luciana","24")
    estudiante4 = EstudianteEjemplo("6","Laura","29")
    estudiantes.append(estudiante.to_json())
    estudiantes.append(estudiante1.to_json())
    estudiantes.append(estudiante2.to_json())
    estudiantes.append(estudiante3.to_json())
    estudiantes.append(estudiante4.to_json())
    return jsonify(estudiantes)

@app.route('/crearEstudiante', methods=['POST'])
#@token_required
def crear_estudiante():
    data = request.get_json()
    nombre = data.get('nombre')
    codigo = data.get('codigo')
    promedio = data.get('promedio')
    
    estudiante = EstudianteEjemplo(nombre, codigo, promedio)
    estudiantes.append(estudiante.to_json())
    
    return jsonify({"mensaje": "Estudiante creado exitosamente"}), 201

@app.route('/obtenerEstudiante/<codigo>', methods=['GET'])
def obtener_estudiante(codigo):
    estudiante = next((e for e in estudiantes if e['codigo'] == codigo), None)
    
    if estudiante is not None:
        return jsonify(estudiante), 200
    else:
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404

@app.route('/actualizarEstudiante/<codigo>', methods=['PUT'])
def actualizar_estudiante(codigo):
    data = request.get_json()
    estudiante = next((e for e in estudiantes if e['codigo'] == codigo), None)
    
    if estudiante is not None:
        estudiante['nombre'] = data.get('nombre', estudiante['nombre'])
        estudiante['promedio'] = data.get('promedio', estudiante['promedio'])
        
        return jsonify({"mensaje": "Estudiante actualizado exitosamente"}), 200
    else:
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404

@app.route('/eliminarEstudiante/<codigo>', methods=['DELETE'])
def eliminar_estudiante(codigo):
    global estudiantes
    estudiantes = [e for e in estudiantes if e['codigo'] != codigo]
    
    return jsonify({"mensaje": "Estudiante eliminado exitosamente"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
