# xml-to-pdf_RaceData

El archivo gui.py contiene un programa que pide un archivo XML y genera un PDF con la hoja de tiempos de la sesión.

Para generar el ejecutable, hay que:
  1. Eliminar en primer lugar las carpetas dist, build, __pycache__, y el archivo gui.spec.
  2. Abrir la consola en la carpeta donde está el archivo gui.py
  3. Ejectuar la instrucción que está en el archivo "generar_ejecutable.txt"
  4. Copiar los archivos de imagen (imagen_gtc.jpg y gtc.ico) a la carpeta "dist".
  5. Ejecutar gui.exe en la carpeta dist.

Una vez conseguido el ejecutable, se ejecuta y aparece una interfaz en la que se escogen un par de parámetros opcionalmente.
Se pulsa "Examinar", se escoge el XML de la carrera, y el programa genera el PDF correspondiente.

El repositorio incluye dos XML de ejemplo.
