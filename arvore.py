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
from typing import Any, Self
from pptree import Node as PPTreeNode, print_tree
from pptree.pptree import tree_repr


class HuffmanNode:
    def __init__(self, frequency, left, right, char) -> None:
        self.frequency: int = frequency
        self.left  = left
        self.right = right
        self.char  = char


    def __str__(self) -> str:
        """
        Método interno da classe. Retorna a estrutura da classe quando
        transformada em string.
        """
        if self.char is None:
            return str(self.frequency)
        return self.char


    def __lt__(self, object: Self) -> bool:
        """
        Método interno da classe. Implementa o operador '<' 'Less Then'
        """
        if self.frequency < object.frequency:
            return True
        return False

    def __gt__(self, object: Self) -> bool:
        """
        Método interno da classe. Implementa o operador '>' 'Greater Then'
        """
        if self.frequency > object.frequency:
            return True
        return False


class HuffmanTree:
    def __init__(self, root: HuffmanNode) -> None:
        self.root = root

    def create_char_dict(self) -> dict[str, str]:
        """
        Retorna um dicionário com os códigos (em binário) de Huffman para 
        cada caractere encontrado no arquivo.
        """
        codes = dict()
        self._traverse_tree(self.root, "", codes)
        return codes

    def _traverse_tree(self, node: HuffmanNode, current_code: str, codes: dict) -> None:
        """
        Percorre a árvore recursivamente para construir os códigos.
        Args:
            node: Nó atual
            current_code: Código acumulado até o momento
            codes: Dicionário para armazenar os códigos encontrados
        """
        if node is None:
            return

        # Se é um nó folha (tem caractere), adiciona ao dicionário
        if node.char is not None:
            codes[node.char] = current_code
            return

        # Percorre a esquerda (adiciona 0 ao código)
        self._traverse_tree(node.left, current_code + "0", codes)
        
        # Percorre a direita (adiciona 1 ao código)
        self._traverse_tree(node.right, current_code + "1", codes)

    def plot_tree(self, orientation: str="h"):
        """
        Plota a árvore recursivamente, utilizando a biblioteca pptree,
        começando pelo nó raiz.
        """
        pptree_root = convert_to_pptree(self.root)

        if orientation == "v":
            print_tree(pptree_root, horizontal=True)
        elif orientation == "h":
            print_tree(pptree_root, horizontal=False)


def convert_to_pptree(huffman_node: HuffmanNode, parent: PPTreeNode | None = None):
    """
    Converte um nó da árvore de Huffman para um nó da biblioteca de plotagem
    pptree.

    :param huffman_node: O nó da árvore a ser convertido.
    :param parent: Nó pai do nó atual.

    :return None: Caso seja um nó folha, sem filhos.
    :return PPTreeNode: Caso consiga realizar a conversão.
    """
    if huffman_node is None:
        return None

    # Nome do nó: frequência(interno) ou caractere(folha)
    name = str(huffman_node)

    # Converte para um PPTreeNode
    current = PPTreeNode(name, parent)

    # Recursivamente cria os filhos
    convert_to_pptree(huffman_node.left, current)
    convert_to_pptree(huffman_node.right, current)

    return current


