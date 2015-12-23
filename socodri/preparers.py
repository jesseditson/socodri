'''Defines Custom restless preparer classes'''
from restless.preparers import FieldsPreparer


class LaxFieldsPreparer(FieldsPreparer):
    '''
    Restless preparer that gracefully handles fields not provided in the
    returned dict/class
    '''
    def prepare(self, data):
        '''
        Overrides the prepare method defined in the FieldsPreparer
        '''
        result = {}

        if not self.fields:
            return data

        for fieldname, lookup in self.fields.items():
            try:
                result[fieldname] = self.lookup_data(lookup, data)
            except Exception, e:
                continue

        return result
