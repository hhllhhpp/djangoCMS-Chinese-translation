# 富文本编辑器
CKEDITOR_SETTINGS = {
    'language': 'zh-cn',
    'skin': 'moono-lisa',
}

# 是否在URL中显示语言代码
CUSTOM_CMS_LANGUAGE_IN_URL = False

# 自定义CMS上的工具栏
CMS_TOOLBARS = [
    # CMS Toolbars
    'cms.cms_toolbars.PlaceholderToolbar',
    # 去掉语言栏和网站配置中关于语言的用户配置
    'djangocms_dd_custom_config.cms_toolbars.BasicToolbar',
    'cms.cms_toolbars.PageToolbar',

    # third-party Toolbar
]
