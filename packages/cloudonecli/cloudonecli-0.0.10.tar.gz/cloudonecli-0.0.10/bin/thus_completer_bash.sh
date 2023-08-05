#/usr/bin/env bash

_cloudone_completions_ds_functions()
{
case "${COMP_WORDS[COMP_CWORD-1]}" in 
	apikeys)
		 COMPREPLY=($(compgen -W "Current create currentSecretKey delete describe generateSecret list modify modifyCurrent search " "${COMP_WORDS[3]}"))
		 return
		;;
	apiusagemetrics)
		 COMPREPLY=($(compgen -W "list search " "${COMP_WORDS[3]}"))
		 return
		;;
	administrators)
		 COMPREPLY=($(compgen -W "create createRole delete deleteRole describe describeRole list listRoles modify modifyRole search searchRole " "${COMP_WORDS[3]}"))
		 return
		;;
	agentdeploymentscripts)
		 COMPREPLY=($(compgen -W "generate " "${COMP_WORDS[3]}"))
		 return
		;;
	antimalware)
		 COMPREPLY=($(compgen -W "create createdfileExtensionlist createdfilelist createdirectorylist createdschedules delete deletedirectorylist deletefileExtensionlist deletefilelist deleteschedule describe describedirectorylist describefileExtensionlist describefilelist describeschedule list listdirectorylists listfileExtensionlists listfilelists listschedules modify modifydirectorylist modifyfileExtensionlist modifyfilelist modifyschedule search searchdirectorylist searchfileExtensionlist searchfilelist searchschedule " "${COMP_WORDS[3]}"))
		 return
		;;
	applicationcontrol)
		 COMPREPLY=($(compgen -W "createGlobalRule createSoftwareInventory createruleset deleteGlobalRule deleteSoftwareInventory deleteruleset deleterulesetRule describeGlobalRule describeRulesetRule describeSoftwareInventory describeSoftwareInventoryItem describesoftwareChange listGlobalRules listSoftwareInventories listSoftwareInventoryItems listrulesetRules listrulesets listsoftwareChanges modifyGlobalRule modifyruleset modifyrulesetRule reviewSoftwareChange searchGlobalRules searchSoftwareInventory searchSoftwareInventoryItems searchrulesetRules searchrulesets searchsoftwareChanges " "${COMP_WORDS[3]}"))
		 return
		;;
	certificates)
		 COMPREPLY=($(compgen -W "add delete describe getByURL list " "${COMP_WORDS[3]}"))
		 return
		;;
	computergroups)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	computers)
		 COMPREPLY=($(compgen -W "addFirewallAssignment assignIntrusionPreventionAssignment assignLogInspectionAssignment create createIntrusionPreventionAssignment delete deleteComputerIntrusionPreventionAssignment deleteFirewallAssignment deleteIntegrityMonitoringRules deleteIntrusionPreventionApplicationTypes deleteIntrusionPreventionRules deleteLogInspectionAssignment deleteLogInspectionRule describe describeFirewallRules describeIntegrityMonitoringRules describeIntrusionPreventionApplicationTypes describeIntrusionPreventionRule describeLogInspectionRule describeSetting list listFirewallAssignment listFirewallRules listIntegrityMonitoringRules listIntrusionPreventionApplicationTypes listIntrusionPreventionAssignment listIntrusionPreventionRules listLogInspectionAssignment listLogInspectionRules modify modifyFirewallRules modifyIntegrityMonitoringRules modifyIntrusionPreventionApplicationTypes modifyIntrusionPreventionRule modifyLogInspectionRule modifySetting resetFirewallRules resetSetting search setFirewallAssignment setLogInspectionAssignment " "${COMP_WORDS[3]}"))
		 return
		;;
	contacts)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	eventbasedtasks)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	integritymonitoring)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	intrusionprevention)
		 COMPREPLY=($(compgen -W "createRules createType deleteRule deleteType describeRule listRules listTypes modifyRule modifyType searchRules searchTypes " "${COMP_WORDS[3]}"))
		 return
		;;
	loginspectionrules)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	policies)
		 COMPREPLY=($(compgen -W "AddFirewallRuleAssignments AddIntrusionPreventionRuleAssignments AddLogInspectionRuleAssignments SetFirewallRulesAssignments SetIntrusionPreventionRulesAssignments SetLogInspectionRulesAssignments addIntegrityMonitoringRuleAssignments create delete deleteDefaultSetting deleteFirewallRuleAssignments deleteIntegrityMonitoringRules deleteIntrusionPreventionRuleAssignments deleteLogInspectionRuleAssignments describe describeDefaultSetting describeFirewallRules describeIntegrityMonitoringRules describeIntrusionPreventionApplication describeIntrusionPreventionRules describeLogInspection describePolicyDefault list listFirewallRules listFirewallRulesAssignments listIntegrityMonitoringRules listIntegrityMonitoringRulesAssignments listIntrusionPreventionApplication listIntrusionPreventionRules listIntrusionPreventionRulesAssignments listLogInspection listLogInspectionRulesAssignments listPolicyDefault modify modifyDefaultSetting modifyFirewallRules modifyIntegrityMonitoringRules modifyIntrusionPreventionApplication modifyIntrusionPreventionRules modifyLogInspection modifyPolicyDefault modifyPolicySetting removeIntegrityMonitoringRuleAssignments resetFirewallRules resetIntrusionPreventionApplication resetIntrusionPreventionRules resetLogInspection resetPolicySetting search setIntegrityMonitoringRuleAssignments " "${COMP_WORDS[3]}"))
		 return
		;;
	reporttemplates)
		 COMPREPLY=($(compgen -W "describe list search " "${COMP_WORDS[3]}"))
		 return
		;;
	scheduledtasks)
		 COMPREPLY=($(compgen -W "create delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	scripts)
		 COMPREPLY=($(compgen -W "list " "${COMP_WORDS[3]}"))
		 return
		;;
	systemsettings)
		 COMPREPLY=($(compgen -W "delete describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
	tenants)
		 COMPREPLY=($(compgen -W "create createAPIKey delete describe list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
	firewall)
		 COMPREPLY=($(compgen -W "create createContext createInterfaceType createStatefulConfiguration createiplists createmaclists createportlists delete deleteContext deleteIPList deleteInterfaceType deleteStatefulConfiguration deletemacList deleteportList describe describeContext describeIPList describeInterfaceType describeStatefulConfiguration describemacList describeportList list listContexts listIPLists listInterfaceTypes listMacLists listPortLists listStatefulConfigurations modify modifyContext modifyIPList modifyInterfaceType modifyStatefulConfiguration modifymacList modifyportList search searchContexts searchIPLists searchInterfaceTypes searchStatefulConfigurations searchmacLists searchportLists " "${COMP_WORDS[3]}"))
		 return
		;;
	gcpconnector)
		 COMPREPLY=($(compgen -W "create createAction delete describe describeAction list modify search " "${COMP_WORDS[3]}"))
		 return
		;;
esac
}
_cloudone_completions_ds_classes()
{
COMPREPLY=($(compgen -W "apikeys apiusagemetrics administrators agentdeploymentscripts antimalware applicationcontrol certificates computergroups computers contacts eventbasedtasks integritymonitoring intrusionprevention loginspectionrules policies reporttemplates scheduledtasks scripts systemsettings tenants firewall gcpconnector " "${COMP_WORDS[2]}"))
return
}
_cloudone_completions_cs_functions()
{
case "${COMP_WORDS[COMP_CWORD-1]}" in 
	contentrules)
		 COMPREPLY=($(compgen -W "createContentRuleset createContentRulesetCollection deleteContentRuleset deleteContentRulesetCollection describeContentRuleset describeContentRulesetCollection listContentRuleset listContentRulesetCollections modifyContentRuleset modifyContentRulesetCollection " "${COMP_WORDS[3]}"))
		 return
		;;
	identityproviders)
		 COMPREPLY=($(compgen -W "createSAML deleteSAML describeSAML listSAML modifySAML " "${COMP_WORDS[3]}"))
		 return
		;;
	license)
		 COMPREPLY=($(compgen -W "describe " "${COMP_WORDS[3]}"))
		 return
		;;
	overrides)
		 COMPREPLY=($(compgen -W "createChecklistFindingOverride createContentFindingOverride createVulnerabilityFindingOverride deleteChecklistFindingOverride deleteContentFindingOverride deleteVulnerabilityFindingOverride describeChecklistFindingOverride describeContentFindingOverride describeVulnerabilityFindingOverride listChecklistFindingOverrides listContentFindingOverrides listVulnerabilityFindingOverrides modifyChecklistFindingOverride modifyContentFindingOverride modifyVulnerabilityFindingOverride " "${COMP_WORDS[3]}"))
		 return
		;;
	registries)
		 COMPREPLY=($(compgen -W "create delete describe describeRegistryDashboard describeRegistryImage list listRegistryImages modify " "${COMP_WORDS[3]}"))
		 return
		;;
	roles)
		 COMPREPLY=($(compgen -W "create deleteSession describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
	scans)
		 COMPREPLY=($(compgen -W "cancel create describe describeConfigurationChecklist describeScanMetrics list listConfigurationChecklistProfileRules listLayerContentFindingsScans listLayerMalwareFindingsScans listLayerVulnerabilityFindingsScans listScanChecklist " "${COMP_WORDS[3]}"))
		 return
		;;
	sessions)
		 COMPREPLY=($(compgen -W "create delete describe list refresh " "${COMP_WORDS[3]}"))
		 return
		;;
	users)
		 COMPREPLY=($(compgen -W "changePassword create delete describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
	webhook)
		 COMPREPLY=($(compgen -W "create delete describe list modify " "${COMP_WORDS[3]}"))
		 return
		;;
esac
}
_cloudone_completions_cs_classes()
{
COMPREPLY=($(compgen -W "contentrules identityproviders license overrides registries roles scans sessions users webhook " "${COMP_WORDS[2]}"))
return
}


_cloudone_completions()
{
  local cloudone_services="deepsecurity ds smartcheck sc workloadsecurity ws containersecurity cs"
  COMPREPLY=()
  if [ "${#COMP_WORDS[@]}" == "2" ]; then
    COMPREPLY=($(compgen -W "${cloudone_services}" "${COMP_WORDS[1]}"))
    return
  fi
  service=${COMP_WORDS[1]}
  case ${service} in 
    workloadsecurity | ws | ds)
        service="deepsecurity"
        ;;
    containersecurity | cs | sc)
        service="smartcheck"
        ;;
    esac
    
  if [ "${#COMP_WORDS[@]}" == "3" ]; then

   # case ${COMP_WORDS[1]} in 
   case ${service} in 
        deepsecurity)
             _cloudone_completions_ds_classes
             return
        ;;
        smartcheck)
            _cloudone_completions_cs_classes
            return
        ;;
    esac
    return
  fi
    if [ "${#COMP_WORDS[@]}" == "4" ]; then

    case ${COMP_WORDS[1]} in 
        deepsecurity)
            _cloudone_completions_ds_functions
            return
        ;;
        smartcheck)
            _cloudone_completions_cs_functions
            return
        ;;
    esac 
    return
  fi

}

complete -F _thus_completions thus
