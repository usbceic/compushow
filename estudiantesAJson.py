###############################################################
# Script para pasar la lista de estudiantes a un archivo json #
#                                                             #
# Entrada: listaDeEstudiantes.txt                             #
#                                                             #
#          Que es la lista de estudiantes inscritos en el     # 
#          trimestre y debe tener el siguiente formato        #
#          (separado por tabuladores):                        #
#                       carnet  cedula  apellidos nombres     #
#                                                             #
# Salida: nombreDelArchivo.json                               #
#                                                             #
# Una vez obtenido el archivo json, se puede ejecutar el sig  #
# comando:                                                    #
#                                                             #
#       python manage.py loaddata nombreDelArhivo.json        #
#                                                             #
# Donde 'nombreDelArchivo' es el nombre del archivo de salida #
# para cargar a la base de datos a todos los estudiantes      #
#                                                             #
# Autor: Ivan Travecedo - Rosangelis Garcia                   #
#                                                             #
###############################################################

import sys

if len(sys.argv)<3 or len(sys.argv)>3:
  print "Entrada invalida"
  print "Formato esperado:"
  print "\tpython estudiantesAjson.py <archivo1> <archivo2>\n"
  print "Donde:"
  print "\t- archivo1: Archivo plano con la lista de estudiantes inscritos"
  print "\tcon el siguiente formato: carnet cedula apellidos nombres"
  print "\tun estudiante por fila y todos los campos separados por tabuladores"
  print "\n\t- archivo2: Nombre del archivo de salida. Debe ser un archivo .json"

else:
  archivotxt = open(sys.argv[1])
  archivojson = open(sys.argv[2],'w')

  archivojson.write("[\n")

  while True:
    estudiante = archivotxt.readline()
    if not estudiante:
      posicionActual = archivojson.tell()
      archivojson.seek(posicionActual-3)
      archivojson.write("}")
      archivojson.write("\n]")
      archivotxt.close()
      archivojson.close()

      break
    e = estudiante.split('\t')
    archivojson.write("{\n")
    archivojson.write("  \"pk\": \""+e[0][0:2]+"-"+e[0][2:]+"\",\n")
    archivojson.write("  \"model\": \"votaciones.carnet\",\n")
    archivojson.write("  \"fields\": {\n")
    archivojson.write("    \"nombre\": \""+e[3][:len(e[3])-1]+" "+e[2]+"\",\n")
    archivojson.write("    \"usado\": \"False\"\n")
    archivojson.write("  }\n")
    archivojson.write("},\n")