#!/usr/bin/env python3

import numpy as np
from math import sin, cos


def rotx(alpha):
    """
    Creare una matrice di rotazione numpy 3x3 intorno all'asse x

    Le tre colonne rappresentano i nuovi vettori base nel sistema di coordinate globale di un sistema di coordinate
    ruotato da questa matrice.

    Args:
        alpha: angolo di rotazione in radianti

    Restituisce:
        La matrice di rotazione 3D intorno all'asse x

    """

    rotxM = np.array([[1, 0, 0],
                      [0, cos(alpha), -sin(alpha)],
                      [0, sin(alpha), cos(alpha)]])

    return rotxM


def roty(beta):
    """
    Creare una matrice di rotazione numpy 3x3 intorno all'asse y

    Le tre colonne rappresentano i nuovi vettori base nel sistema di coordinate globale di un sistema di coordinate
    ruotato da questa matrice.

    Args:
        beta: angolo di rotazione in radianti

    Restituisce:
        La matrice di rotazione 3D intorno all'asse y

    """

    rotyM = np.array([[cos(beta), 0, sin(beta)],
                      [0, 1, 0],
                      [-sin(beta), 0, cos(beta)]])

    return rotyM


def rotz(gamma):
    """
    Creare una matrice di rotazione numpy 3x3 intorno all'asse z

    Le tre colonne rappresentano i nuovi vettori base nel sistema di coordinate globale di un sistema di coordinate
    ruotato da questa matrice.

    Args:
        gamma: angolo di rotazione in radianti

    Restituisce:
        La matrice di rotazione 3D intorno all'asse z

    """

    rotzM = np.array([[cos(gamma), -sin(gamma), 0],
                      [sin(gamma), cos(gamma), 0],
                      [0, 0, 1]])

    return rotzM


def rotxyz(alpha, beta, gamma):
    """
    Crea una matrice di rotazione numpy 3x3 da tre rotazioni eseguite nell'ordine di x, y e z nel quadro delle coordinate locali mentre ruota.

    Le tre colonne rappresentano i nuovi vettori base nel sistema di coordinate globale di un sistema di coordinate ruotato da questa matrice.

    Args:
        alpha: angolo per la rotazione intorno all'asse x in radianti
        beta: angolo per la rotazione intorno all'asse y in radianti
        gamma: angolo per la rotazione intorno all'asse z in radianti

    Restituisce:
        La matrice di rotazione 3D per una rotazione x, y, z

    """

    return rotx(alpha).dot(roty(beta)).dot(rotz(gamma))


def homog_trasxyz(dx, dy, dz):
    """
    Crea una matrice di trasformazione lineare numpy 4x4

    Args:
        dx: traduzione in x
        dy: traduzione in y
        dz: traslazione in z
    """

    trans = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1]])

    return trans


def homog_transform(dx, dy, dz, alpha, beta, gamma):
    """
    Crea una matrice di rotazione e trasformazione numpy 4x4 da tre rotazioni eseguite
    nell'ordine x, y e z nel quadro di coordinate locali mentre ruota,
    quindi una trasformazione in x, y e z in quel quadro di coordinate ruotate.

    Le tre colonne e le tre righe rappresentano i nuovi vettori base nel sistema di
    coordinate globale di un sistema di coordinate ruotato da questa matrice.
    L'ultima colonna e le tre righe rappresentano la traslazione nel quadro di coordinate ruotato.

    Args:
        alpha: angolo di rotazione intorno all'asse x in radianti
        beta: angolo per la rotazione intorno all'asse y in radianti
        gamma: angolo di rotazione intorno all'asse z in radianti
        dx: traslazione lineare in x
        dy: traslazione lineare in y
        dz: traslazione lineare in z

    Restituisce:
        La matrice di trasformazione omogenea per una rotazione e una traslazione x, y, z.
    """

    rot4x4 = np.eye(4)
    rot4x4[:3, :3] = rotxyz(alpha, beta, gamma)
    return np.dot(homog_trasxyz(dx, dy, dz), rot4x4)


def homog_transform_inverse(matrix):
    """
    Restituisce l'inverso di una matrice di trasformazione omogenea.

                 -------------------------
                 |           |           |
    inverse   =  |    R^T    |  -R^T * d |
                 |___________|___________|
                 | 0   0   0 |     1     |
                 -------------------------
    """

    inverse = matrix
    inverse[:3, :3] = inverse[:3, :3].T
    inverse[:3, 3] = -np.dot(inverse[:3, :3], inverse[:3, 3])
    return inverse
