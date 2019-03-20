from operator import itemgetter
from threading import Thread
import os
import re


max_labels_len = 1
score_arr = []


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


def read_data_set(input_file, delimiter):
    retrieved_data = []
    data_in = open(input_file, "r")
    for f in data_in:
        spl = f.rstrip('\n').split(delimiter)
        type_arr = type_changer(spl)
        retrieved_data.extend([[x for x in type_arr]])
    return retrieved_data


def separate_data(data):
    bufor = data[0][1]
    spl_data_arr = []
    bufor_arr = []
    for i in data:
        if i[1] != bufor:
            spl_data_arr.append(bufor_arr)
            bufor_arr = []
        bufor_arr.append(i)
        bufor = i[1]
    spl_data_arr.append(bufor_arr)
    return spl_data_arr


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


def get_trainers():
    data = read_data_set("../predictionFiles/train.csv", ";")
    trn_split = split_by_user(data, 1)
    trn_separate = separate_data(trn_split)
    return trn_separate


def get_tasks():
    data = read_data_set("../predictionFiles/task.csv", ";")
    urs_split = split_by_user(data, 1)
    split_separate = separate_data(urs_split)
    return split_separate


def transform_data(data, label_pos):
    for i in data:
        i[label_pos] = [i[label_pos]]
    return data


def take_column(matrix, i):
    return [row[i] for row in matrix]


def most_common(lst):
    return max(set(lst), key=lst.count)


def max_genres_len(labels, label_pos):
    labels_col = take_column(labels, label_pos)
    row_col_len = []
    for i in labels_col:
        row_col_len.append(len(i))
    return max(row_col_len)


def get_similar_labels(labels, label, label_pos):
    label_len = len(labels[0][label_pos])
    label_arr = []
    for label_i in labels:
        flag = 0
        for j in label[label_pos]:
            if j in label_i[label_pos]:
                flag += 1
        if flag:
            diff = abs(len(label_i[label_pos]) - flag)
            if label_len > 1:
                label_arr.append([diff, label_i])
            else:
                label_arr.append(label_i)
    return label_arr


def get_similar_score(labels, user_label):
    similar_movies = get_similar_labels(labels, user_label, label_pos=2)
    similar_scores = get_similar_labels(similar_movies, user_label, label_pos=3)
    return similar_scores


def write_data(name, input_data):
    print(name)
    f = open(str(name) + ".csv", "w")
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


def sort_by_val(iterations, value_matrix, val, matrix):
    sorted_by_val = []
    for i in range(0, iterations):
        idx_score = value_matrix.index(min(value_matrix, key=lambda x: abs(x - val)))
        sorted_by_val.append(matrix[idx_score])
        del value_matrix[idx_score]
        del matrix[idx_score]
    return sorted_by_val


def get_scores(scr_arr, tasks, labels):
    usr_lst = take_column(scr_arr, 1)
    mst_cmm_usr = most_common(usr_lst)
    for task in tasks:
        mst_cmm_usr_cp = mst_cmm_usr
        flag = 0
        while task[3] == ["NULL"]:
            for lbl in labels:
                if mst_cmm_usr_cp == lbl[1]:
                    if task[2] == lbl[2][0]:
                        task[3] = lbl[3][0]
            if task[3] != ["NULL"]:
                break
            while mst_cmm_usr_cp in usr_lst:
                flag += 1
                usr_lst.remove(mst_cmm_usr_cp)
            mst_cmm_usr_cp = most_common(usr_lst)
    return tasks


def get_predictions(split_task, labels, usr_train, file_no):
    for i in usr_train[0]:
        i[2] = [i[2]]
        i[3] = [i[3]]
        labels.remove(i)

    score_array = []
    for train_lbl in usr_train[0]:
        sim_score = get_similar_score(labels=labels, user_label=train_lbl)
        score_array += sim_score
    scores = get_scores(score_array, split_task[0], labels)
    write_data(input_data=scores, name="save/file" + str(file_no))


def threads(tasks, labels, trainers):
    thread = []
    for i in range(0, len(tasks)):
        thread.append(Thread(target=get_predictions, args=(tasks[i], labels, trainers[i], i,)))
        thread[i].start()
        thread[i].join()


def connect_results():
    files = os.listdir("save")
    data = []
    for file in files:
        content = read_data_set(input_file="save/" + file, delimiter=";")
        for i in content:
            data.append(i)
    sort_data = sorted(data, key=itemgetter(0))
    write_data(name="predictions", input_data=sort_data)


def main():
    tasks = get_tasks()
    trainers = get_trainers()
    train_data = read_data_set("../predictionFiles/train.csv", ";")
    train_data_transform_format = transform_data(train_data, label_pos=2)
    train_data_transform_format_2 = transform_data(train_data_transform_format, label_pos=3)
    threads(tasks=tasks, labels=train_data_transform_format_2, trainers=trainers)
    connect_results()


if __name__ == '__main__':
    main()
