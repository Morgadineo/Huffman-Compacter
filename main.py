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
from io import BufferedIOBase
from arvore import HuffmanNode, HuffmanTree
from typing import Any
import os

class HuffmanCompactor:
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

    ##-# Métodos Públicos #-###################################################
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
            # Ordena a lista
            huffman_list.sort
            # Elemento de menor frequência na iteração.
            left = huffman_list.pop(0)
            # Elemento de segunda menor frequência da iteração.
            right = huffman_list.pop(0) 
            
            ###################################################################
            # Nó pai, com valor de frequência como a soma da frequência das   #
            # subárvores                                                      #
            ###################################################################
            new_node = HuffmanNode(frequency=(left.frequency + right.frequency),
                                   left=left,
                                   right=right,
                                   char=None)
            huffman_list.append(new_node)

        return huffman_list[0]

    def create_fake_compacted_file(self, filename: str, fake_compact_filename: str, char_dict: dict):
        """
        Cria um arquivo falsamente compactado pelo método de Huffman.
        O arquivo gerado é 'falsamente compactado' pois seu conteúdo é o
        texto com caracteres UNICODE, simulando visualmente um arquivo binário.
        Isso é realizado para fins didáticos de demonstração dos arquivos.

        :param filename: Nome do arquivo a ser falsamente compactado.
        :param fake_compact_filename: Nome do arquivo falso gerado.
        :param char_dict: Dicionário com os caracteres e sua representação
                          binária falsa.
        """
        compact_file = open(fake_compact_filename, "w+")

        with open(filename, "r") as raw_file:
            for line in raw_file.readlines():
                for char in line:
                    char = self.__treat_char__(char)
                    compact_file.write(char_dict[char])

    def decompactor_fake_file(self, fake_compact_filename: str, fake_decompact_filename: str, char_dict: dict):
        r"""
        Descompacta um arquivo falsamente compactado. Arquivos falsamente 
        compactados armazenam uma representação ASCII dos textos em binários,
        ao invés de serem arquivos binários puros. Esse método converte o
        palavras do binárias diretamente do dicionário, não dá árvore.

        :param fake_compact_filename: Nome do arquivo falsamente compactado a ser descompactado.
        :param fake_decompact_filename: Nome do arquivo falsamente descompactado a ser gerado.
        :param fake_char_dict: Dicionário de caracteres do arquivo com a representação de texto do binário.
        """
        decompact_file = open(fake_decompact_filename, "w+")
        inverted_dict: dict[str, str] = {value: key for key, value in char_dict.items()}
        with open(fake_compact_filename, "r") as fake_compact_file:
            code: str = ""
            for bit in fake_compact_file.read():
                code += bit
                if code in inverted_dict.keys():
                    char: str = self.__treat_char__(inverted_dict[code]) 
                    decompact_file.write(char)
                    code = ""

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

    def create_compacted_file(self, filename: str, compact_filename: str, char_dict: dict):
        """
        Método para criar o arquivo binário compactado.

        :param filename: Nome do arquivo a ser compactado.
        :param compact_filename: Nome do arquivo compactado a ser gerado.
        :param char_dict: Dicionário de caracteres do arquivo.
        """
        print(f"Compactando {filename}...")

        file_string: str = self.__transform_file_to_bstr__(filename, char_dict)

        ###################################################################
        # Conserta o ultimo byte do arquivo.
        # "Relutei muito para saber se precisava disso, mas precisa sim."
        #
        # Como a leitura do arquivo compactado será feita pelo tamanho da
        # palavra do processador (1 Byte) é necessário arredondar para
        # evitar leitura lixo na descompactação. Aumenta o tamanho final.
        ###################################################################
        padding = 8 - (len(file_string) % 8)
        if padding > 0:
            file_string += "0" * padding
            print(f"Padding: {padding}")

        byte_array = bytearray()
        byte_array.append(padding)

        # Processa de 8 em 8 bits
        for i in range(0, len(file_string), 8):
            byte = file_string[i:i+8]
            byte_array.append(int(byte, 2))
        
        # Escreve o conteúdo no arquivo binário
        with open(compact_filename, "wb") as compact_file:
            compact_file.write(byte_array)
        print(f"\nArquivo gerado: {compact_filename}")

    def decompact_file(self, compact_filename: str, decompact_filename: str, char_dict: dict):
        """
        Método para descompactar arquivos.

        :param compact_filename: Nome do arquivo a ser descompactado.
        :param decompact_filename: Nome do arquivo descompactado gerado.
        :param char_dict: Dicionário de caracteres de huffman.
        """
        print(f"Descompactando...\n")
        byte_content: bytes = bytes()
        with open(compact_filename, "rb") as compact_file:
            byte_content = compact_file.read()

        bits_str_content: str = ''.join(f'{byte:08b}' for byte in byte_content)
        
        padding_byte = byte_content[0]

        # Conteúdo bruto é antes da remoção do padding
        print(f"Conteúdo bruto: \n{bits_str_content}\n")

        #######################################################################
        # Tratamento do 'padding'
        #
        # O primeiro byte é um binário para a quantidade de paddings no final.
        # A linha abaixo faz o slice para remover o primeiro byte de padding e
        # os bits no final.
        #######################################################################
        bits_str_content = bits_str_content[8:-padding_byte]

        print(f"Conteúdo sem padding: \n{bits_str_content}\n")

        inverted_dict: dict = {value: key for key, value in char_dict.items()}

        with open(decompact_filename, "w+") as decompact_file:
            bit_char = ""
            for bit in bits_str_content:
                bit_char += bit
                if bit_char in inverted_dict:
                    char = self.__treat_char__(inverted_dict[bit_char])
                    decompact_file.write(char)
                    bit_char = ""


        print(f"\n{decompact_filename} criado")

    ##-# Métodos Privados #-###################################################

    def __transform_file_to_bstr__(self, filename: str, char_dict: dict[str, str]) -> str:
        """
        Método para transformar o conteúdo de um arquivo em uma string de bits.
        Esse processo é necessário para que a criação do arquivo compactado
        seja feita. O binário de cada caractere não é feito com base na tabela
        ASCII ou Unicode, mas sim no dicionário de caracteres da árvore de 
        huffman.

        :param filename: Arquivo a transformado.

        :return: Uma string com os binários relativos a árvore de huffman.
        """
        file_string: str = str()
        with open(filename, "r") as raw_file:
            for line in raw_file.readlines():
                for char in line:
                    char = self.__treat_char__(char)
                    file_string += char_dict[char]

        return file_string

    def __order_dict__(self, dictionary: dict[str, int]) -> dict[str, int]:
        """
        #=# MÉTODO INTERNO #=#
        Ordena um dicionário [any, int], em ordem crescente, com base no valor.

        :param dictionary: Dicionário a ser ordenado.

        :return: Um novo dicionário ordenado.
        """
        return dict(sorted(dictionary.items(), key=lambda item: item[1]))

    def __treat_char__(self, char: str) -> str:
        r"""
        Método para tratar caracteres especiais ou que dificultam a
        visualização na saída do terminal. Algumas das conversões realizadas, 
        por exemplo incluem a alteração do caractere '\n' que se não tratado
        como 'raw' ou com uma nova notação, quebra a saída.

        Caso o caracter passado esteja na forma convertida, é retornado
        o caractere sem a conversão.

        Exemplos de mudanças de notação:
            :arg '\n'      -> '<EOL>'
            :arg ' '       -> '<Space>'
            :arg '<EOL>'   -> '\n'
            :arg '<Space>' -> ' '

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

            case '<EOL>':
                return '\n'

            case '<Space>':
                return ' '

            case _:
                return char

def print_dict(dictionary: dict[Any, Any]):
    """
    Exibe um dicionário.

    :param dictionary: Dicionário a ser exibido.
    """
    for key, value in dictionary.items():
        print(f"{key}: {value}")
        
if __name__ == "__main__":
    # Área de Execução
    filename = "teste.txt"
    fake_compact_filename = "teste_fake_compact.huff"
    fake_decompact_filename = "teste_fake_decompact.txt"
    compact_filename = "teste_compact.huff"
    decompact_filename = "teste_decompact.huff"

    # Compactador
    compactor: HuffmanCompactor = HuffmanCompactor()

    print(f"======> Criação da árvore <===============")
    root : HuffmanNode = compactor.create_huffman_tree(filename)
    tree : HuffmanTree = HuffmanTree(root) # Cria a árvore de Huffman
    tree.plot_tree(orientation="v")

    print(f"\n======> Dicionário do arquivo <===========")
    char_dict: dict[str, str] = tree.create_char_dict() # Dicionário de caracteres e seu binário
    print_dict(char_dict)
    
    print(f"\n======> Compactação falsa <===============\n")
    compactor.create_fake_compacted_file(filename, fake_compact_filename, char_dict)
    
    print(f"\n======> Descompactação falsa <============\n")
    compactor.decompactor_fake_file(fake_compact_filename, fake_decompact_filename, char_dict)

    print(f"\n======> Processo de Compactação <=========")
    compactor.create_compacted_file(filename, compact_filename, char_dict)

    print(f"\n======> Processo de Descompactação <======")
    compactor.decompact_file(compact_filename, decompact_filename, char_dict)

