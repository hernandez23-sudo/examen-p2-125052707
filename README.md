# Examen P2 — 125052707
**Pregunta 6/7:** Top 10 productos por ingreso total en todo el año.

## Reproducir
1. `python3 generar_dataset.py 125052707`
2. `cp .env.example .env`
3. `docker compose up --build -d`
4. Ejecutar el job (comando en README sección "Job")
5. `docker compose run --rm cargador`
6. API: http://localhost:8000/docs

## Job
```bash
docker exec -it hadoop bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /data/input/ventas_125052707.csv \
  -output /data/output/resultado \
  -mapper /mapreduce/mapper.py -reducer /mapreduce/reducer.py \
  -file /mapreduce/mapper.py -file /mapreduce/reducer.py

## Tiempos
- MapReduce: 13.28 s
- Secuencial: 12.536s

## Comparativa
En este escenario, el script secuencial (Python puro) y el MapReduce tuvieron tiempos muy similares, e incluso el secuencial pudo ser un poco más rápido. Esto se debe a que MapReduce tiene un *overhead* (costo extra) por el arranque de la máquina virtual de Java (JVM), la lectura de los archivos de configuración, la división de tareas y la fase de *Shuffle and Sort* (ordenamiento). Para un único archivo de 400 MB corriendo en una sola máquina (pseudo-distribuido), un script secuencial aprovecha mejor la memoria caché del sistema operativo. Sin embargo, MapReduce demuestra su verdadero potencial y se vuelve estrictamente necesario cuando el volumen de datos es de Terabytes o Petabytes, ya que permite paralelizar el trabajo en cientos de servidores, algo que un script secuencial jamás podría hacer.
## Evidencias
Todas las capturas se encuentran en la carpeta `evidencias/`:
- `hadoop_version.png`: Verificación de la instalación.
- `ssh_localhost.png`: Acceso sin contraseña.
- `mapreduce_output.png`: Resultado del Top 10 de productos.
- `api_get.png`: Respuesta de la API.
- `persistencia.png`: Demostración de que los datos sobreviven al `docker compose down` y `up`.