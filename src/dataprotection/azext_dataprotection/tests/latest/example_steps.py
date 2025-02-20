# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------


from .. import try_manual


# EXAMPLE: /BackupPolicies/put/CreateOrUpdate BackupPolicy
@try_manual
def step_backup_policy_create(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-policy create '
             '--name "{myBackupPolicy}" '
             '--properties "{{\\"datasourceTypes\\":[\\"OssDB\\"],\\"objectType\\":\\"BackupPolicy\\",\\"policyRules\\"'
             ':[{{\\"name\\":\\"BackupWeekly\\",\\"backupParameters\\":{{\\"backupType\\":\\"Full\\",\\"objectType\\":'
             '\\"AzureBackupParams\\"}},\\"dataStore\\":{{\\"dataStoreType\\":\\"VaultStore\\",\\"objectType\\":\\"Data'
             'StoreInfoBase\\"}},\\"objectType\\":\\"AzureBackupRule\\",\\"trigger\\":{{\\"objectType\\":\\"ScheduleBas'
             'edTriggerContext\\",\\"schedule\\":{{\\"repeatingTimeIntervals\\":[\\"R/2019-11-20T08:00:00-08:00/P1W\\"]'
             '}},\\"taggingCriteria\\":[{{\\"isDefault\\":true,\\"tagInfo\\":{{\\"tagName\\":\\"Default\\"}},\\"tagging'
             'Priority\\":99}},{{\\"criteria\\":[{{\\"daysOfTheWeek\\":[\\"Sunday\\"],\\"objectType\\":\\"ScheduleBased'
             'BackupCriteria\\",\\"scheduleTimes\\":[\\"2019-03-01T13:00:00Z\\"]}}],\\"isDefault\\":false,\\"tagInfo\\"'
             ':{{\\"tagName\\":\\"Weekly\\"}},\\"taggingPriority\\":20}}]}}}},{{\\"name\\":\\"Default\\",\\"isDefault\\'
             '":true,\\"lifecycles\\":[{{\\"deleteAfter\\":{{\\"duration\\":\\"P1W\\",\\"objectType\\":\\"AbsoluteDelet'
             'eOption\\"}},\\"sourceDataStore\\":{{\\"dataStoreType\\":\\"VaultStore\\",\\"objectType\\":\\"DataStoreIn'
             'foBase\\"}}}}],\\"objectType\\":\\"AzureRetentionRule\\"}},{{\\"name\\":\\"Weekly\\",\\"isDefault\\":fals'
             'e,\\"lifecycles\\":[{{\\"deleteAfter\\":{{\\"duration\\":\\"P12W\\",\\"objectType\\":\\"AbsoluteDeleteOpt'
             'ion\\"}},\\"sourceDataStore\\":{{\\"dataStoreType\\":\\"VaultStore\\",\\"objectType\\":\\"DataStoreInfoBa'
             'se\\"}}}}],\\"objectType\\":\\"AzureRetentionRule\\"}}]}}" '
             '--resource-group "{rg_2}" '
             '--vault-name "PrivatePreviewVault"',
             checks=checks)


# EXAMPLE: /BackupPolicies/get/Get BackupPolicy
@try_manual
def step_backup_policy_show(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-policy show '
             '--name "{myBackupPolicy}" '
             '--resource-group "{rg_2}" '
             '--vault-name "PrivatePreviewVault"',
             checks=checks)


# EXAMPLE: /BackupPolicies/get/List BackupPolicy
@try_manual
def step_backup_policy_list(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-policy list '
             '--resource-group "{rg_2}" '
             '--vault-name "PrivatePreviewVault"',
             checks=checks)


# EXAMPLE: /BackupInstances/put/Create BackupInstance
@try_manual
def step_backup_instance_create(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance create '
             '--name "{myBackupInstance}" '
             '--data-source-info datasource-type="Microsoft.DBforPostgreSQL/servers/databases" '
             'object-type="Datasource" resource-id="/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Mi'
             'crosoft.DBforPostgreSQL/servers/{rg_3}/databases/testdb" resource-location="" resource-name="testdb" '
             'resource-type="Microsoft.DBforPostgreSQL/servers/databases" resource-uri="" '
             '--data-source-set-info datasource-type="Microsoft.DBforPostgreSQL/servers/databases" '
             'object-type="DatasourceSet" resource-id="/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers'
             '/Microsoft.DBforPostgreSQL/servers/{rg_3}" resource-location="" resource-name="{rg_3}" '
             'resource-type="Microsoft.DBforPostgreSQL/servers" resource-uri="" '
             '--policy-parameters objectType="SecretStoreBasedAuthCredentials" secretStoreResource={{"secretStoreType":'
             '"AzureKeyVault","uri":"https://samplevault.vault.azure.net/secrets/credentials"}} '
             '--friendly-name "harshitbi2" '
             '--object-type "BackupInstance" '
             '--policy-id "/subscriptions/{subscription_id}/resourceGroups/{rg_2}/providers/Microsoft.DataProtection/Ba'
             'ckupvaults/{myBackupVault}/backupPolicies/{myBackupPolicy2}" '
             '--policy-parameters data-store-parameters-list={{"dataStoreType":"OperationalStore","objectType":"AzureOp'
             'erationalStoreParameters","resourceGroupId":"/subscriptions/f75d8d8b-6735-4697-82e1-1a7a3ff0d5d4/resource'
             'Groups/viveksipgtest"}} '
             '--validation-type "ShallowValidation" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=[])
    test.cmd('az dataprotection backup-instance wait --created '
             '--name "{myBackupInstance}" '
             '--resource-group "{rg_2}"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/StopProtection
@try_manual
def step_backup_instance_stop_protection(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance stop-protection '
             '--name "{myBackupInstance2}" '
             '--resource-group "{rg_4}" '
             '--vault-name "testvault"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/SuspendBackups
@try_manual
def step_backup_instance_suspend_backup(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance suspend-backup '
             '--name "{myBackupInstance2}" '
             '--resource-group "{rg_4}" '
             '--vault-name "testvault"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/Trigger Adhoc Backup
@try_manual
def step_backup_instance_adhoc_backup(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance adhoc-backup '
             '--name "{myBackupInstance}" '
             '--rule-name "BackupWeekly" '
             '--retention-tag-override "yearly" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/Trigger Restore
@try_manual
def step_backup_instance_restore_trigger(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance restore trigger '
             '--name "{myBackupInstance}" '
             '--restore-request-object "{{\\"objectType\\":\\"AzureBackupRecoveryPointBasedRestoreRequest\\",\\"recover'
             'yPointId\\":\\"hardcodedRP\\",\\"restoreTargetInfo\\":{{\\"datasourceAuthCredentials\\":{{\\"objectType\\'
             '":\\"SecretStoreBasedAuthCredentials\\",\\"secretStoreResource\\":{{\\"secretStoreType\\":\\"AzureKeyVaul'
             't\\",\\"uri\\":\\"https://samplevault.vault.azure.net/secrets/credentials\\"}}}},\\"datasourceInfo\\":{{'
             '\\"datasourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"objectType\\":\\"Datasource\\",'
             '\\"resourceID\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostg'
             'reSQL/servers/{rg_3}/databases/targetdb\\",\\"resourceLocation\\":\\"\\",\\"resourceName\\":\\"targetdb\\'
             '",\\"resourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"resourceUri\\":\\"\\"}},\\"data'
             'sourceSetInfo\\":{{\\"datasourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"objectType\\'
             '":\\"DatasourceSet\\",\\"resourceID\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/provider'
             's/Microsoft.DBforPostgreSQL/servers/{rg_3}\\",\\"resourceLocation\\":\\"\\",\\"resourceName\\":\\"{rg_3}'
             '\\",\\"resourceType\\":\\"Microsoft.DBforPostgreSQL/servers\\",\\"resourceUri\\":\\"\\"}},\\"objectType\\'
             '":\\"RestoreTargetInfo\\",\\"recoveryOption\\":\\"FailIfExists\\",\\"restoreLocation\\":\\"southeastasia'
             '\\"}},\\"sourceDataStoreType\\":\\"VaultStore\\",\\"sourceResourceId\\":\\"/subscriptions/{subscription_i'
             'd}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostgreSQL/servers/{rg_3}/databases/testdb\\"}}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/Trigger Restore As Files
@try_manual
def step_backup_instance_restore_trigger2(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance restore trigger '
             '--name "{myBackupInstance}" '
             '--restore-request-object "{{\\"objectType\\":\\"AzureBackupRecoveryPointBasedRestoreRequest\\",\\"recover'
             'yPointId\\":\\"hardcodedRP\\",\\"restoreTargetInfo\\":{{\\"objectType\\":\\"RestoreFilesTargetInfo\\",\\"'
             'recoveryOption\\":\\"FailIfExists\\",\\"restoreLocation\\":\\"southeastasia\\",\\"targetDetails\\":{{\\"f'
             'ilePrefix\\":\\"restoredblob\\",\\"restoreTargetLocationType\\":\\"AzureBlobs\\",\\"url\\":\\"https://tes'
             'tstorage.blob.core.windows.net/restoretest\\"}}}},\\"sourceDataStoreType\\":\\"VaultStore\\",\\"sourceRes'
             'ourceId\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostgreSQL/'
             'servers/{rg_3}/databases/testdb\\"}}" '
             '--resource-group "{rg_2}" '
             '--vault-name "PrivatePreviewVault1"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/Trigger Restore With Rehydration
@try_manual
def step_backup_instance_restore_trigger3(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance restore trigger '
             '--name "{myBackupInstance}" '
             '--restore-request-object "{{\\"objectType\\":\\"AzureBackupRestoreWithRehydrationRequest\\",\\"recoveryPo'
             'intId\\":\\"hardcodedRP\\",\\"rehydrationPriority\\":\\"High\\",\\"rehydrationRetentionDuration\\":\\"7D'
             '\\",\\"restoreTargetInfo\\":{{\\"datasourceInfo\\":{{\\"datasourceType\\":\\"OssDB\\",\\"objectType\\":\\'
             '"Datasource\\",\\"resourceID\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Micro'
             'soft.DBforPostgreSQL/servers/{rg_3}/databases/testdb\\",\\"resourceLocation\\":\\"\\",\\"resourceName\\":'
             '\\"testdb\\",\\"resourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"resourceUri\\":\\"\\'
             '"}},\\"datasourceSetInfo\\":{{\\"datasourceType\\":\\"OssDB\\",\\"objectType\\":\\"DatasourceSet\\",\\"re'
             'sourceID\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostgreSQL'
             '/servers/{rg_3}\\",\\"resourceLocation\\":\\"\\",\\"resourceName\\":\\"{rg_3}\\",\\"resourceType\\":\\"Mi'
             'crosoft.DBforPostgreSQL/servers\\",\\"resourceUri\\":\\"\\"}},\\"objectType\\":\\"RestoreTargetInfo\\",\\'
             '"recoveryOption\\":\\"FailIfExists\\",\\"restoreLocation\\":\\"southeastasia\\"}},\\"sourceDataStoreType'
             '\\":\\"VaultStore\\",\\"sourceResourceId\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/pro'
             'viders/Microsoft.DBforPostgreSQL/servers/{rg_3}/databases/testdb\\"}}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/Validate For Backup
@try_manual
def step_backup_instance_validate_for_backup(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance validate-for-backup '
             '--data-source-info datasource-type="OssDB" object-type="Datasource" resource-id="/subscriptions/{subscrip'
             'tion_id}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostgreSQL/servers/{rg_3}/databases/testdb" '
             'resource-location="" resource-name="testdb" resource-type="Microsoft.DBforPostgreSQL/servers/databases" '
             'resource-uri="" '
             '--data-source-set-info datasource-type="OssDB" object-type="DatasourceSet" '
             'resource-id="/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostgreSQL/s'
             'ervers/{rg_3}" resource-location="" resource-name="{rg_3}" resource-type="Microsoft.DBforPostgreSQL/serve'
             'rs" resource-uri="" '
             '--policy-parameters objectType="SecretStoreBasedAuthCredentials" secretStoreResource={{"secretStoreType":'
             '"AzureKeyVault","uri":"https://samplevault.vault.azure.net/secrets/credentials"}} '
             '--friendly-name "harshitbi2" '
             '--object-type "BackupInstance" '
             '--policy-id "/subscriptions/{subscription_id}/resourceGroups/{rg_2}/providers/Microsoft.DataProtection/Ba'
             'ckupvaults/{myBackupVault}/backupPolicies/{myBackupPolicy2}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/Validate Restore
@try_manual
def step_backup_instance_validate_for_restore(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance validate-for-restore '
             '--name "{myBackupInstance}" '
             '--restore-request-object "{{\\"objectType\\":\\"AzureBackupRecoveryPointBasedRestoreRequest\\",\\"recover'
             'yPointId\\":\\"hardcodedRP\\",\\"restoreTargetInfo\\":{{\\"datasourceAuthCredentials\\":{{\\"objectType\\'
             '":\\"SecretStoreBasedAuthCredentials\\",\\"secretStoreResource\\":{{\\"secretStoreType\\":\\"AzureKeyVaul'
             't\\",\\"uri\\":\\"https://samplevault.vault.azure.net/secrets/credentials\\"}}}},\\"datasourceInfo\\":{{'
             '\\"datasourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"objectType\\":\\"Datasource\\",'
             '\\"resourceID\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostg'
             'reSQL/servers/{rg_3}/databases/targetdb\\",\\"resourceLocation\\":\\"\\",\\"resourceName\\":\\"targetdb\\'
             '",\\"resourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"resourceUri\\":\\"\\"}},\\"data'
             'sourceSetInfo\\":{{\\"datasourceType\\":\\"Microsoft.DBforPostgreSQL/servers/databases\\",\\"objectType\\'
             '":\\"DatasourceSet\\",\\"resourceID\\":\\"/subscriptions/{subscription_id}/resourceGroups/{rg_3}/provider'
             's/Microsoft.DBforPostgreSQL/servers/{rg_3}\\",\\"resourceLocation\\":\\"\\",\\"resourceName\\":\\"{rg_3}'
             '\\",\\"resourceType\\":\\"Microsoft.DBforPostgreSQL/servers\\",\\"resourceUri\\":\\"\\"}},\\"objectType\\'
             '":\\"RestoreTargetInfo\\",\\"recoveryOption\\":\\"FailIfExists\\",\\"restoreLocation\\":\\"southeastasia'
             '\\"}},\\"sourceDataStoreType\\":\\"VaultStore\\",\\"sourceResourceId\\":\\"/subscriptions/{subscription_i'
             'd}/resourceGroups/{rg_3}/providers/Microsoft.DBforPostgreSQL/servers/{rg_3}/databases/testdb\\"}}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupPolicies/delete/Delete BackupPolicy
@try_manual
def step_backup_policy_delete(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-policy delete -y '
             '--name "{myBackupPolicy}" '
             '--resource-group "{rg_2}" '
             '--vault-name "PrivatePreviewVault"',
             checks=checks)


# EXAMPLE: /BackupVaults/put/Create BackupVault
@try_manual
def step_backup_vault_create(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-vault create '
             '--type "None" '
             '--location "WestUS" '
             '--storage-settings type="LocallyRedundant" datastore-type="VaultStore" '
             '--tags key1="val1" '
             '--resource-group "{rg}" '
             '--vault-name "swaggerExample"',
             checks=checks)


# EXAMPLE: /BackupVaults/put/Create BackupVault With MSI
@try_manual
def step_backup_vault_create2(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-vault create '
             '--type "systemAssigned" '
             '--location "WestUS" '
             '--storage-settings type="LocallyRedundant" datastore-type="VaultStore" '
             '--tags key1="val1" '
             '--resource-group "{rg}" '
             '--vault-name "swaggerExample"',
             checks=checks)


# EXAMPLE: /BackupVaults/get/Get BackupVault
@try_manual
def step_backup_vault_show(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-vault show '
             '--resource-group "{rg}" '
             '--vault-name "swaggerExample"',
             checks=checks)


# EXAMPLE: /BackupVaults/get/Get BackupVault With MSI
@try_manual
def step_backup_vault_show2(test, checks=None):
    return step_backup_vault_show(test, checks)


# EXAMPLE: /BackupVaults/patch/Patch BackupVault
@try_manual
def step_backup_vault_update(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-vault update '
             '--tags newKey="newVal" '
             '--resource-group "{rg}" '
             '--vault-name "swaggerExample"',
             checks=checks)


# EXAMPLE: /BackupInstances/get/Get BackupInstance
@try_manual
def step_backup_instance_show(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance show '
             '--name "{myBackupInstance}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupInstances/get/List BackupInstances in a Vault
@try_manual
def step_backup_instance_list(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance list '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupInstances/post/ResumeProtection
@try_manual
def step_backup_instance_resume_protection(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance resume-protection '
             '--name "{myBackupInstance2}" '
             '--resource-group "{rg_4}" '
             '--vault-name "testvault"',
             checks=checks)


# EXAMPLE: /BackupInstances/delete/Delete BackupInstance
@try_manual
def step_backup_instance_delete(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-instance delete -y '
             '--name "{myBackupInstance}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /BackupVaults/delete/Delete BackupVault
@try_manual
def step_backup_vault_delete(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection backup-vault delete -y '
             '--resource-group "{rg}" '
             '--vault-name "swaggerExample"',
             checks=checks)


# EXAMPLE: /Jobs/get/Get Job
@try_manual
def step_job_show(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection job show '
             '--job-id "3c60cb49-63e8-4b21-b9bd-26277b3fdfae" '
             '--resource-group "{rg_5}" '
             '--vault-name "BugBashVaultForCCYv11"',
             checks=checks)


# EXAMPLE: /Jobs/get/Get Jobs
@try_manual
def step_job_list(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection job list '
             '--resource-group "{rg_5}" '
             '--vault-name "BugBashVaultForCCYv11"',
             checks=checks)


# EXAMPLE: /RecoveryPoints/get/Get Recovery Point
@try_manual
def step_recovery_point_show(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection recovery-point show '
             '--backup-instance-name "{myBackupInstance}" '
             '--recovery-point-id "7fb2cddd-c5b3-44f6-a0d9-db3c4f9d5f25" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /RecoveryPoints/get/List Recovery Points in a Vault
@try_manual
def step_recovery_point_list(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection recovery-point list '
             '--backup-instance-name "{myBackupInstance}" '
             '--resource-group "{rg_2}" '
             '--vault-name "{myBackupVault}"',
             checks=checks)


# EXAMPLE: /RestorableTimeRanges/post/Find Restorable Time Ranges
@try_manual
def step_restorable_time_range_find(test, checks=None):
    if checks is None:
        checks = []
    test.cmd('az dataprotection restorable-time-range find '
             '--backup-instance-name "{myBackupInstance3}" '
             '--end-time "2021-02-24T00:35:17.6829685Z" '
             '--source-data-store-type "OperationalStore" '
             '--start-time "2020-10-17T23:28:17.6829685Z" '
             '--resource-group "{rg_6}" '
             '--vault-name "ZBlobBackupVaultBVTD3"',
             checks=checks)
