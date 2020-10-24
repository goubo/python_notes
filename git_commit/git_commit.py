import random
import os
import datetime

start = "2020-01-01"
end = "2020-12-31"

week_commit_probability = [80, 80, 80, 80, 80, 60, 40]

commit_num = 30
deviation = 10

git_path = "/Users/bobo/my/java-tool"


def git_commit(date):
    md5_path = git_path + "/md5"
    if not os.path.exists(md5_path):
        os.system(r"touch {}".format(md5_path))
    commit_count = random.randint(deviation, commit_num)
    if random_index(50):
        commit_count += deviation
    else:
        commit_count -= deviation
    os.system("md5 " + md5_path + " > " + md5_path)
    os.system("git add . ")
    os.system('git commit -m "1" --date ' + date)


def gen_commit_date():
    if not start:
        start_time = datetime.date(datetime.date.today().year, 1, 1)
    else:
        start_time = datetime.datetime.strptime(start, '%Y-%m-%d').date()

    if not end:
        end_time = datetime.date.today()
    else:
        end_time = datetime.datetime.strptime(end, '%Y-%m-%d').date()

    if start_time > end_time:
        print('结束时间大于开始时间,参数错误')

    while start_time < end_time:
        if random_index(week_commit_probability[start_time.weekday()]):
            print(start_time)
        start_time += datetime.timedelta(days=1)


def random_index(rate):
    return random.randint(1, 100) < (rate + 1)


if __name__ == '__main__':
    git_commit("2020-10-24")
# print(datetime.date.today().weekday())
# gen_commit_date()
