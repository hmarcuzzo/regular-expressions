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
    print("Expressão regular é: " + str(ER))
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

#######################################################
""" Criado uma lista com a estrutura de um automâto finito """
fa =[ ]
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
""" Separo a Expressão Regular em uniões """
ER_AUX = ER.split('+')
AUX = []

# print(ER_AUX)


#######################################################
""" É checado se nas separações de união existem algum parenteses, se houver é marcado o começo e o fim, e é setado
        a flag dizendo que existe """

begin = []
end = []
flag = 0

for i in range(len(ER_AUX)):
    for j in range(len(ER_AUX[i])):
        if ER_AUX[i][j] == '(':
            flag = 1
            begin.append(i)
        if ER_AUX[i][j] == ')':
            end.append(i)

""" Se existe parenteses nas separações, é feito a junção novamente com a união """
if flag == 1:
    for i in range(len(begin)):
        for j in range(begin[i], end[i]):
            if j != end[i]:
                ER_AUX[begin[i]] = str(ER_AUX[begin[i]]) + "+" + str(ER_AUX[j + 1])

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

# print(ER_AUX)

first = 0
last = 1

states = 1


#######################################################
""" Criando as primeiras transações do que foi separado com a união """

begin.clear()
end.clear()

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
begin2 = []
end2 = []

for i in range(len(ER_AUX)):
    flag = 0

    if len(ER_AUX[i]) > 1:
        AUX = ER_AUX[i]
        AUX = AUX.split('.')

        """ É checado se nas separações de concatenação existem algum parenteses, se houver é marcado o começo e o fim, 
                e é setado a flag dizendo que existe """
        for i in range(len(AUX)):
            for j in range(len(AUX[i])):
                if AUX[i][j] == '(':
                    flag = 1
                    begin2.append(i)
                if AUX[i][j] == ')':
                    end2.append(i)

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

        # print("AUX: " + str(AUX))

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

#######################################################
""" Criando as transições para os Fecho Kleene """

auxKleen = ''
finishKleen = ''
AUX.clear()
for i in range(len(ER)):
    if ER[i] == '*':
#         if ER[i - 1] == ')':
#             j = i
#             while j > 0:
#                 auxKleen = str(auxKleen) + str(ER[j])

#                 if ER[j] == '(':
#                     break

#                 j -= 1
#             auxKleen = list(reversed(auxKleen))
#             for h in range(len(auxKleen)):
#                 finishKleen = str(finishKleen) + str(auxKleen[h])   
#             AUX.append(finishKleen)
        # else:
        AUX.append(ER[i - 1] + ER[i])

# print("AUX: " + str(AUX))

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

                    fa[0].transitions.append("q" + str(states) + " " + str(AUX[i][0]) + " q" + str(states + 1))
                    states += 1

                    fa[0].transitions.append("q" + str(states) + " " + str(fa[0].lambda_[0]) + " q" + str(h))

        k += 1

#######################################################
""" Removendo os parenteses para repetir os ciclos de União Concatenação e Fecho Kleene """

for i in range(len(ER_AUX)):
    ER_AUX[i] = ER_AUX[i].replace('(', '')
    ER_AUX[i] = ER_AUX[i].replace(')', '')

# print("ER_AUX: " + str(ER_AUX))   


#######################################################
""" Adicionando no Autômato Finito a quantidade de estados, o estado inicial e o estado final """

for i in range(states + 1):
    fa[0].states.append("q" + str(i))

fa[0].initial_state.append("q" + str(first))
fa[0].final_states.append("q" + str(last))

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