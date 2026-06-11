# Que es ProxmarkV3 ? 

El ProxmarkV3 es un dispositivo que te permite leer y grabar comunicaciones de radiofrecuencia 13Mhz y 135khz, pudiendo analizar las comunicaciones de los dispositivos que usan estas, NFC y RFID por ejemplo. Esto lo hace atraves del sofware mantenido por la comunidad en github en el [repo](https://github.com/RfidResearchGroup/proxmark3.git), el cual tiene todo tipo de herramientas para explotar al maximo este dispositivo, y poder penetrar la seguridad de este tipo de tecnologias, con sus respectivos limites al hardware.  Esta formado por 3 partes el lector de low frequency 135khz, y el lector high frequency 13Mhz, y el microcontrolador **AT91SAM7S512 (ARM7TDMI, 512KB flash, 64KB RAM)** ,  este chip es mas rapido que el tipico arduino, y es el que se encarga de correr el firmware que controla los lectores y orquesta los ataques. Todo este hardware es de arquitectura abierta de ahi que existan clones chinos. 

# Instalacion

**El proxmark ya lleva un firmware por defecto pero suele estar muy desactualizado, dejando mucho que desear a la hora de realizar ataques, lo mejor es actualizar.** 

La instalacion es bastante simple y se podria resumir en x pasos. Si bien antes de realizar la,  lo mejor es  checkear el **README** del repositorio antes, pues tiene *warnings*. 
Un warning importante es **deshabilitar modemmanager** si vas a actualizar el firmware . **( De no hacerlo podria brickearse por un intento de este servicio de establecer una comunicacion con un modem tipo 4G 3G LTE )**

1.  Lo primero instalar las dependencias : ```
```bash 
sudo apt-get install --no-install-recommends git ca-certificates build-essential pkg-config \	libreadline-dev gcc-arm-none-eabi libnewlib-dev qtbase5-dev \
libbz2-dev liblz4-dev libbluetooth-dev libpython3-dev libssl-dev libgd-dev
```

*Si no usaras scripts de python puedes quitar libpython, si no usaras el cliente grafico 
0	puedes quitar qtbase5, y si no usaras comunicacion por bluetooth puedes quitar 
libbluethoth*

1.  Seguido tocaria clonar el repo:

```bash 
git clone https://github.com/RfidResearchGroup/proxmark3.git && cd proxmark3
```

4.  Luego compilamos, es importante saber que plataforma de proxmark tenemos en mi caso es un clon chino asi que uso el siguiente alias en el platform :

```bash 
make clean &&  make PLATFORM=PM3GENERIC all
```

5.  Ahora hay que conectar el proxmark al pc y verificar el puerto al que esta conectado : 
	```dmesg | grep tty``` *Normalmente /dev/ttyACM0 o /dev/ttyUSB0*
	**Recordemos apagar el modemmanager**

6.  Ejecutar los dos scripts pm3-flash-bootrom   pm3-flash-fullimage. Hay que darle al boton del lateral antes de cada ejecucion para que entre en el modo bootloader. Se encienden las luces del modo bootloader. 
	*El ultimo paso no me funciono a la primera pero si a la segunda cabe destacar que a mi el pm3-flash-all no me funciono.  


# Uso


> Hecho esto la instalacion esta finalizada y podemos iniciar el programa de la proxmax con el script pm3.  ```./pm3 ```

>[!note] Si tienes error de permisos del puerto agregate al grupo   
sudo usermod -aG uucp < user > 

Una vez arrancado el `./pm3` , para usarlo contra una tarjeta mifare classic podemos usar los siguientes comandos:
``` bash
hf mf info
```
esto nos da información muy valiosa, a parte de poder ver que sectores tienen contraseña por defecto, también podemos identificar los que no. también podemos extraer la clave de backdoor que dejan los desarrolladores para poder entrar a la tarjeta en modo debug y poder leer todo, para sacar todas las claves desde el modo debug, podemos ejecutar el script que nos recomienda el propio output del comando anterior:

 hf 15 list
[+] Recorded activity ( 3599 bytes )
[=] start = start of start frame. end = end of frame. src = source of transfer.
[=] ISO15693 / iCLASS - all times are in carrier periods (1/13.56MHz)

      Start |        End | Src | Data (! denotes parity error)                                           | CRC | Annotation
------------+------------+-----+-------------------------------------------------------------------------+-----+--------------------
          0 |      22016 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
 hf 15 list
[+] Recorded activity ( 3599 bytes )
[=] start = start of start frame. end = end of frame. src = source of transfer.
[=] ISO15693 / iCLASS - all times are in carrier periods (1/13.56MHz)

      Start |        End | Src | Data (! denotes parity error)                                           | CRC | Annotation
------------+------------+-----+-------------------------------------------------------------------------+-----+--------------------
          0 |      22016 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
 4294958784 |      13504 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
      17792 |      71040 | Tag |00  02  60  62  60  75  08  01  04  E0  C1  33                           |  ok |
 4294959040 |      42432 | Rdr |22  2B  60  62  60  75  08  01  04  E0  34  02                           |  ok | GET_SYSTEM_INFO
      46720 |     120448 | Tag |00  0F  60  62  60  75  08  01  04  E0  02  00  4F  03  01  93  E5       |  ok |
 4294959104 |      46592 | Rdr |22  AB  04  60  62  60  75  08  01  04  E0  D9  A1                       |  ok | GET_NXP_SYSTEM_INFO
      50880 |      95936 | Tag |00  00  00  00  7F  35  00  00  DC  D4                                   |  ok |
 4294959104 |      46592 | Rdr |22  A5  04  60  62  60  75  08  01  04  E0  22  20                       |  ok | EAS_ALARM
 4294959104 |      46592 | Rdr |22  BD  04  60  62  60  75  08  01  04  E0  59  9B                       |  ok | READ_SIGNATURE
      50880 |     198336 | Tag |00  F6  76  84  F3  D3  92  A9  23  92  73  7A  F5  46  6E  37  24  D7   |     |
            |            |     |1B  EE  F2  8F  C0  25  E2  3D  AA  B5  0C  E3  E3  FB  CF  27  41       |  ok |
 4294958784 |      13504 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
      17792 |      71040 | Tag |00  02  60  62  60  75  08  01  04  E0  C1  33                           |  ok |
 4294959040 |      42432 | Rdr |22  2B  60  62  60  75  08  01  04  E0  34  02                           |  ok | GET_SYSTEM_INFO
      46720 |     120448 | Tag |00  0F  60  62  60  75  08  01  04  E0  02  00  4F  03  01  93  E5       |  ok |
     415232 |     470016 | Rdr |62  20  60  62  60  75  08  01  04  E0  00  98  57                       |  ok | READBLOCK(0)
     474304 |     511168 | Tag |00  00  85  08  69  A1  BA  74                                           |  ok |
     804416 |     859200 | Rdr |62  20  60  62  60  75  08  01  04  E0  01  11  46                       |  ok | READBLOCK(1)
     863424 |     900288 | Tag |00  00  C2  1D  02  01  F3  AD                                           |  ok |
    1193024 |    1247808 | Rdr |62  20  60  62  60  75  08  01  04  E0  02  8A  74                       |  ok | READBLOCK(2)
    1252032 |    1288896 | Tag |00  00  BF  2A  B6  78  DA  C5                                           |  ok |
    1579904 |    1634688 | Rdr |62  20  60  62  60  75  08  01  04  E0  03  03  65                       |  ok | READBLOCK(3)
    1638976 |    1675840 | Tag |00  00  4C  30  50  49  90  FC                                           |  ok |
    1966912 |    2021696 | Rdr |62  20  60  62  60  75  08  01  04  E0  04  BC  11                       |  ok | READBLOCK(4)
    2025920 |    2062784 | Tag |00  00  42  20  53  42  FC  43                                           |  ok |
    2356800 |    2411584 | Rdr |62  20  60  62  60  75  08  01  04  E0  05  35  00                       |  ok | READBLOCK(5)
    2415872 |    2452736 | Tag |00  00  2E  00  4F  43  AF  63                                           |  ok |
    2743744 |    2798528 | Rdr |62  20  60  62  60  75  08  01  04  E0  06  AE  32                       |  ok | READBLOCK(6)
    2802752 |    2839616 | Tag |00  00  4E  00  00  00  7A  4F                                           |  ok |
    3130432 |    3185216 | Rdr |62  20  60  62  60  75  08  01  04  E0  07  27  23                       |  ok | READBLOCK(7)
    3189504 |    3226368 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    3515392 |    3570176 | Rdr |62  20  60  62  60  75  08  01  04  E0  08  D0  DB                       |  ok | READBLOCK(8)
    3574464 |    3611328 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    3900480 |    3955264 | Rdr |62  20  60  62  60  75  08  01  04  E0  09  59  CA                       |  ok | READBLOCK(9)
    3959552 |    3996416 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    4289408 |    4344192 | Rdr |62  20  60  62  60  75  08  01  04  E0  0A  C2  F8                       |  ok | READBLOCK(10)
    4348480 |    4385344 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    4678912 |    4733696 | Rdr |62  20  60  62  60  75  08  01  04  E0  0B  4B  E9                       |  ok | READBLOCK(11)
    4737920 |    4774784 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    5065856 |    5120640 | Rdr |62  20  60  62  60  75  08  01  04  E0  0C  F4  9D                       |  ok | READBLOCK(12)
    5124928 |    5161792 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    5454784 |    5509568 | Rdr |62  20  60  62  60  75  08  01  04  E0  0D  7D  8C                       |  ok | READBLOCK(13)
    5513856 |    5550720 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    5843840 |    5898624 | Rdr |62  20  60  62  60  75  08  01  04  E0  0E  E6  BE                       |  ok | READBLOCK(14)
    5902848 |    5939712 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    6232576 |    6287360 | Rdr |62  20  60  62  60  75  08  01  04  E0  0F  6F  AF                       |  ok | READBLOCK(15)
    6291648 |    6328512 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    6621376 |    6676160 | Rdr |62  20  60  62  60  75  08  01  04  E0  10  19  47                       |  ok | READBLOCK(16)
    6680448 |    6717312 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    7010304 |    7065088 | Rdr |62  20  60  62  60  75  08  01  04  E0  11  90  56                       |  ok | READBLOCK(17)
    7069376 |    7106240 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    7399104 |    7453888 | Rdr |62  20  60  62  60  75  08  01  04  E0  12  0B  64                       |  ok | READBLOCK(18)
    7458176 |    7495040 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    7786944 |    7841728 | Rdr |62  20  60  62  60  75  08  01  04  E0  13  82  75                       |  ok | READBLOCK(19)
    7845952 |    7882816 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    8177280 |    8232064 | Rdr |62  20  60  62  60  75  08  01  04  E0  14  3D  01                       |  ok | READBLOCK(20)
    8236352 |    8273216 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    8564352 |    8619136 | Rdr |62  20  60  62  60  75  08  01  04  E0  15  B4  10                       |  ok | READBLOCK(21)
    8623360 |    8660224 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    8953280 |    9008064 | Rdr |62  20  60  62  60  75  08  01  04  E0  16  2F  22                       |  ok | READBLOCK(22)
    9012352 |    9049216 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    9342272 |    9397056 | Rdr |62  20  60  62  60  75  08  01  04  E0  17  A6  33                       |  ok | READBLOCK(23)
    9401344 |    9438208 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    9731136 |    9785920 | Rdr |62  20  60  62  60  75  08  01  04  E0  18  51  CB                       |  ok | READBLOCK(24)
    9790208 |    9827072 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   10117952 |   10172736 | Rdr |62  20  60  62  60  75  08  01  04  E0  19  D8  DA                       |  ok | READBLOCK(25)
   10177024 |   10213888 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   10506624 |   10561408 | Rdr |62  20  60  62  60  75  08  01  04  E0  1A  43  E8                       |  ok | READBLOCK(26)
   10565696 |   10602560 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   10895616 |   10950400 | Rdr |62  20  60  62  60  75  08  01  04  E0  1B  CA  F9                       |  ok | READBLOCK(27)
   10954688 |   10991552 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   11282368 |   11337152 | Rdr |62  20  60  62  60  75  08  01  04  E0  1C  75  8D                       |  ok | READBLOCK(28)
   11341440 |   11378304 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   11672576 |   11727360 | Rdr |62  20  60  62  60  75  08  01  04  E0  1D  FC  9C                       |  ok | READBLOCK(29)
   11731648 |   11768512 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   12061312 |   12116096 | Rdr |62  20  60  62  60  75  08  01  04  E0  1E  67  AE                       |  ok | READBLOCK(30)
   12120384 |   12157248 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   12450176 |   12504960 | Rdr |62  20  60  62  60  75  08  01  04  E0  1F  EE  BF                       |  ok | READBLOCK(31)
   12509248 |   12546112 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   12838976 |   12893760 | Rdr |62  20  60  62  60  75  08  01  04  E0  20  9A  76                       |  ok | READBLOCK(32)
   12898048 |   12934912 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   13227904 |   13282688 | Rdr |62  20  60  62  60  75  08  01  04  E0  21  13  67                       |  ok | READBLOCK(33)
   13286976 |   13323840 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   13616768 |   13671552 | Rdr |62  20  60  62  60  75  08  01  04  E0  22  88  55                       |  ok | READBLOCK(34)
   13675840 |   13712704 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   14005568 |   14060352 | Rdr |62  20  60  62  60  75  08  01  04  E0  23  01  44                       |  ok | READBLOCK(35)
   14064576 |   14101440 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   14394368 |   14449152 | Rdr |62  20  60  62  60  75  08  01  04  E0  24  BE  30                       |  ok | READBLOCK(36)
   14453376 |   14490240 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   14783296 |   14838080 | Rdr |62  20  60  62  60  75  08  01  04  E0  25  37  21                       |  ok | READBLOCK(37)
   14842368 |   14879232 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   15175168 |   15229952 | Rdr |62  20  60  62  60  75  08  01  04  E0  26  AC  13                       |  ok | READBLOCK(38)
   15234240 |   15271104 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   15564480 |   15619264 | Rdr |62  20  60  62  60  75  08  01  04  E0  27  25  02                       |  ok | READBLOCK(39)
   15623552 |   15660416 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   15953472 |   16008256 | Rdr |62  20  60  62  60  75  08  01  04  E0  28  D2  FA                       |  ok | READBLOCK(40)
   16012480 |   16049344 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   16342336 |   16397120 | Rdr |62  20  60  62  60  75  08  01  04  E0  29  5B  EB                       |  ok | READBLOCK(41)
   16401408 |   16438272 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   16729088 |   16783872 | Rdr |62  20  60  62  60  75  08  01  04  E0  2A  C0  D9                       |  ok | READBLOCK(42)
   16788096 |   16824960 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   17118144 |   17172928 | Rdr |62  20  60  62  60  75  08  01  04  E0  2B  49  C8                       |  ok | READBLOCK(43)
   17177216 |   17214080 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   17507072 |   17561856 | Rdr |62  20  60  62  60  75  08  01  04  E0  2C  F6  BC                       |  ok | READBLOCK(44)
   17566144 |   17603008 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   17895872 |   17950656 | Rdr |62  20  60  62  60  75  08  01  04  E0  2D  7F  AD                       |  ok | READBLOCK(45)
   17954944 |   17991808 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   18283072 |   18337856 | Rdr |62  20  60  62  60  75  08  01  04  E0  2E  E4  9F                       |  ok | READBLOCK(46)
   18342144 |   18379008 | Tag |00  00  00  80  01  00  BB  E2                                           |  ok |
   18672000 |   18726784 | Rdr |62  20  60  62  60  75  08  01  04  E0  2F  6D  8E                       |  ok | READBLOCK(47)
   18731072 |   18767936 | Tag |00  00  00  18  00  20  DA  95                                           |  ok |
   19061056 |   19115840 | Rdr |62  20  60  62  60  75  08  01  04  E0  30  1B  66                       |  ok | READBLOCK(48)
   19120064 |   19156928 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   19450496 |   19505280 | Rdr |62  20  60  62  60  75  08  01  04  E0  31  92  77                       |  ok | READBLOCK(49)
   19509568 |   19546432 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   19840320 |   19895104 | Rdr |62  20  60  62  60  75  08  01  04  E0  32  09  45                       |  ok | READBLOCK(50)
   19899328 |   19936192 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   20227264 |   20282048 | Rdr |62  20  60  62  60  75  08  01  04  E0  33  80  54                       |  ok | READBLOCK(51)
   20286272 |   20323136 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   20616640 |   20671424 | Rdr |62  20  60  62  60  75  08  01  04  E0  34  3F  20                       |  ok | READBLOCK(52)
   20675648 |   20712512 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   21005568 |   21060352 | Rdr |62  20  60  62  60  75  08  01  04  E0  35  B6  31                       |  ok | READBLOCK(53)
   21064640 |   21101504 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   21392384 |   21447168 | Rdr |62  20  60  62  60  75  08  01  04  E0  36  2D  03                       |  ok | READBLOCK(54)
   21451392 |   21488256 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   21781312 |   21836096 | Rdr |62  20  60  62  60  75  08  01  04  E0  37  A4  12                       |  ok | READBLOCK(55)
   21840320 |   21877184 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   22170176 |   22224960 | Rdr |62  20  60  62  60  75  08  01  04  E0  38  53  EA                       |  ok | READBLOCK(56)
   22229248 |   22266112 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   22557120 |   22611904 | Rdr |62  20  60  62  60  75  08  01  04  E0  39  DA  FB                       |  ok | READBLOCK(57)
   22616128 |   22652992 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   22945984 |   23000768 | Rdr |62  20  60  62  60  75  08  01  04  E0  3A  41  C9                       |  ok | READBLOCK(58)
   23005056 |   23041920 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   23335424 |   23390208 | Rdr |62  20  60  62  60  75  08  01  04  E0  3B  C8  D8                       |  ok | READBLOCK(59)
   23394432 |   23431296 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   23724288 |   23779072 | Rdr |62  20  60  62  60  75  08  01  04  E0  3C  77  AC                       |  ok | READBLOCK(60)
   23783296 |   23820160 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   24113216 |   24168000 | Rdr |62  20  60  62  60  75  08  01  04  E0  3D  FE  BD                       |  ok | READBLOCK(61)
   24172288 |   24209152 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   24501952 |   24556736 | Rdr |62  20  60  62  60  75  08  01  04  E0  3E  65  8F                       |  ok | READBLOCK(62)
   24561024 |   24597888 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   24888832 |   24943616 | Rdr |62  20  60  62  60  75  08  01  04  E0  3F  EC  9E                       |  ok | READBLOCK(63)
   24947840 |   24984704 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   25277888 |   25332672 | Rdr |62  20  60  62  60  75  08  01  04  E0  40  9C  15                       |  ok | READBLOCK(64)
   25336960 |   25373824 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   25664768 |   25719552 | Rdr |62  20  60  62  60  75  08  01  04  E0  41  15  04                       |  ok | READBLOCK(65)
   25723776 |   25760640 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   26052160 |   26106944 | Rdr |62  20  60  62  60  75  08  01  04  E0  42  8E  36                       |  ok | READBLOCK(66)
   26111232 |   26148096 | Tag |00  00  02  D2  4F  02  F2  12                                           |  ok |
   26438976 |   26493760 | Rdr |62  20  60  62  60  75  08  01  04  E0  43  07  27                       |  ok | READBLOCK(67)
   26497984 |   26534848 | Tag |00  00  F0  B6  E4  C5  67  C3                                           |  ok |
   26825792 |   26880576 | Rdr |62  20  60  62  60  75  08  01  04  E0  44  B8  53                       |  ok | READBLOCK(68)
   26884800 |   26921664 | Tag |00  00  BC  57  DD  0D  67  3A                                           |  ok |
   27212544 |   27267328 | Rdr |62  20  60  62  60  75  08  01  04  E0  45  31  42                       |  ok | READBLOCK(69)
   27271552 |   27308416 | Tag |00  00  20  BD  22  7E  9B  87                                           |  ok |
   27601536 |   27656320 | Rdr |62  20  60  62  60  75  08  01  04  E0  46  AA  70                       |  ok | READBLOCK(70)
   27660544 |   27697408 | Tag |00  00  B2  56  5D  96  6F  68                                           |  ok |
   27990336 |   28045120 | Rdr |62  20  60  62  60  75  08  01  04  E0  47  23  61                       |  ok | READBLOCK(71)
   28049408 |   28086272 | Tag |00  00  A1  11  AF  37  4B  FF                                           |  ok |
   28377024 |   28431808 | Rdr |62  20  60  62  60  75  08  01  04  E0  48  D4  99                       |  ok | READBLOCK(72)
   28436032 |   28472896 | Tag |00  00  FC  11  AF  37  D2  A1                                           |  ok |
   28764160 |   28818944 | Rdr |62  20  60  62  60  75  08  01  04  E0  49  5D  88                       |  ok | READBLOCK(73)
   28823168 |   28860032 | Tag |00  00  FC  11  AF  37  D2  A1                                           |  ok |
   29150976 |   29205760 | Rdr |62  20  60  62  60  75  08  01  04  E0  4A  C6  BA                       |  ok | READBLOCK(74)
   29210048 |   29246912 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   29537856 |   29592640 | Rdr |62  20  60  62  60  75  08  01  04  E0  4B  4F  AB                       |  ok | READBLOCK(75)
   29596928 |   29633792 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   29924608 |   29979392 | Rdr |62  20  60  62  60  75  08  01  04  E0  4C  F0  DF                       |  ok | READBLOCK(76)
   29983616 |   30020480 | Tag |00  00  41  88  2F  00  56  97                                           |  ok |
   30311360 |   30366144 | Rdr |62  20  60  62  60  75  08  01  04  E0  4D  79  CE                       |  ok | READBLOCK(77)
   30370432 |   30407296 | Tag |00  00  00  24  48  82  69  B8                                           |  ok |
   30698240 |   30753024 | Rdr |62  20  60  62  60  75  08  01  04  E0  4E  E2  FC                       |  ok | READBLOCK(78)
   30757312 |   30794176 | Tag |00  00  27  CB  11  00  88  80                                           |  ok |
   31085056 |   31139840 | Rdr |62  20  60  62  60  75  08  01  04  E0  4F  6B  ED                       |  ok | READBLOCK(79)
   31144128 |   31180992 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
 4294958784 |      13504 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
      17792 |      71040 | Tag |00  02  60  62  60  75  08  01  04  E0  C1  33                           |  ok |
 4294959104 |      46592 | Rdr |62  20  60  62  60  75  08  01  04  E0  00  98  57                       |  ok | READBLOCK(0)
      50880 |      87744 | Tag |00  00  85  08  69  A1  BA  74                                           |  ok |
[usb] pm3 -->      17792 |      71040 | Tag |00  02  60  62  60  75  08  01  04  E0  C1  33                           |  ok |
 4294959040 |      42432 | Rdr |22  2B  60  62  60  75  08  01  04  E0  34  02                           |  ok | GET_SYSTEM_INFO
      46720 |     120448 | Tag |00  0F  60  62  60  75  08  01  04  E0  02  00  4F  03  01  93  E5       |  ok |
 4294959104 |      46592 | Rdr |22  AB  04  60  62  60  75  08  01  04  E0  D9  A1                       |  ok | GET_NXP_SYSTEM_INFO
      50880 |      95936 | Tag |00  00  00  00  7F  35  00  00  DC  D4                                   |  ok |
 4294959104 |      46592 | Rdr |22  A5  04  60  62  60  75  08  01  04  E0  22  20                       |  ok | EAS_ALARM
 4294959104 |      46592 | Rdr |22  BD  04  60  62  60  75  08  01  04  E0  59  9B                       |  ok | READ_SIGNATURE
      50880 |     198336 | Tag |00  F6  76  84  F3  D3  92  A9  23  92  73  7A  F5  46  6E  37  24  D7   |     |
            |            |     |1B  EE  F2  8F  C0  25  E2  3D  AA  B5  0C  E3  E3  FB  CF  27  41       |  ok |
 4294958784 |      13504 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
      17792 |      71040 | Tag |00  02  60  62  60  75  08  01  04  E0  C1  33                           |  ok |
 4294959040 |      42432 | Rdr |22  2B  60  62  60  75  08  01  04  E0  34  02                           |  ok | GET_SYSTEM_INFO
      46720 |     120448 | Tag |00  0F  60  62  60  75  08  01  04  E0  02  00  4F  03  01  93  E5       |  ok |
     415232 |     470016 | Rdr |62  20  60  62  60  75  08  01  04  E0  00  98  57                       |  ok | READBLOCK(0)
     474304 |     511168 | Tag |00  00  85  08  69  A1  BA  74                                           |  ok |
     804416 |     859200 | Rdr |62  20  60  62  60  75  08  01  04  E0  01  11  46                       |  ok | READBLOCK(1)
     863424 |     900288 | Tag |00  00  C2  1D  02  01  F3  AD                                           |  ok |
    1193024 |    1247808 | Rdr |62  20  60  62  60  75  08  01  04  E0  02  8A  74                       |  ok | READBLOCK(2)
    1252032 |    1288896 | Tag |00  00  BF  2A  B6  78  DA  C5                                           |  ok |
    1579904 |    1634688 | Rdr |62  20  60  62  60  75  08  01  04  E0  03  03  65                       |  ok | READBLOCK(3)
    1638976 |    1675840 | Tag |00  00  4C  30  50  49  90  FC                                           |  ok |
    1966912 |    2021696 | Rdr |62  20  60  62  60  75  08  01  04  E0  04  BC  11                       |  ok | READBLOCK(4)
    2025920 |    2062784 | Tag |00  00  42  20  53  42  FC  43                                           |  ok |
    2356800 |    2411584 | Rdr |62  20  60  62  60  75  08  01  04  E0  05  35  00                       |  ok | READBLOCK(5)
    2415872 |    2452736 | Tag |00  00  2E  00  4F  43  AF  63                                           |  ok |
    2743744 |    2798528 | Rdr |62  20  60  62  60  75  08  01  04  E0  06  AE  32                       |  ok | READBLOCK(6)
    2802752 |    2839616 | Tag |00  00  4E  00  00  00  7A  4F                                           |  ok |
    3130432 |    3185216 | Rdr |62  20  60  62  60  75  08  01  04  E0  07  27  23                       |  ok | READBLOCK(7)
    3189504 |    3226368 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    3515392 |    3570176 | Rdr |62  20  60  62  60  75  08  01  04  E0  08  D0  DB                       |  ok | READBLOCK(8)
    3574464 |    3611328 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    3900480 |    3955264 | Rdr |62  20  60  62  60  75  08  01  04  E0  09  59  CA                       |  ok | READBLOCK(9)
    3959552 |    3996416 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    4289408 |    4344192 | Rdr |62  20  60  62  60  75  08  01  04  E0  0A  C2  F8                       |  ok | READBLOCK(10)
    4348480 |    4385344 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    4678912 |    4733696 | Rdr |62  20  60  62  60  75  08  01  04  E0  0B  4B  E9                       |  ok | READBLOCK(11)
    4737920 |    4774784 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    5065856 |    5120640 | Rdr |62  20  60  62  60  75  08  01  04  E0  0C  F4  9D                       |  ok | READBLOCK(12)
    5124928 |    5161792 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    5454784 |    5509568 | Rdr |62  20  60  62  60  75  08  01  04  E0  0D  7D  8C                       |  ok | READBLOCK(13)
    5513856 |    5550720 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    5843840 |    5898624 | Rdr |62  20  60  62  60  75  08  01  04  E0  0E  E6  BE                       |  ok | READBLOCK(14)
    5902848 |    5939712 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    6232576 |    6287360 | Rdr |62  20  60  62  60  75  08  01  04  E0  0F  6F  AF                       |  ok | READBLOCK(15)
    6291648 |    6328512 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    6621376 |    6676160 | Rdr |62  20  60  62  60  75  08  01  04  E0  10  19  47                       |  ok | READBLOCK(16)
    6680448 |    6717312 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    7010304 |    7065088 | Rdr |62  20  60  62  60  75  08  01  04  E0  11  90  56                       |  ok | READBLOCK(17)
    7069376 |    7106240 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    7399104 |    7453888 | Rdr |62  20  60  62  60  75  08  01  04  E0  12  0B  64                       |  ok | READBLOCK(18)
    7458176 |    7495040 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    7786944 |    7841728 | Rdr |62  20  60  62  60  75  08  01  04  E0  13  82  75                       |  ok | READBLOCK(19)
    7845952 |    7882816 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    8177280 |    8232064 | Rdr |62  20  60  62  60  75  08  01  04  E0  14  3D  01                       |  ok | READBLOCK(20)
    8236352 |    8273216 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    8564352 |    8619136 | Rdr |62  20  60  62  60  75  08  01  04  E0  15  B4  10                       |  ok | READBLOCK(21)
    8623360 |    8660224 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    8953280 |    9008064 | Rdr |62  20  60  62  60  75  08  01  04  E0  16  2F  22                       |  ok | READBLOCK(22)
    9012352 |    9049216 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    9342272 |    9397056 | Rdr |62  20  60  62  60  75  08  01  04  E0  17  A6  33                       |  ok | READBLOCK(23)
    9401344 |    9438208 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
    9731136 |    9785920 | Rdr |62  20  60  62  60  75  08  01  04  E0  18  51  CB                       |  ok | READBLOCK(24)
    9790208 |    9827072 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   10117952 |   10172736 | Rdr |62  20  60  62  60  75  08  01  04  E0  19  D8  DA                       |  ok | READBLOCK(25)
   10177024 |   10213888 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   10506624 |   10561408 | Rdr |62  20  60  62  60  75  08  01  04  E0  1A  43  E8                       |  ok | READBLOCK(26)
   10565696 |   10602560 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   10895616 |   10950400 | Rdr |62  20  60  62  60  75  08  01  04  E0  1B  CA  F9                       |  ok | READBLOCK(27)
   10954688 |   10991552 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   11282368 |   11337152 | Rdr |62  20  60  62  60  75  08  01  04  E0  1C  75  8D                       |  ok | READBLOCK(28)
   11341440 |   11378304 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   11672576 |   11727360 | Rdr |62  20  60  62  60  75  08  01  04  E0  1D  FC  9C                       |  ok | READBLOCK(29)
   11731648 |   11768512 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   12061312 |   12116096 | Rdr |62  20  60  62  60  75  08  01  04  E0  1E  67  AE                       |  ok | READBLOCK(30)
   12120384 |   12157248 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   12450176 |   12504960 | Rdr |62  20  60  62  60  75  08  01  04  E0  1F  EE  BF                       |  ok | READBLOCK(31)
   12509248 |   12546112 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   12838976 |   12893760 | Rdr |62  20  60  62  60  75  08  01  04  E0  20  9A  76                       |  ok | READBLOCK(32)
   12898048 |   12934912 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   13227904 |   13282688 | Rdr |62  20  60  62  60  75  08  01  04  E0  21  13  67                       |  ok | READBLOCK(33)
   13286976 |   13323840 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   13616768 |   13671552 | Rdr |62  20  60  62  60  75  08  01  04  E0  22  88  55                       |  ok | READBLOCK(34)
   13675840 |   13712704 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   14005568 |   14060352 | Rdr |62  20  60  62  60  75  08  01  04  E0  23  01  44                       |  ok | READBLOCK(35)
   14064576 |   14101440 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   14394368 |   14449152 | Rdr |62  20  60  62  60  75  08  01  04  E0  24  BE  30                       |  ok | READBLOCK(36)
   14453376 |   14490240 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   14783296 |   14838080 | Rdr |62  20  60  62  60  75  08  01  04  E0  25  37  21                       |  ok | READBLOCK(37)
   14842368 |   14879232 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   15175168 |   15229952 | Rdr |62  20  60  62  60  75  08  01  04  E0  26  AC  13                       |  ok | READBLOCK(38)
   15234240 |   15271104 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   15564480 |   15619264 | Rdr |62  20  60  62  60  75  08  01  04  E0  27  25  02                       |  ok | READBLOCK(39)
   15623552 |   15660416 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   15953472 |   16008256 | Rdr |62  20  60  62  60  75  08  01  04  E0  28  D2  FA                       |  ok | READBLOCK(40)
   16012480 |   16049344 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   16342336 |   16397120 | Rdr |62  20  60  62  60  75  08  01  04  E0  29  5B  EB                       |  ok | READBLOCK(41)
   16401408 |   16438272 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   16729088 |   16783872 | Rdr |62  20  60  62  60  75  08  01  04  E0  2A  C0  D9                       |  ok | READBLOCK(42)
   16788096 |   16824960 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   17118144 |   17172928 | Rdr |62  20  60  62  60  75  08  01  04  E0  2B  49  C8                       |  ok | READBLOCK(43)
   17177216 |   17214080 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   17507072 |   17561856 | Rdr |62  20  60  62  60  75  08  01  04  E0  2C  F6  BC                       |  ok | READBLOCK(44)
   17566144 |   17603008 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   17895872 |   17950656 | Rdr |62  20  60  62  60  75  08  01  04  E0  2D  7F  AD                       |  ok | READBLOCK(45)
   17954944 |   17991808 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   18283072 |   18337856 | Rdr |62  20  60  62  60  75  08  01  04  E0  2E  E4  9F                       |  ok | READBLOCK(46)
   18342144 |   18379008 | Tag |00  00  00  80  01  00  BB  E2                                           |  ok |
   18672000 |   18726784 | Rdr |62  20  60  62  60  75  08  01  04  E0  2F  6D  8E                       |  ok | READBLOCK(47)
   18731072 |   18767936 | Tag |00  00  00  18  00  20  DA  95                                           |  ok |
   19061056 |   19115840 | Rdr |62  20  60  62  60  75  08  01  04  E0  30  1B  66                       |  ok | READBLOCK(48)
   19120064 |   19156928 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   19450496 |   19505280 | Rdr |62  20  60  62  60  75  08  01  04  E0  31  92  77                       |  ok | READBLOCK(49)
   19509568 |   19546432 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   19840320 |   19895104 | Rdr |62  20  60  62  60  75  08  01  04  E0  32  09  45                       |  ok | READBLOCK(50)
   19899328 |   19936192 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   20227264 |   20282048 | Rdr |62  20  60  62  60  75  08  01  04  E0  33  80  54                       |  ok | READBLOCK(51)
   20286272 |   20323136 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   20616640 |   20671424 | Rdr |62  20  60  62  60  75  08  01  04  E0  34  3F  20                       |  ok | READBLOCK(52)
   20675648 |   20712512 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   21005568 |   21060352 | Rdr |62  20  60  62  60  75  08  01  04  E0  35  B6  31                       |  ok | READBLOCK(53)
   21064640 |   21101504 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   21392384 |   21447168 | Rdr |62  20  60  62  60  75  08  01  04  E0  36  2D  03                       |  ok | READBLOCK(54)
   21451392 |   21488256 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   21781312 |   21836096 | Rdr |62  20  60  62  60  75  08  01  04  E0  37  A4  12                       |  ok | READBLOCK(55)
   21840320 |   21877184 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   22170176 |   22224960 | Rdr |62  20  60  62  60  75  08  01  04  E0  38  53  EA                       |  ok | READBLOCK(56)
   22229248 |   22266112 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   22557120 |   22611904 | Rdr |62  20  60  62  60  75  08  01  04  E0  39  DA  FB                       |  ok | READBLOCK(57)
   22616128 |   22652992 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   22945984 |   23000768 | Rdr |62  20  60  62  60  75  08  01  04  E0  3A  41  C9                       |  ok | READBLOCK(58)
   23005056 |   23041920 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   23335424 |   23390208 | Rdr |62  20  60  62  60  75  08  01  04  E0  3B  C8  D8                       |  ok | READBLOCK(59)
   23394432 |   23431296 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   23724288 |   23779072 | Rdr |62  20  60  62  60  75  08  01  04  E0  3C  77  AC                       |  ok | READBLOCK(60)
   23783296 |   23820160 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   24113216 |   24168000 | Rdr |62  20  60  62  60  75  08  01  04  E0  3D  FE  BD                       |  ok | READBLOCK(61)
   24172288 |   24209152 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   24501952 |   24556736 | Rdr |62  20  60  62  60  75  08  01  04  E0  3E  65  8F                       |  ok | READBLOCK(62)
   24561024 |   24597888 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   24888832 |   24943616 | Rdr |62  20  60  62  60  75  08  01  04  E0  3F  EC  9E                       |  ok | READBLOCK(63)
   24947840 |   24984704 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   25277888 |   25332672 | Rdr |62  20  60  62  60  75  08  01  04  E0  40  9C  15                       |  ok | READBLOCK(64)
   25336960 |   25373824 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   25664768 |   25719552 | Rdr |62  20  60  62  60  75  08  01  04  E0  41  15  04                       |  ok | READBLOCK(65)
   25723776 |   25760640 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   26052160 |   26106944 | Rdr |62  20  60  62  60  75  08  01  04  E0  42  8E  36                       |  ok | READBLOCK(66)
   26111232 |   26148096 | Tag |00  00  02  D2  4F  02  F2  12                                           |  ok |
   26438976 |   26493760 | Rdr |62  20  60  62  60  75  08  01  04  E0  43  07  27                       |  ok | READBLOCK(67)
   26497984 |   26534848 | Tag |00  00  F0  B6  E4  C5  67  C3                                           |  ok |
   26825792 |   26880576 | Rdr |62  20  60  62  60  75  08  01  04  E0  44  B8  53                       |  ok | READBLOCK(68)
   26884800 |   26921664 | Tag |00  00  BC  57  DD  0D  67  3A                                           |  ok |
   27212544 |   27267328 | Rdr |62  20  60  62  60  75  08  01  04  E0  45  31  42                       |  ok | READBLOCK(69)
   27271552 |   27308416 | Tag |00  00  20  BD  22  7E  9B  87                                           |  ok |
   27601536 |   27656320 | Rdr |62  20  60  62  60  75  08  01  04  E0  46  AA  70                       |  ok | READBLOCK(70)
   27660544 |   27697408 | Tag |00  00  B2  56  5D  96  6F  68                                           |  ok |
   27990336 |   28045120 | Rdr |62  20  60  62  60  75  08  01  04  E0  47  23  61                       |  ok | READBLOCK(71)
   28049408 |   28086272 | Tag |00  00  A1  11  AF  37  4B  FF                                           |  ok |
   28377024 |   28431808 | Rdr |62  20  60  62  60  75  08  01  04  E0  48  D4  99                       |  ok | READBLOCK(72)
   28436032 |   28472896 | Tag |00  00  FC  11  AF  37  D2  A1                                           |  ok |
   28764160 |   28818944 | Rdr |62  20  60  62  60  75  08  01  04  E0  49  5D  88                       |  ok | READBLOCK(73)
   28823168 |   28860032 | Tag |00  00  FC  11  AF  37  D2  A1                                           |  ok |
   29150976 |   29205760 | Rdr |62  20  60  62  60  75  08  01  04  E0  4A  C6  BA                       |  ok | READBLOCK(74)
   29210048 |   29246912 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   29537856 |   29592640 | Rdr |62  20  60  62  60  75  08  01  04  E0  4B  4F  AB                       |  ok | READBLOCK(75)
   29596928 |   29633792 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
   29924608 |   29979392 | Rdr |62  20  60  62  60  75  08  01  04  E0  4C  F0  DF                       |  ok | READBLOCK(76)
   29983616 |   30020480 | Tag |00  00  41  88  2F  00  56  97                                           |  ok |
   30311360 |   30366144 | Rdr |62  20  60  62  60  75  08  01  04  E0  4D  79  CE                       |  ok | READBLOCK(77)
   30370432 |   30407296 | Tag |00  00  00  24  48  82  69  B8                                           |  ok |
   30698240 |   30753024 | Rdr |62  20  60  62  60  75  08  01  04  E0  4E  E2  FC                       |  ok | READBLOCK(78)
   30757312 |   30794176 | Tag |00  00  27  CB  11  00  88  80                                           |  ok |
   31085056 |   31139840 | Rdr |62  20  60  62  60  75  08  01  04  E0  4F  6B  ED                       |  ok | READBLOCK(79)
   31144128 |   31180992 | Tag |00  00  00  00  00  00  8F  F7                                           |  ok |
 4294958784 |      13504 | Rdr |26  01  00  F6  0A                                                       |  ok | INVENTORY
      17792 |      71040 | Tag |00  02  60  62  60  75  08  01  04  E0  C1  33                           |  ok |
 4294959104 |      46592 | Rdr |62  20  60  62  60  75  08  01  04  E0  00  98  57                       |  ok | READBLOCK(0)
      50880 |      87744 | Tag |00  00  85  08  69  A1  BA  74                                           |  ok |
[usb] pm3 -->``` bash
[=] --- ISO14443-a Information -----------------------------  
[+]  UID: 35 EC 8A B4    
[+] ATQA: 00 04  
[+]  SAK: 08 [1]  
  
[=] --- Keys Information  
[+] loaded 2 user keys  
[+] loaded 61 hardcoded keys  
[+] Sector 0 key A... FFFFFFFFFFFF  
[+] Sector 0 key B... FFFFFFFFFFFF  
[+] Sector 1 key A... FFFFFFFFFFFF  
[+] Sector 1 key B... FFFFFFFFFFFF  
[+] Backdoor key..... A396EFA4E24F  
[+] Block 0.......... 35EC8AB4E7080400041674BE015D8090 | ..t..]..  
  
[=] --- Fingerprint  
[+] Fudan FM11RF08S 0490  
  
[=] --- Magic Tag Information  
[=] <n/a>  
  
[=] --- PRNG Information  
[+] Prng....... weak  
[+] Static enc nonce... yes  
[?] Hint: Try `script run fm11rf08s_recovery.py`
```
como podemos ver, el comando `script run fm11rf08s_recovery.py` nos extrae las contraseñas a traves del modo backdoor/recovery:
``` bash
[+] -----+-----+--------------+---+--------------+----  
[+]  Sec | Blk | key A        |res| key B        |res  
[+] -----+-----+--------------+---+--------------+----  
[+]  000 | 003 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  001 | 007 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  002 | 011 | 6C9127BEF580 | 1 | 6C9127BEF580 | 1    
[+]  003 | 015 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  004 | 019 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  005 | 023 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  006 | 027 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  007 | 031 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  008 | 035 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  009 | 039 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  010 | 043 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  011 | 047 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  012 | 051 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  013 | 055 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  014 | 059 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  015 | 063 | FFFFFFFFFFFF | 1 | FFFFFFFFFFFF | 1    
[+]  032 | 131 | AF55E2B254C9 | 1 | 0000563B602F | 1    
[+] -----+-----+--------------+---+--------------+----
```
ademas, a parte de este output, también se nos informa de que hay un dumpeo de los datos en binario, el cual podemos codificar en ASCII o cualquier text encoding para poder leer los datos.
