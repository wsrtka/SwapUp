def shorten_subject_name(name, level):
    levels_max_sizes = {1:40, 2:20, 3:14, 4: 9}
    
    words = name.split(" ")

    if level >= 5:
        if len(words) == 2 and words[1].isnumeric():
            return words[0][0:5] + "" + words[1]

        if len(words) == 1:
            return words[0][0:7]
        
        return "".join(e[0] for e in name.split())
    
    if len(name) > levels_max_sizes[level]:

        to_cut = len(name) - levels_max_sizes[level]
        if len(words) == 2:
            return strip_two_words(words,to_cut)
        if len(words) == 3 and words[2].isnumeric():
            return strip_two_words(words, to_cut) + " " + words[2]
    
        return "".join(e[0] for e in name.split())    
    return name



def strip_two_words(words, to_cut):
    if (len(words[0])>= to_cut + 3) and words[0][2] not in ('a', 'e', 'i', 'o', 'u'):
        words[0] = words[0][0:3]
        return " ".join((words[0],words[1],str(number)))  
    to_cut -= (len(words[0]) - 4)
    words[0] = words[0][0:4]

    words[1] = words[1][0: (len(words[1]) - to_cut)]
    return " ".join((words[0],words[1]))

def shorten_time(time, level):
    if level >= 4:
        return time[0:5]
    else:
        return time

def shorten_teacher(teacher, level):
    levels_max_sizes = {1:40, 2:20, 3:14, 4: 9, 5: 6}

    if level>=6:
        return teacher.split(" ")[0][0] + "." + teacher.split(" ")[1][0] + "." 

    if  len(teacher) > levels_max_sizes[level]:
        teacher = teacher.split(" ")[0][0] + " " + teacher.split(" ")[1]

    if len(teacher) > levels_max_sizes[level]:
        if '-' in teacher.split(" ")[1]:
            teacher = teacher.split(" ")[0][0] + " " + teacher.split(" ")[1].split("-")[0][0] + "-" +  teacher.split(" ")[1].split("-")[1]

    return teacher[0:levels_max_sizes[level]]

def shorten(subject, time, teacher, level):
    subject_short, time_short, teacher_short = subject, time, teacher
    try:
        subject_short = shorten_subject_name(subject, level)
        time_short = shorten_time(time, level)
        teacher_short = shorten_teacher(teacher, level)
    finally:
        return subject_short, time_short, teacher_short