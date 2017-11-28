"""Fields module."""

import datetime

import six

from . import errors


class Field(property):
    """Base field."""

    def __init__(self, default=None, required=False):
        """Initializer."""
        super(Field, self).__init__(self.get_value, self.set_value)
        self.name = None
        self.storage_name = None

        self.setter_fn = None
        self.getter_fn = None

        self.model_cls = None

        self.default = default
        self.required = required

    def bind_name(self, name):
        """Bind field to its name in model class."""
        if self.name:
            raise errors.Error('Already bound "{0}" with name "{1}" could not '
                               'be rebound'.format(self, self.name))
        self.name = name
        self.storage_name = ''.join(('_', self.name))
        return self

    def bind_model_cls(self, model_cls):
        """Bind field to model class."""
        if self.model_cls:
            raise errors.Error('"{0}" has been already bound to "{1}" and '
                               'could not be rebound to "{2}"'.format(
                                   self, self.model_cls, model_cls))
        self.model_cls = model_cls
        return self

    def init_model(self, model, value):
        """Init model with field.

        :param DomainModel model:
        :param object value:
        """
        if value is None and self.default is not None:
            value = self.default() if callable(self.default) else self.default

        self.set_value(model, value)

    def get_value(self, model, default=None):
        """Return field's value.

        :param DomainModel model:
        :param object default:
        :rtype object:
        """
        if default is not None:
            default = self._converter(default)

        if callable(self.getter_fn):
            value = self.getter_fn(model)
        else:
            value = getattr(model, self.storage_name)

        return value if value is not None else default

    def set_value(self, model, value):
        """Set field's value.

        :param DomainModel model:
        :param object value:
        """
        if value is None and self.required:
            raise AttributeError("This field is required.")

        if value is not None:
            value = self._converter(value)

        if callable(self.setter_fn) and value is not None:
            self.setter_fn(model, value)
        else:
            setattr(model, self.storage_name, value)

    def get_builtin_type(self, model):
        """Return built-in type representation of Field.

        :param DomainModel model:
        :rtype object:
        """
        return self.get_value(model)

    def getter(self, fn):
        """Set function for implementation custom getter feature."""
        self.getter_fn = fn

    def setter(self, fn):
        """Set function for implementation custom setter feature."""
        self.setter_fn = fn

    def _converter(self, value):
        """Convert raw input value of the field.

        :param object value:
        :rtype object:
        """
        return value

    @staticmethod
    def _get_model_instance(model_cls, data):
        """Convert dict into object of class of passed model.

        :param class model_cls:
        :param object data:
        :rtype DomainModel:
        """
        if not isinstance(data, (model_cls, dict)):
            raise TypeError('{0} is not valid type, instance of '
                            '{1} or dict required'.format(data, model_cls))
        return model_cls(**data) if isinstance(data, dict) else data


class Bool(Field):
    """Bool field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        return bool(value)


class Int(Field):
    """Int field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        return int(value)


class Float(Field):
    """Float field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        return float(value)


class String(Field):
    """String field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        return str(value)


class Binary(Field):
    """Binary field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        return six.binary_type(value)


class Date(Field):
    """Date field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        if not isinstance(value, datetime.date):
            raise TypeError('{0} is not valid date'.format(value))
        return value


class DateTime(Field):
    """Date and time field."""

    def _converter(self, value):
        """Convert raw input value of the field."""
        if not isinstance(value, datetime.datetime):
            raise TypeError('{0} is not valid date and time')
        return value


class Model(Field):
    """Model relation field."""

    def __init__(self, related_model_cls, default=None, required=False):
        """Initializer."""
        super(Model, self).__init__(default=default, required=required)
        self.related_model_cls = related_model_cls

    def _converter(self, value):
        """Convert raw input value of the field.

        :param object value:
        :rtype object:
        """
        return self._get_model_instance(self.related_model_cls, value)

    def get_builtin_type(self, model):
        """Return built-in type representation of Model.

        :param DomainModel model:
        :rtype dict:
        """
        return self.get_value(model).get_data()


class Collection(Field):
    """Models collection relation field."""

    def __init__(self, related_model_cls, default=None, required=False):
        """Initializer."""
        super(Collection, self).__init__(default=default, required=required)
        self.related_model_cls = related_model_cls

    def _converter(self, value):
        """Convert raw input value of the field.

        :param object value:
        :rtype object:
        """
        if type(value) is not self.related_model_cls.Collection:
            value = self.related_model_cls.Collection([
                self._get_model_instance(self.related_model_cls, item)
                for item in value])
        return value

    def get_builtin_type(self, model):
        """Return built-in type representation of Collection.

        :param DomainModel model:
        :rtype list:
        """
        return [item.get_data() if isinstance(item, self.related_model_cls)
                else item for item in self.get_value(model)]
