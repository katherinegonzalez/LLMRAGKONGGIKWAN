# Asistente IA Kong Gi Kwan 🥋

Asistente IA Kong Gi Kwan es una aplicación en la cual se ha mejorado un modelo de LLM con RAG para que cuente con información específica de Taekwondo y la Academia Kong Gi Kwan.

Este proyecto ha sido implementado como trabajo de grado para el examen de ascenso de grado a Cinturón Negro Segundo Dan en la Aacademia de Taekwondo Kong Gi Kwan. 

Si deseas ver el documento académico del proyecto haz cick en el siguiente link:
[Artículo: Desarrollo de un Prototipo de Asistente de IA para la Academia de Taekwondo Kong Gi Kwan: Mejorando la Precisión de los LLMs con RAG](https://drive.google.com/file/d/1QmR0giS0yq8cP4-9AEWY3kGz_iK9tyag/view?usp=sharing)

Dentro de este repositorio se encuentran la aplicación Web implementada con Python con la librería Streamlite.

# Enlace a la aplicación 💻 

[Enlace a la aplicación Asistente IA Kong Gi Kwan](https://asistenteiakonggikwan.streamlit.app/ )

# Estructura de Carpetas 📂

Las carpetas se estructuran de la siguiente manera:
- **/**: En la raíz del proyecto se encuentra el código de streamline de la Aplicación.
- **/scripts**: Contiene un archivo para cargar los documentos en formato pdf, y un archivo que se encarga de crear y almacenar el índice vectorial, así como el vector de base de datos.
- **/utils**: Contiene un archivo de constantes donde se encuentran las rutas para almacenar los datos.
- **/documents**: Aquí se encuentran los documentos a los que va a acceder el modelo.

## Librerias 📋

* [LangChain](https://www.langchain.com/): Esta librería permite combinar modelos de lenguaje con datos externos como documentos, bases de datos o APIs.
* [LangChain Community](https://pypi.org/project/langchain-community/): Esta librería proporciona conectores y herramientas creadas por la comunidad para ampliar las funcionalidades de LangChain.
* [Langchain OpenAI](https://python.langchain.com/docs/integrations/providers/openai/): Esta librería se usó para integrar fácilmente el modelo de OpenAI dentro del flujo de trabajo de LangChain.
* [Streamlite](https://streamlit.io/): Esta librería fue usada para la implementación de la interfaz de la aplicación.

## Instalación 💻 

Para instalar y configurar el proyecto en tu ambiente local, sigue los siguientes pasos:

1. Clona el repositorio: `git clone https://github.com/katherinegonzalez/LLMRAGKONGGIKWAN`
2. Crea y Activa el entorno de python: 
    * `python -m venv env`
    * `source env/bin/activate`

3. Instala las siguientes dependencias: 

    * `pip install langchain`
    * `pip install langchain-community`
    * `pip install langchain-openai`
    * `pip install streamlit`

    O simplemente:

    * `pip install -r requirements.txt`

##  Ejecución del Proyecto 💻 

Para ejecutar el proyecto en tu ambiente local:

1. Crea una Key en la página de OpenIA
2. Dentro de la carpeta scriots crea un archivo llamado secret.py y pon tu llave ahí: OPEN_KEY
3. Ve al terminal, en la raíz del proyecto.
3. Ejecuta el comando `streamlit run main.py`, de esta manera se ejecuta el servidor en nuestro ambiente local, generalmente en el puerto `8050` - `http://127.0.0.1:8050/`

## Github repository 📦

[Github Asistente IA Kong Gi Kwan](https://github.com/katherinegonzalez/LLMRAGKONGGIKWAN)

## Autora 😊

Katherine Xiomar González Santacruz  
