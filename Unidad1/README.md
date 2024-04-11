# Unidad 1 - Práctica
Esta carpeta del repositorio contiene los ejercicios correspondientes a la Unidad 1 de la materia Computer Vision de la TUIA
## Ejercicio 5
Consigna: Genere un video en un patio o en un hall de edificio donde en un principio se vea vacío y luego aparezca una persona. Mediante los métodos de motion detection (sin usar deep learning) logre una detección de la persona cuando entra al cuadro suponiendo la utilidad para una cámara de seguridad. 

Dentro de esta carpeta se encuentran notebooks donde se detalla la implementación de los tres métodos:
- Sin deep learning: Utilizando diferencia de frames.
- Sparse Optical Flow, Lucas-Kanade method.
- Dense Optical Flow, Gunnar-Farneback method.

Sin entrar en mucho detalle, podemos sacar conclusiones respecto a los resultados:
- El primer método resultó medianamente satisfactorio: pudo identificar a la persona caminando, sin embargo los bounding boxes no encajaban de manera satisfactoria en la persona, además de que se observan múltiples bounding boxes para la persona. Si bien esto podría ser mejorado mediante modificación de parámetros en el proceso y en la supresión de no máximos, seria poco viable llegar a una solución robusta usando este método. Además hay que agregar el fallo de este método al detectar movimiento donde no lo hay por el cambio natural de los píxeles en las cámaras, cosa que no se puede evitar.
- El segundo método resultaría muy satisfactorio de no ser por un problema crucial: al comenzar el video, no hay ninguna persona en el pasillo. El método de Lucas-Kanade comienza con los frames iniciales detectando features o keypoints de interés. Al no estar presente la persona al comenzar el video, no detecta keypoints en ella, por lo que continúa sin ser reconocida.
- El tercer método parece ser el más satisfactorio: Si bien el modelo parece ser afectado por el ruido natural, este puede ser fácilmente filtrado. Incluso, el modelo puede detectar a la persona utilizando objetos distintos a un bounding box. Dejando de lado el lado positivo de este método, viene con una gran desventaja: el precio de computar los píxeles de manera densa hace a este método muy lento, lo que en ciertas aplicaciones puede hacerlo inviable.

## Ejercicio 6
Consigna: Explique cuál es diferencia entre localización de objetos y clasificación de imágenes. Muestre ejemplos de ello.

La respuesta a esto puede darse sin la necesidad de remitirse a hablar de las tareas de localización de objetos y clasificación de imágenes en específico. Podemos hablar en general de las tareas de localización de features y clasificación o mejor dicho descripción de features. En general, y de forma intuitiva, primero ocurre la detección y luego la descripción en los casos donde ámbas están presentes.
Tomemos como supuesto que estamos dentro del problema de matcheo de features, de esta manera explicamos ambas tareas juntas. 

### Localización de features
Por un lado, tenemos a la tarea de localización. Dado una imagen, esta tarea se encarga de dar con una colección de puntos a nivel de píxel que detallan la ubicación espacial del feature en la imagen. En el caso de querer detectar una región, esto puede variar, por ejemplo se puede dar con el pixel inicial y final de un bounding box. Esta tarea se encarga únicamente de detectar la ubicación del feature, no da información alguna respecto del contexto de ese feature (en la mayoría de los casos)

### Descripción de features
Luego de ser detectado, se necesita describir al pixel para poder luego compararlo con otros features y de esta manera poder establecer algún tipo de correspondencia. Generalmente, al decir describir nos estamos refiriendo a vectorizar, de esta manera se cuenta con un vector que puede ser fácilmente comparado utilizando distancia euclideana o NN (Nearest Neighbors). El descriptor de un feature puede ser computado de forma escasa o densa, la primera corresponde a, luego de localizar un keypoint, calcular su descriptor tomando un fragmento alrededor del píxel; la segunda corresponde a computar el keypoint a lo largo de toda la imagen, lo que puede hacerlo más costoso pero más robusto.

En particular, la clasificación de features se refiere a la tarea de, dada una categorización, entrenar un modelo para poder identificar a cada imagen o cada keypoint con una clase en particular.
En este caso, el cómputo del descriptor es el mismo, lo que cambia es que se definen las clases usando NN (creo).
