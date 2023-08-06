from typing import List, Optional
from os.path import join

from rastervision2.pipeline.pipeline import Pipeline
from rastervision2.pipeline.file_system import str_to_file, file_to_str
from rastervision2.pipeline.pipeline_config import PipelineConfig
from rastervision2.pipeline.config import register_config, Config
from rastervision2.pipeline.utils import split_into_groups


@register_config('message_maker')
class MessageMakerConfig(Config):
    greeting: str = 'hello'

    def build(self):
        return MessageMaker(self)


class MessageMaker():
    def __init__(self, config):
        self.config = config

    def make_message(self, name):
        # Use the greeting field to make the message.
        return '{} {}!'.format(self.config.greeting, name)


@register_config('sample_pipeline2')
class SamplePipeline2Config(PipelineConfig):
    names: List[str] = ['alice', 'bob']
    message_uris: Optional[List[str]] = None
    # Fields can have other Configs as types.
    message_maker: MessageMakerConfig = MessageMakerConfig()

    def build(self, tmp_dir):
        return SamplePipeline2(self, tmp_dir)

    def update(self):
        if self.message_uris is None:
            self.message_uris = [
                join(self.root_uri, '{}.txt'.format(name))
                for name in self.names
            ]


class SamplePipeline2(Pipeline):
    commands: List[str] = ['save_messages', 'print_messages']
    split_commands = ['save_messages']
    gpu_commands = []

    def save_messages(self, split_ind=0, num_splits=1):
        message_maker = self.config.message_maker.build()

        split_groups = split_into_groups(
            list(zip(self.config.names, self.config.message_uris)), num_splits)
        split_group = split_groups[split_ind]

        for name, message_uri in split_group:
            # Unlike before, we use the message_maker to make the message.
            message = message_maker.make_message(name)
            str_to_file(message, message_uri)
            print('Saved message to {}'.format(message_uri))

    def print_messages(self):
        for message_uri in self.config.message_uris:
            message = file_to_str(message_uri)
            print(message)
