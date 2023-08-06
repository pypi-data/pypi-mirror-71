# Django Db 增强（目前只完善MySQL）

## 主要功能

+ 迁移支持写入表注释及字段注释

+ 迁移支持写入字段默认值

+ 常用字段数据模型基类 `django_kelove_db.abstract_models`

+ 在线数据库设计文档生成

+ JSON字段支持

## 使用示例

+ 修改django配置文件 ENGINE 为 django_kelove_db.backends.mysql

+ 配置 `INCLUDE_DEFAULT` (可选)，示例如下

```
DATABASES = {
    'default': {
        'ENGINE': 'django_kelove_db.backends.mysql',
        'NAME': 'django_kelove',
        'USER': 'django_kelove',
        'PASSWORD': 'django_kelove',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'INCLUDE_DEFAULT': lambda model, field, include_default, connection: False if field.db_parameters(
            connection=connection
        )['type'] in ['longtext', 'longblob'] else True
    }
}

KELOVE_DATABASES = {
    'FOREIGN_DELETE_TYPE': 'django.db.models.deletion.PROTECT',
    'DB_CONSTRAINT': False,
    'DB_CONSTRAINT_USER': False,
    'USER_EDITABLE': False,
    'STATUS_CHOICES': [(-1, '草稿'), (0, '待审'), (1, '通过'), (2, '驳回')],
    'DOC_TITLE': '数据库设计文档',
    'JSON_FIELD_SETTINGS': {
        "mode": "tree",
        "modes": ["code", "form", "text", "tree", "view", "preview"],
    },
    'EDITOR_MD_FIELD_SETTINGS': {
        'readOnly': False,
        'theme': '',
        'previewTheme': '',
        'editorTheme': 'default',
        'autoFocus': False,
        'toolbarAutoFixed': False,
        'emoji': True,
        'codeFold': True,
        'tocDropdown': True,
        'mode': 'markdown',
    }
}

```

+ 使用数据库文档功能时，需要将应用添加到 `INSTALLED_APPS` ,并添加路由

```
INSTALLED_APPS = [
    ...
    'django_kelove_db.apps.DjangoKeloveDbConfig',
    ...
]

```

```
from django.conf.urls import url
from django.urls import include

urlpatterns = [
    ...
    url(r'doc/', include('django_kelove_db.urls')),
    ...
]

```

+ 扩展字段使用示例

```

from django.db import models

from django_kelove_db.util import fields

class JsonFieldTable(models.Model):

    """ json 字段 """
    json_field = fields.JSONField(
        default='{}',
        field_settings={
            "mode": "tree",
            "modes": ["code", "form", "text", "tree", "view", "preview"],
        },
        verbose_name='JSON字段',
    )

    """ Markdown 编辑器字段 """
    markdown_field = fields.EditorMdField(
         default='### 测试',
         verbose_name='EditorMdField',
         field_settings={
             'readOnly': True,
             'theme': '',
             'previewTheme': '',
         },
     )
```
