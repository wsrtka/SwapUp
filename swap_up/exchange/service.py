"""Skracanie nazw"""

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

"""Tworzenie słownika do wyświetlania przedmiotu"""

def create_class_dict(c):
        class_dict = {}

        subject = c.subject_id
        teacher = c.teacher_id

        class_dict['id'] = str(c.id)


        class_dict['subject_name'] = str(subject.subject_name)
        class_dict['category'] = str(subject.category)
        class_dict['capacity'] = str(c.capacity)
        class_dict['teacher'] = str(teacher.first_name) + " " + str(teacher.last_name)
        class_dict['room'] = str(c.room)
        class_dict['week'] = str(c.week)
        class_dict['week'] = str(c.week)


        hour_start, minute_start, seconds_start = str(c.time).split(':')
        hour_start, minute_start = int(hour_start), int(minute_start)
        hour_end, minute_end = hour_start, minute_start
        minute_end += 90
        while minute_end >= 60:
            hour_end += 1
            minute_end -= 60

        class_dict['time'] = str(hour_start) + ":" + "{:02d}".format(minute_start) + " - " + str(
            hour_end) + ":" + "{:02d}".format(minute_end)

        # Template from 7:30 to 20:00 (13 h total)

        #arrange top and bottom position of div in display
        time_from = 7.5
        time_to = 20


        class_dict['top'] = 100 * (hour_start + minute_start / 60 - time_from) / (time_to - time_from)
        class_dict['bottom'] = 100 * (time_to - hour_end - minute_end / 60) / (time_to - time_from)


        class_dict['start'] = hour_start + minute_start/60
        class_dict['end'] = hour_end + minute_end/60

        return class_dict


def count_collisions(c, class_dict, schedule):
    class_dict['colliders'] = []
    class_dict['collider_id'] = 0
    
    try:
        for other_class in schedule[str(c.day)]:
            if (class_dict['end'] >= other_class['start'] >= class_dict['start']) or ( class_dict['end'] >= other_class['end'] >= class_dict['start']) :

                if other_class not in class_dict['colliders']:
                    class_dict['colliders'].append(other_class)
                if class_dict not in other_class['colliders']:
                    other_class['colliders'].append(class_dict)

                for other_class_collider in other_class['colliders']:
                    if other_class_collider not in class_dict['colliders']:
                        class_dict['colliders'].append(other_class_collider)
                    if class_dict not in other_class_collider['colliders']:
                        other_class_collider['colliders'].append(class_dict)

                if class_dict in class_dict['colliders']:
                    class_dict['colliders'].remove(class_dict)

                class_dict['collider_id'] = len(class_dict['colliders'])
    except:
        #exception occurs in case of wrong day in database
        pass

    try:
        schedule[str(c.day)].append(class_dict)
    except:
        pass

def arrange_horizontal_position(schedule):
    for day in ('Pn', 'Wt', 'Śr', 'Czw', 'Pt'):
        for class_dict in schedule[day]:
            n = len(class_dict['colliders']) + 1
            i = class_dict['collider_id']

            class_dict['width'] = 100/n
            class_dict['left'] = (i) * (100/n)
            #truncate text
            class_dict['short_subject_name'], class_dict['short_time'], class_dict['short_teacher'] = shorten(class_dict['subject_name'],class_dict['time'],class_dict['teacher'],n)
