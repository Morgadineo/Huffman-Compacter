###############################################################################
#
# -> Projeto Compactador de Huffman <-
# 
# 
# Grupo  : A
# Membros: Arthur Morgado Teixeira,
#              ...,
#              ...,
#
# Data   : 18/06/2025
###############################################################################
# Implementa uma árvore binária para ser utilizada pelo algoritmo de Huffman.
# 
# 1) Nós folhas armazenam os caracteres
# 2) bit 0 move para esquerda, bit 1 move para direita
###############################################################################
from typing import Self

class HuffmanNode:
    def __init__(self, frequency, left, right, char) -> None:
        self.frequency: int = frequency
        self.left  = left
        self.right = right
        self.char  = char

    def __lt__(self, object: Self) -> bool:
        if self.frequency < object.frequency:
            return True
        return False

    def __gt__(self, object: Self) -> bool:

        if self.frequency > object.frequency:
            return True
        return False


class HuffmanTree:
    def __init__(self, root: HuffmanNode) -> None:
        pass


