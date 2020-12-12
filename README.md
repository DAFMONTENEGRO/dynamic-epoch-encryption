# dynamic-epoch-encryption
El proyecto consiste en un encriptador dinámico el cual utiliza el pequeño teorema de Fermat tanto para cifrar como para descifrar un cierto mensaje por medio de cada uno de sus caracteres. Esto se hace descomponiendo el resultado ASCII del carácter en una suma de n enteros y a su vez creando una llave de n números primos generada a través del Epoch Time del computador. Dichos elementos se combinan uno a uno utilizando el teorema antes mencionado, un valor de verificación obtenido a raíz de la llave y un paso dinámico establecido por el usuario. Esto permite que para cada mensaje se cree una encriptación distinta, incluso variando en caracteres repetidos del mismo mensaje.

# Proyecto Matemáticas Discretas 2

- Daniel Felipe Montenegro Herrera

- Juan Sebastián Piñerez Quintero

## 1. Introducción

En el mundo moderno existen muchas alternativas de encriptación a nivel de algoritmos, sin embargo, muchas de estas existen hace años y aun se cree que son efectivas debido a las limitaciones computacionales al momento de desencriptar estos algoritmos [1]. Esto no deja de ser cierto, pero al haber sido públicos durante tanto tiempo, muchos individuos descubrieron que se podían “romper” estas limitaciones creando de forma colaborativa mecanismos como diccionarios de encriptación que a día de hoy se encuentran públicos en la red [2].

Esta problemática ha sido abordada anteriormente por trabajos como los de Pastor [3] donde se propone un método de encriptación de mensajes dinámico basados en características tales como la fecha, hora, entre otros.

## 2. Materiales y métodos

### 2.1. Datos utilizados

#### 2.1.1. ASCII:

Para el proyecto se decidió hacer uso de mensajes codificados con código ASCII, para obtener la facilidad de trabajar con números representativos de cada carácter. Este es un código de caracteres que asigna un número en el rango de 7 bits a cada determinado carácter, u 8 bits para versiones extendidas (como la usada en este caso) [4].

#### 2.1.2. Epoch time:

Uno de los principales objetivos a la hora de dar solución a este proyecto, fue el de generar la encriptación de los datos de forma dinámica. Para ello se optó por utilizar un factor que varía constantemente, el tiempo. En los sistemas digitales utilizados actualmente se sigue el estándar de tiempo conocido como Epoch time, también llamado Unix time; este es un sistema para describir un punto en el tiempo, y se lleva contando desde el 1 de Enero de 1970 [5]. La precisión de dicha magnitud se limita a la precisión de python para mostrar decimales. La forma en la que se usó epoch time, fue para hallar números primos. Esto se realizó en base a la búsqueda en un cierto intervalo de decimales, lo que permitía obtener números primos esencialmente "aleatorios", que nos servirán posteriormente para crear las llaves de encriptado/desencriptado.

### 2.2. Descripción matemática de los métodos

#### 2.2.1. Pequeño teorema de Fermat [6]

El principio del pequeño teorema de Fermat fue usado en el algoritmo con el fin de hallar el inverso multiplicativo de un cierto número bajo operación modular. Esto se quiere ya que los caracteres se encriptarán bajo cierto función que utiliza el módulo, por lo tanto a la hora de descifrar dicho mensaje se requiere de la función inversa a la inicialmente planteada.

Este nos dice que:

a^(p-1) ≡ 1 (mod p)

siendo a y p coprimos, lo que se tiene para todo a>0 si p es primo.

De la anterior afirmación, multiplicando a ambos lados por a^(-1) se puede derivar que:

a^(-1) = a^(p-2) (mod p) = x

Donde x es el inverso multiplicativo de a (mod p)

Por lo tanto, al plantear la ecuación de encriptado:

E(n) = a*n (mod p) = c

Su función inversa, o de desencriptado, está dada por:

D(c) = x*c (mod p)

### 2.3. Algoritmos
Revisar archivo “PMD2.py”

### 2.4. Configuración experimental

(zona demarcada en el código)

NOTA IMPORTANTE: Para que los algoritmos funcionen correctamente es necesario ejecutar el entorno de desarrollo con una versión de Python superior a la 3.8 [7].


## 3. Resultados

Los resultados del proyecto fueron satisfactorios. Como se puede verificar en el apartado de configuración experimental, el programa desarrollado permite ingresar un cierto mensaje de texto y hacerle la encriptación, así como el correspondiente desencriptado.

Se obtuvo que el programa encripta de forma dinámica, en base al "epoch time", esto quiere decir que un mismo mensaje encriptado en dos momentos distintos, serán diferentes en su forma cifrada. Un detalle a resaltar es que incluso si el mensaje contiene letras o dígitos iguales, en el mensaje encriptado no se tendrán elementos iguales que permitan reconocer que tales elementos hacen referencia a un mismo carácter.

## 4. Conclusiones

Una de las mayores dificultades a la hora de abarcar la solución del problema planteado, fue el de definir un sistema para el que fuese esencial la encriptación, para dar un uso correcto a las llaves privadas y públicas, sin embargo este área de conocimiento es bastante extenso, por lo que se optó por crear un cifrador dinámico que no tenga en cuenta tales elementos pertinentes al sistema que lo use como tal.

Finalmente, se alcanzó el objetivo, y a su vez se obtuvo que el desarrollo de un cifrador/descifrador es un trabajo complejo, que requiere no únicamente conocimientos de programación, sino también ciertos fundamentos en el área matemática, al menos si lo que se quiere es conseguir un programa verdaderamente funcional.

## 5. Referencias

[1] Criptografia. Tomado de: https://es.wikipedia.org/wiki/Cifrado_(criptograf%C3%ADa)

[2] Diccionario MD5. Tomado de: https://md5online.es/

[3] Propuesta de un Método Alternativo de Encriptación Dinámica para un Administrador de Correo Electrónico. Pastor, D. Tomado de: http://dspace.espoch.edu.ec/handle/123456789/4223

[4]. ASCII. Tomado de: https://es.wikipedia.org/wiki/ASCII

[5]. Unix time. Tomado de: https://en.wikipedia.org/wiki/Unix_time

[6]. Inverso aditivo, inverso xor, inverso multiplicativo. Ramió, J. 2020. Obtenido de: http://www.criptored.upm.es/descarga/Class4cryptc4c2.3_Inversos_aditivo_xor_multiplicativo.pdf

[7] Pow() Python. Tomado de: https://docs.python.org/3/library/functions.html#pow
