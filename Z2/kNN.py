from operator import itemgetter
from threading import Thread
import re
import os

max_labels_len = 0
sorted_labels = []
scores_arr = []


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


def get_tasks():
    data = read_data_set("../predictionFiles/task.csv", ";")
    urs_split = split_by_user(data, 1)
    split_separate = separate_data(urs_split)
    return split_separate


def get_trainers():
    data = read_data_set("../predictionFiles/train.csv", ";")
    trn_split = split_by_user(data, 1)
    trn_separate = separate_data(trn_split)
    return trn_separate


def max_genres_len(labels, label_pos):
    labels_col = take_column(labels, label_pos)
    row_col_len = []
    for i in labels_col:
        row_col_len.append(len(i))
    return max(row_col_len)


def take_column(matrix, i):
    return [row[i] for row in matrix]


def score_difference(labels, score):
    for i in range(0, len(labels)):
        score_diff = abs(score - labels[i][1][1])
        labels[i][0] += score_diff
    return labels


def get_similar_labels(labels, label, label_pos):
    label_arr = []
    for label_i in labels:
        flag = 0
        for j in label[label_pos]:
            if j in label_i[label_pos]:
                flag += 1
        if flag:
            diff = abs(len(label_i[label_pos]) - flag)
            if flag == len(label[2]):
                diff -= 1
            label_arr.append([diff, label_i])
    return label_arr


def similar_labels(user_label):
    score = user_label[1]
    sorted_labels_cp = sorted_labels[:]
    same_genres = get_similar_labels(sorted_labels_cp, user_label, label_pos=2)
    score_diff = score_difference(labels=same_genres, score=score)
    same_genres = sorted(score_diff, key=lambda a_entry: a_entry[0])
    print(same_genres)
    for i in range(0, len(same_genres)):
        same_genres[i] = same_genres[i][1]
    return same_genres


def get_prediction_arr(label_arr, train_arr, neighbours):
    flag = 0
    prediction_arr = []
    for label in label_arr:
        for train in train_arr:
            if label[0] == train[2]:
                prediction_arr.append(train)
                flag += 1
                if flag == neighbours:
                    return prediction_arr
    return prediction_arr


def most_common(lst):
    lst_sort = sorted(lst)
    # try:
    #     times_occur = max(set(lst), key=lst.count)
    # except ValueError:
    #     return randint(0, 5)
    # last_no_bufor = -1
    # dominant_arr = []
    # for l_srt in lst_sort:
    #     if l_srt != last_no_bufor:
    #         times_occur_bfr = lst.count(l_srt)
    #         if times_occur_bfr == times_occur:
    #             dominant_arr.append(l_srt)
    #     last_no_bufor = l_srt
    # if not dominant_arr:
    #     return times_occur
    avg_score = sum(lst_sort) / float(len(lst_sort))
    return avg_score


def get_average_score(label_arr, train_arr):
    neighbours = 7
    prediction_arr = get_prediction_arr(label_arr, train_arr, neighbours)
    score_col = take_column(matrix=prediction_arr, i=3)
    avg_score = most_common(score_col)
    return round(avg_score)


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


def get_predictions(split_task, split_train, labels, file_no):
    task_arr = []
    for i in range(0, len(split_task)):
        for every_task in split_task[i]:
            user_label = labels[every_task[2] - 1]
            sim_lab = similar_labels(user_label=user_label)
            average_score = get_average_score(sim_lab, split_train[i])
            every_task[3] = average_score
            task_arr.append(every_task)
    write_data(input_data=task_arr, name="save/file" + str(file_no))


def threads(tasks, train, labels):
    global sorted_labels, scores_arr
    sorted_labels = sorted(labels, key=itemgetter(1))
    scores_arr = take_column(sorted_labels, 1)
    thread = []
    for i in range(0, len(tasks)):
        thread.append(Thread(target=get_predictions, args=(tasks[i], train[i], labels, i,)))
        thread[i].start()


def connect_results():
    files = os.listdir("save")
    data = []
    for file in files:
        content = read_data_set(input_file="save/" + file, delimiter=";")
        for i in content:
            data.append(i)
    sort_data = sorted(data, key=itemgetter(0))
    write_data(name="submission", input_data=sort_data)


def main():
    global max_labels_len
    labels = read_data_set("../predictionFiles/movie_labels.csv", ";")
    train = get_trainers()
    tasks = get_tasks()
    max_labels_len = max_genres_len(labels, label_pos=2)
    threads(tasks, train, labels)
    connect_results()


if __name__ == '__main__':
    main()
