#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, CloudBackend, NamedCloudWorkspace, TerraformVariable
from cdktf_cdktf_provider_snowflake.provider import SnowflakeProvider
from cdktf_cdktf_provider_snowflake.database import Database
from cdktf_cdktf_provider_snowflake.schema import Schema

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        snowflake_account = TerraformVariable(self, "snowflake_account", type="string")

        snowflake_username = TerraformVariable(self, "snowflake_username", type="string")

        snowflake_password = TerraformVariable(self, "snowflake_password", type="string", sensitive=True)

        SnowflakeProvider(self, 'snowflake',
                          account=snowflake_account.string_value,
                          username=snowflake_username.string_value,
                          password=snowflake_password.string_value)

        test_database = Database(self, id_="test_database", name='TEST_DATABASE')
        test_schema = Schema(self, id_='test_schema', database=test_database.name, name='TEST_SCHEMA')

app = App()
stack = MyStack(app, "cdktf-snowflake-poc")
CloudBackend(stack,
  hostname='app.terraform.io',
  organization='example-org-8f2301',
  workspaces=NamedCloudWorkspace('cdktf-snowflake-poc')
)

app.synth()
