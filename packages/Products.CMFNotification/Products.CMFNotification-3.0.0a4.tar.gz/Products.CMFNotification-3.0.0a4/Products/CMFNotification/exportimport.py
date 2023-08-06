"""CMFNotification Generic Setup handlers.

$Id$
"""

from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter

from Products.GenericSetup.interfaces import IBody

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import setDefaultRoles

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from Products.CMFNotification.browser import portlet
from Products.CMFNotification.config import PORTLET_NAME
from Products.CMFNotification.permissions import SUBSCRIBE_PERMISSION


_FILENAME = 'cmfnotification.xml'


def importCMFNotification(context):
    """Import CMFNotification tool properties."""
    site = context.getSite()
    logger = context.getLogger('CMFNotification')
    ntool = getToolByName(site, 'portal_notification', None)

    body = context.readDataFile(_FILENAME)
    if body is None:
        logger.info('Nothing to import.')
        return

    importer = queryMultiAdapter((ntool, context), IBody)
    if importer is None:
        logger.warning('Import adapter missing.')
        return

    importer.body = body
    logger.info('CMFNotification tool imported.')


def exportCMFNotification(context):
    """Export CMFNotification tool properties."""
    site = context.getSite()
    logger = context.getLogger('CMFNotification')
    ntool = getToolByName(site, 'portal_notification', None)
    if ntool is None:
        logger.info('Nothing to export.')
        return

    exporter = queryMultiAdapter((ntool, context), IBody)
    if exporter is None:
        logger.warning('CMFNotification adapter missing.')
        return

    context.writeDataFile(_FILENAME, exporter.body, exporter.mime_type)
    logger.info('MemberData tool exported.')


def addPortlet(context):
    """Add CMFNotification portlet to the right column."""
    if not context.readDataFile(_FILENAME):
        return

    portal = context.getSite()
    rightColumn = getUtility(IPortletManager,
                             name=u'plone.rightcolumn',
                             context=portal)
    right = getMultiAdapter((portal, rightColumn),
                            IPortletAssignmentMapping,
                            context=portal)
    if PORTLET_NAME not in right:
        right[PORTLET_NAME] = portlet.Assignment()


def addPermissions(context):
    """Add specific permissions."""
    setDefaultRoles(SUBSCRIBE_PERMISSION, ('Manager', ))
