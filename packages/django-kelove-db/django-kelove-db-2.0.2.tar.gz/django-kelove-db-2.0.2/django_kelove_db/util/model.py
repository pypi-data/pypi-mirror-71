# ==================================================================
#       文 件 名: model.py
#       概    要: 模型基类
#       作    者: IT小强 
#       创建时间: 6/8/20 2:38 PM
#       修改时间: 
#       copyright (c) 2016 - 2020 mail@xqitw.cn
# ==================================================================

import json

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from . import helper


class Model(models.Model):
    """
    数据模型基类
    """

    class Meta:
        abstract = True


class ModelCreatedBy(models.Model):
    """
    添加创建人外键
    """

    # 创建人
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('创建用户ID'),
        related_name="created_by_set",
        on_delete=helper.get_kelove_databases_settings('FOREIGN_DELETE_TYPE', models.PROTECT),
        db_constraint=helper.get_kelove_databases_settings('DB_CONSTRAINT_USER', False),
        null=True,
        blank=True,
        editable=False,
        default=None
    )

    class Meta:
        abstract = True


class ModelUpdatedBy(models.Model):
    """
    添加更新人外键
    """

    # 更新人
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('更新用户ID'),
        related_name="updated_by_set",
        on_delete=helper.get_kelove_databases_settings('FOREIGN_DELETE_TYPE', models.PROTECT),
        db_constraint=helper.get_kelove_databases_settings('DB_CONSTRAINT_USER', False),
        null=True,
        blank=True,
        editable=False,
        default=None
    )

    class Meta:
        abstract = True


class ModelCreatedTime(models.Model):
    """
    添加创建时间
    """

    # 创建时间
    created_at = models.DateTimeField(verbose_name=_('创建时间'), auto_now_add=True, editable=True)

    class Meta:
        abstract = True


class ModelUpdatedTime(models.Model):
    """
    添加更新时间
    """

    # 更新时间
    updated_at = models.DateTimeField(verbose_name=_('更新时间'), auto_now=True)

    class Meta:
        abstract = True


class ModelStatus(models.Model):
    """
    添加状态字段
    """

    # 状态
    status = models.IntegerField(
        verbose_name=_('状态'),
        null=False,
        default=0,
        choices=helper.get_kelove_databases_settings('STATUS_CHOICES', helper.STATUS_CHOICES),
        help_text=_('状态') + json.dumps(
            dict(helper.get_kelove_databases_settings('STATUS_CHOICES', helper.STATUS_CHOICES)),
            ensure_ascii=False
        )
    )

    class Meta:
        abstract = True


class ModelEnabled(models.Model):
    """
    添加是否启用字段
    """

    # 是否启用
    enabled = models.BooleanField(
        verbose_name=_('是否启用'),
        default=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class ModelSort(models.Model):
    """
    添加排序字段
    """

    # 排序
    sort = models.IntegerField(
        verbose_name=_('排序'),
        null=False,
        default=0,
    )

    class Meta:
        abstract = True


class ModelBaseNoUser(ModelCreatedTime, ModelUpdatedTime, ModelSort, ModelStatus, ModelEnabled):
    """
    数据模型基类（不包括创建人、更新人字段）
    """

    class Meta:
        abstract = True


class ModelBaseOnlyTime(ModelCreatedTime, ModelUpdatedTime):
    """
    数据模型基类（仅包含时间字段）
    """

    class Meta:
        abstract = True


class ModelBaseOnlyUser(ModelCreatedBy, ModelUpdatedBy):
    """
    数据模型基类（仅包含创建、更新用户字段）
    """

    class Meta:
        abstract = True


class ModelBaseAll(ModelBaseOnlyUser, ModelBaseOnlyTime, ModelStatus, ModelEnabled, ModelStatus):
    """
    数据模型基类(添加全部公用字段)
    """

    class Meta:
        abstract = True
