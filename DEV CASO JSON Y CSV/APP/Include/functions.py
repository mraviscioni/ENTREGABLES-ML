import json
import pandas as pd
import re

# FUNCIONES
# ************************************************
#FUNCION PARA RECUPERAR CSV
def RecuperarCSV(PATH):
	objData = pd.read_csv(PATH)
	return objData

# FUNCION PARA RECUPERAR JSON
def RecuperarJSON(PATH):
	#RECUPERO EL JSON y lo LEO
	with open(str(PATH), 'r') as strJsonContent:
		obj = json.load(strJsonContent) #Recupero la info del JSON 
	return obj

# FUNCION PARA NORMALIZAR STRINGS
def NormalizeString(STR):
	return str(STR).lower().lstrip()

def CheckValidMail(email):

    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

    if re.match(regex, email):
        return True
    else:
        return False

# FUNCION PRINCIPAL===================================================
def ProcesarAutorizacion(JSONPATH, CSVPATH):

	#RECUPERO EL JSON y lo LEO
	arrBBDD = RecuperarJSON(JSONPATH)
	lstDB = [] #Armo una nueva lista solo con las bbdd high
	lstDBERROR = [] #Armo una nueva lista para llevar la trazabilidad de errores

	for i in arrBBDD:
		# VALIDO QUE LOS DATOS REQUERIDOS NO ESTEN VACIOS
		valClasificacion = NormalizeString(i["clasificacion"])
		valDbName		 = NormalizeString(i["nombre_db"])
		valUserId		 = NormalizeString(i["user_id"])

		if valClasificacion != "" and  valDbName != "" and valUserId != "":
			if valClasificacion == "high": #DEJO SOLO LAS BBDD QUE TIENEN CLASIFICACION HIGH
				lstDB.append(i)
		else:
			lstDBERROR.append(i) #AGREGO TODOS LOS REGISTROS CON ALGUN DATO REQUERIDO FALTANTE

	# LEVANTO EL CSV DEL TIPO DATAFRAME
	objCSV = RecuperarCSV(CSVPATH) 

	# ARMO LAS CABECERAS DE LA BASE DE DATOS DE RESULTADOS
	dfColumns		= ["DB_NAME", "EMAIL_OWNER", "EMAIL_MANAGER", "CLASIFICATION"]
	dfTable			= pd.DataFrame(columns=dfColumns)
	dfUsrNoMatch	= pd.DataFrame(columns=dfColumns)

	# RECORRO MI LISTA DE BBDD CLASIFICADAS HIGH Y BUSCO LOS MANAGER DE CADA UNA DE ESTAS SEGUN
	for dbElement in lstDB:
		#POR CADA DB RECORRO LA LISTA DE USUARIO Y MANAGER
		for i in range(len(objCSV)):
			
			regUsr = objCSV.iloc[i]
			
			#Evaluo si el reg del CSV machea con la BBDD que estoy analizando
			if regUsr["user_id"] == dbElement["user_id"]:
				# ARMO UN DATAFRAME CON LO SOLICITADO PARA DESPUES EXPORTARLO A CSV
				dfTable = dfTable._append({	"DB_NAME":			NormalizeString(dbElement["nombre_db"]).upper(), 
											"EMAIL_OWNER":		NormalizeString(dbElement["user_id"]), 
											"EMAIL_MANAGER":	NormalizeString(regUsr["user_manager"]), 
											"CLASIFICATION":	NormalizeString(dbElement["clasificacion"])}, 
											ignore_index=True)

			else:
				#Evaluo cual fue el error, si es porque el mail no tiene una estructura valida o bien no machea el registro con lo que busco.
				
				if CheckValidMail(regUsr["user_manager"]) : 
					strERROR = "NO MATCH" 
				else:
					strERROR = "INVALID EMAIL"
				
				dfUsrNoMatch = dfUsrNoMatch._append({	
											"DB_NAME":			NormalizeString(dbElement["nombre_db"]).upper(), 
											"EMAIL_OWNER":		NormalizeString(dbElement["user_id"]), 
											"EMAIL_MANAGER":	NormalizeString(regUsr["user_manager"]), 
											"CLASIFICATION":	NormalizeString(dbElement["clasificacion"]),
											"ERROR":			strERROR}, 
											ignore_index=True)

	objReturn = {"MANAGER":dfTable, "EXCLUIDOS":dfUsrNoMatch, "ERRORES": pd.DataFrame(lstDBERROR, columns=["nombre_db", "clasificacion","user_id"])}
	return objReturn
