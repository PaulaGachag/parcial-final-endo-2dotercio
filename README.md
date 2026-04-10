# Parcial Segundo Corte - Paula Andrea Gacha
# FastFinTech - Enfoque DataOps


# 1. Análisis del incidente y fallas de gobierno de datos


## 1.1 Cinco fallas 


### Falla 1: No existía control adecuado sobre datos sensibles

La empresa permitió que un analista descargara datos personales de miles de clientes a un equipo personal eo significa que no habia una política estricta que limitara la extracción de información sensible, ni mecanismos técnicos para evitarla, este obviamente es un problema grave porque los datos incluían nombres, cédulas, ingresos e historial de pagos y sa combinación permite identificar directamente a las personas y conocer información financiera delicada. En un contexto de servicios financieros esto no se debe tratar como un archivo cualquiera

**Principio DataOps violado:** seguridad y control de acceso al dato

Desde DataOps el acceso a los datos debe estar gobernado porue no se trata solo de “tener permisos” sino de que el uso del dato esté controlado, monitoreado y alineado con el nivel de sensibilidad de la información.


### Falla 2: No se anonimizaban ni protegían los datos antes del análisis

El analista recibió información sin anonimización, lo que quiere decir que no existía un proceso previo para proteger los datos antes de ser usados en tareas exploratorias o análisis no productivos

**Principio DataOps violado:** calidad y seguridad desde el diseño

En DataOps, la calidad del proceso no solo significa que el dato esté “bien formado”, sino también que sea usado de forma apropiada según el contexto el hechon de entregar datos reales donde no eran necesarios es un erro grave 


### Falla 3: No había auditoría suficiente

El caso sugiere que la organización no tenía suficiente trazabilidad sobre quién descargaba datos, cuándo lo hacía qué archivo usaba ni para que proposito

**Principio DataOps violado:** observabilidad y trazabilidad.

DataOps insiste en que los flujos de datos deben dejar evidencia. Cada ejecución, validación, cambio importante y uso sensible debería poder revisarse después porque si no hay rastro, no hay control real


### Falla 4: No existían validaciones automáticas de calidad suficientemente fuertes

El error en la transformación afectó a una región específica durante tres meses y eso demuestra que no existían reglas automáticas capaces de detectar comportamientos anormales o resultados incoherentes

**Principio DataOps violado:** monitoreo continuo y validación automatizada.

Uno de los objetivos centrales de DataOps es encontrar errores lo antes posible y como aca vemos si una empresa depende de revisar todo manualmente o de notar el problema cuando ya afectó a miles de clientes, entonces su proceso no es confiable


### Falla 5: No existía una definición clara de responsables del dato

El incidente también deja ver que no había dueños claros del dato, ni del pipeline, ni del cumplimiento de políticas y cuando no hay responsables definidos, los errores se mueven entre áreas sin que nadie los asuma completamente

**Principio DataOps violado:** colaboración y responsabilidad compartida.

DataOps promueve que negocio, ingeniería y analítica trabajen juntos con responsabilidades claras, sk el dato es crítico para el negocio, entonces no puede quedar sl aire

## 1.3 Cómo la falta de un modelo de gobierno de datos permitio que el incidente pasara desapercibido durante meses

La falta de un modelo de gobierno de datos fue la razón principal por la cual el problema duró tanto tiempo sin ser detectado porque cuando una organización no tiene gobierno de datos normalmente tampoco tiene reglas claras, responsables definidos, criterios de calidad obligatorios, controles de acceso estrictos, mecanismos de auditoría ni monitoreo constante y racias a todo eso crea un ambiente donde los errores pueden crecer en silencio

En el caso de FastFinTech, el incidente no pasó desapercibido solo porque hubo un error técnico gtambien pas desapercibido porque no existía una estructura organizacional y operativa capaz de verlo a tiempo.

## 1.4 KPIs para prevenir incidentes similares

### KPI 1: Porcentaje de registros con error de calidad

**Objetivo:** detectar si el pipeline está recibiendo o generando datos defectuosos.

**Fórmula:**

`(registros con error de calidad / registros totales procesados) * 100`

**Qué se considera error de calidad en este contexto:**
- campos obligatorios nulos
- cédulas duplicadas
- ingresos negativos o cero
- montos inválidos
- categorías fuera de lo permitido
- registros que no cumplen el esquema

**Umbral de alerta:** mayor a 2%

**Frecuencia de medición:** en cada ejecución del pipeline

**Justificación:**
Este indicador es importante porque permite ver rápidamente si algo cambió en la entrada o en una etapa del proceso, asi sii el porcentaje aumenta de manera repentina se debe revisar antes de continuar, es basico pero funcional


### KPI 2: Porcentaje de accesos o extracciones no autorizadas

**Objetivo:** detectar mal uso del dato, especialmente si se trata de información sensible

**Fórmula:**

`(accesos o extracciones fuera de política / total de accesos o extracciones) * 100`

**Qué puede contarse como acceso fuera de política:**
- exportación de datos sensibles sin aprobación
- consulta a datos personales desde dispositivos no autorizados
- descargas masivas no justificadas
- acceso a información que no corresponde al rol del usuario

**Umbral de alerta:** mayor a 0%

**Frecuencia de medición:** diaria

**Justificación:**
En seguridad de datos sensibles un solo acceso indebido ya merece atención, por eso el umbral puede ser cero en este KPI ayuda a no normalizar pequeñas violaciones, que muchas veces luego terminan en incidentes más graves


### KPI 3: Diferencia de tasa de rechazo entre regiones

**Objetivo:** detectar sesgos, errores de transformación o comportamiento anormal del modelo o del pipeline.

**Fórmula:**

`tasa de rechazo más alta entre regiones - tasa de rechazo más baja entre regiones`


**Umbral de alerta:** más de 10 puntos porcentuales de diferencia

**Frecuencia de medición:** semanal

**Justificación:**
En el caso el problema afectó a una región específica por eso este KPI sería muy útil claramente no asegura por sí solo que el sistema sea justo, pero sí ayuda a descubrir diferencias llamativas que merecen revisión.



# 2. Arquitectura y estrategia DataOps

## 2.1 Diagrama del pipeline con paradigma ELT

A continuación se presenta un diagrama simple del pipeline bajo el enfoque ELT.

```text
+----------------------+      +----------------------+
| API de transacciones |      | CSV de clientes      |
+----------+-----------+      +----------+-----------+
           |                             |
           +-------------+---------------+
                         |
                         v
                 +---------------+
                 |   Data Lake   |
                 |  datos crudos |
                 +-------+-------+
                         |
                         v
         +----------------------------------+
         | Transformaciones / validaciones  |
         | limpieza, reglas, enriquecimiento|
         +----------------+-----------------+
                          |
                          v
                  +---------------+
                  | Data Warehouse|
                  | datos curados |
                  +-------+-------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
     +----------------+      +------------------+
     | Reportes/BI    |      | Modelos ML       |
     | dashboards     |      | scoring/riesgo   |
     +----------------+      +------------------+
---

## 2.2 ¿Por que elegir ETL sobre ETL startup

Para este caso, considero que ELT es una mejor opción que ETL, especialmente para una startup de microcréditos que puede crecer rápido, cambiar reglas con frecuencia y necesitar rehacer análisis cuando encuentre errores

La diferencia principal es que en ETL primero se transforma y luego se carga, mientras que en ELT primero se carga el dato crudo a una plataforma central y después se transforma dentro del entorno de almacenamiento o análisis


### **Venaja 1**: Permite conservar el dato original

 Si el dato crudo se conserva en el Data Lake, entonces cuando se descubre un error en una transformación se puede volver a procesar desde el origen sin perder información

En este caso eso habría sido especialmente útil porque el problema estuvo tres meses sin detectarse. Si no se conserva el dato original, corregir retrospectivamente puede ser mucho más difícil

### **Vengtaja 2:** Da más flexibilidad para cambiar reglas de negocio

En microcréditos, las reglas de riesgo pueden cambiar con frecuencia. Por ejemplo:

puede cambiar la forma de calcular una cuota
puede ajustarse la clasificación del riesgo
puede agregarse una nueva variable
puede revisarse una regla de negocio por cumplimiento o por auditoría

Con ELT, estas transformaciones se pueden rehacer sin volver a reconstruir completamente todo el flujo desde fuentes externas y esso da más agilidad y también más control

## 2.3 Múltiples entornos para un equipo de 5 personas con recursos limitados

- 2.3.1 Entorno de desarrollo

Este ambiente sirve para que cada integrante haga pruebas, construya nuevas transformaciones, revise reglas y corrija errores sin afectar a los demás.

Qué datos usaría:

datos sintéticos o anonimizados
muestras pequeñas
archivos de ejemplo controlados

¿por que?:

reduce riesgo de exposición
hace más rápida la prueba
evita trabajar con información real innecesaria

- 2.3.2 Entorno de staging

Este ambiente sirve para probar el pipeline de forma más cercana a producción antes del despliegue final.

Qué datos usaría?:

una muestra más grande
estructura lo más parecida posible a producción
datos anonimizados o pseudonimizados
simulaciones de errores reales

¿por que?:
Por qué:
Staging debe comportarse parecido a producción, porque ahí se valida que el cambio realmente funciona

- 2.3.3 Entorno de producción

Es el ambiente real donde corre el pipeline oficial y donde se generan las salidas usadas por el negocio o el modelo

Qué datos usaría?:

datos completos
fuentes oficiales
controles estrictos de acceso
auditoría obligatoria

¿por que?:

Producción es donde el impacto del error es real, por eso debe tener el mayor nivel de protección, revisión y monitoreo

## 2.4 Cómo evitar el “pantano de datos”
1. Separar los datos por capas
2. Mantener nombres claros y consistentes
3. Documentar qué contiene cada dataset
4. Aplicar validaciones de calidad antes de promover datos
5. Eliminar o archivar duplicados innecesarios
6. Asignar responsables por dataset o dominio

## 2.5 Cómo garantizar que los cambios que pasan en staging no rompan producción

1. Usar pruebas automáticas
2. Hacer revisión por pull request
3. Usar staging con datos representativos
4. Definir condiciones mínimas antes de desplegar
5. Tener trazabilidad de la versión desplegada
6. Monitorear después del despliegue

# 3. etica, regulaciones y cultura de datos
## 3.1 (4) pasos para evitar sesgo 
### 1: Revisar la calidad y representatividad de los datos: antes de entrenar o desplegar un modelo, se debe analizar si los datos: tienen errores, tienen faltantes, están desbalanceados, representan bien a los distintos grupos, contienen variables que puedan introducir discriminación indirecta

### 2: Evaluar el resultado por grupos y no solo en promedio general: no basta con decir que el modelo tiene buen desempeño “en general”, ambién hay que revisar cómo se comporta por diferentes regiones, genero, y demas segmentos

### 3: Documentar riesgos, supuestos y límites del modelo ya que todo modelo debe ir acompañado por una explicación comlo: que datos usa, que variables son críticas, que tan sensible es a errores en el pipeline, qu grupos podrían verse afectados entre otras

### 4: Aprobar y monitorear antes y después de producción, antes del despliegue debe haber una revisión mínima de calidad, desempeño y posible sesgo ya luego del despliegue el monitoreo debe continuar y mo se debe asumir que el modelo será correcto para siempre

## 3.2 Aplicación del principio “datos como producto”

Decir que los datos son un producto significa que deben verse como algo que tiene usuarios, responsables, reglas, calidad esperada y propósito claro

En FastFinTech esto sería muy útil porque los datos no los usa un solo equipo por ejemplo enegocio los usa para decisiones y reportes, los IT los mueve y protege y los deciencia de datos los usa para entrenar o alimentar modelos

### Artefacto 1: Contrato de datos: un contrato de datos o acuerdo técnico donde se define:
nombre del dataset, campos obligatorios, tipos de datos, reglas de calidad,responsables del productor y consumidor

Artefacto 3: Matriz de acceso y clasificación de sensibilidad, otro artefacto muy útil sería una matriz que indique: que datasets existen, que nivel de sensibilidad tienen, quién puede verlos, quien puede exportarlos, quien puede modificarlos

## 3.3 Scraping de información crediticia, Habeas Data y alternativas legales

### Razón 1: viola el principio de autorización y control del titular: los datos crediticios son datos personales usados para decisiones importantes en Colombia u otros paises, no se pueden recolectar y usar libremente sin base legal ni autorización adecuada del titular

Hacer scraping para obtener esta información sin el procedimiento correcto ignoraría el derecho que tiene la persona a saber quién consulta su información, para qué se consulta y cual es lña justificacion

### Razón 2: el hecho de que la información sea visible o accesible técnicamente no significa que sea libre de usar, muchos errores éticos nacen de esa idea de que si se puede extraer entonces se puede usar lo cual obviamente no es verdad

Aunque un sitio tenga información disponible, eso no autoriza a terceros a automatizar la recolección de datos sensibles para su propio beneficio.

### Razón 3: se incumplen principios de finalidad, proporcionalidad y uso legítimo, la protección de datos personales no se basa solo en tener el dato, sino en para qué se obtiene y cómo se usa

### Alternativa 1: Contratar una fuente autorizada o buró de crédito por canal oficial, la empresa puede hacer un convenio o contrato formal con una entidad autorizada que provea la información por medios legales y con trazabilidad
-Viabilidad: alta
-Costo estimado: medio o alto
-Nivel de confianza de los datos: alto

### Alternativa 2: Obtener consentimiento explícito del titular y consultar por API o servicio oficial, durante la solicitud de crédito, la empresa puede pedir autorización clara al cliente para consultar su información crediticia mediante una fuente oficial.

-Viabilidad: alta
-Costo estimado: medio
-Nivel de confianza de los datos: alto

### Alternativa 3: Usar información interna histórica de comportamiento de pago, si la empresa ya tiene historial propio de pagos, mora, cumplimiento y comportamiento, puede usar esa información como variable complementaria

-Viabilidad: media
-Costo estimado: bajo
-Nivel de confianza de los datos: medio

### Seudocodigo 
func scrape_credit_score(cedula):

    registrar_log(
        evento="inicio_consulta",
        cedula=cedula,
        fecha_hora=ahora(),
        usuario="sistema_fastfintech"
    )

    si cache_existe(cedula) y cache_no_expirada(cedula):
        dato = leer_cache(cedula)

        registrar_log(
            evento="cache_hit",
            cedula=cedula,
            fecha_hora=ahora(),
            detalle="dato obtenido desde cache"
        )

        retornar dato

    aplicar_rate_limit()

    headers = {
        "User-Agent": "FastFinTech-Audit-Client/1.0"
    }

    intentar:
        respuesta = consultar_fuente_autorizada(
            cedula=cedula,
            headers=headers,
            timeout=5
        )

        si respuesta.codigo == 404:
            registrar_log(
                evento="no_encontrado",
                cedula=cedula,
                fecha_hora=ahora(),
                detalle="la cédula no existe en la fuente"
            )
            retornar null

        si respuesta.estructura_invalida:
            registrar_log(
                evento="cambio_estructura",
                cedula=cedula,
                fecha_hora=ahora(),
                detalle="la respuesta cambió de formato"
            )
            retornar error("estructura inesperada")

        puntaje = extraer_puntaje(respuesta)
        guardar_en_cache(cedula, puntaje, ttl=3600)

        registrar_log(
            evento="consulta_exitosa",
            cedula=cedula,
            fecha_hora=ahora(),
            detalle="puntaje obtenido y guardado en cache"
        )

        retornar puntaje

    excepto timeout:
        registrar_log(
            evento="timeout",
            cedula=cedula,
            fecha_hora=ahora(),
            detalle="la fuente no respondió a tiempo"
        )
        retornar error("timeout")

    excepto error_red:
        registrar_log(
            evento="error_red",
            cedula=cedula,
            fecha_hora=ahora(),
            detalle="falló la conexión"
        )
        retornar error("fallo de red")

    excepto excepcion_general:
        registrar_log(
            evento="error_general",
            cedula=cedula,
            fecha_hora=ahora(),
            detalle="error inesperado"
        )
        retornar error("error inesperado")

## 3.4 Si mi jefe hace scraping sin autorizacion
Le explicaría de forma clara que la empresa puede exponerse a sanciones, demandas, daño reputacional o problemas con auditorias. le propondría una alternativa legal que sí permita avanzar, aunque tenga costo y si no accede, dejaría constancia por escrito de mi posición, si aun así la instrucción continuara escalaría el caso a un área de cumplimiento, legal o a un superior con responsabilidad 

# REQUISITO D PARTE PRACTICA 
# 4. Diseño de scraping ético y autorizado
## 4.1 Si hipotéticamente la empresa sí tuviera autorización válida y una fuente legal para consultar información crediticia, entonces el sistema debería diseñarse respetando controles técnicos y de gobernanza

Diagrama de secuencia simplificado
Usuario interno autorizado
        |
        v
Servicio de consulta crediticia
        |
        |--- verificar consentimiento vigente --->
        |
        |--- consultar cache con TTL ----------->
        |             |
        |             |-- si existe --> retornar dato
        |
        |--- aplicar rate limiting -------------->
        |
        |--- consultar fuente oficial ----------->
        |
        |--- registrar auditoría ---------------->
        |
        |--- guardar en cache ------------------->
        |
        v
Retornar resultado
## 4.2 Explicación del diseño
-Consentimiento del titular, lo primero debe ser verificar si la persona autorizó la consulta. Sin esto, no debería hacerse ninguna petición.
-Caché con TTL, antes de consultar a la fuente externa, se revisa si ya existe un dato reciente en caché. Esto ayuda a reducir consumo, latencia y carga sobre la fuente.
-Rate limiting,no se deben disparar peticiones sin control. El rate limiting sirve para respetar la fuente, evitar abuso y mantener estabilidad.
-Auditoría de cada consulta, toda consulta debe registrar:fecha y hora, usuario o sistema que consulta, cédula consultada, resultado de la operación,i vino de caché o de fuente externa

## 4.3 Pseudocódigo no ejecutable pedido en el requisito D
func consultar_puntaje_crediticio(cedula, usuario):

    si no existe_consentimiento_vigente(cedula):
        registrar_audit_log(
            timestamp=ahora(),
            usuario=usuario,
            cedula=cedula,
            evento="sin_consentimiento"
        )
        retornar error("no hay consentimiento vigente")

    dato_cache = buscar_en_cache_redis(cedula)

    si dato_cache existe:
        registrar_audit_log(
            timestamp=ahora(),
            usuario=usuario,
            cedula=cedula,
            evento="cache_hit"
        )
        retornar dato_cache

    aplicar_rate_limit()

    respuesta = consultar_fuente_autorizada(cedula)

    si respuesta exitosa:
        guardar_en_cache_redis(cedula, respuesta, ttl=3600)

        registrar_audit_log(
            timestamp=ahora(),
            usuario=usuario,
            cedula=cedula,
            evento="consulta_exitosa"
        )

        retornar respuesta

    registrar_audit_log(
        timestamp=ahora(),
        usuario=usuario,
        cedula=cedula,
        evento="consulta_fallida"
    )

    retornar error("no fue posible consultar el puntaje")

## 5.4 Métricas para monitorear la salud del sistema de extracción crediticia
### Métrica 1: Tiempo promedio de respuesta
Qué mide: cuánto tarda en promedio una consulta.
Por qué importa:
Si el tiempo sube demasiado, el sistema se vuelve lento y puede afectar la experiencia o la operación.

### Métrica 2: Tasa de éxito de consultas
Qué mide: porcentaje de consultas que terminan correctamente.
Fórmula sugerida:
consultas exitosas / consultas totales * 100
Por qué importa:
Permite saber si la fuente está respondiendo bien o si el sistema está fallando demasiado.

### Métrica 3: Latencia o tiempo de respuesta de caché
Qué mide: cuánto tarda el sistema en responder cuando el dato viene de caché.
Por qué importa:
La caché debe hacer el sistema más eficiente. Si también se vuelve lenta, deja de cumplir su propósito.