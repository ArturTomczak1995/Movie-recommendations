from random import uniform


class Converter:

    def create_polynomial(dimensions, degree):
        list_first = []
        list_no = 0
        final_list = []
        for i in range(degree):
            list_first.append(dimensions)
        final_list.append(list_first)
        element_no = len(list_first) - 1
        try:
            while final_list[list_no][0] != 0:
                bufor = final_list[list_no][:]
                if bufor[element_no] == 0:
                    for j in range(0, len(bufor)):
                        if bufor[j] == 0:
                            bufor[j - 1] -= 1
                            for k in range(j, len(bufor)):
                                bufor[k] = bufor[j - 1]
                            break
                    final_list.append(bufor)
                    list_no += 1

                bufor = final_list[list_no][:]
                if bufor[element_no] == 0:
                    pass
                else:
                    bufor[element_no] -= 1
                    final_list.append(bufor)
                    list_no += 1
        except ValueError:
            pass
        description = [[dimensions, degree]]
        for i in final_list:
            line = []
            for x in i:
                line.append(x)
            if dimensions != 0:
                line.append(round(uniform(-1, 1), 1))
            description.append(line)
        return description

    def function_fx(function_parameters, coordinates_x):
        degree = int(function_parameters[0][1])
        whole_equation = []
        for z in range(0, len(coordinates_x)):
            equation_arr = []
            for x in range(1, len(function_parameters)):
                equation = 0
                bufor = 1
                sumx = 0
                a = 1
                for i in range(0, degree):
                    if int(function_parameters[x][i]) == 0:
                        sumx += -1
                    else:
                        bufor *= float(coordinates_x[z][(int(function_parameters[x][i])) - 1])
                if sumx == -function_parameters[0][1]:
                    bufor = 1
                equation += a * bufor
                equation_arr.append(equation)
            whole_equation.append(equation_arr)
        return whole_equation
