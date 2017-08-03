# Contact have severals methods to modify it because it's not an
# object as simple as account or domain

from zimsoap import zobjects


class MethodMixin:
    def create_contact(self, params):
        """Create a new contact
        example of params =
        {
            'cn': {
                'l': '13',
                'a': [
                    {
                        'n': 'bla',
                        '_content': 'mavaleur'
                    }
                ]
                'm': [
                    {
                        'op': '+',
                        'type': 'G',
                        'value': 'uid='
                    }
                ]
            }
        }

        :param contact: a zobject Contact
        :type contact: zobjects.mail.Contact

        :returns: the created zobjects.Contact
        :rtype: zobjects.mail.Contact
        """
        return self.request_single(
            'CreateContact', params, zobjects.mail.Contact)

    def get_contacts(self, f={}):
        """ Get all contacts for the current user or selected ones with
        contacts parameter

        :param f: a dict to filter contacts based on SOAP attributes
        :type f: dict

        :returns: a list of contact objects or None
        :rtype: [zobjects.mail.Contact]
        """

        return self.request_list(
            'GetContacts', f, zobjects.mail.Contact)

    def modify_contact(self, params):
        """
        Modify a contact. By default, it will merge. Set
        params={'replace': '1'} to replace attributes values.

        {
            'replace': True,
            'cn': {
                'id': 244,
                'a': [
                    {
                        'n': 'bla',
                        '_content': 'mavaleur'
                    }
                ]
                'm': [
                    {
                        'op': '+',
                        'type': 'G',
                        'value': 'uid='
                    }
                ]
            }
        }

        :param params: parameters of informations to modify
        :type params: dict

        :returns:       the modified zobject Contact
        :rtype: zobjects.mail.Contact
        """

        return self.request_single(
            'ModifyContact', params, zobjects.mail.Contact)

    def modify_contact_attributes(self, contact, attrs):
        """
        :param contact: a zobject contact to use as selector
        :type contact: zobjects.mail.Contact

        :param attrs: a dict of attributes
        :type attrs: dict

        :returns: the modified zobject
        :rtype: zobjects.mail.Contact
        """

        a = [{'n': k, '_content': v} for k, v in attrs.items()]
        params = {
            'cn': {
                'id': contact.id,
                'a': a
            }
        }

        return self.request_single(
            'ModifyContact', params, zobjects.mail.Contact)

    def create_group(self, name, members, attrs={}, **kwargs):
        """
        :param name: the group nickname
        :type attrs: string

        :param members: a list of zobject ContactGroupMember
        :type members: [zobjects.mail.ContactGroupMember]

        :param attrs: a dict of attributes
        :type attrs: dict

        :param kwargs: infos like l for folder_id or t for tags. cf SOAP doc
        :type kwargs: kwargs

        :returns: the modified zobject
        :rtype: zobjects.mail.Contact
        """
        attrs['type'] = 'group'
        attrs['nickname'] = name
        attrs = [{'n': k, '_content': v} for k, v in attrs.items()]

        kwargs['a'] = attrs
        kwargs['m'] = []

        for member in members:
            kwargs['m'].append({'type': member.type, 'value': member.value})

        params = {'cn': kwargs}

        return self.request_single(
            'CreateContact', params, zobjects.mail.Contact)

    def delete_contacts(self, contacts):
        """ Delete selected contacts for the current user

        :param contacts: a list of Contacts object to use as filter
        :type contacts: [zobjects.mail.Contact]

        :returns: None (the API returns nothing)
        """

        str_ids = self._return_comma_list(contacts)
        self.request('ContactAction', {'action': {'op': 'delete',
                                                  'id': str_ids}})

    def add_group_members(self, group, members):
        """

        :param group: a zobject contact to use as selector
        :type group: zobjects.mail.Contact

        :param members: a list of zobject ContactGroupMember
        :type members: [zobjects.mail.ContactGroupMember]

        :returns: the modified zobject
        :rtype: zobjects.mail.Contact
        """
        params = {'cn': {'id': group.id, 'm': []}}

        for member in members:
            m = {
                'op': '+',
                'type': member.type,
                'value': member.value
            }
            params['cn']['m'].append(m)

        return self.request_single(
            'ModifyContact', params, zobjects.mail.Contact)

    def remove_group_members(self, group, members):
        """

        :param group: a zobject contact to use as selector
        :type group: zobjects.mail.Contact

        :param members: a list of zobject ContactGroupMember
        :type members: [zobjects.mail.ContactGroupMember]

        :returns: the modified zobject
        :rtype: zobjects.mail.Contact
        """
        params = {'cn': {'id': group.id, 'm': []}}

        for member in members:
            m = {
                'op': '-',
                'type': member.type,
                'value': member.value
            }
            params['cn']['m'].append(m)

        return self.request_single(
            'ModifyContact', params, zobjects.mail.Contact)

    def delete_groups(self, groups):
        """ Delete selected contacts for the current user

        :param groups: a list of Contacts object to use as filter
        :type groups: [zobjects.mail.Contact]

        :returns: None (the API returns nothing)
        """

        str_ids = self._return_comma_list(groups)
        self.request('ContactAction', {'action': {'op': 'delete',
                                                  'id': str_ids}})
