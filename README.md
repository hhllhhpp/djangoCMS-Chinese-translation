# djangoCMS-Chinese-translation
djangoCMS的中文翻译不全，此项目用于将djangCMS全部汉化

python版本：3.5.3

django版本：1.8.18

djangCMS版本：3.4.4

# 安装

### 注：下述需要修改的文件大多在site-packages中。修改文件示例中是修改好的文件，可以拿来参考

1. 安装
将djangocms_dd_custom_config文件夹拷贝到你的项目文件夹下

2. 在settings.py的INSTALLED_APPS中添加
```python
djangocms_dd_custom_config
```
在settings.py的LOCALE_PATHS中添加
```python
os.path.join(BASE_DIR, 'djangocms_dd_custom_config', 'locale'),
```
将settings.py的LANGUAGES和CMS_LANGUAGES中的gettext('zh')改为'中文'

3. 在settings.py中添加
```python
from djangocms_dd_custom_config.settings import *
```
4. 将settings.py同目录下urls.py中的
```python
urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)
```
改为
```python
if settings.CUSTOM_CMS_LANGUAGE_IN_URL:
    urlpatterns += i18n_patterns(
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('cms.urls')),
    )
else:
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include('cms.urls')),
    ]
```
5. 将cmsplugin_filer_file、cmsplugin_filer_folder、cmsplugin_filer_image、cmsplugin_filer_link、cmsplugin_filer_teaser、cmsplugin_filer_video应用下的cms_plugins.py中的module = 'Filer'修改为module = _('Filer')
6. 将cms/models/static_placeholder.py的第44行的
```python
site = models.ForeignKey(Site, null=True, blank=True)
```
改为
```python
site = models.ForeignKey(Site, null=True, blank=True, verbose_name=_('site'))
```
7. 将filer/admin/folderadmin.py的第430行的
```python
'title': 'Directory listing for %s' % folder.name,
```
改为
```python
'title': _('Directory listing for %s') % folder.name,
```
8. 将djangocms_colunm/models.py的第36行添加
```python
class Meta:
    verbose_name = _("Multi Columns")
    verbose_name_plural = _("Multi Columns")
```
在第61行添加
```python
class Meta:
    verbose_name = _("Column")
    verbose_name_plural = _("Column")
```
9. 将djangocms_filer_file/models.py的第85行添加
```python
class Meta:
    verbose_name = _("filer file")
    verbose_name_plural = _("filer file")
```
10. 将djangocms_filer_folder/models.py的第52行添加
```python
class Meta:
    verbose_name = _("filer folder")
    verbose_name_plural = _("filer folder")
```
11. 将djangocms_filer_folder/models.py的第23行的
```python
folder = FilerFolderField(null=True, on_delete=models.SET_NULL)
```
改为
```python
folder = FilerFolderField(null=True, on_delete=models.SET_NULL, verbose_name=_("Folder"))
```
12. 将django/contrib/auth/model.py的第80行的
```python
six.text_type(self.name))
```
改为
```python
_(six.text_type(self.name)))
```

13. 将cms/models/aliaspluginmodel.py的第5行添加
```python
from django.utils.translation import ugettext_lazy as _
```
在第18行添加
```python
verbose_name = _('aliaspluginmodel')
verbose_name_plural = _('aliaspluginmodel')
```

14. 将cms/models/pluginmodel.py的第196行添加
```python
verbose_name = _('cmsplugin')
verbose_name_plural = _('cmsplugin')
```

15. 将cms/models/placeholdermodel.py的第46行添加
```python
verbose_name = _('placeholder')
verbose_name_plural = _('placeholder')
```

16. 将cms/models/placeholderpluginmodel.py的第7行添加
```python
from django.utils.translation import ugettext_lazy as _
```
在第17行添加
```python
verbose_name = _('placeholderreference')
verbose_name_plural = _('placeholderreference')
```
17. 将cms/models/titlemodels.py的第54行添加
```python
verbose_name = _('title')
verbose_name_plural = _('title')
```

18. 将cms/models/apphooks_reload.py的第8行添加
```python
from django.utils.translation import ugettext_lazy as _
```
在第16行添加
```python
verbose_name = _('urlconfrevision')
verbose_name_plural = _('urlconfrevision')
```

19. 将djangocms_googlemap/model.py的第194行添加
```python
class Meta:
    verbose_name = _("google map")
    verbose_name_plural = _("google map")
```
在第264行添加
```python
class Meta:
    verbose_name = _("google map maker")
    verbose_name_plural = _("google map maker")
```
在第308行添加
```python
class Meta:
    verbose_name = _("google map route")
    verbose_name_plural = _("google map route")
```
20. 将djangcms_link/models.py的第218行添加
```python
verbose_name = _("link")
verbose_name_plural = _('link')
```

21. 将djangocms_style/models.py的第230行添加
```python
class Meta:
    verbose_name = _("style")
    verbose_name_plural = _("style")
```

22. 将menus/models.py的第3行添加
```python
from django.utils.translation import ugettext_lazy as _
```
在第34行添加
```python
class Meta:
    verbose_name = _("cache key")
    verbose_name_plural = _("cache key")
```

23. 将easy_thumbnails/models.py的第5行添加
```python
from django.utils.translation import ugettext_lazy as _
```
第72行pass改为
```python
class Meta:
    verbose_name = _("source")
    verbose_name_plural = _("source")
```
在第85行添加
```python
verbose_name = _("thumbnail")
verbose_name_plural = _("thumbnail")
```
在第102行添加
```python
class Meta:
    verbose_name = _("thumbnaildimensions")
    verbose_name_plural = _("thumbnaildimensions")
```

24. 将djangocms_text_ckeditor/models.py的第123行添加
```python
verbose_name = _("text")
verbose_name_plural = _("text")
```

25. 将djangocms_video/models.py的第96行添加
```python
class Meta:
    verbose_name = _("video player")
    verbose_name_plural = _("video player")
```
将第150行添加
```python
class Meta:
    verbose_name = _("video source")
    verbose_name_plural = _("video source")
```
将第201行添加
```python
class Meta:
    verbose_name = _("video track")
    verbose_name_plural = _("video track")
```

26. 将djangocms_snippet/models.py的第70行
```python
snippet = models.ForeignKey(Snippet)
```
改为
```python
snippet = models.ForeignKey(Snippet, verbose_name=_('snippet'))
```

# 使用
1. 如果想自定义djangocms_dd_custom_config的翻译，需要首先安装gettext。然后修改djangocms_dd_custom_config/locale/zh/LC_MESSAGES/collection中相对应的po文件（注：djangocms_dd_custom_config/locale/zh/LC_MESSAGES/collection中的po文件是手动搜集的INSTALLED_APPS中应用的po文件，翻译的时候最好确保所有po文件相同词条下的翻译是相同的）。最后运行
```bash
msgcat --use-first -o ./djangocms_dd_custom_config/locale/zh/LC_MESSAGES/django.po ./djangocms_dd_custom_config/locale/zh/LC_MESSAGES/collection/*.po
msgcat --use-first -o ./djangocms_dd_custom_config/locale/zh/LC_MESSAGES/djangojs.po ./djangocms_dd_custom_config/locale/zh/LC_MESSAGES/collection/js/*.po
python manage.py compilemessages
```
2. CKEDITOR_SETTINGS——DjangoCMS中文本框的配置项
3. CUSTOM_CMS_LANGUAGE_IN_URL——在单语言模式下，是否在URL中显示语言代码的配置项，设置为False则不显示语言代码
