from zimsoap import zobjects
from zimsoap.exceptions import ZimSOAPException


class MethodMixin:
    def add_filter_rule(
            self, name, condition, filters, actions, active=1, way='in'):
        """
        :param: name filter name
        :param: condition allof or anyof
        :param: filters dict of filters
        :param: actions dict of actions
        :param: way string discribing if filter is for 'in' or 'out' messages
        :returns: list of user's zobjects.FilterRule
        """

        filters['condition'] = condition

        new_rule = {
            'name': name,
            'active': active,
            'filterTests': filters,
            'filterActions': actions
        }

        new_rules = [zobjects.mail.FilterRule.from_dict(new_rule)]
        prev_rules = self.get_filter_rules(way=way)

        # if there is already some rules
        if prev_rules:
            for rule in prev_rules:
                # don't add rule if it already exist
                if rule.name == new_rules[0].name:
                    raise ZimSOAPException(
                        'filter %s already exists' % rule.name)
            new_rules = new_rules + prev_rules

        content = {
            'filterRules': {
                'filterRule': [r._full_data for r in new_rules]
            }
        }

        if way == 'in':
            self.request('ModifyFilterRules', content)
        elif way == 'out':
            self.request('ModifyOutgoingFilterRules', content)
        return new_rules

    def get_filter_rule(self, zfilter, way='in'):
        """ Return the filter rule

        :param: zfilter a zobjects.FilterRule
        :param: way string discribing if filter is for 'in' or 'out' messages
        :returns: a zobjects.FilterRule"""
        for f in self.get_filter_rules(way=way):
            if f.name == zfilter.name:
                return f
        return None

    def get_filter_rules(self, way='in'):
        """
        :param: way string discribing if filter is for 'in' or 'out' messages
        :returns: list of zobjects.FilterRule
        """

        if way == 'in':
            resp = self.request('GetFilterRules')
        elif way == 'out':
            resp = self.request('GetOutgoingFilterRules')
        return [zobjects.mail.FilterRule.from_dict(i)
                for i in resp['filterRules']['filterRule']]

    def apply_filter_rule(self, zfilter, query='in:inbox', way='in'):
        """
        :param: zfilter a zobjects.FilterRule
        :param: query on what will the filter be applied
        :param: way string discribing if filter is for 'in' or 'out' messages
        :returns: list of impacted message's ids
        """

        content = {
            'filterRules': {
                'filterRule': {'name': zfilter.name}
                },
            'query': {'_content': query}
        }
        if way == 'in':
            ids = self.request('ApplyFilterRules', content)
        elif way == 'out':
            ids = self.request('ApplyOutgoingFilterRules', content)

        if ids:
            return [int(m) for m in ids['m']['ids'].split(',')]
        else:
            return []

    def delete_filter_rule(self, zfilter, way='in'):
        """ delete a filter rule

        :param: _filter a zobjects.FilterRule or the filter name
        :param: way string discribing if filter is for 'in' or 'out' messages
        :returns: a list of zobjects.FilterRule
        """
        updated_rules = []
        rules = self.get_filter_rules(way=way)

        if rules:
            for rule in rules:
                if not rule.name == zfilter.name:
                    updated_rules.append(rule)

        if rules != updated_rules:
            content = {
                'filterRules': {
                    'filterRule': [f._full_data for f in updated_rules]
                }
            }
            if way == 'in':
                self.request('ModifyFilterRules', content)
            elif way == 'out':
                self.request('ModifyOutgoingFilterRules', content)

        return updated_rules
