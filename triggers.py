
class BaseTrigger:
    @classmethod
    def use(cls, xxx):
        for _func in cls.registry:
            _func(xxx)

    @classmethod
    def register(cls, user_class):
        if hasattr(user_class, 'action'):
            cls.registry.append(getattr(user_class, "action"))


class ErrorTrigger(BaseTrigger):
    registry = []


class LogTrigger(BaseTrigger):
    registry = []
