# Sistema de Relaciones Bidireccionales y Búsqueda en Marie

---

## **1. Arquitectura de Relaciones Bidireccionales**

### **Estructura de Datos**
```sql
-- Tabla principal de conceptos/notas
Concepts:
- id (UUID)
- title (string)
- content (text)
- type (enum: fugaz, bibliografica, permanente, moc)
- embedding (vector)
- created_at, updated_at
- source_id (referencia a fuente original)
- position_metadata (timestamp, página, etc.)

-- Tabla de tags
Tags:
- id (UUID)
- name (string) -- ej: "algoritmo", "matematicas", "python"
- category (enum: domain, method, technology, difficulty, source_type)
- color (string) -- para visualización
- auto_generated (boolean) -- si fue creado por IA o usuario
- usage_count (integer) -- frecuencia de uso

-- Tabla de relación conceptos-tags (many-to-many)
ConceptTags:
- concept_id (UUID)
- tag_id (UUID)
- confidence (float 0-1) -- confianza si fue asignado por IA
- assigned_by (enum: ai, user, system)

-- Tabla de relaciones bidireccionales
Relationships:
- id (UUID)
- concept_a_id (UUID)
- concept_b_id (UUID)
- relationship_type (enum: contradice, complementa, extiende, ejemplifica, causa, efecto)
- strength (float 0-1) -- confianza de la IA en la relación
- explanation (text) -- por qué están conectados
- created_by (enum: ai, user, system)
- validated_by_user (boolean)

-- Tabla de fuentes/recursos
Sources:
- id (UUID)
- title (string)
- url (text, nullable) -- para links y videos
- file_path (text, nullable) -- para archivos locales
- source_type (enum: youtube_video, youtube_playlist, pdf, web_page, book, article, podcast, course, manual_note)
- author (string, nullable)
- publication_date (date, nullable)
- duration_minutes (integer, nullable) -- para videos/podcasts
- page_count (integer, nullable) -- para documentos
- language (string, default: 'es')
- quality_score (float 0-1) -- evaluación de calidad del contenido
- processing_status (enum: pending, processing, completed, failed)
- metadata_json (text) -- metadatos específicos por tipo
- created_at, updated_at
- last_accessed_at (timestamp)

-- Tabla de temas/MOCs
Topics:
- id (UUID)
- name (string)
- description (text)
- parent_topic_id (UUID, nullable)
- user_defined (boolean)
- embedding (vector)
- color_code (string)
```

### **Tipos de Relaciones**
1. **Semánticas:** Conceptos relacionados por significado
2. **Causales:** Relaciones causa-efecto
3. **Jerárquicas:** Conceptos generales → específicos
4. **Temporales:** Secuencia cronológica de ideas
5. **Contradictorias:** Ideas que se oponen
6. **Complementarias:** Ideas que se refuerzan mutuamente
7. **Por Tags:** Conceptos que comparten tags similares (relación implícita)

### **Categorías de Tags**
1. **Domain:** Área de conocimiento (ej: "machine-learning", "matematicas", "fisica")
2. **Method:** Metodología o técnica (ej: "algoritmo", "teoria", "practica")
3. **Technology:** Herramientas específicas (ej: "python", "tensorflow", "sql")
4. **Difficulty:** Nivel de complejidad (ej: "basico", "intermedio", "avanzado")
5. **Source_type:** Tipo de fuente (ej: "video", "paper", "libro", "curso")

### **Tipos de Fuentes/Recursos**
1. **youtube_video:** Videos individuales de YouTube
2. **youtube_playlist:** Listas completas de YouTube
3. **pdf:** Documentos PDF (libros, papers, manuales)
4. **web_page:** Páginas web y artículos online
5. **book:** Libros físicos o digitales
6. **article:** Artículos académicos o de blog
7. **podcast:** Episodios de podcast
8. **course:** Cursos online completos
9. **manual_note:** Notas creadas manualmente por el usuario

### **Algoritmos de Asignación de Tags**
```python
def auto_assign_tags(concept):
    # 1. Tags por dominio (usando embeddings)
    domain_tags = classify_domain(concept.content)
    
    # 2. Tags por tecnología (NER + patrones)
    tech_tags = extract_technologies(concept.content)
    
    # 3. Tags por dificultad (análisis de complejidad)
    difficulty_tag = assess_difficulty(concept.content, concept.source)
    
    # 4. Tags por método (análisis sintáctico)
    method_tags = identify_methods(concept.content)
    
    return {
        'domain': domain_tags,
        'technology': tech_tags, 
        'difficulty': [difficulty_tag],
        'method': method_tags
    }
```

---

## **2. Motor de Búsqueda Híbrido**

### **Búsqueda Semántica (Vector)**
```python
def semantic_search(query, top_k=10):
    query_embedding = embed_model.encode(query)
    
    # Búsqueda en Chroma DB
    results = chroma_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['documents', 'metadatas', 'distances']
    )
    
    return results
```

### **Búsqueda por Palabras Clave (BM25)**
```python
def keyword_search(query, top_k=10):
    # Búsqueda tradicional en SQLite con FTS5
    cursor.execute("""
        SELECT * FROM concepts_fts 
        WHERE concepts_fts MATCH ? 
        ORDER BY bm25(concepts_fts) 
        LIMIT ?
    """, (query, top_k))
    
    return cursor.fetchall()
```

### **Búsqueda por Tags**
```python
def tag_search(tags, operator="AND"):
    if operator == "AND":
        # Conceptos que tienen TODOS los tags
        query = """
            SELECT c.* FROM concepts c
            JOIN concept_tags ct ON c.id = ct.concept_id
            JOIN tags t ON ct.tag_id = t.id
            WHERE t.name IN ({})
            GROUP BY c.id
            HAVING COUNT(DISTINCT t.id) = ?
        """.format(','.join(['?'] * len(tags)))
        
    else:  # OR
        # Conceptos que tienen AL MENOS uno de los tags
        query = """
            SELECT DISTINCT c.* FROM concepts c
            JOIN concept_tags ct ON c.id = ct.concept_id
            JOIN tags t ON ct.tag_id = t.id
            WHERE t.name IN ({})
        """.format(','.join(['?'] * len(tags)))
    
    return execute_query(query, tags + [len(tags)] if operator == "AND" else tags)

### **Búsqueda por Tipo de Fuente**
```python
def source_type_search(source_types, include_concepts=True):
    if include_concepts:
        # Buscar conceptos que provienen de tipos específicos de fuentes
        query = """
            SELECT c.*, s.source_type, s.title as source_title, s.url, s.author
            FROM concepts c
            JOIN sources s ON c.source_id = s.id
            WHERE s.source_type IN ({})
            ORDER BY s.quality_score DESC, c.created_at DESC
        """.format(','.join(['?'] * len(source_types)))
    else:
        # Buscar solo las fuentes
        query = """
            SELECT * FROM sources 
            WHERE source_type IN ({})
            ORDER BY quality_score DESC, created_at DESC
        """.format(','.join(['?'] * len(source_types)))
    
    return execute_query(query, source_types)

def advanced_source_filter(filters):
    """
    Filtros avanzados para fuentes:
    - source_types: lista de tipos
    - min_quality: score mínimo de calidad
    - date_range: rango de fechas
    - author: autor específico
    - min_duration/max_duration: para videos/podcasts
    - language: idioma
    """
    conditions = []
    params = []
    
    if filters.get('source_types'):
        placeholders = ','.join(['?'] * len(filters['source_types']))
        conditions.append(f"source_type IN ({placeholders})")
        params.extend(filters['source_types'])
    
    if filters.get('min_quality'):
        conditions.append("quality_score >= ?")
        params.append(filters['min_quality'])
    
    if filters.get('author'):
        conditions.append("author LIKE ?")
        params.append(f"%{filters['author']}%")
    
    if filters.get('language'):
        conditions.append("language = ?")
        params.append(filters['language'])
    
    if filters.get('min_duration'):
        conditions.append("duration_minutes >= ?")
        params.append(filters['min_duration'])
    
    if filters.get('max_duration'):
        conditions.append("duration_minutes <= ?")
        params.append(filters['max_duration'])
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT s.*, COUNT(c.id) as concept_count
        FROM sources s
        LEFT JOIN concepts c ON s.id = c.source_id
        WHERE {where_clause}
        GROUP BY s.id
        ORDER BY s.quality_score DESC, concept_count DESC
    """
    
    return execute_query(query, params)

def tag_similarity_search(concept_id, min_shared_tags=2):
    # Encuentra conceptos que comparten tags con el concepto dado
    query = """
        SELECT c2.*, COUNT(shared_tags.tag_id) as shared_count
        FROM concepts c2
        JOIN concept_tags ct2 ON c2.id = ct2.concept_id
        JOIN (
            SELECT ct1.tag_id FROM concept_tags ct1 
            WHERE ct1.concept_id = ?
        ) shared_tags ON ct2.tag_id = shared_tags.tag_id
        WHERE c2.id != ?
        GROUP BY c2.id
        HAVING shared_count >= ?
        ORDER BY shared_count DESC
    """
    return execute_query(query, [concept_id, concept_id, min_shared_tags])
```

### **Búsqueda Híbrida con Re-ranking + Tags**
```python
def hybrid_search_with_tags(query, tags=None, alpha=0.7, beta=0.2):
    semantic_results = semantic_search(query, top_k=20)
    keyword_results = keyword_search(query, top_k=20)
    
    # Si hay tags, incluir búsqueda por tags
    tag_results = []
    if tags:
        tag_results = tag_search(tags, operator="OR")
    
    # Combinar y re-rankear resultados (semántico + keywords + tags)
    combined_results = combine_and_rerank_with_tags(
        semantic_results, 
        keyword_results,
        tag_results,
        alpha=alpha,  # peso semántico
        beta=beta     # peso tags
    )
    
    return combined_results[:10]
```

---

## **3. Presentación de Temas para Estudio**

### **Vista Principal: Dashboard de Tema**
```
┌─────────────────────────────────────────────────────────┐
│ 🧠 MACHINE LEARNING                                     │
├─────────────────────────────────────────────────────────┤
│ 📊 Progreso: ████████░░ 80% completado                 │
│ 📚 23 fuentes • 156 conceptos • 89 conexiones          │
│ ⏱️ Última actualización: hace 2 días                   │
├─────────────────────────────────────────────────────────┤
│ 🎯 CONCEPTOS CLAVE                                      │
│ • Redes Neuronales (15 conexiones) ⭐⭐⭐⭐⭐           │
│ • Gradient Descent (12 conexiones) ⭐⭐⭐⭐            │
│ • Overfitting (8 conexiones) ⭐⭐⭐                     │
│                                                         │
│ 🔗 TEMAS RELACIONADOS                                   │
│ • Deep Learning → 23 conexiones                        │
│ • Statistics → 15 conexiones                           │
│ • Python Programming → 12 conexiones                   │
│                                                         │
│ 📈 RUTAS DE APRENDIZAJE SUGERIDAS                      │
│ 1. Fundamentos → Algoritmos → Implementación           │
│ 2. Teoría → Práctica → Optimización                    │
└─────────────────────────────────────────────────────────┘
```

### **Vista de Exploración: Mapa Mental Interactivo**
```
        [Statistics] ←──── [Machine Learning] ────→ [Deep Learning]
             │                     │                        │
             │                     ↓                        │
        [Probability]      [Gradient Descent]        [Neural Networks]
             │                     │                        │
             ↓                     ↓                        ↓
      [Bayes Theorem]      [Backpropagation]         [CNN] [RNN] [LSTM]
```

### **Vista de Estudio: Sesión Estructurada**
```
┌─────────────────────────────────────────────────────────┐
│ 📖 SESIÓN DE ESTUDIO: Redes Neuronales                 │
├─────────────────────────────────────────────────────────┤
│ 🎯 OBJETIVO: Comprender arquitecturas básicas          │
│ ⏱️ TIEMPO ESTIMADO: 45 minutos                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 📝 CONCEPTOS A REVISAR (5/8)                           │
│ ✅ Perceptrón                                           │
│ ✅ Función de Activación                                │
│ ✅ Weights y Bias                                       │
│ ✅ Forward Propagation                                  │
│ ✅ Loss Function                                        │
│ ⏳ Backpropagation ← ACTUAL                             │
│ ⭕ Gradient Descent                                      │
│ ⭕ Learning Rate                                         │
│                                                         │
│ 💡 INSIGHT GENERADO:                                    │
│ "Backpropagation es esencialmente la aplicación       │
│ de la regla de la cadena para calcular gradientes     │
│ en redes multicapa"                                    │
│                                                         │
│ 🔗 CONEXIONES DETECTADAS:                              │
│ • Se relaciona con Cálculo → Derivadas                │
│ • Conecta con Optimización → Gradient Descent         │
│ • Fundamental para Deep Learning                       │
│                                                         │
│ 📚 FUENTES:                                             │
│ • Video: "Neural Networks Explained" (min 12:30)      │
│ • Paper: "Learning representations..." (p. 45)        │
│ • Curso: "Deep Learning Specialization" (Week 2)      │
└─────────────────────────────────────────────────────────┘
```

---

## **4. Algoritmos de Detección de Relaciones**

### **Detección Semántica con Embeddings**
```python
def detect_semantic_relationships(concept_a, concept_b, threshold=0.75):
    embedding_a = get_concept_embedding(concept_a)
    embedding_b = get_concept_embedding(concept_b)
    
    similarity = cosine_similarity(embedding_a, embedding_b)
    
    if similarity > threshold:
        # Usar modelo profundo para explicar la relación
        explanation = deep_model.generate_explanation(
            concept_a, concept_b, similarity
        )
        
        return {
            'strength': similarity,
            'type': classify_relationship_type(concept_a, concept_b),
            'explanation': explanation
        }
    
    return None
```

### **Detección de Relaciones Causales**
```python
def detect_causal_relationships(text_chunk):
    # Patrones lingüísticos para causalidad
    causal_patterns = [
        r"(.+) causa (.+)",
        r"(.+) resulta en (.+)",
        r"debido a (.+), (.+)",
        r"(.+) lleva a (.+)"
    ]
    
    relationships = []
    for pattern in causal_patterns:
        matches = re.findall(pattern, text_chunk, re.IGNORECASE)
        for cause, effect in matches:
            relationships.append({
                'type': 'causal',
                'cause': cause.strip(),
                'effect': effect.strip(),
                'strength': 0.8
            })
    
    return relationships
```

### **GraphRAG para Relaciones Complejas**
```python
def build_knowledge_graph():
    # Construir grafo con NetworkX
    G = nx.DiGraph()
    
    # Agregar nodos (conceptos)
    for concept in get_all_concepts():
        G.add_node(concept.id, 
                  title=concept.title,
                  type=concept.type,
                  embedding=concept.embedding)
    
    # Agregar aristas (relaciones)
    for rel in get_all_relationships():
        G.add_edge(rel.concept_a_id, rel.concept_b_id,
                  type=rel.relationship_type,
                  strength=rel.strength,
                  explanation=rel.explanation)
    
    return G

def find_learning_paths(start_concept, end_concept, max_depth=5):
    G = build_knowledge_graph()
    
    # Encontrar todos los caminos posibles
    paths = list(nx.all_simple_paths(G, start_concept, end_concept, 
                                   cutoff=max_depth))
    
    # Rankear por fuerza de conexiones
    ranked_paths = rank_paths_by_strength(G, paths)
    
    return ranked_paths[:3]  # Top 3 rutas
```

---

## **5. Interfaz de Usuario para Estudio**

### **Barra de Búsqueda Inteligente**
```
┌─────────────────────────────────────────────────────────┐
│ 🔍 ¿Qué quieres aprender hoy?                          │
│ [neural networks backpropagation        ] 🎯 Buscar    │
├─────────────────────────────────────────────────────────┤
│ 💡 SUGERENCIAS INTELIGENTES:                            │
│ • "Cómo funciona backpropagation en CNN"               │
│ • "Diferencia entre SGD y Adam optimizer"              │
│ • "Implementar red neuronal desde cero"                │
│                                                         │
│ 🎯 BÚSQUEDAS RECIENTES:                                 │
│ • Gradient descent optimization                         │
│ • Overfitting prevention techniques                     │
└─────────────────────────────────────────────────────────┘
```

### **Panel de Navegación Contextual**
```
┌─────────────────────────────────────────────────────────┐
│ 🧭 NAVEGACIÓN CONTEXTUAL                                │
├─────────────────────────────────────────────────────────┤
│ 📍 ESTÁS AQUÍ: Backpropagation                         │
│                                                         │
│ ⬆️ CONCEPTOS PADRE:                                     │
│ • Neural Networks                                       │
│ • Supervised Learning                                   │
│                                                         │
│ ⬇️ CONCEPTOS HIJO:                                      │
│ • Chain Rule Application                                │
│ • Gradient Calculation                                  │
│                                                         │
│ ↔️ CONCEPTOS HERMANOS:                                  │
│ • Forward Propagation                                   │
│ • Loss Functions                                        │
│                                                         │
│ 🔗 CONEXIONES FUERTES:                                  │
│ • Calculus (95% relevancia)                            │
│ • Optimization (87% relevancia)                        │
│ • Deep Learning (92% relevancia)                       │
└─────────────────────────────────────────────────────────┘
```

### **Modo de Estudio Adaptativo**
```python
class AdaptiveStudySession:
    def __init__(self, topic, user_level="intermediate"):
        self.topic = topic
        self.user_level = user_level
        self.concepts_to_review = []
        self.current_concept = None
        self.progress = {}
    
    def generate_study_plan(self):
        # Analizar conceptos del tema
        all_concepts = get_topic_concepts(self.topic)
        
        # Ordenar por dependencias y dificultad
        ordered_concepts = topological_sort_by_difficulty(
            all_concepts, self.user_level
        )
        
        # Crear sesiones de 30-45 minutos
        study_sessions = chunk_concepts_by_time(
            ordered_concepts, target_time=40
        )
        
        return study_sessions
    
    def adapt_to_performance(self, concept_id, understanding_score):
        if understanding_score < 0.7:
            # Agregar conceptos prerequisitos
            prerequisites = find_prerequisites(concept_id)
            self.concepts_to_review.extend(prerequisites)
        
        elif understanding_score > 0.9:
            # Acelerar y agregar conceptos avanzados
            advanced_concepts = find_advanced_concepts(concept_id)
            self.concepts_to_review.extend(advanced_concepts[:2])
```

---

## **6. Sistema de Evaluación Integrado**

### **Preguntas Contextuales**
```python
def generate_contextual_questions(concept, related_concepts):
    prompt = f"""
    Basándote en el concepto '{concept.title}' y sus relaciones con 
    {[r.title for r in related_concepts]}, genera 3 preguntas que evalúen:
    
    1. Comprensión básica del concepto
    2. Capacidad de conectar con conceptos relacionados  
    3. Aplicación práctica o ejemplo concreto
    
    Concepto: {concept.content}
    Relaciones: {get_relationship_explanations(concept, related_concepts)}
    """
    
    questions = deep_model.generate(prompt)
    return parse_questions(questions)
```

### **Retroalimentación Inteligente**
```python
def provide_intelligent_feedback(user_answer, correct_concept, related_concepts):
    feedback = {
        'accuracy': calculate_semantic_similarity(user_answer, correct_concept),
        'missing_connections': find_missing_connections(user_answer, related_concepts),
        'suggestions': generate_study_suggestions(user_answer, correct_concept),
        'next_concepts': recommend_next_concepts(correct_concept, user_performance)
    }
    
    return feedback
```

---

## **7. Flujo de Estudio Completo**

### **Escenario: Usuario quiere estudiar "Machine Learning"**

1. **Búsqueda Inicial:**
   ```
   Usuario: "quiero aprender machine learning"
   Marie: Encuentra tema "Machine Learning" con 156 conceptos
   ```

2. **Análisis de Conocimiento Previo:**
   ```
   Marie: "Veo que ya tienes conocimientos de Python y Estadística.
          ¿Quieres empezar con fundamentos teóricos o implementación práctica?"
   ```

3. **Generación de Plan de Estudio:**
   ```
   Sesión 1 (40 min): Fundamentos
   - Supervised vs Unsupervised Learning
   - Training vs Test Data
   - Bias-Variance Tradeoff
   
   Sesión 2 (45 min): Algoritmos Básicos
   - Linear Regression
   - Logistic Regression  
   - Decision Trees
   ```

4. **Estudio Interactivo:**
   ```
   Marie presenta concepto → Usuario lee/ve fuentes → 
   Marie genera preguntas → Usuario responde → 
   Marie evalúa y sugiere conexiones → Siguiente concepto
   ```

5. **Visualización de Progreso:**
   ```
   Mapa mental se actualiza en tiempo real mostrando:
   - Conceptos dominados (verde)
   - Conceptos en progreso (amarillo)  
   - Conceptos pendientes (gris)
   - Conexiones descubiertas (líneas punteadas → sólidas)
   ```

6. **Adaptación Continua:**
   ```
   Marie detecta que usuario domina rápido conceptos básicos
   → Acelera el ritmo y sugiere temas avanzados
   → Actualiza plan de estudio dinámicamente
   ```

---

*Sistema diseñado para maximizar retención y comprensión profunda*  
*Basado en principios Zettelkasten y ciencia cognitiva*

---

## **13. Sistema de Mapa Mental Interactivo**

### **13.1 Concepto: Red Neuronal de Conocimiento**

Inspirado en las conexiones neuronales del cerebro, donde cada tema es un "nodo" con diferentes estados visuales basados en progreso, evaluaciones completadas y próximos temas recomendados.

### **13.2 Esquema de Base de Datos Extendido**

#### Evaluaciones y Rutas de Aprendizaje
```sql
CREATE TABLE topic_assessments (
    id INTEGER PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    laboratory_id INTEGER REFERENCES laboratories(id),
    assessment_type ENUM('quiz', 'exam', 'practical', 'self_evaluation'),
    questions_total INTEGER,
    questions_correct INTEGER,
    score_percentage FLOAT,
    time_taken_minutes INTEGER,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced'),
    assessment_date TIMESTAMP,
    notes TEXT
);

CREATE TABLE learning_paths (
    id INTEGER PRIMARY KEY,
    laboratory_id INTEGER REFERENCES laboratories(id),
    from_topic_id INTEGER REFERENCES topics(id),
    to_topic_id INTEGER REFERENCES topics(id),
    path_type ENUM('prerequisite', 'recommended_next', 'related', 'advanced'),
    strength_score FLOAT,              -- 0-1, qué tan fuerte es la conexión
    learning_difficulty FLOAT,        -- 0-1, qué tan difícil es la transición
    estimated_time_hours INTEGER,
    created_by ENUM('ai', 'user', 'system'),
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE mind_map_nodes (
    id INTEGER PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    laboratory_id INTEGER REFERENCES laboratories(id),
    x_position FLOAT,                  -- Posición X en el mapa
    y_position FLOAT,                  -- Posición Y en el mapa
    node_size INTEGER DEFAULT 50,     -- Tamaño basado en importancia
    color_code VARCHAR(7),             -- Color basado en progreso
    is_visible BOOLEAN DEFAULT true,
    last_updated TIMESTAMP
);
```

### **13.3 Interfaz del Mapa Mental**

#### Visualización Principal
```
🧠 MAPA MENTAL - LABORATORIO IA

┌─────────────────────────────────────────────────────────────────────┐
│                    🎯 LEYENDA                                       │
│ 🟢 Dominado (>80%)  🟡 En Progreso (40-80%)  🔴 Pendiente (<40%)   │
│ ⭐ Evaluado  🔗 Conexión Fuerte  ➡️ Próximo Recomendado            │
└─────────────────────────────────────────────────────────────────────┘

                    🟢 Python Basics ⭐
                         │
                    🔗───┼───🔗
                    │         │
            🟡 Data Structures    🟢 Functions ⭐
                    │                   │
                    🔗                  🔗
                    │                   │
            🟡 Algorithms ⭐      🟡 OOP Concepts
                    │                   │
                    └─────🔗─────┬─────🔗
                                 │
                        🔴 Machine Learning ➡️
                              │
                        ┌─────🔗─────┐
                        │             │
                🔴 Supervised      🔴 Unsupervised ➡️
                Learning ➡️         Learning
```

#### Panel de Detalles del Nodo
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 NODO SELECCIONADO: Machine Learning                             │
│                                                                     │
│ 🎯 Progreso: ████░░░░░░ 25% (12h estudiadas)                      │
│ ⭐ Evaluaciones: 2/5 completadas                                   │
│ 📅 Última sesión: Hace 3 días                                     │
│ 🔄 Próxima revisión: ¡HOY!                                        │
│                                                                     │
│ 📋 EVALUACIONES REALIZADAS:                                        │
│ ✅ Quiz Básico: 85% (8/10) - Hace 1 semana                       │
│ ✅ Conceptos Fundamentales: 78% (15/19) - Hace 4 días            │
│ ⏳ Pendientes: Algoritmos, Práctica, Examen Final                 │
│                                                                     │
│ ➡️ PRÓXIMOS TEMAS RECOMENDADOS:                                   │
│ 1. 🎯 Supervised Learning (Prerrequisito: 80% ML)                │
│ 2. 🔗 Data Preprocessing (Conexión fuerte)                       │
│ 3. 📊 Statistics Review (Recomendado por IA)                     │
│                                                                     │
│ [📚 Estudiar] [📝 Evaluar] [🔗 Ver Conexiones] [➡️ Siguiente]    │
└─────────────────────────────────────────────────────────────────────┘
```

### **13.4 Estados Visuales de los Nodos**

#### Por Progreso
- **🟢 DOMINADO (>80%):** Verde brillante, tamaño grande, pulso suave, ⭐ si evaluado
- **🟡 EN PROGRESO (40-80%):** Amarillo/Naranja, tamaño mediano, borde animado, ⚡ si activo
- **🔴 PENDIENTE (<40%):** Rojo/Rosa, tamaño pequeño, opacidad reducida, ➡️ si recomendado
- **⚫ NO INICIADO:** Gris, muy pequeño, punteado, 🔒 si requiere prerrequisitos

#### Por Tipo de Conexión
- **🔗 CONEXIÓN FUERTE (>0.8):** Línea gruesa azul con flujo de partículas
- **➡️ PRERREQUISITO:** Flecha direccional verde sólida
- **🔄 RELACIONADO:** Línea punteada gris bidireccional
- **⚡ RECOMENDACIÓN IA:** Línea dorada brillante con destellos

### **13.5 Funcionalidades Inteligentes**

#### Cálculo de Próximos Temas
```python
def calculate_next_recommendations(current_topic_id, user_progress):
    """
    Calcula próximos temas basado en:
    - Prerrequisitos completados
    - Similitud semántica
    - Dificultad progresiva
    - Patrones de aprendizaje del usuario
    """
    
    recommendations = []
    eligible_topics = get_topics_with_prerequisites_met(current_topic_id, user_progress)
    
    for topic in eligible_topics:
        score = calculate_recommendation_score(
            semantic_similarity=get_semantic_similarity(current_topic_id, topic.id),
            difficulty_progression=calculate_difficulty_progression(current_topic_id, topic.id),
            user_interest=get_user_interest_score(topic.id),
            learning_velocity=get_user_learning_velocity()
        )
        
        recommendations.append({
            'topic': topic,
            'score': score,
            'estimated_time': estimate_learning_time(topic.id, user_progress),
            'reason': generate_recommendation_reason(current_topic_id, topic.id)
        })
    
    return sorted(recommendations, key=lambda x: x['score'], reverse=True)[:5]
```

#### Sistema de Evaluaciones Adaptativas
```python
def generate_adaptive_assessment(topic_id, user_level):
    """
    Genera evaluaciones adaptativas basadas en nivel del usuario
    y conceptos específicos del tema
    """
    
    key_concepts = get_topic_concepts(topic_id)
    questions = []
    
    for concept in key_concepts:
        concept_questions = generate_questions_for_concept(
            concept=concept,
            user_level=user_level,
            question_types=['multiple_choice', 'true_false', 'practical', 'explanation']
        )
        questions.extend(concept_questions)
    
    return balance_difficulty(questions, user_level)

def update_mind_map_after_assessment(assessment_result):
    """
    Actualiza mapa mental después de evaluación:
    - Cambia color del nodo según resultado
    - Actualiza conexiones recomendadas
    - Recalcula próximos temas
    """
    
    topic_id = assessment_result['topic_id']
    score = assessment_result['score_percentage']
    
    if score >= 80:
        update_node_status(topic_id, 'mastered', color='#4CAF50')
        unlock_advanced_topics(topic_id)
    elif score >= 60:
        update_node_status(topic_id, 'good_progress', color='#FF9800')
    else:
        update_node_status(topic_id, 'needs_review', color='#F44336')
        schedule_review(topic_id, days=3)
    
    update_recommendations(topic_id, assessment_result)
```

### **13.6 Casos de Uso**

#### Planificación de Estudio
```
Usuario abre mapa mental → Ve progreso actual → 
Identifica próximos temas recomendados → 
Selecciona "Supervised Learning" → 
Ve prerrequisitos (ML 80% ✅) → 
Inicia sesión de estudio
```

#### Después de Evaluación
```
Usuario completa quiz de "Deep Learning" (65%) → 
Nodo cambia a amarillo → 
Sistema sugiere revisar "Neural Networks" → 
Actualiza recomendaciones → 
Programa revisión en 5 días
```

---

*Sistema diseñado para maximizar retención y comprensión profunda*  
*Basado en principios Zettelkasten y ciencia cognitiva*
