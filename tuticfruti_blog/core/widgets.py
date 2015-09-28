# -*- coding: utf-8 -*-
from django.forms import widgets
from django.utils import formats
from django.utils.encoding import force_text
from django.forms.utils import flatatt
from django.utils.html import format_html


class BootstrapInput(widgets.Widget):
    input_type = None

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value is None:
            value = ''
        if value:
            final_attrs['value'] = force_text(self._format_value(value))
        if final_attrs.get('class'):
            final_attrs['class'] = '{} {}'.format(final_attrs['class'], 'form-control')
        else:
            final_attrs['class'] = 'form-control'

        return format_html(
            '<label for={}">{}</label>\r\n'.format(name, name.capitalize()) +
            '<input{}>\r\n',
            flatatt(final_attrs))


class BootstrapTextInput(BootstrapInput):
    input_type = 'text'


class BootstrapEmailInput(BootstrapInput):
    input_type = 'email'


class BootstrapTextarea(widgets.Widget):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if final_attrs.get('class'):
            final_attrs['class'] = '{} {}'.format(final_attrs['class'], 'form-control')
        else:
            final_attrs['class'] = 'form-control'

        return format_html(
            '<textarea{}>\r\n' +
            '  {}\r\n' +
            '</textarea>\r\n',
            flatatt(final_attrs),
            force_text(value))
