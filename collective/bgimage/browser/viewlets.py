from zope.component import getMultiAdapter

from plone.memoize.view import memoize
from plone.app.layout.viewlets import common as base
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.interfaces import ISiteRoot

# Logo sollte default sein
default = None

TEMPLATE = u"""
<script type="text/javascript" class="javascript-settings">
    var FullscreenrOptions = {  width: %(width)s, height: %(height)s, bgID: '#bgimg1' };
    jQuery.fn.fullscreenr(FullscreenrOptions);
</script>
"""

class BGImageViewlet(base.ViewletBase):
    """ Add a div with a background image
    """

    def getContainer(self):
        """ Get the item for which we perform the listing
        """
        context = self.context.aq_inner
        if IFolderish.providedBy(context):
            return context
        else:
            return context.aq_parent

    def getBGImageFromFolder(self, folder):
        brains = folder.getFolderContents({'portal_type':'Image',
                                           'Subject':'background',}) 
        if len(brains)>0:
            return brains[0].getObject()
        return None

    def getDefaultImage(self):
        portal_state = getMultiAdapter((self.context, self.request), 
                                       name=u'plone_portal_state')
        site = portal_state.portal()
        return self.getBGImageFromFolder(site)

    def getBGimage(self):
        """
        """
        self.image = None
        folder = self.getContainer()
        while not ISiteRoot.providedBy(folder):
            if not hasattr(folder, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(parent))
            self.image = self.getBGImageFromFolder(folder)
            folder = folder.aq_parent
            if self.image is not None:
                return
        self.image = self.getDefaultImage()

    @memoize
    def bgimg(self):
        self.getBGimage()
        if self.image:
            return self.image

    def bgimageurl(self):
        image = self.bgimg()
        if image==None:
            return
        return image.absolute_url()

    def init_js(self):
        image = self.bgimg()
        if image==None:
            return
        width = image.width
        height = image.height
        # Use Python string template facility to produce the code
        html = TEMPLATE % { "width" : width, "height" : height, }
        return html