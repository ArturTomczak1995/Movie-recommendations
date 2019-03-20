from Converter import Converter
from random import uniform
import re


def get_k_degree_sets(n, k):
    polynomial_set = Converter.create_polynomial(dimensions=n, degree=k)
    return polynomial_set


def type_changer(arr):
    type_arr = []
    for i in arr:
        try:
            type_arr.append(int(i))
        except (ValueError, TypeError):
            try:
                type_arr.append(float(i))
            except (ValueError, TypeError):
                i = re.sub('[] \'[]', '', i)
                spl = i.split(',')
                type_arr.append(spl)
    return type_arr


def read_data_set_cf(input_file, delimiter):
    retrieved_data = []
    data_in = open(input_file, "r")
    for f in data_in:
        spl = f.rstrip('\n').split(delimiter)
        type_arr = type_changer(spl)
        retrieved_data.extend([[x for x in type_arr]])
    return retrieved_data


def split_by_user(data, idx):
    usr_arr = []
    bufor_val = data[0][idx]
    bufor_arr = []
    for i in data:
        if i[1] != bufor_val:
            usr_arr.append(bufor_arr)
            bufor_arr = []
        bufor_arr.append(i)
        bufor_val = i[idx]
    usr_arr.append(bufor_arr)
    return usr_arr


def get_tasks():
    data = read_data_set_cf("../predictionFiles/task.csv", ";")
    urs_split = split_by_user(data, 1)
    return urs_split


def get_trainers():
    data = read_data_set_cf("../predictionFiles/train.csv", ";")
    trn_split = split_by_user(data, 1)
    return trn_split


def get_features(labels, features_no):
    feature_arr = []
    for i in range(len(labels) - 1, -1, -1):
        bufor_arr = [labels[i][0]]
        for j in range(0, features_no):
            random_parameter = uniform(-1, 1)
            bufor_arr.append(random_parameter)
        feature_arr.append(bufor_arr)
    return feature_arr


def get_parameters(train, features_no):
    description_arr = []
    for i in range(0, len(train)):
        description_1st_degree = get_k_degree_sets(n=features_no, k=1)
        description_arr.append(description_1st_degree)
    return description_arr


def data_to_train(train, features_arr):
    features_usr_arr = []
    for usr in train:
        bufor_arr = []

        for mv in usr:
            bufor = features_arr[mv[2] - 1][1:][:]
            bufor.append(mv[3])
            bufor_arr.append(bufor)
        features_usr_arr.append(bufor_arr)
    return features_usr_arr


def data_to_predict(task, features_arr):
    features_usr_arr = []
    for usr in task:
        bufor_arr = []

        for mv in usr:
            bufor = features_arr[mv[2] - 1][1][:]
            bufor_arr.append(bufor)
        features_usr_arr.append(bufor_arr)
    return features_usr_arr


def coordinates_from_data(data):
    user_arr = []
    for user in data:
        coordinates_x = []
        coordinates_y = []
        for movie in user:
            coordinates_x.append([movie[0]])
            coordinates_y.append([movie[1]])
        user_arr.append([coordinates_x, coordinates_y])
    return user_arr


def function_fx_cf(function_parameters, coordinates_x, k):
    equation = 0
    for l in range(1, len(function_parameters)):
        bufor = 1
        sumx = 0
        a = function_parameters[l][len(function_parameters[l]) - 1]
        for m in range(0, int(function_parameters[0][1])):
            if int(function_parameters[l][m]) == 0:
                sumx += -1
            else:
                bufor *= coordinates_x[k][(int(function_parameters[l][m])) - 1]
        if sumx == -function_parameters[0][1]:
            bufor = 1
        equation += a * bufor
    return equation


def polynomial_trainer_cf(coordinates_x, coordinates_y, function_parameters, iterations):
    function_parameters_in = function_parameters[:]
    alpha = 0.1

    for iteration in range(iterations):
        p0_element_before_sum = []
        gradient = []
        for no_x in range(0, len(coordinates_x[0])):
            p1_element_before_sum = []
            for k in range(0, len(coordinates_x)):
                sum_p0 = 0
                sum_p1 = 0
                equation = function_fx_cf(function_parameters, coordinates_x, k)
                sum_p0 += equation - coordinates_y[k][0]
                p0_element_before_sum.append(sum_p0)
                sum_p1 += sum_p0 * coordinates_x[k][no_x]
                p1_element_before_sum.append(sum_p1)

            p_n_derivative = (1 / float(len(coordinates_x))) * sum(p1_element_before_sum)
            gradient.append(p_n_derivative)

        p0_derivative = (1 / float(len(coordinates_x))) * sum(p0_element_before_sum)
        gradient.append(p0_derivative)

        for i in range(0, len(gradient)):
            gradient_i = gradient[i - 1]
            for j in range(1, len(function_parameters_in)):
                x_j = function_parameters_in[j][0]
                if x_j == i:
                    bufor = function_parameters[j][len(function_parameters_in[1]) - 1]
                    function_parameters[j][len(function_parameters_in[1]) - 1] = bufor - alpha * gradient_i
    return function_parameters


def features_to_params(coordinates_x_y):
    parameter_arr = []
    for user in coordinates_x_y[0]:
        parameter_arr.append([len(user) - 1, 1])
        for i in range(len(user) - 1, -1, -1):
            parameter_arr.append([i, user[i]])
    return parameter_arr


def params_connect(params, train, features_arr):
    param_arr = []
    params_y = []
    for i in range(0, len(features_arr)):
        bufor_arr = []
        params_buff = []
        for j in range(0, len(train)):
            for k in range(0, len(train[i])):
                movie = train[j][k][2] - 1
                if movie == i:
                    score = train[j][k][3]
                    params_buff.append([score])
                    for param in params[j][1:2]:
                        bufor_arr.append([param[1]])
        param_arr.append(bufor_arr)
        params_y.append(params_buff)
    return param_arr, params_y


def feature_to_coordinate(feature_arr):
    coordinates_x = [[len(feature_arr), 1]]
    for i in range(len(feature_arr) - 1, -1, -1):
        coordinates_x.append([feature_arr[i][0], feature_arr[i][1:][0]])
    coordinates_x.append([0, 1])
    return coordinates_x


def coord_y_connect(coordinates_x_y):
    coord_y = []
    for user in coordinates_x_y:
        for score in user[1]:
            coord_y.append(score)
    return coord_y


def feature_changer(feature_arr):
    coordinates_x = []
    for i in range(len(feature_arr) - 1, -1, -1):
        bufor_arr = [i, [feature_arr[i][1]]]
        coordinates_x.append(bufor_arr)
    return coordinates_x


def train_for_each(coordinates_x_y, users_parameters, features_arr, train):
    for i in range(0, 10):
        print(i)
        params_arr = []
        for j in range(0, len(coordinates_x_y)):
            coord_x = coordinates_x_y[j][0]
            coord_y = coordinates_x_y[j][1]
            function_param = users_parameters[j]
            new_params = polynomial_trainer_cf(coord_x, coord_y, function_param, iterations=1)
            params_arr.append(new_params)
        users_parameters = params_arr[:]
        parameters_x_y = params_connect(users_parameters, train, features_arr)
        for k in range(len(parameters_x_y[0]) - 1, -1, -1):
            bufor = features_arr[k][0]
            features_arr[k][0] = 1
            parameters_x = parameters_x_y[0][k]
            parameters_y = parameters_x_y[1][k]
            features = [[1, 1], features_arr[k], [0, 1]]
            new_features = polynomial_trainer_cf(parameters_x, parameters_y, features, iterations=1)
            features_arr[k] = [bufor, new_features[1][1]]
            break
        if i % 10 == 0:
            print(users_parameters[1:10])
        data_for_regress = data_to_train(train, features_arr)
        coordinates_x_y = coordinates_from_data(data_for_regress)
    print()
    print(users_parameters)
    print()
    print(features_arr)
    return users_parameters, features_arr


def prediction(tasks, users_parameters, cord_x):
    for i in range(0, (len(tasks))):
        user_parameter = users_parameters[i]
        for j in range(0, len(tasks[i])):
            movie = tasks[i][j][2]
            movie_feature = cord_x[movie - 1][1]
            predicted_value = movie_feature * user_parameter[1][1] + user_parameter[2][1]
            predicted_value = round(abs(predicted_value))
            if predicted_value < 0:
                predicted_value = 0
            if predicted_value > 5:
                predicted_value = 5
            tasks[i][j][3] = predicted_value
    return tasks


def write_data_cf(name, tasks):
    print(name)
    f = open(str(name) + ".csv", "w")
    for input_data in tasks:
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


def main():
    labels = read_data_set_cf("../predictionFiles/movie_labels.csv", ";")
    train = get_trainers()
    tasks = get_tasks()
    features_no = 1
    users_parameters = get_parameters(train, features_no)
    features_arr = get_features(labels, features_no)
    data_for_regress = data_to_train(train, features_arr)
    coordinates_x_y = coordinates_from_data(data_for_regress)
    params_and_features = train_for_each(coordinates_x_y, users_parameters, features_arr, train)
    predict_sores = prediction(tasks, params_and_features[0], params_and_features[1])
    write_data_cf("submission", predict_sores)


if __name__ == '__main__':
    main()
