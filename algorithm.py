# import os

SIGMA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
GAMMA = [x.upper() for x in SIGMA]


def check_input(content):
    k = None
    try:
        k = int(content[0])
    except ValueError:
        return False
    for char in content[1]:
        if char not in SIGMA:
            return False
    for i in range(2, 2+k):
        t_k = content[i]
        print(t_k)
        for char in t_k:
            if not ((char in SIGMA) or (char in GAMMA)):
                print(char)
                return False
    for i in range(2+k, len(content)):
        r_i = content[i]
        if not r_i[0] in GAMMA:
            return False
        if not r_i[1] == ':':
            return False
        r_i_translations = r_i[2:].split(",")
        print(r_i_translations)
        for r_i_translation in r_i_translations:
            for char in r_i_translation:
                if (char not in SIGMA) or char == '':  # TODO: check for empty char
                    return False
    return True

# {"length":,
#  "s":
#  "ts": [],
#  "Rs": {"A": []}}


def construct_dict(content):
    input_dict = {}
    k = int(content[0])
    input_dict['k'] = k
    input_dict['s'] = content[1]

    ts = content[2:2+k]
    input_dict['ts'] = ts

    Rs = {}
    for i in range(2+k, len(content)):
        line = content[i]
        gamma_letter = line[0]
        Ri = line[2:].split(",")
        Rs[gamma_letter] = Ri

    input_dict['Rs'] = Rs

    return input_dict


def check_translations_substrings_in_s(input_dict):
    for gamma_char in input_dict["Rs"].keys():
        translation = input_dict["Rs"][gamma_char]
        translation = [
            element for element in translation if element in input_dict["s"]]
        input_dict["Rs"][gamma_char] = translation


def check_ts_with_Sigma_letters(input_dict):
    pass


def brute_force_the_rest(input_dict):
    pass


def solve(input_dict):
    check_translations_substrings_in_s(input_dict)
    check_ts_with_Sigma_letters(input_dict)
    brute_force_the_rest(input_dict)


if __name__ == "__main__":
    # print(os.getcwd())
    # 1. Read input
    file_path = 'examples/test01.swe'
    with open(file_path, "r", encoding="ASCII") as f:
        content = f.readlines()
        content = [x.strip() for x in content]  # remove \n
        print(content)
        print(check_input(content))
        input_dict = construct_dict(content)
        print(input_dict)
        check_translations_substrings_in_s(input_dict)
        print(input_dict['Rs'])

    # 2. Check if format is correct
    # 3. Heuristics
