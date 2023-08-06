from rastervision2.pipeline.config import register_config
from rastervision2.examples.sample_pipeline2.sample_pipeline2 import (
    MessageMakerConfig, MessageMaker)


# You always need to use the register_config decorator.
@register_config('deluxe_message_maker')
class DeluxeMessageMakerConfig(MessageMakerConfig):
    # Note that this inherits the greeting field from MessageMakerConfig.
    level: int = 1

    def build(self):
        return DeluxeMessageMaker(self)


class DeluxeMessageMaker(MessageMaker):
    def make_message(self, name):
        # Uses the level field to determine the number of exclamation marks.
        exclamation_marks = '!' * self.config.level
        return '{} {}{}'.format(self.config.greeting, name, exclamation_marks)
