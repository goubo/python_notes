import random
import os
import datetime

start = "2020-02-01"
end = "2020-12-31"
git_path = "/Users/bobo/my/java-tool"
week_commit_probability = [80, 80, 80, 80, 80, 60, 40]

commit_num = 30
deviation = 10

os.chdir(git_path)


def git_commit(date):
    md5_path = git_path + "/md5"
    if not os.path.exists(md5_path):
        os.system(r"touch {}".format(md5_path))
    commit_count = random.randint(deviation, commit_num)
    if random_index(50):
        commit_count += deviation
    else:
        commit_count -= deviation
    for num in range(0, commit_count):
        os.system("pwd")
        os.system("echo '{}_{}' > md5".format(date, num))
        os.system("git add .")
        os.system('git commit -a -m "{}_{}" --date {}'.format(date, num, date))


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
            git_commit(start_time)
        start_time += datetime.timedelta(days=1)


def random_index(rate):
    return random.randint(1, 100) < (rate + 1)


if __name__ == '__main__':
    gen_commit_date()
