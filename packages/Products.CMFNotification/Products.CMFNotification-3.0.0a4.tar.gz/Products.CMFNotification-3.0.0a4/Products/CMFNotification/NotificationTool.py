# This file is part of CMFNotification
#
# Copyright (c) 2005-2008 by Pilot Systems (http://www.pilotsystems.net)
#
# CMFNotification is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#
"""Define notification tool.

$Id$
"""

import re
import inspect
import logging
from types import StringType

from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from ZODB.POSException import ConflictError
from OFS.PropertyManager import PropertyManager
from BTrees.IOBTree import IOBTree
from BTrees.OOBTree import OOBTree
from zope.component import getUtility

from AccessControl import Unauthorized
from AccessControl import ClassSecurityInfo
from AccessControl import getSecurityManager
from AccessControl.PermissionRole import rolesForPermissionOn

from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFEditions.interfaces.IArchivist import ArchivistUnregisteredError

from Products.CMFNotification.utils import getBasicBindings
from Products.CMFNotification.utils import getPreviousVersion
from Products.CMFNotification.utils import getExpressionContext
from Products.CMFNotification.utils import getPreviousWorkflowState
from Products.CMFNotification.exceptions import DisabledFeature
from Products.CMFNotification.exceptions import InvalidEmailAddress
from Products.CMFNotification.permissions import SUBSCRIBE_PERMISSION
from Products.CMFNotification.interfaces import INotificationDelivery

from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.interface import implementer
from zope.interface import Interface
from Products.CMFPlone.interfaces import ISimpleItemWithProperties


class FakeInterface(Interface): pass


try:
    from plone.dexterity.interfaces import IDexterityContent
except ImportError:
    IDexterityContent = FakeInterface

try:
    from Products.ATContentTypes.interface.interfaces import IATContentType
except ImportError:
    IATContentType = FakeInterface


ID = 'portal_notification'
TITLE = 'CMF Notification tool'
META_TYPE = 'CMFNotificationTool'

## This regexp was taken from Silva ('Silva/subscriptionservice.py').
EMAIL_REGEXP = re.compile('^[0-9a-zA-Z_&.%+-]+@([0-9a-zA-Z]([0-9a-zA-Z-]*[0-9a-zA-Z])?\.)+[a-zA-Z]{2,6}$')
RULE_DELIMITER = '::'
LOG = logging.getLogger('CMFNotification')
## Ignore objects temporarily created by the Plone Factory Tool
DEFAULT_IGNORE_RULES = ["python: getattr(context, 'isTemporary', lambda: False)()"]

MAIL_HOST_META_TYPES = ('Mail Host', 'Secure Mail Host', 'Maildrop Host',
    'Secure Maildrop Host')


@implementer(ISimpleItemWithProperties)
class NotificationTool(UniqueObject, SimpleItem, PropertyManager):
    """Main notification tool."""
    id = ID
    title = TITLE
    meta_type = META_TYPE

    manage_options = (PropertyManager.manage_options
                      + SimpleItem.manage_options)

    ## Extra subscriptions
    extra_subscriptions_enabled = False
    extra_subscriptions_recursive = True

    ## Debug mode
    debug_mode = False

    ## Ignore rules
    ignore_rules = DEFAULT_IGNORE_RULES

    ## Item creation
    item_creation_notification_enabled = False
    on_item_creation_users = []
    on_item_creation_mail_template = []
    ## Item modification
    item_modification_notification_enabled = False
    on_item_modification_users = []
    on_item_modification_mail_template = []
    ## Item removal
    item_removal_notification_enabled = False
    on_item_removal_users = []
    on_item_removal_mail_template = []
    ## Workflow transition
    wf_transition_notification_enabled = False
    on_wf_transition_users = []
    on_wf_transition_mail_template = []
    ## Member registration
    member_registration_notification_enabled = False
    on_member_registration_users = []
    on_member_registration_mail_template = []
    ## Member modification
    member_modification_notification_enabled = False
    on_member_modification_users = []
    on_member_modification_mail_template = []
    ## Discussion item creation
    discussion_item_creation_notification_enabled = False
    on_discussion_item_creation_users = []
    on_discussion_item_creation_mail_template = []

    _properties = ({'id': 'extra_subscriptions_enabled',
                    'label': 'Enable extra subscriptions',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'extra_subscriptions_recursive',
                    'label': 'Toggle recursive mode for extra subscriptions',
                    'mode': 'w',
                    'type': 'boolean'},

                   {'id': 'debug_mode',
                    'label': 'Toggle debug mode',
                    'mode': 'w',
                    'type': 'boolean'},

                   {'id': 'ignore_rules',
                    'label': 'Rules (ignore)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'item_creation_notification_enabled',
                    'label': 'Enable item creation notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_item_creation_users',
                    'label': 'Rules on item creation (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_item_creation_mail_template',
                    'label': 'Rules on item creation (mail template)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'item_modification_notification_enabled',
                    'label': 'Enable item modification notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_item_modification_users',
                    'label': 'Rules on item modification (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_item_modification_mail_template',
                    'label': 'Rules on item modification (mail template)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'item_removal_notification_enabled',
                    'label': 'Enable item removal notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_item_removal_users',
                    'label': 'Rules on item removal (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_item_removal_mail_template',
                    'label': 'Rules on item removal (mail template)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'wf_transition_notification_enabled',
                    'label': 'Enable workflow transition notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_wf_transition_users',
                    'label': 'Rules on workflow transition (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_wf_transition_mail_template',
                    'label': 'Rules on workflow transition (mail template)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'member_registration_notification_enabled',
                    'label': 'Enable member registration notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_member_registration_users',
                    'label': 'Rules on member registration (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_member_registration_mail_template',
                    'label': 'Rules on member registration (mail template)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'member_modification_notification_enabled',
                    'label': 'Enable member modification notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_member_modification_users',
                    'label': 'Rules on member modification (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_member_modification_mail_template',
                    'label': 'Rules on member modification (mail template)',
                    'mode': 'w',
                    'type': 'lines'},

                   {'id': 'discussion_item_creation_notification_enabled',
                    'label': 'Enable discussion item creation notification',
                    'mode': 'w',
                    'type': 'boolean'},
                   {'id': 'on_discussion_item_creation_users',
                    'label': 'Rules on discussion item creation (users)',
                    'mode': 'w',
                    'type': 'lines'},
                   {'id': 'on_discussion_item_creation_mail_template',
                    'label': 'Rules on discussion item creation (mail template)',
                    'mode': 'w',
                    'type': 'lines'},
                   )

    security = ClassSecurityInfo()
    decPrivate = security.declarePrivate
    decProtected = security.declareProtected
    decPublic = security.declarePublic


    def __init__(self, *args, **kwargs):
        self._uid_to_path = IOBTree()
        self._subscriptions = OOBTree()


    #################################################################
    ## Notification handlers
    ########################
    decPrivate('onItemCreation')
    def onItemCreation(self, obj):
        """Handler called when an item is created.

        It returns the number of mails which have been sent.

        **Warning:** this handler is not called when a discussion item
        is added. In this case, ``onDiscussionItemCreation()`` is
        called instead.
        """
        if not self.getProperty('item_creation_notification_enabled'):
            return 0
        if self.ignoreNotification(obj):
            return 0

        extra_bindings = getBasicBindings(obj)
        changenote = self._getChangeNote(obj)
        extra_bindings.update({'changenote': changenote })
        return self._handlerHelper(obj, 'item_creation', extra_bindings)


    decPrivate('onItemModification')
    def onItemModification(self, obj):
        """Handler called when an item is modified.

        It returns the number of mails which have been sent.
        """
        if not self.getProperty('item_modification_notification_enabled'):
            return 0
        if self.ignoreNotification(obj):
            return 0

        extra_bindings = getBasicBindings(obj)
        changenote = self._getChangeNote(obj)
        extra_bindings.update({'current': obj,
                               'previous': getPreviousVersion(obj),
                               'changenote': changenote })
        return self._handlerHelper(obj, 'item_modification', extra_bindings)

    decPrivate('onItemRemoval')
    def onItemRemoval(self, obj):
        """Handler called when an item is removed.

        It returns the number of mails which have been sent.
        """
        if not self.getProperty('item_removal_notification_enabled'):
            return 0
        if self.ignoreNotification(obj):
            return 0

        extra_bindings = getBasicBindings(obj)
        return self._handlerHelper(obj, 'item_removal', extra_bindings)


    decPrivate('onWorkflowTransition')
    def onWorkflowTransition(self, obj, action):
        """Handler called when a workflow transition is triggered.

        It returns the number of mails which have been sent.
        """
        if not self.getProperty('wf_transition_notification_enabled'):
            return 0
        if self.ignoreNotification(obj):
            return 0

        wtool = getToolByName(self, 'portal_workflow')
        comments = wtool.getInfoFor(obj, 'comments')
        extra_bindings = getBasicBindings(obj)
        extra_bindings.update({'transition': action,
                               'comments': comments,
                               'previous_state': getPreviousWorkflowState(obj)})
        return self._handlerHelper(obj, 'wf_transition', extra_bindings)


    decPrivate('onMemberRegistration')
    def onMemberRegistration(self, member, properties):
        """Handler called when a new portal member has been
        registered.

        It returns the number of mails which have been sent.
        """
        if not self.getProperty('member_registration_notification_enabled'):
            return 0
        if self.ignoreNotification(member):
            return 0

        if properties is None:
            properties = {} ## FIXME: How could it be? (Damien)

        current_user = getSecurityManager().getUser()
        extra_bindings = getBasicBindings(member)
        extra_bindings.update({'current_user': current_user,
                               'member': member,
                               'properties': properties,
                               'event': 'registration'})
        return self._handlerHelper(member, 'member_registration',
                                   extra_bindings)


    decPrivate('onMemberModification')
    def onMemberModification(self, member):
        """Handler called when a member changes his/her properties.

        It returns the number of mails which have been sent.
        """
        ## FIXME: this should go away when we rely on the appropriate
        ## event.
        ## This method can also be called when the member is
        ## registered. We have to check that.
        stack = inspect.stack()
        ## 1st item is ourself
        ## 2nd item is 'CMFCore.MemberDataTool.notifyMemberModified()'
        ## 3rd item is 'CMFCore.MemberDataTool.setMemberProperties()'
        ## 4th item is what we want to check: it is either 'addMember'
        ## or 'setProperties()'
        caller = stack[3][3]
        if caller != 'setProperties':
            return 0

        if not self.getProperty('member_modification_notification_enabled'):
            return 0
        if self.ignoreNotification(member):
            return 0

        ## FIXME: what is the purpose of the following lines? (Damien)
        memberdata = getToolByName(self, 'portal_memberdata')
        properties = {}
        for key, value in memberdata.propertyItems():
            properties[key] = value

        current_user = getSecurityManager().getUser()
        extra_bindings = getBasicBindings(None)
        extra_bindings.update({'current_user': current_user,
                               'member': member,
                               'properties': properties,
                               'event': 'modification'})
        return self._handlerHelper(member, 'member_modification',
                                   extra_bindings)


    decPrivate('onDiscussionItemCreation')
    def onDiscussionItemCreation(self, discussion_item):
        """Handler called when a discussion item is created.

        It returns the number of mails which have been sent.
        """
        if not self.getProperty('discussion_item_creation_notification_enabled'):
            return 0
        if self.ignoreNotification(discussion_item):
            return 0

        ## We add two bindings to disambiguate the meaning of 'here'
        ## in the mail template and the rules: 'discussion_item' and
        ## 'discussed_item'.
        discussed_item = discussion_item
        while discussed_item.meta_type == discussion_item.meta_type:
            discussed_item = discussed_item.aq_inner.aq_parent.aq_parent
        extra_bindings = getBasicBindings(discussed_item)
        extra_bindings.update({'discussion_item': discussion_item,
                               'discussed_item': discussed_item})
        return self._handlerHelper(discussion_item, 'discussion_item_creation',
                                   extra_bindings)


    def _handlerHelper(self, obj, what, extra_bindings):
        """An helper method for ``on*()`` handlers.

        It returns the number of mails which have been sent.
        """
        self._updateSubscriptionMapping(obj)
        users_by_label = self.getUsersToNotify(obj, what, extra_bindings)
        if self.isExtraSubscriptionsEnabled():
            users = users_by_label.get('', [])
            users.extend(self.getExtraSubscribersOf(self._getPath(obj)).items())
            users_by_label[''] = users

        n_sent = 0
        for label, users in users_by_label.items():
            users = self.removeUnAuthorizedSubscribers(users, obj)
            bindings = extra_bindings.copy()
            bindings['label'] = label
            for user, how in users:
                # Fetch the delivery utilities the user requested, then use
                # that to notify
                for h in how:
                    try:
                        delivery = getUtility(INotificationDelivery, h)
                    except:
                        # The method is not known, or the third party
                        # product that provided it was uninstalled
                        LOG.warning("Could not look up INotificationDelivery "\
                            "utility named '%s'", h)
                        continue
                    n_sent += delivery.notify(obj, user, what, label,
                        bindings)

        return n_sent
    #################################################################


    #################################################################
    ## Utility methods
    ###############################
    decPrivate('ignoreNotification')
    def ignoreNotification(self, obj):
        """Return whether notification have been set to be ignored for
        ``obj``.
        """
        ec = getExpressionContext(obj)
        for match_expr in self.getProperty('ignore_rules', ()):
            try:
                if self._match(match_expr, ec):
                    return True
            except ConflictError:
                raise
            except:
                LOG.error("Error in 'ignore_rules' rule "\
                          "('%s') for '%s'",
                          match_expr, obj.absolute_url(1),
                          exc_info=True)
        return False


    decPrivate('getUsersToNotify')
    def getUsersToNotify(self, obj, what, ec_bindings=None):
        """Return a mapping from label to a list of user/how tuples,
        based on the passed ``what`` and ``ob``. ``what`` is one of the
        implemented notifications (*item_modification*, *wf_transition*,
        etc.). ``how`` is a string that says which delivery method to use.

        ``ec_bindings`` is a mapping which is injected into the
        expression context of the expression of the rules.
        """
        rules = self.getProperty('on_%s_users' % what, None)
        if rules is None:
            raise NotImplementedError, \
                "Notification on '%s' is not implemented." % what

        ec = getExpressionContext(obj, ec_bindings)
        users_by_label = {}
        ignore_next_rules = False
        for rule in rules:
            try:
                match_expr, users_expr = rule.split(RULE_DELIMITER, 1)
                parts = users_expr.split(RULE_DELIMITER)
                label = ''
                how = ('mail',)
                if len(parts) > 1:
                    users_expr, label = parts[:2]
                if len(parts) > 2:
                    how = tuple([p.strip() for p in parts[2:]])
            except ValueError:
                LOG.error("'%s' is not a valid rule "\
                          "('on_%s_users' on '%s')",
                          rule, what, obj.absolute_url(1))
                continue
            match_expr = match_expr.strip()
            users_expr = users_expr.strip()
            label = label.strip()
            users = users_by_label.get(label, [])
            try:
                if not self._match(match_expr, ec):
                    continue
            except ConflictError:
                raise
            except:
                LOG.error("Error in 'on_%s_users' rule "\
                          "('%s') for '%s'",
                          what, match_expr, obj.absolute_url(1),
                          exc_info=True)
                continue
            if users_expr == '*':
                users.extend([(u, how) for u in self.getAllUsers()])
                ignore_next_rules = True
            else:
                try:
                    users.extend([(u, how) for u in Expression(users_expr)(ec)])
                except ConflictError:
                    raise
                except:
                    LOG.error("Error in 'on_%s_users' rule "\
                              "('%s') for '%s'",
                              what, users_expr, obj.absolute_url(1),
                              exc_info=True)
            users_by_label[label] = users
            if ignore_next_rules:
                break
        return users_by_label


    decPrivate('getTemplate')
    def getTemplate(self, obj, what, ec_bindings=None):
        """Return the template to notify for the ``what`` of an object
        ``obj``, ``what`` being one of the implemented notification
        ("*item_modification*", "*wf_transition*", etc.), or ``None``
        if none could be found.

        ``ec_bindings`` is a mapping which is injected into the
        expression context of the expression of the rules.
        """
        rules = self.getProperty('on_%s_mail_template' % what, None)
        if rules is None:
            raise NotImplementedError, \
                'Notification on "%s" is not implemented.'

        ec = getExpressionContext(obj, ec_bindings)
        template = None
        for rule in rules:
            try:
                match_expr, template_expr = rule.split(RULE_DELIMITER)
                match_expr, template_expr = match_expr.strip(), template_expr.strip()
            except ValueError:
                LOG.error("'%s' is not a valid rule "\
                          "('on_%s_mail_template' on '%s')",
                          rule, what, obj.absolute_url(1))
                continue
            match_expr = match_expr.strip()
            template_expr = template_expr.strip()
            try:
                if not self._match(match_expr, ec):
                    continue
            except ConflictError:
                raise
            except:
                LOG.error("Error in 'on_%s_mail_template' rule "\
                          "('%s') for '%s'",
                          what, match_expr, obj.absolute_url(1),
                          exc_info=True)
                continue
            try:
                template = Expression(template_expr)(ec)
            except ConflictError:
                raise
            except:
                LOG.error("Error in 'on_%s_mail_template' rule "\
                          "('%s') for '%s'",
                          what, template_expr, obj.absolute_url(1),
                          exc_info=True)
                continue
            if type(template) == StringType:
                template = obj.restrictedTraverse(template, None)
            if template is not None:
                break
        return template


    decPrivate('getAllUsers')
    def getAllUsers(self):
        """Return a list of all user ids of the portal.

        **Warning:** this method may be costly if you rely on an
        external (non ZODB) user source. Use it at your own risk.
        """
        mtool = getToolByName(self, 'portal_membership')
        return mtool.listMemberIds()


    decPrivate('removeUnAuthorizedSubscribers')
    def removeUnAuthorizedSubscribers(self, subscribers, obj):
        """Return users from ``subscribers`` who are authorized to
        view ``obj``.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        mtool = getToolByName(self, 'portal_membership')
        filtered_subscribers = []
        for subscriber, notifymethod in subscribers:
            if self._anonymousShouldBeNotified(obj):
                filtered_subscribers.append((subscriber, notifymethod))
            else:
                ## We use '_huntUser()' and not 'mtool.getMemberById()'
                ## because the latter would provide a wrapped user
                ## object, with a specific context where the user is
                ## not allowed to view 'obj'.
                member = mtool._huntUser(str(subscriber), portal)
                if member is not None:
                    if member.has_permission('View', obj):
                        filtered_subscribers.append((subscriber, notifymethod))

        return filtered_subscribers


    def _match(self, expr, ec):
        """Return ``True`` if ``expr`` returns something which can be
        evaluated to ``True`` in the expression context (``ec``) or if
        ``expr`` is "*".
        """
        if expr == '*':
            return True
        expr = Expression(expr)
        return bool(expr(ec))


    def _getPath(self, obj):
        """Return path of ``obj``.

        A slash (``/``) is appended to the path if the object is
        folderish. The returned path is relative to the portal object.
        """
        utool = getToolByName(self, 'portal_url')
        path = utool.getRelativeContentURL(obj)
        path = '/' + path
        if not getattr(obj.aq_base, 'isPrincipiaFolderish', False):
            return path
        if path[-1] != '/':
            path += '/'
        return path


    def _getParents(self, path):
        """Get the parents of the item corresponding to ``path`` and
        return their respective path.

        Parents are returned from ``path`` to the portal root object.
        """
        if path == '/':
            return []
        if path[-1] == '/':
            path = path[:-1]
        parent = path[:path.rfind('/') + 1]
        parents = [parent]
        parents.extend(self._getParents(parent))
        return tuple(parents)


    def _getUID(self, obj):
        """Return UID of the object."""
        if not IATContentType.providedBy(obj) and not\
           IDexterityContent.providedBy(obj):
            return None

        portal_uidhandler = getToolByName(self, 'portal_uidhandler')
        uid = portal_uidhandler.queryUid(obj, None)
        # it should only register on subscribe. CSRF!
        return uid


    def _anonymousShouldBeNotified(self, obj):
        """Return whether anonymous users should be notified, i.e.
        whether anonymous users can view ``obj``.
        """
        return 'Anonymous' in rolesForPermissionOn('View', obj)

    def _getChangeNote(self, obj):
        """ If obj has version control, get the last change note and
        return it, otherwise return None. """
        request_changenote = self.REQUEST.get('cmfeditions_version_comment')
        if request_changenote is not None:
            return request_changenote

        # CMFEditions might not be around, protect against that.
        try:
            archivist = getToolByName(self, 'portal_archivist')
        except AttributeError:
            return None

        try:
            history = archivist.getHistory(obj)
        except ArchivistUnregisteredError:
            return None

        if len(history)>0:
            return history[-1].sys_metadata['comment']
        return None

    #################################################################


    #################################################################
    ## Extra subscriptions settings
    ###############################
    decProtected('View', 'isExtraSubscriptionsEnabled')
    def isExtraSubscriptionsEnabled(self):
        """Return whether extra subscriptions are enabled."""
        return self.getProperty('extra_subscriptions_enabled')


    decProtected('View', 'isExtraSubscriptionsRecursive')
    def isExtraSubscriptionsRecursive(self):
        """Return whether extra subscriptions are recursive.

        Note that this method does not check whether extra
        subscriptions are enabled or not.
        """
        return self.getProperty('extra_subscriptions_recursive')
    #################################################################


    #################################################################
    ## Extra subscriptions logic
    ############################
    def _updateSubscriptionMapping(self, obj, register=False):
        """Update subscription mapping."""
        uid = self._getUID(obj)
        if uid is None and register is not False:  # Not yet registered
            portal_uidhandler = getToolByName(self, 'portal_uidhandler')
            uid = portal_uidhandler.register(obj)
        if not uid:
            return

        path = self._getPath(obj)
        known_path = self._uid_to_path.get(uid)
        if known_path != path:
            self._uid_to_path[uid] = path
            if known_path is not None:
                ## We have old informations for this object
                for key, value in self._subscriptions.items():
                    if key.startswith(known_path):
                        new_key = path + key[len(known_path) : ]
                        self._subscriptions[new_key] = value
                        del self._subscriptions[key]


    decPublic('currentUserHasSubscribePermission')
    def currentUserHasSubscribePermissionOn(self, obj):
        """Return whether the current user is allowed to subscribe to
        or unsubscribe from ``obj``.
        """
        return True

        if not IATContentType.providedBy(obj) and not \
                IDexterityContent.providedBy(obj) and not \
                IPloneSiteRoot.providedBy(obj):
            return False

        mtool = getToolByName(self, 'portal_membership')
        return mtool.checkPermission(SUBSCRIBE_PERMISSION, obj)


    decPublic('subscribeTo')
    def subscribeTo(self, obj, email=None, how=['mail']):
        """Subscribe ``email`` (or the current user if ``email`` is
        None) to ``obj``. You can pass the methods by which the user should
        be notified as a tuple using the ``how`` keyword argument.
        """
        if not self.isExtraSubscriptionsEnabled():
            raise DisabledFeature

        if not self.currentUserHasSubscribePermissionOn(obj):
            raise Unauthorized
        elif email is not None:
            if not EMAIL_REGEXP.match(email):
                raise InvalidEmailAddress
            ## FIXME: an anonymous user would like to subscribe
            ## his/her address. This has not yet been implemented, so
            ## we raise an exception.
            raise NotImplementedError
        else:
            self._updateSubscriptionMapping(obj, register=True)
            path = self._getPath(obj)
            subscribers = self._subscriptions.get(path, {})
            user = getSecurityManager().getUser().getId()
            subscribers[user] = tuple(how)
            self._subscriptions[path] = subscribers


    decPublic('unSubscribeFrom')
    def unSubscribeFrom(self, obj, email=None):
        """Unsubscribe ``email`` (or the current user if ``email`` is
        ``None``) from ``obj``.
        """
        if not self.isExtraSubscriptionsEnabled():
            raise DisabledFeature

        if not self.currentUserHasSubscribePermissionOn(obj):
            raise Unauthorized
        elif email is not None:
            if not EMAIL_REGEXP.match(email):
                raise InvalidEmailAddress
            ## FIXME: an anonymous user would like to unsubscribe
            ## his/her address. This has not yet been implemented, so
            ## we raise an exception.
            raise NotImplementedError
        else:
            self._updateSubscriptionMapping(obj)
            path = self._getPath(obj)
            subscribers = self._subscriptions.get(path, {})
            user = getSecurityManager().getUser().getId()
            try:
                del subscribers[user]
                self._subscriptions[path] = subscribers
            except KeyError:
                pass ## User was not subscribed.


    decPublic('unSubscribeFromObjectAbove')
    def unSubscribeFromObjectAbove(self, obj, email=None):
        """Find folderish items above ``obj`` and unsubscribe
        ``email`` (or the current user if ``email`` is ``None``) from
        the first one (s)he is subscribed to.

        If ``user`` is subscribed to ``obj``, this method is
        equivalent to ``unSubscribeFrom(obj, user)``.
        """
        if not self.isExtraSubscriptionsEnabled():
            raise DisabledFeature

        if not self.currentUserHasSubscribePermissionOn(obj):
            raise Unauthorized
        elif email is not None:
            if not EMAIL_REGEXP.match(email):
                raise InvalidEmailAddress
            ## FIXME: an anonymous user would like to unsubscribe
            ## his/her address. This has not yet been implemented, so
            ## we raise an exception.
            raise NotImplementedError
        else:
            self._updateSubscriptionMapping(obj)
            utool = getToolByName(obj, 'portal_url')
            portal = utool.getPortalObject()
            portal_container = portal.aq_inner.aq_parent
            while obj != portal_container:
                if self.isSubscribedTo(obj, as_if_not_recursive=True):
                    self.unSubscribeFrom(obj)
                    break
                obj = obj.aq_parent


    decPublic('isSubscribedTo')
    def isSubscribedTo(self, obj, email=None,
                       as_if_not_recursive=False):
        """Return whether ``email`` (or the current user if ``email``
        is ``None``) is subscribed to ``obj``.

        If ``as_if_not_recursive`` is ``True``, this method acts as if
        the recursive mode was off.
        """
        if not self.isExtraSubscriptionsEnabled():
            raise DisabledFeature

        if email is None:
            ## Yes, 'email' is actually the id of the current user.
            email = getSecurityManager().getUser().getId()
        path = self._getPath(obj)
        subscribers = self.getExtraSubscribersOf(path,
                                                 as_if_not_recursive)
        return subscribers.has_key(email)


    decPrivate('getExtraSubscribersOf')
    def getExtraSubscribersOf(self, path, as_if_not_recursive=False):
        """Return users or email addresses which are subscribed to
        the given path.

        This method returns a mapping of users to tuples of notification
        methods, that is, each user can subscribe to be notified in more
        than one way.  If ``as_if_not_recursive`` is ``True``, this
        method acts as if the recursive mode was off.
        """
        subscribers = self._subscriptions.get(path, {}).copy()
        if self.isExtraSubscriptionsRecursive() and \
                not as_if_not_recursive:
            if path[-1] == '/':
                path = path[:-1]
            i = path.rfind('/')
            if i != -1:
                parent = path[:i + 1]
                subscribers.update(self.getExtraSubscribersOf(parent))
        return subscribers
    #################################################################


InitializeClass(NotificationTool)
