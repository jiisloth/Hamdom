import argparse
import os.path
import colorsys
import random


class Leaf:
    def __init__(self, name):
        self.name = name
        self.values = []


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def create_tree(file):
    tree = Leaf("root")
    path = [tree]
    current = tree
    for i, line in enumerate(file):
        if '"' in line:  # valuepair
            valuepair = line.strip().split('" "')
            current.values.append([valuepair[0][1:], valuepair[1][:-1]])
        elif '{' == line.strip():  # open
            path.append(current)
        elif '}' == line.strip():  # close
            path.pop()
            current = path[-1]
        else:  # class
            new = Leaf(line.strip())
            current.values.append(new)
            current = new

    return tree


def rotate(entities, args):
    r = {'y': [], 'z': [], 'x': []}
    order = ['y', 'z', 'x']
    editing = ['y', 'z', 'x']
    wasnum = True
    for arg in args:
        if arg[0] == '~' and is_number(arg[1:]):
            wasnum = True
            for axis in editing:
                r[axis].append(arg[1:])
        elif is_number(arg):
            wasnum = True
            for axis in editing:
                r[axis].append(float(arg))
        else:
            for axis in r.keys():
                if axis in arg.lower():
                    if wasnum:
                        editing = []
                        wasnum = False
                    editing.append(axis)

    found = 0
    for entity in entities:
        for value in entity.values:
            if type(value) == list:
                if value[0] == "angles":
                    found += 1
                    if not args:

                        value[1] = str(random.randint(0, 360 * 10 - 1) / 10) + " " + \
                                   str(random.randint(0, 360 * 10 - 1) / 10) + " " + \
                                   str(random.randint(0, 360 * 10 - 1) / 10)
                    else:
                        orgs = value[1].split(" ")
                        orgs = {'y': orgs[0], 'z': orgs[1], 'x': orgs[2]}

                        angles = []
                        for axis in order:
                            if len(r[axis]) == 1:
                                if type(r[axis][0]) == str:
                                    r[axis].append('0')
                                else:
                                    r[axis].append(0)
                            if len(r[axis]) == 2:
                                if type(r[axis][0]) == str:
                                    r[axis][0] = float(r[axis][0]) + float(orgs[axis])
                                if type(r[axis][1]) == str:
                                    r[axis][1] = float(r[axis][1]) + float(orgs[axis])
                                r[axis] = sorted(r[axis])
                                angles.append(str(random.randint(r[axis][0]*10, r[axis][1]*10)/10))

                            elif len(r[axis]) > 2:
                                print("Too many values in rotation for " + axis.upper() + "-axis!")
                                exit()
                        value[1] = " ".join(angles)
    return found


def colorize(entities, args):
    c = {'h': [], 's': [], 'b': []}
    order = ['h', 's', 'b']
    editing = ['h', 's', 'b']
    wasnum = True
    for arg in args:
        if arg[0] == '~' and is_number(arg[1:]):
            wasnum = True
            for cv in editing:
                c[cv].append(arg[1:])
        elif is_number(arg):
            wasnum = True
            for cv in editing:
                c[cv].append(float(arg))
        else:
            for cv in c.keys():
                if cv in arg.lower():
                    if wasnum:
                        editing = []
                        wasnum = False
                    editing.append(cv)

    found = 0
    for entity in entities:
        for value in entity.values:
            if type(value) == list:
                if value[0] == "rendercolor":
                    found += 1
                    if not args:
                        r, g, b = colorsys.hsv_to_rgb(random.randint(0, 3600)/3600,
                                                      random.randint(0, 1000)/1000,
                                                      random.randint(0, 1000))/1000
                        value[1] = str(r) + " " + str(g) + " " + str(b)
                    else:
                        orgs = value[1].split(" ")
                        h, s, b = colorsys.rgb_to_hsv(float(orgs[0])/255, float(orgs[1])/255, float(orgs[2])/255)
                        orgs = {'h': h, 's': s, 'b': b}

                        colorvalues = []
                        for cv in order:
                            if len(c[cv]) == 1:
                                if type(c[cv][0]) == str:
                                    c[cv].append('0')
                                else:
                                    c[cv].append(0)
                            if len(c[cv]) == 2:
                                if type(c[cv][0]) == str:
                                    c[cv][0] = float(c[cv][0]) + float(orgs[cv])
                                if type(c[cv][1]) == str:
                                    c[cv][1] = float(c[cv][1]) + float(orgs[cv])
                                c[cv] = sorted(c[cv])
                                colorvalues.append(random.randint(c[cv][0] * 10, c[cv][1] * 10) / 10)

                            elif len(c[cv]) > 2:
                                print("Too many values in colorization for " + cv.upper() + "-value!")
                                exit()
                        r, g, b = colorsys.hsv_to_rgb(colorvalues[0]/360, colorvalues[1]/100, colorvalues[2]/100)

                        value[1] = " ".join(["{0:.2f}".format(r), "{0:.2f}".format(g), "{0:.2f}".format(b)])

    return found


def scale(entities, args):
    s = []
    for arg in args:
        if arg[0] == '~' and is_number(arg[1:]):
            s.append(arg[1:])
        elif is_number(arg):
            s.append(float(arg))
        else:
            print("Error parsing argument for scale operation.")

    found = 0
    for entity in entities:
        for value in entity.values:
            if type(value) == list:
                if value[0] == "uniformscale":
                    found += 1
                    if not args:
                        print("No values given for scaling.")
                        exit()
                    else:
                        org = value[1]

                        if len(s) == 1:
                            if type(s[0]) == str:
                                s.append('0')
                            else:
                                s.append(0)
                        if len(s) == 2:
                            if type(s[0]) == str:
                                s[0] = float(s[0]) + float(org)
                            if type(s[1]) == str:
                                s[1] = float(s[1]) + float(org)
                            s = sorted(s)
                            value[1] = str(random.randint(s[0] * 10, s[1] * 10) / 10)

                        elif len(s) > 2:
                            print("Too many values in colorization for scaling!")
                            exit()

    return found


def testfile(new, old):
    errors = []
    for i, line in enumerate(new):
        if line != old[i]:
            errors.append("Line " + str(i) + ":" + old[i])
    if errors:
        print("Error while parsing input file:")
        for i, error in enumerate(errors):
            print(error)
            if i > 10:
                break
        print(str(len(errors)) + " errors found!")


def print_leaf(node, tab=0):
    file = ""
    for value in node.values:
        if type(value) == list:
            file += tab * "	" + '"' + value[0] + '" "' + value[1] + '"\n'
        else:
            file += tab * "	" + value.name + '\n'
            file += tab * "	" + '{\n'
            tab += 1
            file += print_leaf(value, tab)
            tab -= 1
            file += tab * "	" + '}\n'
    return file


def get_entities(root, selectors):
    entities = []
    for value in root.values:
        if type(value) != list:
            if value.name == "entity":
                entity = check_entity(value, selectors)
                if entity:
                    entities.append(entity)
    return entities


def check_entity(entity, selectors):
    group = False
    model = False
    for value in entity.values:
        if type(value) != list:
            if value.name == "editor" and selectors["groups"]:
                group = check_for_value(value, selectors)

        if type(value) == list:
            if value[0] == "model" and value[1] in selectors["models"]:
                model = True
    if (group or not selectors["groups"]) and (model or not selectors["models"]):
        return entity
    return None


def check_for_value(editor, selectors):
    for value in editor.values:
        if type(value) == list:
            if value[0] == "visgroupid" and value[1] in selectors["groups"].values():
                return True
    return False


def get_visgroups(node, visgroups=[]):
    for value in node.values:
        if type(value) != list:
            if value.name == "visgroups":
                visgroups = get_visgroups(value, visgroups)
            elif value.name == "visgroup":
                visgroups.append(value)
                visgroups = get_visgroups(value, visgroups)
    return visgroups


def get_selectors(groups, selectors):
    group_selectors = {}
    for group in groups:
        name = ""
        pid = ""
        for value in group.values:
            if type(value) == list:
                if value[0] == "name":
                    name = value[1]
                if value[0] == "visgroupid":
                    pid = value[1]
        if name and pid and name in selectors:
            group_selectors[name] = pid

    model_selectors = []
    for selector in selectors:
        if selector not in group_selectors.keys():
            model_selectors.append(selector)
    selectors = {"models": model_selectors, "groups": group_selectors}
    return selectors


def check_output(filename, overwrite):
    if filename.split('.')[-1] == "vmf":
        if os.path.isfile(filename) and not overwrite:
            print(filename + ' already exists. Never overwrite your maps without backing them up first!'
                             '\nUse --overwrite / -o if you want to overwrite the file.')
            exit()
        else:
            return
    else:
        print('Output file must be .vmf file!')
    exit()


def read_input(filename):
    if filename.split('.')[-1] == "vmf":
        try:
            with open(filename, 'r') as f:
                map_input = f.read().splitlines()
        except FileNotFoundError:
            print(filename + " not found.")
            exit()
        else:
            return map_input
    else:
        print('Input file must be .vmf file!')
    exit()


def write_output(output, filename):
    with open(filename, 'w') as f:
        for line in output:
            f.write(line + "\n")


def parse():
    parser = argparse.ArgumentParser(description='Randomize vmf entities.')
    parser.add_argument('input',
                        help='Path/name for the input file.')
    parser.add_argument('output',
                        help='Path/name for the output file.')
    parser.add_argument('selectors',
                        help='Way to select the entities. '
                             'Can be World Model or the VisGroup name or both. '
                             'Model names must include the path show in hammer. For example: '
                             'models/props/de_dust/hr_dust/foliage/palm_tree_small_02.mdl RandomGroup_1',
                        nargs='*')
    parser.add_argument("-r", "--rotate",
                        help="Randomize rotation over axis Y Z X (0-360). "
                             "By default rotates entity randomly around all axes. "
                             "Axes and rotations can be defined as arguments. Relative values can be used. "
                             "For example: "
                             "/ -r X 10 40 YZ ~20 / "
                             "Changes entity rotation over X axis to something random between 10 and 40 degrees "
                             "and add 0 to 20 degrees to the rotation of Z and Y."
                             "/ -r X / will rotate entity randomly around X axis.",
                        nargs="*")
    parser.add_argument("-c", "--colorize",
                        help="Randomize Hue (0-360) Saturation (0-100) and Brightness (0-100) "
                             "(HSB) values of the entity. "
                             "By default changes all HSB color values randomly. "
                             "Values can be defined with arguments. Relative values can be used. "
                             "For example:"
                             "/ -c H 20 30 SB ~30 / "
                             "or "
                             "/ -c hue 20 30 SaturationBrightness ~30 / "
                             "Changes the Hue value of the entity to something between 20 and 30"
                             "and adds 0 to 30 to the values of Saturation and Brightness."
                             "/ -c H / or / -c Hue / will give the entity random Hue value (0-360)",
                        nargs="*")
    parser.add_argument("-s", "--scale",
                        help="Randomize the scale of the entity. "
                             "Values can be defined with arguments. Relative values can be used. "
                             "For example:"
                             "/ -s 1.2 1.5 / "
                             "Changes the scale of the entity to something between 1.2 and 1.5"
                             "/ -s 0.8 / "
                             "Changes the scale of the entity to something between 0.8 and 1."
                             "/ -s ~0.1 / "
                             "Adds something between 0 and 0.1 to the scale of the entity",
                        nargs="*")
    parser.add_argument("-o", "--overwrite", action="store_true",
                        help="Overwrites existing output file. "
                             "Only use this if you are absolutely sure you know what you are doing!")

    return parser.parse_args()


def main():
    args = parse()
    print(args)
    if args.rotate is None and args.colorize is None and args.scale is None:
        print("No operation selected!")
        exit()
    file = read_input(args.input)
    check_output(args.output, args.overwrite)
    tree = create_tree(file)

    refile = print_leaf(tree).splitlines()
    testfile(refile, file)

    visgroups = get_visgroups(tree)
    selectors = get_selectors(visgroups, args.selectors)
    print(selectors)
    entities = get_entities(tree, selectors)
    print("Found " + str(len(entities)) + " matching entities")
    if args.rotate is not None:
        done = rotate(entities, args.rotate)
        print("Rotated " + str(done) + " entities.")
    if args.colorize is not None:
        done = colorize(entities, args.colorize)
        print("Colorized " + str(done) + " entities.")
    if args.scale is not None:
        done = scale(entities, args.scale)
        print("Scaled " + str(done) + " entities.")
    newfile = print_leaf(tree).splitlines()
    write_output(newfile, args.output)


if __name__ == '__main__':
    main()
