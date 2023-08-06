[![Build Status](https://travis-ci.org/avdata99/ckanext-siu-harvester.svg?branch=master)](https://travis-ci.org/avdata99/ckanext-siu-harvester)
[![Docker Pulls](https://img.shields.io/docker/pulls/avdata99/ckan-env.svg)](https://hub.docker.com/r/avdata99/ckan-env/tags)
[![Docker Automated](https://img.shields.io/docker/automated/avdata99/ckan-env.svg)](https://hub.docker.com/r/avdata99/ckan-env/tags)
[![](https://img.shields.io/pypi/implementation/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/pyversions/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/wheel/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/:period/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/format/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/status/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/l/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)
[![](https://img.shields.io/pypi/v/ckanext-siu-harvester)](https://pypi.org/project/ckanext-siu-harvester/)

# SIU Harvester
Esta extensión de CKAN permite cosechar (_harvest_) datos expuestos en sistemas [SIU](https://www.siu.edu.ar/).  
El **Sistema de Información Universitaria** es un [conjunto de aplicaciones](https://www.siu.edu.ar/como-obtengo-los-sistemas/) que permite de manera gratuita a las Universidades argentinas contar con las herramientas de software para su gestión integral.

Esta extensión de CKAN esta pensada para obtener estos datos y publicarlos en formatos reutilizables para darles mayor accesibilidad al público general.

## Portal de transparencia

SIU incluye un [portal de transparencia](http://documentacion.siu.edu.ar/wiki/SIU-Wichi/Version6.6.0/portal_transparencia) que incluye un API.  
Estos datos se toman de la base SIU-Wichi, que contiene datos provenientes de los módulos SIU-Pilaga (Presupuesto), SIU-Mapuche (RRHH), SIU-Diaguita (Compras y Patrimonio) y SIU-Araucano (Académicos).

### Instalacion

Disponible en [Pypi](https://pypi.org/project/ckanext-siu-harvester/) o vía GitHub.  

```
pip install ckanext-siu-harvester
ó
pip install -e git+https://github.com/avdata99/ckanext-siu-harvester.git#egg=ckanext-siu-harvester

+
pip install -r https://raw.githubusercontent.com/avdata99/ckanext-siu-harvester/master/requirements.txt

```

### Agregar origen

La URL los _harvest sources_ de este tipo son de la forma:
```
http://wichi.siu.edu.ar/pentaho/plugin/cda/api/doQuery
```

Debe elegir la URL de la instancia de la que desea obtener datos

### Configuración

Para conectarse es requisito que para cada _harvest source_ definir una configuración.  
Ejemplo:

```json
{
    "username": "user",
    "password": "password"    
}
```

### Datos a extraer

Estos endpoints pueden incluir multiples recursos. Cada recurso es un _query_ al endpoint ya listo para usar.  
Estos ya están configurados en el directorio `ckanext/siu_harvester/harvesters/siu_transp_data/queries/`

Por ejemplo `egresados-pos-facultad.json`

```
{
    "name": "evolucion-de-cargos-activos-por-escalafon",
    "title": "Evolución de cargos activos por escalafón",
    "notes": "",
    "internals": "Describir mejor",
    "iterables": {
        "sub_list": {
            "help": "Necesitamos primero obtener la lista de unidades académicas con otra consulta",
            "name": "lista-de-unidades-academicas",
            "params": {
                "paramprm_tablero_visible": "18",
                "dataAccessId": "param_ua_cargos",
                "sortBy": ""
            },
            "apply_to": "paramprm_ua_cargos"
        }
    },
    "tags": [
        "Cargos", "Personal"
    ],
    "params": {
        "paramprm_ua_cargos": "",
        "path": "/home/SIU-Wichi/Portal Transparencia/cda/4_rrhh.cda",
        "dataAccessId": "tablero_18",
        "outputIndexId": 1,
        "pageSize": 0,
        "pageStart": 0,
        "sortBy": "2D"
        }
}
```

De esta forma este _harvester_ va a iterar por los años disponibles y creará un dataset para cada año.  
Es posible agregar más _queries_ para consumir más datos.

