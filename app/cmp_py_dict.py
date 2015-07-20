"""
Compare two python dictionaries (hash tables) and return another
dictionary with the following keys

return_dict = {
                'new' : set(),
                'modified' : set(),
                'deleted' : set()
              }
"""
from string import Template

g_new_template = Template('${dict_name}.${key_name}')
g_mod_template = Template('${dict_name}.${key_name} - [${old_val} -> ${new_val}]')
g_del_template = Template('${dict_name}.${key_name}')
g_name_template = Template('${old_name}.${new_name}')

def get_diffs(old_dict, new_dict):

    #initialize the return dictionary
    return_dict = {
            'new' : set(),
            'modified' : set(),
            'deleted' : set()
            }

    #call the cmp_py_dict function
    for key, val in cmp_py_dict(old_dict, new_dict):
        return_dict[key].add(val)

    return return_dict

def cmp_py_dict(old_dict, new_dict, name='', level=-1):
    """
    this is a recursive generator which yeilds the following tuple
    (observed_change, key)
    """

    #input validation
    if not isinstance(old_dict, dict)\
       or not isinstance(new_dict, dict):
           raise TypeError('Function works with only dictionaries')

    #increment the level
    level += 1

    #iterate over old_dict keys
    for key in old_dict:

        #find modified keys
        if key in new_dict:
            #recursively call if values are dictionaries
            if isinstance(old_dict[key], dict)\
                and isinstance(new_dict[key], dict):
                    for op in cmp_py_dict(old_dict[key],
                                          new_dict[key],
                                          name=g_name_template.substitute(old_name=name, new_name=key)):
                        yield op
            else:
                if new_dict[key] != old_dict[key]:
                    yield 'modified', g_mod_template.substitute(dict_name=name,
                                                                 key_name=key,
                                                                 old_val=old_dict[key],
                                                                 new_val=new_dict[key])
        #if key is not there then its deleted
        else:
            yield 'deleted', g_del_template.substitute(dict_name=name,
                                                        key_name=key)

    #iterate over new_dict keys
    for key in new_dict:
        if key not in old_dict:
            yield 'new', g_new_template.substitute(dict_name=name,
                                                    key_name=key)






