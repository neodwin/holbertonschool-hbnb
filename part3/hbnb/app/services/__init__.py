#!/usr/bin/env python3
"""
Module d'initialisation des services de l'application HolbertonBnB.
Ce fichier crée une instance globale de la façade qui centralise l'accès aux fonctionnalités.
La façade est rendue disponible pour tous les modules qui importent 'app.services'.
"""

from app.services.facade import HBnBFacade

# Création d'une instance unique de la façade pour toute l'application
# Cela permet d'accéder aux services depuis n'importe quel point de l'application
# sans avoir à créer une nouvelle instance à chaque fois
facade = HBnBFacade() 