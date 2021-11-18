[GWN3, GNU Wireless Network 3](https://github.com/vagonbar/gr-gwn3)


# GWN Stop & Wait, preguntas y ejercicios

[Tallerine telecomunicaciones inalámbricas](https://eva.fing.edu.uy/course/view.php?id=1248).

##  Condiciones previas

1. Instalación de GNU Radio 3.9. En máquina virtual, se recomienda Linux Mint XFCE, una distribución basada en Ubuntu con la interfaz gráfica liviana XFCE (ver Installation en el [sitio de GWN3](https://github.com/vagonbar/gr-gwn3)).
2. Instalación de GWN3, página [Quick start](https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/docs/QuickStart.md).
3. Introducción al lenguaje de programación Python de Tallerine.


## Estudio

1. Estudiar las características principales de GWN, en estas páginas:
	1. [Página principal de GWN3](https://github.com/vagonbar/gr-gwn3).
	2. [GWN block characteristics](https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/docs/GWN3Block.md). Describe puertos de entrada y salida, temporizadores repetitivos (timers) y temporizadors por única vez (timeouts).
	3. [Standard blocks](https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/docs/StandardBlocks.md).
3. Estudiar Máquina de Estados; más precisamente, Autómata Finito Determinista. Posible referencia: Wikipedia ES, artículos [Autómata Finito](https://es.wikipedia.org/wiki/Aut%C3%B3mata_finito), y  [Autómata Finito Determinista](https://es.wikipedia.org/wiki/Aut%C3%B3mata_finito_determinista). 
4. Estudiar la implementación en GWN de máquina de estados, página [FSM, Finite State Machine](https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/docs/FSM.md).
5. Estudiar el procolo de transmisión de datos Stop and Wait (buscar referencias).
6. Estudiar la página GWN3 [Stop and Wait network protocol FSM](https://github.com/vagonbar/gr-gwn3/blob/master/libgwn/docs/StopAndWaitFSM.md).
7. Probar la implementación de Stop and Wait en GWN, 
  - en ambiente gráfico con los grafos de flujo `examples/stop_wait_ack.grc` y `examples/stop_wait_send.grc`. 
  - en la terminal de comandos, corriendo desde el directorio `build`, con los comandos
```
 python3 ../python/qa_stop_wait_ack.py     # prueba solo bloque ACK
 python3 ../python/qa_stop_wait_send.py    # prueba bloques send y ACK 
```


## Preguntas y ejercicios

### Sobre la máquina de estados (FSM, Finite State Machine).

  - en la máquina de estados Stop and Wait, ¿cuáles son los símbolos? Estos símbolos no vienen en los mensajes. ¿Cómo resolver esto? 
  - ¿qué es una lista FIFO (First In First Out). ¿Qué otras modalidades existen? ¿Por qué se usa FIFO en el protocolo Stop and Wait?
  - ¿qué es un "deque"? ¿Por qué se usa esta estructura? Ver documentación de Python, `collections.deque`.

En esta implementación en GWN del protocolo Stop and Wait.
  - ¿en qué módulo está codificada la máquina de estados? ¿De qué módulos depende? ¿Qué hace cada uno?
  - ¿en qué bloque se construye el objeto máquina de estados? ¿Quién le pasa a la máquina de estados los eventos recibidos? ¿Cómo devuelve la máquina de estados sus resultados? ¿Qué campos contiene ese retorno? ¿Qué significa cada uno?
  - ¿Qué relación hay entre el mensaje recibido y el símbolo que se le pasa a la máquina de estados? ¿Dónde se define esa relación?
  - en la máquina de estados, la función `fn_push`, antes de encolar un evento, ¿no debería verificar si el buffer está lleno?
  - la función `fn_resend`, antes de ejecutarse, ¿no debería verificar que no se han agotado los reintentos?
  - en el módulo `stop_wait_FSM.py` existen las funciones de condición (retornan True o False) `cn_retries_left` y `cn_no_retries_left`. ¿Por qué son necesarias dos funciones, si una es la opuesta de la otra?
  - en el módulo `stop_wait_FSM.py`, en algunas funciones aparece la variable `command`. ¿Para qué sirve?
  - las funciones del módulo `stop_wait_send.py` reciben como parámetros `(fsm, event, block)`. ¿Qué es cada uno? ¿Por qué son necesarios?


### Sobre el protocolo Stop and Wait


En Stop and Wait intervienen estos parámetros:
  - probabilidad de pérdida en el canal.
  - tiempo antes de reintentar el envío de un paquete sin acuse de recibo (sin ACK).
  - cantidad de reintentos antes de desistir (FSM a estado Stop por exceso de reintentos).
  - tamaño del buffer, cantidad de paquetes enviados sin acuse de recibo antes de desistir (FSM a estado Stop por buffer lleno).
  - intervalo de envío entre mensajes.
  - cantidad de mensajes a enviar.
  - tiempo de ejecución.

**Objetivo:** encontrar una fórmula para la probabilidad de recibir el envío completo de un cierto número de paquetes, en un tiempo máximo total, para una probabilidad de pérdida determinada. Esto dependerá del intervalo entre paquetes, el tiempo antes de cada reintento, la cantidad de reintentos, y el tamaño del buffer. Con esta fórmula, será posible determinar estos últimos parámetros para asegurar la recepción completa del envío con una cierta probabilidad. 

Estudiar la relación entre estos parámetros:
  - fijadas una probabilidad de pérdida, un intervalo y la cantidad de mensajes a enviar, ¿en cuánto se debería fijar el tiempo de ejecución para recibir todos los mensajes? Tratándose de probabilidades de pérdida, no hay un valor único. Para un cierto tiempo de ejecución, ¿cuál sería la probabilidad de completar la ejecución?
  - estudiar la relación entre intervalo de envíos y tiempo de reintento. ¿Puede establecerse alguna recomendación?
  - para comprobar el llenado del buffer, ¿cómo deberían ajustarse la probabilidad de pérdida, el tamaño del buffer, el tiempo de reintento? ¿Por qué importan esas relaciones? ¿Y la cantidad de reintentos?
  - para comprobar el agotamiento de los reintentos, ¿cómo deberían fijarse los parámetros anteriores?
  - diseñar experimentos para comprobar las conclusiones de las preguntas anteriores. Tratándose de probabilidades, hacer al menos 5 pruebas con cada configuración y anotar los resultados.
  - determinar un conjunto de valores de parámetros para visualizar en un solo experimento, con una cierta probabilidad, estos fenómenos: 1) todos los paquetes se recibieron; 2) se llenó el buffer; 3) se agotaron los reintentos. Como criterio de aceptación, en 10 pruebas deberían aparecer las tres situaciones al menos una vez.

El grafo de flujo usado en estas pruebas asume pérdida solo en el envío, no en el retorno, por lo que no se pierde ningún ACK. Si para modelar una situación más realista se coloca un canal virtual con pérdida también en el retorno, ¿seguirá funcionando? ¿Qué cambios se esperarían?
 
 **Sugerencia.** Para cambiar los parámetros de ejecución resulta más práctico usar la prueba QA (módulo python `qa_stop_wait_send.py` que el diagrama de flujo GRC (en el GNU Radio Companion, interfaz gráfica).
 
 **Propuesta.**
 ¿Cómo podría modificarse el módulo `qa_stop_wait_send.py` para pedir al usuario los valores de los parámetros antes de ejecutarse? Dejar valores sugeridos, si el usiario no los cambia, se toman esos.
 
 
[Back to README](../../README.md)

