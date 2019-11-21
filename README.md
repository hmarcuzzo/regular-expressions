<!-- Este projeto pode ser encontrado no GitHub atráves deste link: https://github.com/hmarcuzzo/regularExpressions -->

# Conceitos da implementação

Este trabalho consiste em transformar uma expressão regular em um automato finito, para isso todas as operações de União, Concatenação e Fecho de Kleene são feitas, nesta ordem, nos operadores que se encontram fora de parenteses.

Ao final deste ciclo, tenta-se retirar um ciclo de parenteses, se ocorrer com sucesso, ou se seja haviam parenteses para ser retirado, o ciclo de União, Concatenação e Fecho de Kleene se repetem até que não existam mais parenteses para serem retirados.

# Como compilar

python3 RegularExpression_to_FiniteAutomaton.py ER.txt finiteAutomaton.txt "input"

* RegularExpression_to_FiniteAutomaton.py - É o código que ira transformar a expressão regular em um autômato finito

* ER.txt - O arquivo que conterá a expressão regular

* finiteAutomaton.txt - O arquivo onde o autômato finito será escrito

* "input" - A palavra que deseja testar se o autômato finito gerado é aceito

# Como executar

Para alterar a expressão regular basta abrir o arquivo ER.txt e escrever uma nova expressão regular, onde a nomenclatura aceita é:

* "+"   - Representa a união

* "."   - Representa a concatenação

* "*"   - Representa o Fecho de Kleene

* "()"  - Utilizado para marcar a ordem que devem ser feitas as operações de União, Concatenação e Fecho de Kleene

# Bibliotecas usadas (descrever as não padrões)

* sys - da acesso à variaveis usadas pelo terminal e para funções que interagem diretamente com ele. Neste projeto foi utilizada apenas para pegar variáveis por linha de comando

* subprocess - permite gerar novos processos, conectar-se aos tubos de entrada / saída / erro e obter seus códigos de retorno.

# Exemplo de uso

    Arquivo ER.txt de entrada:
        a.(b+c)

Entrada do terminal:
```
python3 RegularExpression_to_FiniteAutomaton.py ER.txt finiteAutomaton.txt ab
```

Saida do terminal:
```
[ab]@Sq0 -> [ab]@Sq2
[ab]@Sq2 -> [b]@Sq4
[b]@Sq4 -> [b]@Sq5
[b]@Sq5 -> [b]@Sq7
[b]@Sq5 -> [b]@Sq9
[b]@Sq7 -> []@Sq8
[]@Sq8 -> []@Sq6
[]@Sq6 -> []@Sq3
[]@Sq3 -> []@Sq1
Aceitou
```

Entrada do terminal:
```
python3 RegularExpression_to_FiniteAutomaton.py ER.txt finiteAutomaton.txt abc
```

Saida do terminal:
```
[abc]@Sq0 -> [abc]@Sq2
[abc]@Sq2 -> [bc]@Sq4
[bc]@Sq4 -> [bc]@Sq5
[bc]@Sq5 -> [bc]@Sq7
[bc]@Sq5 -> [bc]@Sq9
[bc]@Sq7 -> [c]@Sq8
[c]@Sq8 -> [c]@Sq6
[c]@Sq6 -> [c]@Sq3
[c]@Sq3 -> [c]@Sq1
Rejeitou
```