# Ejercicio 8
En el archivo dog_walking_oclussion.mp4 dentro de la carpeta se encuentra un video de un perro donde en momentos se muestra parcialmente obstruído. 

## Modelos a utilizar
Dentro del siguiente colab:

https://colab.research.google.com/drive/1J3fuUyjCkzP4D278gkagkIFKwZLqkCoT


se encuentran instrucciones para poder utilizar la arquitectura YOLOv8 entrenada sobre el dataset COCO para poder realizar la tarea de detección de objetos sobre la clase perro. Esto lo hace posible el dataset COCO al incluir la clase perro entre sus categorías.

Se realizaron modificaciones sobre este colab, las cuales pueden ser vistas en este colab:

https://colab.research.google.com/drive/105nYEeLi8r0wpn3HBznKmiAdBiwyuVdV

Entre las modificaciones, se encuentra la modificación en el código que hace que solo los bounding boxes correspondientes a los perros sean dibujados, dejando afuera todo lo demás. 

## Conflictos
Se intentó también utilizar DeepSORT, sin embargo debido a errores en las dependencias no fue posible hacerlo funcionar. El colab incluye otras cosas interesantes como contadores.


