from tkinter import *
from tkinter.filedialog import askopenfilename
from urllib.parse import MAX_CACHE_SIZE
from lxml import etree
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

###############
# RAIZ
##############
root= Tk()
root.title("Imprimir archivo .XML")
root.resizable(1, 1)            # width, height (redimensionamiento, verdadero o falso)
root.iconbitmap("gtc.ico")  # Icono
root.geometry("650x350")       # El tamaño de la raiz se adapta al tamaño del frame
root.config(bg="green") #bg=background
root.config(bd=10)
root.config(relief="groove")

################
#FRAME
###############
miFrame= Frame(root, width= 500, height= 500)
miFrame.pack()

###################
#LABELS
###################

nombre_label= Label(miFrame, text="Elige archivo XML:")
nombre_label.grid(row=0, column=0, sticky="e")      #Sticky: al este

###################
#DATOS DE MÁRGENES
###################

w, h=A4     # w=595.27, h=841.88
x_margin=int(w*0.05)
y_margin=int(h*0.05)
y_startgrid=int(h*5/6)
x_padding=int((w-x_margin*2)/9)
y_padding=15
#Nº vueltas
max_vueltas=0

max_pilotos=0
tipo_sesion=''


###################
#BOTÓN
###################

# MÉTODO PARA GENERAR PDF A PARTIR DE LOS DATOS DEL XML
def generar_pdf(titulo_pdf, datos_carrera):
    print("aun en desarrollo")
    global max_vueltas
    num_pilotos=int(datos_carrera['Numero_Pilotos'])
    fecha_hora=datos_carrera['Fecha_Hora']
    max_vueltas=0
    c=canvas.Canvas(titulo_pdf, pagesize=A4)

    # TEXTOS CABECERA
    x_text_header=w/2
    y_text_header=h-32
    textHeader=c.beginText(x_text_header, y_text_header)
    textHeader.setFont("Times-Roman", 12)
    textHeader.textLines("Fecha y hora: "+fecha_hora+"\nCircuito: "+datos_carrera['Circuito']+"\nSesión de "+tipo_sesion)
    c.drawText(textHeader)
    #posiciones de prueba textos
    x_text_pilot=x_margin+3
    y_text_pilot=y_startgrid-y_padding+3
    

    textPiloto=c.beginText(x_text_pilot+3, y_text_pilot)
    textPiloto.setFont("Times-Bold", 10)
    textPiloto.textLine("Piloto")
    c.drawText(textPiloto)

    textCoche=c.beginText(x_text_pilot+3, y_text_pilot-y_padding)
    textCoche.setFont("Times-Bold", 10)
    textCoche.textLine("Coche")
    c.drawText(textCoche)

    # Pilotos (eje x)
    x_position=x_margin+3
    y_position=y_startgrid-y_padding+3
    c.line(x_position, y_position-3+y_padding, x_position+(num_pilotos+1)*x_padding, y_position-3+y_padding) # linea superior
    c.line(x_position, y_position-3, x_position+(num_pilotos+1)*x_padding, y_position-3)    # linea inferior
    for clave in datos_carrera.keys():
        if clave.startswith('Piloto'):
            if datos_carrera[clave]['Humano'] == 'si':
                x_position=x_position+x_padding
                textPiloto=c.beginText(x_position, y_position)
                textPiloto.textLine(datos_carrera[clave]['Nombre'][0:11])
                c.drawText(textPiloto)
                num_vueltas_actuales=int(datos_carrera[clave]['Num_Vueltas'])
                if max_vueltas < num_vueltas_actuales:
                    max_vueltas=num_vueltas_actuales
    # Coches (eje x)
    x_position=x_margin+3
    y_position=y_startgrid-2*y_padding+3
    c.line(x_position, y_position-3, x_position+(num_pilotos+1)*x_padding, y_position-3)    # linea inferior
    for clave in datos_carrera.keys():
        if clave.startswith('Piloto'):
            if datos_carrera[clave]['Humano'] == 'si':
                x_position=x_position+x_padding
                textCoche=c.beginText(x_position, y_position)
                textCoche.setFont("Times-Roman", 6)
                textCoche.textLine(datos_carrera[clave]['Coche'][0:16])
                c.drawText(textCoche)
    # Vueltas (eje y)
    x_position=x_margin+6
    y_position=y_startgrid-2*y_padding+3
    c.line(x_position+x_padding-10, y_startgrid, x_position+x_padding-10, y_startgrid-(max_vueltas+2)*y_padding)
    for n in range(1, max_vueltas+1):
        y_position=y_position-y_padding
        c.setLineWidth(0.5)
        c.line(x_position, y_position-3, x_position+(num_pilotos+1)*x_padding, y_position-3)    # linea inferior
        textNumVuelta=c.beginText(x_position, y_position)
        textNumVuelta.setFont("Times-Bold", 9)
        textNumVuelta.textLine("Vuelta "+str(n))
        c.drawText(textNumVuelta)
    # Texto Mejor Vuelta
    y_position=y_position-2*y_padding
    textMejorVuelta=c.beginText(x_position, y_position)
    textMejorVuelta.setFont("Times-Bold", 9)
    textMejorVuelta.textLine("Mejor")
    c.drawText(textMejorVuelta)
    # Texto Media Tiempo Vuelta
    if tipo_sesion=='Carrera':
        y_position=y_position-y_padding
        textTiempoMedio=c.beginText(x_position, y_position)
        textTiempoMedio.setFont("Times-Bold", 9)
        textTiempoMedio.textLine("Media")
        c.drawText(textTiempoMedio)
    # Tiempos de vuelta (ejes x, y)
    x_position=x_margin+3
    y_position=y_startgrid-3*y_padding+3
    for clave in datos_carrera.keys():
        if clave.startswith('Piloto'):
            if datos_carrera[clave]['Humano'] == 'si':
                x_position=x_position+x_padding
                y_position=y_startgrid-2*y_padding+3
                mejor_tiempo_piloto=datos_carrera[clave]['Mejor_tiempo_vuelta']
                if tipo_sesion=='Carrera':
                    tiempo_total_piloto=datos_carrera[clave]['Tiempo_total']
                for i in range(1, 100):
                    lap=datos_carrera[clave].get('Vuelta_'+str(i))
                    if lap == None:
                        break
                    else:
                        y_position=y_position-y_padding
                        textLap=c.beginText(x_position, y_position)
                        textLap.setFont("Times-Roman", 9)
                        tiempo=lap['Tiempo_vuelta']
                        if tiempo.startswith('-'):
                            textLap.textLine('-')
                            c.drawText(textLap)
                        else:
                            segundos=tiempo[0:tiempo.find(".")]  #segundos
                            minutos=int(int(segundos)/60)
                            segundos=int(int(segundos)-60*minutos)
                            tiempo_vuelta=str(minutos)+':'+str(segundos)+tiempo[tiempo.find("."):len(tiempo)-1]
                            if tiempo == mejor_tiempo_piloto:
                                textLap.setFont("Times-Bold", 10)
                                bestLapMMSS=tiempo_vuelta
                            textLap.textLine(tiempo_vuelta)
                            c.drawText(textLap)
                            # Poner sectores
                            for j in range(1, 100):
                                sec=datos_carrera[clave]['Vuelta_'+str(i)].get('Sector_'+str(i))
                                if sec == None:
                                    break
                                else:
                                    print('aqui va el sector: '+str(i))
                # Mejor Vuelta
                y_position=y_position-2*y_padding
                textBestLap=c.beginText(x_position, y_position)
                textBestLap.setFont('Times-Bold', 10)
                textBestLap.textLine(bestLapMMSS)
                c.drawText(textBestLap)
                # Tiempo de vuelta medio
                if tipo_sesion=='Carrera':
                    y_position=y_position-y_padding
                    tiempo_medio=str(round(float(tiempo_total_piloto)/num_vueltas_actuales, 3))
                    segundos=tiempo_medio[0:tiempo_medio.find(".")]  #segundos
                    minutos=int(int(segundos)/60)
                    segundos=int(int(segundos)-60*minutos)
                    tiempo_total=str(minutos)+':'+str(segundos)+tiempo_medio[tiempo_medio.find("."):len(tiempo_medio)]
                    textTotalTime=c.beginText(x_position, y_position)
                    textTotalTime.setFont('Times-Bold', 10)
                    textTotalTime.textLine(tiempo_total)
                    c.drawText(textTotalTime)
    c.drawImage("imagen_gtc.jpg", 50, h - 100, width=160, height=80)
    c.showPage()
    c.save()


# MÉTODO PARA EXTRAER LA INFORMACIÓN DEL XML
def extrae_info_xml(doc):
    #Datos carrera
    global tipo_sesion
    dic_carrera={}
    race_results=doc.find("RaceResults")    #Leemos todo el xml
    if race_results.find("Race") != None:
        conductores=race_results.find("Race").findall("Driver")     # Lista de pilotos
        tipo_sesion='Carrera'
    elif race_results.find("Practice1") != None:
        conductores=race_results.find("Practice1").findall("Driver")     # Lista de pilotos
        tipo_sesion='Práctica'
    elif race_results.find("Qualify") != None:
        conductores=race_results.find("Qualify").findall("Driver")     # Lista de pilotos
        tipo_sesion='Clasificación'
    else:
        conductores=[]
    pista=race_results.find("TrackCourse").text     # Nombre de la pista
    duracion=race_results.find("RaceTime").text     # Duración de la sesión
    fechaHora=race_results.find("TimeString").text
    dic_carrera['Circuito']=pista
    dic_carrera['Duracion']=duracion
    dic_carrera['Fecha_Hora']=fechaHora
    print("La carrera se ha disputado en %s, ha durado %s minutos, y han corrido los siguientes conductores:\n" % (dic_carrera.get('Circuito'), dic_carrera.get('Duracion')))
    num_pilotos=0       # Contador de pilotos
    for conductor in conductores:
        dic_piloto={}
        piloto_key="Piloto_"+str(num_pilotos)
        nombre_piloto=conductor.find("Name").text
        mejor_vuelta_piloto=conductor.find("BestLapTime").text
        coche_piloto=conductor.find("CarClass").text
        piloto_humano=conductor.find("isPlayer").text
        num_vueltas=conductor.find("Laps").text
        if piloto_humano == '1':
            humano='si'
            num_pilotos=num_pilotos+1
        else:
            humano='no'
        dic_piloto['Nombre']=nombre_piloto
        dic_piloto['Mejor_tiempo_vuelta']=mejor_vuelta_piloto
        dic_piloto['Coche']=coche_piloto
        dic_piloto['Num_Vueltas']=num_vueltas
        dic_piloto['Humano']=humano
        if tipo_sesion=='Carrera':
            tiempo_total_piloto=conductor.find("FinishTime").text
            dic_piloto['Tiempo_total']=tiempo_total_piloto
        vueltas=conductor.findall("Lap")
        for lap in vueltas:
            dic_vueltas={}
            numero_vuelta=lap.get("num")
            vuelta_key="Vuelta_"+str(numero_vuelta)
            sector1=lap.get("s1")
            sector2=lap.get("s2")
            sector3=lap.get("s3")
            tiempo_vuelta_seg=lap.text
            dic_vueltas['Sector_1']=sector1
            dic_vueltas['Sector_2']=sector2
            dic_vueltas['Sector_3']=sector3
            dic_vueltas['Tiempo_vuelta']=tiempo_vuelta_seg
            dic_piloto[vuelta_key]=dic_vueltas

        dic_carrera[piloto_key]=dic_piloto
        dic_carrera['Numero_Pilotos']=num_pilotos
    #print(dic_carrera['Piloto_1']['Vuelta_3']['Sector_2'])
    titulo_archivo=tipo_sesion+'_'+fechaHora.replace('/', '_').replace(':', '')+'_'+pista+'.pdf'
    generar_pdf(titulo_archivo, dic_carrera)

#MÉTODO SELECCIONAR ARCHIVO
def escogeArchivo():
    filename = askopenfilename()
    print(filename)
    
    if filename.endswith('xml'):
        print('\nEs un xml\n')
        doc = etree.parse(filename)
        extrae_info_xml(doc)
        #raiz=doc.getroot()
        #print(raiz.tag)
        #print(len(raiz))
        
    else:
        print('\nNo es un xml\n')


    
#BOTÓN
boton = Button(miFrame, text="Examinar", command=escogeArchivo, cursor="hand2")
boton.grid(row=0, column=2, sticky="e")

###################
#LANZAMOS GUI
###################
root.mainloop()


