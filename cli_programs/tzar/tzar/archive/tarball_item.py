# Copyright 2016 Steven Cooper
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from .base_item import BaseItem

class TarballItem(BaseItem):

    @classmethod
    def item_for_path_if_matching(cls, path, parsed_name, config_data, **kwargs):
        if parsed_name.extension_prefix:
            if parsed_name.extension_prefix == 'tar':
                if parsed_name.extension == 'bz2':
                    return TarballItem(path, 'bzip2', config_data, **kwargs)
                if parsed_name.extension == 'xz':
                    return TarballItem(path, 'xz', config_data, **kwargs)
                if parsed_name.extension == 'lz':
                    return TarballItem(path, 'lzip', config_data, **kwargs)
                if parsed_name.extension == 'gz':
                    return TarballItem(path, 'gzip', config_data, **kwargs)
        else:
            if parsed_name.extension == 'tgz':
                return TarballItem(path, 'gzip', config_data, **kwargs)
            if parsed_name.extension == 'tbz2':
                return TarballItem(path, 'bzip2', config_data, **kwargs)
            if parsed_name.extension == 'txz':
                return TarballItem(path, 'xz', config_data, **kwargs)
            if parsed_name.extension == 'tlz':
                return TarballItem(path, 'lzip', config_data, **kwargs)

    def __init__(self, path, compression, config_data, **kwargs):
        BaseItem.__init__(self, path, config_data, **kwargs)
        self.compression = compression
        if self.compression == 'bzip2':
            self.external_compression_program = self.config_data.REPLACEMENT_BZIP2
            self.tar_compression_options = 'j'
            self.tar_extension = '.tar.bz2'
        elif self.compression == 'xz':
            # xz has a threading
            if  'XZ_OPT' in os.environ:
                os.environ['XZ_OPT'] = '%s --threads=0' % os.environ['XZ_OPT']
            else:
                os.environ['XZ_OPT'] = '--threads=0'
            self.tar_compression_options = 'J'
            self.external_compression_program = self.config_data.REPLACEMENT_XZ
            self.tar_extension = '.tar.xz'
        elif self.compression == 'lzip':
            # does this work for lzip, like xz?
            if  'LZ_OPT' in os.environ:
                os.environ['LZ_OPT'] = '%s --threads=0' % os.environ['LZ_OPT']
            else:
                os.environ['LZ_OPT'] = '--threads=0'
            self.tar_compression_options = None
            self.external_compression_program = self.config_data.REPLACEMENT_LZIP
            self.tar_extension = '.tar.lz'
        else:
            self.tar_compression_options = 'z'
            self.external_compression_program = self.config_data.REPLACEMENT_GZIP
            self.tar_extension = '.tar.gz'
        verbose_option = 'v' if not self.is_metered() else ''
        self.tar_create_options = []
        if self.external_compression_program:
            compression_options = ''
            self.tar_create_options.extend(['--use-compress-program',
                                            self.external_compression_program])
        else:
            compression_options = self.tar_compression_options
        self.tar_create_options.append('-c%s%s' % (verbose_option, compression_options))
        self.tar_create_options.append('-f')
        self.tar_restore_options = '-%s%s%s' % ('x', self.tar_compression_options, 'pf')
        self.tar_compare_options = '-%s%s%s' % ('d', self.tar_compression_options, 'f')

    def build_create_batch(self, batch):
        output_path = ''.join([self.archive, self.tar_extension])
        if batch.is_metered():
            batch.add_command('echo', ('Creating "', output_path, '"...'))
        batch.add_command('tar')
        batch.add_exclude_args('--exclude')
        batch.add_args(*self.tar_create_options)
        if batch.is_metered():
            batch.add_metered_redirection_args(output_path, self.path)
        else:
            batch.add_args(output_path, self.path)
        batch.add_source_deletion()
        batch.add_error_deletion_path(output_path)

    def build_restore_batch(self, batch):
        restore_to_dir = disk.get_versioned_path(os.path.basename(self.path)[:-len(self.tar_extension)])
        os.mkdir(restore_to_dir)
        console.info('Restoring to "%s"...' % restore_to_dir)
        #TODO: Untested
        batch.add_command('tar', self.tar_restore_options, self.path,
                          '--strip-components', '1', '-C', restore_to_dir)

    def build_compare_batch(self, batch):
        #TODO: Untested - runs against working directory?
        batch.add_command('tar', self.tar_compare_options, self.path)
