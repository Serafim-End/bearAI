# coding: utf-8
import json
import re

from datetime import datetime, timedelta

from slots.models import Parameter

from slots.adapter import SlotFillingAdapter
from assistant.utils.w2v_processing import morph


class CustomSlotFillingAdapter(SlotFillingAdapter):

    DIGIT = 'integer'
    FLOAT = 'float'
    DATETIME = 'time'

    def __init__(self, intent, parameters, **kwargs):
        super(CustomSlotFillingAdapter, self).__init__(intent, **kwargs)

        self.parameters = parameters

    def can_process(self, statement):
        if statement.message:
            return True
        return False

    def process(self, statement):
        """
        example of base_parameters :
        base_parameters = {
            'personsCount': {'is_obligatory': True, 'value': DIGIT},
            'datetime': {'is_obligatory': True, 'value': DATETIME},
            'rest_name': {
                'is_obligatory': True,
                'value': {
                    'воронеж': ('ворож', 'ворожня'),
                    'какуля': ('какулин', 'какастаран'),
                    'карлсон': ('карлик', 'форсизонс'),
                }
            },
            'latitude': {'is_obligatory': False, 'value': FLOAT},
            'longitude': {'is_obligatory': False, 'value': FLOAT}
        }
        :param statement:
        :return:
        """

        def try_json(myjson):
            try:
                return json.loads(myjson)
            except ValueError, e:
                return None

        def load_parameters(value):
            pos_json = try_json(value)
            if pos_json:
                return pos_json
            else:
                return value

        words = statement.message.split(' ')

        # should be a list of Parameter
        base_parameters = Parameter.objects.filter(intent=self.intent).all()

        if not self.parameters:
            self.parameters = []

        dict_base_parameters = []
        for parameter in base_parameters:
            par_dict = {
                'name': parameter.name,
                'is_obligatory': parameter.is_obligatory,
                'value': load_parameters(parameter.value)
            }
            if len(self.parameters) < len(base_parameters):
                self.parameters.append({})
            dict_base_parameters.append(par_dict)

        for k, v in enumerate(dict_base_parameters):
            value = v['value']
            self.parameters[k]['name'] = v['name']
            self.parameters[k]['is_obligatory'] = v['is_obligatory']
            for t, func in {self.FLOAT: self._detect_float,
                            self.DIGIT: self._detect_digit}.iteritems():
                if value == t:
                    prm_value, words = func(words)
                    if prm_value:
                        self.parameters[k]['value'] = prm_value
            if value == self.DATETIME:
                prm_value, words = self._detect_datetime(statement.message)
                if prm_value:
                    self.parameters[k]['value'] = prm_value.isoformat()
            if isinstance(value, dict):
                prm_value, words = self._detect_name(value, words)
                if prm_value:
                    self.parameters[k]['value'] = prm_value
        return self.parameters

    def _detect_name(self, value, words):
        def get_value(names, candidates):
            for sinonym in names:
                for w in candidates:
                    if w.find(sinonym) > -1:
                        return w
            return None

        for n, ren in value.iteritems():
            names = [n] + list(ren)
            candidate = get_value(names, words)
            if candidate:
                words.remove(candidate)
                return n, words

        return None, words

    def _detect_digit(self, words):
        for w in words:
            if w.isdigit():
                # return w, words.pop(w) вероятно ошибочно
                words.remove(w)
                return w, words
        return None, words

    def _detect_float(self, words):
        for w in words:
            count, flag = 0, True
            for s in w:
                if s == '.' and count < 2:
                    count += 1
                elif not s.isdigit():
                    flag = False
                    break
            if flag:
                return w, words.pop(w)
        return None, words

    def _detect_datetime(self, words):

        when_month = {
            'january': 'январь',
            'february': 'февраль',
            'march': 'март',
            'april': 'апрель',
            'may': 'май',
            'june': 'июнь',
            'july': 'июль',
            'august': 'август',
            'september': 'сентябрь',
            'october': 'октябрь',
            'november': 'ноябрь',
            'december': 'декабрь'
        }

        when_nearest_tuple = (
            (('сегодня', 'сейчас', 'ближайшее'), 0),
            (('послезавтра', ), 2),
            (('завтра', ), 1))

        when_week = {
            0: ['понедельник'],
            1: ['вторник'],
            2: ['среду', 'среда'],
            3: ['четверг'],
            4: ['пятниц', 'пятницу'],
            5: ['cуббот', 'суботу', 'субботу', 'суббота'],
            6: ['воскрес', 'воскресенье']
        }

        # TODO: write some lewinstein distance here, but not for reg exp

        def word_root(word):
            m = morph.parse(when_month[word].decode('utf-8'))[0].normal_form
            if m[-1] == u'ь':
                return m[:-1]
            return m

        def get_text_date(search_text, d):
            text_date = re.search(
                '\d{1,2} ' + word_root(d.strftime(format='%B').lower()),
                search_text
            )

            if text_date:
                try:
                    d_time = datetime.utcnow().replace(day=int(
                        text_date.group(0).split(' ')[0]))
                except:
                    d_time = None

                return d_time

        text = words.lower()
        n = datetime.utcnow()

        digit_date = re.search('\d{1,2}[\.|: ;мю,]\d{1,2}', text)
        if digit_date:
            d, m = map(int, re.split('[\.|: ;мю,]', digit_date.group(0)))

            try:
                d_time = datetime.utcnow().replace(month=m, day=d)
            except:
                d_time = None

            return d_time, words.split(' ')

        _current_month_r = get_text_date(text, n)
        if _current_month_r:
            return _current_month_r, words.split(' ')

        _next_month_r = get_text_date(text,
                                      datetime.utcnow() + timedelta(days=10))
        if _next_month_r:
            return _next_month_r, words.split(' ')

        text = text.encode('utf-8')
        for k in when_nearest_tuple:
            for w in k[0]:
                if text.find(w) > -1:
                    return n + timedelta(days=k[1]), words.split(' ')

        for k, ws in when_week.iteritems():
            for w in ws:
                if text.find(w) > -1:
                    week_day = n.isoweekday()
                    if week_day > k:
                        return (
                            n + timedelta(days=(7 - week_day + 1 + k)),
                            words.split(' ')
                        )
                    else:
                        return (
                            n + timedelta(days=(k - week_day + 1)),
                            words.split(' ')
                        )
        return n, words.split(' ')
