# Product Requirements Document (PRD)
## Marie - Gestor de Conocimiento Personal con RAG

---

### 1. **Resumen Ejecutivo**

**Nombre del Proyecto:** Marie

**Historia y Sustento del Nombre:**
Marie Curie (1867-1934) fue una científica pionera que revolucionó la forma de entender y organizar el conocimiento científico. Su legado inspira este proyecto por múltiples razones:

- **Curiosidad Incansable:** Marie dedicó su vida a investigar lo desconocido, transformando información dispersa en descubrimientos revolucionarios
- **Metodología Rigurosa:** Desarrolló métodos sistemáticos para organizar y analizar datos complejos, estableciendo nuevos estándares de investigación
- **Conexión de Conceptos:** Fue la primera persona en ganar premios Nobel en dos disciplinas diferentes (Física y Química), demostrando su capacidad para conectar conocimientos interdisciplinarios
- **Persistencia ante la Complejidad:** Procesó toneladas de material para extraer elementos puros, similar a como nuestro sistema procesará grandes volúmenes de información para extraer conocimiento valioso
- **Innovación Tecnológica:** Sus descubrimientos abrieron nuevas fronteras científicas, al igual que nuestro proyecto busca abrir nuevas formas de gestionar el conocimiento

**Tagline:** "Tu compañera de descubrimiento en el universo del conocimiento"

**Visión:** Crear un agente inteligente que transforme la forma en que organizas y procesas información para el aprendizaje, eliminando la dispersión de datos y facilitando la construcción de conocimiento estructurado.

**Misión:** Empoderar el aprendizaje continuo y la innovación tecnológica mediante la creación de herramientas de IA que liberen a las personas de tareas repetitivas de organización de información, permitiéndoles enfocarse en lo verdaderamente importante: generar insights, conectar ideas y desarrollar soluciones que transformen empresas y mejoren la productividad humana.

**Alineación con Ikigai Personal:**
- **Pasión:** Combina tu amor por innovar con IA y enfrentar desafíos tecnológicos
- **Misión Personal:** Se alinea con tu objetivo de aumentar productividad liberando a las personas de trabajo repetitivo
- **Vocación:** Desarrolla una solución por la que otros estarían dispuestos a pagar dado su valor
- **Profesión:** Aplica tu experiencia en transformación digital y consultoría para crear productos escalables

**Problema a Resolver:** 
Actualmente, cuando quieres aprender sobre un tema específico, la información se encuentra dispersa en múltiples formatos y ubicaciones:
- Videos de YouTube con información valiosa en transcripciones y descripciones
- Links a recursos y referencias de expertos
- Anotaciones personales y recomendaciones
- Archivos PDF y documentos

Esta dispersión hace que sea difícil conectar conceptos, generar insights y tener una visión holística del conocimiento adquirido.

---

### 2. **Objetivos del Producto**

#### **Objetivos Primarios:**
- **Centralización:** Unificar toda la información de aprendizaje en una base de conocimiento local
- **Organización Automática:** Procesar y estructurar automáticamente la información ingresada
- **Visualización:** Crear mapas mentales y gráficos de conocimiento para entender conexiones
- **Síntesis:** Generar resúmenes inteligentes y árboles temáticos

#### **Objetivos Secundarios:**
- Servir como proyecto práctico para aprender sobre RAGs (Retrieval-Augmented Generation)
- Crear una alternativa más simple y eficiente que Notion para gestión de conocimiento personal

---

### 3. **Usuario Objetivo**

**Usuario Principal:** Tú mismo (desarrollador/estudiante)
- Persona que busca aprender sobre temas específicos de manera estructurada
- Necesita organizar grandes cantidades de información de múltiples fuentes
- Prefiere soluciones locales por privacidad y control de datos
- Interesado en entender cómo la IA procesa y conecta información

**Casos de Uso:**
- Investigación profunda sobre un tema técnico
- Preparación para proyectos o certificaciones
- Construcción de base de conocimiento personal
- Análisis de tendencias y conexiones entre conceptos

---

### 4. **Funcionalidades Principales**

#### **4.1 Ingesta de Información**
- **Videos de YouTube:** 
  - Extracción automática de transcripciones
  - Análisis de descripciones y comentarios
  - Identificación de links y recursos mencionados
  - **Procesamiento de listas de YouTube:** Análisis completo de playlists y canales
- **Documentos PDF:** Procesamiento y extracción de texto
- **Links de páginas web:** Scraping y análisis de contenido
- **Anotaciones manuales:** Interfaz para agregar notas personales

#### **4.2 Procesamiento y Organización**
- **Análisis semántico:** Identificación de temas y conceptos clave
  - **Temas y subtemas personalizados:** Opción para que el usuario defina temas específicos con descripciones detalladas
  - **Validación semántica por IA:** Sistema que valida coherencia de subtemas y sugiere mejoras
  - **Clasificación inteligente:** IA utiliza descripciones de temas para categorizar nueva información automáticamente
- **Categorización automática:** Agrupación por temas y subtemas
- **Extracción de entidades:** Personas, conceptos, tecnologías mencionadas
- **Detección de relaciones:** Conexiones entre diferentes piezas de información

#### **4.3 Visualización y Navegación**
- **Mapas mentales interactivos:** Representación visual de conceptos y relaciones
- **Gráficos de conocimiento:** Visualización de cómo la IA conecta la información utilizando **GraphRAG** para análisis avanzado de relaciones
- **Árboles temáticos:** Estructura jerárquica de temas y subtemas
- **Timeline de aprendizaje:** Progresión cronológica del conocimiento adquirido

#### **4.4 Síntesis y Generación**
- **Resúmenes inteligentes:** Por tema, fuente o período
- **Resúmenes comparativos:** Análisis de múltiples fuentes sobre el mismo tema
- **Generación de insights:** Conexiones no obvias entre conceptos
- **Recomendaciones:** Sugerencias de temas relacionados para explorar

#### **4.5 Evaluación y Aprendizaje Activo**
- **Sistema de evaluación por IA:** Generación automática de preguntas relacionadas con temas específicos
- **Evaluaciones adaptativas:** Preguntas que se ajustan al nivel de conocimiento demostrado
- **Seguimiento de progreso:** Métricas de comprensión y áreas de mejora
- **Retroalimentación inteligente:** Sugerencias personalizadas basadas en resultados de evaluaciones

---

### 5. **Arquitectura Técnica**

#### **5.1 Arquitectura de Modelos Duales**

**Modelo Ligero (Tareas Básicas):**
- **Opciones:** Llama-3.2-3B, Phi-3-mini, o Gemma-2B
- **Responsabilidades:**
  - Categorización automática de contenido
  - Extracción de entidades básicas
  - Resúmenes simples y directos
  - Validación de coherencia semántica
- **Ventajas:** Respuesta rápida (<2 segundos), bajo consumo de recursos

**Modelo Profundo (Análisis Complejo):**
- **Opciones:** Llama-3.1-8B, Mistral-7B, o Qwen2-7B
- **Responsabilidades:**
  - Análisis semántico profundo y detección de relaciones complejas
  - Generación de insights y conexiones no obvias
  - Creación de preguntas de evaluación sofisticadas
  - Procesamiento de GraphRAG para gráficos de conocimiento
- **Ventajas:** Mayor capacidad de razonamiento y comprensión contextual

#### **5.2 Opciones de Base de Datos Local:**

**Opción 1: Vector Database + SQLite + Graph Database (Recomendada)**
- **Chroma DB** para embeddings y búsqueda semántica
- **SQLite** para metadatos y relaciones estructuradas
- **NetworkX** o **Neo4j Embedded** para GraphRAG
- **Ventajas:** Máxima flexibilidad, rendimiento optimizado por tipo de consulta

**Opción 2: Graph Database**
- **Neo4j Community Edition** (local)
- **Ventajas:** Ideal para relaciones complejas y gráficos de conocimiento
- **Desventajas:** Mayor complejidad de setup

**Opción 3: Hybrid Approach**
- **PostgreSQL** con extensión **pgvector** para embeddings
- **Ventajas:** Robustez, escalabilidad, soporte completo SQL y vectorial

#### **5.3 Stack Tecnológico Sugerido:**
- **Backend:** Python (FastAPI)
- **Frontend:** React/Vue.js con D3.js para visualizaciones
- **Procesamiento de texto:** spaCy, NLTK, Transformers
- **Embeddings:** Sentence-Transformers (modelos locales)
- **GraphRAG:** Microsoft GraphRAG o implementación personalizada con NetworkX
- **Visualización:** D3.js, Cytoscape.js, React Flow
- **YouTube API:** yt-dlp para transcripciones y metadatos de listas
- **Modelos locales:** Ollama para gestión de modelos LLM

---

### 6. **Flujo de Usuario Principal**

1. **Ingesta:** Usuario proporciona URL de YouTube (individual o lista completa), PDF, o link web
2. **Procesamiento Dual:** 
   - Modelo ligero realiza categorización inicial y extracción básica
   - Modelo profundo analiza semánticamente y detecta relaciones complejas
3. **Organización Inteligente:** IA categoriza usando temas personalizados del usuario y valida coherencia
4. **Visualización GraphRAG:** Usuario explora mapas mentales y gráficos de conocimiento generados
5. **Evaluación Opcional:** Sistema genera preguntas para validar comprensión del tema
6. **Síntesis:** Usuario solicita resúmenes o insights específicos
7. **Iteración:** Sistema aprende de interacciones y evaluaciones para mejorar organización

---

### 7. **Criterios de Éxito**

#### **Métricas Funcionales:**
- Tiempo de procesamiento < 2 minutos por video de YouTube
- Tiempo de procesamiento < 10 minutos por lista de YouTube (50+ videos)
- Precisión en categorización > 85%
- Capacidad de procesar al menos 1000 documentos sin degradación
- **Precisión en evaluaciones > 90%** (preguntas relevantes y bien formuladas)

#### **Métricas de Experiencia:**
- Facilidad de uso superior a Notion para este caso específico
- Capacidad de encontrar información relevante en < 30 segundos
- Generación de insights útiles y no obvios
- **Tiempo de respuesta < 3 segundos para tareas básicas**
- **Tiempo de respuesta < 15 segundos para análisis profundo**

---

### 8. **Fases de Desarrollo**

#### **Fase 1: MVP (Minimum Viable Product)**
- Ingesta básica de URLs de YouTube (individuales y listas)
- Extracción de transcripciones y metadatos
- Implementación de arquitectura dual de modelos
- Almacenamiento en base de datos local (Chroma + SQLite)
- Búsqueda semántica básica

#### **Fase 2: Organización Inteligente**
- Sistema de temas y subtemas personalizados
- Categorización automática con validación semántica
- Generación de resúmenes con modelo dual
- Interfaz web básica

#### **Fase 3: Visualización y GraphRAG**
- Implementación de GraphRAG para análisis de relaciones
- Mapas mentales interactivos
- Gráficos de conocimiento dinámicos
- Árboles temáticos navegables

#### **Fase 4: Evaluación y Síntesis Avanzada**
- Sistema de evaluación por IA con preguntas adaptativas
- Generación de insights complejos
- Resúmenes comparativos
- Recomendaciones inteligentes basadas en progreso

---

### 9. **Riesgos y Mitigaciones**

#### **Riesgos Técnicos:**
- **Calidad de transcripciones:** Usar múltiples fuentes y validación
- **Rendimiento con grandes volúmenes:** Implementar indexación eficiente
- **Precisión de categorización:** Entrenamiento iterativo y feedback del usuario

#### **Riesgos de Producto:**
- **Complejidad de uso:** Priorizar UX simple e intuitiva
- **Sobrecarga de información:** Implementar filtros y vistas personalizables

---

### 10. **Próximos Pasos**

1. **Seleccionar stack tecnológico definitivo**
2. **Crear arquitectura detallada**
3. **Desarrollar MVP con funcionalidad básica**
4. **Iterar basado en uso real**

---

### 11. **Inspiración y Referencias**

- **Marie Curie:** Pionera en investigación sistemática y organización del conocimiento científico
- **Fabric:** Herramienta existente para análisis de videos YouTube (`C:\Users\User\Documents\GitHub\fabric`)
- **Obsidian:** Para conceptos de gráficos de conocimiento
- **Roam Research:** Para conexiones bidireccionales
- **Notion:** Como referencia de lo que NO queremos (complejidad excesiva)

---

*Documento creado: 27 de agosto, 2025*
*Versión: 1.0*
