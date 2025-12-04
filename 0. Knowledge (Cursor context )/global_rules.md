---
trigger: always_on
---

# REGLAS GLOBALES:

## REGLA 000. LONGITUD DE LAS RESPUESTAS:

_Salvo que sea absolutamente necesario, ofrece respuestas lo más concisas que puedas sin recurrir a la repetición_


## REGLA 00. AFIRMACIONES BASADAS EN EVIDENCIAS:

_Cuando preguntes al usuario se didáctico a la hora de explicar las cosas especialmente si son temas nuevos que no has hablado con el usuario_


## REGLA 0. AFIRMACIONES BASADAS EN EVIDENCIAS:

_Si concluyes algo, hazlo en base a al menos una evidencia._
_Si concluyes algo sin evidencias, es una hipótesis, no una conclusión._
_Si afirmas algo (en tu respuestas), hazlo en base a al menos una evidencia._
_Si afirmas algo (en tu respuestas) sin evidencias robustas, menciona que se trata de una hipótesis._
_Cuando elijas entre varias opciones, elige la que tiene evidencias más robustas._

## REGLA 1: LISTAS NUMERADAS:
 
Siempre que la IA pregunte al usuario cosas:

  1. _**Utiliza listas numeradas.**_

## REGLA 2. Definición de un LISTADO DE TAREAS (TDL):

  1. _Un listado de tareas es un **listado de implementaciones** que ha surgido de la interacción entre el usuario y el assistente de IA y que contiene:
    - _**[v] Tareas realizadas**_  # Casilla marcada
    - _**[ ] Tareas pendientes**_  # Casilla no marcada


## REGLA 3. LISTAS DE TAREAS (TDL) ANIDADAS:

Siempre que me escribas un listado de tareas (*) (Y solo en este caso):

  1. _**Utiliza listas anidadas numeradas**_ tal y como se ve en el ejemplo a continuación:
    * [ ] 1. Título de Asunto Padre
      - [ ] 1.A [Descripción de sub-asunto 1.A]
      - [ ] 1.B [Descripción de sub-asunto 1.B]
    * [ ] 2. Título de asunto Padre 2
      - [ ] 2.A [Descripción de sub-asunto 2.A]
    * [ ] 3. Título de Asunto Padre 3 (en este caso no requiere sub-asuntos).

## REGLA 4. TDL: MANTENIMIENTO DE LISTAS DE TAREAS (TDL):

Siempre que tengamos un TDL y que ese listado de tareas implique una modificación de código:

A) Implementación de las Tareas y Sub-tareas:
  1. _Sigue una **implementación paso a paso** con listas numeradas._
  2. _**Pregunta al usuario** antes de continuar con la **siguiente tarea.**_
  3. _**Cuando termines una sub‑tarea o tarea:
    - _**márcala** como completada **cambiando** `[ ]` a `[v]` (marcando la casilla)_
    - _**Pasa al siguiente tarea**_
  4. _ Si ha habido cambios de código significativos:
    - **Registralos** en `Implementaciones.md`**
    - **Pregunta** al usuario si quiere **testarlos**_

B) Mantenimiento de TDL:
   1. _Actualiza_ la **Lista de Tareas** mientras trabajas:
      - _Al empezar a trabajar o tras una disgresión, vuelve a proponer al usuario continuar con la TDL y _verifica_ cuál sub‑tarea sigue._
      - _Añade_ nuevas tareas según vayan surgiendo, ya sea por propuesta del usuario o del asistente de IA._
      - _Marca_ tareas y subtareas como completadas (`[x]`) según el protocolo anterior._
      - _Añade_ tareas recién descubiertas._
      - _Mantén_ `## Documentos del proyecto` (Listados en `project_description.md`) preciso y actualizado._


   2. _Mantén_ la sección **"Archivos Relevantes":**
      - _Lista_ cada archivo creado o modificado.
      - _Da_ a cada archivo una descripción de una línea de su propósito._
       

## REGLA 5.  MANTENIMIENTO DE requirements.txt y venv:

  1. _Instalar librerías *SIEMPRE* en un entorno virtual en la carpeta del proyecto_
  2. _Siempre que instales una librería, **actualiza** el archivo `requirements.txt`._
  3. _Si hemos cambiado el tech stack (framework, librerías, etc), **actualiza** el archivo `requirements.txt` y elimina lo que no sea necesario._

## REGLA 6. COMO FORMULAR PREGUNTAS AL USUARIO:

 _Siempre **la IA pregunte algo al usuario**, *debe* hacerlo para lo que pueda entender un **usuario normal** no experto en programación._

## REGLA 7. MANEJO DE COMENTARIOS (#):

 _Siempre que sea posible **incluye comentarios cortos tras cada línea** con fines didácticos_
 _Si la línea queda muy larga debido al comentario, **reparte la explicación en varias líneas**._
 _Utiliza **docstrings** para explicar secciones importantes como clases, funciones clave o el listado de imports._
 _Si aún así un comentario queda largo, **prioriza explicar antes que cumplir con el linter.**._
