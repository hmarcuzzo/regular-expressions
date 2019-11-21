import sys
import subprocess

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
fa =[ ]
fa.append(FiniteAutomaton())


#######################################################
""" Criando a primeira transição da Expressão regular e adicionando os estados inicias e finais """
fa[0].transitions.append("q0" + " " + str(ER) + " " + "q1")

fa[0].initial_state.append("q0")
fa[0].final_states.append("q1")

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
""" Separo a Expressão Regular em uniões """
def Union(ER):
    global states
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
                            del(fa[0].transitions[k])
                            control -= 1
                            k -= 1

                            first = j
                            last = h
                k += 1

        # onde houver o símbolo '+' é separado, gerando vários itens na listas se houver
        ER_AUX = ER.split('+')              

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
                        ER_AUX[begin[i]] = str(ER_AUX[begin[i]]) + "+" + str(ER_AUX[j + 1])


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
""" Criando as transações para as Concatenações """
def Concatenation():
    global states
    global begin
    global end
    global ER_AUX

    begin2 = []
    end2 = []

    for i in range(len(ER_AUX)):
        flag = 0

        if len(ER_AUX[i]) > 2:
            AUX = ER_AUX[i]
            AUX = AUX.split('.')

            """ É checado se nas separações de concatenação existem algum parenteses, se houver é marcado o começo e o fim, 
                    e é setado a flag dizendo que existe """
            parenteses = 0

            for i in range(len(AUX)):
                for j in range(len(AUX[i])):
                    if AUX[i][j] == ')':
                        parenteses -= 1

                        if parenteses == 0:
                            end2.append(i)
                    if AUX[i][j] == '(':
                        if parenteses == 0:
                            begin2.append(i)
                        parenteses += 1
                        flag = 1

            """ Se existe parenteses nas separações, é feito a junção novamente com a concatenação """
            if flag == 1:
                for i in range(len(begin2)):
                    for j in range(begin2[i], end2[i]):
                        if j != end2[i]:
                            AUX[begin2[i]] = str(AUX[begin2[i]]) + "." + str(AUX[j + 1])

                for i in range(len(begin2)):
                    j = begin2[i]
                    while j < end2[i]:
                        end2[i] = end2[i] - 1
                        if i < (len(begin2) - 1):
                            begin2[i + 1] = begin2[i + 1] - 1
                            end2[i + 1] = end2[i + 1] - 1
                        
                        del(AUX[j + 1])
                        j -= 1
                        j += 1

            print("AUX Contatenation: " + str(AUX))

            k = 0
            control = len(fa[0].transitions)
            while k < control:
                if fa[0].transitions[k].find("q" + str(begin[i]) + " " + str(ER_AUX[i]) + " q" + str(end[i])) == 0:
                    del(fa[0].transitions[k])
                    control -= 1
                    k -= 1

                    for h in range(len(AUX)):
                        fa[0].transitions.append("q" + str(begin[i]) + " " + str(fa[0].lambda_[0]) + " q" + str(states + 1))
                        states += 1


                        fa[0].transitions.append("q" + str(states) + " " + str(AUX[h]) + " q" + str(states + 1))
                        states += 1

                        if h == len(AUX) - 1:
                            fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " q" + str(end[i]))
                        else:
                            fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " q" + str(states + 1))
                            states += 1
                            begin[i] = states
                k += 1

# #######################################################
""" Criando as transições para os Fecho Kleene """
def FechoKleene():
    global states
    global AUX

    parenteses = 0
    auxKleen = ''
    finishKleen = ''
    AUX = []

    for i in range(len(ER)):
        if ER[i] == '*':
            if ER[i - 1] == ')':
                j = i
                while j >= 0:
                    if ER[j] == ')':
                        parenteses += 1

                    auxKleen = str(auxKleen) + str(ER[j])

                    if ER[j] == '(':
                        parenteses -= 1
                        if parenteses == 0:
                            break
                    j -= 1

                auxKleen = list(reversed(auxKleen))
                for h in range(len(auxKleen)):
                    finishKleen = str(finishKleen) + str(auxKleen[h])   
                AUX.append(finishKleen)
            else:
                AUX.append(ER[i - 1] + ER[i])


    for i in range(len(AUX)):
        k = 0
        control = len(fa[0].transitions)
        while k < control:
            for j in range(states):
                for h in range(states + 1):
                    if fa[0].transitions[k].find("q" + str(j) + " " + str(AUX[i]) + " q" + str(h)) == 0 and h != 1:
                        # print("Transition: " + str(fa[0].transitions[k]) + str(" j: ") + str(j) +str(" h: ") + str(h))
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
def RemoveParenteses(level):
    global AUX
    global ER_AUX
    global endCondition
    global lenER_AUX
    global EXECUTIONS
    
    NextRemove = ER

    # print("ER_AUX: " + str(ER_AUX))
    # print("ER: " + str(ER))

    ER_AUX = []

    print("NextRemove1: " + str(NextRemove))

    for j in range(level):
        parenteses = 0
        for i in range(len(NextRemove)):
            if NextRemove[i] == ')':
                parenteses -= 1
                if parenteses == 0:
                    ER_AUX.append(AUX)
                    # lenER_AUX = len(ER_AUX)

                    print("ER_AUX " +str(ER_AUX))
               
            if parenteses > 0:
                AUX = AUX + NextRemove[i]
            if ER[i] == '(':
                if parenteses == 0:
                    AUX = ''
                parenteses += 1
        
        # NextRemove = ''
        # parenteses = 0
        # for i in range(len(ER_AUX)):
        #     for h in range(len(ER_AUX[i])):
        #         NextRemove = NextRemove + ER_AUX[i][h]

        if j < (level - 1):
            AUX = ''
            parenteses = 0
            for i in range(len(NextRemove)):
                if NextRemove[i] == '(':
                    if parenteses == 0:
                        AUX = ''
                    parenteses += 1

                if parenteses > 1:
                    AUX = AUX + NextRemove[i]
                    
                if NextRemove[i] == ')':
                    parenteses -= 1

            # if parenteses > 0:
            NextRemove = AUX
            ER_AUX = []
            print("NextRemove2: " + str(NextRemove))

    print("ER_AUX Final: " + str(ER_AUX))
    print()

    for i in range(len(ER_AUX)):     
        k = 0
        control = len(fa[0].transitions)
        while k < control:
            for j in range(states):
                for h in range(states + 1):

                    if fa[0].transitions[k].find("q" + str(j) + " (" + str(ER_AUX[i]) + ") q" + str(h)) == 0 and h != 1:
                        # print("ER_AUXi: " + str(ER_AUX[i]))
                        del(fa[0].transitions[k])
                        control -= 1
                        k -= 1

                        fa[0].transitions.append("q" + str(j) + " " + str(ER_AUX[i]) + " q" + str(h))

                        endCondition = 0
            k += 1

############### Declaração de Variaveis ###############

states = 1

first = 0
last = 1

begin = []
end = []

AUX = []

EXECUTIONS = 0
lenER_AUX = 0

################# - Fluxo Principal - #################
endCondition = 0            # diz se o programa deve terminar ou não

ER_AUX = []                 # variável que será mandada para a execução do código (será mandado em partes)
ER_AUX.append(ER)

level = 0                   # quantidde de parenteses que devem ser tirados

while endCondition == 0:
    EXECUTIONS = 0
    lenER_AUX = len(ER_AUX)

    endCondition = 1

    Union(ER_AUX[0])
    Concatenation()
    FechoKleene()
    # RemoveParenteses(level) 
   
    level = 1              # quantidade de parenteses que devem ser retirados da próxima vez

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