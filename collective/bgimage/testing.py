from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CollectiveBgimage(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.bgimage
        xmlconfig.file('configure.zcml',
                       collective.bgimage,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.bgimage:default')

COLLECTIVE_BGIMAGE_FIXTURE = CollectiveBgimage()
COLLECTIVE_BGIMAGE_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_BGIMAGE_FIXTURE, ),
                       name="CollectiveBgimage:Integration")