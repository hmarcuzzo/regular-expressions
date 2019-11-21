import sys
import subprocess

############### Declaração de Variaveis ###############

states = 1      # variavel que controlara quantos estados tem o autômato finito

ER = ''         # variavel que contera a expressão regular
fa =[]          # variavel que contera toda a estrutura do autômato finito

first = 0
last = 1

begin = []
end = []

ER_AUX = []
AUX = []

EXECUTIONS = 0
lenER_AUX = 0

#######################################################
""" Classe com todas as linhas de um automato finito. """
class FiniteAutomaton(object):
    def __init__(self):
        self.machine = []
        self.input_alphabet = []
        self.lambda_ = []
        self.states = []
        self.initial_state = []
        self.final_states = []
        self.transitions = []


def printfaData(fa_aux, i):
    print()
    print(f'Tipo da máquina {i+1} : {fa_aux.machine}')
    print(f'Alfabeto da máquina {i+1} : {fa_aux.input_alphabet}')
    print(f'Lambda da máquina {i+1} : {fa_aux.lambda_}')
    print(f'Estados da máquina {i+1} : {fa_aux.states}')
    print(f'Estado incial da máquina {i+1} : {fa_aux.initial_state}')
    print(f'Estado final da máquina {i+1} : {fa_aux.final_states}')
    print(f'Transições da máquina {i+1} : ')
    for j in fa_aux.transitions:
        print(j)
    print()

#######################################################
""" Inicia o programa com que deve ser feito antes das transformações """
def init():
    global ER
    global fa

    """ Pego a Expressão Regular do .txt """
    fp = open(sys.argv[1], "r")
    lines_cmd = fp.readlines()
    fp.close()
    for line in lines_cmd:
        ER = (line.rstrip())

    print()
    print("Expressão regular é: " + str(ER))

    #######################################################
    """ Criado uma lista com a estrutura de um automâto finito """
    
    fa.append(FiniteAutomaton())

    #######################################################
    """ Colocando o tipo do autômato finito """
    fa[0].machine = "N D F A"

    #######################################################
    """ Pegando o alfabeto do autômato finito """
    for i in range(len(ER)):
        if ER[i] != '(' and ER[i] != ')' and ER[i] != '+' and ER[i] != '.' and ER[i] != '*':
            if ER[i] not in fa[0].input_alphabet:
                fa[0].input_alphabet.append(ER[i])

    #######################################################
    """ Procuramos no alfabeto do Automato Finito, a partir da letra "B" uma letra não que não estivesse
            no alfabeto da fita para que podesse representar o Lambda """
    letter = 66
    for i in range(25):
        if chr(letter) not in fa[0].input_alphabet:
            fa[0].lambda_.append(chr(letter))
            break
        letter += 1

    #######################################################
    """ Criando a primeira transição da Expressão regular e adicionando os estados inicias e finais """
    fa[0].transitions.append("q0" + " " + str(ER) + " " + "q1")

    fa[0].initial_state.append("q0")
    fa[0].final_states.append("q1")

#######################################################

def organizaParenteses(tipo):
    global begin
    global end
    global ER_AUX
    
    """ É checado se nas separações de união existem algum parenteses, se houver é marcado o começo e o fim, e é setado
                a flag dizendo que existe """
    parenteses = 0                      # caso haja mais um nível de parenteses esse contador irá controlar para que nenhuma união sejá perdido
    flag = 0                            # flag que dirá se há parenteses na separação
    begin.clear()                       # irá marcar o inicio do parenteses, sendo em listas para o caso de haver parenteses em posições separadas
    end.clear()                         # irá marcar o fim do parentes, sendo em listas para o caso de haver parenteses em posições separadas
        
    """ procura os parenteses para fazer as uniões """
    for i in range(len(ER_AUX)):
        for j in range(len(ER_AUX[i])):
            if ER_AUX[i][j] == ')':
                parenteses -= 1

                if parenteses == 0:
                    end.append(i)
            if ER_AUX[i][j] == '(':
                if parenteses == 0:
                    begin.append(i)
                parenteses += 1
                flag = 1

    print(begin)
    print(end)
    """ Se existe parenteses nas separações, é feito a junção novamente com o simblo da união na posição de inicio das separações """
    if flag == 1:
        for i in range(len(begin)):
            for j in range(begin[i], end[i]):
                if j != end[i]:
                    ER_AUX[begin[i]] = str(ER_AUX[begin[i]]) + str(tipo) + str(ER_AUX[j + 1])

    """ Deleta-se as partes após o inicio das separações, pois já estão na posição onde occoreu as junções """
    for i in range(len(begin)):
        j = begin[i]
        while j < end[i]:
            end[i] = end[i] - 1
            if i < (len(begin) - 1):
                begin[i + 1] = begin[i + 1] - 1
                end[i + 1] = end[i + 1] - 1
            
            del(ER_AUX[j + 1])
            j -= 1
            j += 1

""" Separo a Expressão Regular em uniões """
def Union(ER):
    global states
    global fa
    global first
    global last
    global begin
    global end
    global ER_AUX


    if len(ER) > 1:                 # se o tamanho do ER for 1 significa que já está pronto e nada deve ser feito na transação
        for i in range(len(ER)):     
            k = 0
            control = len(fa[0].transitions)
            while k < control:

                for j in range(states):
                    for h in range(states + 1):
                        # procura uma transação que tenha ER na transação para deleta-lo
                        if fa[0].transitions[k].find("q" + str(j) + " " + str(ER) + " q" + str(h)) == 0:      
                            print(fa[0].transitions[k])     
                            del(fa[0].transitions[k])
                            control -= 1
                            k -= 1

                            first = j
                            last = h
                k += 1

        # onde houver o símbolo '+' é separado, gerando vários itens na listas se houver
        ER_AUX = ER.split('+')             
        
        organizaParenteses('+')

        """ Criando as primeiras transações do que foi separado com a união """
        begin.clear()       # marca o inicio da nova transação
        end.clear()         # marca o fim da nova transação

        for i in range(len(ER_AUX)):
            fa[0].transitions.append("q" + str(first) + " " + str(fa[0].lambda_[0]) + " " + "q" + str((states + 1)))
            begin.append(states + 1)
            states += 1
            
            fa[0].transitions.append("q" + str(begin[i]) + " " + str(ER_AUX[i]) + " " + "q" + str((states + 1)))
            end.append(states + 1)
            states += 1

            fa[0].transitions.append("q" + str(end[i]) + " " + str(fa[0].lambda_[0]) + " " + "q" + str((last)))
#######################################################


















################# - Fluxo Principal - #################

init()


Union(ER)
# Concatenation()
# endCondition = 0            # diz se o programa deve terminar ou não

# ER_AUX = []                 # variável que será mandada para a execução do código (será mandado em partes)
# ER_AUX.append(ER)
# AUX_Parenteses = []
# AUX_Recover = []

# level = 0                   # quantidde de parenteses que devem ser tirados

# while endCondition == 0:
#     endCondition = 1
#     level = 1              # quantidade de parenteses que devem ser retirados da próxima vez

#     print("ER_AUX main: " + str(ER_AUX))

#     AUX_Recover = ER_AUX
#     AUX_Parenteses = AUX
#     print("AUX main: " + str(AUX_Recover))

#     for i in range(len(ER_AUX)):
#         print("ER_AUX: " + str(ER_AUX))
#         Union(ER_AUX[i])
#         print("União: " + str(ER_AUX))      
#         Concatenation()
#         print("Concatenação: " + str(ER_AUX))   
#         FechoKleene()
#         print("Fecho Kleene: " + str(ER_AUX))  
#         # AUX_Parenteses.append(ER_AUX[i])
#         ER_AUX = AUX_Recover


#     AUX = ''
#     for i in range(len(AUX_Parenteses)):
#         AUX = AUX + AUX_Parenteses[i]
#     RemoveParenteses(level, AUX)

#######################################################
""" Adicionando no Autômato Finito a quantidade de estados, o estado inicial e o estado final """

for i in range(states + 1):
    fa[0].states.append("q" + str(i))

#######################################################
printfaData(fa[0], 0)
print()

""" Aberto o arquivo vindo por comando, na pasta ."/fla/dfa.txt" e escreve a união das duas fa """
re_to_fa = open(sys.argv[2], 'w')
for i in range(len(fa[0].machine)):
    re_to_fa.write(fa[0].machine[i])
re_to_fa.write("\n")
for i in range(len(fa[0].input_alphabet)):
    re_to_fa.write(fa[0].input_alphabet[i] + " ")
re_to_fa.write("\n")
for i in range(len(fa[0].lambda_)):
    re_to_fa.write(fa[0].lambda_[i] + " ")
re_to_fa.write("\n")
for i in range(len(fa[0].states)):
    re_to_fa.write(str(fa[0].states[i]) + " ")
re_to_fa.write("\n")
for i in range(len(fa[0].initial_state)):
    re_to_fa.write(str(fa[0].initial_state[i]) + " ")
re_to_fa.write("\n")
for i in range(len(fa[0].final_states)):
    re_to_fa.write(str(fa[0].final_states[i]) + " ")
re_to_fa.write("\n")
for i in range(len(fa[0].transitions)):
    for j in range(len(fa[0].transitions[i])):
        re_to_fa.write(str(fa[0].transitions[i][j]))
    re_to_fa.write("\n")

re_to_fa.close()
#######################################################
""" Verifica se o automato aceita a palavra colocada """

if len(sys.argv[3:]) > 0:
    inputTest = ""
    for i in range(len(sys.argv[3:])):
        inputTest = inputTest + sys.argv[3:][i]

    return_code = subprocess.call('python3 ./fla/main.py ' + sys.argv[2] + " " + inputTest, shell=True)