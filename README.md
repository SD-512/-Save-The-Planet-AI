# 🌍 Save The Planet AI

Aplicación educativa interactiva que combina IA, gamificación y conciencia ambiental.

## Tecnologías

- 🐍 Python
- 🔥 Flask
- 🗄 SQLite
- 🎤 SpeechRecognition (próximamente)
- HTML5
- CSS3

## Funciones

- ✔ Juego ambiental con preguntas de opción múltiple
- ✔ Sistema de vidas y tiempo límite por pregunta (sin JavaScript)
- ✔ Salud del planeta que baja con cada respuesta incorrecta
- ✔ EcoGPT: asistente que responde por palabra clave
- ✔ Quiz educativo estilo Kahoot
- ✔ Resultados personalizados (estado del planeta, impacto positivo)
- ✔ Resultados guardados en SQLite

## Instalación

```
pip install -r requirements.txt
python app.py
```

Luego abrí `http://127.0.0.1:5000` en el navegador.

## Estructura

```
SaveThePlanetAI
│   app.py
│   README.md
│   requirements.txt
│
├── static
│   ├── css/style.css
│   ├── images/          (agregar forest.jpg, before.jpg, after.jpg, planet.jpg)
│   ├── sounds/
│   └── videos/
├── templates
│   ├── index.html
│   ├── game.html
│   ├── quiz.html
│   ├── chatbot.html
│   ├── about.html
│   ├── before_after.html
│   └── result.html
├── data
│   ├── questions.json
│   ├── facts.json
│   └── tips.json
└── database
    └── database.db      (se crea solo al iniciar la app)
```

## Autora

Sara Drago Ponzoni · Hackathon 2026