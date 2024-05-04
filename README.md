<h1>Simulación en entorno Webots aplicando Aprendizaje por Refuerzo</h1>
<h2>Repositorio creado para la asignatura Modelling Brains en la carrera de Ingeniería de Software de la Universidad Nacional del Centro de la Provincia de Buenos Aires de Tandil.</h2>
<h2>Fecha de realización: Octubre 2023</h2>

<h3>1. Introducción</h3>
<p>El objetivo del presente proyecto era realizar la simulación de un robot Pioneer en el entorno Webots. El robot Pioneer 3-At posee cuatro motores: una rueda derecha frontal, una rueda izquierda frontal, otra rueda derecha trasera y otra rueda izquierda 
  trasera. Además el modelo propuesto por webots posee 16 sensores de distancia numerados del 0 al 15. Para lograr los objetivos del proyecto se añadió un sensor de cámara, dos sensores de distancia infra-rojos, un nodo compass y un nodo GPS.</p>
<p>El objetivo del robot era encontrar determinado objeto y llevarlo a la posición correspondiente evitando dejarlo en una posición prohibida, complementario a lo mencionado el robot debía lograr el mejor camino evitando los obstáculos presentes 
  en el entorno.</p>
<p>Como comportamientos simples se implementan la evasión de obstáculos y la detección del objetivo. Mientras que como comportamiento aprendido, aplicando Q-Learning, el robot aprende a llevar el objetivo a la posición correspondiente evitando llevarlo a la posición prohibida.</p>

<h3>2. Comportamientos implementados</h3>
<h4>2.1 Comportamientos simples</h4>
<p>La implementación de los comportamientos simples se basó en el concepto de Vehículos de Braitenberg, ideado por Valentino Braitenberg.</p>
<h4>2.1.1 Evasión de obstáculos</h4>
<p>Los movimientos realizados por el robot para evadir obstáculos se basaron en la relación de los sensores con los motores de manera inhibitoria. Partiendo de la idea de conectar un cable entre el motor y el sensor para que los valores brindados por el 
  sensor determinen la velocidad del motor, se dividieron los sensores frontales en dos partes una destinada al lado derecho y otra destinada al lado izquierdo.</p>

![robot](https://github.com/melisamessa/QLearning_Webots/assets/105131503/420d90ca-5bc0-41f0-9cc8-f5ac7082f86a)

<p>De esta manera visualizandolo en la imagen, para la implementación del control de manera inhibitoria se establece que cuanto mayor son los valores de los sensores so3, so4, so15 menor será la velocidad de los motores del lado derecho y mayor la velocidad de los motores izquierdos. 
  En cambio cuando son mayores los valores de los sensores so4, so2, so5, so7, so0, so8 tendrán mayor velocidad los motores izquierdos y menor velocidad los motores derechos.</p>
<p>Entonces cuando se da el caso 1, el robot girará a la derecha, y cuando se da el caso 2, el robot girará a la izquierda.</p>
<p>Mientras los sensores se mantienen estables las velocidades de los motores son equivalentes y por lo tanto el robot se mueve hacía adelante.</p>

<h4>2.1.2 Detección de objetivo</h4>
<p>La cámara se utilizó para la detección del objetivo. Se usaron las funciones de reconocimiento para detectar los objetos y que el robot los reconociera por su color.</p>
<p>De esta manera el robot detecta todos los objetos del entorno y avanza entre ellos buscando el objetivo.</p>
<p>Cuando la cámara detecta el verdadero objetivo se podría decir que se utiliza la ideología de braitenberg para ir hacía él en base a lo que el robot percibe por la cámara. En este caso utiliza la posición del objeto en la imagen de la cámara y en base a si se presenta a la derecha o 
  a la izquierda se establece la velocidad de los motores.</p>
<p>Si el objeto se encuentra en la mitad de la imagen de la cámara -1, entonces significa que está a la izquierda por ende establece una velocidad negativa izquierda y una positiva derecha. Mientras que si se encuentra en la mitad de la cámara +1 girara a la derecha estableciendo una 
  velocidad negativa al motor derecho y positiva al motor izquierdo.</p>

<h4>2.2 Comportamiento aprendido</h4>
<p>El comportamiento planteado es llevar el objeto objetivo a la posición correspondiente donde el robot deberá dejarlo.</p>
<p>La implementación de un comportamiento aprendido se realiza mediante alguna técnica, en el caso del presente proyecto se realizó aplicando Aprendizaje por refuerzo (Reinforcement Learning).</p>
<p>Lo que intentará el agente es construir una política óptima interactuando con el entorno adaptando una técnica explícita basada en prueba y error. Aprenderá intentando repetidamente resolver el problema utilizando diversos enfoques en episodios diferentes mientras actualiza continuamente la política.</p>
<p>El agente inteligente seguirá el proceso de decisión de Markov.</p>

<h4>2.2.1 Proceso de decisión de Markov</h4>
<p>El agente percibe un conjunto finito de estados distintos del entorno, E, y un conjunto finito de acciones, A, para interactuar con el mismo.</p>
<p>En cada instante de tiempo el agente percibe un estado concreto, E<sub>t</sub>, y selecciona una acción posible, A<sub>t</sub>, que ejecuta para obtener un nuevo estado E<sub>t+1</sub>.</p>
<p>El entorno responderá a la acción del agente por medio de una recompensa o castigo, R<sub>t</sub>.</p>
<p>Tanto la recompensa como el estado siguiente dependen únicamente del estado actual y de la acción tomada.</p>

![proceso_Markov](https://github.com/melisamessa/QLearning_Webots/assets/105131503/0b08bf8a-0554-4cf6-b464-079c41d0de81)

<h4>2.2.2 Algoritmo Q-Learning</h4>
<p>El algoritmo Q-Learning involucra a un agente inteligente en un entorno con diversos estados.</p>
<p>En Q-Learning el valor Q indica la la calidad de una acción particular, a, en un estado dado, s, representado por la siguiente función Q(s, a).</p>
<p>El agente estará interesado en identificar la acción de mayor calidad en el estado en que se encuentra.</p>
<p>Formalmente, los valores Q son las estimaciones actuales de la suma de recompensas futuras si se toma una acción particular en ese instante de tiempo. Estiman cuánta recompensa se puede esperar acumular a través de todos los pasos restantes en el episodio actual si el agente se encuentra actualmente en el estado 
  s y decide tomar la acción a. Por lo tanto, los valores Q aumentan cada vez que el agente se acerca a la recompensa más alta.</p>
<p>En aprendizaje por refuerzo, este algoritmo se puede usar con recompensas positivas o negativas. Entonces el objetivo del agente inteligente es maximizar las recompensas positivas y minimizar las negativas.</p>
<p>Los valores Q mencionados se almacenan en una tabla donde la cantidad de filas es la cantidad de estados posibles, y cada una contiene una columna para cada acción posible. Una tabla Q óptima será aquella que contenga valores que permitan al agente tomar la mejor acción en cualquier estado posible. La tabla representa 
  la política de actuación de los agentes en el entorno actual.</p>
<p>Para obtener los valores Q se utiliza la fórmula de diferencias temporales que nos brinda un método para calcular cuánto se debe cambiar el valor Q para la acción realizada en el estado anterior en función de lo que el agente ha aprendido de los valores Q para el estado actual.</p>
<p>$TD(s_t, a_t)= r_t + γ . max Q(s_{t+1}, a_t) - Q(s_t, a_t)$</p>

* r<sub>t</sub>: recompensa inmediata tomada en el estado anterior
* γ: factor de descuento gamma, comúnmente utilizado con el valor 0.9, proporciona un mecanismo para descontar recompensas futuras.
* max Q(s<sub>t+1</sub>, a<sub>t</sub>): valor máximo Q actualmente disponible para cualquier acción en el estado actual.
* Q(s<sub>t</sub>, a<sub>t</sub>): valor Q de la acción más reciente.

<p>Finalmente la ecuación de Bellman nos indica exactamente el nuevo valor Q para la acción realizada en el estado anterior. Está ecuación incluye un parámetro alfa, tasa de aprendizaje, que define qué tan rápido se ajustan los valores Q, controlando la rapidez con la que el agente aprende.</p>
<p>$Q^{new}(s_t, a_t)= Q^{old}(s_t, a_t)+\alpha . TD(s_t, a_t)$</p>

<p>Para elegir qué acción tomar se debe tener en cuenta implementar un algoritmo que  permita al agente explorar todo su entorno. Por ende se utiliza el algoritmo Epsilon-Greedy que permite elegir la acción con mayor valor Q el 90% de las veces, y el restante 10% de las veces elige una acción al azar. 
  De esta manera el agente explorará lo que parece ser un camino no prometedor a corto plazo con la esperanza de que pueda conducir al descubrimiento de un camino prometedor a largo plazo.</p>

![proceso_QLearning](https://github.com/melisamessa/QLearning_Webots/assets/105131503/49a14d38-97b9-4471-87a2-3dadafcc23b6)

<h4>2.2.3 Implementación</h4>
<p>El diseño del sistema Q-Learning es la definición del entorno. Dicho entorno consta de estados, acciones y recompensas.</p>
<h4>Estados</h4>
<p>La arena de la simulación de Webots se puede representar como un diagrama de filas y columnas. De está manera cada celda del piso del entorno representa un estado posible. Las celdas especiales son la celda que contiene un plano rojo que es el estado que el robot debe evitar, y la celda que contiene 
  un plano verde que es el estado objetivo al que el robot debe llegar.</p>
<p>Entonces cada una de las 36 celdas representa un estado o una situación en la que el robot podría encontrarse en algún momento determinado.</p>
<p>El estado es identificado por el índice de fila y el índice de columna.</p>

![diagrama_estados](https://github.com/melisamessa/QLearning_Webots/assets/105131503/7ae977d4-91e2-436f-b450-43bae3d5bf58)

<h4>Acciones</h4>
<p>Las acciones para el agente en el escenario planteado son únicamente las direcciones que puede tomar para llegar al siguiente estado. Es decir el robot se puede mover hacía arriba, hacía la derecha, hacía la izquierda o hacía abajo a partir del estado actual en que se encuentre.</p>
<p>Para establecer estas direcciones se tomo en cuenta el entorno observado por el programador, siendo que hacía arriba toma la dirección hacía filas menores, hacía abajo toma la dirección hacía filas mayores, a la izquierda toma dirección hacía columnas menores y a la derecha toma dirección hacía columnas mayores. Se definió de está manera para que no dependiera la acción de hacía donde estaba posicionado el frente del robot, si no que siempre desde una celda si se toma una acción determinada se llega a la misma celda destino que en cualquier momento de la ejecución.</p>
<p>Se utiliza un arreglo unidimensional para guardar las 4 acciones.</p>

<h4>Recompensas</h4>
<p>A cada estado del entorno se le asigna una recompensa. Sea cual sea la posición del robot, él siempre buscará maximizar su recompensa y minimizar su castigo.</p>
<p>En el ambiente hay una posición objetivo, celda verde, y una posición prohibida, celda roja. Al estado objetivo se le da una recompensa altamente positiva, mientras que al estado prohibido se le aplica una recompensa altamente negativa.</p>
<p>Además en el escenario planteado se utilizan recompensas nulas para todas las demás celdas que no son la posición objetivo. Esto alentará al agente inteligente a minimizar sus castigos debiendo identificar también el camino más corto a la posición final.</p>
<p>Se establecen recompensas nulas a casi la totalidad de estados del entorno, porque si fueran positivas el agente podría decidir quedarse ciclando en ellas sin ir nunca a la posición objetivo, obteniendo una mayor recompensa que logrando el objetivo.</p>
<p>Se utiliza una matriz bidimensional para guardar las recompensas.</p>

![diagrama_recompensas](https://github.com/melisamessa/QLearning_Webots/assets/105131503/126dd8d0-4721-4e46-9aa1-f8e6080f9d02)

<p>Una vez ya determinado el entorno se inicializan las estructuras antes mencionadas con sus valores correspondientes y se inicializa la tabla de valores Q con valores iguales a cero. Son 36 estados, donde cada estado tendrá 4 columnas destinada a las 4 posibles acciones.</p>

<h4>Comienzo y finalización del episodios</h4>
<p>Se estableció 1000 como número de episodios totales.</p>
<p>Por el objetivo planteado como comportamiento complejo se estableció que el primer estado inicial para el primer episodio fuera la celda en la que el robot encontrará el objeto objetivo. Los restantes estados iniciales, que se darán cada vez que comienza un nuevo episodio, serán una celda elegida al azar.</p>
<p>La finalización del episodio se da cada vez que el robot llega a la celda verde y/o cada vez que el robot llega a la celda roja.</p>
<p>El robot únicamente llevará en el primer episodio el objeto objetivo a una de las celdas diferenciadas, roja o verde, y en los restantes episodios se dedicará a aprender a ir a la celda color verde y a evitar la celda color rojo.</p>

<h4>Observaciones adicionales</h4>
<p>En base al objetivo planteado, se debieron tener en cuenta cuestiones adicionales propias del robot para lograr aplicar Q-Learning.</p>
<p>Observando que al trasladarse los motores del robot tenían un pequeño desvío fue necesario utilizar sensores infrarrojos para lograr que todo el tiempo el agente se mantuviera en línea recta movilizándose por las diversas celdas. De está manera se logró tener cuatro acciones y no ocho, donde las cuatro adicionales serían las direcciones en diagonal. Los sensores infrarrojos fueron colocados con el eje x apuntando al suelo, de está manera utilizando la luz el agente lograba detectar el color de la línea posicionada en el suelo y seguirla durante todo el tiempo de aprendizaje.</p>
<p>Teniendo en cuenta que el robot se traslada debido a la velocidad de sus motores las acciones deben coincidir con la dirección en la que se encuentra el robot, su rotación, por ello cada acción que toma el robot es un direccionamiento:</p>

* Si el frente del robot se encuentra hacía arriba, y el agente decide:
   - Al tomar la acción arriba, las velocidades de los motores se mantienen iguales y el ángulo de giro será de 0°.
   - Al tomar la acción derecha, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 45°.
   - Al tomar la acción abajo, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 90°.
   - Al tomar la acción izquierda, la velocidad de los motores derechos será positiva y la de los motores izquierdos negativa, y girará un ángulo de 45°.
* Si el frente del robot se encuentra hacía la derecha, y el agente decide:
   - Al tomar la acción arriba, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 45°.
   - Al tomar la acción derecha, las velocidades de los motores se mantienen iguales y el ángulo de giro será de 0°.
   - Al tomar la acción abajo, la velocidad de los motores derechos será positiva y la de los motores izquierdos negativa, y girará un ángulo de 45°.
   - Al tomar la acción izquierda, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 90°.
* Si el frente del robot se encuentra hacía abajo, y el agente decide:
   - Al tomar la acción arriba, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 90°.
   - Al tomar la acción derecha, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 45°.
   - Al tomar la acción abajo, las velocidades de los motores se mantienen iguales y el ángulo de giro será de 0°.
   - Al tomar la acción izquierda, la velocidad de los motores derechos será positiva y la de los motores izquierdos negativa, y girará un ángulo de 45°.
* Si el frente del robot se encuentra hacía la izquierda, y el agente decide:
   - Al tomar la acción arriba, la velocidad de los motores derechos será positiva y la de los motores izquierdos negativa, y girará un ángulo de 45°.
   - Al tomar la acción derecha, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 90°.
   - Al tomar la acción abajo, la velocidad de los motores derechos será negativa y la de los motores izquierdos positiva, y girará un ángulo de 45°.
   - Al tomar la acción izquierda, las velocidades de los motores se mantienen iguales y el ángulo de giro será de 0°.

<p>Teniendo en cuenta lo planteado anteriormente, adicionalmente hay que establecer los límites que son dados por las paredes del entorno y por las celdas que contienen un obstáculo. Entonces se debió establecer que desde cualquier celda de la fila 0 el agente tiene prohibido tomar la acción arriba, desde cualquier celda de la fila 5 el robot tiene prohibido tomar la acción abajo, desde cualquier celda de la columna 0 el robot tiene prohibido tomar la acción izquierda, y desde cualquier celda de la columna 5 el robot tiene prohibido tomar la acción derecha. De la misma manera se planteó para las celdas que contienen obstáculos de manera estática, por ejemplo si el robot se encuentra en la posición [1, 2] no puede tomar la acción derecha porque en la celda [0,2] hay un obstáculo.</p>
<p>Para realizar todo el proceso era necesario saber en todo momento hacía que dirección se encontraba el frente del robot. Para la primera instancia, se utiliza el nodo compass que modela una brújula digital y devuelve un vector que indica la dirección del norte. Estudiando los valores obtenidos por este vector se establecieron los rangos de valores en los que el robot se encuentra posicionado en las diversas direcciones y así fue posible identificar hacía donde apuntaba el frente del robot.</p>
<p>Una vez comenzando a aprender ya no fue posible utilizar el nodo compass porque los valores se volvían inexactos gracias al redireccionamiento para mantener al agente movilizándose en línea recta. Por ello fue necesario relacionar la acción con la dirección, y en base a la acción elegida tomar la dirección del robot, ya que si la acción era arriba el robot estaría apuntando hacia arriba, si era abajo hacía abajo, si era izquierda hacía la izquierda y si era derecha hacía la derecha.</p>
<p>Por último, la movilización desde el estado final hacía la nueva celda de inicio del nuevo episodio, se realizó teniendo en cuenta la celda y las direcciones. Primeramente el robot llega a la fila nueva y una vez en la fila, se moviliza por las columnas hasta llegar a la celda random indicada. Para realizar estos movimientos también era necesario mantener al robot moviéndose en línea recta y tener en cuenta los obstáculos que se podían presentar en las filas y/o las columnas. Además de tener en cuenta las celdas que no podían ser elegidas como celda random para el inicio del episodio: la celda objetivo, la celda prohibida y las dos celdas que contienen obstáculos.</p>

<h4>Proceso de aprendizaje</h4>
<p>El proceso de aprendizaje sigue los siguientes pasos:</p>

1. El robot se dirige a la celda de inicio de episodio, que será la celda donde se encuentra el objetivo para el primer episodio y la celda random para el resto de los episodios.
2. El robot elige una acción para el estado actual utilizando el algoritmo Epsilon-Greedy, que generalmente elegirá la acción más prometedora y en el 10% de las veces una acción al azar.
3. Realiza la acción elegida y hace la transición al siguiente estado.
4. Recibe la recompensa por realizar la acción para ir al estado y se calcula la diferencia temporal asociada al movimiento.
5. Se actualiza el valor Q para el estado anterior y la acción realizada.
6. Si el nuevo estado al que se dirige el robot no es un estado terminal entonces continúa nuevamente con el paso 2. Si es un estado terminal entonces comenzará desde el paso 1.

<h3>3. Coordinación de los comportamientos</h3>
<p>La gestión y transición adecuada de comportamientos es necesaria para lograr los comportamientos complejos en robots. Ya sea si se busca lograr un comportamiento complejo con un único robot o con más de uno.</p>
<p>Cuando el robot tiene múltiples comportamientos y cada comportamiento está dedicado a realizar una tarea particular es necesario definir un modo de coordinarlos a todos.</p>
<p>Existen diversas formas de coordinar los comportamientos. La coordinación cooperativa se da cuando dos comportamientos se ejecutan en simultáneo cooperando entre ellos. En la coordinación competitiva los comportamientos se van activando de a uno a la vez, y un comportamiento puede interrumpir al otro. La coordinación híbrida sería una combinación de las dos mencionadas anteriormente.</p>
<p>En el presente proyecto se coordinan los comportamientos de manera híbrida. La primera parte de la simulación, por decirlo de alguna manera, comienza con el robot evadiendo obstáculos y la cámara detectando los objetos del entorno, estos dos comportamientos se coordinan cooperativamente.</p>
<p>Cuando la cámara detecta el objeto objetivo, se da una coordinación competitiva, entonces el robot interrumpe la tarea de evitar obstáculos y comienza a dirigirse hacía el objetivo, para entonces poder agarrarlo con el gripper.</p>
<p>Una vez que tiene el objetivo, comienza el comportamiento de aprendizaje, este comportamiento se da de forma competitiva y se mantiene hasta el final de la ejecución.</p>

![diagrama_coordinacion](https://github.com/melisamessa/QLearning_Webots/assets/105131503/92801ca5-d83a-4720-ad45-a107a65940c4)

<h3>4. Resultados experimentales</h3>
<p>Evasión de obstáculos: en las siguientes ilustraciones captadas del entorno Webots se visualizan los valores que poseen los sensores. La primera imagen denota un valor de cero para el sensor número 4, mientras que a medida que avanza el robot hacía el obstáculo se ve que el valor del sensor antes mencionado aumenta a más de 800 y por tanto el robot inhibe la velocidad de las ruedas izquierdas y produce un giro hacía la dirección mencionada. Este resultado sigue la ideología de Valentino Braitenberg.</p>

![resultados_evasion](https://github.com/melisamessa/QLearning_Webots/assets/105131503/6a78e7df-6b68-47d5-a7f8-c06c0b34e390)

<p>Detección del objetivo: en las próximas ilustraciones podemos observar cómo se produce la detección del objeto. En la primera imagen el robot detecta el objeto a la lejanía sobre el lado izquierdo de la imagen capturada por la cámara. Una vez detectado, se puede visualizar en la imagen 2 como el robot se acomoda, el objeto aparece en la parte de la imagen izquierda por ende el robot establece la velocidad de los motores izquierdos en negativo y los derechos en positivo produciendo un giro a la izquierda. Una vez que el robot se acomoda de frente al objeto, es decir, cuando el objeto está al medio de la imagen captada por la cámara comienza a trasladarse hacía el.</p>

![resultados_deteccion](https://github.com/melisamessa/QLearning_Webots/assets/105131503/c13c2e44-df33-4c80-81b2-94756c22cc27)

<p>Q-Learning: en la figura número 9 se visualizan los valores tomados por cada estado ante determinada acción:</p>

![resutlados_qlearning](https://github.com/melisamessa/QLearning_Webots/assets/105131503/de32b44d-5a7b-4f1e-a157-f79993c451f2)

<p>Interpretando los valores de la figura 9 podemos observar:</p>

* Las celdas pertenecientes a los obstáculos poseen valores nulos porque el agente nunca puede posicionarse en ellas. Las celdas correspondientes a la placa verde y la placa roja también poseen valores nulos porque una vez que llega el agente a esa posición el episodio termina y no aprende hasta reposicionarse.
* El valor para la acción up de la celda [1,5] y el valor para la acción right de la celda [0,4] son negativos. Esto se debe a que llegando a esa posición y tomando esa decisión el agente llega a la placa roja.
* Podemos ver que los valores de las celdas de la fila 0 cuando toman la acción left, van en escalera hasta llegar al valor 100 en la celda [0,1]. Esto se debe a que el agente aprendió que desde la celda [0,1] tiene una recompensa muy alta al ir a la izquierda y lo mismo con las otras celdas de la fila 0, ya que tomando la acción izquierda repetidas veces llega a la celda objetivo.
* Como lo planteado anteriormente también denota que desde la fila 1 la acción que aprendió a tomar es la acción up, que lo lleva a la fila 0 desde la cual toma la acción left y llega al objetivo.
* Los valores que se encuentran en cero, especialmente en la fila 5, implican que el robot necesita aún más episodios para lograr completar la tabla de valores. Necesita más interacción con el entorno, y más instancias en las que tomé la decisión random y no la decisión de la acción máxima. Como está visualización es de menos de 100 episodios realizados, es obvio que el robot no llega a aprender todo y que por eso está planteado para 1000 episodios de aprendizaje. Sin embargo se puede ver que ya para menos de 100 episodios tiende a dirigirse a la celda objetivo.

<p>Siguiendo los valores podemos visualizar como ejemplo los siguientes recorridos marcados en amarillo:</p>

![camino1](https://github.com/melisamessa/QLearning_Webots/assets/105131503/4e368c91-4d30-49c7-bd92-5715f6857723)

![camino2](https://github.com/melisamessa/QLearning_Webots/assets/105131503/544c2bb6-1509-4719-81e9-2557cdcb7e76)

![camino3](https://github.com/melisamessa/QLearning_Webots/assets/105131503/1629bbcf-2148-4797-8877-93211ff9fc5c)

<p>En está última figura número 12, podemos observar como el agente rodea y evita la celda que contiene la placa roja, [0,5], y llega a la celda objetivo que posee la placa verde, [0,0].</p>
<p>Los valores de la tabla y los ejemplos de recorrido demuestran el aprendizaje al que llegó el agente, en todos los ejemplos y en la tabla misma se ve que todas las decisiones con mayor valor lo llevan hacía la celda objetivo. Se puede entonces decir con certeza que el agente aprendió.</p>

<h3>5. Extensiones</h3>
<h4>Dinamismo</h4>
<p>Los resultados demuestran que si bien es un proyecto avanzado se podrían considerar diversos factores que posibilitan la necesidad de continuar explorando diversas soluciones.</p>
<p>Primeramente se podría cambiar la coordinación del comportamiento complejo, haciendo que sea cooperativa con el comportamiento simple de evasión de obstáculos y que de esa manera cuando se presenta un obstáculo en el Q-learning el agente lo evite con el comportamiento simple y luego continúe con el comportamiento complejo. De está manera sería más dinámico y no sería necesario especificar estáticamente donde se encuentran los obstáculos.</p>

<h4>PQ-Learning</h4>
<p>Una posible extensión del proyecto, sería aplicar un algoritmo llamado PQ-Learning. Este algoritmo determina como un agente debe comportarse en un entorno de modo que maximice su recompensa, pero en este caso la recompensa es un vector donde cada componente del mismo pertenece a un objetivo. Es decir se utilizará la información brindada por el algoritmo Q-Learning para obtener un resultado en el que el robot aprenda a resolver más de un objetivo.</p>
<p>PQ-Learning permite encontrar equilibrio entre objetivos competitivos y/o cooperativos.</p>

<h4>Deep Learning - Clustering</h4>
<p>Realizar una mejora en el objetivo de detección, extendiendo el proyecto para utilizar técnicas como Deep-Learning y Clustering para que la cámara pueda determinar el objeto y sus cualidades, de esta manera el robot aprendiera por ejemplo a sortear algún obstáculo, como podría ser tener que buscar un objeto al que no se le reconoce el color por alguna situación del entorno.</p>

<h4>Solución de la rotación del robot</h4>
<p>La primera posible actualización debería proveer una manera de no utilizar los sensores que apuntan al suelo para detectar las líneas y mantenerse en línea recta. Se debería de utilizar el compass para esta tarea buscando la forma de que los valores no sean erroneos y realizando entonces un if sobre los valores del sensor para que el robot no tenga ningún desvío y tampoco sean necesarias las líneas del suelo.</p>

<h3>Bibliografía</h3>

* Fernandez-León, J.A., Acosta, G., & Mayosky, M. (2009). Behavioral control through evolutionary neurocontrollers for autonomous mobile robot navigation. Journal of Robotics & Autonomous System, Vol. 57, Issue 4, Elsevier, 411-419.
* Stefano Nolfi (2021). Behavioral and Cognitive Robotics an Adaptive Perspective.
* Fernando Sancho Caparrini, (2019). Aprendizaje por refuerzo: algoritmo Q-Learning.
* Jesse Clifton, Eric Laber (2020). Q-Learning: Theory and Applications.
* César Daniel Garrido, Fernando Lozano Martínez, Carolina Higuera Arias (2020). Sistema de navegación para robot móvil basado en aprendizaje por refuerzo.
* Diego Felipe Ruiz Barreto, María Carolina Bravo Navarro, (2019). Navegación Autónoma y Evasión de Obstáculos en UAV usando Aprendizaje por Refuerzo.
