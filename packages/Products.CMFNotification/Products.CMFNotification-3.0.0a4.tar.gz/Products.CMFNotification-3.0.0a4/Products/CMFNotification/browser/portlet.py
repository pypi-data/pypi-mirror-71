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
"""Define subscription portlet.

$Id$
"""

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import getUtilitiesFor
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import MessageFactory
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.CMFNotification.NotificationTool import ID as NTOOL_ID
from Products.CMFNotification.interfaces import INotificationDelivery


mf = MessageFactory('cmfnotification')


class ISubscriptionPortlet(IPortletDataProvider):
    """A portlet which allow an user to subscribe/unsubscribe to
    content changes.
    """


class Assignment(base.Assignment):
    implements(ISubscriptionPortlet)

    title = mf(u'notification_portlet_header',
               default=u'Subscription')


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('templates/portlet.pt')


    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        ## FIXME: looks like 'update()' is not called before render if
        ## I do not do that
        if self.available:
            self.update()


    @property
    def available(self):
        ntool = getToolByName(self.context, NTOOL_ID, None)
        if ntool is None:
            ## Looks like the product has been removed but the portlet
            ## is still configured to appear somewhere.
            return False
        if not ntool.isExtraSubscriptionsEnabled():
            return False

        # Don't show the portlet for temporary content in portal_factory
        if getattr(self.context, 'isTemporary', lambda: False)():
            return False

        return ntool.currentUserHasSubscribePermissionOn(self.context)


    @property
    def notifiers(self):
        li = [dict(id=i, description=d.description) for \
            i, d in getUtilitiesFor(INotificationDelivery)]
        return li

    @property
    def isSubscriptionToParentAllowed(self):
        """Return whether subscription to the parent of the context
        (i.e. the first folderish item above the context) is allowed.
        """
        ntool = getToolByName(self.context, NTOOL_ID)
        if not ntool.isExtraSubscriptionsRecursive():
            return False

        context = self.context.aq_inner
        plone_view = getMultiAdapter((context, self.request),
                                     name='plone')

        if not plone_view.isDefaultPageInFolder():
            return False

        parent = context.aq_parent
        return ntool.currentUserHasSubscribePermissionOn(parent)


    def update(self):
        ntool = getToolByName(self.context, NTOOL_ID)
        self.is_subscribed = ntool.isSubscribedTo(self.context)
        self.is_subscribed_here = ntool.isSubscribedTo(self.context,
                                                       as_if_not_recursive=True)


class AddForm(base.NullAddForm):
    def create(self):
        return Assignment()
