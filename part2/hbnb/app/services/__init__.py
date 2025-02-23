"""
Package contenant les services de l'application HBnB.
Ce package fournit une façade qui encapsule toute la logique métier
et coordonne les interactions entre les différents composants.
"""

from app.services.facade import HBnBFacade

# Instance globale de la façade, point d'entrée unique pour
# toutes les opérations de l'application
facade = HBnBFacade() 