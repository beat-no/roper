def get_line_start(code, offset):
    """
    NOTE: Slight rework of method in rope. Maybe change it upstream so it can be used here?
    """
    try:
        return code.rindex('\n', 0, offset + 1)
    except ValueError:
        return 0


def get_line_end(code, offset):
    """
    NOTE: Slight rework of method in rope. Maybe change it upstream so it can be used here?
    """
    try:
        return code.index('\n', offset)
    except ValueError:
        return len(code)


def get_line(code, offset):
    line_start = get_line_start(code, offset)
    line_end = get_line_end(code, offset)
    return code[line_start:line_end]


def find_module_resources(resource):
    for child in resource.get_children():
        if not child.is_folder() and child.name.endswith(".py"):
            yield child
        elif child.is_folder():
            yield from find_module_resources(child)
        #else:
            #print("WARNING: unexpected!", child.name)


def occ_info(occ):
    checks = {
        #"is_defined": occ.is_defined(),
        "DEFINITION": occ.is_defined(),
        
        #"is_in_import_statement": occ.is_in_import_statement(),
        "IMPORT": occ.is_in_import_statement(),
        
        "is_a_fixed_primary": occ.is_a_fixed_primary(),
        "is_called": occ.is_called(),
        "is_function_keyword_parameter": occ.is_function_keyword_parameter(),
        "is_unsure": occ.is_unsure(),
        "is_written": occ.is_written()
    }
    return [key for key, val in checks.items() if val]


def print_occurences(occurrences):
    for occ in occurrences:
        print("{filename}:{offset} {occurrence_types}: {code_line}".format(
            filename=occ.resource.path,
            offset=occ.offset,
            code_line=get_line(occ.resource.read(), occ.offset).strip(),
            occurrence_types=occ_info(occ)))
