from itertools import product

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
        # print(t_k)
        for char in t_k:
            if not ((char in SIGMA) or (char in GAMMA)):
                # print(char)
                return False
    for i in range(2+k, len(content)):
        r_i = content[i]
        if not r_i[0] in GAMMA:
            return False
        if not r_i[1] == ':':
            return False
        r_i_translations = r_i[2:].split(",")
        # print(r_i_translations)
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

def repeats(s, substring):
    return max((i for i in range(1, s.count(substring) + 1) if substring * i in s), default=0)

def heu_subsequent_Gamma_appearances(input_dict):
    # The translations for GAMMA character 'A' must all be substrings of 's.' 
    # If, for example, GAMMA character 'A' appears three times in a row in one of the 't_k' strings, 
    # then its translations must also appear as substrings in 's' three times in a row. 
    max_repats = [max([repeats(t, gamma_char) for t in input_dict['ts']]) for gamma_char in input_dict['Rs'].keys()]
    for gamma_char, max_repat in zip(input_dict["Rs"].keys(), max_repats):
        translation = input_dict["Rs"][gamma_char]
        translation = [
            element for element in translation if element*max_repat in input_dict["s"]]
        input_dict["Rs"][gamma_char] = translation
    return not empty_solution_space(input_dict)

def heu_ts_with_Sigma_letters(input_dict):
    return True

def translate(translation_mapping, t):
    t_translated = t
    for gamma_char in translation_mapping.keys():
        t_translated = t_translated.replace(gamma_char, translation_mapping[gamma_char])
    return t_translated

def check_translation_mapping(translation_mapping, ts, input_dict):
    for t in ts:
        t_translated = translate(translation_mapping, t)
        if t_translated not in input_dict["s"]:
            return False
    return True 

def exhaustive_search(input_dict):
    gamma_chars = list(input_dict["Rs"].keys())
    for configs in product(*[input_dict["Rs"][gamma_char] for gamma_char in gamma_chars]):
        translation_mapping = {gamma_char: config for gamma_char, config in zip(gamma_chars, configs)}
        if check_translation_mapping(translation_mapping, input_dict['ts'], input_dict):
            return True, translation_mapping
    return False, None

def solve_t(t, input_dict):
    gamma_chars = list(input_dict['Rs'])
    gamma_chars_in_t = [gamma_char for gamma_char in gamma_chars if gamma_char in t]
    new_translations = {gamma_char: [] for gamma_char in gamma_chars}
    for configs in product(*([input_dict['Rs'][gamma_char][0]] if gamma_char not in t else input_dict['Rs'][gamma_char] for gamma_char in gamma_chars)):
        translation_mapping = {gamma_char: config for gamma_char, config in zip(gamma_chars, configs)}
        if check_translation_mapping(translation_mapping, [t], input_dict):
            for gamma_char_in_t in gamma_chars_in_t:
                new_translations[gamma_char_in_t].append(translation_mapping[gamma_char_in_t])
    for gamma_char in gamma_chars:
        new_translations[gamma_char] = list(set(new_translations[gamma_char]) if gamma_char in t else input_dict['Rs'][gamma_char])
    input_dict['Rs'] = new_translations

def empty_solution_space(input_dict):
    return 0 in [len(input_dict["Rs"][gamma_char]) for gamma_char in input_dict["Rs"].keys()]

def heu_solve_ts(input_dict):
    # When examining 'ts' one at a time, if we determine that gamma character 'A' 
    # cannot be translated to sigma character 'a' in the first string, we can eliminate this translation. 
    for t in sorted(input_dict['ts'], key=len):
        solve_t(t, input_dict)
        if empty_solution_space(input_dict):
            return False
    return True

def heu_Gamma_letter_not_in_any_t(input_dict):
    # if a letter gamma doesn't appear in any t, we can just set it to something arbitrary. 
    all_ts = ""
    for t in input_dict["ts"]:
        all_ts += t
    for gamma_char in input_dict["Rs"].keys():
        if gamma_char not in all_ts:
            input_dict["Rs"][gamma_char] = [input_dict["Rs"][gamma_char][0]]
    return not empty_solution_space(input_dict)

def solve(input_dict):
    # 3. Heuristics
    if not heu_subsequent_Gamma_appearances(input_dict):
        return False, None
    if not heu_ts_with_Sigma_letters(input_dict):
        return False, None
    if not heu_Gamma_letter_not_in_any_t(input_dict):
        return False, None
    if not heu_solve_ts(input_dict):
        return False, None
    # 4. Exhaustive search
    succes, sol = exhaustive_search(input_dict)
    return succes, sol

def main():
    # 1. Read input
    file_path = 'examples/test02.swe'
    with open(file_path, "r", encoding="ASCII") as f:
        content = f.readlines()
        content = [x.strip() for x in content]  # remove \n
    # 2. Check if format is correct        
    if not check_input(content):
        print("wrongly formatted content")
        return
    input_dict = construct_dict(content)
    succes, sol = solve(input_dict)
    print(succes)
    print(sol)

if __name__ == "__main__":
    main()
