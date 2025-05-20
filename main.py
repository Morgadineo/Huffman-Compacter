###############################################################################
#
# -> Compactador de Huffman <-
# 
# Grupo  : A
# Membros: Arthur Morgado Teixeira,
#              ...,
#              ...,
#
# Data   : 18/06/2025
###############################################################################
from arvore import HuffmanNode, HuffmanTree

class HuffmanCompacter:
    """
    Um código Huffman é um tipo específico de código de prefixo ótimo comumente
    usado para compressão de dados sem perdas. O processo de encontrar ou usar 
    tal código é a codificação Huffman, um algoritmo desenvolvido por David A. 
    Huffman enquanto ele era aluno de doutorado no MIT e publicado no artigo 
    de 1952 "Um Método para a Construção de Códigos de Redundância Mínima".
    
    O compactador deve funcionar para qualquer tipo arquivo, independente da
    extensão.

    """
    def __init__(self) -> None:
        pass

    def __treat_char__(self, char) -> str:
        r"""
        Método para tratar caracteres especiais ou que dificultam a
        visualização na saída do terminal. Algumas das conversões realizadas, 
        por exemplo incluem a alteração do caractere '\n' que se não tratado
        como 'raw' ou com uma nova notação, quebra a saída.

        Exemplos de mudanças de notação:
            :arg '\n' -> '<EOL>'
            :arg ' '  -> '<Space>'

        Caracteres comuns ou alfanuméricos não precisam de tratamento, por isso
        não recebem uma nova notação.

        :param char: Caractere cru a ser tratado

        :return: Uma string substituta para o caractere.
        """

        match char:
            case '\n':
                # Caractere de final de linha
                return '<EOL>'

            case ' ':
                # Torna o caracter mais vísivel
                return '<Space>'

            case _:
                return char

    def read_file(self, filename: str) -> dict[str, int]:
        r"""
        Lê um arquivo e realiza a contagem de caracteres.
        Caracteres especiais como '\n' são considerados e recebem uma nova
        notação para não causar efeitos colaterais na saída do terminal.
        Confira __treat_char__() para mais informações.

        :param filename: Nome do arquivo a ser lido.

        :return: Dicionário na qual as chaves são os caracteres encontrados e o
                 valor são a quantidade de ocorrências (frequência).
        """
        char_dict: dict[str, int] = dict()

        with open(filename, 'r') as file:
            for line in file.readlines():
                for character in line:
                    # Trata o caractere.
                    character: str = self.__treat_char__(character)

                    if character in char_dict:
                        char_dict[character] += 1
                    else:
                        char_dict.update({character: 1})
                
        return char_dict

    def __order_dict__(self, dictionary: dict[str, int]) -> dict[str, int]:
        """
        #=# MÉTODO INTERNO #=#
        Ordena um dicionário [any, int], em ordem crescente, com base no valor.

        :param dictionary: Dicionário a ser ordenado.

        :return: Um novo dicionário ordenado.
        """
        return dict(sorted(dictionary.items(), key=lambda item: item[1]))
            
    def create_huffman_tree(self, filename: str) -> HuffmanNode:
        """
        Cria uma arvóre de caracteres de Huffman para um determinado arquivo.
        Os caracteres presentes no arquivo são armazenados na folha.
        Confira a classe HuffmanNode para mais informações.
        
        :param filename: Nome do arquivo da qual a árvore será gerada.

        :return: A raiz da árvore.
        """
        char_dict = self.read_file(filename)
        char_dict = self.__order_dict__(char_dict)

        # Lista para criar as subárvores
        huffman_list: list[HuffmanNode] = list()

        #######################################################################
        # - Transforma cada caracter presente no dicionário em um nó folha. - #
        # O nó folha da árvore de huffman só armazena o caractere e a         #
        # frequência.                                                         #
        #######################################################################
        for char in char_dict:
            huffman_list.append(HuffmanNode(char_dict[char], None, None, char))

        #######################################################################
        # Continua fazendo o processo de criação da árvore, até a lista só    #
        # possuir um valor que é a raiz da árvore.                            #
        #######################################################################
        while len(huffman_list) != 1:
            # Elemento de menor frequência na iteração.
            element_1 = huffman_list.pop(0)
            # Elemento de segunda menor frequência da iteração.
            element_2 = huffman_list.pop(0) 
            
            ###################################################################
            # Nó pai, com valor de frequência como a soma da frequência das   #
            # subárvores                                                      #
            ###################################################################
            new_node = HuffmanNode(frequency=(element_1.frequency + element_2.frequency),
                                   left=element_1,
                                   right=element_2,
                                   char=None)
            huffman_list.append(new_node)
            huffman_list.sort()

        return huffman_list[0]

if __name__ == "__main__":
    # Área de Execução
    filename = "teste.txt"
    compacter = HuffmanCompacter()

    root = compacter.create_huffman_tree(filename)
    tree = HuffmanTree(root)

    tree.plot_tree()

