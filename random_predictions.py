from random import randint


def read_data_set(input_file, delimiter):
    retrieved_data = []
    data_in = open(input_file, "r")
    for f in data_in:
        spl = map(str, f.rstrip('\n').split(delimiter))
        retrieved_data.extend([[x for x in spl]])
    return retrieved_data


def write_data(i, input_data):
    f = open("submission" + str(i) + ".csv", "w")
    for i in range(len(input_data)):
        space = ";"
        for j in range(0, len(input_data[i])):
            if j == len(input_data[i]) - 1:
                space = "\n"
            else:
                input_data[i][j] = input_data[i][j]
            if i == 0:
                input_data[i][j] = input_data[i][j]
            f.write(str(input_data[i][j]) + space)
    f.close()


def replace():
    data = read_data_set("../predictionFiles/task.csv", ";")
    whole_data = []
    for i in data:
        data_bufor = []
        for j in i:
           try:
               data_bufor.append(int(j))
           except:
               data_bufor.append(randint(0, 5))
        whole_data.append(data_bufor)
    write_data("", whole_data)



if __name__ == '__main__':
    replace()