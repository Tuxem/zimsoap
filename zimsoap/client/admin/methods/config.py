from zimsoap import zobjects


class MethodMixin:
    def get_all_config(self):
        """ Fetches the values of all global config attributes

        :returns: a dict-like Config object
        :rtype:   zobjects.admin.Config or None
        """
        return self.request_single('GetAllConfig', {}, zobjects.admin.Config)

    def get_config(self, attr):
        """ Fetches global config
        :param attr:  the name of the config attribute to fetch
        :type attr:   str

        :returns: value of global config for the specified attribute
        :rtype:   str
        """

        gacf = self.get_all_config()
        try:
            return gacf.property(attr)
        except KeyError:
            raise Exception('no attribute "{}" in global config'.format(attr))

    def modify_config(self, config):
        """ Sets the value a global config attribute

        :param value: a zobjects.config with values to modify
        :type value:  zobjects.config

        :returns: all configuration
        :rtype:   zobjects.config
        """

        immuables_attr = [
            'zimbraProduct',
            'zimbraAuthTokenKey',
            'zimbraExternalAccountProvisioningKey',
            'zimbraCsrfTokenKey',
            'zimbraMtaSmtpSaslSecurityOptions'
        ]
        for attr in immuables_attr:
            config.remove_property(attr)

        self.request('ModifyConfig', config.to_creator())
        return self.get_all_config()
