"""
author:木木夕
date:2020-01-07 09:58
"""
from django.db.models.fields.related_descriptors import ForwardOneToOneDescriptor, ReverseOneToOneDescriptor
from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor,ForwardManyToOneDescriptor

# 筛选所需要的字段
def jsonify(instance,allow=None,exclude=[],asname:dict=None,perfix="",is_verbosename=False):
    """
    过滤器
    :param instance:  查询集，单个
    :param allow:  白名单
    :param exclude:  黑名单
    :param asname:  使用自定义别名，字典
    :param perfix: 名称前缀
    :param is_verbosename:  #是否使用数据库，默认的别名verbose_name ,默认不使用
    :return:
    """
    # allow优先，如果有，就使用allow指定的字段，这时候exclude无效
    # allow如果为空，就全体，但要看看有exclude中的要排除
    if instance==None:
        return {}
    modelcls = type(instance)
    if allow:
        fn = (lambda x:x.name in allow)
    else:
        fn = (lambda x:x.name not in exclude)
    from django.db import models
    # 对于外键，取其id值
    def fnvalue(name):
        value = getattr(modelcls,name)
        # logging.info("&&&&&&&&&&&&&&&& {}, {}".format(value,type(value)))
        if isinstance(value,(ForwardOneToOneDescriptor,ReverseOneToOneDescriptor,ReverseManyToOneDescriptor,ForwardManyToOneDescriptor)):
            return getattr(instance,name+"_id")
        else:
            return getattr(instance,name)
    if asname:
        return {asname.get(k.name):fnvalue(k.name) for k in filter(fn,modelcls._meta.fields)}

    return {(perfix + (k.verbose_name if is_verbosename else k.name)) :fnvalue(k.name) for k in filter(fn,modelcls._meta.fields)}