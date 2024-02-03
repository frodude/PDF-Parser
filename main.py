import models


def main():
    # the 5 functions that will be looped through on each line
    functions = [models.titles, models.description, models.part_numbers, models.options, models.oem_year]

    # reading in entire file
    with open('for testing.txt', 'r') as file:
        lines = file.readlines()

    # stripping the new line from all lines
    lines = [l.strip('\n') for l in lines]
    # instance of PartEntry class that will hold a certain part
    pe = models.PartEntry()
    # holds all the parts' data
    all_parts_data = []

    # traversing file lines
    for ln, line in enumerate(lines):
        # looping through every function with each line
        for f in functions:
            fn_result = f(line)

            # if title
            if not pe.title_satisfied and fn_result[0] == 'title' and fn_result[1] is not None:
                pe.data['title'] = fn_result[1]
                pe.title_satisfied = True
                pe.starting_line_number = ln
                continue
            # when encountering next title, meaning we are done with previous part
            elif pe.title_satisfied and fn_result[0] == 'title' and fn_result[1] is not None:
                models.cleanup(pe)
                pe.ending_line_number = ln
                # new instance aka resetting
                all_parts_data.append(pe)
                pe = models.PartEntry()

                # assigning title to the new instance of partEntry
                pe.data['title'] = fn_result[1]
                pe.title_satisfied = True
                continue
            # if description
            elif not pe.desc_satisfied and fn_result[0] == 'description' and fn_result[1] is not None:
                pe.data['description'] += (" " + fn_result[1])
                continue
            # if part number
            elif not pe.pn_satisfied and fn_result[0] == 'part_numbers' and fn_result[1] is not None:
                pe.desc_satisfied = True
                pe.data['part_numbers'].extend(fn_result[1])
                continue
            # if options
            elif not pe.options_satisfied and fn_result[0] == 'options' and fn_result[1] is not None:
                pe.pn_satisfied = True
                pe.data['options'].append(fn_result[1])
                continue
            # if oems
            elif not pe.oems_satisfied and fn_result[0] == 'oems' and fn_result[1] is not None:
                pe.options_satisfied = True
                pe.pn_satisfied = True
                pe.data['oems'].append(fn_result[1])
                continue

    # appending the very last entry in the file
    models.cleanup(pe)
    all_parts_data.append(pe)

    # expanding the data into all_dicts_data before dumping into json
    all_dicts_data = [e.data for e in all_parts_data]
    models.json_dump(all_dicts_data)


if __name__ == "__main__":
    main()