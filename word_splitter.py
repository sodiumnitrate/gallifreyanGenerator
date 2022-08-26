splitters = ["PH","WH","GH","CH","SH","QU","NG"]
vowels = ['A','E','I','O','U']

def split(word,splitter):
    new = word.split(splitter)
    new_grouping = []
    for group in new:
        if len(group) == 0:
            new_grouping.append(splitter)
        else:
            new_grouping.append(group)
            new_grouping.append(splitter)
    return new_grouping[:-1]

def split_double(word,splitter):
    if isinstance(word, str):
        word = [word]
    new = []
    for group in word:
        b = split(group,splitter)
        for el in b:
            new.append(el)

    return new

def split_splitters(word):
    splitters = ["PH","WH","GH","CH","SH","QU","NG"]
    for splitter in splitters:
        word = split_double(word,splitter)

    return word

def separate_non_splitters(word):
    splitters = ["PH","WH","GH","CH","SH","QU","NG"]
    new = []
    for group in word:
        if group not in splitters:
            for letter in group:
                new.append(letter)
        else:
            new.append(group)

    return new

def merge_vowels(word):
    vowels = ['A','E','I','O','U']
    new = []
    for i,group in enumerate(word):
        if i==0:
            new.append(group)
        if i>0:
            if group in vowels:
                prev_group = word[i-1]
                if prev_group[-1] in vowels:
                    new.append(group)
                else:
                    new[-1] += group
            else:
                new.append(group)

    return new

def get_split_word(word):
    separated = separate_non_splitters(split_splitters(word))
    return merge_vowels(separated)