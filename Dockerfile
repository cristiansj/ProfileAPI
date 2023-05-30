# Utiliza una imagen base de Python (puedes elegir la versión que prefieras)
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios para ejecutar tu aplicación
COPY . .

# Instala las dependencias
#RUN pip install --no-cache-dir -r requirements.txt

# Agrega /usr/local/bin a la variable de entorno $PATH
ENV PATH="/usr/local/bin:${PATH}"

# Ejecuta tu aplicación con Uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
