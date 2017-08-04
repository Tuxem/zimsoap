from zimsoap import utils
from . import ZObject


class ContactGroupMember(ZObject):
    """ Contact group member information

    .. code:: xml
        <m type="{member-type}" value="{member-value}">
    """
    TAG_NAME = 'm'


class Contact(ZObject):
    """A contact object

    .. code:: xml
        (<cn [sf="{contact-sort-field}"] [exp="{can-expand} (0|1)"]
                 id="{contact-id}" [l="{contact-folder-id}"]
                 [f="{contact-flags}"] [t="{contact-tags}"]
                 [tn="{contact-tag-names}"]
                 [md="{contact-modified-date-secs} (Long)"]
                 [ms="{contact-modified-seq} (Integer)"]
                 [d="{contact-date-millis} (Long)"]
                 [rev="{saved-sequence-number} (Integer)"]
                 [fileAsStr="{contact-file-as}"]
                 [email="{contact-email}"] [email2="{contact-email2}"]
                 [email3="{contact-email3}"] [type="{contact-type}"]
                 [dlist="{contact-dlist}"]
                 [ref="{contact-gal-entry-ref}"]
                 [tooManyMembers="{contact-too-many-members} (0|1)"]
          > ## ContactInfo
            (<meta [section="{section}"]> ## MailCustomMetadata
                (<a n="{key}">{value}</a> ## KeyValuePair)*
              </meta>)*
            (<a [part="{contact-part-id}"] [ct="{contact-content-type}"]
                    [s="{contact-size} (Integer)"]
                    [filename="{contact-content-filename}"]
                    n="{key}" /> ## ContactAttr)*
            (ContactGroupMember)*
          </cn>)*
    """
    TAG_NAME = 'cn'

    @classmethod
    def from_dict(cls, d):
        """ Override default, adding the capture of members.
        """

        members = []
        if 'm' in d.keys():
            members = [ContactGroupMember.from_dict(w)
                       for w in utils.as_list(d['m'])]
            del d['m']

        m = super(Contact, cls).from_dict(d)

        m.members = members

        return m


class Conversation(ZObject):
    """ A conversation object


    """
    TAG_NAME = 'c'


class FilterRule(ZObject):
    """A filter rule object

    """
    TAG_NAME = 'filterRule'

    ALLOWED_TESTS = [
        "addressBookTest", "addressTest", "attachmentTest", "bodyTest",
        "bulkTest", "contactRankingTest", "conversationTest",
        "currentDayOfWeekTest", "currentTimeTest", "dateTest",
        "facebookTest", "flaggedTest", "headerExistsTest", "headerTest",
        "importanceTest", "inviteTest", "linkedinTest", "listTest",
        "meTest", "mimeHeaderTest", "sizeTest", "socialcastTest",
        "trueTest", "twitterTest", "communityRequestsTest",
        "communityContentTest", "communityConnectionsTest"
    ]
    ALLOWED_ACTIONS = [
        "actionKeep", "actionDiscard", "actionFileInto", "actionFlag",
        "actionTag", "actionRedirect", "actionReply", "actionNotify",
        "actionStop"
        ]

    @classmethod
    def from_dict(cls, d):
        tests = []
        if 'filterTests' in d:
            tests = [FilterRuleTests.from_dict(w)
                     for w in utils.as_list(d['filterTests'])]
        if 'filterActions' in d:
            actions = [FilterRuleActions.from_dict(w)
                       for w in utils.as_list(d['filterActions'])]

        o = super(FilterRule, cls).from_dict(d)
        o.tests = tests
        o.actions = actions

        return o

    def to_creator(self):
        """ Returns a dict suitable for Create or Modify requests

        :returns: the creator dictionary
        :rtype:   dict
        """
        c = {
            'name': self.name,
            'active': self.active,
            'filterActions': {},
            'filterTests': {}
        }
        for action in self.actions:
            c['filterActions'] = dict(
                list(c['filterActions'].items()) +
                list(action._full_data.items())
            )
        for test in self.tests:
            c['filterTests'] = dict(
                list(c['filterTests'].items()) +
                list(test._full_data.items())
            )

        return c


class FilterRuleTests(ZObject):

    @classmethod
    def from_dict(cls, d):
        tests = {}

        for attr in FilterRule.ALLOWED_TESTS:
            if attr in d.keys():
                cl_name = 'Filter' + attr[0].upper() + attr[1::]
                tests[attr] = globals()[cl_name].from_dict(d[attr])

        o = super(FilterRuleTests, cls).from_dict(d)
        for k, v in tests.items():
            setattr(o, k, v)

        return o


class FilterAddressBookTest(ZObject):
    pass


class FilterAddressTest(ZObject):
    pass


class FilterAttachmentTest(ZObject):
    pass


class FilterBodyTest(ZObject):
    pass


class FilterBulkTest(ZObject):
    pass


class FilterContactRankingTest(ZObject):
    pass


class FilterConversationTest(ZObject):
    pass


class FilterCurrentDayOfWeekTest(ZObject):
    pass


class FilterCurrentTimeTest(ZObject):
    pass


class FilterDateTest(ZObject):
    pass


class FilterFacebookTest(ZObject):
    pass


class FilterFlaggedTest(ZObject):
    pass


class FilterHeaderExistsTest(ZObject):
    pass


class FilterHeaderTest(ZObject):
    pass


class FilterImportanceTest(ZObject):
    pass


class FilterInviteTest(ZObject):
    pass


class FilterLinkedinTest(ZObject):
    pass


class FilterListTest(ZObject):
    pass


class FilterMeTest(ZObject):
    pass


class FilterMimeHeaderTest(ZObject):
    pass


class FilterSizeTest(ZObject):
    pass


class FilterSocialcastTest(ZObject):
    pass


class FilterTrueTest(ZObject):
    pass


class FilterTwitterTest(ZObject):
    pass


class FilterCommunityRequestsTest(ZObject):
    pass


class FilterCommunityContentTest(ZObject):
    pass


class FilterCommunityConnectionsTest(ZObject):
    pass


class FilterRuleActions(ZObject):
    @classmethod
    def from_dict(cls, d):
        actions = {}

        for attr in FilterRule.ALLOWED_ACTIONS:
            if attr in d.keys():
                cl_name = 'Filter' + attr[0].upper() + attr[1::]
                actions[attr] = globals()[cl_name].from_dict(d[attr])

        o = super(FilterRuleActions, cls).from_dict(d)
        for k, v in actions.items():
            setattr(o, k, v)

        return o


class FilterActionKeep(ZObject):
    pass


class FilterActionDiscard(ZObject):
    pass


class FilterActionFileInto(ZObject):
    pass


class FilterActionFlag(ZObject):
    pass


class FilterActionTag(ZObject):
    pass


class FilterActionRedirect(ZObject):
    pass


class FilterActionReply(ZObject):
    pass


class FilterActionNotify(ZObject):
    pass


class FilterActionStop(ZObject):
    pass


class Task(ZObject):
    TAG_NAME = 'task'
    ATTRNAME_PROPERTY = 'id'

    def to_creator(self, subject, desc):
        """ Return a python-zimbra dict for CreateTaskRequest

        Example :
        <CreateTaskRequest>
            <m su="Task subject">
                <inv>
                    <comp name="Task subject">
                        <fr>Task comment</fr>
                        <desc>Task comment</desc>
                    </comp>
                </inv>
                <mp>
                    <content/>
                </mp>
            </m>
        </CreateTaskRequest>
        """

        task = {
            'm': {
                'su': subject,
                'inv': {
                    'comp': {
                        'name': subject,
                        'fr': {'_content': desc},
                        'desc': {'_content': desc},
                        'percentComplete': '0'
                    }
                },
                'mp': {
                    'content': {}
                }
            }
        }

        return task
