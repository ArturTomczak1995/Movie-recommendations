import requests
import json
from api_key import get_api_key


api_key = get_api_key
labels = ["vote_average", "vote_count", "popularity", "revenue"]
user_id = 1
user_movie_id = 2
user_score = 3


def movie_url(id):
    movie_url_data = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + api_key + "&language=en-US"
    return movie_url_data


def read_data_set(input_file, delimiter):
    retrieved_data = []
    data_in = open(input_file, "r")
    for f in data_in:
        spl = map(str, f.rstrip('\n').split(delimiter))
        retrieved_data.extend([[x for x in spl]])
    return retrieved_data


def split_data(x_norm, splits):
    x_norm_out = []
    while len(x_norm) > splits:
        part = x_norm[:splits]
        x_norm_out.append(part)
        x_norm = x_norm[splits:]
    x_norm_out.append(x_norm)
    return x_norm_out


def get_movie_data(movie_id):
    response = requests.get(movie_url(movie_id))
    if response.status_code == 200:
        resp_dict = json.loads(response.text)
        # print(movie_id, "true")
        return resp_dict
    else:
        # print(movie_id, "false")
        return False


def write_data(i, input_data):
    f = open("data/file" + str(i) + ".txt", "w")
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


def get_movies_labels(movie_info, movie_id):
    # movie_title = '\"' + movie_title + '\"'
    revenue = int(movie_info["revenue"])
    budget = int(movie_info["budget"])
    vote_average = movie_info["vote_average"]
    genres = movie_info["genres"]
    genres_arr = []
    for genre in genres:
        genres_arr.append(genre["name"])
    # profit = revenue - budget
    return [movie_id, vote_average, genres_arr]


def get_movies():
    data_to_split = read_data_set("../predictionFiles/ovie.csv", ";")
    movie_info_cleaned = []
    for i in range(0, len(data_to_split)):
        movie_id = data_to_split[i][0]
        movie_id_in_db = data_to_split[i][1]
        movie_info = get_movie_data(movie_id=movie_id_in_db)
        movie_labels = get_movies_labels(movie_info, movie_id)
        movie_info_cleaned.append(movie_labels)
        print(movie_info_cleaned)
    write_data(0, movie_info_cleaned)


if __name__ == '__main__':
    get_movies()
