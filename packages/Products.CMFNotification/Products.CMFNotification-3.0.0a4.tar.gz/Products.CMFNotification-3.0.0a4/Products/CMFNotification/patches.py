"""Define CMFNotification patches for CMFCore to call appropriated
handlers when specific events occur.

$Id$
"""

from Products.CMFCore.utils import getToolByName
from NotificationTool import ID, LOG

## FIXME: PAS does fire events, we should use them to replace these
## monkey-patches: see "PluggableAuthService/interfaces/events.py".

######### CMFCore.RegistrationTool patch ########################
def afterAdd(self, member, id, password, properties):
    """Call the original method and also CMFNotification handler."""
    self._cmf_notification_orig_afterAdd(member, id, password, properties)
    ntool = getToolByName(self, ID, None)
    if ntool is not None:
        ntool.onMemberRegistration(member, properties)

from Products.CMFCore.RegistrationTool import RegistrationTool
RegistrationTool._cmf_notification_orig_afterAdd = RegistrationTool.afterAdd
RegistrationTool.afterAdd = afterAdd
LOG.info('Monkey-patched CMFCore.RegistrationTool')
######### End of CMFCore.RegistrationTool patch #################


######### CMFCore.MemberDataTool patch ##########################
def notifyMemberModified(self):
    """Call the original method and also CMFNotification handler."""
    self._cmf_notification_orig_notifyModified()
    ntool = getToolByName(self, ID, None)
    if ntool is not None:
        membership = getToolByName(self, 'portal_membership')
        member = membership.getMemberById(self.getId())
        ntool.onMemberModification(member)

# TODO: Instead of patching, better use a more specific adapter.
from pkg_resources import get_distribution
from pkg_resources import parse_version
plone_version = get_distribution('Products.CMFPlone').version
PLONE_52 = parse_version(plone_version) >= parse_version('5.2a1')
if PLONE_52:
    from Products.CMFCore.MemberDataTool import MemberAdapter
    MemberAdapter._cmf_notification_orig_notifyModified = MemberAdapter.notifyModified
    MemberAdapter.notifyModified = notifyMemberModified
else:
    from Products.CMFCore.MemberDataTool import MemberData
    MemberData._cmf_notification_orig_notifyModified = MemberData.notifyModified
    MemberData.notifyModified = notifyMemberModified


LOG.info('Monkey-patched CMFCore.MemberDataTool')
######### End of CMFCore.MemberDataTool patch ###################
