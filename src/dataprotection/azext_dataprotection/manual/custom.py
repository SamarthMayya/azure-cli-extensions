# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
# pylint: disable=line-too-long
# pylint: disable=too-many-branches
import uuid
import copy
import re
from knack.util import CLIError
from knack.log import get_logger
from azure.cli.core.util import sdk_no_wait
from azext_dataprotection.vendored_sdks.resourcegraph.models import \
    QueryRequest, QueryRequestOptions
from azext_dataprotection.manual import backupcenter_helper, helpers as helper

logger = get_logger(__name__)


def dataprotection_backup_vault_list(client, resource_group_name=None):
    if resource_group_name is not None:
        return client.get_in_resource_group(resource_group_name=resource_group_name)
    return client.get_in_subscription()


def dataprotection_backup_vault_create(client,
                                       resource_group_name,
                                       vault_name,
                                       storage_settings,
                                       e_tag=None,
                                       location=None,
                                       tags=None,
                                       type_=None,
                                       alerts_for_all_job_failures=None,
                                       no_wait=False):
    parameters = {}
    parameters['e_tag'] = e_tag
    parameters['location'] = location
    parameters['tags'] = tags
    if type_ is not None:
        parameters['identity'] = {}
        parameters['identity']['type'] = type_
    parameters['properties'] = {}
    parameters['properties']['storage_settings'] = storage_settings
    if alerts_for_all_job_failures is not None:
        parameters['properties']['monitoring_settings'] = {}
        parameters['properties']['monitoring_settings']['azure_monitor_alert_settings'] = {}
        parameters['properties']['monitoring_settings']['azure_monitor_alert_settings']['alerts_for_all_job_failures'] = alerts_for_all_job_failures
    return sdk_no_wait(no_wait,
                       client.begin_create_or_update,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       parameters=parameters)


def dataprotection_backup_vault_update(client,
                                       resource_group_name,
                                       vault_name,
                                       tags=None,
                                       alerts_for_all_job_failures=None,
                                       type_=None,
                                       no_wait=False):
    parameters = {}
    parameters['tags'] = tags
    if alerts_for_all_job_failures is not None:
        parameters['properties'] = {}
        parameters['properties']['monitoring_settings'] = {}
        parameters['properties']['monitoring_settings']['azure_monitor_alert_settings'] = {}
        parameters['properties']['monitoring_settings']['azure_monitor_alert_settings']['alerts_for_all_job_failures'] = alerts_for_all_job_failures
    if type_ is not None:
        parameters['identity'] = {}
        parameters['identity']['type'] = type_
    return sdk_no_wait(no_wait,
                       client.begin_update,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       parameters=parameters)


def dataprotection_resource_guard_list(client, resource_group_name=None):
    if resource_group_name is not None:
        return client.get_resources_in_resource_group(resource_group_name=resource_group_name)
    return client.get_resources_in_subscription()


def resource_guard_list_protected_operations(client, resource_group_name, resource_guards_name, resource_type):
    resource_guard_object = client.get(resource_group_name, resource_guards_name)
    protected_operations = resource_guard_object.properties.resource_guard_operations
    resource_type_protected_operation = []
    for protected_operation in protected_operations:
        if resource_type in protected_operation.vault_critical_operation:
            resource_type_protected_operation.append(protected_operation)
    return resource_type_protected_operation


def dataprotection_resource_guard_create(client,
                                         resource_group_name,
                                         resource_guards_name,
                                         e_tag=None,
                                         location=None,
                                         tags=None,
                                         type_=None):
    parameters = {}
    parameters['e_tag'] = e_tag
    parameters['location'] = location
    parameters['tags'] = tags
    if type_ is not None:
        parameters['identity'] = {}
        parameters['identity']['type'] = type_
    parameters['properties'] = {}
    return client.put(resource_group_name=resource_group_name,
                      resource_guards_name=resource_guards_name,
                      parameters=parameters)


def dataprotection_resource_guard_update(client,
                                         resource_group_name,
                                         resource_guards_name,
                                         tags=None,
                                         type_=None,
                                         resource_type=None,
                                         critical_operation_exclusion_list=None):
    resource_guard_object = client.get(resource_group_name, resource_guards_name)
    parameters = {}
    parameters['e_tag'] = resource_guard_object.e_tag
    parameters['location'] = resource_guard_object.location
    parameters['tags'] = tags
    if type_ is not None:
        parameters['identity'] = {}
        parameters['identity']['type'] = type_
    if resource_type is not None and critical_operation_exclusion_list is not None:
        critical_operation_list = []
        for critical_operation in critical_operation_exclusion_list:
            critical_operation_list.append(resource_type + helper.critical_operation_map[critical_operation])
        parameters['properties'] = {}
        parameters['properties']['vault_critical_operation_exclusion_list'] = critical_operation_list
    return client.put(resource_group_name=resource_group_name,
                      resource_guards_name=resource_guards_name,
                      parameters=parameters)


def dataprotection_backup_instance_create(client, vault_name, resource_group_name, backup_instance, no_wait=False):
    backup_instance_name = backup_instance["backup_instance_name"]
    validate_backup_instance = copy.deepcopy(backup_instance)
    backup_instance["backup_instance_name"] = None

    validate_for_backup_request = {}
    validate_for_backup_request['backup_instance'] = validate_backup_instance['properties']

    sdk_no_wait(no_wait, client.begin_validate_for_backup, vault_name=vault_name,
                resource_group_name=resource_group_name, parameters=validate_for_backup_request).result()
    return sdk_no_wait(no_wait,
                       client.begin_create_or_update,
                       vault_name=vault_name,
                       resource_group_name=resource_group_name,
                       backup_instance_name=backup_instance_name,
                       parameters=backup_instance)


def dataprotection_backup_instance_validate_for_backup(client, vault_name, resource_group_name, backup_instance,
                                                       no_wait=False):
    validate_for_backup_request = {}
    validate_for_backup_request['backup_instance'] = backup_instance['properties']
    return sdk_no_wait(no_wait, client.begin_validate_for_backup, vault_name=vault_name,
                       resource_group_name=resource_group_name, parameters=validate_for_backup_request)


def dataprotection_backup_instance_initialize(datasource_type, datasource_id, datasource_location, policy_id,
                                              secret_store_type=None, secret_store_uri=None):
    datasource_info = helper.get_datasource_info(datasource_type, datasource_id, datasource_location)
    datasourceset_info = None
    manifest = helper.load_manifest(datasource_type)
    if manifest["isProxyResource"]:
        datasourceset_info = helper.get_datasourceset_info(datasource_type, datasource_id, datasource_location)

    policy_parameters = None
    # Azure Disk specific code for adding datastoreparameter list in the json
    if datasource_type == "AzureDisk":
        policy_parameters = {
            "data_store_parameters_list": [
                {
                    "object_type": "AzureOperationalStoreParameters",
                    "data_store_type": "OperationalStore",
                    "resource_group_id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
                }
            ]
        }

    datasource_auth_credentials_info = None
    if manifest["supportSecretStoreAuthentication"]:
        if secret_store_uri and secret_store_type:
            datasource_auth_credentials_info = {
                "secret_store_resource": {
                    "uri": secret_store_uri,
                    "value": None,
                    "secret_store_type": secret_store_type
                },
                "object_type": "SecretStoreBasedAuthCredentials"
            }
        elif secret_store_uri or secret_store_type:
            raise CLIError("Either secret store uri or secret store type not provided.")

    policy_info = {
        "policy_id": policy_id,
        "policy_parameters": policy_parameters
    }

    guid = uuid.uuid1()
    backup_instance_name = ""
    if manifest["isProxyResource"]:
        backup_instance_name = datasourceset_info["resource_name"] + "-" + datasource_info["resource_name"] + "-" + str(guid)
    else:
        backup_instance_name = datasource_info["resource_name"] + "-" + datasource_info["resource_name"] + "-" + str(guid)

    return {
        "backup_instance_name": backup_instance_name,
        "properties": {
            "data_source_info": datasource_info,
            "data_source_set_info": datasourceset_info,
            "policy_info": policy_info,
            "datasource_auth_credentials": datasource_auth_credentials_info,
            "object_type": "BackupInstance"
        }
    }


def dataprotection_backup_instance_update_policy(client, resource_group_name, vault_name, backup_instance_name, policy_id, no_wait=False):
    backup_instance = client.get(vault_name=vault_name,
                                 resource_group_name=resource_group_name,
                                 backup_instance_name=backup_instance_name)

    backup_instance.properties.policy_info.policy_id = policy_id
    return sdk_no_wait(no_wait,
                       client.begin_create_or_update,
                       vault_name=vault_name,
                       resource_group_name=resource_group_name,
                       backup_instance_name=backup_instance_name,
                       parameters=backup_instance)


def dataprotection_backup_instance_list_from_resourcegraph(client, datasource_type, resource_groups=None, vaults=None, subscriptions=None, protection_status=None, datasource_id=None):
    if subscriptions is None:
        subscriptions = [backupcenter_helper.get_selected_subscription()]
    query = backupcenter_helper.get_backup_instance_query(datasource_type, resource_groups, vaults, protection_status, datasource_id)
    request_options = QueryRequestOptions(
        top=1000,
        skip=0
    )
    request = QueryRequest(query=query, subscriptions=subscriptions, options=request_options)
    response = client.resources(request)
    return response.data


def dataprotection_backup_instance_update_msi_permissions(cmd, client, resource_group_name, datasource_type, vault_name, operation, permissions_scope, backup_instance=None, keyvault_id=None):
    backup_vault = client.get(resource_group_name=resource_group_name,
                              vault_name=vault_name)
    principal_id = backup_vault.identity.principal_id

    role_assignments_arr = []

    # print(type(cmd))
    # print(vars(cmd))
    # print("\n\n")
    # print(cmd.command_kwargs)
    # print("\n\n")

    if operation == 'Backup' and backup_instance is None:
        raise CLIError("--backup-instance needs to be given when --operation is given as Backup")

    from azure.cli.command_modules.role.custom import list_role_assignments, create_role_assignment

    if datasource_type == 'AzureDisk':
        # Create scope variables for role assignment
        resource_scope_assignment = backup_instance['properties']['data_source_info']['resource_id']
        snapshot_rg_scope_assignment = backup_instance['properties']['policy_info']['policy_parameters']['data_store_parameters_list'][0]['resource_group_id']
        resource_scope = resource_scope_assignment
        snapshot_rg_scope = snapshot_rg_scope_assignment

        if permissions_scope == 'ResourceGroup':
            resource_scope_assignment = "/".join(resource_scope_assignment.split("/")[:5])  # Snapshot RG is already in RG scope, so change for resource
        elif permissions_scope == 'Subscription':
            # Change scope for both resource and Snapshot RG
            resource_scope_assignment = "/".join(resource_scope_assignment.split("/")[:3])
            snapshot_rg_scope_assignment = "/".join(snapshot_rg_scope_assignment.split("/")[:3])

        role_assignments = [role_assignment['roleDefinitionName'] for role_assignment in list_role_assignments(cmd, assignee=principal_id, scope=resource_scope, include_inherited=True)]
        if 'Disk Backup Reader' not in role_assignments:
            role_assignments_arr.append(create_role_assignment(cmd, role='Disk Backup Reader', assignee=principal_id, scope=resource_scope_assignment))

        role_assignments = [role_assignment['roleDefinitionName'] for role_assignment in list_role_assignments(cmd, assignee=principal_id, scope=snapshot_rg_scope, include_inherited=True)]
        if 'Disk Snapshot Contributor' not in role_assignments:
            role_assignments_arr.append(create_role_assignment(cmd, role='Disk Snapshot Contributor', assignee=principal_id, scope=snapshot_rg_scope_assignment))

        return role_assignments_arr

    if datasource_type == 'AzureBlob':
        storage_account_scope = backup_instance['properties']['data_source_info']['resource_id']
        storage_account_scope_assignment = storage_account_scope

        if permissions_scope == 'ResourceGroup':
            storage_account_scope_assignment = "/".join(storage_account_scope_assignment.split("/")[:5])
        elif permissions_scope == 'Subscription':
            storage_account_scope_assignment = "/".join(storage_account_scope_assignment.split("/")[:3])

        role_assignments = [role_assignment['roleDefinitionName'] for role_assignment in list_role_assignments(cmd, assignee=principal_id, scope=storage_account_scope, include_inherited=True)]
        if 'Storage Account Backup Contributor' not in role_assignments:
            role_assignments_arr.append(create_role_assignment(cmd, role='Storage Account Backup Contributor', assignee=principal_id, scope=storage_account_scope_assignment))

        return role_assignments_arr

    if datasource_type == 'AzureDatabaseForPostgreSQL':
        db_scope = backup_instance['properties']['data_source_info']['resource_id']
        server_scope_arr = db_scope.split("/")
        server_scope = "/".join(server_scope_arr[:9])
        # print(server_scope)
        # print("\n\n")
        server_name = server_scope_arr[8]
        server_scope_assign = server_scope
        server_rg = server_scope_arr[4]

        if permissions_scope == 'ResourceGroup':
            server_scope_assign = "/".join(server_scope_assign.split("/")[:5])
        elif permissions_scope == 'Subscription':
            server_scope_assign = "/".join(server_scope_assign.split("/")[:3])

        role_assignments = [role_assignment['roleDefinitionName'] for role_assignment in list_role_assignments(cmd, assignee=principal_id, scope=server_scope, include_inherited=True)]
        if 'Reader' not in role_assignments:
            role_assignments_arr.append(create_role_assignment(cmd, role='Reader', assignee=principal_id, scope=server_scope_assign))

        from azure.cli.core.profiles import get_api_version, ResourceType

        from azure.cli.command_modules.keyvault._client_factory import (
            get_client, get_client_factory, Clients, is_azure_stack_profile)

        _keyvault_scope_arr = keyvault_id.split('/')
        keyvault_name = _keyvault_scope_arr[-1]
        keyvault_rg = _keyvault_scope_arr[4]
        keyvault_subscription = _keyvault_scope_arr[2]

        cmd.command_kwargs['operation_group'] = 'vaults'

        # mgmt_vaults_entity = get_client(cmd.cli_ctx, ResourceType.MGMT_KEYVAULT, Clients.vaults)
        # keyvault_client = mgmt_vaults_entity.client_factory(cmd.cli_ctx, None)
        from azure.cli.core.commands.client_factory import get_mgmt_service_client
        keyvault_client = getattr(get_mgmt_service_client(cmd.cli_ctx, ResourceType.MGMT_KEYVAULT, subscription_id=keyvault_subscription), Clients.vaults)
        # print(keyvault_client)
        keyvault = keyvault_client.get(resource_group_name=keyvault_rg, vault_name=keyvault_name)
        # print("Keyvault before doing any changes: \n\n")
        # print(keyvault.properties.access_policies)
        # print("\n\n")
        keyvault_scope = keyvault_id
        keyvault_scope_assign = keyvault_scope
        keyvault_secret_permissions_object = {policy.object_id: policy.permissions.secrets for policy in keyvault.properties.access_policies}

        # print("Keyvault properties before set policy but after object creation: ")
        # print(keyvault.properties.access_policies)
        # print("\n\n")
        if permissions_scope == 'ResourceGroup':
            keyvault_scope_assign = "/".join(keyvault_scope_assign.split("/")[:5])
        elif permissions_scope == 'Subscription':
            keyvault_scope_assign = "/".join(keyvault_scope_assign.split("/")[:3])

        if keyvault.properties.enable_rbac_authorization:  
            role_assignments = [role_assignment['roleDefinitionName'] for role_assignment in list_role_assignments(cmd, assignee=principal_id, scope=keyvault_scope)]
            if 'Key Vault Secrets User' not in role_assignments:
                role_assignments_arr.append(create_role_assignment(cmd, role='Key Vault Secrets User', assignee=principal_id, scope=keyvault_scope_assign))
        else:
            from azure.cli.command_modules.keyvault.custom import set_policy

            secret_permissions_arr = ['Get', 'List']
            if principal_id in keyvault_secret_permissions_object:
                secret_permissions_arr = keyvault_secret_permissions_object[principal_id]
                # print("Parameters of secret arr: ")
                # print(type(secret_permissions_arr))
                # print(secret_permissions_arr)
                # print("\n\n")
                for permission in ['Get', 'List']:
                    if permission not in  secret_permissions_arr:
                        secret_permissions_arr.append(permission)

            print("Keyvault permissions before set policy: \n\n")
            print(keyvault.properties.access_policies)
            
            keyvault = set_policy(cmd, keyvault_client, keyvault_rg, keyvault_name, object_id=principal_id, secret_permissions=secret_permissions_arr)
            # keyvault.properties.access_policies.permissions.secrets = secret_permissions_arr
            keyvault = keyvault.result()
            # print("Keyvault permissions after set policy: \n\n")
            # print(keyvault.properties.access_policies)


        # Network line of sight access on the server
        from azure.cli.command_modules.rdbms._client_factory import cf_postgres_firewall_rules
        postgres_firewall_client = cf_postgres_firewall_rules(cmd.cli_ctx, None)
        # print("RG: {}, Server: {}".format(server_rg, server_name))
        firewall_rule_list = postgres_firewall_client.list_by_server(resource_group_name=server_rg, server_name=server_name)
        
        allow_access_to_azure_ips = False
        for rule in firewall_rule_list:
            if rule.start_ip_address == rule.end_ip_address and rule.start_ip_address == '0.0.0.0':
                allow_access_to_azure_ips = True
                break

        if allow_access_to_azure_ips is False:
            firewall_rule_name = 'AllowAllWindowsAzureIps'
            parameters = {'name': firewall_rule_name, 'start_ip_address': '0.0.0.0', 'end_ip_address': '0.0.0.0'}

            role_assignments_arr.append(postgres_firewall_client.begin_create_or_update(server_rg, server_name, firewall_rule_name, parameters))



        # Network line of sight access on the keyvault
        # print(keyvault.properties.network_acls.bypass == 'None')
        
        if keyvault.properties.public_network_access == 'Disabled':
            raise CLIError("Keyvault needs to have public network access enabled.")

        from azure.cli.command_modules.keyvault.custom import _create_network_rule_set, update_vault_setter
        keyvault_copy = keyvault
        update=False
        if keyvault_copy.properties.network_acls is None:
            keyvault_copy.properties.network_acls = _create_network_rule_set(cmd, bypass='AzureServices', default_action='Allow')
            update=True
        elif keyvault_copy.properties.network_acls.bypass == 'None' or keyvault_copy.properties.network_acls.default_action == 'Deny':
            keyvault_copy.properties.network_acls.bypass = 'AzureServices'
            keyvault_copy.properties.network_acls.default_action = 'Allow'
            update=True

        if update:
            # print('Updating...')
            # print("\n\nKeyvault properties for backup vault: \n\n")
            # print(keyvault_copy.properties.access_policies)
            print(update_vault_setter(cmd, keyvault_client, keyvault_copy, resource_group_name=keyvault_rg, vault_name=keyvault_name))
        

        return role_assignments_arr



    raise CLIError("Invalid params passed")


def dataprotection_job_list_from_resourcegraph(client, datasource_type, resource_groups=None, vaults=None,
                                               subscriptions=None, start_time=None, end_time=None,
                                               status=None, operation=None, datasource_id=None):
    if subscriptions is None:
        subscriptions = [backupcenter_helper.get_selected_subscription()]

    query = backupcenter_helper.get_backup_job_query(datasource_type, resource_groups, vaults, start_time, end_time, status, operation, datasource_id)
    request_options = QueryRequestOptions(
        top=1000,
        skip=0
    )
    request = QueryRequest(query=query, subscriptions=subscriptions, options=request_options)
    response = client.resources(request)
    return response.data


def dataprotection_recovery_point_list(client, vault_name, resource_group_name, backup_instance_name,
                                       start_time=None, end_time=None):
    rp_filter = ""
    if start_time is not None:
        rp_filter += "startDate eq '" + start_time + "'"
    if end_time is not None:
        if start_time is not None:
            rp_filter += " and "
        rp_filter += "endDate eq '" + end_time + "'"
    return client.list(vault_name=vault_name,
                       resource_group_name=resource_group_name,
                       backup_instance_name=backup_instance_name,
                       filter=rp_filter)


def dataprotection_backup_policy_create(client, vault_name, resource_group_name, policy, backup_policy_name):
    parameters = {}
    parameters['properties'] = policy
    return client.create_or_update(vault_name=vault_name,
                                   resource_group_name=resource_group_name,
                                   backup_policy_name=backup_policy_name,
                                   parameters=parameters)


def dataprotection_backup_policy_get_default_policy_template(datasource_type):
    manifest = helper.load_manifest(datasource_type)
    if manifest is not None and manifest["policySettings"] is not None and manifest["policySettings"]["defaultPolicy"] is not None:
        return manifest["policySettings"]["defaultPolicy"]
    raise CLIError("Unable to get default policy template.")


def dataprotection_backup_policy_trigger_create_schedule(interval_type, interval_count, schedule_days):
    # Do validations on interval_type and interval_count
    if interval_type.lower() in ["daily", "weekly"] and interval_count != 1:
        raise CLIError("Interval Count for Daily or Weekly Backup must be 1.")

    if interval_type.lower() == "hourly" and interval_count not in [4, 6, 8, 12]:
        raise CLIError("Interval Count for Hourly Backup must be one of 4, 6, 8, 12.")

    if interval_count <= 0:
        raise CLIError("Interval count must be greater than zero.")

    repeating_time_intervals = []
    for day in schedule_days:
        backup_frequency = helper.get_backup_frequency_string(interval_type, interval_count)
        time_interval = "R/" + day + "+00:00/" + backup_frequency
        repeating_time_intervals.append(time_interval)

    return repeating_time_intervals


def dataprotection_backup_policy_create_lifecycle(source_datastore, retention_duration_type, retention_duration_count, target_datastore=None, copy_option=None):
    delete_after = {
        "objectType": "AbsoluteDeleteOption",
        "duration": "P" + str(retention_duration_count) + retention_duration_type[0]
    }

    source_data_store = {
        "objectType": "DataStoreInfoBase",
        "dataStoreType": source_datastore
    }

    copy_settings = None
    if target_datastore is not None and copy_option is not None:
        copy_settings = {
            "dataStore": {
                "objectType": "DataStoreInfoBase",
                "dataStoreType": target_datastore
            },
            "copyAfter": {
                "objectType": copy_option
            }
        }

    return {
        "deleteAfter": delete_after,
        "sourceDataStore": source_data_store,
        "targetDataStoreCopySettings": copy_settings
    }


def dataprotection_backup_policy_retention_set_in_policy(policy, name, lifecycles):
    retention_policy_index = -1
    for index in range(0, len(policy["policyRules"])):
        if policy["policyRules"][index]["objectType"] == "AzureRetentionRule" and policy["policyRules"][index]["name"] == name:
            retention_policy_index = index
            break

    if retention_policy_index == -1:
        datasource_type = helper.get_client_datasource_type(policy["datasourceTypes"][0])
        manifest = helper.load_manifest(datasource_type)
        if manifest["policySettings"]["disableAddRetentionRule"]:
            raise CLIError("Adding New Retention Rule is not supported for " + datasource_type + " datasource type")

        if name not in manifest["policySettings"]["supportedRetentionTags"]:
            raise CLIError("Selected Retention Rule " + name + " is not applicable for Datasource Type " + datasource_type)

        new_retention_rule = {
            "objectType": "AzureRetentionRule",
            "isDefault": name == "Default",
            "name": name,
            "lifecycles": lifecycles
        }

        policy["policyRules"].append(new_retention_rule)
        return policy

    policy["policyRules"][retention_policy_index]["lifecycles"] = lifecycles
    return policy


def dataprotection_backup_policy_retention_remove_in_policy(name, policy):
    if name == "Default":
        raise CLIError("Removing Default Retention Rule is not allowed. Please try again with different rule name.")

    for index in range(0, len(policy["policyRules"])):
        if policy["policyRules"][index]["objectType"] == "AzureRetentionRule" and policy["policyRules"][index]["name"] == name:
            policy["policyRules"].pop(index)
            break

    return policy


def dataprotection_backup_policy_trigger_set_in_policy(policy, schedule):
    datasource_type = helper.get_client_datasource_type(policy["datasourceTypes"][0])
    helper.validate_backup_schedule(datasource_type, schedule)

    backup_rule_index = -1
    for index in range(0, len(policy["policyRules"])):
        if policy["policyRules"][index]["objectType"] == "AzureBackupRule":
            backup_rule_index = index
            break

    if index != -1:
        policy["policyRules"][backup_rule_index]["trigger"]["schedule"]["repeatingTimeIntervals"] = schedule
        policy["policyRules"][backup_rule_index]["name"] = helper.get_backup_frequency_from_time_interval(schedule)

    return policy


def dataprotection_backup_policy_create_absolute_criteria(absolute_criteria):
    return {
        "objectType": "ScheduleBasedBackupCriteria",
        "absoluteCriteria": [absolute_criteria]
    }


def dataprotection_backup_policy_create_generic_criteria(days_of_week=None, weeks_of_month=None, months_of_year=None, days_of_month=None):
    days_of_month_criteria = None
    if days_of_month is not None:
        days_of_month_criteria = []
        for day_of_month in days_of_month:
            if day_of_month.isdigit():
                day_of_month = int(day_of_month)
                if day_of_month > 28:
                    raise CLIError("Day of month should be between 1 and 28.")
                days_of_month_criteria.append({
                    "date": day_of_month,
                    "is_last": False
                })
            else:
                if day_of_month.lower() != "last":
                    raise CLIError("Day of month should either be between 1 and 28 or it should be last")
                days_of_month_criteria.append({"is_last": True})

    return {
        "object_type": "ScheduleBasedBackupCriteria",
        "days_of_month": days_of_month_criteria,
        "days_of_the_week": days_of_week,
        "months_of_year": months_of_year,
        "weeks_of_the_month": weeks_of_month
    }


def dataprotection_backup_policy_tag_set_in_policy(name, policy, criteria):
    datasource_type = helper.get_client_datasource_type(policy["datasourceTypes"][0])
    manifest = helper.load_manifest(datasource_type)

    if name not in manifest["policySettings"]["supportedRetentionTags"]:
        raise CLIError("Selected Retention Tag " + name + " is not applicable for Datasource Type " + datasource_type)

    if manifest["policySettings"]["disableCustomRetentionTag"]:
        for criterion in criteria:
            if "absoluteCriteria" not in criterion:
                raise CLIError("Only Absolute Criteria is supported for this policy")

    backup_rule_index = -1
    for index in range(0, len(policy["policyRules"])):
        if policy["policyRules"][index]["objectType"] == "AzureBackupRule":
            backup_rule_index = index
            break

    if backup_rule_index != -1:
        tagindex = -1
        for index in range(0, len(policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"])):
            if policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"][index]["tagInfo"]["tagName"] == name:
                tagindex = index
                break

        if tagindex != -1:
            policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"][tagindex]["Criteria"] = criteria
            return policy

        tagcriteria = {
            "criteria": criteria,
            "isDefault": False,
            "taggingPriority": helper.get_tagging_priority(name),
            "tagInfo": {
                "tagName": name
            }
        }

        policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"].append(tagcriteria)
        return policy

    return policy


def dataprotection_backup_policy_tag_remove_in_policy(name, policy):
    backup_rule_index = -1
    for index in range(0, len(policy["policyRules"])):
        if policy["policyRules"][index]["objectType"] == "AzureBackupRule":
            backup_rule_index = index
            break

    for index in range(0, len(policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"])):
        if policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"][index]["tagInfo"]["tagName"] == name:
            policy["policyRules"][backup_rule_index]["trigger"]["taggingCriteria"].pop(index)
            break

    return policy


def restore_initialize_for_data_recovery(target_resource_id, datasource_type, source_datastore, restore_location,
                                         recovery_point_id=None, point_in_time=None, secret_store_type=None,
                                         secret_store_uri=None, rehydration_priority=None, rehydration_duration=15):

    restore_request = {}
    restore_mode = None
    if recovery_point_id is not None and point_in_time is not None:
        raise CLIError("Please provide either recovery point id or point in time parameter, not both.")

    if recovery_point_id is not None:
        restore_request["object_type"] = "AzureBackupRecoveryPointBasedRestoreRequest"
        restore_request["recovery_point_id"] = recovery_point_id
        restore_mode = "RecoveryPointBased"

    if point_in_time is not None:
        restore_request["object_type"] = "AzureBackupRecoveryTimeBasedRestoreRequest"
        restore_request["recovery_point_time"] = point_in_time
        restore_mode = "PointInTimeBased"

    if recovery_point_id is None and point_in_time is None:
        raise CLIError("Please provide either recovery point id or point in time parameter.")

    manifest = helper.load_manifest(datasource_type)
    if manifest is not None and manifest["allowedRestoreModes"] is not None and restore_mode not in manifest["allowedRestoreModes"]:
        raise CLIError(restore_mode + " restore mode is not supported for datasource type " + datasource_type +
                       ". Supported restore modes are " + ','.join(manifest["allowedRestoreModes"]))

    if source_datastore in manifest["policySettings"]["supportedDatastoreTypes"]:
        restore_request["source_data_store_type"] = source_datastore
        if rehydration_priority:
            if rehydration_duration < 10 or rehydration_duration > 30:
                raise CLIError("The allowed range of rehydration duration is 10 to 30 days.")
            restore_request["object_type"] = "AzureBackupRestoreWithRehydrationRequest"
            restore_request["rehydration_priority"] = rehydration_priority
            restore_request["rehydration_retention_duration"] = "P" + str(rehydration_duration) + "D"
    else:
        raise CLIError(source_datastore + " datastore type is not supported for datasource type " + datasource_type +
                       ". Supported datastore types are " + ','.join(manifest["policySettings"]["supportedDatastoreTypes"]))

    restore_request["restore_target_info"] = {}
    restore_request["restore_target_info"]["object_type"] = "RestoreTargetInfo"
    restore_request["restore_target_info"]["restore_location"] = restore_location
    restore_request["restore_target_info"]["recovery_option"] = "FailIfExists"
    restore_request["restore_target_info"]["datasource_info"] = helper.get_datasource_info(datasource_type, target_resource_id, restore_location)

    if manifest["isProxyResource"]:
        restore_request["restore_target_info"]["datasource_set_info"] = helper.get_datasourceset_info(datasource_type, target_resource_id, restore_location)

    if manifest["supportSecretStoreAuthentication"]:
        if secret_store_uri and secret_store_type:
            restore_request["restore_target_info"]["datasource_auth_credentials"] = {
                "secret_store_resource": {
                    "uri": secret_store_uri,
                    "value": None,
                    "secret_store_type": secret_store_type
                },
                "object_type": "SecretStoreBasedAuthCredentials"
            }
        elif secret_store_uri or secret_store_type:
            raise CLIError("Either secret store uri or secret store type not provided.")

    return restore_request


def restore_initialize_for_data_recovery_as_files(target_blob_container_url, target_file_name, datasource_type, source_datastore,
                                                  restore_location, recovery_point_id=None, point_in_time=None,
                                                  rehydration_priority=None, rehydration_duration=15):

    restore_request = {}
    restore_mode = None
    if recovery_point_id is not None and point_in_time is not None:
        raise CLIError("Please provide either recovery point id or point in time parameter, not both.")

    if recovery_point_id is not None:
        restore_request["object_type"] = "AzureBackupRecoveryPointBasedRestoreRequest"
        restore_request["recovery_point_id"] = recovery_point_id
        restore_mode = "RecoveryPointBased"

    if point_in_time is not None:
        restore_request["object_type"] = "AzureBackupRecoveryTimeBasedRestoreRequest"
        restore_request["recovery_point_time"] = point_in_time
        restore_mode = "PointInTimeBased"

    if recovery_point_id is None and point_in_time is None:
        raise CLIError("Please provide either recovery point id or point in time parameter.")

    manifest = helper.load_manifest(datasource_type)
    if manifest is not None and manifest["allowedRestoreModes"] is not None and restore_mode not in manifest["allowedRestoreModes"]:
        raise CLIError(restore_mode + " restore mode is not supported for datasource type " + datasource_type +
                       ". Supported restore modes are " + ','.join(manifest["allowedRestoreModes"]))

    if source_datastore in manifest["policySettings"]["supportedDatastoreTypes"]:
        restore_request["source_data_store_type"] = source_datastore
        if rehydration_priority:
            if rehydration_duration < 10 or rehydration_duration > 30:
                raise CLIError("The allowed range of rehydration duration is 10 to 30 days.")
            restore_request["object_type"] = "AzureBackupRestoreWithRehydrationRequest"
            restore_request["rehydration_priority"] = rehydration_priority
            restore_request["rehydration_retention_duration"] = "P" + str(rehydration_duration) + "D"
    else:
        raise CLIError(source_datastore + " datastore type is not supported for datasource type " + datasource_type +
                       ". Supported datastore types are " + ','.join(manifest["policySettings"]["supportedDatastoreTypes"]))

    restore_request["restore_target_info"] = {}
    restore_request["restore_target_info"]["object_type"] = "RestoreFilesTargetInfo"
    restore_request["restore_target_info"]["restore_location"] = restore_location
    restore_request["restore_target_info"]["recovery_option"] = "FailIfExists"
    restore_request["restore_target_info"]["target_details"] = {}
    restore_request["restore_target_info"]["target_details"]["url"] = target_blob_container_url
    restore_request["restore_target_info"]["target_details"]["file_prefix"] = target_file_name
    restore_request["restore_target_info"]["target_details"]["restore_target_location_type"] = "AzureBlobs"

    return restore_request


def restore_initialize_for_item_recovery(client, datasource_type, source_datastore, restore_location, backup_instance_id,
                                         recovery_point_id=None, point_in_time=None, container_list=None,
                                         from_prefix_pattern=None, to_prefix_pattern=None):

    restore_request = {}
    restore_mode = None
    if recovery_point_id is not None and point_in_time is not None:
        raise CLIError("Please provide either recovery point id or point in time parameter, not both.")

    if recovery_point_id is not None:
        restore_request["object_type"] = "AzureBackupRecoveryPointBasedRestoreRequest"
        restore_request["recovery_point_id"] = recovery_point_id
        restore_mode = "RecoveryPointBased"

    if point_in_time is not None:
        restore_request["object_type"] = "AzureBackupRecoveryTimeBasedRestoreRequest"
        restore_request["recovery_point_time"] = point_in_time
        restore_mode = "PointInTimeBased"

    if recovery_point_id is None and point_in_time is None:
        raise CLIError("Please provide either recovery point id or point in time parameter.")

    manifest = helper.load_manifest(datasource_type)
    if manifest is not None and manifest["allowedRestoreModes"] is not None and restore_mode not in manifest["allowedRestoreModes"]:
        raise CLIError(restore_mode + " restore mode is not supported for datasource type " + datasource_type +
                       ". Supported restore modes are " + ','.join(manifest["allowedRestoreModes"]))

    if manifest is not None and not manifest["itemLevelRecoveyEnabled"]:
        raise CLIError("Specified DatasourceType " + datasource_type + " doesn't support Item Level Recovery")

    restore_request["source_data_store_type"] = source_datastore
    restore_request["restore_target_info"] = {}
    restore_request["restore_target_info"]["object_type"] = "ItemLevelRestoreTargetInfo"
    restore_request["restore_target_info"]["restore_location"] = restore_location
    restore_request["restore_target_info"]["recovery_option"] = "FailIfExists"

    restore_criteria_list = []
    if container_list is not None and (from_prefix_pattern is not None or to_prefix_pattern is not None):
        raise CLIError("Please specify either container list or prefix pattern.")

    if container_list is not None:
        if len(container_list) > 10:
            raise CLIError("A maximum of 10 containers can be restored. Please choose up to 10 containers.")
        for container in container_list:
            if container[0] == '$':
                raise CLIError("container name can not start with '$'. Please retry with different sets of containers.")
            restore_criteria = {}
            restore_criteria["object_type"] = "RangeBasedItemLevelRestoreCriteria"
            restore_criteria["min_matching_value"] = container
            restore_criteria["max_matching_value"] = container + "-0"

            restore_criteria_list.append(restore_criteria)

    if from_prefix_pattern is not None or to_prefix_pattern is not None:
        if from_prefix_pattern is None or to_prefix_pattern is None or \
           len(from_prefix_pattern) != len(to_prefix_pattern) or len(from_prefix_pattern) > 10:
            raise CLIError(
                "from-prefix-pattern and to-prefix-pattern should not be null, both of them should have "
                "equal length and can have a maximum of 10 patterns."
            )

        for index, _ in enumerate(from_prefix_pattern):
            if from_prefix_pattern[index][0] == '$' or to_prefix_pattern[index][0] == '$':
                raise CLIError(
                    "Prefix patterns should not start with '$'. Please provide valid prefix patterns and try again."
                )

            if not 3 <= len(from_prefix_pattern[index]) <= 63 or not 3 <= len(to_prefix_pattern[index]) <= 63:
                raise CLIError(
                    "Prefix patterns needs to be between 3 to 63 characters."
                )

            if from_prefix_pattern[index] >= to_prefix_pattern[index]:
                raise CLIError(
                    "From prefix pattern must be less than to prefix pattern."
                )

            regex_pattern = r"^[a-z0-9](?!.*--)[a-z0-9-]{1,61}[a-z0-9](\/.{1,60})*$"
            if re.match(regex_pattern, from_prefix_pattern[index]) is None:
                raise CLIError(
                    "prefix patterns must start or end with a letter or number,"
                    "and can contain only lowercase letters, numbers, and the dash (-) character. "
                    "consecutive dashes are not permitted."
                    "Given pattern " + from_prefix_pattern[index] + " violates the above rule."
                )

            if re.match(regex_pattern, to_prefix_pattern[index]) is None:
                raise CLIError(
                    "prefix patterns must start or end with a letter or number,"
                    "and can contain only lowercase letters, numbers, and the dash (-) character. "
                    "consecutive dashes are not permitted."
                    "Given pattern " + to_prefix_pattern[index] + " violates the above rule."
                )

            for compareindex in range(index + 1, len(from_prefix_pattern)):
                if (from_prefix_pattern[index] <= from_prefix_pattern[compareindex] and to_prefix_pattern[index] >= from_prefix_pattern[compareindex]) or \
                   (from_prefix_pattern[index] >= from_prefix_pattern[compareindex] and from_prefix_pattern[index] <= to_prefix_pattern[compareindex]):
                    raise CLIError(
                        "overlapping ranges are not allowed."
                    )

        for index, _ in enumerate(from_prefix_pattern):
            restore_criteria = {}
            restore_criteria["object_type"] = "RangeBasedItemLevelRestoreCriteria"
            restore_criteria["min_matching_value"] = from_prefix_pattern[index]
            restore_criteria["max_matching_value"] = to_prefix_pattern[index]

            restore_criteria_list.append(restore_criteria)

    if container_list is None and from_prefix_pattern is None and to_prefix_pattern is None:
        raise CLIError("Provide ContainersList or Prefixes for Item Level Recovery")

    restore_request["restore_target_info"]["restore_criteria"] = restore_criteria_list

    vault_resource_group = backup_instance_id.split('/')[4]
    vault_name = backup_instance_id.split('/')[8]
    backup_instance_name = backup_instance_id.split('/')[-1]

    backup_instance = client.get(vault_name=vault_name, resource_group_name=vault_resource_group, backup_instance_name=backup_instance_name)
    datasource_id = backup_instance.properties.data_source_info.resource_id

    restore_request["restore_target_info"]["datasource_info"] = helper.get_datasource_info(datasource_type, datasource_id, restore_location)

    if manifest["isProxyResource"]:
        restore_request["restore_target_info"]["datasource_set_info"] = helper.get_datasourceset_info(datasource_type, datasource_id, restore_location)

    return restore_request
