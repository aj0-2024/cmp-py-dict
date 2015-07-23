"""
Compare two python dictionaries (hash tables) and return another
dictionary with the following keys

return_dict = {
                'new' : set(),
                'modified' : set(),
                'deleted' : set()
              }
"""
class CmpDict(object):
    """
    Compare two dictionaries and find out new, deleted and modified registers
    """

    def __init__(self, old_dict, new_dict):
        """
        Initialize with old and new dictionaries
        """

        #input validation
        if not isinstance(old_dict, dict) or not isinstance(new_dict, dict):
            raise TypeError('Function works with only dictionaries')

        self._old_dict = old_dict
        self._new_dict = new_dict
        self._new_tmp = self._del_tmp = self._name_tmp = '{tmp.dict_name}.{tmp.key_name}'
        self._mod_tmp = '{tmp.dict_name}.{tmp.key_name} - [{tmp.old_val} -> {tmp.new_val}]'
        self._return_dict = {'new' : set(), 'modified' : set(), 'deleted' : set()}

        #parse
        self._get_diffs(self._old_dict, self._new_dict)

    def _cmp_py_dict(self, old_dict, new_dict, name='', level=-1):
        """
        this is a recursive generator which yeilds the following tuple
        (observed_change, key)
        """

        #increment the level
        level += 1

        #inst the template variable
        class Env(object):
            pass
        tmp = Env()

        #iterate over old_dict keys
        for key in old_dict:

            tmp.dict_name = name
            tmp.key_name = key

            #find modified keys
            if key in new_dict:
                #recursively call if values are dictionaries
                if isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                    name = self._name_tmp.format(tmp=tmp)

                    #yield from recursive generator
                    for key, val in self._cmp_py_dict(old_dict[key],
                                                      new_dict[key],
                                                      name=name,
                                                      level=level):
                        yield key, val
                else:
                    if new_dict[key] != old_dict[key]:
                        tmp.old_val = old_dict[key]
                        tmp.new_val = new_dict[key]
                        yield 'modified', self._mod_tmp.format(tmp=tmp)
            #if key is not there then its deleted
            else:
                yield 'deleted', self._del_tmp.format(tmp=tmp)

        #iterate over new_dict keys
        for key in new_dict:
            if key not in old_dict:
                tmp.dict_name = name
                tmp.key_name = key
                yield 'new', self._new_tmp.format(tmp=tmp)

    def _get_diffs(self, old_dict, new_dict):
        """
        Call the generator and store the diffs
        """
        #call the cmp_py_dict function
        for key, val in self._cmp_py_dict(old_dict, new_dict):
            self._return_dict[key].add(val)

    @property
    def new(self):
        """Return the new keys"""
        return self._return_dict['new']

    @property
    def modified(self):
        """Return old keys"""
        return self._return_dict['modified']

    @property
    def deleted(self):
        """Return deleted keys"""
        return self._return_dict['deleted']






