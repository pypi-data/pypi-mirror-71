# Copyright (C) 2019 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptoken', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='apptoken',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='apptoken',
            constraint=models.UniqueConstraint(
                fields=('user', 'app'),
                name='unique_app_token_and_user',
            ),
        ),
    ]
