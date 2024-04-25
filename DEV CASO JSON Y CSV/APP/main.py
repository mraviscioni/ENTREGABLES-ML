import Include.functions as fn
import os 

#Defino los path donde estan alojados los archivos
strJsonPath	= "Json/base_datos.json"
strCsvPath	= "CSV/User_Managers.csv"
strPATHRESULT = "Result/"

result = fn.ProcesarAutorizacion(strJsonPath, strCsvPath)
print("-|| LISTADO MANAGER'S PARA SOLICITAR APROBACION ||-")
print(result["MANAGER"])
print("")
print("-|| LISTADO DE MANAGER's EXCLUIDOS ||-")
print(result["EXCLUIDOS"])
print("")
print("-|| LISTADO DE REGISTROS ERRONEOS ||-")
print(result["ERRORES"])
print("")

print("Desea Exportar los resultados? \n - Digite 1 para exportar \n - Digite 0 para omitir la exportacion")
boolExport = input()

if int(boolExport) == 1:
	result["MANAGER"].to_csv(strPATHRESULT + "Manager_notification.csv", index=False)
	result["EXCLUIDOS"].to_csv(strPATHRESULT + "Manager_exluidos.csv", index=False)
	result["ERRORES"].to_csv(strPATHRESULT + "Error_data.csv", index=False)
	
	clear()
	print("Se generaron los siguientes archivos:")

	for export in os.listdir(strPATHRESULT):
		print("- ./" + strPATHRESULT + str(export))
#	print("Usted puede encontrar los resultados en la siguiente ruta:" + str(os.path.dirname(strPATHRESULT)))
print("")
print("Se realizo la revalida exitosamente")
