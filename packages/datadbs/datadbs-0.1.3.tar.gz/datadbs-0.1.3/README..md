DataDBS
======

Este módulo provee la estructura básica para gestionar datos y llevar registro de eventos

Instalar

pip install datadbs

Cómo se usa
==========

Hereda tu clase de

from datadabs import Generaldata


Class Nueva(GaneralData):
	pass


Necesitarás entregar datos de conexion (code, host, port) y te provee accesso al elemento 'logger'
para registrar eventos.
