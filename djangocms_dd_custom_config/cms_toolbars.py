# -*- coding: utf-8 -*-
from classytags.utils import flatten_context
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_permission_codename, get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import NoReverseMatch
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from cms.api import get_page_draft
from cms.models import CMSPlugin
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.i18n import get_language_tuple
from cms.utils import get_cms_setting
from cms.utils import page_permissions
from cms.utils.permissions import get_user_sites_queryset

from cms.utils.urlutils import admin_reverse
from menus.utils import DefaultLanguageChanger


# Identifiers for search
ADMIN_MENU_IDENTIFIER = 'admin-menu'
LANGUAGE_MENU_IDENTIFIER = 'language-menu'
TEMPLATE_MENU_BREAK = 'Template Menu Break'
PAGE_MENU_IDENTIFIER = 'page'
PAGE_MENU_ADD_IDENTIFIER = 'add_page'
PAGE_MENU_FIRST_BREAK = 'Page Menu First Break'
PAGE_MENU_SECOND_BREAK = 'Page Menu Second Break'
PAGE_MENU_THIRD_BREAK = 'Page Menu Third Break'
PAGE_MENU_FOURTH_BREAK = 'Page Menu Fourth Break'
PAGE_MENU_LAST_BREAK = 'Page Menu Last Break'
HISTORY_MENU_BREAK = 'History Menu Break'
MANAGE_PAGES_BREAK = 'Manage Pages Break'
ADMIN_SITES_BREAK = 'Admin Sites Break'
ADMINISTRATION_BREAK = 'Administration Break'
CLIPBOARD_BREAK = 'Clipboard Break'
USER_SETTINGS_BREAK = 'User Settings Break'
ADD_PAGE_LANGUAGE_BREAK = "Add page language Break"
REMOVE_PAGE_LANGUAGE_BREAK = "Remove page language Break"
COPY_PAGE_LANGUAGE_BREAK = "Copy page language Break"
TOOLBAR_DISABLE_BREAK = 'Toolbar disable Break'


@toolbar_pool.register
class BasicToolbar(CMSToolbar):
    """
    Basic Toolbar for site and languages menu
    """
    page = None
    _language_menu = None
    _admin_menu = None

    def init_from_request(self):
        self.page = get_page_draft(self.request.current_page)

    def populate(self):
        if not self.page:
            self.init_from_request()
            self.clipboard = self.request.toolbar.user_settings.clipboard
            self.add_admin_menu()

    def add_admin_menu(self):
        if not self._admin_menu:
            self._admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, self.current_site.name)
            # Users button
            self.add_users_button(self._admin_menu)

            # sites menu
            sites_queryset = get_user_sites_queryset(self.request.user)

            if len(sites_queryset) > 1:
                sites_menu = self._admin_menu.get_or_create_menu('sites', _('Sites'))
                sites_menu.add_sideframe_item(_('Admin Sites'), url=admin_reverse('sites_site_changelist'))
                sites_menu.add_break(ADMIN_SITES_BREAK)
                for site in sites_queryset:
                    sites_menu.add_link_item(site.name, url='http://%s' % site.domain,
                                             active=site.pk == self.current_site.pk)

            # admin
            self._admin_menu.add_sideframe_item(_('Administration'), url=admin_reverse('index'))
            self._admin_menu.add_break(ADMINISTRATION_BREAK)

            # clipboard
            if self.toolbar.edit_mode or self.toolbar.build_mode:
                # True if the clipboard exists and there's plugins in it.
                clipboard_is_bound = self.get_clipboard_plugins().exists()

                self._admin_menu.add_link_item(_('Clipboard...'), url='#',
                        extra_classes=['cms-clipboard-trigger'],
                        disabled=not clipboard_is_bound)
                self._admin_menu.add_link_item(_('Clear clipboard'), url='#',
                        extra_classes=['cms-clipboard-empty'],
                        disabled=not clipboard_is_bound)
                self._admin_menu.add_break(CLIPBOARD_BREAK)

            # Disable toolbar
            self._admin_menu.add_link_item(_('Disable toolbar'), url='?%s' % get_cms_setting('CMS_TOOLBAR_URL__DISABLE'))
            self._admin_menu.add_break(TOOLBAR_DISABLE_BREAK)

            # logout
            self.add_logout_button(self._admin_menu)

    def add_users_button(self, parent):
        User = get_user_model()

        if User in admin.site._registry:
            opts = User._meta

            if self.request.user.has_perm('%s.%s' % (opts.app_label, get_permission_codename('change', opts))):
                user_changelist_url = admin_reverse('%s_%s_changelist' % (opts.app_label, opts.model_name))
                parent.add_sideframe_item(_('Users'), url=user_changelist_url)

    def add_logout_button(self, parent):
        # If current page is not published or has view restrictions user is redirected to the home page:
        # * published page: no redirect
        # * unpublished page: redirect to the home page
        # * published page with login_required: redirect to the home page
        # * published page with view permissions: redirect to the home page

        if (self.page and self.page.is_published(self.current_lang) and not self.page.login_required and
                page_permissions.user_can_view_page(AnonymousUser(), page=self.page)):
            on_success = self.toolbar.REFRESH_PAGE
        else:
            on_success = '/'

        # We'll show "Logout Joe Bloggs" if the name fields in auth.User are completed, else "Logout jbloggs". If
        # anything goes wrong, it'll just be "Logout".

        user_name = self.get_username()
        logout_menu_text = _('Logout %s') % user_name if user_name else _('Logout')

        parent.add_ajax_item(logout_menu_text, action=admin_reverse('logout'), active=True, on_success=on_success)

    def add_language_menu(self):
        if settings.USE_I18N and not self._language_menu:
            self._language_menu = self.toolbar.get_or_create_menu(LANGUAGE_MENU_IDENTIFIER, _('Language'), position=-1)
            language_changer = getattr(self.request, '_language_changer', DefaultLanguageChanger(self.request))
            for code, name in get_language_tuple(self.current_site.pk):
                try:
                    url = language_changer(code)
                except NoReverseMatch:
                    url = DefaultLanguageChanger(self.request)(code)
                self._language_menu.add_link_item(name, url=url, active=self.current_lang == code)

    def get_username(self, user=None, default=''):
        user = user or self.request.user
        try:
            name = user.get_full_name()
            if name:
                return name
            else:
                return user.get_username()
        except (AttributeError, NotImplementedError):
            return default

    def get_clipboard_plugins(self):
        self.populate()

        if not hasattr(self, "clipboard"):
            return CMSPlugin.objects.none()
        return self.clipboard.get_plugins().select_related('placeholder')

    def render_addons(self, context):
        context.push()
        context['local_toolbar'] = self
        clipboard = mark_safe(render_to_string('cms/toolbar/clipboard.html', flatten_context(context)))
        context.pop()
        return [clipboard]
