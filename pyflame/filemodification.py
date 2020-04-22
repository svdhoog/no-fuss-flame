import re
import sys

def modifyXMLdotC(path, variables):
    # open xml.c
    with open(path + "/xml.c", 'r') as file:
        xml_c = file.read()

    # remove writing of unwanted agents
    p = re.compile('void write_.*agent')
    agents_in_model = []
    for s in re.findall(p,xml_c):
        agents_in_model.append(s[11:-6])

    for a in agents_in_model:
        if a not in variables.keys():
            xml_c = xml_c.replace('write_' + a + '_agent(file', '//write_' + a + '_agent(file', 1)

    # modify write functions
    for a in variables.keys():
        current_pos = xml_c.find("<name>" + a + "</name>")
        current_pos = xml_c.find("</name>", current_pos)+19

        while True:
            end_pos = xml_c.find("</xagent>", current_pos) - 8

            z1 = xml_c.find("<", current_pos)+1
            if z1 > end_pos:
                break

            z2 = xml_c.find(">", z1)

            var_name = xml_c[z1:z2]

            start_block = z1 - 10
            end_block = xml_c.find(">\\n", start_block)+13

            if var_name not in variables[a]:
                xml_c = xml_c[:start_block] + xml_c[end_block:]
            else:
                current_pos = end_block

    # remove writing environment
    start_env = xml_c.find("<environment>") - 7
    end_env = xml_c.find("</environment>") + 26
    xml_c = xml_c[:start_env] + xml_c[end_env:]

    # write new xml.c
    with open(path + "/xml.c", 'w') as file:
        file.write(xml_c)


def modify0xml(zero_xml_file, params):
    if params is not None:
        with open(zero_xml_file, 'r') as file:
            zero_xml = file.read()

        for p in params.keys():
            v = params[p]

            x1 = zero_xml.find("<" + p)
            if x1 > 0:
                x1 = zero_xml.find(">", x1) + 1
                x2 = zero_xml.find("</" + p + ">")

                zero_xml = zero_xml[:x1] + str(v) + zero_xml[x2:]
            else:
                sys.stderr.write("Parameter " + p + " not found!\n")
                exit(0)

        with open(zero_xml_file, 'w') as file:
            file.write(zero_xml)





