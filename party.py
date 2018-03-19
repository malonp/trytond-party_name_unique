#This file is part party_name_unique module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.


from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


__all__ = ['Party']


class Party:
    __metaclass__ = PoolMeta
    __name__ = 'party.party'

    @classmethod
    def copy(cls, parties, default=None):
        if default is None:
            default = {}
        default['name'] = None
        return super(Party, cls).copy(parties, default=default)

    @classmethod
    def validate(cls, parties):
        super(Party, cls).validate(parties)
        for party in parties:
            party.strip_name()
            party.unique_name()

    def strip_name(self):
        #Warn on existing name and constraint non stripped names
        if (self.id > 0):
            if not (self.name == self.name.strip()):
                self.raise_user_error(
                    "Party name should be stripped!")

    def unique_name(self):
        user = Transaction().user

        if (self.id > 0 and user > 1):
            parties = Pool().get('party.party')
            #Must explicitly search on records with active=False
            #otherwise only search on records with active=True
            parties_count = parties.search_count(
                [('name', '=', self.name), ('active', 'in', (True, False))])
            if (parties_count > 1):
                self.raise_user_warning('warn_party_with_same_name.%d' % self.id,
                    'Party name "%s" already exists!', self.rec_name)

