import sys
import subprocess

############### Declaração de Variaveis ###############

endCondition = 0        # variavel que controlara se o programa terminou ou não
states = 1              # variavel que controlara quantos estados tem o autômato finito

ER = ''                 # variavel que ira conter a expressão regular
fa =[]                  # variavel que ira conter toda a estrutura do autômato finito

first = 0               # variavel que tera sempre o começo de uma operação
last = 1                # variavel que contera o final de uma operação

begin = []              
end = []

ER_AUX = []             # variavel auxiliar da Expressão Regular
AUX = []                # variavel auxiliar da auxiliar da Expressão Regular

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
""" Junta novamente os parenteses que foram separados pelo o split de algum tipo """
def organizaParenteses(tipo, ER_AUX):
    global begin
    global end
    
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

#######################################################
""" Separo a Expressão Regular em uniões """
def Union(ER):
    # declarando as variaveis globais
    global states
    global fa
    global first
    global last
    global ER_AUX


    # se o tamanho do ER for 1 significa que já está pronto e nada deve ser feito na transação
    if len(ER) > 1:                 
        for i in range(len(ER)):     
            k = 0
            control = len(fa[0].transitions)
            while k < control:

                for j in range(states):
                    for h in range(states + 1):
                        # procura uma transação que tenha ER na transação para deleta-lo
                        if fa[0].transitions[k].find("q" + str(j) + " " + str(ER) + " q" + str(h)) == 0:      
                            # print(fa[0].transitions[k])     
                            del(fa[0].transitions[k])
                            control -= 1
                            k -= 1

                            first = j
                            last = h
                k += 1

        # onde houver o símbolo '+' é separado, gerando vários itens na listas se houver
        ER_AUX = ER.split('+')             
        
        organizaParenteses('+', ER_AUX)

        """ Criando as transações do que foi separado com a união """
        for i in range(len(ER_AUX)):
            fa[0].transitions.append("q" + str(first) + " " + str(fa[0].lambda_[0]) + " " + "q" + str((states + 1)))
            states += 1
            
            fa[0].transitions.append("q" + str(states) + " " + str(ER_AUX[i]) + " " + "q" + str((states + 1)))
            states += 1

            fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " " + "q" + str((last)))

#######################################################
""" Criando as transações para as Concatenações """
def Concatenation():
    # declarando as variaveis globais
    global states
    global first
    global last
    global ER_AUX
    global AUX


    for i in range(len(ER_AUX)):
        flag = 0

        if len(ER_AUX[i]) > 2:
            AUX = ER_AUX[i]
            AUX = AUX.split('.')

            organizaParenteses('.', AUX)


            k = 0
            control = len(fa[0].transitions)
            while k < control:

                for j in range(states):
                    for l in range(states + 1):
                        if fa[0].transitions[k].find("q" + str(j) + " " + str(ER_AUX[i]) + " q" + str(l)) == 0:
                            del(fa[0].transitions[k])
                            control -= 1
                            k -= 1

                            first = j
                            last = l

                            for h in range(len(AUX)):

                                fa[0].transitions.append("q" + str(first) + " " + str(AUX[h]) + " q" + str(states + 1))
                                states += 1

                                if h == len(AUX) - 1:
                                    fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " q" + str(last))
                                else:
                                    fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " q" + str(states + 1))
                                    states += 1
                                    first = states
                k += 1

#######################################################
""" Criando as transições para os Fecho Kleene """
def FechoKleene():
    global states
    global AUX
    global AUX_Recover

    parenteses = 0
    auxKleen = ''
    finishKleen = ''
    AUX = []

    for i in range(len(ER_AUX)):
        for j in range(len(ER_AUX[i])):
            if ER_AUX[i][j] == '(':
                parenteses += 1
            if ER_AUX[i][j] == ')':
                parenteses -= 1
            if ER_AUX[i][j] == '*' and parenteses == 0:
                if ER_AUX[i][j - 1] == ')':
                    k = j
                    while k >= 0:
                        if ER_AUX[i][k] == ')':
                            parenteses += 1

                        auxKleen = str(auxKleen) + str(ER_AUX[i][k])

                        if ER_AUX[i][k] == '(':
                            parenteses -= 1
                            if parenteses == 0:
                                break
                        k -= 1

                    auxKleen = list(reversed(auxKleen))
                    for h in range(len(auxKleen)):
                        finishKleen = str(finishKleen) + str(auxKleen[h])   
                    AUX.append(finishKleen)
                else:
                    AUX.append(ER_AUX[i][j - 1] + ER_AUX[i][j])

    # print("Fecho AUX: " + str(AUX))

    for i in range(len(AUX)):
        k = 0
        control = len(fa[0].transitions)
        while k < control:
            for j in range(states):
                for h in range(states + 1):
                    if fa[0].transitions[k].find("q" + str(j) + " " + str(AUX[i]) + " q" + str(h)) == 0 and h != 1:
                        del(fa[0].transitions[k])
                        control -= 1
                        k -= 1

                        fa[0].transitions.append("q" + str(j) + " " + str(fa[0].lambda_[0]) + " q" + str(h))
                        fa[0].transitions.append("q" + str(h) + " " + str(fa[0].lambda_[0]) + " q" + str(j))

                        fa[0].transitions.append("q" + str(j) + " " + str(fa[0].lambda_[0]) + " q" + str(states + 1))
                        states += 1

                        finishKleen = ''
                        for l in range(len(AUX[i]) - 1):
                            finishKleen = str(finishKleen) + AUX[i][l]
                        AUX[i] = finishKleen

                        fa[0].transitions.append("q" + str(states) + " " + str(AUX[i]) + " q" + str(states + 1))
                        states += 1

                        fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " q" + str(h))

            k += 1

# #######################################################
""" Removendo um nível dos parenteses para repetir os ciclos de União Concatenação e Fecho Kleene """
def RemoveParenteses(level, ER_COPY):
    global AUX
    global ER_AUX
    global endCondition

    NextRemove = ''
    
    NextRemove = ER_COPY

    ER_AUX = []

    for j in range(level):
        parenteses = 0
        for i in range(len(NextRemove)):
            if NextRemove[i] == ')':
                parenteses -= 1
                if parenteses == 0:
                    ER_AUX.append(AUX)
               
            if parenteses > 0:
                AUX = AUX + NextRemove[i]
            if NextRemove[i] == '(':
                if parenteses == 0:
                    AUX = ''
                parenteses += 1


    for i in range(len(ER_AUX)):     
        k = 0
        control = len(fa[0].transitions)
        while k < control:
            for j in range(states):
                for h in range(states + 1):

                    if fa[0].transitions[k].find("q" + str(j) + " (" + str(ER_AUX[i]) + ") q" + str(h)) == 0 and h != 1:
                        del(fa[0].transitions[k])
                        control -= 1
                        k -= 1

                        fa[0].transitions.append("q" + str(j) + " " + str(ER_AUX[i]) + " q" + str(h))

                        endCondition = 0
            k += 1

################# - Fluxo Principal - #################

init()

ER_AUX.append(ER)

AUX_Recover = []

level = 1              # quantidade de parenteses que devem ser retirados da próxima vez


while endCondition == 0:
    endCondition = 1

    AUX_Recover = ER_AUX
    
    for i in range(len(ER_AUX)):
        Union(ER_AUX[i])
        Concatenation()
        FechoKleene()
        ER_AUX = AUX_Recover

    AUX = ''
    for i in range(len(AUX_Recover)):
        AUX = AUX + AUX_Recover[i]
    RemoveParenteses(level, AUX)

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